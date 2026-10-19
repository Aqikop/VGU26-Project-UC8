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

        // A. 4 Cột nhôm định hình: 2 cột ngoài cùng và 2 cột tạo khung Cổng gắp phôi trung tâm (Pick Portal)
        float[] postX = { -0.80f, -0.22f, 0.22f, 0.80f };
        for (int i = 0; i < postX.Length; i++)
        {
            GameObject post = GameObject.CreatePrimitive(PrimitiveType.Cube);
            post.name = $"Post_{i + 1}";
            post.transform.SetParent(shieldRoot.transform, false);
            post.transform.localPosition = new Vector3(postX[i], 0f, 0f);
            post.transform.localScale = new Vector3(0.025f, 0.36f, 0.035f);
            post.GetComponent<MeshRenderer>().material = aluminumMat;
            Object.DestroyImmediate(post.GetComponent<Collider>());

            // Chân đế bắt bu-lông xuống bàn
            GameObject foot = GameObject.CreatePrimitive(PrimitiveType.Cube);
            foot.name = $"Foot_{i + 1}";
            foot.transform.SetParent(shieldRoot.transform, false);
            foot.transform.localPosition = new Vector3(postX[i], -0.175f, 0f);
            foot.transform.localScale = new Vector3(0.055f, 0.01f, 0.08f);
            foot.GetComponent<MeshRenderer>().material = blackMat;
            Object.DestroyImmediate(foot.GetComponent<Collider>());
        }

        // B. CÁNH TRÁI (Bảo hộ trước Thùng Đỏ - Left Protective Wing): từ X = -0.80m đến X = -0.22m
        GameObject wingLeft = new GameObject("Wing_Left_RedBin");
        wingLeft.transform.SetParent(shieldRoot.transform, false);

        GameObject topRailL = GameObject.CreatePrimitive(PrimitiveType.Cube);
        topRailL.name = "TopRail_Left";
        topRailL.transform.SetParent(wingLeft.transform, false);
        topRailL.transform.localPosition = new Vector3(-0.51f, 0.17f, 0f);
        topRailL.transform.localScale = new Vector3(0.58f, 0.02f, 0.035f);
        topRailL.GetComponent<MeshRenderer>().material = aluminumMat;
        Object.DestroyImmediate(topRailL.GetComponent<Collider>());

        GameObject bottomRailL = GameObject.CreatePrimitive(PrimitiveType.Cube);
        bottomRailL.name = "BottomRail_Left";
        bottomRailL.transform.SetParent(wingLeft.transform, false);
        bottomRailL.transform.localPosition = new Vector3(-0.51f, -0.17f, 0f);
        bottomRailL.transform.localScale = new Vector3(0.58f, 0.02f, 0.035f);
        bottomRailL.GetComponent<MeshRenderer>().material = aluminumMat;
        Object.DestroyImmediate(bottomRailL.GetComponent<Collider>());

        GameObject glassL = GameObject.CreatePrimitive(PrimitiveType.Cube);
        glassL.name = "Glass_Left";
        glassL.transform.SetParent(wingLeft.transform, false);
        glassL.transform.localPosition = new Vector3(-0.51f, 0f, 0f);
        glassL.transform.localScale = new Vector3(0.55f, 0.32f, 0.008f);
        glassL.GetComponent<MeshRenderer>().material = glassMat;
        Object.DestroyImmediate(glassL.GetComponent<Collider>());

        GameObject stripeL = GameObject.CreatePrimitive(PrimitiveType.Cube);
        stripeL.name = "Stripe_Left";
        stripeL.transform.SetParent(wingLeft.transform, false);
        stripeL.transform.localPosition = new Vector3(-0.51f, 0f, 0f);
        stripeL.transform.localScale = new Vector3(0.55f, 0.025f, 0.010f);
        stripeL.GetComponent<MeshRenderer>().material = yellowMat;
        Object.DestroyImmediate(stripeL.GetComponent<Collider>());

        // BoxCollider cánh trái chắn trước Thùng Đỏ (Bắt buộc robot phải né khi bỏ phôi đỏ)
        BoxCollider colL = wingLeft.AddComponent<BoxCollider>();
        colL.center = new Vector3(-0.51f, 0f, 0f);
        colL.size = new Vector3(0.58f, 0.36f, 0.08f);
        colL.isTrigger = false;

        // C. CÁNH PHẢI (Bảo hộ trước Thùng Vàng - Right Protective Wing): từ X = +0.22m đến X = +0.80m
        GameObject wingRight = new GameObject("Wing_Right_YellowBin");
        wingRight.transform.SetParent(shieldRoot.transform, false);

        GameObject topRailR = GameObject.CreatePrimitive(PrimitiveType.Cube);
        topRailR.name = "TopRail_Right";
        topRailR.transform.SetParent(wingRight.transform, false);
        topRailR.transform.localPosition = new Vector3(0.51f, 0.17f, 0f);
        topRailR.transform.localScale = new Vector3(0.58f, 0.02f, 0.035f);
        topRailR.GetComponent<MeshRenderer>().material = aluminumMat;
        Object.DestroyImmediate(topRailR.GetComponent<Collider>());

        GameObject bottomRailR = GameObject.CreatePrimitive(PrimitiveType.Cube);
        bottomRailR.name = "BottomRail_Right";
        bottomRailR.transform.SetParent(wingRight.transform, false);
        bottomRailR.transform.localPosition = new Vector3(0.51f, -0.17f, 0f);
        bottomRailR.transform.localScale = new Vector3(0.58f, 0.02f, 0.035f);
        bottomRailR.GetComponent<MeshRenderer>().material = aluminumMat;
        Object.DestroyImmediate(bottomRailR.GetComponent<Collider>());

        GameObject glassR = GameObject.CreatePrimitive(PrimitiveType.Cube);
        glassR.name = "Glass_Right";
        glassR.transform.SetParent(wingRight.transform, false);
        glassR.transform.localPosition = new Vector3(0.51f, 0f, 0f);
        glassR.transform.localScale = new Vector3(0.55f, 0.32f, 0.008f);
        glassR.GetComponent<MeshRenderer>().material = glassMat;
        DestroyImmediate(glassR.GetComponent<Collider>());

        GameObject stripeR = GameObject.CreatePrimitive(PrimitiveType.Cube);
        stripeR.name = "Stripe_Right";
        stripeR.transform.SetParent(wingRight.transform, false);
        stripeR.transform.localPosition = new Vector3(0.51f, 0f, 0f);
        stripeR.transform.localScale = new Vector3(0.55f, 0.025f, 0.010f);
        stripeR.GetComponent<MeshRenderer>().material = yellowMat;
        DestroyImmediate(stripeR.GetComponent<Collider>());

        // BoxCollider cánh phải chắn trước Thùng Vàng (Bắt buộc robot phải né khi bỏ phôi vàng)
        BoxCollider colR = wingRight.AddComponent<BoxCollider>();
        colR.center = new Vector3(0.51f, 0f, 0f);
        colR.size = new Vector3(0.58f, 0.36f, 0.08f);
        colR.isTrigger = false;

        // D. CỔNG GẮP TRUNG TÂM (Robotic Pick Portal - X từ -0.22m đến +0.22m):
        // Mở hoàn toàn không có collider, có thanh xà đỉnh vát trên cao ở Y = 0.22m kết nối toàn bộ hệ thống
        GameObject portalHeader = GameObject.CreatePrimitive(PrimitiveType.Cube);
        portalHeader.name = "Pick_Portal_Header_Rail";
        portalHeader.transform.SetParent(shieldRoot.transform, false);
        portalHeader.transform.localPosition = new Vector3(0f, 0.22f, 0f);
        portalHeader.transform.localScale = new Vector3(0.44f, 0.02f, 0.035f);
        portalHeader.GetComponent<MeshRenderer>().material = aluminumMat;
        Object.DestroyImmediate(portalHeader.GetComponent<Collider>());

        Undo.RecordObject(shieldRoot.transform, "Update Acrylic_Safety_Shield Transform");
        // Tọa độ Unity: (0m, 0.18m, -0.38m)
        shieldRoot.transform.position = new Vector3(0f, 0.18f, -0.38f);
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
