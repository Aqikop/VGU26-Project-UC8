# BÁO CÁO TIẾN ĐỘ TUẦN 02 (WEEK 02 REPORT)

- **Môn học:** Robotic Project - VGU
- **Đề tài:** Robotic Arm Conveyor Pick-and-Place with Obstacle Avoidance (UC8)
- **Giai đoạn:** Tuần 2 - Nền tảng ROS & Robot UR10e (R2)
- **Ngày thực hiện:** 03/10/2026
- **Trạng thái:** **ĐẠT (DONE)**

---

## 1. Kết quả thực hiện theo 5 bài tập tuần 2

| Bài tập | Mô tả | Đầu ra / Bằng chứng | Trạng thái |
| :---: | :--- | :--- | :---: |
| **Bài 2.1** | Chuẩn bị môi trường Ubuntu 20.04 & ROS Noetic | Ubuntu 20.04.6 LTS native, Python 3.8.10, ROS Noetic | **Done** |
| **Bài 2.2** | Thiết lập Catkin Workspace & package `uc8_robot_sorting` | `project_blueprint/ros_ws` build sạch trong 2.7s | **Done** |
| **Bài 2.3** | Cấu hình tham số robot baseline MoveIt | Lưu tại [`config/robot_baseline.yaml`](file:///home/kduy/RoboticProject/project_blueprint/config/robot_baseline.yaml) | **Done** |
| **Bài 2.4** | Lập kế hoạch MoveIt RViz (Home $\rightarrow$ Pose A) | Script [`test_ur10e_planning.py`](file:///home/kduy/RoboticProject/project_blueprint/ros_ws/src/uc8_robot_sorting/scripts/test_ur10e_planning.py) | **Done** |
| **Bài 2.5** | Kiểm thử an toàn mục tiêu ngoài tầm với (Unreachable) | Bằng chứng tại [`evidence/unreachable_goal_test.txt`](file:///home/kduy/RoboticProject/project_blueprint/docs/week02/evidence/unreachable_goal_test.txt) | **Done** |

---

## 2. Bảng kết quả kiểm thử Pose Goals

| Tình huống kiểm thử | Vị trí mục tiêu $(X, Y, Z)$ [m] | Kết quả Planning | Thời gian tính toán | Số điểm quỹ đạo | Thực thi (Execution) | Kết luận an toàn |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Test 1: Pose A (Reachable)** | $(0.45, -0.20, 0.40)$ | **SUCCESS** | **0.134 s** | **12 waypoints** | Không (Plan-only) | Quỹ đạo mượt mà, hợp lệ |
| **Test 2: Out of reach** | $(10.0, 0.0, 0.50)$ | **FAILED (Timeout)** | **5.087 s** (đúng timeout) | $0$ points | Không gửi lệnh | Robot đứng yên an toàn |

---

## 3. Trả lời câu hỏi vấn đáp tuần 2

1. **URDF cung cấp gì cho MoveIt?**
   * Mô hình động học (Kinematics) của 6 khớp và các mắt xích liên kết.
   * Giới hạn góc quay, vận tốc và gia tốc của từng khớp (`joint_limits`).
   * Hình học va chạm 3D (`collision meshes`) để MoveIt kiểm tra tự va chạm trong quá trình chuyển động.

2. **RViz chuyển động có chứng minh robot Unity đã chạy không?**
   * **Không.** Trong Tuần 2, RViz mới chỉ hiển thị kết quả giả lập (fake execution) trên máy tính bằng `fake_controller`. Chưa có kết nối mạng hay bộ điều khiển vật lý nào gửi tín hiệu thực thi sang Unity. Điều này sẽ được hiện thực hóa ở Tuần 3 và Tuần 4.
