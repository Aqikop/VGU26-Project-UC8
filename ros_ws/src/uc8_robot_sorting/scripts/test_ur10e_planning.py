#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script kiểm thử lập kế hoạch chuyển động cho robot UR10e qua MoveIt.
Thuộc tuần: Week 02 / Requirement R2
Dự án: UC8 - Robotic Arm Conveyor Pick-and-Place with Obstacle Avoidance
"""

import sys
import time
import rospy
import moveit_commander
from geometry_msgs.msg import Pose, Point, Quaternion

def run_tests():
    # 1. Khởi tạo node ROS và MoveIt Commander
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node("test_ur10e_planning", anonymous=True)

    print("\n==================================================")
    print("       UC8 - WEEK 02: UR10e MOVEIT PLANNING TEST  ")
    print("==================================================")

    robot = moveit_commander.RobotCommander()
    scene = moveit_commander.PlanningSceneInterface()
    group = moveit_commander.MoveGroupCommander("manipulator")

    # Đọc cấu hình
    planning_frame = group.get_planning_frame()
    eef_link = group.get_end_effector_link() or "tool0"
    
    print(f"[*] Planning Frame    : {planning_frame}")
    print(f"[*] End-Effector Link : {eef_link}")
    print(f"[*] Planning Group    : {group.get_name()}")
    print(f"[*] Current Joints    : {[round(j, 3) for j in group.get_current_joint_values()]}")

    # Cấu hình an toàn cho planner
    group.set_planning_time(5.0)
    group.set_num_planning_attempts(10)
    group.set_max_velocity_scaling_factor(0.2)
    group.set_max_acceleration_scaling_factor(0.2)

    # -----------------------------------------------------------
    # TEST 1: Mục tiêu hợp lệ trong không gian làm việc (Reachable)
    # -----------------------------------------------------------
    print("\n>>> BẮT ĐẦU TEST 1: Lập quỹ đạo tới vị trí hợp lệ (Pose A)")
    pose_target_a = Pose()
    pose_target_a.position = Point(x=0.45, y=-0.20, z=0.40)
    # Hướng gắp chúc thẳng xuống (quaternion: x=1.0, y=0.0, z=0.0, w=0.0)
    pose_target_a.orientation = Quaternion(x=1.0, y=0.0, z=0.0, w=0.0)

    group.set_pose_target(pose_target_a)
    
    t0 = time.time()
    plan_result = group.plan()
    dt = time.time() - t0

    # Tương thích giữa các phiên bản MoveIt (tuple hoặc RobotTrajectory)
    success_1 = False
    traj_1 = None
    if isinstance(plan_result, tuple):
        success_1 = plan_result[0]
        traj_1 = plan_result[1]
    else:
        traj_1 = plan_result
        success_1 = len(traj_1.joint_trajectory.points) > 0

    if success_1 and len(traj_1.joint_trajectory.points) > 0:
        pts = len(traj_1.joint_trajectory.points)
        print(f"  [+] KẾT QUẢ TEST 1: THÀNH CÔNG (PASSED)")
        print(f"  [+] Thời gian tính toán : {dt:.3f} s")
        print(f"  [+] Số điểm quỹ đạo     : {pts} waypoints")
        print(f"  [+] Trạng thái thực thi : KHÔNG GỬI LỆNH (Chế độ Plan-only an toàn)")
    else:
        print(f"  [-] KẾT QUẢ TEST 1: THẤT BẠI (FAILED) - Không tìm thấy đường đi")

    group.clear_pose_targets()
    time.sleep(1.0)

    # -----------------------------------------------------------
    # TEST 2: Mục tiêu bất khả thi ngoài tầm với (Unreachable Goal)
    # -----------------------------------------------------------
    print("\n>>> BẮT ĐẦU TEST 2: Mục tiêu ngoài tầm với (x=10.0m)")
    pose_unreachable = Pose()
    pose_unreachable.position = Point(x=10.0, y=0.0, z=0.50)
    pose_unreachable.orientation = Quaternion(x=1.0, y=0.0, z=0.0, w=0.0)

    group.set_pose_target(pose_unreachable)

    t0 = time.time()
    plan_result_2 = group.plan()
    dt_2 = time.time() - t0

    success_2 = False
    if isinstance(plan_result_2, tuple):
        success_2 = plan_result_2[0]
    else:
        success_2 = len(plan_result_2.joint_trajectory.points) > 0

    if not success_2:
        print(f"  [+] KẾT QUẢ TEST 2: THÀNH CÔNG (PASSED - Từ chối chính xác)")
        print(f"  [+] Thời gian phản hồi  : {dt_2:.3f} s (Đúng ngưỡng timeout 5s)")
        print(f"  [+] Hành vi an toàn     : Robot đứng yên an toàn, không phát sinh quỹ đạo nguy hiểm.")
    else:
        print(f"  [-] KẾT QUẢ TEST 2: THẤT BẠI (FAILED) - Hệ thống báo nhầm quỹ đạo ngoài tầm với")

    group.clear_pose_targets()

    print("\n==================================================")
    print("          KẾT THÚC BỘ KIỂM THỬ TUẦN 02 (R2)       ")
    print("==================================================\n")

    moveit_commander.roscpp_shutdown()

if __name__ == "__main__":
    try:
        run_tests()
    except rospy.ROSInterruptException:
        pass
