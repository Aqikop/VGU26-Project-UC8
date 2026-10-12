# UC8: ROBOTIC ARM CONVEYOR PICK-AND-PLACE WITH OBSTACLE AVOIDANCE
## Milestone 1 Defense & Presentation — Closed-Loop Sorting Workcell & Future Roadmap

- **Course:** Robotic Project — Vietnamese-German University (VGU)
- **Project Topic:** Use Case 08 (UC8) — Robotic Sorting Workcell
- **Simulated Hardware:** UR10e (6-DOF Industrial Manipulator) + 3.6m Conveyor Belt + 3 Dedicated Sorting Bins + Procedural 2-Finger Claw
- **Engineering Stack:** Unity 2022.3 LTS (PhysX 4.x / ArticulationBody) + ROS Noetic (MoveIt Motion Planning) + ROS-TCP-Endpoint
- **Milestone Status:** Milestone 1 Formal Defense (Fulfilling R1, R2, R3, R4)
- **Next Phase:** Week 06 Sprint & Milestone 2 (R5, R6, R7, R8 — Static Obstacle Avoidance & Perception)

---

## PRESENTATION AGENDA

| Slide | Topic | Key Focus |
| :---: | :--- | :--- |
| **01** | **Title Cover** | UC8 Milestone 1 Defense & Performance Evaluation |
| **02** | **Presentation Agenda** | Complete overview of 15 structured presentation slides |
| **03** | **Week 03 Baseline & Commitments** | Baseline achievements and commitments set out from Week 03 for Milestone 1 |
| **04** | **Milestone 1 Scope & Fulfillment** | 100% fulfillment of commitments (R1, R2, R3, R4) with verified closed loop |
| **05** | **System Architecture & Pipeline** | Bidirectional real-time closed loop between Unity 2022.3 and ROS Noetic |
| **06** | **Instructor Feedback & Resolutions** | Industrial 2-finger claw, anti-miss sensor, orthogonal alignment & zero-sink parenting |
| **07** | **Workcell Layout Re-engineering** | Spatial optimization of Option 1 (Symmetric Front Pick - Flanking Bins) |
| **08** | **Non-singular Kinematics** | Strict 90° downward wrist lock and pure base SCARA sweep (65% cycle time cut) |
| **09** | **Realistic PhysX & Multi-Item Flow** | Friction-based zero-teleport deceleration and continuous 2-3 item conveyor flow |
| **10** | **7-Step Task State Machine** | Autonomous execution sequencer from Standby to Release without human intervention |
| **11** | **Empirical Benchmark Trials (QA)** | Statistical analysis of 70 trials: 100% grasp/place success rate, 11.23s cycle time |
| **12** | **Technical Defenses (Faculty Q&A)** | Formal engineering answers to key faculty committee questions |
| **13** | **Week 06 Objectives & Sprint Backlog** | R5 continuous conveyor operation (5+ min zero-jam), seeded spawner, fault recovery |
| **14** | **Milestone 2 Strategic Roadmap** | R5-R8 roadmap: Computer Vision, 3D Pose Localization, and Static Obstacle Avoidance |
| **15** | **Summary & M1 Acceptance Conclusion** | Milestone 1 compliance sign-off and transition to Milestone 2 development |

---

## SLIDE 01: TITLE COVER
- **Project Title:** UC8: Robotic Arm Conveyor Pick-and-Place with Obstacle Avoidance
- **Subtitle:** Milestone 1 Defense & Verification — Autonomous Closed-Loop Sorting Workcell
- **Academic Context:** Vietnamese-German University (VGU) — Robotic Project Course
- **Platform:** UR10e Manipulator, Unity 2022.3 LTS PhysX Engine, ROS Noetic MoveIt Planning Framework
- **Milestone Scope:** Verification of Requirements R1 (Scope/Architecture), R2 (UR10e MoveIt), R3 (ROS-Unity Bridge), R4 (Closed-Loop Pick-and-Place)

---

## SLIDE 02: PRESENTATION AGENDA
- Comprehensive walkthrough covering:
  1. Technical foundation and commitment fulfillment from earlier sprints.
  2. Complete bidirectional closed-loop architecture.
  3. **Instructor Feedback Analysis & Rapid Engineering Resolutions** (Claw mechanism, sensor reliability, orthogonal grasp).
  4. Workcell spatial layout re-engineering and non-singular kinematic trajectory optimization.
  5. Empirical quality assurance with 70 logged benchmark trials (100% success rate).
  6. **Week 06 Technical Objectives & Milestone 2 Strategic Roadmap (Static Obstacle Avoidance & Perception).**

---

## SLIDE 03: BASELINE ACHIEVED IN WEEK 03 & COMMITMENTS SET OUT
### 1. What was Achieved in Week 03 (Baseline Foundation):
- **ROS-Unity Network Bridge:** Seamless socket streaming on port 10000 via `ROS-TCP-Endpoint`.
- **Coordinate Conversion:** Standardized transformation mapping from Unity Left-Handed to ROS FLU Right-Handed:
  $$\begin{cases} X_{\text{ROS}} = Z_{\text{Unity}} \\ Y_{\text{ROS}} = -X_{\text{Unity}} \\ Z_{\text{ROS}} = Y_{\text{Unity}} \end{cases}$$
- **Object Perception:** Streaming cube 3D pose to `/detected_object_pose` and color classification to `/detected_object_type` at 10 Hz.
- **MoveIt Inverse Kinematics:** Solved theoretical IK trajectories hovering +15cm above object on RViz.

### 2. Commitments Set Out for Milestone 1:
- **Commitment 1 (Trajectory Execution):** Break through 'plan-only' barrier; stream real-time `/joint_states` at 50 Hz to drive physical UR10e in Unity.
- **Commitment 2 (Grasping Mechanism):** Implement an operational grasping/release mechanism for cube interaction.
- **Commitment 3 (Task State Machine):** Construct autonomous closed-loop sequencer connecting perception, motion, and release.
- **Commitment 4 (Multi-Bin Sorting):** Route red, yellow, and blue cubes to dedicated destination bins without collision.

---

## SLIDE 04: MILESTONE 1 TECHNICAL SCOPE & 100% COMMITMENT FULFILLMENT
### 1. 100% Commitment Fulfillment Status:
1. **Trajectory Execution (R2/R3):** Streamed `/joint_states` at 50 Hz to 6 ArticulationBodies with zero sagging and smooth tracking. (**100% DONE**)
2. **Grasping Mechanism (R4):** Implemented industrial Attach/Parenting logic in `GripperController.cs` with instant latching upon command. (**100% DONE**)
3. **Closed-Loop State Machine (R4):** Constructed 7-step autonomous sequencer (`task_state_machine.py`) with zero human intervention. (**100% DONE**)
4. **3-Bin Sorting System (R4):** Deployed Red (Left), Yellow (Right), and Blue (Rear) bins with dedicated non-singular trajectories. (**100% DONE**)

### 2. Milestone 1 Performance Metric Compliance:
- **Target:** $\ge 8 / 10$ successful pick-and-place trials, cycle time $< 30\text{s}$.
- **Achieved:** **70 / 70 trials (100% success rate)**, mean cycle time **11.23s** (2.7x faster than required threshold).

---

## SLIDE 05: SYSTEM ARCHITECTURE & BIDIRECTIONAL PIPELINE
- **Data Flow 1 (Perception):** Unity `PickZoneSensor.cs` $\to$ `ObjectLocalizationReporter.cs` $\to$ `/detected_object_pose` & `/detected_object_type` via TCP 10000 to ROS.
- **Data Flow 2 (Planning & Control):** `task_state_machine.py` coordinates state transitions $\to$ MoveIt `compute_cartesian_path()` and `move_group.go()` $\to$ `/joint_states` streamed at 50 Hz to Unity `UR10eController.cs`.
- **Data Flow 3 (Gripper Actuation):** ROS publishes `/ur10e/gripper_command` (Bool) $\to$ `GripperController.cs` executes attach/release logic and updates `/ur10e/gripper_status`.

---

## SLIDE 06: INSTRUCTOR FEEDBACK & RAPID TECHNICAL RESOLUTIONS
### 1. Feedback A — Visible Mechanical Gripper Claw:
- **Proposed/Requested:** Instructor requested a visible mechanical gripper claw on the robot rather than an abstract suction/contact point.
- **Technical Solution:** Designed and implemented procedural industrial 2-finger claw (`VisualClaw`): Flange mount adapter ($1.2\text{cm}$), navy housing chassis ($2.0\text{cm}$), dual-color status LED (Cyan standby, Emerald Green clamped), and aluminum fingers ($4.0\text{cm}$) with black rubber friction pads.

### 2. Feedback B — Missed Cubes in Continuous Multi-Item Flow:
- **Identified Issue:** Cubes occasionally slipped past the pick station when running continuous flows for an extended duration due to missed `OnTriggerEnter` trigger events.
- **Technical Solution:** Completely replaced fragile trigger collisions with continuous active scanning (`FindLeadingCubeOnConveyor()`) + safety stop latch in `PickZoneSensor.cs`. Conveyor stops predictably whenever a leading cube enters the pick zone ($X \ge -0.015\text{m}$).

### 3. Feedback C — Gripper Sinking & Off-Axis Twist Resolution:
- **Identified Issue:** Claw penetrated conveyor belt during Cartesian descent, and upon clamping, the cube shifted and twisted off-axis ($13.6^\circ$).
- **Technical Solution:**
  1. Standardized `down_orientation = Quaternion(0.7071068, 0.7071068, 0, 0)` ($100\%$ strictly orthogonal to conveyor and cube faces).
  2. Tuned `grasp_offset_z = 0.065m` with compact $4.0\text{cm}$ fingers, ensuring fingertips float $+2.3\text{cm}$ above conveyor belt surface (zero sinking).
  3. Pure parenting with `worldPositionStays = true` (`SetParent(attachPoint, true)`), preserving $100\%$ of natural world position and rotation without any jerk, shift, or twist.

---

## SLIDE 07: WORKCELL LAYOUT RE-ENGINEERING (OPTION 1)
- **Conveyor Belt:** 3.6m long, centered directly in front of the robot ($X = -0.60\text{m}$). Maximizes dexterous workspace and provides ample gliding run.
- **Pick Zone Station:** Symmetric front center ($X = -0.60\text{m}, Y = 0.00\text{m}$). Bilateral symmetry minimizes inertial moments and travel time.
- **Flanking Bins:** Red Bin on Left ($Y = +0.55\text{m}$), Yellow Bin on Right ($Y = -0.55\text{m}$), Blue Bin on Rear ($X = +0.50\text{m}$). Clear transfer paths eliminate conveyor collision hazards.
- **Bin Dimensions:** Scaled +35% to $0.38\text{m} \times 0.38\text{m} \times 0.10\text{m}$ for 100% free-fall capture rate.
- **Heavy Industrial Table:** Expanded to $4.0\text{m} \times 2.0\text{m}$ heavy-duty foundation supporting conveyor, bins, and UR10e base.

---

## SLIDE 08: NON-SINGULAR KINEMATICS OPTIMIZATION
- **Strict 90° Downward Wrist Lock ($q_4 = 90.0^\circ$):** End-effector `tool0` maintains invariant downward vector $[0, 0, -1]$ throughout all states. Prevents wrist singularities, inverted arm postures, and erratic 180° elbow flips.
- **Pure Base Shoulder Pan Rotation (SCARA-Style):** Shoulder lift and elbow angles remain virtually constant ($\Delta < 10^\circ$) during transfers. Robot sorts items by rotating **only `shoulder_pan_joint`**, reducing path length by 65% and cutting cycle time down to 11.23s.

---

## SLIDE 09: REALISTIC PHYSX SIMULATION & MULTI-ITEM FLOW
- **Pure PhysX Friction Deceleration (Zero-Teleportation):** Cubes glide from $X = -1.5\text{m}$ at $0.3\text{m/s}$. When reaching $X \ge -0.015\text{m}$, `PickZoneSensor.cs` cuts conveyor power (`StopConveyor()`). Natural surface friction ($0.8$) halts cube smoothly at exactly $X \approx 0.000\text{m}$ ($\pm 3\text{mm}$ deviation).
- **Continuous Multi-Item Flow:** Spawner maintains 2-3 active cubes on belt simultaneously with a minimum spacing of $38\text{cm}$ (`IsSpawnAreaClear()`), eliminating pile-ups.
- **Visual Rig Consistency:** Belt texture scrolling is synchronized 1:1 with physical object velocity ($0.3\text{m/s}$). Industrial aluminum rails, dual chrome rollers, gearmotor housing, and dual-color optical sensor LED.

---

## SLIDE 10: 7-STEP CLOSED-LOOP TASK STATE MACHINE
- **1. STANDBY:** Arm hovers at safe elevation over pick zone ($Z = 0.42\text{m}$) with wrist locked 90° downward.
- **2. APPROACH:** Rapid Cartesian descent to Pre-grasp Pose ($+16\text{cm}$ above object center) in $< 0.5\text{s}$.
- **3. DESCENT:** Cartesian vertical descent to Grasp Pose ($+6.5\text{cm}$ above center, fingertips floating $2.3\text{cm}$ above belt).
- **4. GRASP:** Sends grasp command; Unity attaches cube to `tool0` via `SetParent(attachPoint, true)` without shifting; MoveIt attaches collision box in PlanningScene.
- **5. LIFT:** Vertical Cartesian lift back to safe altitude ($+16\text{cm}$), clearing conveyor rails.
- **6. MOVE_TO_BIN:** Pure shoulder pan sweep to target sorting bin (`Red` / `Yellow` / `Blue`).
- **7. RELEASE:** Opens gripper, detaches cube, restores gravity for soft landing; triggers conveyor resume and spawner for next item.

---

## SLIDE 11: EMPIRICAL BENCHMARK TRIALS & QA ANALYSIS
- Logged automatically to `experiments/week04/trials.csv`:
  - **Consecutive Logged Trials:** 70 consecutive cycles (target: $\ge 10$) $\to$ **Exceeds target by 700%**.
  - **Grasp Success Rate:** 100.0% (70 / 70 trials) $\to$ **Zero grasp drops**.
  - **Sorting Placement Success Rate:** 100.0% (70 / 70 trials) $\to$ **Zero placement misses**.
  - **Mean Cycle Time:** 11.23 s / cycle (target: $< 30\text{s}$) $\to$ **2.7x faster than requirement**.
  - **Coasting Stop Position:** $X = 0.00\text{m} \pm 3\text{mm}$ repeatability.

---

## SLIDE 12: TECHNICAL DEFENSES (FACULTY Q&A PREPARATION)
- **Q1: Why are Pre-grasp and Lift poses mandatory?**
  - *Defense:* Industrial workcells strictly separate free-space transit from fine Cartesian approach. Moving diagonally from afar risks collisions with conveyor guide rails or bin sidewalls.
- **Q2: Why avoid fixed sleep delays in favor of closed-loop feedback?**
  - *Defense:* Motion duration varies with angular distance ($1.07\text{rad}$ to Red vs $2.78\text{rad}$ to Blue). Fixed delays cause premature grasp failures or wasted cycle time. Closed-loop feedback uses MoveIt's trajectory completion flag (`wait=True`).
- **Q3: How were ragdoll oscillations and joint sagging prevented in ArticulationBody?**
  - *Defense:* Immovable base link, gravity compensation handled by MoveIt dynamics (`useGravity = false`), and high drive stiffness (`stiffness = 50000`, `damping = 1000`, `forceLimit = 10000`).

---

## SLIDE 13: WEEK 06 TECHNICAL OBJECTIVES & SPRINT BACKLOG
### 1. Fulfilling Requirement R5 (Conveyor & Spawner Robustness):
- **5-Minute Continuous Non-Stop Operation:** Validate that conveyor, spawner, and pick-zone sensor run uninterrupted for 5+ minutes with zero jams or memory leaks.
- **Seed-Based Deterministic Spawning:** Implement configurable PRNG seed parameters for random spawner to allow 100% reproducible test batches.
- **Dynamic Speed Modulation:** Implement variable conveyor speed control ($0.1\text{m/s} - 0.5\text{m/s}$) via ROS parameter service.

### 2. Autonomous Fault Recovery:
- **Stall & Jam Auto-Clear:** Automated recovery routine if an unexpected obstacle obstructs belt flow.
- **Perception Timeout Handler:** Fail-safe state machine rollback if object detection frame drops.

---

## SLIDE 14: MILESTONE 2 (WEEK 10) STRATEGIC ROADMAP & COMMITMENTS
### 1. Milestone 2 Scope & Core Requirements (R5, R6, R7, R8):
- **R5 (Continuous Conveyor Feed):** Industrial belt running continuously with random multi-item queue.
- **R6 (Computer Vision Color Classifier):** Camera-based perception pipeline replacing metadata detection. Segmenting Red, Blue, and Yellow cubes via OpenCV HSV color thresholding / deep classifier.
- **R7 (3D Coordinate Mapping):** Camera-to-robot coordinate calibration converting pixel centroids to $(X, Y, Z)$ in `base_link` with localization error $\le 20\text{mm}$.
- **R8 (Static Obstacle Avoidance):** Introducing a physical Static Wall barrier in the workspace. Updating MoveIt PlanningScene; arm dynamically calculates collision-free trajectories around the wall in **Stop-and-Pick** mode.

### 2. Forward Alignment to Milestone 3 (W14) & Final Acceptance (W15):
- **Milestone 3 (W14):** Dynamic moving obstacles, Risk Monitor, Safe-Stop $\to$ Replan $\to$ Resume.
- **Final Acceptance (W15):** Continuous Moving-Belt Picking (R9) and complete production handover (R12).

---

## SLIDE 15: SUMMARY & MILESTONE 1 ACCEPTANCE CONCLUSION
- **Milestone 1 Objectives 100% Met:**
  - Full closed-loop integration: Unity $\leftrightarrow$ ROS-TCP $\leftrightarrow$ MoveIt $\leftrightarrow$ State Machine.
  - Industrial 2-finger claw successfully implemented and verified.
  - 100% empirical success rate across 70 logged trials with 11.23s mean cycle time.
  - All instructor feedback resolved cleanly with documented engineering rationales.
- **Milestone 1 Acceptance Request:** Formal sign-off and approval to proceed with Week 06 / Milestone 2 sprint.
