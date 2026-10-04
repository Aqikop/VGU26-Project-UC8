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

        // Tự động tạo và cập nhật các quả cầu Waypoint Visual Markers tại vị trí mới
        EnsureWaypointMarkers();

        if (changed)
        {
            EditorSceneManager.MarkAllScenesDirty();
            Debug.Log("<color=green>[WorkcellLayout] Successfully applied Option 1 layout and updated Waypoint Visual Markers in Unity Scene!</color>");
        }
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
