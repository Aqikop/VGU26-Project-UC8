using UnityEngine;

/// <summary>
/// Điều khiển góc nhìn Camera chuyên nghiệp cho Workcell UR10e:
/// - Góc mặc định: Góc toàn cảnh 3/4 Isometric (Góc đẹp nhất, bao quát 100% băng chuyền 3.6m, robot và 3 thùng).
/// - Hỗ trợ chuyển đổi mượt mà giữa 4 góc máy điện ảnh bằng phím tắt [1], [2], [3], [4] hoặc GUI trên màn hình.
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

    private Vector3 targetPosition;
    private Quaternion targetRotation;
    private float targetFov;

    private void Awake()
    {
        cam = GetComponent<Camera>();

        // Thiết lập 2 góc máy chọn lọc theo yêu cầu:
        // [1] Cinematic Isometric: Góc toàn cảnh 3/4 bao quát 100% băng chuyền 3.6m, robot và 3 thùng
        // [3] Close-Up Gripper: Cận cảnh phôi và tay gắp
        presets = new CameraPreset[]
        {
            new CameraPreset("[1] Isometric", new Vector3(-1.20f, 1.70f, -2.20f), new Vector3(30f, 30f, 0f), 52f),
            new CameraPreset("[3] Close-Up",  new Vector3(-0.70f, 0.85f, -1.35f), new Vector3(22f, 35f, 0f), 45f)
        };

        ApplyPresetInstant(0);
    }

    private void Update()
    {
        // Phím tắt chuyển đổi nhanh giữa 2 góc máy: [1] Toàn cảnh và [3] Cận cảnh
        if (Input.GetKeyDown(KeyCode.Alpha1) || Input.GetKeyDown(KeyCode.Keypad1)) SwitchToPreset(0);
        if (Input.GetKeyDown(KeyCode.Alpha3) || Input.GetKeyDown(KeyCode.Keypad3) ||
            Input.GetKeyDown(KeyCode.Alpha2) || Input.GetKeyDown(KeyCode.Keypad2)) SwitchToPreset(1);

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
        // Thanh công cụ chuyển camera siêu gọn ở góc trên bên trái
        GUILayout.BeginArea(new Rect(12, 12, 210, 36), GUI.skin.box);
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
