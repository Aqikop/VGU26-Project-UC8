using System.Collections;
using UnityEngine;

/// <summary>
/// Sinh ngẫu nhiên các khối hộp (Đỏ, Xanh, Vàng) ở đầu băng chuyền.
/// Kiểm soát chặt chẽ nhịp độ: DUY NHẤT 1 KHỐI HỘP trên băng chuyền tại một thời điểm.
/// Tuyệt đối không sinh dồn dập, chỉ sinh khối mới khi khối cũ đã được gắp và phân loại.
/// Dự án: UC8 - Robotic Arm Conveyor Pick-and-Place
/// Tuần: Week 04 (R4 - Strict Single-Item Flow)
/// </summary>
public class RandomObjectSpawner : MonoBehaviour
{
    [Header("Cube Dimensions (m)")]
    [SerializeField] private float cubeSize = 0.06f; // 6cm

    [Header("Minimum Spawn Cooldown (s)")]
    [SerializeField] private float minSpawnCooldown = 1.0f;

    private int currentSpawnCount = 0;
    private float lastSpawnTime = -999f;
    private bool isSpawningScheduled = false;

    private void Start()
    {
        // Sinh đúng 1 khối hộp đầu tiên khi vừa bấm Play
        StartCoroutine(SpawnInitialObject());

        // Chạy watchdog an toàn: nếu trên băng chuyền không có hộp nào thì sinh đúng 1 hộp
        StartCoroutine(WatchdogLoop());
    }

    private IEnumerator SpawnInitialObject()
    {
        yield return new WaitForSeconds(0.5f);
        TrySpawnObject();
    }

    private IEnumerator WatchdogLoop()
    {
        while (true)
        {
            yield return new WaitForSeconds(3.0f);

            // Nếu trên băng chuyền hoàn toàn sạch bóng và không có lịch hẹn sinh
            if (!HasActiveObjectOnBelt() && !isSpawningScheduled)
            {
                TrySpawnObject();
            }
        }
    }

    /// <summary>
    /// Kiểm tra xem có khối hộp nào thực sự đang nằm trên mặt băng chuyền hay không
    /// (khối hộp đang được robot kẹp, hoặc đã vào thùng sẽ không tính là trên băng chuyền)
    /// </summary>
    public bool HasActiveObjectOnBelt()
    {
        SortableObject[] allObjects = FindObjectsOfType<SortableObject>();
        foreach (SortableObject obj in allObjects)
        {
            if (obj == null) continue;
            // Nếu đã được phân loại vào thùng -> Không còn trên băng tải
            if (obj.isSorted) continue;
            // Nếu đang được tay kẹp giữ (đã SetParent vào tool0) -> Đã rời khỏi băng tải
            if (obj.transform.parent != null) continue;
            // Băng chuyền nằm ở Z = -0.60m. Nếu hộp đã được nhấc sang vùng Z > -0.35m -> Đã rời băng tải
            if (obj.transform.position.z > -0.35f) continue;
            // Nếu hộp rơi khỏi bàn -> Bỏ qua
            if (obj.transform.position.y < -0.2f) continue;

            return true;
        }
        return false;
    }

    /// <summary>
    /// Được gọi bởi PickZoneSensor hoặc GripperController khi cánh tay robot đã gắp và nhấc hộp đi
    /// </summary>
    public void TriggerNextSpawn(float delay = 1.0f)
    {
        isSpawningScheduled = true;
        StopCoroutine(nameof(SpawnAfterDelayRoutine));
        StartCoroutine(SpawnAfterDelayRoutine(delay));
    }

    private IEnumerator SpawnAfterDelayRoutine(float delay)
    {
        yield return new WaitForSeconds(delay);
        isSpawningScheduled = false;
        TrySpawnObject();
    }

    public void TrySpawnObject()
    {
        // Kiểm tra thời gian hồi chiêu
        if (Time.time - lastSpawnTime < minSpawnCooldown)
        {
            return;
        }

        // Nếu trên băng tải ĐÃ CÓ hộp chưa phân loại, tuyệt đối không sinh thêm
        if (HasActiveObjectOnBelt())
        {
            return;
        }

        SpawnSingleObject();
    }

    private void SpawnSingleObject()
    {
        lastSpawnTime = Time.time;

        // 1. Tạo một Cube 3D trực tiếp từ Unity Engine
        GameObject newCube = GameObject.CreatePrimitive(PrimitiveType.Cube);
        newCube.name = $"Cube_{++currentSpawnCount}";
        newCube.transform.position = transform.position;
        newCube.transform.localScale = Vector3.one * cubeSize;

        // 2. Thêm Rigidbody để tương tác vật lý trôi trên băng chuyền
        Rigidbody rb = newCube.AddComponent<Rigidbody>();
        rb.mass = 0.2f;
        rb.collisionDetectionMode = CollisionDetectionMode.Continuous;

        // Triệt tiêu độ nảy (Zero-Bounce) để hộp rơi êm ru vào thùng, không nảy tưng tưng
        PhysicMaterial noBounceMat = new PhysicMaterial("NoBounceMat")
        {
            bounciness = 0f,
            bounceCombine = PhysicMaterialCombine.Minimum,
            dynamicFriction = 0.8f,
            staticFriction = 0.8f,
            frictionCombine = PhysicMaterialCombine.Maximum
        };
        BoxCollider boxCol = newCube.GetComponent<BoxCollider>();
        if (boxCol != null)
        {
            boxCol.material = noBounceMat;
        }

        // 3. Gắn component logic SortableObject
        SortableObject sortable = newCube.AddComponent<SortableObject>();

        // 4. Phân bố ngẫu nhiên 3 màu chuẩn: Red, Blue, Yellow
        float rand = Random.value;
        Color cubeColor;
        SortableObject.ColorType type;

        if (rand < 0.33f)
        {
            type = SortableObject.ColorType.Red;
            cubeColor = new Color(0.9f, 0.15f, 0.15f); // Đỏ tươi
        }
        else if (rand < 0.66f)
        {
            type = SortableObject.ColorType.Blue;
            cubeColor = new Color(0.15f, 0.45f, 0.95f); // Xanh dương
        }
        else
        {
            type = SortableObject.ColorType.Yellow;
            cubeColor = new Color(0.95f, 0.85f, 0.15f); // Vàng
        }

        Renderer renderer = newCube.GetComponent<Renderer>();
        if (renderer != null)
        {
            Material mat = new Material(Shader.Find("Standard"));
            mat.color = cubeColor;
            renderer.material = mat;
        }

        sortable.SetObjectType(type);
        Debug.Log($"[Spawner] Spawned single cube: {newCube.name} ({type}) at {transform.position}");
    }
}
