using System;
using System.Collections.Generic;
using UnityEngine;
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Sensor;

/// <summary>
/// Lắng nghe chuỗi góc khớp từ MoveIt (/joint_states) và điều khiển 
/// 6 khớp xoay của cánh tay UR10e chuyển động mượt mà trong Unity bằng ArticulationBody.
/// Tự động loại bỏ Controller mặc định của URDF Importer (thủ phạm set forceLimit = 0),
/// khóa cứng đế robot (immovable) và triệt tiêu võng do trọng lực.
/// Dự án: UC8 - Robotic Arm Conveyor Pick-and-Place
/// Tuần: Week 04 (R4 - Trajectory Execution)
/// </summary>
public class UR10eController : MonoBehaviour
{
    [Header("ROS Topic Configuration")]
    [SerializeField] private string jointStatesTopic = "/joint_states";

    [Header("PhysX Joint Drive Parameters")]
    [SerializeField] private float stiffness = 50000f;
    [SerializeField] private float damping = 1000f;
    [SerializeField] private float forceLimit = 10000f;

    // 6 tên khớp chuẩn mực của UR10e theo chuẩn ROS URDF
    private readonly string[] rosJointNames =
    {
        "shoulder_pan_joint",
        "shoulder_lift_joint",
        "elbow_joint",
        "wrist_1_joint",
        "wrist_2_joint",
        "wrist_3_joint"
    };

    // Tên các GameObject Link tương ứng trong cây phân cấp của robot
    private readonly string[] linkNames =
    {
        "shoulder_link",
        "upper_arm_link",
        "forearm_link",
        "wrist_1_link",
        "wrist_2_link",
        "wrist_3_link"
    };

    private readonly Dictionary<string, int> jointNameToIndex = new Dictionary<string, int>();
    private ArticulationBody[] joints;
    private float[] targetAnglesDegrees;
    private bool isInitialized = false;
    private bool hasReceivedFirstMsg = false;

    // Góc chờ công nghiệp tối ưu cho Phương án 1:
    // Cánh tay co cao thanh thoát, cổ tay luôn chĩa thẳng đứng 90 độ xuống mặt băng chuyền ngay tại đỉnh trạm gắp
    private readonly float[] defaultStandbyAnglesDegrees = { 16.9f, -84.6f, -121.9f, -63.2f, 90.0f, 30.3f };

    private void Awake()
    {
        // QUAN TRỌNG: Xóa Controller mặc định của URDF-Importer (thủ phạm set forceLimit = 0 làm liệt robot)
        MonoBehaviour[] allScripts = GetComponentsInChildren<MonoBehaviour>(true);
        foreach (MonoBehaviour s in allScripts)
        {
            if (s != null && s != this && (s.GetType().Name == "Controller" || s.GetType().Name == "JointControl" || s.GetType().Name == "FKRobot"))
            {
                Debug.Log($"[UR10eController] Removed conflicting script: {s.GetType().Name}");
                DestroyImmediate(s);
            }
        }

        // Đồng bộ vị trí các thiết bị ngoại vi theo Phương án 1 (Front Pick - Flanking Bins)
        EnsureWorkcellLayout();

        // Tự động gắn bộ điều khiển góc máy điện ảnh cho Main Camera
        Camera mainCam = Camera.main;
        if (mainCam != null && mainCam.GetComponent<WorkcellCameraController>() == null)
        {
            mainCam.gameObject.AddComponent<WorkcellCameraController>();
        }
    }

    private void EnsureWorkcellLayout()
    {
        GameObject table = GameObject.Find("Table");
        if (table != null)
        {
            table.transform.position = new Vector3(0f, -0.05f, 0f);
            table.transform.localScale = new Vector3(4.0f, 0.1f, 2.0f);
        }

        GameObject conveyor = GameObject.Find("Conveyor");
        if (conveyor != null)
        {
            conveyor.transform.position = new Vector3(0f, 0.1f, -0.6f);
            conveyor.transform.localScale = new Vector3(3.6f, 0.1f, 0.35f);
        }

        GameObject spawner = GameObject.Find("ObjectSpawner");
        if (spawner != null) spawner.transform.position = new Vector3(-1.5f, 0.35f, -0.6f);

        GameObject sensor = GameObject.Find("PickZoneSensor");
        if (sensor != null)
        {
            sensor.transform.localPosition = new Vector3(0f, 1f, 0f);
            sensor.transform.localScale = new Vector3(0.25f, 1f, 1f);
        }

        GameObject binRed = GameObject.Find("Bin_Red");
        if (binRed != null)
        {
            binRed.transform.position = new Vector3(-0.55f, 0.01f, -0.1f);
            binRed.transform.localScale = new Vector3(1.35f, 1.25f, 1.35f);
        }

        GameObject binYellow = GameObject.Find("Bin_Yellow");
        if (binYellow != null)
        {
            binYellow.transform.position = new Vector3(0.55f, 0.01f, -0.1f);
            binYellow.transform.localScale = new Vector3(1.35f, 1.25f, 1.35f);
        }

        GameObject binBlue = GameObject.Find("Bin_Blue");
        if (binBlue != null)
        {
            binBlue.transform.position = new Vector3(0f, 0.01f, 0.5f);
            binBlue.transform.localScale = new Vector3(1.35f, 1.25f, 1.35f);
        }

        // Tự động tạo và đồng bộ vật cản tĩnh (Static Obstacle Barrier - Requirement R8)
        EnsureStaticBarrier();

        // Tự động tạo và cập nhật các quả cầu Waypoint Visual Markers tại vị trí mới
        EnsureWaypointMarkers();

        Debug.Log("[UR10eController] Workcell layout, Static Barrier Wall (R8), and Waypoint visual markers synchronized (Option 1)!");
    }

    private void EnsureStaticBarrier()
    {
        GameObject barrier = GameObject.Find("Static_Barrier_Wall");
        if (barrier == null)
        {
            barrier = GameObject.CreatePrimitive(PrimitiveType.Cube);
            barrier.name = "Static_Barrier_Wall";

            Material mat = new Material(Shader.Find("Standard") ?? Shader.Find("Universal Render Pipeline/Lit") ?? Shader.Find("Diffuse"));
            mat.color = new Color(0.95f, 0.55f, 0.05f, 1.0f); // Safety Amber Orange
            mat.EnableKeyword("_EMISSION");
            mat.SetColor("_EmissionColor", new Color(0.35f, 0.20f, 0.02f));
            MeshRenderer mr = barrier.GetComponent<MeshRenderer>();
            if (mr != null) mr.material = mat;
        }

        // Tọa độ Unity: (-0.28m, 0.18m, -0.38m) khớp 100% với ROS base_link (X=-0.38m, Y=0.28m, Z=0.18m)
        barrier.transform.position = new Vector3(-0.28f, 0.18f, -0.38f);
        barrier.transform.localScale = new Vector3(0.30f, 0.36f, 0.12f);
        barrier.transform.rotation = Quaternion.identity;

        BoxCollider col = barrier.GetComponent<BoxCollider>();
        if (col != null) col.isTrigger = false;
    }

    private void EnsureWaypointMarkers()
    {
        GameObject parentObj = GameObject.Find("Waypoint_Visual_Markers");
        if (parentObj == null)
        {
            parentObj = new GameObject("Waypoint_Visual_Markers");
        }

        CreateOrUpdateMarker(parentObj.transform, "Marker_IDLE / READY", new Vector3(0f, 0.42f, -0.60f), new Color(0.2f, 0.95f, 0.3f));
        CreateOrUpdateMarker(parentObj.transform, "Marker_PICK ZONE",    new Vector3(0f, 0.18f, -0.60f), new Color(0.1f, 0.85f, 0.95f));
        CreateOrUpdateMarker(parentObj.transform, "Marker_RED BIN",      new Vector3(-0.55f, 0.35f, -0.10f), new Color(0.95f, 0.2f, 0.2f));
        CreateOrUpdateMarker(parentObj.transform, "Marker_YELLOW BIN",   new Vector3(0.55f, 0.35f, -0.10f), new Color(0.98f, 0.88f, 0.15f));
        CreateOrUpdateMarker(parentObj.transform, "Marker_BLUE BIN",     new Vector3(0f, 0.35f, 0.50f), new Color(0.2f, 0.5f, 1.0f));
    }

    private void CreateOrUpdateMarker(Transform parent, string name, Vector3 pos, Color color)
    {
        Transform child = parent.Find(name);
        GameObject markerObj = child != null ? child.gameObject : null;

        if (markerObj == null)
        {
            markerObj = GameObject.CreatePrimitive(PrimitiveType.Sphere);
            markerObj.name = name;
            markerObj.transform.SetParent(parent, false);
            markerObj.transform.localScale = Vector3.one * 0.06f; // Đường kính 6cm nhỏ gọn

            // Tắt Collider để tuyệt đối không cản trở chuyển động vật lý
            Collider col = markerObj.GetComponent<Collider>();
            if (col != null) col.enabled = false;

            Material mat = new Material(Shader.Find("Standard"));
            mat.color = color;
            mat.EnableKeyword("_EMISSION");
            mat.SetColor("_EmissionColor", color * 0.5f);
            MeshRenderer mr = markerObj.GetComponent<MeshRenderer>();
            if (mr != null) mr.material = mat;
        }

        markerObj.transform.position = pos;
    }

    private void Start()
    {
        joints = new ArticulationBody[6];
        targetAnglesDegrees = new float[6];

        // 1. Tìm tất cả ArticulationBody và cố định đế robot (base_link)
        ArticulationBody[] allBodies = GetComponentsInChildren<ArticulationBody>(true);
        foreach (ArticulationBody body in allBodies)
        {
            if (body.isRoot || body.name == "base_link" || body.name == "ur10e" || body.name == "ur10e_robot" || body.name == "base_link_inertia" || body.name == "base")
            {
                body.immovable = true;
                Debug.Log($"[UR10eController] Locked robot base (immovable = true): {body.name}");
            }
        }

        // 2. Cấu hình 6 khớp xoay của cánh tay UR10e
        for (int i = 0; i < linkNames.Length; i++)
        {
            foreach (ArticulationBody body in allBodies)
            {
                if (body.name == linkNames[i])
                {
                    joints[i] = body;
                    break;
                }
            }

            if (joints[i] == null)
            {
                Debug.LogWarning($"[UR10eController] ArticulationBody not found for link: {linkNames[i]}");
                continue;
            }

            jointNameToIndex[rosJointNames[i]] = i;

            // Khóa trọng lực để cánh tay không bị trĩu/rụng do trọng trường PhysX
            joints[i].useGravity = false;

            // Khởi tạo tư thế Standby công nghiệp thanh thoát ngay từ frame đầu tiên
            float initialAngle = defaultStandbyAnglesDegrees[i];
            targetAnglesDegrees[i] = initialAngle;

            if (joints[i].dofCount > 0)
            {
                joints[i].jointPosition = new ArticulationReducedSpace(initialAngle * Mathf.Deg2Rad);
            }

            // Cấu hình thông số PID Drive giữ vị trí cực kỳ vững chãi và lực kéo mạnh mẽ
            ArticulationDrive drive = joints[i].xDrive;
            drive.stiffness = stiffness;
            drive.damping = damping;
            drive.forceLimit = forceLimit;
            drive.target = initialAngle;
            joints[i].xDrive = drive;
        }

        // 3. Bỏ qua va chạm vật lý giữa robot và các bề mặt tĩnh (Table, Conveyor) để chống kẹt/đập bàn
        string[] staticEnvNames = { "Table", "Conveyor" };
        Collider[] robotColliders = GetComponentsInChildren<Collider>(true);
        foreach (string envName in staticEnvNames)
        {
            GameObject envObj = GameObject.Find(envName);
            if (envObj != null)
            {
                Collider[] envColliders = envObj.GetComponentsInChildren<Collider>(true);
                foreach (var rc in robotColliders)
                {
                    foreach (var ec in envColliders)
                    {
                        Physics.IgnoreCollision(rc, ec, true);
                    }
                }
            }
        }
        Debug.Log("[UR10eController] Configured collision avoidance: Ignored collisions between robot arm and Table/Conveyor.");

        // Đăng ký Subscriber nhận lệnh từ MoveIt qua ROS-TCP
        ROSConnection.GetOrCreateInstance().Subscribe<JointStateMsg>(jointStatesTopic, OnReceiveJointState);
        isInitialized = true;

        Debug.Log($"[UR10eController] Successfully initialized 6 UR10e joints (forceLimit={forceLimit}). Ready to receive {jointStatesTopic}");
    }

    private void OnReceiveJointState(JointStateMsg msg)
    {
        if (!isInitialized || msg == null || msg.name == null || msg.position == null)
            return;

        int count = Math.Min(msg.name.Length, msg.position.Length);

        // Khớp góc xoay theo tên khớp (không phụ thuộc vào thứ tự trong message)
        for (int n = 0; n < count; n++)
        {
            if (jointNameToIndex.TryGetValue(msg.name[n], out int jointIndex))
            {
                double angleRadian = msg.position[n];
                if (!double.IsNaN(angleRadian) && !double.IsInfinity(angleRadian))
                {
                    // Chuyển từ Radian (ROS) sang Độ (Unity)
                    targetAnglesDegrees[jointIndex] = (float)(angleRadian * Mathf.Rad2Deg);
                }
            }
        }

        if (!hasReceivedFirstMsg)
        {
            Debug.Log($"[UR10eController] Received /joint_states stream from ROS! Joint shoulder_pan: {targetAnglesDegrees[0]:F1} deg");
            hasReceivedFirstMsg = true;
        }
    }

    private void FixedUpdate()
    {
        if (!isInitialized) return;

        // Cập nhật mục tiêu chuyển động của từng khớp vào vật lý PhysX
        for (int i = 0; i < joints.Length; i++)
        {
            if (joints[i] != null)
            {
                ArticulationDrive drive = joints[i].xDrive;
                drive.target = targetAnglesDegrees[i];
                joints[i].xDrive = drive;
            }
        }
    }
}
