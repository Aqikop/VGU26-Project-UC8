# BÁO CÁO TIẾN ĐỘ TUẦN 03 (WEEK 03 REPORT)

- **Môn học:** Robotic Project - VGU
- **Đề tài:** Robotic Arm Conveyor Pick-and-Place with Obstacle Avoidance (UC8)
- **Giai đoạn:** Tuần 3 - Nối Unity với ROS & Lập kế hoạch theo vị trí vật thể (R3)
- **Ngày thực hiện:** 03/10/2026
- **Máy trạm thực nghiệm:** kduy-5560
- **Trạng thái:** **ĐẠT 100% (PASSED & VERIFIED)**

---

## 1. Kết quả kiểm thử tích hợp thực tế (End-to-End Test Results)

Hệ thống đã chạy thực nghiệm thành công với toàn bộ chuỗi mắt xích liên hoàn:

1. **Unity Simulation Engine:**
   * Script [`RandomObjectSpawner.cs`](file:///home/kduy/RoboticProject/project_blueprint/unity/UC8-Simulation/Assets/Scripts/RandomObjectSpawner.cs) sinh ngẫu nhiên các khối hộp 6cm màu Đỏ, Xanh, Vàng.
   * Script [`ConveyorController.cs`](file:///home/kduy/RoboticProject/project_blueprint/unity/UC8-Simulation/Assets/Scripts/ConveyorController.cs) vận hành kéo vật thể trôi ổn định ở tốc độ $0.3\text{ m/s}$.
   * Cảm biến [`PickZoneSensor.cs`](file:///home/kduy/RoboticProject/project_blueprint/unity/UC8-Simulation/Assets/Scripts/PickZoneSensor.cs) kích hoạt dừng băng chuyền và hãm đứng yên khối hộp ngay khi vật đi vào vùng gắp.

2. **Cầu nối TCP & Chuyển đổi tọa độ:**
   * Script [`ObjectLocalizationReporter.cs`](file:///home/kduy/RoboticProject/project_blueprint/unity/UC8-Simulation/Assets/Scripts/ObjectLocalizationReporter.cs) tính tọa độ vật so với `base_link`, chuyển đổi từ hệ trục thuận tay trái của Unity sang hệ trục FLU (Forward-Left-Up) của ROS và bắn qua `ROS-TCP-Connector`.
   * Gói [`ROS-TCP-Endpoint`](file:///home/kduy/RoboticProject/project_blueprint/ros_ws/src/ROS-TCP-Endpoint) trên cổng 10000 tiếp nhận và phân phối lên 2 topic:
     * `/detected_object_pose` (`geometry_msgs/Pose`)
     * `/detected_object_type` (`std_msgs/String`)

3. **Bộ não MoveIt Pre-grasp Planning:**
   * Node [`moveit_pregrasp_planner.py`](file:///home/kduy/RoboticProject/project_blueprint/ros_ws/src/uc8_robot_sorting/scripts/moveit_pregrasp_planner.py) bắt cặp đồng bộ tọa độ và nhãn màu.
   * Tính toán điểm tiếp cận Pre-grasp Pose an toàn lơ lửng trên đầu vật ($Z_{\text{pregrasp}} = Z_{\text{obj}} + 0.15\text{ m}$) với hướng kẹp cắm thẳng đứng (quaternion $[1, 0, 0, 0]$).
   * MoveIt tìm đường đi mượt mà không tự va chạm $\rightarrow$ Báo kết quả: **`PLAN TEST PASSED`** và hiển thị bóng quỹ đạo trên RViz!

---

## 2. Tiêu chí chuyển giao sang Tuần 04 (R4 / Milestone 1)

* **Hiện trạng hoàn thành:** Toàn bộ pipeline từ Mô phỏng vật lý $\rightarrow$ Nhận diện vị trí $\rightarrow$ Lập kế hoạch MoveIt đã thông suốt.
* **Mục tiêu Tuần 04:** 
  1. Kích hoạt thực thi chuyển động (Trajectory Execution): Gửi chuỗi góc khớp từ MoveIt sang Unity để cánh tay UR10e thật sự cử động theo quỹ đạo.
  2. Triển khai cơ chế kẹp/nhả vật (Grasping logic) bằng cơ chế Attach/Parenting.
  3. Xây dựng State Machine tuần tự 7 bước hoàn thiện chu trình Pick-and-Place tĩnh chuẩn bị nghiệm thu **Milestone 1 (W5)**.
