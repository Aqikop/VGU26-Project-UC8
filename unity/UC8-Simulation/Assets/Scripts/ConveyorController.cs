using System.Collections.Generic;
using UnityEngine;

/// <summary>
/// Điều khiển chuyển động và trực quan hóa băng chuyền chuẩn công nghiệp (Industrial Conveyor System):
/// - Vận chuyển vật thể mượt mà theo vật lý PhysX.
/// - Hiệu ứng cuộn bề mặt cao su có rãnh gân (Animated Ribbed Rubber Belt UV Scrolling).
/// - Khung nhôm định hình viền 2 bên (Aluminium Guide Rails).
/// - 2 con lăn mạ Chrome quay đồng bộ ở 2 đầu (Synchronized Drive & Idler Rollers).
/// - Chân đế cơ khí đỡ thân băng tải vững chãi trên bàn.
/// - Hộp động cơ giảm tốc công nghiệp (Gearmotor Unit).
/// - Cột cảm biến quang học tại trạm gắp với đèn LED chỉ thị (Xanh khi chạy, Đỏ khi dừng).
/// </summary>
public class ConveyorController : MonoBehaviour
{
    [Header("Conveyor Configuration")]
    [Tooltip("Conveyor belt movement speed (m/s)")]
    [SerializeField] private float speed = 0.3f;

    [Tooltip("Conveyor belt movement direction (Vector3)")]
    [SerializeField] private Vector3 moveDirection = Vector3.right;

    [Tooltip("Conveyor belt active running state")]
    [SerializeField] private bool isRunning = true;

    // Danh sách các vật thể đang nằm trên bề mặt băng chuyền
    private readonly List<Rigidbody> objectsOnConveyor = new List<Rigidbody>();

    // Visual animation elements
    private Material beltMaterial;
    private float textureOffsetX = 0f;
    private Material sensorLedMaterial;

    public bool IsRunning => isRunning;
    public float Speed => speed;

    private void Awake()
    {
        SetupIndustrialBeltVisuals();
        BuildConveyorMechanicalStructure();
    }

    private void Start()
    {
        UpdateSensorLed();
    }

    private void Update()
    {
        if (isRunning)
        {
            // Cuộn dải băng cao su cùng chiều và đồng tốc 100% với vận tốc vật lý của phôi
            if (beltMaterial != null)
            {
                textureOffsetX += (speed / 3.6f) * Time.deltaTime;
                beltMaterial.mainTextureOffset = new Vector2(textureOffsetX, 0f);
            }
        }
    }

    private void FixedUpdate()
    {
        if (!isRunning) return;

        Vector3 movement = moveDirection.normalized * speed * Time.fixedDeltaTime;

        // Di chuyển đồng bộ tất cả Rigidbody nằm trên băng tải
        for (int i = objectsOnConveyor.Count - 1; i >= 0; i--)
        {
            Rigidbody rb = objectsOnConveyor[i];
            if (rb != null && !rb.isKinematic)
            {
                rb.MovePosition(rb.position + movement);
            }
            else if (rb == null)
            {
                objectsOnConveyor.RemoveAt(i);
            }
        }
    }

    private void OnCollisionEnter(Collision collision)
    {
        Rigidbody rb = collision.rigidbody;
        if (rb != null && !objectsOnConveyor.Contains(rb))
        {
            objectsOnConveyor.Add(rb);
        }
    }

    private void OnCollisionExit(Collision collision)
    {
        Rigidbody rb = collision.rigidbody;
        if (rb != null && objectsOnConveyor.Contains(rb))
        {
            objectsOnConveyor.Remove(rb);
        }
    }

    /// <summary>
    /// Dừng băng tải ngay lập tức
    /// </summary>
    public void StopConveyor()
    {
        isRunning = false;
        UpdateSensorLed();
        Debug.Log("[Conveyor] Conveyor belt stopped (STOPPED).");
    }

    /// <summary>
    /// Khởi động lại băng tải
    /// </summary>
    public void StartConveyor()
    {
        isRunning = true;
        UpdateSensorLed();
        Debug.Log("[Conveyor] Conveyor belt resumed (RUNNING).");
    }

    public void SetSpeed(float newSpeed)
    {
        speed = Mathf.Max(0f, newSpeed);
    }

    private void UpdateSensorLed()
    {
        if (sensorLedMaterial != null)
        {
            Color ledColor = isRunning ? new Color(0.1f, 0.95f, 0.2f) : new Color(0.95f, 0.15f, 0.15f);
            sensorLedMaterial.color = ledColor;
            sensorLedMaterial.SetColor("_EmissionColor", ledColor * 0.8f);
        }
    }

    /// <summary>
    /// Tạo chất liệu dải băng cao su có rãnh gân công nghiệp (Ribbed Industrial Rubber)
    /// </summary>
    private void SetupIndustrialBeltVisuals()
    {
        Renderer rend = GetComponent<Renderer>();
        if (rend != null)
        {
            beltMaterial = new Material(Shader.Find("Standard"));
            beltMaterial.name = "IndustrialBelt_Rubber_Mat";

            Texture2D tex = CreateRibbedRubberTexture();
            beltMaterial.mainTexture = tex;
            beltMaterial.mainTextureScale = new Vector2(18f, 1f); // Lặp vân cao su dọc 3.6m
            beltMaterial.SetFloat("_Glossiness", 0.35f);
            beltMaterial.SetFloat("_Metallic", 0.15f);

            rend.material = beltMaterial;
        }
    }

    private Texture2D CreateRibbedRubberTexture()
    {
        int width = 128;
        int height = 128;
        Texture2D tex = new Texture2D(width, height, TextureFormat.RGBA32, true);
        tex.wrapMode = TextureWrapMode.Repeat;
        tex.filterMode = FilterMode.Bilinear;

        Color darkRubber = new Color(0.13f, 0.14f, 0.15f); // Đen xám cao su
        Color ribLine = new Color(0.05f, 0.05f, 0.06f);    // Rãnh chìm
        Color highlight = new Color(0.22f, 0.23f, 0.24f);  // Gân nổi sáng nhẹ

        for (int y = 0; y < height; y++)
        {
            for (int x = 0; x < width; x++)
            {
                int modX = x % 16;
                Color col;
                if (modX == 0 || modX == 1)
                    col = ribLine;
                else if (modX == 2)
                    col = highlight;
                else
                    col = darkRubber;

                // Viền gia cố mép 2 bên dải băng
                if (y < 4 || y > height - 5)
                    col = ribLine;

                tex.SetPixel(x, y, col);
            }
        }
        tex.Apply();
        return tex;
    }

    /// <summary>
    /// Tự động xây dựng bộ khung cơ khí công nghiệp hoàn chỉnh (Frame, Rollers, Legs, Motor, Sensor)
    /// </summary>
    private void BuildConveyorMechanicalStructure()
    {
        GameObject existing = GameObject.Find("Conveyor_Industrial_Rig");
        if (existing != null)
        {
            DestroyImmediate(existing);
        }

        GameObject rig = new GameObject("Conveyor_Industrial_Rig");
        rig.transform.position = Vector3.zero;
        rig.transform.rotation = Quaternion.identity;

        // 1. Vật liệu kim loại nhôm định hình & thép mạ
        Material aluminiumMat = new Material(Shader.Find("Standard"));
        aluminiumMat.color = new Color(0.82f, 0.84f, 0.86f);
        aluminiumMat.SetFloat("_Metallic", 0.85f);
        aluminiumMat.SetFloat("_Glossiness", 0.70f);

        Material chromeMat = new Material(Shader.Find("Standard"));
        chromeMat.color = new Color(0.75f, 0.77f, 0.80f);
        chromeMat.SetFloat("_Metallic", 0.95f);
        chromeMat.SetFloat("_Glossiness", 0.90f);

        Material steelDarkMat = new Material(Shader.Find("Standard"));
        steelDarkMat.color = new Color(0.22f, 0.23f, 0.25f);
        steelDarkMat.SetFloat("_Metallic", 0.60f);
        steelDarkMat.SetFloat("_Glossiness", 0.40f);

        Material motorMat = new Material(Shader.Find("Standard"));
        motorMat.color = new Color(0.12f, 0.30f, 0.45f); // Xanh dương cơ khí Siemens/SEW
        motorMat.SetFloat("_Metallic", 0.50f);
        motorMat.SetFloat("_Glossiness", 0.50f);

        // 2. Thanh nhôm dẫn hướng 2 mép (Aluminium Guide Rails) nhô cao hơn mặt băng 2.5cm
        CreateVisualBox(rig.transform, "Front_Rail", new Vector3(0f, 0.165f, -0.415f), new Vector3(3.64f, 0.045f, 0.025f), aluminiumMat);
        CreateVisualBox(rig.transform, "Back_Rail",  new Vector3(0f, 0.165f, -0.785f), new Vector3(3.64f, 0.045f, 0.025f), aluminiumMat);

        // Nẹp dưới khung băng tải
        CreateVisualBox(rig.transform, "Front_Bottom_Beam", new Vector3(0f, 0.07f, -0.415f), new Vector3(3.64f, 0.04f, 0.025f), steelDarkMat);
        CreateVisualBox(rig.transform, "Back_Bottom_Beam",  new Vector3(0f, 0.07f, -0.785f), new Vector3(3.64f, 0.04f, 0.025f), steelDarkMat);

        // 3. Con lăn 2 đầu trục (End Rollers) - Cố định tĩnh
        CreateVisualCylinder(rig.transform, "Left_Drive_Roller", new Vector3(-1.80f, 0.10f, -0.60f), new Vector3(0.10f, 0.175f, 0.10f), chromeMat);
        CreateVisualCylinder(rig.transform, "Right_Idler_Roller", new Vector3(1.80f, 0.10f, -0.60f), new Vector3(0.10f, 0.175f, 0.10f), chromeMat);

        // 4. Chân đế cơ khí đỡ băng tải (Support Stands) tại 3 vị trí (-1.4m, 0m, +1.4m)
        float[] legX = { -1.4f, 0.0f, 1.4f };
        foreach (float lx in legX)
        {
            // Cột chân trước
            CreateVisualBox(rig.transform, $"Leg_Front_{lx}", new Vector3(lx, 0.045f, -0.415f), new Vector3(0.045f, 0.09f, 0.045f), steelDarkMat);
            // Cột chân sau
            CreateVisualBox(rig.transform, $"Leg_Back_{lx}",  new Vector3(lx, 0.045f, -0.785f), new Vector3(0.045f, 0.09f, 0.045f), steelDarkMat);
            // Thanh giằng ngang
            CreateVisualBox(rig.transform, $"Leg_Brace_{lx}", new Vector3(lx, 0.025f, -0.600f), new Vector3(0.035f, 0.03f, 0.350f), steelDarkMat);
        }

        // 5. Cụm động cơ giảm tốc công nghiệp (Gearmotor Drive Unit) ở đầu dẫn động
        CreateVisualBox(rig.transform, "Gearmotor_Gearbox", new Vector3(-1.75f, 0.10f, -0.36f), new Vector3(0.16f, 0.14f, 0.10f), motorMat);
        CreateVisualCylinder(rig.transform, "Gearmotor_MotorBody", new Vector3(-1.75f, 0.10f, -0.28f), new Vector3(0.10f, 0.07f, 0.10f), motorMat);

        // 6. Cột cảm biến quang học tại trạm gắp (Photoelectric Sensor Post)
        CreateVisualBox(rig.transform, "Optical_Sensor_Post", new Vector3(0f, 0.18f, -0.40f), new Vector3(0.025f, 0.10f, 0.025f), steelDarkMat);
        GameObject ledObj = CreateVisualBox(rig.transform, "Optical_Sensor_LED", new Vector3(0f, 0.22f, -0.42f), new Vector3(0.03f, 0.025f, 0.025f), null);

        sensorLedMaterial = new Material(Shader.Find("Standard"));
        sensorLedMaterial.EnableKeyword("_EMISSION");
        MeshRenderer ledRend = ledObj.GetComponent<MeshRenderer>();
        if (ledRend != null) ledRend.material = sensorLedMaterial;
        UpdateSensorLed();
    }

    private GameObject CreateVisualBox(Transform parent, string name, Vector3 pos, Vector3 scale, Material mat)
    {
        GameObject obj = GameObject.CreatePrimitive(PrimitiveType.Cube);
        obj.name = name;
        obj.transform.SetParent(parent, false);
        obj.transform.position = pos;
        obj.transform.localScale = scale;

        Collider col = obj.GetComponent<Collider>();
        if (col != null) col.enabled = false; // Tắt hoàn toàn va chạm vật lý

        if (mat != null)
        {
            MeshRenderer mr = obj.GetComponent<MeshRenderer>();
            if (mr != null) mr.material = mat;
        }
        return obj;
    }

    private GameObject CreateVisualCylinder(Transform parent, string name, Vector3 pos, Vector3 scale, Material mat)
    {
        GameObject obj = GameObject.CreatePrimitive(PrimitiveType.Cylinder);
        obj.name = name;
        obj.transform.SetParent(parent, false);
        obj.transform.position = pos;
        obj.transform.rotation = Quaternion.Euler(90f, 0f, 0f); // Nằm ngang theo trục Z
        obj.transform.localScale = scale;

        Collider col = obj.GetComponent<Collider>();
        if (col != null) col.enabled = false;

        if (mat != null)
        {
            MeshRenderer mr = obj.GetComponent<MeshRenderer>();
            if (mr != null) mr.material = mat;
        }
        return obj;
    }
}
