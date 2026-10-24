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

---

## 3. Deviation Log (as-built vs. plan) — added 2026-10-24, Week 6 close-out

All items are **pending instructor acknowledgement**. Only the instructor approves scope changes.

| ID | Planned | As built | Why / plan | Status |
|---|---|---|---|---|
| D1 | W6 = R5 (seeded spawner, belt status, 5-min run). R8 in W9-10 | Static guarding (shields, control box, Manhattan trajectories) built in W6; most R5 items not done | R5 closed in the follow-up sprint (seed done in code; belt status + 5-min run + `environment.csv` still open) | Open |
| D2 | R8: wall blocks direct path; OMPL (RRT-Connect, BiTRRT, PRM*) finds the detour; benchmark table; no-path handling | Hand-scripted 4-leg "Manhattan" fly-over with hardcoded apex heights (0.52 m / 0.60 m) + default RRTConnect for hops | Keep Manhattan as the *baseline row*; add OMPL benchmark (>=50 plans per planner per goal) and no-path hold before M2 (W10) | Open |
| D3 | Red/Blue objects (Q5) | Red/Blue/Yellow, 3 bins | Needs instructor sign-off; R6 detector must handle 3 hue ranges | Open |
| D4 | `interfaces.md`: `PoseStamped` + `uc8_msgs` types | As built: `/detected_object_pose` (`Pose`, no header), `/detected_object_type` (`String`), `/ur10e/gripper_command` (`Bool`) | Migrate to `PoseStamped` with frame/timestamp when the camera node is built (W7-8); `uc8_msgs` deferred | Open |
| D5 | Success = cube lifted / in bin (guide W4) | `grasp_success` / `place_success` in `trials.csv` are set when the command is *sent*, not from object-state feedback | Add Unity gripper/object status feedback; until then label results "command-complete" | Open |
| D6 | Q4: MoveIt `AttachedCollisionObject` while holding | No attach call found in `task_state_machine.py` | Add attach/detach around GRASP/RELEASE before M2 | Open |
| D7 | M2 at Session 10 | W6 slides said "Milestone 2 Defense (Weeks 07-08)" | Corrected to Session 10 | Closed |
| D8 | Reported results traceable to logs | W6 slides claimed 100% over 500+ trials, ISO 9283 pose accuracy, <120 ms collision rejection | `trials.csv`: 532/550 (96.7%); ISO-9283 and latency figures were never measured. Slides/report corrected | Closed |
