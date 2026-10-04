# HƯỚNG DẪN CÀI ĐẶT & THIẾT LẬP MÔI TRƯỜNG (SETUP GUIDE)

- **Dự án:** UC8 - UR10e Robot Sorting & Obstacle Avoidance
- **Mục tiêu:** Thiết lập nền tảng cho Tuần 02 (R2)

---

## 1. Cài đặt ROS Noetic trên Ubuntu 20.04

Chạy tuần tự các lệnh sau trong terminal:

```bash
# 1. Cấu hình nguồn phần mềm ROS
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'

# 2. Thiết lập apt key
sudo apt install -y curl
curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -

# 3. Cập nhật và cài đặt phiên bản ROS Desktop Full
sudo apt update
sudo apt install -y ros-noetic-desktop-full

# 4. Thiết lập biến môi trường tự động
echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
source ~/.bashrc

# 5. Cài đặt công cụ build và dependencies
sudo apt install -y python3-rosdep python3-rosinstall python3-rosinstall-generator python3-wstool build-essential python3-catkin-tools
sudo rosdep init
rosdep update
```

---

## 2. Cài đặt MoveIt 1 và Gói Robot UR10e

```bash
# Cài đặt MoveIt 1
sudo apt install -y ros-noetic-moveit

# Cài đặt gói điều khiển và mô hình Universal Robots
sudo apt install -y ros-noetic-ur-description ros-noetic-ur10e-moveit-config
```

---

## 3. Khởi tạo Catkin Workspace của dự án

```bash
# Di chuyển vào thư mục workspace
cd /home/kduy/RoboticProject/ros_ws

# Khởi tạo workspace bằng catkin_tools
catkin init
catkin config --extend /opt/ros/noetic
catkin build

# Thêm source workspace vào ~/.bashrc
echo "source /home/kduy/RoboticProject/ros_ws/devel/setup.bash" >> ~/.bashrc
source /home/kduy/RoboticProject/ros_ws/devel/setup.bash
```

---

## 4. Kiểm tra hoạt động (Smoke Test W2)

1. Mở terminal kiểm tra core:
   ```bash
   roscore
   ```
2. Mở terminal mới chạy demo MoveIt RViz của UR10e:
   ```bash
   roslaunch ur10e_moveit_config demo.launch
   ```
3. Trong giao diện RViz:
   - Fixed Frame chọn `base_link` hoặc `world`.
   - Trong tab **MotionPlanning**, chọn planning group: `manipulator`.
   - Chọn Goal State sang một tư thế ngẫu nhiên hoặc kéo tay robot, bấm **Plan & Execute**.
