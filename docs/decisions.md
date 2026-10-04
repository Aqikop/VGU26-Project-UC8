# QUYẾT ĐỊNH KIẾN TRÚC & PHẠM VI DỰ ÁN (DECISION LOG)

- **Dự án:** UC8 - Robotic Arm Conveyor Pick-and-Place with Obstacle Avoidance
- **Phiên bản:** 1.0 (Cập nhật sau trao đổi với Giảng viên)
- **Ngày ghi nhận:** 03/10/2026
- **Trạng thái:** Đã phê duyệt (Approved)

---

## 1. Danh sách quyết định kiến trúc đã chốt

### Q1: Môi trường triển khai (Simulation vs. Hardware)
* **Quyết định:** Giai đoạn chính hiện tại tập trung hoàn toàn vào môi trường mô phỏng **Unity 2022.3 LTS**. 
* **Tương lai:** Kiến trúc phần mềm phân tầng rõ ràng (ROS core + MoveIt độc lập với execution layer), sẵn sàng chuyển đổi sang cánh tay robot UR10e vật lý trong phòng lab nếu được cấp quyền và đủ thời gian.
* **Lý do:** Đảm bảo an toàn, tối ưu tốc độ thử nghiệm các thuật toán phức tạp (dynamic obstacle avoidance, continuous picking).

### Q2: Middleware và Nền tảng ROS
* **Quyết định:** Chốt dứt khoát sử dụng **ROS 1 Noetic** trên nền hệ điều hành **Ubuntu 20.04.6 LTS (Focal Fossa)**.
* **Lý do:** Tương thích trực tiếp, nguyên bản (native) trên hệ thống hiện tại, tính ổn định cao với MoveIt 1, hệ sinh thái gói hỗ trợ UR10e (`ur_description`, `ur10e_moveit_config`) và `ROS-TCP-Endpoint` đã hoàn thiện.

### Q3: Chế độ gắp trên băng chuyền (Continuous Picking - R9)
* **Quyết định:** **Continuous Picking (gắp vật khi băng chuyền đang di chuyển liên tục)** là yêu cầu **BẮT BUỘC** tại buổi nghiệm thu Final (W15).
* **Lộ trình thực hiện:**
  * **W5 (M1):** Pick-and-place trên bàn tĩnh (bước đệm vững chắc).
  * **W10 (M2):** Triển khai và nghiệm thu ở chế độ **Stop-and-Pick** để chốt mốc hệ thống tích hợp cơ bản.
  * **W11 - W14 (M3):** Phát triển bộ ước lượng vận tốc băng chuyền ($v$), thuật toán bù trễ và dự báo vị trí đón đầu $p_{\text{pick}} = p_{\text{last}} + v \cdot \Delta t$.
  * **W15 (Final):** Nghiệm thu chính thức Continuous Picking.

### Q4: Mô hình vật lý & Xử lý tiếp xúc (Friction vs. Algorithm)
* **Quyết định:** **Bỏ qua mô phỏng ma sát phức tạp** giữa ngón kẹp và vật thể; tập trung 100% năng lực vào phát triển thuật toán (Planning, Vision, Dynamic Obstacle Avoidance, Trajectory Interception, State Machine).
* **Cơ chế Grasping:** Áp dụng **Attach Logic / Constraint Parenting** trong Unity kết hợp với MoveIt `AttachedCollisionObject` ngay khi End-Effector đạt dung sai vị trí (tolerance window) cho phép.

### Q5: Đối tượng vật thể (Objects)
* **Quyết định:** Giai đoạn phát triển và nghiệm thu các mốc M1–M3 sử dụng **các khối lập phương (Cubes) có màu sắc (Red/Blue) và kích thước khác nhau**. 
* **Tương lai:** Sau khi thuật toán ổn định, có thể mở rộng thử nghiệm sang các mesh vật thể 3D phức tạp hơn.

---

## 2. Ma trận theo dõi tác động

| Quyết định | Tác động đến Unity (SIM) | Tác động đến ROS / MoveIt | Tác động đến Vision (VIS) | Tác động đến QA |
| :--- | :--- | :--- | :--- | :--- |
| **Ubuntu 20.04 + Noetic** | Dùng ROS-TCP-Connector ROS1 | Sử dụng MoveIt 1, build Catkin | Dùng `cv_bridge` ROS Noetic | Môi trường test native sạch |
| **Bỏ qua ma sát / Attach** | Script Attach/Detach theo trigger | Cập nhật `AttachedCollisionObject` | Không ảnh hưởng | Bỏ qua các ca trượt do PhysX |
| **Khối lập phương (Cubes)** | Model đơn giản, collider Box | Bounding box chuẩn xác | Thuật toán HSV + Bounding Box | Dễ thiết lập ground truth |
| **Continuous Picking (R9)** | Giữ belt chạy liên tục | Lập quỹ đạo đón đầu thời gian thực | Track ID và đo vận tốc $v$ | Cần đo sai số dự báo $\Delta p$ |
