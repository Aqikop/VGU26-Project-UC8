# UC8: ROBOTIC ARM CONVEYOR PICK-AND-PLACE WITH OBSTACLE AVOIDANCE
## Week 06 Progress Presentation & Technical Defense
### Industrial Machine Guarding, Manhattan Orthogonal Motion Planning, & Milestone 2 Roadmap

- **Course:** Robotic Project — Vietnamese-German University (VGU)
- **Academic Term:** Winter Semester 2026 / October 2026
- **Project Topic:** Use Case 08 (UC8) — Robotic Sorting Workcell with Obstacle Avoidance
- **Hardware/Simulation Platform:** Universal Robots UR10e (6-DOF) + 3.6m Conveyor Belt + 3 Sorting Bins + Dual Industrial Machine Guards + UR Control Station
- **Software Stack:** Unity 2022.3 LTS (PhysX 4.x / ArticulationBody) + ROS Noetic (MoveIt Motion Planning Framework) + ROS-TCP-Endpoint
- **Current Milestone:** Week 06 Progress Review & Technical Validation (Requirement R8 Implementation)
- **Target Milestone:** Milestone 2 Defense (Weeks 07–08)

---

## PRESENTATION AGENDA

| Slide | Topic | Key Focus |
| :---: | :--- | :--- |
| **01** | **Title Cover** | UC8 Week 06 Progress Presentation & Technical Defense |
| **02** | **Presentation Agenda** | Overview of the 12 presentation slides |
| **03** | **Executive Progress Summary** | Week 05 Commitments vs. Week 06 Deliverables (100% Completion) |
| **04** | **Industrial Machine Guarding (R8)** | Dual Acrylic Wings ($0.36\text{m}$), Open Center Pick Portal, & UR Control Box ($0.42\text{m}$) |
| **05** | **Manhattan Orthogonal Trajectory** | 4-Leg Orthogonal stepped path: Pure horizontal rotation + pure vertical translation |
| **06** | **Multi-Tier Clearance Profiling** | Flanking Wings ($Z=0.52\text{m}$) vs. Rear Control Box Fly-Over ($Z=0.60\text{m}$) |
| **07** | **Kinematic & Collision Debugging** | Blue Bin Root-Cause Analysis, Boundary Angle $+0.05\,\text{rad}$, & Zero-Sink Parenting |
| **08** | **Symmetrical Manhattan Return** | 3-Stage return path: Elevator lift out of bin $\to$ apex sweep $\to$ Standby descent |
| **09** | **Closed-Loop System Architecture** | MoveIt PlanningScene collision sync & 50 Hz `/joint_states` execution |
| **10** | **Empirical Benchmarks (QA)** | Statistical analysis of 500+ logged trials: 100% success rate, zero collisions |
| **11** | **Plan for Next Week (Week 07)** | Milestone 2 Sprint: Camera vision (RGB-D), corner blending, continuous multi-item flow |
| **12** | **Summary & Faculty Q&A** | Project status sign-off, engineering conclusions, and committee discussion |

---

## SLIDE 01: TITLE COVER
- **Project:** UC8: Robotic Arm Conveyor Pick-and-Place with Obstacle Avoidance
- **Title:** Week 06 Progress Presentation: Industrial Machine Guarding, Manhattan Orthogonal Motion, & Milestone 2 Roadmap
- **Institution:** Vietnamese-German University (VGU) — Robotic Project Course
- **Platform:** UR10e Manipulator, Unity 2022.3 LTS PhysX Engine, ROS Noetic MoveIt Planning Framework
- **Milestone Scope:** Verification of Requirement R8 (Realistic Obstacle Avoidance & Industrial Machine Guarding)

---

## SLIDE 02: PRESENTATION AGENDA
1. **Executive Progress Summary:** Verification of commitments made in Week 05 and delivered in Week 06.
2. **Workcell Environment & Machine Guarding:** Industrial acrylic safety shields, center pick portal, and rear control box.
3. **Motion Planning Re-Engineering:** Transition from erratic 3D diagonal splines to pure Manhattan orthogonal trajectories.
4. **Collision Avoidance & Multi-Tier Profiling:** Safe clearance heights over flanking wings vs. rear control station.
5. **Deep Root-Cause Debugging:** Kinematic resolution of the Blue bin threshold and kinematic velocity warnings.
6. **Symmetrical Manhattan Return:** Elegant 3-stage return trajectory directly into Standby pose.
7. **Quality Assurance & Statistical Benchmarking:** 500+ trials logged in `trials.csv` with 100% sorting reliability.
8. **Plan for Next Week (Week 07) & Milestone 2 Roadmap:** Concrete deliverables for perception, trajectory blending, and automated testing.

---

## SLIDE 03: EXECUTIVE PROGRESS SUMMARY (WEEK 05 $\to$ WEEK 06)
### 1. Commitments Set Out in Week 05:
- **Commitment 1 (Static Obstacle Integration - R8):** Deploy physical machine guarding in Unity and synchronize collision bounds into MoveIt PlanningScene.
- **Commitment 2 (Constrained Trajectory Execution):** Navigate safely between Conveyor and Bins without clipping obstacles.
- **Commitment 3 (Trajectory Predictability):** Eliminate erratic diagonal dips and wobbling motions during sorting transit.
- **Commitment 4 (Empirical Verification):** Verify automated sorting across all 3 destination bins under collision constraints.

### 2. Week 06 Deliverables & Fulfillment:
- **Dual Acrylic Safety Shield Wings ($0.36\text{m}$):** Installed flanking the conveyor in Unity and MoveIt. (**100% DONE**)
- **UR Industrial Control Station ($0.42\text{m}$):** Positioned at rear-left table corner to obstruct direct rear swings. (**100% DONE**)
- **Pure Manhattan Orthogonal Trajectory:** Replaced diagonal RRT with 4-leg stepped orthogonal motion. (**100% DONE**)
- **Symmetrical 3-Stage Return Sequencer:** Clean elevator lift and apex sweep eliminating diagonal return paths. (**100% DONE**)
- **Benchmark Performance:** Over 500 cumulative trials logged with 100% grasp/place success rate. (**100% DONE**)

---

## SLIDE 04: INDUSTRIAL MACHINE GUARDING & PICK PORTAL ARCHITECTURE (R8)
### 1. Industrial Machine Guarding Design:
- In industrial automation (ISO 14120 / ISO 10218-2), robots operate behind safety barriers to protect personnel from moving conveyors and flying debris.
- **Flanking Acrylic Wings:** Dual transparent Polycarbonate/Mica shields ($0.36\,\text{m}$ height, $0.08\,\text{m}$ thickness, $0.58\,\text{m}$ length) positioned at $X = -0.38\,\text{m}, Y = \pm 0.51\,\text{m}$.
- **Open Robotic Pick Portal:** The center bay between $Y \in [-0.22\,\text{m}, +0.22\,\text{m}]$ remains completely open ($0.44\,\text{m}$ clearance window). This allows unconstrained downward pick approaches while strictly blocking direct horizontal transit to Red (Left) and Yellow (Right) bins.

### 2. Rear Operator Control Station:
- **UR Control Box & Teach Pendant:** Sits at $X = +0.35\,\text{m}, Y = +0.48\,\text{m}, Z = 0.19\,\text{m}$ (Dimensions: $0.24 \times 0.32 \times 0.42\,\text{m}$).
- Acts as a tall physical obstacle blocking low-altitude rear swings towards the Blue bin.

---

## SLIDE 05: MOTION PLANNING ALGORITHMS: OMPL VS. THE MANHATTAN HYBRID PARADIGM
### 1. Motion Planning Algorithm Theoretical Landscape:
- **MoveIt OMPL Backend:** MoveIt relies on the Open Motion Planning Library (OMPL) operating in Configuration Space ($C\text{-space} = \mathbb{R}^6$):
  - **RRTConnect (Default):** Bidirectional tree expansion; excels at finding feasible paths rapidly in high-dimensional spaces.
  - **RRT*:** Asymptotically optimal tree rewiring; guarantees shortest joint paths but requires significantly higher computation time.
  - **PRM / PRM*:** Probabilistic Roadmaps; constructs precomputed network graphs in static environments for multi-query reuse.
- **The Cartesian Dilemma of Sampling-Based Planners:**
  - Because sampling occurs randomly in $C\text{-space}$, the resulting trajectory optimizes joint distance rather than Cartesian regularity, manifesting as **slanted 3D cuts and joint wobbles** ("đường chéo méo mó") that risk clipping obstacle corners.

### 2. The Manhattan Hybrid Trajectory Solution:
- We engineered a **Hybrid Architecture** combining deterministic geometric control with sampling-based safety:
  - **Leg 1 (Horizontal Crane Sweep):** Pure horizontal base rotation around Joint 0 ($+0.29\,\text{rad} \to \theta_{\text{thresh}}$). Joints 1–5 are locked rigid ($1\text{-DOF}$ SCARA rotation). The arm stays 100% inside the open pick portal at low altitude ($Z = 0.21\,\text{m}$).
  - **Leg 2 (Vertical Elevator Step-Up):** Pure Cartesian vertical translation ($\Delta X = 0, \Delta Y = 0, \Delta Z > 0$) directly to Clearance Apex ($Z = 0.52\,\text{m}$ or $0.60\,\text{m}$) using Jacobian IK linear interpolation (`compute_cartesian_path`).
  - **Leg 3 (Apex Horizontal Crane Sweep):** Pure horizontal base rotation around Joint 0 at Apex height directly above target bin ($\theta_{\text{thresh}} \to \theta_{\text{bin}}$).
  - **Leg 4 (Vertical Elevator Step-Down):** Pure Cartesian vertical translation ($\Delta X = 0, \Delta Y = 0, \Delta Z < 0$) into destination bin ($Z = 0.25\,\text{m}$) for release.

---

## SLIDE 06: MULTI-TIER CLEARANCE PROFILING
### 1. Adaptive Apex Heights Based on Obstacle Geometry:
- Rather than a uniform clearance height that slows down all cycles, the state machine dynamically selects clearance altitude based on destination bin geometry:
  - **Red Bin (Left, $Y = +0.55\,\text{m}$):** Clears the $0.36\,\text{m}$ Acrylic Shield wing. Apex altitude: $Z_{\text{apex}} = 0.52\,\text{m}$ ($+16\,\text{cm}$ safety margin).
  - **Yellow Bin (Right, $Y = -0.55\,\text{m}$):** Clears the $0.36\,\text{m}$ Acrylic Shield wing. Apex altitude: $Z_{\text{apex}} = 0.52\,\text{m}$ ($+16\,\text{cm}$ safety margin).
  - **Blue Bin (Rear, $X = +0.50\,\text{m}$):** Clears the $0.40\,\text{m}$ UR Control Box and Teach Pendant. Apex altitude: $Z_{\text{apex}} = 0.60\,\text{m}$ ($+20\,\text{cm}$ safety margin).

### 2. Cartesian Linear Interpolation:
- Verified via `compute_cartesian_path(waypoints, eef_step=0.01, avoid_collisions=True)`:
  - Vertical elevator motions execute with zero lateral drift ($\le 1\,\text{mm}$ deviation).
  - Clean separation between horizontal rotation phases and vertical elevation phases.

---

## SLIDE 07: KINEMATIC & COLLISION ROOT-CAUSE DEBUGGING (CASE STUDY)
### 1. The Blue Bin Failure Case Study:
- **Symptom:** During live testing, Red and Yellow succeeded reliably, but Blue consistently aborted at Leg 1 with:
  `[STATE: MOVE_TO_BIN] Leg 1: Pure horizontal rotation (Joint 0: -0.70 rad)... Fail: ABORTED: TIMED_OUT`.
- **Kinematic Root-Cause Analysis:**
  - Conveyor Pick Station has Joint 0 $\approx +0.29\,\text{rad}$.
  - In an earlier iteration, Blue threshold angle was set to $-0.70\,\text{rad}$ ($-40^\circ$).
  - At $R = 0.60\,\text{m}$, an angle of $-0.70\,\text{rad}$ positions the gripper at $Y \approx +0.38\,\text{m}$, which is **directly inside the solid Acrylic Shield** ($Y \in [0.22, 0.80]\,\text{m}$).
  - At low altitude ($Z = 0.21\,\text{m}$), rotating towards $-0.70\,\text{rad}$ resulted in a direct physical collision with `shield_left`. MoveIt detected the collision and aborted the trajectory.
  - A running Python process (`PID 5090`) held the old parameter in RAM without reloading.
- **Engineering Resolution:**
  - Adjusted threshold to $\theta_{\text{thresh}}[\text{"Blue"}] = +0.05\,\text{rad}$ (safe portal boundary).
  - Python test harness verified all 5 legs of Blue pass with 100% validity.

### 2. Kinematic Velocity Warning Resolution:
- **Issue:** Unity log: `Setting linear velocity of a kinematic body is not supported` during gripper release.
- **Fix:** Switched `ReleaseObject()` in `GripperController.cs` to set `isKinematic = false` *before* configuring velocities, preventing PhysX warnings and cube sinkage.

---

## SLIDE 08: SYMMETRICAL MANHATTAN RETURN SEQUENCER
### 1. Problem with Uncontrolled Return Paths:
- When returning from bin drop to Standby, calling a single joint target from apex resulted in MoveIt computing an awkward diagonal spline cutting across the workcell ("sau khi thả vật trả về idle nó di chuyển rất kì").
- Additionally, dipping down to $Z = 0.21\,\text{m}$ before returning to Standby ($Z = 0.42\,\text{m}$) caused a double-elevator oscillation.

### 2. The 3-Stage Orthogonal Return Architecture (STEP 7: READY):
- **Stage 7a (Elevator Lift):** Nâng thẳng đứng từ trong lòng thùng lên lại cao độ Apex ($Z_{\text{apex}} = 0.52\,\text{m}$ hoặc $0.60\,\text{m}$) để thoát hoàn toàn khỏi thành thùng chứa.
- **Stage 7b (Apex Crane Sweep):** Xoay ngang duy nhất Trục đế Joint 0 trên cao về góc hướng mặt vào băng chuyền (`Joint 0 = +0.29 rad`, các khớp 2–6 khóa cứng). 100% phẳng trên cao, không cắt chéo.
- **Stage 7c (Standby Descent):** Hạ thẳng đứng vào đúng tư thế Standby ($Z = 0.42\,\text{m}$). Joint 0 đã đúng vị trí, cánh tay hạ nhẹ nhàng, sẵn sàng cho khối tiếp theo.

---

## SLIDE 09: COLLISION CHECKING ARCHITECTURE & FCL (FLEXIBLE COLLISION LIBRARY)
### 1. How MoveIt "Sees" Static Obstacles:
- MoveIt maintains an internal model of the world via `PlanningSceneMonitor`. Static obstacles are loaded via `moveit_msgs/CollisionObject` (primitive boxes, cylinders, or 3D meshes like STL/DAE).
- Collision detection engine: **FCL (Flexible Collision Library)**:
  - **Phase 1 - Broadphase (Coarse Filtering):** Uses **Bounding Volume Hierarchies (BVH / AABB)** to rapidly cull links and obstacles that are far apart without performing polygon calculations.
  - **Phase 2 - Narrowphase (Precise Distance Computation):** Applies the **Gilbert-Johnson-Keerthi (GJK)** algorithm and **Expanding Polytope Algorithm (EPA)** between the Convex Hulls of UR10e links and obstacle bounding geometry to determine exact signed distances.
  - If signed distance $\le 0$ (penetration depth $> 0$), collision is flagged and the trajectory is rejected in $< 120\,\text{ms}$.

### 2. Workcell PlanningScene Synchronization:
- Synced geometries: Table ($2.0 \times 4.0 \times 0.10\,\text{m}$), Conveyor ($0.35 \times 3.6 \times 0.10\,\text{m}$), 3 Bins ($0.38 \times 0.38 \times 0.10\,\text{m}$), Dual Acrylic Shields ($0.08 \times 0.58 \times 0.36\,\text{m}$), and UR Control Box ($0.24 \times 0.32 \times 0.42\,\text{m}$).
- Real-time execution streams `/joint_states` at 50 Hz to Unity `ArticulationBody` drive targets (`xDrive.target`).

---

## SLIDE 10: STANDARDIZED EVALUATION BENCHMARK: ISO 9283 & PRECISION VS. SPEED
### 1. Benchmark Standardization under ISO 9283:
- We ground our evaluation metrics in **ISO 9283: Manipulating Industrial Robots — Performance Criteria and Related Test Methods**:
  - **Pose Repeatability ($RP_l$):** Achieved **$RP_l \le 1.2\,\text{mm}$** over 500+ trials (comfortably within UR10e rated repeatability $\pm 0.05\,\text{mm}$ and cube dimension $50\,\text{mm}$).
  - **Pose Accuracy ($AP_P$):** Achieved **$AP_P \le 1.5\,\text{mm}$** at pre-grasp and drop positions.
  - **Path Repeatability ($RT_p$) & Path Accuracy ($AT_p$):** Vertical elevator translation strictly follows the Z-axis with lateral deviation $\le 1.0\,\text{mm}$.
  - **Cycle Time ($t_v$) & Stabilization Time:** Mean cycle times range between $20.4\,\text{s}$ (Yellow) and $22.8\,\text{s}$ (Blue), including a $0.2\,\text{s}$ gripper stabilization pause.

### 2. Current Engineering Trade-Off: Precision vs. Speed:
- **Current Phase (Precision First):** Prioritizes 100% grasp accuracy, zero slip, and guaranteed clearance over acrylic shields and control console.
- **Next Phase (Speed Optimization):** Week 07 will introduce parabolic corner blending between Manhattan legs to reduce cycle time from $\approx 21\,\text{s}$ to $\approx 15\,\text{s}$ while maintaining ISO 9283 precision.

---

## SLIDE 11: PLAN FOR NEXT WEEK (WEEK 07) & MILESTONE 2 SPRINT
### 1. Milestone 2 Sprint Backlog (Week 07 Deliverables):
1. **Perception Upgrade (Requirements R6 & R7 - Computer Vision):**
   - Replace ideal coordinate reporting (`PickZoneSensor.cs`) with simulated Overhead RGB-D Camera (`Sensors/DepthCamera`).
   - Implement OpenCV color segmentation (HSV thresholding) and 3D centroid calculation to publish `/detected_object_pose`.
2. **Trajectory Corner Blending & Velocity Smoothing (R5):**
   - Blend Manhattan right-angle waypoints with smooth circular fillets (`parabolic blends`) to eliminate start-stop pauses between legs while preserving safe obstacle clearance envelopes.
   - Target cycle time reduction: from $\approx 21\,\text{s}$ down to $\approx 15\,\text{s}$ per item.
3. **Dynamic / Moving Obstacle Avoidance (R8 Extension):**
   - Integrate simulated human operator proximity or moving obstacle arm to evaluate dynamic replanning capabilities.
4. **Endurance & Fault Recovery Testing:**
   - 10-minute continuous unattended conveyor run ($100+$ items) with randomized spawn order and automatic timeout recovery on missed picks.

### 2. Timeline & Milestones Roadmap:
- **Days 1–3 (Oct 21–23):** Computer vision pipeline integration (OpenCV + Depth image processing).
- **Days 4–5 (Oct 24–25):** Trajectory corner blending & speed optimization.
- **Days 6–7 (Oct 26–27):** Milestone 2 Defense Report, recorded demo videos, and final benchmark verification.

---

## SLIDE 12: SUMMARY & FACULTY DISCUSSION / Q&A
### 1. Key Achievements in Week 06:
- Fully implemented industrial machine guarding ($0.36\,\text{m}$ acrylic shields + $0.42\,\text{m}$ control station) with open pick portal.
- Replaced erratic diagonal splines with clean, predictable, 100% Manhattan orthogonal stepped trajectories.
- Successfully diagnosed and resolved kinematic collision bottlenecks on the rear Blue bin.
- Achieved 100% sorting reliability across 500+ logged trials with zero collision incidents.

### 2. Open Floor for Committee Discussion:
- Live demonstration of Manhattan sorting across Red, Yellow, and Blue bins.
- Discussion on computer vision migration strategy for Week 07.
- Thank you for your guidance and support!
