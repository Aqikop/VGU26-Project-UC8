# QUY ƯỚC GIAO TIẾP TÍCH HỢP HỆ THỐNG (SYSTEM INTERFACES)

- **Dự án:** UC8 - UR10e Robot Sorting & Obstacle Avoidance
- **Phiên bản:** 1.0
- **Tài liệu tham chiếu:** Project_Guide.md - Section 05 & Bài 1.3

---

## 1. Nguyên tắc cốt lõi về tích hợp
1. **Phân biệt Command và Feedback:** Tách riêng chiều phát lệnh (Command) và chiều báo cáo trạng thái hoàn thành thực tế (Feedback). Không bao giờ coi "đã gửi lệnh" là "robot đã hoàn thành".
2. **Quy chuẩn hệ tọa độ (Frame Conversion):**
   * Unity sử dụng hệ tọa độ thuận tay trái (Left-Handed: X sang phải, Y hướng lên trên, Z hướng tới trước).
   * ROS sử dụng hệ tọa độ thuận tay phải (Right-Handed, chuẩn REP-103: X tới trước, Y sang trái, Z hướng lên trên).
   * **Quy tắc:** Mọi phép chuyển đổi hệ tọa độ giữa Unity và ROS chỉ được thực hiện tại một module duy nhất (`CoordinateConverter` trong Unity ROS-TCP-Connector hoặc ROS Endpoint), không tự ý đảo dấu rải rác trong nhiều script.
3. **Đơn vị chuẩn:**
   * Khoảng cách / Tọa độ: Mét ($\text{m}$).
   * Góc / Vận tốc góc: Radian ($\text{rad}$), $\text{rad/s}$.
   * Thời gian: Giây ($\text{s}$) gắn kèm ROS Timestamp (`std_msgs/Header`).

---

## 2. Bảng định nghĩa các Interface chính

| Interface | Chủ quản $\rightarrow$ Sử dụng | Message Type / Định dạng | Nội dung dữ liệu thống nhất |
| :--- | :--- | :--- | :--- |
| **Camera Raw Stream** | SIM (Unity) $\rightarrow$ VIS (ROS) | `sensor_msgs/Image` | Ảnh RGB từ camera top-down, độ phân giải $640 \times 480$, encoding `bgr8` hoặc `rgb8`, timestamp. |
| **Target Detections** | VIS $\rightarrow$ INT | `uc8_msgs/TargetDetection` (custom/standard) | Nhãn (`RED`/`BLUE`), tọa độ pixel tâm $(u, v)$, confidence, timestamp. |
| **Target 3D Pose** | VIS $\rightarrow$ ROS (MoveIt) | `geometry_msgs/PoseStamped` | Tọa độ không gian 3D của vật trong `base_link`, timestamp, Track ID, cờ hợp lệ (`is_valid`). |
| **Arm Trajectory Cmd** | ROS (MoveIt) $\rightarrow$ SIM (Unity) | `trajectory_msgs/JointTrajectory` | Thứ tự 6 khớp chuẩn của UR10e, vị trí góc (rad), vận tốc, thời gian đến từng waypoint. |
| **Arm State Feedback** | SIM (Unity) $\rightarrow$ ROS | `sensor_msgs/JointState` + Task Done | Giá trị góc quay thực tế của 6 khớp, trạng thái `is_executing`, `is_done`, `is_failed`. |
| **Gripper / Attach Cmd** | ROS $\rightarrow$ SIM (Unity) | `std_msgs/Bool` hoặc Service | `True` = Đóng kẹp / Bật Attach; `False` = Mở kẹp / Release. Phản hồi xác nhận trạng thái vật. |
| **Conveyor Control** | INT $\rightarrow$ SIM (Unity) | `uc8_msgs/ConveyorControl` | `run_cmd` (Start/Stop), tốc độ belt ($v$), chiều chuyển động. |
| **Conveyor Status** | SIM $\rightarrow$ INT | `uc8_msgs/ConveyorStatus` | Tình trạng belt (`RUNNING`/`STOPPED`), tốc độ thực tế đã dừng ổn định. |
| **Obstacle Stream** | SIM/Sensor $\rightarrow$ ROS | `moveit_msgs/CollisionObject` | ID vật cản, loại hình học (Box/Cylinder), kích thước, Pose theo `world`/`base_link`, timestamp. |
| **Health & Risk Monitor** | INT / Health Node | Heartbeat flag | Cờ `is_stale` (khi mất dữ liệu quá ngưỡng timeout), cờ cảnh báo rủi ro va chạm. |

---

## 3. Thứ tự 6 khớp chuẩn của UR10e
Khi gửi lệnh điều khiển và đọc feedback, bắt buộc cố định đúng thứ tự 6 khớp theo chuẩn URDF của Universal Robots:
1. `shoulder_pan_joint`
2. `shoulder_lift_joint`
3. `elbow_joint`
4. `wrist_1_joint`
5. `wrist_2_joint`
6. `wrist_3_joint`
