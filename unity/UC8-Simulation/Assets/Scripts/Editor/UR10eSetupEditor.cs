using System.IO;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEditor;
using UnityEditor.SceneManagement;
using Unity.EditorCoroutines.Editor;
using Unity.Robotics.UrdfImporter;

namespace UC8.Editor
{
    public class UR10eSetupEditor
    {
        [MenuItem("UC8/Setup UR10e Robot in Scene", false, 1)]
        public static void SetupUR10eInScene()
        {
            if (EditorApplication.isPlaying)
            {
                EditorUtility.DisplayDialog("Error", "Please EXIT Play Mode before setting up the robot!", "OK");
                return;
            }

            GameObject existingRobot = GameObject.Find("ur10e") ?? GameObject.Find("ur10e_robot");
            if (existingRobot != null)
            {
                bool replace = EditorUtility.DisplayDialog("Notice", $"Robot '{existingRobot.name}' already exists in Scene. Do you want to delete and recreate standard configuration?", "Recreate", "Cancel");
                if (!replace) return;
                Undo.DestroyObjectImmediate(existingRobot);
            }

            string fullUrdfPath = Path.Combine(Application.dataPath, "Robots/UR10e/ur10e.urdf");
            if (!File.Exists(fullUrdfPath))
            {
                EditorUtility.DisplayDialog("Error", $"URDF file not found at:\n{fullUrdfPath}", "OK");
                return;
            }

            EditorCoroutineUtility.StartCoroutineOwnerless(ImportRobotCoroutine(fullUrdfPath));
        }

        private static IEnumerator ImportRobotCoroutine(string urdfPath)
        {
            EditorUtility.DisplayProgressBar("UR10e Setup", "Parsing URDF structure and meshes...", 0.2f);

            ImportSettings settings = ImportSettings.DefaultSettings();
            settings.chosenAxis = ImportSettings.axisType.yAxis;
            settings.convexMethod = ImportSettings.convexDecomposer.vHACD;

            // forceRuntimeMode = false to let Unity use native AssetDatabase
            IEnumerator<GameObject> importEnum = UrdfRobotExtensions.Create(urdfPath, settings, false, false);

            GameObject robotObject = null;
            while (importEnum.MoveNext())
            {
                if (importEnum.Current != null)
                {
                    robotObject = importEnum.Current;
                }
                yield return null;
            }

            EditorUtility.ClearProgressBar();

            if (robotObject == null)
            {
                EditorUtility.DisplayDialog("Error", "Failed to generate Robot from URDF!", "OK");
                yield break;
            }

            robotObject.name = "ur10e";
            robotObject.transform.position = Vector3.zero;
            robotObject.transform.rotation = Quaternion.identity;

            // 0. Lock robot base (immovable = true)
            ArticulationBody[] bodies = robotObject.GetComponentsInChildren<ArticulationBody>(true);
            foreach (ArticulationBody body in bodies)
            {
                if (body.isRoot || body.name == "base_link" || body.name == "ur10e" || body.name == "base_link_inertia" || body.name == "base")
                {
                    body.immovable = true;
                }
                else
                {
                    body.useGravity = false;
                }
            }

            // 1. Remove default URDF Importer scripts
            MonoBehaviour[] defaultScripts = robotObject.GetComponentsInChildren<MonoBehaviour>(true);
            foreach (var s in defaultScripts)
            {
                if (s != null && (s.GetType().Name == "Controller" || s.GetType().Name == "JointControl" || s.GetType().Name == "FKRobot"))
                {
                    Undo.DestroyObjectImmediate(s);
                }
            }

            // 2. Add UR10eController
            UR10eController controller = robotObject.GetComponent<UR10eController>();
            if (controller == null)
            {
                controller = robotObject.AddComponent<UR10eController>();
                Debug.Log("[UC8] Attached UR10eController to robot.");
            }

            // 3. Find tool0 or wrist_3_link and attach GripperController
            Transform tool0 = FindDeepChild(robotObject.transform, "tool0");
            if (tool0 == null)
            {
                tool0 = FindDeepChild(robotObject.transform, "wrist_3_link");
            }

            if (tool0 != null)
            {
                GripperController gripper = tool0.GetComponent<GripperController>();
                if (gripper == null)
                {
                    gripper = tool0.gameObject.AddComponent<GripperController>();
                    Debug.Log($"[UC8] Attached GripperController to link: {tool0.name}");
                }
            }

            Undo.RegisterCreatedObjectUndo(robotObject, "Create UR10e Robot");
            Selection.activeGameObject = robotObject;
            EditorSceneManager.MarkSceneDirty(robotObject.scene);

            EditorUtility.DisplayDialog("Success!", "Successfully created and configured UR10e robot with UR10eController and GripperController in Scene!\n\nPress Ctrl+S to save Scene.", "OK");
        }

        [MenuItem("UC8/Create 3 Sorting Bins in Scene", false, 2)]
        public static void CreateSortingBins()
        {
            if (EditorApplication.isPlaying)
            {
                EditorUtility.DisplayDialog("Error", "Please EXIT Play Mode before creating Bins!", "OK");
                return;
            }

            GameObject binsParent = GameObject.Find("SortingBins");
            if (binsParent != null)
            {
                Undo.DestroyObjectImmediate(binsParent);
            }

            binsParent = new GameObject("SortingBins");
            Undo.RegisterCreatedObjectUndo(binsParent, "Create Sorting Bins");

            CreateSingleBin(binsParent.transform, "Bin_Red",    new Vector3(-0.25f, 0.01f, -0.60f), new Color(0.9f, 0.15f, 0.15f));
            CreateSingleBin(binsParent.transform, "Bin_Blue",   new Vector3( 0.05f, 0.01f, -0.60f), new Color(0.15f, 0.45f, 0.95f));
            CreateSingleBin(binsParent.transform, "Bin_Yellow", new Vector3( 0.35f, 0.01f, -0.60f), new Color(0.95f, 0.85f, 0.15f));

            EditorSceneManager.MarkSceneDirty(binsParent.scene);
            EditorUtility.DisplayDialog("Success!", "Successfully created 3 Sorting Bins (Red, Blue, Yellow) in Scene!\n\nPress Ctrl+S to save Scene.", "OK");
        }

        private static void CreateSingleBin(Transform parent, string name, Vector3 pos, Color color)
        {
            GameObject binObj = new GameObject(name);
            binObj.transform.SetParent(parent);
            binObj.transform.position = pos;

            Material mat = new Material(Shader.Find("Standard"));
            mat.color = color;

            float w = 0.22f; // rộng
            float h = 0.08f; // cao thành thùng
            float t = 0.015f; // độ dày vách

            // Đáy thùng
            GameObject bottom = GameObject.CreatePrimitive(PrimitiveType.Cube);
            bottom.name = "Bottom";
            bottom.transform.SetParent(binObj.transform);
            bottom.transform.localPosition = new Vector3(0, 0.005f, 0);
            bottom.transform.localScale = new Vector3(w, 0.01f, w);
            bottom.GetComponent<Renderer>().material = mat;

            // 4 Thành thùng
            CreateWall(binObj.transform, "Wall_North", new Vector3(0, h / 2f, w / 2f), new Vector3(w, h, t), mat);
            CreateWall(binObj.transform, "Wall_South", new Vector3(0, h / 2f, -w / 2f), new Vector3(w, h, t), mat);
            CreateWall(binObj.transform, "Wall_East",  new Vector3(w / 2f, h / 2f, 0), new Vector3(t, h, w), mat);
            CreateWall(binObj.transform, "Wall_West",  new Vector3(-w / 2f, h / 2f, 0), new Vector3(t, h, w), mat);
        }

        private static void CreateWall(Transform parent, string name, Vector3 localPos, Vector3 scale, Material mat)
        {
            GameObject wall = GameObject.CreatePrimitive(PrimitiveType.Cube);
            wall.name = name;
            wall.transform.SetParent(parent);
            wall.transform.localPosition = localPos;
            wall.transform.localScale = scale;
            wall.GetComponent<Renderer>().material = mat;
        }

        private static Transform FindDeepChild(Transform parent, string childName)
        {
            foreach (Transform child in parent)
            {
                if (child.name.Equals(childName, System.StringComparison.OrdinalIgnoreCase))
                    return child;
                Transform result = FindDeepChild(child, childName);
                if (result != null)
                    return result;
            }
            return null;
        }
    }
}
