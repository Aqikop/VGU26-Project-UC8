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

        // Tự động tạo và đồng bộ Tủ điều khiển UR Control Box (Góc thao tác kỹ sư - Requirement R8)
        EnsureURControlBox();

        // Tự động tạo và đồng bộ Cột rèm quang an toàn Safety Light Curtain (Chặn giữa Băng tải và Thùng Đỏ - Requirement R8)
        EnsureSafetyLightCurtain();

        // Tự động tạo và cập nhật các quả cầu Waypoint Visual Markers tại vị trí mới
        EnsureWaypointMarkers();

        Debug.Log("[UR10eController] Workcell layout, UR Control Box, Safety Light Curtain (R8), and Waypoint visual markers synchronized (Option 1)!");
    }

    private void EnsureURControlBox()
    {
        // Xóa vật cản cũ nếu có
        GameObject oldWall = GameObject.Find("Static_Barrier_Wall");
        if (oldWall != null) DestroyImmediate(oldWall);

        GameObject boxRoot = GameObject.Find("UR_Control_Box");
        if (boxRoot == null)
        {
            boxRoot = new GameObject("UR_Control_Box");

            // Base Shader
            Shader stdShader = Shader.Find("Standard") ?? Shader.Find("Universal Render Pipeline/Lit") ?? Shader.Find("Diffuse");

            // Material: Thân tủ kim loại công nghiệp (Industrial Slate Metallic)
            Material cabinetMat = new Material(stdShader);
            cabinetMat.color = new Color(0.18f, 0.20f, 0.24f);
            if (cabinetMat.HasProperty("_Metallic")) cabinetMat.SetFloat("_Metallic", 0.7f);
            if (cabinetMat.HasProperty("_Glossiness")) cabinetMat.SetFloat("_Glossiness", 0.6f);

            // Material: Mặt trước panel nhôm xước (Brushed Aluminum)
            Material panelMat = new Material(stdShader);
            panelMat.color = new Color(0.38f, 0.42f, 0.48f);
            if (panelMat.HasProperty("_Metallic")) panelMat.SetFloat("_Metallic", 0.5f);

            // Material: Nút E-Stop vàng & đỏ
            Material yellowMat = new Material(stdShader);
            yellowMat.color = new Color(0.98f, 0.82f, 0.05f);
            Material redMat = new Material(stdShader);
            redMat.color = new Color(0.90f, 0.12f, 0.12f);

            // Material: Đèn LED báo nguồn xanh lục phát sáng
            Material greenLedMat = new Material(stdShader);
            greenLedMat.color = new Color(0.1f, 0.95f, 0.3f);
            greenLedMat.EnableKeyword("_EMISSION");
            greenLedMat.SetColor("_EmissionColor", new Color(0.1f, 0.95f, 0.3f) * 0.8f);

            // Material: Màn hình Teach Pendant (Dark Glass)
            Material screenMat = new Material(stdShader);
            screenMat.color = new Color(0.08f, 0.10f, 0.13f);
            if (screenMat.HasProperty("_Glossiness")) screenMat.SetFloat("_Glossiness", 0.9f);

            // A. Thân tủ chính (Cabinet Body: 32cm x 38cm x 24cm)
            GameObject body = GameObject.CreatePrimitive(PrimitiveType.Cube);
            body.name = "Cabinet_Body";
            body.transform.SetParent(boxRoot.transform, false);
            body.transform.localPosition = new Vector3(0f, 0f, 0f);
            body.transform.localScale = new Vector3(0.32f, 0.38f, 0.24f);
            body.GetComponent<MeshRenderer>().material = cabinetMat;
            DestroyImmediate(body.GetComponent<Collider>());

            // B. Mặt Panel trước (Front Panel Inset)
            GameObject panel = GameObject.CreatePrimitive(PrimitiveType.Cube);
            panel.name = "Front_Panel";
            panel.transform.SetParent(boxRoot.transform, false);
            panel.transform.localPosition = new Vector3(0f, 0f, -0.121f);
            panel.transform.localScale = new Vector3(0.28f, 0.34f, 0.008f);
            panel.GetComponent<MeshRenderer>().material = panelMat;
            DestroyImmediate(panel.GetComponent<Collider>());

            // C. Nút dừng khẩn cấp E-Stop (Vòng vàng + Nấm đỏ)
            GameObject eStopBase = GameObject.CreatePrimitive(PrimitiveType.Cylinder);
            eStopBase.name = "EStop_Base";
            eStopBase.transform.SetParent(boxRoot.transform, false);
            eStopBase.transform.localPosition = new Vector3(0.09f, 0.10f, -0.128f);
            eStopBase.transform.localScale = new Vector3(0.045f, 0.005f, 0.045f);
            eStopBase.transform.localRotation = Quaternion.Euler(90f, 0f, 0f);
            eStopBase.GetComponent<MeshRenderer>().material = yellowMat;
            DestroyImmediate(eStopBase.GetComponent<Collider>());

            GameObject eStopCap = GameObject.CreatePrimitive(PrimitiveType.Sphere);
            eStopCap.name = "EStop_Mushroom";
            eStopCap.transform.SetParent(boxRoot.transform, false);
            eStopCap.transform.localPosition = new Vector3(0.09f, 0.10f, -0.138f);
            eStopCap.transform.localScale = new Vector3(0.038f, 0.022f, 0.038f);
            eStopCap.GetComponent<MeshRenderer>().material = redMat;
            DestroyImmediate(eStopCap.GetComponent<Collider>());

            // D. Đèn LED báo trạng thái nguồn
            GameObject led = GameObject.CreatePrimitive(PrimitiveType.Sphere);
            led.name = "Power_LED";
            led.transform.SetParent(boxRoot.transform, false);
            led.transform.localPosition = new Vector3(-0.10f, 0.12f, -0.128f);
            led.transform.localScale = new Vector3(0.014f, 0.014f, 0.014f);
            led.GetComponent<MeshRenderer>().material = greenLedMat;
            DestroyImmediate(led.GetComponent<Collider>());

            // E. Cột đỡ Teach Pendant (Pendant Stand)
            GameObject pole = GameObject.CreatePrimitive(PrimitiveType.Cylinder);
            pole.name = "Pendant_Stand_Pole";
            pole.transform.SetParent(boxRoot.transform, false);
            pole.transform.localPosition = new Vector3(-0.11f, 0.22f, 0f);
            pole.transform.localScale = new Vector3(0.018f, 0.08f, 0.018f);
            pole.GetComponent<MeshRenderer>().material = cabinetMat;
            DestroyImmediate(pole.GetComponent<Collider>());

            // F. Màn hình Teach Pendant (Tablet cảm ứng nghiêng 25 độ hướng ra ngoài)
            GameObject pendant = GameObject.CreatePrimitive(PrimitiveType.Cube);
            pendant.name = "Teach_Pendant_Screen";
            pendant.transform.SetParent(boxRoot.transform, false);
            pendant.transform.localPosition = new Vector3(-0.11f, 0.28f, -0.04f);
            pendant.transform.localScale = new Vector3(0.20f, 0.14f, 0.016f);
            pendant.transform.localRotation = Quaternion.Euler(-25f, 0f, 0f);
            pendant.GetComponent<MeshRenderer>().material = screenMat;
            DestroyImmediate(pendant.GetComponent<Collider>());

            // G. BoxCollider bao trọn toàn bộ tủ và màn hình để phát hiện va chạm vật lý
            BoxCollider col = boxRoot.AddComponent<BoxCollider>();
            col.center = new Vector3(0f, 0.02f, 0f);
            col.size = new Vector3(0.32f, 0.42f, 0.24f);
            col.isTrigger = false;
        }

        // Tọa độ Unity: (-0.48m, 0.19m, 0.35m) ở góc vuông phía sau giữa Thùng Đỏ và Thùng Xanh (chuẩn vị trí kỹ sư đứng vận hành)
        boxRoot.transform.position = new Vector3(-0.48f, 0.19f, 0.35f);
        boxRoot.transform.rotation = Quaternion.Euler(0f, 30f, 0f);
    }

    private void EnsureSafetyLightCurtain()
    {
        GameObject curtainRoot = GameObject.Find("Safety_Light_Curtain");
        if (curtainRoot == null)
        {
            curtainRoot = new GameObject("Safety_Light_Curtain");

            Shader stdShader = Shader.Find("Standard") ?? Shader.Find("Universal Render Pipeline/Lit") ?? Shader.Find("Diffuse");

            // Material: Thân nhôm vàng an toàn công nghiệp (Industrial Safety Amber/Yellow)
            Material yellowMat = new Material(stdShader);
            yellowMat.color = new Color(0.96f, 0.72f, 0.05f);
            if (yellowMat.HasProperty("_Metallic")) yellowMat.SetFloat("_Metallic", 0.3f);
            if (yellowMat.HasProperty("_Glossiness")) yellowMat.SetFloat("_Glossiness", 0.5f);

            // Material: Chân đế kim loại & nắp chụp màu đen nhám (Matte Black)
            Material blackMat = new Material(stdShader);
            blackMat.color = new Color(0.12f, 0.13f, 0.15f);

            // Material: Kính lọc quang học mặt trước (Dark Smoked Acrylic)
            Material lensMat = new Material(stdShader);
            lensMat.color = new Color(0.04f, 0.04f, 0.06f);
            if (lensMat.HasProperty("_Glossiness")) lensMat.SetFloat("_Glossiness", 0.95f);

            // Material: Dải LED cảm biến quang phát sáng (Optical Emitter Status)
            Material emitterLedMat = new Material(stdShader);
            emitterLedMat.color = new Color(1.0f, 0.2f, 0.2f); // Đỏ cảnh báo rèm quang
            emitterLedMat.EnableKeyword("_EMISSION");
            emitterLedMat.SetColor("_EmissionColor", new Color(1.0f, 0.2f, 0.2f) * 0.7f);

            // A. Thân cột nhôm định hình chính (Column: 7cm x 36cm x 7cm)
            GameObject column = GameObject.CreatePrimitive(PrimitiveType.Cube);
            column.name = "Curtain_Column";
            column.transform.SetParent(curtainRoot.transform, false);
            column.transform.localPosition = Vector3.zero;
            column.transform.localScale = new Vector3(0.07f, 0.36f, 0.07f);
            column.GetComponent<MeshRenderer>().material = yellowMat;
            DestroyImmediate(column.GetComponent<Collider>());

            // B. Chân đế bắt bu-lông xuống mặt bàn (Base Flange)
            GameObject flange = GameObject.CreatePrimitive(PrimitiveType.Cube);
            flange.name = "Base_Flange";
            flange.transform.SetParent(curtainRoot.transform, false);
            flange.transform.localPosition = new Vector3(0f, -0.175f, 0f);
            flange.transform.localScale = new Vector3(0.12f, 0.01f, 0.12f);
            flange.GetComponent<MeshRenderer>().material = blackMat;
            DestroyImmediate(flange.GetComponent<Collider>());

            // C. Nắp chụp đầu cột (Top Cap)
            GameObject topCap = GameObject.CreatePrimitive(PrimitiveType.Cube);
            topCap.name = "Top_Cap";
            topCap.transform.SetParent(curtainRoot.transform, false);
            topCap.transform.localPosition = new Vector3(0f, 0.182f, 0f);
            topCap.transform.localScale = new Vector3(0.075f, 0.012f, 0.075f);
            topCap.GetComponent<MeshRenderer>().material = blackMat;
            DestroyImmediate(topCap.GetComponent<Collider>());

            // D. Dải kính quang học mặt trước hướng về phía băng tải (Optical Lens Window)
            GameObject lens = GameObject.CreatePrimitive(PrimitiveType.Cube);
            lens.name = "Optical_Lens_Window";
            lens.transform.SetParent(curtainRoot.transform, false);
            lens.transform.localPosition = new Vector3(0f, 0f, -0.036f);
            lens.transform.localScale = new Vector3(0.045f, 0.32f, 0.005f);
            lens.GetComponent<MeshRenderer>().material = lensMat;
            DestroyImmediate(lens.GetComponent<Collider>());

            // E. Dải mắt LED cảm biến quang hồng ngoại (Status Emitter Strip)
            GameObject emitter = GameObject.CreatePrimitive(PrimitiveType.Cube);
            emitter.name = "Emitter_Light_Strip";
            emitter.transform.SetParent(curtainRoot.transform, false);
            emitter.transform.localPosition = new Vector3(0f, 0f, -0.038f);
            emitter.transform.localScale = new Vector3(0.015f, 0.28f, 0.004f);
            emitter.GetComponent<MeshRenderer>().material = emitterLedMat;
            DestroyImmediate(emitter.GetComponent<Collider>());

            // F. BoxCollider bao bọc toàn bộ cột cảm biến để phát hiện va chạm vật lý
            BoxCollider col = curtainRoot.AddComponent<BoxCollider>();
            col.center = Vector3.zero;
            col.size = new Vector3(0.10f, 0.36f, 0.10f);
            col.isTrigger = false;
        }

        // Tọa độ Unity: (-0.30m, 0.18m, -0.38m) nằm giữa băng tải và Thùng Đỏ, khớp 100% với ROS (X=-0.38m, Y=0.30m, Z=0.18m)
        curtainRoot.transform.position = new Vector3(-0.30f, 0.18f, -0.38f);
        curtainRoot.transform.rotation = Quaternion.identity;
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
