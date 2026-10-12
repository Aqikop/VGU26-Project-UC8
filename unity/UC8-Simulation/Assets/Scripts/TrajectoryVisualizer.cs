using System.Collections;
using UnityEngine;

/// <summary>
/// Hiển thị trực quan quỹ đạo chuyển động của End-Effector (tool0) trong Unity:
/// - Phím tắt [T]: Bật / Tắt hiển thị quỹ đạo (Toggle Trajectory Trail).
/// - Phím tắt [C]: Xóa vệt quỹ đạo hiện tại ngay lập tức (Clear Trail).
/// - Cơ chế chống rối (Anti-Clutter):
///   + Tự động tan biến sau 3.5s (Fade-out lifespan), không lưu vết vĩnh viễn gây rối mắt.
///   + Tự động dọn sạch (Clear) khi hoàn tất chu trình gắp thả để đón chu trình mới.
///   + Vuốt nhọn thẩm mỹ (Tapered ribbon trail): to ở đầu (2.5cm) và nhọn dần về đuôi (0.2cm).
/// - Đổi màu Neon thông minh:
///   + Đang gắp Red cube   -> Neon Hồng/Đỏ (#FF2A6D)
///   + Đang gắp Yellow cube-> Neon Vàng Hổ Phách (#FFD166)
///   + Đang gắp Blue cube  -> Neon Xanh Cyan (#05D9E8)
///   + Trạng thái rảnh     -> Neon Mint/Teal (#06D6A0)
/// Dự án: UC8 - Robotic Arm Conveyor Pick-and-Place
/// Tuần: Week 05 & Milestone 1 (Trajectory Visualization)
/// </summary>
public class TrajectoryVisualizer : MonoBehaviour
{
    [Header("Trajectory Trail Settings")]
    [Tooltip("Bật/Tắt vệt quỹ đạo khi bắt đầu (Ấn phím T để bật/tắt trong lúc chạy)")]
    [SerializeField] private bool isTrailEnabled = true;

    [Tooltip("Thời gian tồn tại của vệt quỹ đạo trước khi tự tan biến (giây)")]
    [SerializeField] private float fadeLifetime = 3.5f;

    [Tooltip("Độ rộng lớn nhất của vệt quỹ đạo tại đầu kẹp (mét)")]
    [SerializeField] private float startWidth = 0.025f;

    [Tooltip("Độ rộng nhỏ nhất của vệt quỹ đạo tại đuôi (mét)")]
    [SerializeField] private float endWidth = 0.002f;

    [Tooltip("Tự động xóa vệt khi nhả hộp vào thùng để đón chu trình mới")]
    [SerializeField] private bool autoClearOnRelease = true;

    [Header("Neon Color Scheme")]
    [SerializeField] private Color idleColor = new Color(0.02f, 0.84f, 0.63f, 1.0f);   // Neon Mint (#06D6A0)
    [SerializeField] private Color redCubeColor = new Color(1.0f, 0.16f, 0.43f, 1.0f); // Neon Crimson (#FF2A6D)
    [SerializeField] private Color yellowCubeColor = new Color(1.0f, 0.82f, 0.40f, 1.0f); // Neon Amber (#FFD166)
    [SerializeField] private Color blueCubeColor = new Color(0.02f, 0.85f, 0.91f, 1.0f); // Neon Cyan (#05D9E8)

    private TrailRenderer trailRenderer;
    private Material trailMaterial;
    private Color currentColor;

    // GUI Notification Banner
    private string notificationText = "";
    private float notificationTimer = 0f;
    private GUIStyle bannerStyle;
    private GUIStyle labelStyle;
    private Texture2D bannerBackground;

    private void Awake()
    {
        SetupTrailRenderer();
    }

    private void Start()
    {
        SetColor(idleColor);
        ShowNotification(isTrailEnabled ? "[T] Trajectory Trail: ON (Press 'T' to toggle)" : "[T] Trajectory Trail: OFF (Press 'T' to toggle)", 3.0f);
    }

    private void Update()
    {
        // Phím tắt [T]: Toggle Bật/Tắt vệt quỹ đạo
        if (Input.GetKeyDown(KeyCode.T))
        {
            ToggleTrail();
        }

        // Phím tắt [C]: Xóa vệt quỹ đạo hiện tại ngay lập tức
        if (Input.GetKeyDown(KeyCode.C))
        {
            ClearTrail();
            ShowNotification("Trajectory Trail: CLEARED", 2.0f);
        }

        if (notificationTimer > 0f)
        {
            notificationTimer -= Time.deltaTime;
        }
    }

    public void ToggleTrail()
    {
        isTrailEnabled = !isTrailEnabled;
        if (trailRenderer != null)
        {
            trailRenderer.emitting = isTrailEnabled;
            if (!isTrailEnabled)
            {
                trailRenderer.Clear();
            }
        }
        ShowNotification(isTrailEnabled ? "[T] Trajectory Trail: ON" : "[T] Trajectory Trail: OFF", 2.5f);
        Debug.Log($"[TrajectoryVisualizer] Trajectory Trail is now {(isTrailEnabled ? "ENABLED" : "DISABLED")}");
    }

    public void ClearTrail()
    {
        if (trailRenderer != null)
        {
            trailRenderer.Clear();
        }
    }

    public void OnObjectGrasped(SortableObject.ColorType colorType)
    {
        switch (colorType)
        {
            case SortableObject.ColorType.Red:
                SetColor(redCubeColor);
                break;
            case SortableObject.ColorType.Yellow:
                SetColor(yellowCubeColor);
                break;
            case SortableObject.ColorType.Blue:
                SetColor(blueCubeColor);
                break;
            default:
                SetColor(idleColor);
                break;
        }
    }

    public void OnObjectReleased()
    {
        SetColor(idleColor);
        if (autoClearOnRelease)
        {
            StartCoroutine(DelayedClear(0.35f));
        }
    }

    private IEnumerator DelayedClear(float delay)
    {
        yield return new WaitForSeconds(delay);
        if (trailRenderer != null)
        {
            trailRenderer.Clear();
        }
    }

    public void SetColor(Color col)
    {
        currentColor = col;
        if (trailRenderer == null) return;

        Gradient gradient = new Gradient();
        gradient.SetKeys(
            new GradientColorKey[] {
                new GradientColorKey(col, 0.0f),
                new GradientColorKey(col * 0.85f, 0.7f),
                new GradientColorKey(col * 0.5f, 1.0f)
            },
            new GradientAlphaKey[] {
                new GradientAlphaKey(0.95f, 0.0f),
                new GradientAlphaKey(0.75f, 0.5f),
                new GradientAlphaKey(0.0f, 1.0f)
            }
        );
        trailRenderer.colorGradient = gradient;
    }

    private void SetupTrailRenderer()
    {
        // Tìm hoặc tạo GameObject con để chứa TrailRenderer
        Transform trailChild = transform.Find("TrajectoryTrail");
        GameObject trailObj;

        if (trailChild != null)
        {
            trailObj = trailChild.gameObject;
        }
        else
        {
            trailObj = new GameObject("TrajectoryTrail");
            trailObj.transform.SetParent(transform, false);
            trailObj.transform.localPosition = Vector3.zero;
            trailObj.transform.localRotation = Quaternion.identity;
        }

        trailRenderer = trailObj.GetComponent<TrailRenderer>();
        if (trailRenderer == null)
        {
            trailRenderer = trailObj.AddComponent<TrailRenderer>();
        }

        // Tạo Material an toàn (không bị lỗi missing shader màu tím)
        Shader shader = Shader.Find("Sprites/Default") 
                     ?? Shader.Find("Universal Render Pipeline/Unlit") 
                     ?? Shader.Find("Particles/Standard Unlit")
                     ?? Shader.Find("Unlit/Color");

        if (shader != null)
        {
            trailMaterial = new Material(shader);
        }
        else
        {
            trailMaterial = new Material(Shader.Find("Legacy Shaders/Particles/Alpha Blended Premultiply"));
        }

        trailMaterial.color = Color.white;
        trailRenderer.material = trailMaterial;

        // Cấu hình thông số thẩm mỹ
        trailRenderer.time = fadeLifetime;
        trailRenderer.minVertexDistance = 0.005f; // Độ phân giải 5mm cho đường cong mượt mà
        trailRenderer.autodestruct = false;
        trailRenderer.emitting = isTrailEnabled;
        trailRenderer.shadowCastingMode = UnityEngine.Rendering.ShadowCastingMode.Off;
        trailRenderer.receiveShadows = false;

        // Tạo đường cong vuốt nhọn (Tapered curve)
        AnimationCurve widthCurve = new AnimationCurve();
        widthCurve.AddKey(0.0f, startWidth);
        widthCurve.AddKey(0.6f, startWidth * 0.6f);
        widthCurve.AddKey(1.0f, endWidth);
        trailRenderer.widthCurve = widthCurve;
    }

    public void ShowNotification(string message, float duration = 2.5f)
    {
        notificationText = message;
        notificationTimer = duration;
    }

    private void OnGUI()
    {
        // Hiển thị thông báo nhỏ gọn tinh tế ở góc trên bên trái khi ấn phím
        if (notificationTimer > 0f && !string.IsNullOrEmpty(notificationText))
        {
            if (bannerBackground == null)
            {
                bannerBackground = new Texture2D(1, 1);
                bannerBackground.SetPixel(0, 0, new Color(0.05f, 0.08f, 0.15f, 0.85f));
                bannerBackground.Apply();

                bannerStyle = new GUIStyle();
                bannerStyle.normal.background = bannerBackground;
                bannerStyle.border = new RectOffset(4, 4, 4, 4);

                labelStyle = new GUIStyle();
                labelStyle.fontStyle = FontStyle.Bold;
                labelStyle.fontSize = 13;
                labelStyle.normal.textColor = isTrailEnabled ? new Color(0.02f, 0.95f, 0.70f) : new Color(0.95f, 0.40f, 0.40f);
                labelStyle.alignment = TextAnchor.MiddleCenter;
            }
            else
            {
                labelStyle.normal.textColor = isTrailEnabled ? new Color(0.02f, 0.95f, 0.70f) : new Color(0.95f, 0.40f, 0.40f);
            }

            float boxWidth = 330f;
            float boxHeight = 32f;
            float x = 16f;
            float y = 16f;

            GUI.Box(new Rect(x, y, boxWidth, boxHeight), GUIContent.none, bannerStyle);
            GUI.Label(new Rect(x, y, boxWidth, boxHeight), notificationText, labelStyle);
        }
    }

    private void OnDestroy()
    {
        if (bannerBackground != null)
        {
            Destroy(bannerBackground);
        }
        if (trailMaterial != null)
        {
            Destroy(trailMaterial);
        }
    }
}
