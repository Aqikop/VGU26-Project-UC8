# PHẠM VI DỰ ÁN & ĐẶC TẢ YÊU CẦU (SCOPE & REQUIREMENTS)

- **Đề tài:** Robotic Arm Conveyor Pick-and-Place with Obstacle Avoidance (UC8)
- **Mã môn học / Khóa:** Project Course - Vietnamese-German University (VGU)
- **Phiên bản:** 1.0 (Dựa trên Project_Guide.md v3.1)

---

## 1. Mô tả tổng quan sản phẩm

Hệ thống tự động hóa sử dụng cánh tay robot công nghiệp 6 bậc tự do **Universal Robots UR10e** để phát hiện, phân loại theo màu sắc (Đỏ / Xanh), gắp và phân chia các vật thể từ băng chuyền vào các thùng chứa (Bins) tương ứng, đồng thời có khả năng né tránh các vật cản tĩnh và động trong không gian làm việc.

```
+---------------+     Lựa chọn Red/Blue      +---------------------+
| Operator (UI) | -------------------------> |  Hệ thống Task INT  |
+---------------+                            +---------------------+
                                                        |
+-------------------+      Camera Stream                v
| Băng chuyền Unity | ---------------------> +---------------------+
| (Spawn Red/Blue)  |                        | Perception & Vision |
+-------------------+                        +---------------------+
         |                                              |  Target Pose (Base frame)
         v                                              v
+-------------------+    Trajectory / Execution      +---------------------+
| Robot UR10e Unity | <---------------------------- | MoveIt Planning     |
| (Gắp -> Đặt Bins) | ----------------------------> | (Tránh vật cản)     |
+-------------------+         Joint States           +---------------------+
```

---

## 2. Đầu vào - Đầu ra của hệ thống

* **Đầu vào (Inputs):**
  * Lựa chọn loại vật phẩm cần gắp từ phía Operator (Target Type: RED hoặc BLUE).
  * Luồng hình ảnh RGB từ Camera gắn cố định phía trên băng chuyền (`sensor_msgs/Image`).
  * Trạng thái góc quay các khớp của robot từ Unity (`sensor_msgs/JointState`).
  * Dữ liệu vị trí/hình học của vật cản tĩnh (bức tường/wall) và vật cản động (barrier).
* **Đầu ra (Outputs):**
  * Vật thể mục tiêu được gắp thành công và đặt an toàn vào đúng thùng chứa chỉ định (Red Bin / Blue Bin).
  * Chuỗi quỹ đạo chuyển động an toàn không va chạm (`trajectory_msgs/JointTrajectory`).
  * Lệnh điều khiển dừng an toàn (Safe-stop / Hold) khi phát hiện nguy cơ va chạm khẩn cấp.
  * Nhật ký kiểm thử, số liệu thời gian chu trình (Cycle time), tỷ lệ gắp thành công (Success rate).

---

## 3. Tiêu chí thành công và nghiệm thu

* **Tính đúng đắn phân loại (Sorting Success):** Vật thể được đưa vào đúng bin theo màu đã chọn; vật không thuộc mục tiêu (non-target) được bỏ qua không gắp.
* **An toàn va chạm (Zero Collision):** Không xảy ra bất kỳ va chạm ngoài ý muốn nào giữa tay máy/vật đang kẹp với môi trường, băng chuyền hay vật cản.
* **Khả năng phục hồi (Recovery):** Khi đường đi bị vật cản cắt ngang, hệ thống tự động phanh dừng kịp thời (Safe-stop), tính toán đường đi vòng thay thế (Replan) và hoàn tất nhiệm vụ khi an toàn (Resume).
* **Khả năng tái lập (Reproducibility):** Bất kỳ thành viên nào trong nhóm hoặc giảng viên đều có thể khởi động lại hệ thống từ trạng thái sạch (clean state) theo đúng tài liệu Runbook.

---

## 4. Bốn cột mốc nghiệm thu chính (Milestone Roadmap)

1. **W5 / Milestone 1 (M1) - Pick-and-Place tĩnh:**
   * Nghiệm thu chu trình gắp và đặt một cube tĩnh vào bin.
   * State Machine cơ bản có timeout và cơ chế xử lý lỗi.
   * Chứng minh việc tùy biến thành công từ tutorial gốc của Unity Robotics Hub sang UR10e.

2. **W10 / Milestone 2 (M2) - Sorting & Tránh vật cản tĩnh:**
   * Tích hợp băng chuyền vận hành sinh vật Red/Blue ngẫu nhiên.
   * Thị giác máy nhận diện phân loại màu và định vị 3D sang `base_link`.
   * Tránh bức tường cản tĩnh (Static Wall).
   * Chế độ nghiệm thu mốc này: **Stop-and-Pick** (dừng belt tại pick zone trước khi gắp).

3. **W14 / Milestone 3 (M3) - Phản ứng vật cản động:**
   * Đồng bộ vật cản chuyển động thời gian thực vào PlanningScene.
   * Cơ chế giám sát rủi ro (Risk Monitor) $\rightarrow$ Safe Stop $\rightarrow$ Replan $\rightarrow$ Resume.
   * Bộ kiểm thử $\ge 20$ trials với ma trận kịch bản đa dạng.

4. **W15 / Final Acceptance - Toàn diện sản phẩm:**
   * Nghiệm thu chế độ **Continuous Picking (gắp trên băng chuyền đang chuyển động)**.
   * Đóng gói toàn bộ source code, config, runbook, video bằng chứng và báo cáo tổng kết.

---

## 5. Ranh giới phạm vi (Scope Boundaries)
* **Hiện tại (Current Scope):** Toàn bộ hoạt động diễn ra trong môi trường mô phỏng Unity 2022.3 và ROS Noetic.
* **Mở rộng tương lai (Future Scope):** Tách biệt các layer để có thể nạp config driver UR10e thật (`ur_robot_driver`) khi được chấp thuận trong lab.
