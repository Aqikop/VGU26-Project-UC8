using UnityEngine;
using Unity.Robotics.ROSTCPConnector;
using RosMessageTypes.Std;

/// <summary>
/// Quản lý cơ chế Kẹp / Nhả vật thể bằng Attach Logic (Parenting) theo chỉ đạo của Giảng viên.
/// Dự án: UC8 - Robotic Arm Conveyor Pick-and-Place
/// Tuần: Week 04 (R4 - Grasping Module)
/// </summary>
public class GripperController : MonoBehaviour
{
    [Header("ROS Topics Configuration")]
    [SerializeField] private string commandTopic = "/ur10e/gripper_command";
    [SerializeField] private string statusTopic = "/ur10e/gripper_status";

    [Header("Attach Logic Configuration")]
    [Tooltip("Search radius around end-effector for target cube (meters)")]
    [SerializeField] private float graspRadius = 0.18f;

    [Tooltip("Transform of tool0 end-effector. If left empty, uses this GameObject")]
    [SerializeField] private Transform attachPoint;

    private ROSConnection ros;
    private GameObject attachedObject = null;
    private bool isHolding = false;

    private void Awake()
    {
        ResolveAttachPoint();
    }

    private void Start()
    {
        ResolveAttachPoint();

        ros = ROSConnection.GetOrCreateInstance();
        ros.Subscribe<BoolMsg>(commandTopic, OnReceiveGripperCommand);
        ros.RegisterPublisher<BoolMsg>(statusTopic);

        Debug.Log($"[Gripper] Initialized Attach Logic Gripper at {attachPoint.name}, listening to {commandTopic}");
    }

    private void ResolveAttachPoint()
    {
        if (attachPoint == null)
        {
            Transform root = transform.root;
            attachPoint = FindDeepChild(root, "tool0");
            if (attachPoint == null)
            {
                attachPoint = FindDeepChild(root, "wrist_3_link");
            }
            if (attachPoint == null)
            {
                attachPoint = transform;
            }
            Debug.Log($"[GripperController] Attach point resolved to: {attachPoint.name}");
        }
    }

    private void OnReceiveGripperCommand(BoolMsg msg)
    {
        if (msg.data)
        {
            // Lệnh KẸP (GRASP)
            GraspNearestObject();
        }
        else
        {
            // Lệnh NHẢ (RELEASE)
            ReleaseObject();
        }

        // Báo cáo trạng thái kẹp về ROS
        ros.Publish(statusTopic, new BoolMsg { data = isHolding });
    }

    public void GraspNearestObject()
    {
        if (isHolding) return;

        ResolveAttachPoint();

        // Tìm tất cả Collider trong bán kính đầu kẹp
        Collider[] hits = Physics.OverlapSphere(attachPoint.position, graspRadius);
        GameObject bestTarget = null;
        float minDistance = float.MaxValue;

        foreach (Collider hit in hits)
        {
            SortableObject sortable = hit.GetComponentInParent<SortableObject>();
            if (sortable != null && !sortable.isSorted)
            {
                float dist = Vector3.Distance(attachPoint.position, sortable.transform.position);
                if (dist < minDistance)
                {
                    minDistance = dist;
                    bestTarget = sortable.gameObject;
                }
            }
        }

        if (bestTarget != null)
        {
            attachedObject = bestTarget;
            Rigidbody rb = attachedObject.GetComponent<Rigidbody>();
            if (rb != null)
            {
                rb.velocity = Vector3.zero;
                rb.angularVelocity = Vector3.zero;
                rb.isKinematic = true; // Khóa vật lý để hộp di chuyển tuyệt đối theo cánh tay
            }

            // Tạm thời chuyển sang Trigger để chống va chạm đâm xuyên mặt bàn/băng chuyền trong lúc vận chuyển
            Collider col = attachedObject.GetComponent<Collider>();
            if (col != null)
            {
                col.isTrigger = true;
            }

            // Snap khối hộp dính khít sát đầu gắp tool0 (hộp 6cm => tâm hộp nằm dưới mặt tool0 đúng 3cm)
            attachedObject.transform.position = attachPoint.position - new Vector3(0f, 0.03f, 0f);
            attachedObject.transform.rotation = Quaternion.identity;
            attachedObject.transform.SetParent(attachPoint, true);
            isHolding = true;

            Debug.Log($"[Gripper] GRASP SUCCESS: Attached and snapped {attachedObject.name} to {attachPoint.name}!");
        }
        else
        {
            Debug.LogWarning($"[Gripper] GRASP FAILED: No target cube found within radius {graspRadius} m!");
            isHolding = false;
        }
    }

    public void ReleaseObject()
    {
        if (!isHolding || attachedObject == null) return;

        // Detach object from gripper
        attachedObject.transform.SetParent(null, true);

        // Ensure object is not below bin floor
        Vector3 curPos = attachedObject.transform.position;
        if (curPos.y < 0.05f)
        {
            curPos.y = 0.05f;
            attachedObject.transform.position = curPos;
        }

        // Restore realistic physics collider
        Collider col = attachedObject.GetComponent<Collider>();
        if (col != null)
        {
            col.isTrigger = false;
        }

        // Restore gravity for free fall into bin
        Rigidbody rb = attachedObject.GetComponent<Rigidbody>();
        if (rb != null)
        {
            rb.velocity = Vector3.zero;
            rb.angularVelocity = Vector3.zero;
            rb.isKinematic = false;
            rb.WakeUp();
        }

        SortableObject sortable = attachedObject.GetComponent<SortableObject>();
        if (sortable != null)
        {
            sortable.isSorted = true;
        }

        Debug.Log($"[Gripper] RELEASE SUCCESS: Released {attachedObject.name} into sorting bin!");

        // Khởi động lại băng chuyền và dọn cảm biến vùng gắp
        PickZoneSensor sensor = FindObjectOfType<PickZoneSensor>();
        if (sensor != null)
        {
            sensor.ForceResume();
        }
        else
        {
            ConveyorController conveyor = FindObjectOfType<ConveyorController>();
            if (conveyor != null) conveyor.StartConveyor();
        }

        // Kích hoạt Spawner sinh tiếp khối hộp mới sau khi đã phân loại xong hộp này
        RandomObjectSpawner spawner = FindObjectOfType<RandomObjectSpawner>();
        if (spawner != null)
        {
            spawner.TriggerNextSpawn(0.5f);
        }

        // Tự hủy khối hộp sau 15 giây để chống tràn thùng
        Destroy(attachedObject, 15.0f);

        attachedObject = null;
        isHolding = false;
    }

    private Transform FindDeepChild(Transform parent, string childName)
    {
        foreach (Transform child in parent)
        {
            if (child.name.Equals(childName, System.StringComparison.OrdinalIgnoreCase))
                return child;
            Transform result = FindDeepChild(child, childName);
            if (result != null)
                return result;
        }
        return null;
    }

    private void OnDrawGizmosSelected()
    {
        // Vẽ vùng bán kính kẹp trong Scene View để dễ căn chỉnh
        Transform pt = (attachPoint != null) ? attachPoint : transform;
        Gizmos.color = isHolding ? Color.green : Color.yellow;
        Gizmos.DrawWireSphere(pt.position, graspRadius);
    }
}
