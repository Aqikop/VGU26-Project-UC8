using UnityEngine;

/// <summary>
/// Định nghĩa thuộc tính nhận diện của vật thể phân loại.
/// Dự án: UC8 - Robotic Arm Conveyor Pick-and-Place
/// Tuần: Week 04 (R4 - State and Sorting Management)
/// </summary>
public class SortableObject : MonoBehaviour
{
    public enum ColorType
    {
        Red,
        Blue,
        Yellow,
        Unknown
    }

    [Header("Object Classification Configuration")]
    [SerializeField] private ColorType objectType = ColorType.Unknown;

    [Tooltip("Marks whether the object has been sorted into a bin (no longer on conveyor belt)")]
    public bool isSorted = false;

    public ColorType ObjectType => objectType;

    /// <summary>
    /// Kiểm tra xem vật thể có thuộc các màu hợp lệ cần phân loại hay không.
    /// </summary>
    public bool IsRecognizedObject => objectType == ColorType.Red || 
                                     objectType == ColorType.Blue || 
                                     objectType == ColorType.Yellow;

    public void SetObjectType(ColorType type)
    {
        objectType = type;
    }
}
