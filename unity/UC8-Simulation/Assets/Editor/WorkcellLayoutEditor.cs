using UnityEngine;
using UnityEditor;
using UnityEditor.SceneManagement;

/// <summary>
/// Tự động cập nhật vị trí thiết bị trong Scene View theo Phương án 1 (Front Pick - Flanking Bins)
/// Mỗi khi Unity load script hoặc người dùng click menu: Workcell -> Apply Layout Option 1
/// </summary>
[InitializeOnLoad]
public class WorkcellLayoutEditor
{
    static WorkcellLayoutEditor()
    {
        EditorApplication.delayCall += ApplyLayout;
    }

    [MenuItem("Workcell/Apply Layout Option 1 (Front Pick & Flanking Bins)")]
    public static void ApplyLayout()
    {
        bool changed = false;

        GameObject table = GameObject.Find("Table");
        if (table != null)
        {
            Undo.RecordObject(table.transform, "Update Table Dimensions");
            table.transform.position = new Vector3(0f, -0.05f, 0f);
            table.transform.localScale = new Vector3(4.0f, 0.1f, 2.0f);
            changed = true;
        }

        GameObject conveyor = GameObject.Find("Conveyor");
        if (conveyor != null)
        {
            Undo.RecordObject(conveyor.transform, "Update Conveyor Dimensions");
            conveyor.transform.position = new Vector3(0f, 0.1f, -0.6f);
            conveyor.transform.localScale = new Vector3(3.6f, 0.1f, 0.35f);
            changed = true;
        }

        GameObject spawner = GameObject.Find("ObjectSpawner");
        if (spawner != null)
        {
            Undo.RecordObject(spawner.transform, "Update Spawner Position");
            spawner.transform.position = new Vector3(-1.5f, 0.35f, -0.6f);
            changed = true;
        }

        GameObject sensor = GameObject.Find("PickZoneSensor");
        if (sensor != null)
        {
            Undo.RecordObject(sensor.transform, "Update Sensor Position");
            sensor.transform.localPosition = new Vector3(0f, 1f, 0f);
            sensor.transform.localScale = new Vector3(0.25f, 1f, 1f);
            changed = true;
        }

        GameObject binRed = GameObject.Find("Bin_Red");
        if (binRed != null)
        {
            Undo.RecordObject(binRed.transform, "Update Bin_Red Position");
            binRed.transform.position = new Vector3(-0.55f, 0.01f, -0.1f);
            binRed.transform.localScale = new Vector3(1.35f, 1.25f, 1.35f);
            changed = true;
        }

        GameObject binYellow = GameObject.Find("Bin_Yellow");
        if (binYellow != null)
        {
            Undo.RecordObject(binYellow.transform, "Update Bin_Yellow Position");
            binYellow.transform.position = new Vector3(0.55f, 0.01f, -0.1f);
            binYellow.transform.localScale = new Vector3(1.35f, 1.25f, 1.35f);
            changed = true;
        }

        GameObject binBlue = GameObject.Find("Bin_Blue");
        if (binBlue != null)
        {
            Undo.RecordObject(binBlue.transform, "Update Bin_Blue Position");
            binBlue.transform.position = new Vector3(0f, 0.01f, 0.5f);
            binBlue.transform.localScale = new Vector3(1.35f, 1.25f, 1.35f);
            changed = true;
        }

        // Tự động tạo và đồng bộ Tủ điều khiển UR Control Box & Pendant (Requirement R8)
        EnsureURControlBox();

        // Tự động tạo và đồng bộ Tấm lưới an toàn mica Acrylic Safety Shield (Requirement R8)
        EnsureAcrylicSafetyShield();
        changed = true;

        // Tự động tạo và cập nhật các quả cầu Waypoint Visual Markers tại vị trí mới
        EnsureWaypointMarkers();

        if (changed)
        {
            EditorSceneManager.MarkAllScenesDirty();
            Debug.Log("<color=green>[WorkcellLayout] Successfully applied Option 1 layout, UR Control Box, Acrylic Safety Shield (R8), and updated Waypoint Visual Markers in Unity Scene!</color>");
        }
    }

    private static void EnsureURControlBox()
    {
        // Xóa vật thể cũ nếu có
        GameObject oldWall = GameObject.Find("Static_Barrier_Wall");
        if (oldWall != null) Undo.DestroyObjectImmediate(oldWall);

        GameObject boxRoot = GameObject.Find("UR_Control_Box");
        if (boxRoot == null)
        {
            boxRoot = new GameObject("UR_Control_Box");
            Undo.RegisterCreatedObjectUndo(boxRoot, "Create UR_Control_Box");

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
            Object.DestroyImmediate(body.GetComponent<Collider>());

            // B. Mặt Panel trước (Front Panel Inset)
            GameObject panel = GameObject.CreatePrimitive(PrimitiveType.Cube);
            panel.name = "Front_Panel";
            panel.transform.SetParent(boxRoot.transform, false);
            panel.transform.localPosition = new Vector3(0f, 0f, -0.121f);
            panel.transform.localScale = new Vector3(0.28f, 0.34f, 0.008f);
            panel.GetComponent<MeshRenderer>().material = panelMat;
            Object.DestroyImmediate(panel.GetComponent<Collider>());

            // C. Nút dừng khẩn cấp E-Stop (Vòng vàng + Nấm đỏ)
            GameObject eStopBase = GameObject.CreatePrimitive(PrimitiveType.Cylinder);
            eStopBase.name = "EStop_Base";
            eStopBase.transform.SetParent(boxRoot.transform, false);
            eStopBase.transform.localPosition = new Vector3(0.09f, 0.10f, -0.128f);
            eStopBase.transform.localScale = new Vector3(0.045f, 0.005f, 0.045f);
            eStopBase.transform.localRotation = Quaternion.Euler(90f, 0f, 0f);
            eStopBase.GetComponent<MeshRenderer>().material = yellowMat;
            Object.DestroyImmediate(eStopBase.GetComponent<Collider>());

            GameObject eStopCap = GameObject.CreatePrimitive(PrimitiveType.Sphere);
            eStopCap.name = "EStop_Mushroom";
            eStopCap.transform.SetParent(boxRoot.transform, false);
            eStopCap.transform.localPosition = new Vector3(0.09f, 0.10f, -0.138f);
            eStopCap.transform.localScale = new Vector3(0.038f, 0.022f, 0.038f);
            eStopCap.GetComponent<MeshRenderer>().material = redMat;
            Object.DestroyImmediate(eStopCap.GetComponent<Collider>());

            // D. Đèn LED báo trạng thái nguồn
            GameObject led = GameObject.CreatePrimitive(PrimitiveType.Sphere);
            led.name = "Power_LED";
            led.transform.SetParent(boxRoot.transform, false);
            led.transform.localPosition = new Vector3(-0.10f, 0.12f, -0.128f);
            led.transform.localScale = new Vector3(0.014f, 0.014f, 0.014f);
            led.GetComponent<MeshRenderer>().material = greenLedMat;
            Object.DestroyImmediate(led.GetComponent<Collider>());

            // E. Cột đỡ Teach Pendant (Pendant Stand)
            GameObject pole = GameObject.CreatePrimitive(PrimitiveType.Cylinder);
            pole.name = "Pendant_Stand_Pole";
            pole.transform.SetParent(boxRoot.transform, false);
            pole.transform.localPosition = new Vector3(-0.11f, 0.22f, 0f);
            pole.transform.localScale = new Vector3(0.018f, 0.08f, 0.018f);
            pole.GetComponent<MeshRenderer>().material = cabinetMat;
            Object.DestroyImmediate(pole.GetComponent<Collider>());

            // F. Màn hình Teach Pendant (Tablet cảm ứng nghiêng 25 độ hướng ra ngoài)
            GameObject pendant = GameObject.CreatePrimitive(PrimitiveType.Cube);
            pendant.name = "Teach_Pendant_Screen";
            pendant.transform.SetParent(boxRoot.transform, false);
            pendant.transform.localPosition = new Vector3(-0.11f, 0.28f, -0.04f);
            pendant.transform.localScale = new Vector3(0.20f, 0.14f, 0.016f);
            pendant.transform.localRotation = Quaternion.Euler(-25f, 0f, 0f);
            pendant.GetComponent<MeshRenderer>().material = screenMat;
            Object.DestroyImmediate(pendant.GetComponent<Collider>());

            // G. BoxCollider bao trọn toàn bộ tủ và màn hình
            BoxCollider col = boxRoot.AddComponent<BoxCollider>();
            col.center = new Vector3(0f, 0.02f, 0f);
            col.size = new Vector3(0.32f, 0.42f, 0.24f);
            col.isTrigger = false;
        }

        Undo.RecordObject(boxRoot.transform, "Update UR_Control_Box Transform");
        // Tọa độ Unity: (-0.48m, 0.19m, 0.35m) ở góc vuông phía sau giữa Thùng Đỏ và Thùng Xanh
        // Xoay mặt chính (màn hình & nút E-Stop) song song 100% với mặt thùng đỏ
        boxRoot.transform.position = new Vector3(-0.48f, 0.19f, 0.35f);
        boxRoot.transform.rotation = Quaternion.identity;
    }

    private static void EnsureAcrylicSafetyShield()
    {
        // Xóa vật cản cũ nếu còn tồn tại trong Scene
        GameObject oldCurtain = GameObject.Find("Safety_Light_Curtain");
        if (oldCurtain != null) Undo.DestroyObjectImmediate(oldCurtain);
        GameObject oldWall = GameObject.Find("Static_Barrier_Wall");
        if (oldWall != null) Undo.DestroyObjectImmediate(oldWall);

        GameObject shieldRoot = GameObject.Find("Acrylic_Safety_Shield");
        if (shieldRoot != null) Undo.DestroyObjectImmediate(shieldRoot);

        shieldRoot = new GameObject("Acrylic_Safety_Shield");
        Undo.RegisterCreatedObjectUndo(shieldRoot, "Create Acrylic_Safety_Shield");

        Shader stdShader = Shader.Find("Standard") ?? Shader.Find("Universal Render Pipeline/Lit") ?? Shader.Find("Diffuse");

        // Material: Khung nhôm định hình xám kim loại công nghiệp (Anodized Aluminum Frame)
        Material aluminumMat = new Material(stdShader);
        aluminumMat.color = new Color(0.28f, 0.30f, 0.34f);
        if (aluminumMat.HasProperty("_Metallic")) aluminumMat.SetFloat("_Metallic", 0.75f);
        if (aluminumMat.HasProperty("_Glossiness")) aluminumMat.SetFloat("_Glossiness", 0.65f);

        // Material: Chân đế kim loại bắt bu-lông màu đen nhám (Base Flange)
        Material blackMat = new Material(stdShader);
        blackMat.color = new Color(0.12f, 0.13f, 0.15f);

        // Material: Tấm chắn Mica / Polycarbonate trong suốt (Transparent Acrylic Glass)
        Material glassMat = new Material(stdShader);
        glassMat.color = new Color(0.85f, 0.93f, 1.0f, 0.35f); // Mica trong suốt ánh xanh nhẹ
        glassMat.SetFloat("_Mode", 3); // Transparent mode
        glassMat.SetInt("_SrcBlend", (int)UnityEngine.Rendering.BlendMode.SrcAlpha);
        glassMat.SetInt("_DstBlend", (int)UnityEngine.Rendering.BlendMode.OneMinusSrcAlpha);
        glassMat.SetInt("_ZWrite", 0);
        glassMat.DisableKeyword("_ALPHATEST_ON");
        glassMat.DisableKeyword("_ALPHABLEND_ON");
        glassMat.EnableKeyword("_ALPHAPREMULTIPLY_ON");
        glassMat.renderQueue = 3000;
        if (glassMat.HasProperty("_Glossiness")) glassMat.SetFloat("_Glossiness", 0.95f);
        if (glassMat.HasProperty("_Metallic")) glassMat.SetFloat("_Metallic", 0.1f);

        // Material: Vạch an toàn cảnh báo vàng công nghiệp (Safety Yellow Warning Stripe)
        Material yellowMat = new Material(stdShader);
        yellowMat.color = new Color(0.96f, 0.75f, 0.05f);

        // A. 4 Cột nhôm định hình đứng gia cố chịu lực (2 cột biên + 2 cột trung gian chia 3 khoang)
        float[] postX = { -0.80f, -0.27f, 0.27f, 0.80f };
        for (int i = 0; i < postX.Length; i++)
        {
            GameObject post = GameObject.CreatePrimitive(PrimitiveType.Cube);
            post.name = $"Post_{i + 1}";
            post.transform.SetParent(shieldRoot.transform, false);
            post.transform.localPosition = new Vector3(postX[i], 0f, 0f);
            post.transform.localScale = new Vector3(0.025f, 0.30f, 0.035f);
            post.GetComponent<MeshRenderer>().material = aluminumMat;
            Object.DestroyImmediate(post.GetComponent<Collider>());

            // Chân đế bắt bu-lông xuống mặt bàn
            GameObject foot = GameObject.CreatePrimitive(PrimitiveType.Cube);
            foot.name = $"Foot_{i + 1}";
            foot.transform.SetParent(shieldRoot.transform, false);
            foot.transform.localPosition = new Vector3(postX[i], -0.145f, 0f);
            foot.transform.localScale = new Vector3(0.055f, 0.01f, 0.08f);
            foot.GetComponent<MeshRenderer>().material = blackMat;
            Object.DestroyImmediate(foot.GetComponent<Collider>());
        }

        // B. Thanh nhôm ngang trên cùng (Top Rail - Dài 1.64m suốt từ Thùng Đỏ sang Thùng Vàng)
        GameObject topRail = GameObject.CreatePrimitive(PrimitiveType.Cube);
        topRail.name = "Top_Rail";
        topRail.transform.SetParent(shieldRoot.transform, false);
        topRail.transform.localPosition = new Vector3(0f, 0.14f, 0f);
        topRail.transform.localScale = new Vector3(1.64f, 0.02f, 0.035f);
        topRail.GetComponent<MeshRenderer>().material = aluminumMat;
        Object.DestroyImmediate(topRail.GetComponent<Collider>());

        // C. Thanh nhôm ngang đáy (Bottom Rail - Dài 1.64m sát mặt bàn)
        GameObject bottomRail = GameObject.CreatePrimitive(PrimitiveType.Cube);
        bottomRail.name = "Bottom_Rail";
        bottomRail.transform.SetParent(shieldRoot.transform, false);
        bottomRail.transform.localPosition = new Vector3(0f, -0.14f, 0f);
        bottomRail.transform.localScale = new Vector3(1.64f, 0.02f, 0.035f);
        bottomRail.GetComponent<MeshRenderer>().material = aluminumMat;
        Object.DestroyImmediate(bottomRail.GetComponent<Collider>());

        // D. 3 Tấm kính Mica trong suốt ghép trong 3 khoang (Trước Thùng Đỏ, Khoang Giữa, Trước Thùng Vàng)
        float[] paneCentersX = { -0.535f, 0.0f, 0.535f };
        float[] paneWidths = { 0.505f, 0.515f, 0.505f };
        string[] paneNames = { "Mica_Panel_RedBin", "Mica_Panel_CenterPick", "Mica_Panel_YellowBin" };

        for (int p = 0; p < 3; p++)
        {
            GameObject glassPanel = GameObject.CreatePrimitive(PrimitiveType.Cube);
            glassPanel.name = paneNames[p];
            glassPanel.transform.SetParent(shieldRoot.transform, false);
            glassPanel.transform.localPosition = new Vector3(paneCentersX[p], 0f, 0f);
            glassPanel.transform.localScale = new Vector3(paneWidths[p], 0.26f, 0.008f);
            glassPanel.GetComponent<MeshRenderer>().material = glassMat;
            Object.DestroyImmediate(glassPanel.GetComponent<Collider>());

            // Dải tem cảnh báo an toàn màu vàng chạy ngang giữa mỗi tấm mica
            GameObject stripe = GameObject.CreatePrimitive(PrimitiveType.Cube);
            stripe.name = $"Warning_Stripe_{p + 1}";
            stripe.transform.SetParent(shieldRoot.transform, false);
            stripe.transform.localPosition = new Vector3(paneCentersX[p], 0f, 0f);
            stripe.transform.localScale = new Vector3(paneWidths[p], 0.025f, 0.010f);
            stripe.GetComponent<MeshRenderer>().material = yellowMat;
            Object.DestroyImmediate(stripe.GetComponent<Collider>());
        }

        // E. BoxCollider bao bọc toàn bộ hệ thống vách chắn mica (Rộng 1.64m, Cao 0.30m, Dày 0.08m)
        BoxCollider col = shieldRoot.AddComponent<BoxCollider>();
        col.center = Vector3.zero;
        col.size = new Vector3(1.64f, 0.30f, 0.08f);
        col.isTrigger = false;

        Undo.RecordObject(shieldRoot.transform, "Update Acrylic_Safety_Shield Transform");
        // Tọa độ Unity: (0m, 0.15m, -0.38m) độ cao 30cm chuẩn để robot vươn gắp phôi trơn tru không chạm cùi chỏ
        shieldRoot.transform.position = new Vector3(0f, 0.15f, -0.38f);
        shieldRoot.transform.rotation = Quaternion.identity;
    }

    private static void EnsureWaypointMarkers()
    {
        GameObject parentObj = GameObject.Find("Waypoint_Visual_Markers");
        if (parentObj == null)
        {
            parentObj = new GameObject("Waypoint_Visual_Markers");
            Undo.RegisterCreatedObjectUndo(parentObj, "Create Waypoint_Visual_Markers");
        }

        CreateOrUpdateMarker(parentObj.transform, "Marker_IDLE / READY", new Vector3(0f, 0.42f, -0.60f), new Color(0.2f, 0.95f, 0.3f));
        CreateOrUpdateMarker(parentObj.transform, "Marker_PICK ZONE",    new Vector3(0f, 0.18f, -0.60f), new Color(0.1f, 0.85f, 0.95f));
        CreateOrUpdateMarker(parentObj.transform, "Marker_RED BIN",      new Vector3(-0.55f, 0.35f, -0.10f), new Color(0.95f, 0.2f, 0.2f));
        CreateOrUpdateMarker(parentObj.transform, "Marker_YELLOW BIN",   new Vector3(0.55f, 0.35f, -0.10f), new Color(0.98f, 0.88f, 0.15f));
        CreateOrUpdateMarker(parentObj.transform, "Marker_BLUE BIN",     new Vector3(0f, 0.35f, 0.50f), new Color(0.2f, 0.5f, 1.0f));
    }

    private static void CreateOrUpdateMarker(Transform parent, string name, Vector3 pos, Color color)
    {
        Transform child = parent.Find(name);
        GameObject markerObj = child != null ? child.gameObject : null;

        if (markerObj == null)
        {
            markerObj = GameObject.CreatePrimitive(PrimitiveType.Sphere);
            markerObj.name = name;
            Undo.RegisterCreatedObjectUndo(markerObj, "Create " + name);
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
}
