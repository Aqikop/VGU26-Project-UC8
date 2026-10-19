#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Task State Machine for Pick-and-Place Cycle.
Manages the 7-step sequence: IDLE -> APPROACH -> DESCENT -> GRASP -> LIFT -> PLACE -> RELEASE -> HOME.
Automatically syncs with MoveIt PlanningScene and logs trials to CSV.
Project: UC8 - Robotic Arm Conveyor Pick-and-Place with Obstacle Avoidance
"""

import os
import sys
import csv
import time
import threading
import rospy
import moveit_commander
from geometry_msgs.msg import Pose, PoseStamped, Point, Quaternion
from std_msgs.msg import String, Bool


class TaskStateMachine:
    def __init__(self):
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node("task_state_machine", anonymous=False)

        rospy.loginfo("==================================================")
        rospy.loginfo("   UC8 - WEEK 04: TASK STATE MACHINE START        ")
        rospy.loginfo("==================================================")

        self.robot = moveit_commander.RobotCommander()
        self.scene = moveit_commander.PlanningSceneInterface()

        rospy.loginfo("[*] Connecting to MoveIt MoveGroup ('manipulator')...")
        self.group = None
        for attempt in range(1, 16):
            try:
                self.group = moveit_commander.MoveGroupCommander("manipulator")
                rospy.loginfo("[*] MoveGroup ('manipulator') connected successfully.")
                break
            except RuntimeError as e:
                rospy.loginfo(f"[*] Waiting for /move_group action server... (attempt {attempt}/15)")
                time.sleep(2.0)

        if self.group is None:
            rospy.logerr("[-] Timed out waiting for MoveGroup after 30 seconds!")
            sys.exit(1)

        # Speed scaling factor (Multiplier > 1.0 increases robot motion speed)
        # Default: 1.8x speed boost (configurable via ROS param ~speed_multiplier)
        self.speed_multiplier = rospy.get_param("~speed_multiplier", 1.8)
        rospy.loginfo(f"[*] Arm Speed Multiplier: {self.speed_multiplier:.1f}x")

        # Safety configuration - max limits enabled for speed scaling
        self.group.set_planning_time(5.0)
        self.group.set_num_planning_attempts(10)
        self.group.set_max_velocity_scaling_factor(1.0)
        self.group.set_max_acceleration_scaling_factor(1.0)
        self.group.allow_replanning(True)

        self.planning_frame = self.group.get_planning_frame()
        self.eef_link = self.group.get_end_effector_link() or "tool0"

        # Multi-threading management
        self.lock = threading.Lock()
        self.latest_pose = None
        self.latest_type = None
        self.pose_time = 0.0
        self.is_busy = False

        # Altitude configuration parameters
        self.pregrasp_offset_z = 0.16 # 16cm above object center (hovering 10cm above cube top)
        self.grasp_offset_z = 0.065   # 6.5cm above object center (fingertips clear conveyor by 2.3cm, zero sinking)
        self.lift_offset_z = 0.16     # Lift 16cm after grasp
        # Optimal STANDBY joint pose (Wrist points strictly 90 degrees downward):
        # Shoulder and elbow elevated, avoiding table and conveyor collisions
        # tool0 points vertically downward onto pick zone (X = -0.60m, Z = 0.42m)
        self.standby_joints = [0.2945, -1.4760, -2.1278, -1.1022, 1.5708, 0.5291]

        # Orientation strictly orthogonal to conveyor and cubes (Z down, X along conveyor, Y across):
        self.down_orientation = Quaternion(x=0.7071068, y=0.7071068, z=0.0, w=0.0)

        # Coordinates for the 3 sorting bins in Option 1 (Front Pick - Flanking Bins):
        # - Red Bin: Robot Left (y = +0.55m)
        # - Yellow Bin: Robot Right (y = -0.55m)
        # - Blue Bin: Robot Rear (x = +0.50m)
        self.bin_positions = {
            "Red":    Point(x=-0.10, y= 0.55, z=0.20),
            "Blue":   Point(x= 0.50, y= 0.00, z=0.20),
            "Yellow": Point(x=-0.10, y=-0.55, z=0.20)
        }
        # Optimal non-singular joint configurations for the 3 sorting bins:
        # Arm profile remains constant, ONLY shoulder_pan_joint rotates like a crane
        self.bin_joints = {
            "Red":    [-1.0741, -1.4731, -2.2727, -0.9602, 1.5708, 0.5291], # X = -0.10m, Y = +0.55m
            "Yellow": [ 1.7077, -1.4731, -2.2727, -0.9602, 1.5708, 0.5291], # X = -0.10m, Y = -0.55m
            "Blue":   [-2.7858, -1.3576, -2.3651, -0.9833, 1.5708, 0.5291]  # X = +0.50m, Y =  0.00m
        }

        # Experiment logging
        self.trial_counter = 0
        self.csv_path = "/home/kduy/RoboticProject/project_blueprint/experiments/week04/trials.csv"
        os.makedirs(os.path.dirname(self.csv_path), exist_ok=True)
        self.init_csv()

        # Publishers & Subscribers
        self.gripper_pub = rospy.Publisher("/ur10e/gripper_command", Bool, queue_size=1)
        rospy.Subscriber("/detected_object_pose", Pose, self.pose_callback, queue_size=5)
        rospy.Subscriber("/detected_object_type", String, self.type_callback, queue_size=5)

        # 1. Clean PlanningScene first to ensure no stale collision objects
        time.sleep(0.3)
        for obj in self.scene.get_known_object_names():
            self.scene.remove_world_object(obj)
        for obj in list(self.scene.get_attached_objects().keys()):
            self.scene.remove_attached_object(self.eef_link, obj)
            self.scene.remove_world_object(obj)
        time.sleep(0.4)

        # 2. Move robot to safe STANDBY joint pose
        self.go_to_ready_pose()

        # 3. Load 3D physical obstacles into MoveIt Planning Scene
        self.setup_workcell_obstacles()
        rospy.loginfo("[*] Task State Machine is ready in STANDBY state (Option 1: Front Pick - Flanking Bins)...")

    def setup_workcell_obstacles(self):
        rospy.loginfo("[MoveIt] Updating collision obstacles in planning scene (Table, Conveyor, Bins)...")
        time.sleep(0.2)

        # 1. Table
        table_pose = PoseStamped()
        table_pose.header.frame_id = self.planning_frame
        table_pose.pose.position.x = 0.0
        table_pose.pose.position.y = 0.0
        table_pose.pose.position.z = -0.07
        table_pose.pose.orientation.w = 1.0
        self.scene.add_box("table", table_pose, size=(2.0, 4.0, 0.10))

        # 2. Conveyor Body: at x = -0.60m, height up to z = 0.10m, length 3.6m
        conveyor_pose = PoseStamped()
        conveyor_pose.header.frame_id = self.planning_frame
        conveyor_pose.pose.position.x = -0.60
        conveyor_pose.pose.position.y = 0.0
        conveyor_pose.pose.position.z = 0.05
        conveyor_pose.pose.orientation.w = 1.0
        self.scene.add_box("conveyor_body", conveyor_pose, size=(0.35, 3.6, 0.10))

        # 3. Three sorting bins:
        # Red Bin (Left: y = +0.55m)
        bin_red_pose = PoseStamped()
        bin_red_pose.header.frame_id = self.planning_frame
        bin_red_pose.pose.position.x = -0.10
        bin_red_pose.pose.position.y = 0.55
        bin_red_pose.pose.position.z = 0.04
        bin_red_pose.pose.orientation.w = 1.0
        self.scene.add_box("bin_red", bin_red_pose, size=(0.38, 0.38, 0.10))

        # Yellow Bin (Right: y = -0.55m)
        bin_yellow_pose = PoseStamped()
        bin_yellow_pose.header.frame_id = self.planning_frame
        bin_yellow_pose.pose.position.x = -0.10
        bin_yellow_pose.pose.position.y = -0.55
        bin_yellow_pose.pose.position.z = 0.04
        bin_yellow_pose.pose.orientation.w = 1.0
        self.scene.add_box("bin_yellow", bin_yellow_pose, size=(0.38, 0.38, 0.10))

        # Blue Bin (Rear: x = +0.50m)
        bin_blue_pose = PoseStamped()
        bin_blue_pose.header.frame_id = self.planning_frame
        bin_blue_pose.pose.position.x = 0.50
        bin_blue_pose.pose.position.y = 0.0
        bin_blue_pose.pose.position.z = 0.04
        bin_blue_pose.pose.orientation.w = 1.0
        self.scene.add_box("bin_blue", bin_blue_pose, size=(0.38, 0.38, 0.10))

        # 4. UR10e Industrial Control Box & Pendant (Requirement R8 - Realistic Obstacle Avoidance)
        # Sits on table at rear-left corner (between Red Bin and Blue Bin) at X = +0.35m, Y = +0.48m, Z = 0.19m
        # Size (0.24, 0.32, 0.42), representing operator station and preventing direct rear swings
        control_box_pose = PoseStamped()
        control_box_pose.header.frame_id = self.planning_frame
        control_box_pose.pose.position.x = 0.35
        control_box_pose.pose.position.y = 0.48
        control_box_pose.pose.position.z = 0.19
        control_box_pose.pose.orientation.w = 1.0
        self.scene.add_box("ur_control_box", control_box_pose, size=(0.24, 0.32, 0.42))
        rospy.loginfo("[MoveIt] Added ur_control_box (R8 Realistic Obstacle) at X=+0.35m, Y=+0.48m, Z=0.19m, size=(0.24, 0.32, 0.42)")

        # 5. Acrylic Safety Shield Partition (Requirement R8 - Realistic Obstacle Avoidance)
        # Sits continuously across conveyor front from Red Bin to Yellow Bin at X = -0.38m, Y = 0.0m, Z = 0.15m
        # Size (0.08, 1.64, 0.30) (thickness 8cm, length 164cm, height 30cm)
        # Optimal 30cm height guarantees safe elbow clearance during grasp while enforcing obstacle avoidance during bin transfer
        shield_pose = PoseStamped()
        shield_pose.header.frame_id = self.planning_frame
        shield_pose.pose.position.x = -0.38
        shield_pose.pose.position.y = 0.00
        shield_pose.pose.position.z = 0.15
        shield_pose.pose.orientation.w = 1.0
        self.scene.add_box("acrylic_safety_shield", shield_pose, size=(0.08, 1.64, 0.30))
        rospy.loginfo("[MoveIt] Added acrylic_safety_shield (R8 Realistic Obstacle) at X=-0.38m, Y=0.00m, Z=0.15m, size=(0.08, 1.64, 0.30)")
        time.sleep(0.5)

    def scale_trajectory_speed(self, traj, factor):
        """
        Scales a RobotTrajectory by factor (> 1.0 = faster, < 1.0 = slower).
        Modifies time_from_start, velocities, and accelerations for all trajectory points.
        """
        if factor <= 0 or factor == 1.0 or traj is None:
            return traj
        for point in traj.joint_trajectory.points:
            point.time_from_start = rospy.Duration.from_sec(point.time_from_start.to_sec() / factor)
            if point.velocities:
                point.velocities = [v * factor for v in point.velocities]
            if point.accelerations:
                point.accelerations = [a * (factor * factor) for a in point.accelerations]
        return traj

    def move_to_joints(self, target_joints):
        """Plan and execute joint trajectory with collision avoidance and speed scaling"""
        try:
            t_plan_start = time.time()
            self.group.set_joint_value_target(target_joints)
            res = self.group.plan()
            t_plan_ms = (time.time() - t_plan_start) * 1000.0

            if isinstance(res, tuple):
                success, plan = res[0], res[1]
            else:
                plan = res
                success = len(plan.joint_trajectory.points) > 0

            if success and len(plan.joint_trajectory.points) > 0:
                rospy.loginfo(f"[MoveIt Planner] RRTConnect planned collision-free trajectory with {len(plan.joint_trajectory.points)} points in {t_plan_ms:.1f}ms")
                scaled_plan = self.scale_trajectory_speed(plan, self.speed_multiplier)
                return self.group.execute(scaled_plan, wait=True)
            else:
                rospy.logwarn(f"[MoveIt Planner] Planning failed after {t_plan_ms:.1f}ms (target unreachable or collision detected)!")
        except Exception as e:
            rospy.logwarn(f"[Joint Motion] Fallback to direct go due to: {e}")

        # Safe fallback
        self.group.set_joint_value_target(target_joints)
        return self.group.go(wait=True)

    def go_to_ready_pose(self):
        rospy.loginfo("[MoveIt] Moving robot to STANDBY pose (Elbow-Up, hovering over pick station)...")
        return self.move_to_joints(self.standby_joints)

    def move_cartesian_line(self, target_pose):
        """Standard Cartesian linear motion (strictly vertical, no drift) with speed scaling"""
        try:
            waypoints = [target_pose]
            # Signature in Noetic C++ wrapper: (waypoints, double eef_step, bool avoid_collisions)
            plan, fraction = self.group.compute_cartesian_path(waypoints, 0.01, True)
            if fraction > 0.8:
                scaled_plan = self.scale_trajectory_speed(plan, self.speed_multiplier)
                return self.group.execute(scaled_plan, wait=True)
        except Exception as e:
            rospy.logwarn(f"[Cartesian Path] Fallback to standard Pose Target due to: {e}")

        # Absolute safe fallback
        self.group.set_pose_target(target_pose)
        res = self.group.plan()
        if isinstance(res, tuple):
            plan = res[1]
        else:
            plan = res
        scaled_plan = self.scale_trajectory_speed(plan, self.speed_multiplier)
        return self.group.execute(scaled_plan, wait=True)

    def init_csv(self):
        if not os.path.exists(self.csv_path):
            with open(self.csv_path, mode="w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["trial_id", "timestamp", "object_type", "grasp_success", "place_success", "cycle_time_s", "failure_stage"])

    def record_trial(self, trial_id, obj_type, grasp_ok, place_ok, cycle_time, fail_stage):
        with open(self.csv_path, mode="a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([trial_id, time.strftime("%Y-%m-%d %H:%M:%S"), obj_type, grasp_ok, place_ok, f"{cycle_time:.2f}", fail_stage])
        rospy.loginfo(f"[QA Log] Recorded Trial #{trial_id} to {self.csv_path}")

    def pose_callback(self, msg):
        with self.lock:
            self.latest_pose = msg
            self.pose_time = time.time()

    def type_callback(self, msg):
        with self.lock:
            if self.is_busy:
                return
            if msg.data in ["Unknown", ""]:
                return
            if self.latest_pose is None or (time.time() - self.pose_time) > 2.0:
                return
            # Mark busy immediately to eliminate race conditions
            self.is_busy = True
            target_pose = self.latest_pose
            target_type = msg.data

        # Launch pick-and-place cycle in separate thread to prevent callback blocking
        threading.Thread(target=self.execute_pick_and_place_sequence, args=(target_pose, target_type)).start()

    def execute_pick_and_place_sequence(self, object_pose, object_type):
        with self.lock:
            self.trial_counter += 1
            current_trial = self.trial_counter

        t_start = time.time()
        rospy.loginfo(f"\n=======================================================")
        rospy.loginfo(f"   STARTING PICK-AND-PLACE CYCLE - TRIAL #{current_trial}")
        rospy.loginfo(f"   Object: {object_type} at X={object_pose.position.x:.3f}, Y={object_pose.position.y:.3f}, Z={object_pose.position.z:.3f}")
        rospy.loginfo(f"=======================================================")

        fail_stage = "None"
        grasp_success = False
        place_success = False

        try:
            # -------------------------------------------------------------
            # STEP 1: APPROACH (Pre-grasp pose hovering over object)
            # -------------------------------------------------------------
            fail_stage = "APPROACH"
            rospy.loginfo("[STATE: APPROACH] Rapid descent to Pre-grasp Pose (+15cm)...")
            pregrasp_pose = Pose()
            pregrasp_pose.position.x = object_pose.position.x
            pregrasp_pose.position.y = object_pose.position.y
            pregrasp_pose.position.z = object_pose.position.z + self.pregrasp_offset_z
            pregrasp_pose.orientation = self.down_orientation

            if not self.move_cartesian_line(pregrasp_pose):
                self.group.set_pose_target(pregrasp_pose)
                if not self.group.go(wait=True):
                    raise RuntimeError("Failed to reach Pre-grasp pose!")

            # -------------------------------------------------------------
            # STEP 2: DESCENT (Cartesian linear descent to contact object)
            # -------------------------------------------------------------
            fail_stage = "DESCENT"
            rospy.loginfo("[STATE: DESCENT] Cartesian linear descent to Grasp Pose...")
            grasp_pose = Pose()
            grasp_pose.position.x = object_pose.position.x
            grasp_pose.position.y = object_pose.position.y
            grasp_pose.position.z = object_pose.position.z + self.grasp_offset_z
            grasp_pose.orientation = self.down_orientation

            if not self.move_cartesian_line(grasp_pose):
                raise RuntimeError("Failed to reach Grasp pose!")

            # -------------------------------------------------------------
            # STEP 3: GRASP (Trigger attach logic in Unity & PlanningScene)
            # -------------------------------------------------------------
            fail_stage = "GRASP"
            rospy.loginfo("[STATE: GRASP] Sending grasp command to Unity...")
            self.gripper_pub.publish(Bool(data=True))
            time.sleep(0.2)
            grasp_success = True

            # Attach payload cube in MoveIt PlanningScene so obstacle avoidance includes payload geometry
            try:
                cube_pose = PoseStamped()
                cube_pose.header.frame_id = self.eef_link
                cube_pose.pose.position.z = 0.03
                cube_pose.pose.orientation.w = 1.0
                self.scene.attach_box(self.eef_link, "grasped_cube", cube_pose, size=(0.06, 0.06, 0.06))
            except Exception as e:
                pass

            # -------------------------------------------------------------
            # STEP 4: LIFT (Cartesian linear vertical lift to safe height)
            # -------------------------------------------------------------
            fail_stage = "LIFT"
            rospy.loginfo("[STATE: LIFT] Cartesian linear lift to safe altitude...")
            if not self.move_cartesian_line(pregrasp_pose):
                raise RuntimeError("Error lifting target object!")

            # -------------------------------------------------------------
            # STEP 5: MOVE_TO_BIN (Rotate shoulder to target sorting bin)
            # -------------------------------------------------------------
            fail_stage = "MOVE_TO_BIN"
            target_joints = self.bin_joints.get(object_type, self.bin_joints["Yellow"])
            rospy.loginfo(f"[STATE: MOVE_TO_BIN] Sweeping arm to {object_type} Bin via optimal joint trajectory...")

            if not self.move_to_joints(target_joints):
                raise RuntimeError("Failed to move to destination sorting bin!")

            # -------------------------------------------------------------
            # STEP 6: RELEASE (Open gripper to drop object into bin)
            # -------------------------------------------------------------
            fail_stage = "RELEASE"
            rospy.loginfo("[STATE: RELEASE] Releasing object into bin...")
            self.gripper_pub.publish(Bool(data=False))
            time.sleep(0.2)
            place_success = True

            # Detach and remove payload cube from MoveIt PlanningScene
            try:
                self.scene.remove_attached_object(self.eef_link, "grasped_cube")
                self.scene.remove_world_object("grasped_cube")
            except Exception as e:
                pass

            # -------------------------------------------------------------
            # STEP 7: READY (Return to standby pose over conveyor)
            # -------------------------------------------------------------
            fail_stage = "READY"
            rospy.loginfo("[STATE: READY] Returning to standby position...")
            self.go_to_ready_pose()

            fail_stage = None
            cycle_time = time.time() - t_start
            rospy.loginfo(f"[+] CYCLE COMPLETED SUCCESSFULLY! Cycle time: {cycle_time:.2f} s")

        except Exception as e:
            cycle_time = time.time() - t_start
            rospy.logerr(f"[-] CYCLE INTERRUPTED at step [{fail_stage}]: {e}")
            # Ensure gripper release on failure
            self.gripper_pub.publish(Bool(data=False))

        finally:
            self.group.clear_pose_targets()
            self.record_trial(current_trial, object_type, grasp_success, place_success, cycle_time, fail_stage)
            with self.lock:
                self.is_busy = False
                self.latest_pose = None
                self.latest_type = None
            rospy.loginfo("[*] System returned to IDLE state, waiting for next object.\n")


def main():
    try:
        sm = TaskStateMachine()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
    finally:
        moveit_commander.roscpp_shutdown()


if __name__ == "__main__":
    main()
