# BÁO CÁO TIẾN ĐỘ TUẦN 04 (WEEK 04 REPORT)

- **Môn học:** Robotic Project - VGU
- **Đề tài:** Robotic Arm Conveyor Pick-and-Place with Obstacle Avoidance (UC8)
- **Giai đoạn:** Tuần 4 - Làm Pick-and-Place tĩnh cơ bản (R4 / Nghiệm thu Milestone 1)
- **Ngày thực hiện:** 03/10/2026
- **Trạng thái:** **HOÀN THÀNH TOÀN DIỆN VÀ NGHIỆM THU THÀNH CÔNG (PASSED & VERIFIED)**

---

## 1. Kết quả thực hiện theo 5 bài tập tuần 4

| Bài tập | Nội dung kỹ thuật | Đầu ra / Bằng chứng | Trạng thái |
| :---: | :--- | :--- | :---: |
| **Bài 4.1** | Thiết lập Scene & Chọn cơ chế Grasping | Script [`GripperController.cs`](file:///home/kduy/RoboticProject/project_blueprint/unity/UC8-Simulation/Assets/Scripts/GripperController.cs) (Attach/Parenting logic theo chỉ đạo GV) | **Done** |
| **Bài 4.2** | Định nghĩa cấu hình các tư thế và thùng chứa | File [`config/pick_place.yaml`](file:///home/kduy/RoboticProject/project_blueprint/config/pick_place.yaml) lưu tọa độ 3 Bins đối diện băng chuyền | **Done** |
| **Bài 4.3** | Nối Trajectory Execution sang Unity | Script [`UR10eController.cs`](file:///home/kduy/RoboticProject/project_blueprint/unity/UC8-Simulation/Assets/Scripts/UR10eController.cs) điều khiển 6 ArticulationBody theo `/joint_states`, khóa đế `immovable`, kháng trọng lực | **Done** |
| **Bài 4.4** | Xây dựng bộ điều phối State Machine 7 bước | Node [`task_state_machine.py`](file:///home/kduy/RoboticProject/project_blueprint/ros_ws/src/uc8_robot_sorting/scripts/task_state_machine.py) (READY $\rightarrow$ APPROACH $\rightarrow$ DESCENT $\rightarrow$ GRASP $\rightarrow$ LIFT $\rightarrow$ MOVE_TO_BIN $\rightarrow$ RELEASE $\rightarrow$ READY) | **Done** |
| **Bài 4.5** | Thu thập dữ liệu kiểm thử thực nghiệm | File log thực tế [`experiments/week04/trials.csv`](file:///home/kduy/RoboticProject/project_blueprint/experiments/week04/trials.csv): Ghi nhận các trials thành công 100% | **Passed** |

---

## 2. Chu trình điều phối 7 bước tối ưu (Optimized 7-Step Sequence)

```
[READY] ──► [APPROACH] ──► [DESCENT] ──► [GRASP] ──► [LIFT] ──► [MOVE_TO_BIN] ──► [RELEASE] ──► [READY]
 (Chờ sà)    (Pre-grasp)   (Hạ 15cm)    (Kẹp dính)   (Nhấc lên)    (Sang thùng)      (Thả vật)     (Về chờ)
```

1. **READY (Tư thế chờ tối ưu):** Cánh tay robot gập khủy chúc thẳng đầu gắp xuống, lơ lửng chờ sẵn ngay trên trạm gắp $Z = 0.38\text{ m}$. Không phải rút về điểm Home xa tít, rút ngắn 70% thời gian tiếp cận.
2. **APPROACH:** Tiếp cận điểm Pre-grasp ngay dưới đầu gắp.
3. **DESCENT:** Hạ thẳng đứng trục $Z$ xuống cự ly sát mặt vật.
4. **GRASP:** Bắn lệnh `/ur10e/gripper_command` = True $\rightarrow$ Unity ghim dính vật vào `tool0`, MoveIt đồng bộ `AttachedCollisionObject`.
5. **LIFT:** Nhấc bổng vật thẳng đứng lên $+15\text{ cm}$. Khối hộp rời khỏi trạm kích hoạt băng chuyền chạy tiếp cho hộp kế.
6. **MOVE_TO_BIN:** Vung tay sang phía đối diện băng chuyền, hạ vào miệng thùng chứa tương ứng (Red/Blue/Yellow Bin tại $X = -0.60\text{ m}$).
7. **RELEASE:** Bắn lệnh `/ur10e/gripper_command` = False $\rightarrow$ Unity thả vật rơi tự do vào thùng, MoveIt xóa object đính kèm. Đánh dấu `isSorted = true`.
8. **READY:** Robot rút tay lên và quay về tư thế chờ sẵn sàng trên đỉnh trạm gắp.

---

## 3. Kết quả đo đạc thực nghiệm (Benchmark Trials Data)

Dữ liệu trích xuất từ file nhật ký tự động [`experiments/week04/trials.csv`](file:///home/kduy/RoboticProject/project_blueprint/experiments/week04/trials.csv) sau khi hoàn thiện:

- **Tỷ lệ kẹp thành công (Grasp Success Rate):** **100%**
- **Tỷ lệ phân loại đúng thùng (Place Success Rate):** **100%**
- **Thời gian chu trình trung bình (Mean Cycle Time):** **~12.02 giây / vật thể** (đáp ứng xuất sắc ngưỡng thời gian thực < 30s của đề tài).
- **Vận tốc băng chuyền:** **0.3 m/s** (chạy dứt khoát, không bị delay).
- **Quy tắc điều phối:** Strict Single-Item Flow (chỉ 1 hộp trên băng tải tại một thời điểm, loại bỏ hoàn toàn hiện tượng dồn ứ va chạm).

---

## 4. Trả lời câu hỏi vấn đáp tuần 4

1. **Vì sao cần Pre-grasp và Lift pose?**
   * Giúp phân tách bài toán không gian tự do (chuyển động vung tay lớn giữa Vị trí chờ, Băng tải, Thùng chứa) khỏi chuyển động tiếp cận cục bộ. Điểm lơ lửng $+15\text{ cm}$ đảm bảo các ngón kẹp không va quẹt vào mép thùng, cạnh băng chuyền hoặc húc đổ các vật thể xung quanh.

2. **Vì sao không nên chờ bằng một thời gian cố định (fixed delay) rồi mặc định robot đã tới?**
   * Trong thực tế, thời gian di chuyển phụ thuộc vào độ dài quãng đường, thuật toán lập quỹ đạo và vận tốc tối đa của từng khớp. Dùng `sleep()` cố định sẽ dẫn đến rủi ro kẹp khi robot chưa tới nơi (gắp hụt) hoặc lãng phí thời gian chờ đợi. Hệ thống chuẩn bắt buộc phải dựa vào cờ hoàn thành quỹ đạo (`wait=True` hoặc action feedback).

3. **Cơ chế chống lật/đổ ragdoll trên ArticulationBody trong Unity:**
   * Đế robot (`base_link`) bắt buộc phải được thiết lập `immovable = true` để gắn chặt vào tọa độ thế giới. Tắt trọng lực `useGravity = false` trên các khớp cánh tay và nâng `stiffness`, `forceLimit` của `ArticulationDrive` để cánh tay kháng võng hoàn hảo.
