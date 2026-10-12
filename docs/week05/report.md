# BÁO CÁO NGHIỆM THU MILESTONE 1 (TUẦN 05) & KẾ HOẠCH TUẦN 06 / MILESTONE 2

- **Môn học:** Robotic Project — Vietnamese-German University (VGU)
- **Đề tài:** Robotic Arm Conveyor Pick-and-Place with Obstacle Avoidance (UC8)
- **Giai đoạn:** Tuần 5 — Nghiệm thu chính thức Milestone 1 (Yêu cầu R1, R2, R3, R4)
- **Hệ thống:** UR10e (6-DOF Manipulator) + Băng chuyền 3.6m + Bộ kẹp cơ khí 2 ngón + 3 Thùng phân loại
- **Nền tảng kỹ thuật:** Unity 2022.3 LTS (PhysX 4.x / ArticulationBody) + ROS Noetic (MoveIt) + ROS-TCP-Endpoint
- **Trạng thái:** **NGHIỆM THU THÀNH CÔNG 100% (PASSED & VERIFIED)**

---

## 1. Tổng hợp Nghiệm thu 4 Yêu cầu Cốt lõi của Milestone 1 (R1 – R4)

| Mã ID | Yêu cầu kỹ thuật | Tiêu chí nghiệm thu (DoD) | Kết quả thực nghiệm đạt được | Trạng thái |
| :---: | :--- | :--- | :--- | :---: |
| **R1** | Scope, Architecture, Workflow & Quyết định cốt lõi | Tài liệu phê duyệt kiến trúc 2 chiều, Option 1 Workcell Layout | Hệ thống khép kín Unity $\leftrightarrow$ ROS-TCP $\leftrightarrow$ MoveIt $\leftrightarrow$ State Machine hoạt động ổn định | **Passed** |
| **R2** | Nạp mô hình UR10e & Planning qua MoveIt RViz | Lập kế hoạch Home $\rightarrow$ Pick $\rightarrow$ Place không va chạm | MoveIt điều phối quỹ đạo mượt mà, khử điểm kỳ dị bằng khóa cổ tay $90^\circ$ | **Passed** |
| **R3** | Bridge Unity $\leftrightarrow$ ROS truyền dữ liệu & lệnh 2 chiều | Stream `/joint_states` 50 Hz, nhận Pose 10 Hz, không trễ mạng | Khóa đế `immovable`, kháng trọng lực, streaming 50 Hz mượt mà tới 6 ArticulationBodies | **Passed** |
| **R4** | Chu trình Pick-and-Place tĩnh khép kín & phân loại | Gắp cube và đặt vào 3 bins $\ge 8/10$ trials, State Machine tự động | **70/70 chu kỳ thành công ($100.0\%$)**, chu kỳ trung bình **$11.23\text{s}$** (nhanh gấp 2.7 lần yêu cầu $<30\text{s}$) | **Passed** |

---

## 2. Cập nhật Phản hồi của Giảng viên & Giải pháp Kỹ thuật Đã Triển khai

Trong quá trình chuẩn bị bảo vệ Milestone 1, nhóm đã tiếp thu 3 phản hồi kỹ thuật từ Giảng viên hướng dẫn và xử lý triệt để:

### 2.1. Phản hồi 1: Thiết kế & Tích hợp Bộ kẹp cơ khí 2 ngón (Industrial 2-Finger Claw)
- **Đề xuất của GV:** Cần có mô hình kẹp gắp cơ khí trực quan trên đầu `tool0`, không dùng điểm tiếp xúc ảo trừu tượng.
- **Giải pháp:** Thiết kế và xây dựng bộ kẹp công nghiệp procedural (`VisualClaw`):
  - Mặt bích kết nối (Flange Mount Adapter): $1.2\text{cm}$.
  - Thân bộ truyền động (Chassis Housing): $2.0\text{cm}$ với đèn LED chỉ thị trạng thái 2 màu (Xanh lơ khi chờ, Xanh lục bảo khi đã kẹp).
  - Hai cụm ngón kẹp hợp kim nhôm ($4.0\text{cm}$) tích hợp đệm cao su chịu ma sát ($3.2\text{cm}$), trượt mở/khép mượt mà ($9.2\text{cm} \to 6.1\text{cm}$).

### 2.2. Phản hồi 2: Khắc phục hiện tượng trôi lọt/bỏ sót hộp (Missed Cubes)
- **Vấn đề phát hiện:** Khi chạy dòng chảy liên tục (Multi-Item Flow), đôi lúc xảy ra hiện tượng bỏ sót hộp do cơ chế va chạm trigger (`OnTriggerEnter`) bị rớt frame.
- **Giải pháp:** Thay thế toàn bộ trigger thụ động bằng thuật toán quét chủ động đa luồng `FindLeadingCubeOnConveyor()` trong `PickZoneSensor.cs`. Bổ sung chốt an toàn dừng băng tải nếu có phôi đang chờ tại trạm ($X \ge -0.015\text{m}$), đạt độ tin cậy đón phôi $100\%$.

### 2.3. Phản hồi 3: Khắc phục hiện tượng lún băng chuyền & xoay lệch hộp khi gắp
- **Vấn đề phát hiện:** Khi hạ kẹp, đầu ngón kẹp bị cấn lún xuống mặt băng chuyền; khi kẹp thì khối hộp bị giật xoay lệch một góc chéo ($13.6^\circ$).
- **Giải pháp:**
  1. Chuẩn hóa góc chúc xuống: Đổi `down_orientation = Quaternion(0.7071068, 0.7071068, 0, 0)` trong `task_state_machine.py`. Các trục của kẹp vuông góc tuyệt đối $100\%$ với các mặt phẳng của hộp và băng tải.
  2. Nâng khoảng sáng gầm an toàn: Đặt `grasp_offset_z = 0.065m` và ngón nhôm $4.0\text{cm}$, giúp đầu ngón kẹp **dừng lơ lửng cách mặt băng chuyền tới $2.3\text{cm}$** (triệt tiêu hoàn toàn hiện tượng lún).
  3. Cơ chế Parenting bảo toàn: Sử dụng `attachedObject.transform.SetParent(attachPoint, true)` giữ nguyên $100\%$ vị trí và góc quay tự nhiên của khối hộp trên băng tải, loại bỏ hoàn toàn hiện tượng xoay hay xê dịch.

---

## 3. Kết quả Đo đạc Thực nghiệm (70 Chu kỳ QA Benchmark)

Dữ liệu ghi nhận từ file log thực tế [`experiments/week04/trials.csv`](file:///home/kduy/RoboticProject/project_blueprint/experiments/week04/trials.csv):
- **Tổng số chu kỳ thử nghiệm:** **70 chu kỳ liên tiếp** (vượt chỉ tiêu $\ge 10$ trials của M1 tới 700%).
- **Tỷ lệ kẹp thành công (Grasp Success Rate):** **100.0% (70 / 70)**.
- **Tỷ lệ phân loại đúng thùng (Place Success Rate):** **100.0% (70 / 70)**.
- **Thời gian chu trình trung bình (Mean Cycle Time):** **11.23 giây / chu kỳ** (Nhanh nhất: 10.8s, Chậm nhất: 12.1s).
- **Vận tốc băng chuyền:** **0.30 m/s** ổn định tuyệt đối.
- **Độ lệch điểm dừng hãm ma sát tự nhiên:** $\mathbf{\pm 3\text{ mm}}$ quanh tâm trạm gắp $X = 0.00\text{m}$.

---

## 4. Kế hoạch Tuần 06 (Khởi động Chu kỳ Milestone 2)

Sau khi hoàn tất bảo vệ Milestone 1 tại Tuần 5, nhóm bước vào Tuần 6 với các mục tiêu kỹ thuật trọng tâm nhằm đáp ứng **Yêu cầu R5**:

1. **Vận hành Băng chuyền & Spawner liên tục (Requirement R5):**
   - Kiểm thử độ ổn định dài hạn: Băng chuyền chạy liên tục $> 5$ phút không kẹt, không rớt vật thể, không rò rỉ bộ nhớ.
   - Cơ chế Spawner có tham số Seed (PRNG Seed Determinism): Cho phép tái lập chính xác $100\%$ chuỗi sinh phôi (ví dụ: Đỏ $\to$ Xanh $\to$ Vàng) để phục vụ kiểm thử hồi quy tự động.
   - Điều khiển dải vận tốc linh hoạt ($0.1\text{m/s} - 0.5\text{m/s}$) thông qua ROS parameter service.
2. **Cơ chế Phục hồi Lỗi Tự động (Autonomous Fault Recovery):**
   - Thuật toán tự đảo chiều/dọn kẹt (Reverse-and-Clear) nếu xảy ra tắc nghẽn bất thường trên băng tải.
   - Rollback trạng thái an toàn nếu bị rớt frame dữ liệu từ perception.

---

## 5. Lộ trình Chiến lược Milestone 2 (Tuần 10)

Milestone 2 (W10) đánh dấu bước chuyển mình quan trọng từ hệ thống tĩnh sang bài toán phân loại thông minh và né tránh vật cản:

1. **Yêu cầu R5:** Băng chuyền vận hành công nghiệp & sinh vật thể liên tục.
2. **Yêu cầu R6 (Thị giác máy phân loại màu):**
   - Thay thế việc đọc metadata bằng module Camera Perception thời gian thực.
   - Áp dụng thuật toán phân đoạn màu OpenCV HSV / Classifier nhận diện chính xác 3 màu Đỏ, Xanh dương, Vàng dưới các điều kiện ánh sáng khác nhau.
3. **Yêu cầu R7 (Định vị 3D sang tọa độ `base_link`):**
   - Hiệu chuẩn Hand-Eye Calibration giữa Camera và Robot.
   - Chuyển đổi tọa độ tâm vật thể từ ảnh pixel sang tọa độ 3D $(X, Y, Z)$ trong hệ quy chiếu `base_link` với sai số đo đạc $\le 20\text{mm}$.
4. **Yêu cầu R8 (Lập kế hoạch né tránh vật cản tĩnh - Static Obstacle Avoidance):**
   - Bố trí bức tường cản tĩnh (Static Wall Barrier) chắn giữa trạm gắp và các thùng phân loại.
   - Cập nhật vật cản vào MoveIt PlanningScene; thuật toán OMPL tự động tìm đường vòng an toàn vượt qua bức tường mà không va chạm.
   - Nghiệm thu trong chế độ **Stop-and-Pick** (băng chuyền dừng lại trước khi gắp).
