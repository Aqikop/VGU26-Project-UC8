using System.Collections;
using UnityEngine;

/// <summary>
/// Cảm biến vùng gắp (PickZone) - Vận hành thuần vật lý thực tế (Pure Realistic Physics):
/// Khối hộp tự do trôi tự nhiên trên băng chuyền. Khi trôi đến đúng tâm trạm gắp (X >= -0.01m),
/// băng chuyền dừng lại để ma sát tự nhiên hãm khối hộp đứng yên ngay trước mặt robot.
/// Tuyệt đối không dùng teleport, không snap tọa độ nhân tạo, đảm bảo độ chân thực 100%.
/// </summary>
public class PickZoneSensor : MonoBehaviour
{
    [Header("Component References")]
    [SerializeField] private ConveyorController conveyor;
    [SerializeField] private ObjectLocalizationReporter localizationReporter;

    [Header("Pose Publishing Rate (Hz)")]
    [SerializeField] private float publishRateHz = 10f;

    [Header("Natural Stop Target Coordinate (World X Axis)")]
    [Tooltip("Threshold X coordinate where conveyor cuts power to let object coast to a stop")]
    [SerializeField] private float stopThresholdX = -0.015f;

    private float lastPublishTime = 0f;
    private GameObject currentObject;
    private bool hasStoppedConveyor = false;

    private void Awake()
    {
        if (conveyor == null) conveyor = FindObjectOfType<ConveyorController>();
        if (localizationReporter == null) localizationReporter = GetComponent<ObjectLocalizationReporter>();
    }

    private void Update()
    {
        if (currentObject == null) return;

        SortableObject sortable = currentObject.GetComponent<SortableObject>();
        if (sortable == null || sortable.isSorted || currentObject.transform.parent != null)
        {
            // Vật thể đã được robot kẹp nhấc lên hoặc đã phân loại
            currentObject = null;
            hasStoppedConveyor = false;
            return;
        }

        // 1. Theo dõi chuyển động tự nhiên của khối hộp trên băng tải
        if (!hasStoppedConveyor)
        {
            // Khi khối hộp trôi tự nhiên tới tâm trạm gắp trước mặt robot
            if (currentObject.transform.position.x >= stopThresholdX)
            {
                hasStoppedConveyor = true;
                if (conveyor != null)
                {
                    conveyor.StopConveyor();
                }
                Debug.Log($"[PickZone] Object {currentObject.name} coasted to pick station center (X={currentObject.transform.position.x:F3}m). Stopping conveyor naturally!");
            }
        }

        // 2. Stream target object pose to ROS at 10Hz
        if (hasStoppedConveyor)
        {
            float interval = 1f / Mathf.Max(1f, publishRateHz);
            if (Time.time - lastPublishTime >= interval)
            {
                lastPublishTime = Time.time;
                if (localizationReporter != null)
                {
                    localizationReporter.ReportObjectPose(currentObject.transform, sortable);
                }
            }
        }
    }

    private void OnTriggerEnter(Collider other)
    {
        Rigidbody body = other.attachedRigidbody;
        GameObject detectedObject = (body != null) ? body.gameObject : other.gameObject;

        SortableObject sortable = detectedObject.GetComponent<SortableObject>();
        if (sortable == null || sortable.isSorted || detectedObject.transform.parent != null)
        {
            return;
        }

        // Detect object but do NOT stop conveyor yet; let it coast to center
        currentObject = detectedObject;
        hasStoppedConveyor = false;
        Debug.Log($"[PickZone] Object {detectedObject.name} ({sortable.ObjectType}) entered sensor area, gliding to pick center...");
    }

    private void OnTriggerExit(Collider other)
    {
        Rigidbody body = other.attachedRigidbody;
        GameObject exitedObj = (body != null) ? body.gameObject : other.gameObject;

        if (currentObject != null && exitedObj == currentObject)
        {
            Debug.Log($"[PickZone] Object {exitedObj.name} left pick zone.");
            currentObject = null;
            hasStoppedConveyor = false;
        }
    }

    /// <summary>
    /// Reset or resume state
    /// </summary>
    public void ForceResume()
    {
        currentObject = null;
        hasStoppedConveyor = false;
        if (conveyor != null)
        {
            conveyor.StartConveyor();
            Debug.Log("[PickZone] Conveyor resumed via ForceResume.");
        }
    }
}
