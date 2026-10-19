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

        // Tự động tạo và đồng bộ Cột rèm quang an toàn Safety Light Curtain (Requirement R8)
        EnsureSafetyLightCurtain();
        changed = true;

        // Tự động tạo và cập nhật các quả cầu Waypoint Visual Markers tại vị trí mới
        EnsureWaypointMarkers();

        if (changed)
        {
            EditorSceneManager.MarkAllScenesDirty();
            Debug.Log("<color=green>[WorkcellLayout] Successfully applied Option 1 layout, UR Control Box, Safety Light Curtain (R8), and updated Waypoint Visual Markers in Unity Scene!</color>");
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
        boxRoot.transform.position = new Vector3(-0.48f, 0.19f, 0.35f);
        boxRoot.transform.rotation = Quaternion.Euler(0f, 30f, 0f);
    }

    private static void EnsureSafetyLightCurtain()
    {
        GameObject curtainRoot = GameObject.Find("Safety_Light_Curtain");
        if (curtainRoot == null)
        {
            curtainRoot = new GameObject("Safety_Light_Curtain");
            Undo.RegisterCreatedObjectUndo(curtainRoot, "Create Safety_Light_Curtain");

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
            emitterLedMat.color = new Color(1.0f, 0.2f, 0.2f);
            emitterLedMat.EnableKeyword("_EMISSION");
            emitterLedMat.SetColor("_EmissionColor", new Color(1.0f, 0.2f, 0.2f) * 0.7f);

            // A. Thân cột nhôm định hình chính (Column: 7cm x 36cm x 7cm)
            GameObject column = GameObject.CreatePrimitive(PrimitiveType.Cube);
            column.name = "Curtain_Column";
            column.transform.SetParent(curtainRoot.transform, false);
            column.transform.localPosition = Vector3.zero;
            column.transform.localScale = new Vector3(0.07f, 0.36f, 0.07f);
            column.GetComponent<MeshRenderer>().material = yellowMat;
            Object.DestroyImmediate(column.GetComponent<Collider>());

            // B. Chân đế bắt bu-lông xuống mặt bàn (Base Flange)
            GameObject flange = GameObject.CreatePrimitive(PrimitiveType.Cube);
            flange.name = "Base_Flange";
            flange.transform.SetParent(curtainRoot.transform, false);
            flange.transform.localPosition = new Vector3(0f, -0.175f, 0f);
            flange.transform.localScale = new Vector3(0.12f, 0.01f, 0.12f);
            flange.GetComponent<MeshRenderer>().material = blackMat;
            Object.DestroyImmediate(flange.GetComponent<Collider>());

            // C. Nắp chụp đầu cột (Top Cap)
            GameObject topCap = GameObject.CreatePrimitive(PrimitiveType.Cube);
            topCap.name = "Top_Cap";
            topCap.transform.SetParent(curtainRoot.transform, false);
            topCap.transform.localPosition = new Vector3(0f, 0.182f, 0f);
            topCap.transform.localScale = new Vector3(0.075f, 0.012f, 0.075f);
            topCap.GetComponent<MeshRenderer>().material = blackMat;
            Object.DestroyImmediate(topCap.GetComponent<Collider>());

            // D. Dải kính quang học mặt trước hướng về phía băng tải (Optical Lens Window)
            GameObject lens = GameObject.CreatePrimitive(PrimitiveType.Cube);
            lens.name = "Optical_Lens_Window";
            lens.transform.SetParent(curtainRoot.transform, false);
            lens.transform.localPosition = new Vector3(0f, 0f, -0.036f);
            lens.transform.localScale = new Vector3(0.045f, 0.32f, 0.005f);
            lens.GetComponent<MeshRenderer>().material = lensMat;
            Object.DestroyImmediate(lens.GetComponent<Collider>());

            // E. Dải mắt LED cảm biến quang hồng ngoại (Status Emitter Strip)
            GameObject emitter = GameObject.CreatePrimitive(PrimitiveType.Cube);
            emitter.name = "Emitter_Light_Strip";
            emitter.transform.SetParent(curtainRoot.transform, false);
            emitter.transform.localPosition = new Vector3(0f, 0f, -0.038f);
            emitter.transform.localScale = new Vector3(0.015f, 0.28f, 0.004f);
            emitter.GetComponent<MeshRenderer>().material = emitterLedMat;
            Object.DestroyImmediate(emitter.GetComponent<Collider>());

            // F. BoxCollider bao bọc toàn bộ cột cảm biến để phát hiện va chạm vật lý
            BoxCollider col = curtainRoot.AddComponent<BoxCollider>();
            col.center = Vector3.zero;
            col.size = new Vector3(0.10f, 0.36f, 0.10f);
            col.isTrigger = false;
        }

        Undo.RecordObject(curtainRoot.transform, "Update Safety_Light_Curtain Transform");
        // Tọa độ Unity: (-0.30m, 0.18m, -0.38m) nằm giữa băng tải và Thùng Đỏ, khớp 100% với ROS (X=-0.38m, Y=0.30m, Z=0.18m)
        curtainRoot.transform.position = new Vector3(-0.30f, 0.18f, -0.38f);
        curtainRoot.transform.rotation = Quaternion.identity;
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
