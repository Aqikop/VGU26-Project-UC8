using UnityEngine;

/// <summary>
/// Điều khiển góc nhìn Camera chuyên nghiệp cho Workcell UR10e:
/// - [1] Góc toàn cảnh 3/4 Isometric: Bao quát 100% băng chuyền 3.6m, robot và 3 thùng.
/// - [2] Góc cận cảnh Thùng Xanh (Blue Bin): Quan sát vị trí thùng xanh phía sau robot.
/// - [3] Góc cận cảnh Trạm Gắp (Close-Up Gripper): Quan sát phôi và mỏ kẹp tool0.
/// Hỗ trợ chuyển đổi mượt mà bằng phím tắt [1], [2], [3] (cả hàng số trên và bàn phím số Numpad).
/// GUI mặc định ẩn hoàn toàn theo yêu cầu để màn hình thông thoáng.
/// </summary>
public class WorkcellCameraController : MonoBehaviour
{
    public struct CameraPreset
    {
        public string name;
        public Vector3 position;
        public Vector3 eulerAngles;
        public float fov;

        public CameraPreset(string name, Vector3 pos, Vector3 rot, float fov)
        {
            this.name = name;
            this.position = pos;
            this.eulerAngles = rot;
            this.fov = fov;
        }
    }

    private CameraPreset[] presets;
    private int currentPresetIndex = 0;
    private Camera cam;

    [Header("Camera Transition Speed")]
    [SerializeField] private float transitionSpeed = 5.0f;

    [Header("GUI Configuration")]
    [Tooltip("Bật/tắt thanh nút bấm GUI (mặc định tắt để tránh che màn hình)")]
    [SerializeField] private bool showGUI = false;

    [Tooltip("Khoảng cách từ lề trái (pixels)")]
    [SerializeField] private float guiX = 12f;

    [Tooltip("Khoảng cách từ lề trên (pixels)")]
    [SerializeField] private float guiY = 78f;

    private Vector3 targetPosition;
    private Quaternion targetRotation;
    private float targetFov;

    private void Awake()
    {
        cam = GetComponent<Camera>();

        // Thiết lập 3 góc máy điện ảnh:
        // [1] Isometric: Toàn cảnh bao quát workcell
        // [2] Blue Bin: Cận cảnh thùng xanh (Blue Bin) ở tọa độ Z = 0.5m
        // [3] Close-Up: Cận cảnh trạm gắp phôi và cánh tay
        presets = new CameraPreset[]
        {
            new CameraPreset("[1] Isometric", new Vector3(-1.20f, 1.70f, -2.20f), new Vector3(30f, 30f, 0f), 52f),
            new CameraPreset("[2] Blue Bin",  new Vector3( 0.65f, 0.90f,  1.10f), new Vector3(35f, -135f, 0f), 46f),
            new CameraPreset("[3] Close-Up",  new Vector3(-0.70f, 0.85f, -1.35f), new Vector3(22f, 35f, 0f), 45f)
        };

        ApplyPresetInstant(0);
    }

    private void Update()
    {
        // Phím tắt chuyển đổi nhanh giữa 3 góc máy:
        // Phím [1]: Toàn cảnh Isometric
        if (Input.GetKeyDown(KeyCode.Alpha1) || Input.GetKeyDown(KeyCode.Keypad1)) SwitchToPreset(0);

        // Phím [2]: Cận cảnh Thùng Xanh (Blue Bin)
        if (Input.GetKeyDown(KeyCode.Alpha2) || Input.GetKeyDown(KeyCode.Keypad2)) SwitchToPreset(1);

        // Phím [3]: Cận cảnh Trạm Gắp (Close-Up Gripper)
        if (Input.GetKeyDown(KeyCode.Alpha3) || Input.GetKeyDown(KeyCode.Keypad3)) SwitchToPreset(2);

        // Lướt chuyển động mượt mà (Smooth Interpolation)
        transform.position = Vector3.Lerp(transform.position, targetPosition, Time.deltaTime * transitionSpeed);
        transform.rotation = Quaternion.Slerp(transform.rotation, targetRotation, Time.deltaTime * transitionSpeed);
        if (cam != null)
        {
            cam.fieldOfView = Mathf.Lerp(cam.fieldOfView, targetFov, Time.deltaTime * transitionSpeed);
        }
    }

    public void SwitchToPreset(int index)
    {
        if (index < 0 || index >= presets.Length) return;
        currentPresetIndex = index;
        targetPosition = presets[index].position;
        targetRotation = Quaternion.Euler(presets[index].eulerAngles);
        targetFov = presets[index].fov;
        Debug.Log($"[Camera] Switched to preset: {presets[index].name}");
    }

    private void ApplyPresetInstant(int index)
    {
        currentPresetIndex = index;
        targetPosition = presets[index].position;
        targetRotation = Quaternion.Euler(presets[index].eulerAngles);
        targetFov = presets[index].fov;

        transform.position = targetPosition;
        transform.rotation = targetRotation;
        if (cam != null) cam.fieldOfView = targetFov;
    }

    private void OnGUI()
    {
        if (!showGUI) return;

        // Thanh công cụ chuyển camera (chỉ hiện khi showGUI = true)
        GUILayout.BeginArea(new Rect(guiX, guiY, 310, 36), GUI.skin.box);
        GUILayout.BeginHorizontal();

        for (int i = 0; i < presets.Length; i++)
        {
            bool isCurrent = (i == currentPresetIndex);
            string btnText = isCurrent ? $"<b>▶ {presets[i].name}</b>" : presets[i].name;
            if (GUILayout.Button(btnText, GUILayout.Height(22)))
            {
                SwitchToPreset(i);
            }
        }

        GUILayout.EndHorizontal();
        GUILayout.EndArea();
    }
}
