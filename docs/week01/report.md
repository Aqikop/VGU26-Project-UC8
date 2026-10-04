# BÁO CÁO TIẾN ĐỘ TUẦN 01 (WEEK 01 REPORT)

- **Môn học:** Robotic Project - VGU
- **Đề tài:** Robotic Arm Conveyor Pick-and-Place with Obstacle Avoidance (UC8)
- **Giai đoạn:** Tuần 1 - Khởi tạo & Chốt phạm vi (Scope & Organization)
- **Ngày báo cáo:** 03/10/2026
- **Trạng thái tuần 1:** **ĐẠT (DONE)**

---

## 1. Tóm tắt kết quả hoàn thành trong tuần 1
* **Hoàn thành Bài 1.1:** Xác định rõ ràng phạm vi, luồng dữ liệu, đầu vào - đầu ra và tiêu chí hoàn thành tại [docs/scope.md](file:///home/kduy/RoboticProject/docs/scope.md).
* **Hoàn thành Bài 1.2:** Đóng toàn bộ 5 câu hỏi mở sau khi trao đổi và thống nhất với Giảng viên tại [docs/decisions.md](file:///home/kduy/RoboticProject/docs/decisions.md):
  1. *Nền tảng:* Mô phỏng trên Unity 2022.3, cấu trúc module sẵn sàng chuyển đổi sang robot thật trong tương lai.
  2. *Middleware:* Chốt ROS 1 Noetic trên Ubuntu 20.04 native.
  3. *Continuous Picking (R9):* Xác nhận là yêu cầu bắt buộc ở Final (W15); M2 (W10) dùng Stop-and-Pick làm bước đệm.
  4. *Ma sát & Grasping:* Bỏ qua tính toán ma sát vật lý phức tạp, tập trung vào thuật toán; áp dụng cơ chế Attach logic.
  5. *Vật thể:* Chuẩn hóa khối lập phương (Cubes) có kích thước và màu sắc Red/Blue.
* **Hoàn thành Bài 1.3:** Thiết lập bảng quy ước giao tiếp tích hợp giữa Unity và ROS tại [docs/interfaces.md](file:///home/kduy/RoboticProject/docs/interfaces.md).
* **Hoàn thành Bài 1.4:** Phân rã 12 yêu cầu kỹ thuật (R1 đến R12) gắn liền 4 cột mốc W5, W10, W14, W15 tại [docs/backlog.md](file:///home/kduy/RoboticProject/docs/backlog.md).

---

## 2. Kế hoạch công việc Tuần 02 (W2 Plan / R2)
* **Mục tiêu:** Cài đặt nền tảng ROS 1 Noetic trên Ubuntu 20.04, thiết lập Catkin Workspace, nạp mô hình cánh tay robot UR10e (`ur_description`), cấu hình MoveIt 1 (`ur10e_moveit_config`) và kiểm thử lập kế hoạch chuyển động cơ bản trong RViz (Home $\rightarrow$ Pose A $\rightarrow$ Home).
* **Checklist chuẩn bị:**
  - [ ] Thêm kho apt của ROS Noetic và cài đặt `ros-noetic-desktop-full`.
  - [ ] Cài đặt các công cụ build: `python3-catkin-tools`, `python3-rosdep`, `python3-rosinstall`.
  - [ ] Khởi tạo catkin workspace tại `/home/kduy/RoboticProject/ros_ws`.
  - [ ] Clone các gói mô hình UR10e: `universal_robot` (nhánh noetic-devel).
  - [ ] Chạy launch RViz demo và ghi video kiểm thử Home $\rightarrow$ Pose A.
