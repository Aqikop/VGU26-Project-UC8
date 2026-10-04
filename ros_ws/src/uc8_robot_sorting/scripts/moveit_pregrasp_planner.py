#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Node Lập Kế Hoạch Pre-Grasp bằng MoveIt khi nhận được vị trí vật từ Unity.
Đã xử lý đồng bộ thời gian (Time-Sync) tránh hiện tượng nhãn màu đến trước tọa độ Pose.
Dự án: UC8 - Robotic Arm Conveyor Pick-and-Place with Obstacle Avoidance
Tuần: Week 03 / Requirement R3
"""

import sys
import threading
import time
import rospy
import moveit_commander
from geometry_msgs.msg import Pose, Point, Quaternion
from std_msgs.msg import String


class MoveItPreGraspPlanner:
    def __init__(self):
        # 1. Khởi tạo MoveIt Commander và ROS node
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node("moveit_pregrasp_planner", anonymous=False)

        rospy.loginfo("==================================================")
        rospy.loginfo("   UC8 - WEEK 03: MOVEIT PRE-GRASP PLANNER START  ")
        rospy.loginfo("==================================================")

        self.robot = moveit_commander.RobotCommander()
        self.scene = moveit_commander.PlanningSceneInterface()
        self.group = moveit_commander.MoveGroupCommander("manipulator")

        # Khóa dữ liệu đa luồng (Thread-safe)
        self.lock = threading.Lock()
        self.latest_pose = None
        self.latest_type = "Unknown"
        self.pose_time = 0.0
        self.type_time = 0.0
        self.is_planning = False

        # Độ cao an toàn trên đầu vật (15 cm)
        self.pregrasp_height = rospy.get_param("~pregrasp_height", 0.15)

        # Cấu hình nhóm MoveIt
        self.group.set_planning_time(5.0)
        self.group.set_num_planning_attempts(10)
        self.group.set_max_velocity_scaling_factor(0.2)
        self.group.set_max_acceleration_scaling_factor(0.2)
        self.group.allow_replanning(True)

        self.planning_frame = self.group.get_planning_frame()
        self.end_effector_link = self.group.get_end_effector_link() or "tool0"

        rospy.loginfo(f"[*] Planning Frame    : {self.planning_frame}")
        rospy.loginfo(f"[*] End-Effector Link : {self.end_effector_link}")
        rospy.loginfo(f"[*] Planning Group    : manipulator")
        rospy.loginfo(f"[*] Pre-grasp Offset Z: +{self.pregrasp_height} m")

        # 2. Đăng ký Subscriber nhận dữ liệu từ Unity
        rospy.Subscriber("/detected_object_pose", Pose, self.pose_callback, queue_size=5)
        rospy.Subscriber("/detected_object_type", String, self.type_callback, queue_size=5)

        rospy.loginfo("[*] Đang lắng nghe topics: /detected_object_pose & /detected_object_type...")

    def pose_callback(self, msg):
        with self.lock:
            self.latest_pose = msg
            self.pose_time = time.time()
            rospy.loginfo_throttle(2.0, f"[Pose Rx] Đã nhận tọa độ: X={msg.position.x:.3f}, Y={msg.position.y:.3f}, Z={msg.position.z:.3f}")

    def type_callback(self, msg):
        with self.lock:
            self.latest_type = msg.data
            self.type_time = time.time()

        if self.latest_type in ["Unknown", ""]:
            return

        # Đợi tối đa 0.3s để gói tin Pose (vận chuyển qua TCP) kịp cập nhật
        target_pose = None
        for _ in range(6):
            with self.lock:
                if self.latest_pose is not None and (time.time() - self.pose_time) < 3.0:
                    target_pose = self.latest_pose
                    break
            time.sleep(0.05)

        if target_pose is None:
            rospy.logwarn(f"[Planner] Nhận được màu '{self.latest_type}' nhưng chưa có Pose hợp lệ gần nhất! (Bỏ qua)")
            return

        if self.is_planning:
            rospy.logwarn("[Planner] Đang bận lập quỹ đạo cho vật trước, bỏ qua request mới.")
            return

        # Bắt đầu lập quỹ đạo
        self.is_planning = True
        self.plan_pregrasp(target_pose, self.latest_type)
        self.is_planning = False

    def plan_pregrasp(self, object_pose, object_type):
        rospy.loginfo(f"\n>>> [BẮT ĐẦU LẬP QUỸ ĐẠO MỤC TIÊU] Loại: {object_type}")
        rospy.loginfo(f"    Tọa độ vật: X={object_pose.position.x:.3f}, Y={object_pose.position.y:.3f}, Z={object_pose.position.z:.3f} m")

        # 1. Tính toán điểm Pre-grasp Pose
        pregrasp_pose = Pose()
        pregrasp_pose.position.x = object_pose.position.x
        pregrasp_pose.position.y = object_pose.position.y
        # CỘNG THÊM 15CM ĐỂ ĐỨNG LƠ LỬNG TRÊN ĐẦU VẬT THỂ
        pregrasp_pose.position.z = object_pose.position.z + self.pregrasp_height

        # GÓC CHÚC THẲNG ĐỨNG XUỐNG ĐẤT (Quaternion)
        pregrasp_pose.orientation = Quaternion(x=1.0, y=0.0, z=0.0, w=0.0)

        rospy.loginfo(f"    Điểm đón Pre-grasp: X={pregrasp_pose.position.x:.3f}, Y={pregrasp_pose.position.y:.3f}, Z={pregrasp_pose.position.z:.3f} m")

        # 2. Ra lệnh MoveIt tìm đường đi
        self.group.set_pose_target(pregrasp_pose)
        t_start = time.time()
        plan_result = self.group.plan()
        calc_time = time.time() - t_start

        success = False
        traj = None
        if isinstance(plan_result, tuple):
            success = plan_result[0]
            traj = plan_result[1]
        else:
            traj = plan_result
            success = len(traj.joint_trajectory.points) > 0

        if success and len(traj.joint_trajectory.points) > 0:
            num_points = len(traj.joint_trajectory.points)
            rospy.loginfo(f"  [+] KẾT QUẢ: LẬP QUỸ ĐẠO THÀNH CÔNG (SUCCESS)")
            rospy.loginfo(f"  [+] Thời gian tính toán : {calc_time:.3f} s")
            rospy.loginfo(f"  [+] Số điểm quỹ đạo     : {num_points} waypoints")
            rospy.loginfo(f"  [+] Trạng thái thực thi : Execute called = NO (Đúng tiêu chuẩn Tuần 3 plan-only)")
            rospy.loginfo("  [+] ==> PLAN TEST PASSED! <==\n")
        else:
            rospy.logwarn(f"  [-] KẾT QUẢ: THẤT BẠI - MoveIt không tìm thấy đường tới điểm gắp này.\n")

        self.group.clear_pose_targets()


def main():
    try:
        planner = MoveItPreGraspPlanner()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
    finally:
        moveit_commander.roscpp_shutdown()


if __name__ == "__main__":
    main()
