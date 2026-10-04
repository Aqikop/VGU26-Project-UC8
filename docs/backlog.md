# MA TRẬN YÊU CẦU & KẾ HOẠCH THỰC HIỆN (PRODUCT BACKLOG)

- **Dự án:** UC8 - UR10e Sorting & Obstacle Avoidance
- **Phiên bản:** 1.0

---

## 1. Ma trận 12 Yêu cầu Kỹ thuật (R1 – R12)

| Mã ID | Yêu cầu / Đầu ra kỹ thuật | Cột mốc | Tuần thực hiện | Tiêu chí nghiệm thu (Definition of Done) | Trạng thái hiện tại |
| :---: | :--- | :---: | :---: | :--- | :---: |
| **R1** | Scope, Architecture, Workflow & Quyết định cốt lõi | W1 | Tuần 1 | Bộ tài liệu `scope.md`, `decisions.md`, `interfaces.md` được phê duyệt. | **Done** |
| **R2** | Nạp mô hình UR10e & Planning qua MoveIt RViz | W2 | Tuần 2 | RViz nạp đúng UR10e; lập kế hoạch Home $\rightarrow$ Pose A $\rightarrow$ Home thành công không lỗi. | **Done** |
| **R3** | Bridge Unity $\leftrightarrow$ ROS truyền dữ liệu & lệnh 2 chiều | W3 | Tuần 3 | Truyền nhận Pose cube chính xác; map đúng 6 khớp; command & feedback riêng biệt. | **Done** |
| **R4** | Chu trình Pick-and-Place tĩnh cơ bản | **M1** | Tuần 4–5 | Gắp cube tĩnh và đặt vào bin ổn định $\ge 8/10$ trials; state machine có timeout. | Backlog |
| **R5** | Băng chuyền vận chuyển & Spawner sinh vật ngẫu nhiên | M2 | Tuần 6 | Băng chuyền chạy 5 phút không kẹt; spawner sinh Red/Blue có seed; lệnh Start/Stop/Reset ổn định. | Backlog |
| **R6** | Thị giác máy nhận dạng & phân loại màu Red/Blue | M2 | Tuần 7 | Xử lý ảnh camera tách đúng Red/Blue; test set gán nhãn đạt độ chính xác cao; tách detector & selector. | Backlog |
| **R7** | Định vị 3D vật thể sang hệ tọa độ robot (`base_link`) | M2 | Tuần 8 | Chuyển đổi pixel sang $(X, Y, Z)$ trong `base_link`; đo sai số 10 điểm so với ground truth $\le 20\text{ mm}$. | Backlog |
| **R8** | Lập kế hoạch né tránh vật cản tĩnh (Static Wall) | **M2** | Tuần 9–10 | MoveIt PlanningScene nhận diện Wall; quỹ đạo tự động vòng qua vật cản an toàn; báo no-path khi bị chặn. | Backlog |
| **R9** | Theo dõi, dự báo và gắp vật thể trên băng chuyền chuyển động | **Final** | Tuần 11, 14–15 | Ước lượng vận tốc $v$; dự báo vị trí đón đầu; gắp thành công khi belt di chuyển liên tục (Continuous Picking). | Backlog |
| **R10**| Cập nhật và đồng bộ vật cản động thời gian thực | M3 | Tuần 12 | Barrier di chuyển được cập nhật liên tục vào PlanningScene; phát hiện dữ liệu cũ (Stale timeout). | Backlog |
| **R11**| Phản ứng an toàn: Safe-Stop $\rightarrow$ Replan $\rightarrow$ Resume | **M3** | Tuần 13–14 | Khi barrier cắt ngang: phanh dừng (Hold) $\rightarrow$ lập lại đường đi mới từ trạng thái thực $\rightarrow$ tiếp tục thực hiện. | Backlog |
| **R12**| Tích hợp toàn diện hệ thống & Đóng gói bàn giao | **Final**| Tuần 15 | Bàn giao trọn gói mã nguồn (tag `final-demo`), tài liệu hướng dẫn chạy sạch (clean start), video demo và báo cáo. | Backlog |

---

## 2. Kế hoạch Milestones chi tiết

* **Milestone 1 (W5):** Nghiệm thu R1, R2, R3, R4 (Nền tảng Pick-and-Place).
* **Milestone 2 (W10):** Nghiệm thu R5, R6, R7, R8 (Phân loại & Tránh vật cản tĩnh, chế độ Stop-and-Pick).
* **Milestone 3 (W14):** Nghiệm thu R10, R11 (Phản ứng vật cản động với $\ge 20$ trials, đánh giá sơ bộ R9).
* **Milestone Final (W15):** Nghiệm thu hoàn thiện R9 (Continuous Picking) và R12 (Bàn giao sản phẩm cuối).
