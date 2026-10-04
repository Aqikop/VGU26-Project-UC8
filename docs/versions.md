# BẢNG THEO DÕI PHIÊN BẢN CÔNG NGHỆ (VERSIONS PINNING)

- **Dự án:** UC8 - UR10e Robot Sorting & Obstacle Avoidance
- **Cập nhật gần nhất:** 03/10/2026

---

## 1. Môi trường Hệ điều hành & Runtime

| Thành phần | Phiên bản thực tế | Ghi chú |
| :--- | :--- | :--- |
| **Hệ điều hành** | Ubuntu 20.04.6 LTS (Focal Fossa) | Chạy native trực tiếp |
| **Kiến trúc CPU** | x86_64 | |
| **Python** | Python 3.8.10 | Mặc định của Ubuntu 20.04 |
| **ROS Distro** | ROS 1 Noetic Ninjemys | Target baseline |
| **Build Tool** | `catkin_tools` (`catkin build`) | Chuẩn hóa cho nhóm |

---

## 2. Phần mềm & Thư viện Mô phỏng

| Thành phần | Phiên bản mục tiêu | Ghi chú |
| :--- | :--- | :--- |
| **Unity Hub** | v3.x | Đã có sẵn trên máy |
| **Unity Editor** | 2022.3.x LTS | Phiên bản ổn định tương thích ROS-TCP-Connector |
| **ROS-TCP-Connector**| v0.7.0 (hoặc nhánh tương thích ROS1)| Cài đặt qua Unity Package Manager (Git URL) |
| **URDF Importer** | v0.5.2 | Import mô hình URDF vào Unity |

---

## 3. Các gói ROS chính (ROS Packages)

| Gói ROS | Phiên bản / Git Branch | Mục đích sử dụng |
| :--- | :--- | :--- |
| **MoveIt 1** | `ros-noetic-moveit` | Lập quỹ đạo, kiểm tra va chạm |
| **universal_robot** | `noetic-devel` | Mô hình URDF, mesh và moveit_config cho UR10e |
| **ros_tcp_endpoint**| `main` / `v0.7.0` | Node ROS nhận kết nối TCP từ Unity |
| **cv_bridge** | `ros-noetic-cv-bridge` | Chuyển đổi giữa ROS Image và OpenCV matrix |
| **OpenCV** | OpenCV 4.2+ (Python 3) | Nhận diện màu sắc và phân loại contour |
