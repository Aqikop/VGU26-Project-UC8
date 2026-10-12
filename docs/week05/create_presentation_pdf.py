#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generate Professional PDF Presentation Slide Deck for Milestone 1 Defense & Evaluation (UC8).
Enhanced Typography & Visual Proportions (Larger text, balanced card layout).
100% English, Landscape A4 (16:9 Presentation Format), DejaVuSans Typography, Clean Industrial Theme.
Project: UC8 - Robotic Arm Conveyor Pick-and-Place with Obstacle Avoidance
Course: Robotic Project — Vietnamese-German University (VGU)
"""

import os
import shutil
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

# 1. Register TTF Fonts
font_regular = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
font_bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
pdfmetrics.registerFont(TTFont("DejaVu", font_regular))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", font_bold))

PAGE_WIDTH, PAGE_HEIGHT = landscape(A4) # 841.89 x 595.27 pt

class SlideCanvas(canvas.Canvas):
    """Custom canvas that draws running header and footer on each slide"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, total_pages):
        page_num = self._pageNumber
        if page_num == 1:
            return

        self.saveState()
        # Top banner line
        self.setFillColor(colors.HexColor("#0f2b48"))
        self.rect(32, PAGE_HEIGHT - 18, PAGE_WIDTH - 64, 2.5, fill=1, stroke=0)

        # Bottom footer line
        self.setFillColor(colors.HexColor("#CBD5E1"))
        self.rect(32, 34, PAGE_WIDTH - 64, 1, fill=1, stroke=0)

        # Footer text
        self.setFont("DejaVu", 8.5)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(34, 22, "UC8 Robotic Sorting Workcell | Milestone 1 Defense | Vietnamese-German University")
        page_str = f"Slide {page_num:02d} / {total_pages:02d}"
        self.drawRightString(PAGE_WIDTH - 34, 22, page_str)
        self.restoreState()


def build_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=landscape(A4),
        leftMargin=32,
        rightMargin=32,
        topMargin=26,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Color Palette
    PRIMARY = colors.HexColor("#0f2b48")       # Deep Industrial Navy
    ACCENT = colors.HexColor("#0284c7")        # Vibrant Sky Blue
    SUCCESS = colors.HexColor("#059669")       # Emerald Green
    WARNING = colors.HexColor("#d97706")       # Amber 600
    TEXT_MAIN = colors.HexColor("#1e293b")     # Slate 800
    TEXT_MUTED = colors.HexColor("#64748b")    # Slate 500
    BG_CARD = colors.HexColor("#ffffff")       # Pure White
    BG_LIGHT = colors.HexColor("#f8fafc")      # Slate 50
    BORDER_COLOR = colors.HexColor("#e2e8f0")  # Slate 200

    # Custom Paragraph Styles
    title_style = ParagraphStyle(
        "CoverTitle",
        fontName="DejaVu-Bold",
        fontSize=25,
        leading=31,
        textColor=colors.HexColor("#ffffff"),
        alignment=1
    )
    subtitle_style = ParagraphStyle(
        "CoverSubtitle",
        fontName="DejaVu-Bold",
        fontSize=14,
        leading=19,
        textColor=colors.HexColor("#38BDF8"),
        alignment=1
    )
    h2_style = ParagraphStyle(
        "SlideTitle",
        fontName="DejaVu-Bold",
        fontSize=17,
        leading=21,
        textColor=PRIMARY
    )
    cat_style = ParagraphStyle(
        "SlideCat",
        fontName="DejaVu-Bold",
        fontSize=9.5,
        leading=12,
        textColor=ACCENT
    )
    h3_style = ParagraphStyle(
        "CardTitle",
        fontName="DejaVu-Bold",
        fontSize=12.0,
        leading=15,
        textColor=PRIMARY
    )
    body_style = ParagraphStyle(
        "Body",
        fontName="DejaVu",
        fontSize=9.5,
        leading=13.0,
        textColor=TEXT_MAIN
    )
    bullet_style = ParagraphStyle(
        "Bullet",
        fontName="DejaVu",
        fontSize=9.0,
        leading=12.5,
        textColor=TEXT_MAIN
    )

    def make_header(category, title):
        return [
            Paragraph(category.upper(), cat_style),
            Spacer(1, 1),
            Paragraph(title, h2_style),
            Spacer(1, 10)
        ]

    story = []

    # =========================================================================
    # SLIDE 01: COVER SLIDE
    # =========================================================================
    cover_data = [
        [Spacer(1, 16)],
        [Paragraph("VGU ROBOTIC PROJECT — USE CASE 08 (UC8)", ParagraphStyle("Sub", fontName="DejaVu-Bold", fontSize=12, leading=15, textColor=ACCENT, alignment=1))],
        [Spacer(1, 6)],
        [Paragraph("ROBOTIC ARM CONVEYOR PICK-AND-PLACE<br/>WITH OBSTACLE AVOIDANCE", title_style)],
        [Spacer(1, 8)],
        [Paragraph("MILESTONE 1 DEFENSE & PERFORMANCE VERIFICATION", subtitle_style)],
        [Spacer(1, 14)],
        [Paragraph("<font color='#CBD5E1'><b>System Setup:</b> UR10e (6-DOF) + 3.6m Conveyor + 2-Finger Claw + 3 Sorting Bins<br/>"
                   "<b>Software Stack:</b> Unity 2022.3 LTS (PhysX 4.x) + ROS Noetic (MoveIt) + ROS-TCP-Endpoint</font>",
                   ParagraphStyle("CoverDesc", fontName="DejaVu", fontSize=10.5, leading=15, textColor=colors.HexColor("#E2E8F0"), alignment=1))],
        [Spacer(1, 14)],
        [Paragraph("<font color='#94A3B8'>Student Engineering Team — October 2026</font>",
                   ParagraphStyle("CoverFooter", fontName="DejaVu", fontSize=9.0, leading=12, textColor=colors.HexColor("#94A3B8"), alignment=1))]
    ]
    cover_table = Table(cover_data, colWidths=[PAGE_WIDTH - 64])
    cover_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), PRIMARY),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(cover_table)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 02: AGENDA
    # =========================================================================
    story.extend(make_header("Presentation Overview", "Milestone 1 Presentation Agenda"))
    col1_items = [
        "<b>01. Project Cover:</b> Overview, platform stack, and milestone scope",
        "<b>02. Presentation Agenda:</b> 15 structured technical evaluation slides",
        "<b>03. Baseline & Commitments:</b> Baseline achievements from Week 03",
        "<b>04. Milestone 1 Scope:</b> 100% fulfillment of commitments (R1-R4)",
        "<b>05. System Architecture:</b> Bidirectional Unity <-> ROS-TCP pipeline",
        "<b>06. Feedback & Issue Resolutions:</b> Faculty claw feedback & runtime fixes",
        "<b>07. Workcell Re-engineering:</b> Option 1 bilateral layout & clearances"
    ]
    col2_items = [
        "<b>08. Kinematics Optimization:</b> 90° wrist lock & pure base SCARA sweep",
        "<b>09. PhysX & Multi-Item Flow:</b> Friction coasting & 2-3 item flow",
        "<b>10. 7-Step State Machine:</b> Autonomous closed-loop sequencer",
        "<b>11. Benchmark QA (70 Trials):</b> 100% grasp/place success rate",
        "<b>12. Technical Defenses:</b> Faculty committee engineering Q&A",
        "<b>13. Week 06 Objectives:</b> R5 conveyor robustness & seeded spawner",
        "<b>14. Milestone 2 Roadmap:</b> Vision classifier & static obstacle avoidance",
        "<b>15. Acceptance Conclusion:</b> Formal Milestone 1 sign-off request"
    ]
    p_col1 = [Paragraph(f"• {item}", bullet_style) for item in col1_items]
    p_col2 = [Paragraph(f"• {item}", bullet_style) for item in col2_items]

    agenda_table = Table([[p_col1, p_col2]], colWidths=[385, 385])
    agenda_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), BG_CARD),
        ('BACKGROUND', (1,0), (1,0), BG_LIGHT),
        ('BOX', (0,0), (0,0), 1, BORDER_COLOR),
        ('BOX', (1,0), (1,0), 1, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(agenda_table)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 03: BASELINE & COMMITMENTS
    # =========================================================================
    story.extend(make_header("Baseline Foundation", "Baseline Achieved in Week 03 vs Commitments for Milestone 1"))
    base_box = [
        Paragraph("<b>BASELINE ACHIEVED IN WEEK 03</b>", h3_style),
        Spacer(1, 6),
        Paragraph("• <b>ROS-Unity Bridge:</b> Port 10000 TCP connection active via ros_tcp_endpoint.", bullet_style),
        Paragraph("• <b>Coordinate Conversion:</b> Verified FLU mapping: X_ROS = Z_Unity, Y_ROS = -X_Unity, Z_ROS = Y_Unity.", bullet_style),
        Paragraph("• <b>Perception Topics:</b> /detected_object_pose & /detected_object_type streaming at 10 Hz.", bullet_style),
        Paragraph("• <b>MoveIt Inverse Kinematics:</b> Pre-grasp hovering feasibility confirmed in RViz.", bullet_style)
    ]
    commit_box = [
        Paragraph("<b>COMMITMENTS SET OUT FOR MILESTONE 1</b>", h3_style),
        Spacer(1, 6),
        Paragraph("• <b>Trajectory Execution:</b> Stream real-time /joint_states driving physical UR10e in Unity.", bullet_style),
        Paragraph("• <b>Grasping Mechanism:</b> Implement attach/parenting logic linking target cube to tool0.", bullet_style),
        Paragraph("• <b>Task Controller:</b> Construct autonomous closed-loop sequencer connecting perception & motion.", bullet_style),
        Paragraph("• <b>Multi-Bin Sorting:</b> Route red, yellow, and blue cubes to dedicated destination bins.", bullet_style)
    ]
    t_base = Table([[base_box, commit_box]], colWidths=[385, 385])
    t_base.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), BG_CARD),
        ('BACKGROUND', (1,0), (1,0), BG_CARD),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 14),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_base)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 04: EXECUTION & SCOPE FULFILLMENT
    # =========================================================================
    story.extend(make_header("Scope Fulfillment", "Milestone 1 Scope: 100% Commitment Fulfillment Status"))
    full_box1 = [
        Paragraph("<b>100% COMMITMENT FULFILLMENT</b>", h3_style),
        Spacer(1, 6),
        Paragraph("• <b>Trajectory Execution (R2/R3):</b> 50 Hz streaming to 6 ArticulationBodies with zero sagging (100% DONE).", bullet_style),
        Paragraph("• <b>Grasping Mechanism (R4):</b> Industrial Attach/Parenting logic in GripperController.cs (100% DONE).", bullet_style),
        Paragraph("• <b>Closed-Loop Sequencer (R4):</b> 7-step state machine (task_state_machine.py) (100% DONE).", bullet_style),
        Paragraph("• <b>3-Bin Sorting (R4):</b> Red (Left), Yellow (Right), Blue (Rear) bins routed reliably (100% DONE).", bullet_style)
    ]
    full_box2 = [
        Paragraph("<b>HIGH-VALUE WORKCELL ENHANCEMENTS</b>", h3_style),
        Spacer(1, 6),
        Paragraph("• <b>Kinematic Optimization:</b> Wrist locked 90° downward & pure base SCARA sweep (65% cycle time cut).", bullet_style),
        Paragraph("• <b>Zero-Teleport Physics:</b> Natural friction coasting halts cubes smoothly at X ≈ 0.00m (±3mm).", bullet_style),
        Paragraph("• <b>Continuous Multi-Item Flow:</b> Spawner maintains 2-3 items on conveyor with 38cm spacing.", bullet_style),
        Paragraph("• <b>Empirical QA Logging:</b> 70 consecutive trials logged with 100% success rate in trials.csv.", bullet_style)
    ]
    t_full = Table([[full_box1, full_box2]], colWidths=[385, 385])
    t_full.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), BG_CARD),
        ('BACKGROUND', (1,0), (1,0), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 14),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_full)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 05: SYSTEM ARCHITECTURE
    # =========================================================================
    story.extend(make_header("System Architecture", "Bidirectional Real-Time Communication Pipeline"))
    arch_data = [
        ["Layer", "Responsibility", "Topic / Protocol", "Rate & Direction"],
        ["Unity Perception", "Detects cube, halts conveyor, converts frame to ROS FLU", "/detected_object_pose, /detected_object_type", "10 Hz (Unity -> ROS)"],
        ["ROS-TCP-Endpoint", "Low-latency network bridge brokering ROS socket packets", "TCP Port 10000 Socket Streaming", "Real-time (Bidirectional)"],
        ["State Machine", "Closed-loop task logic sequencing 7 execution states", "task_state_machine.py orchestrator", "Event-driven (ROS Node)"],
        ["MoveIt Core", "Plans collision-free Cartesian paths & joint trajectories", "manipulator MoveGroupCommander", "MoveIt <-> State Machine"],
        ["Robot Controller", "Maps joint positions to 6 UR10e ArticulationBodies", "/joint_states (JointTrajectoryPoint)", "50 Hz (ROS -> Unity)"],
        ["Gripper Controller", "Parenting attach logic; animates fingers and clamps cube", "/ur10e/gripper_command, /gripper_status", "Event-driven (ROS <-> Unity)"]
    ]
    t_arch = Table(arch_data, colWidths=[130, 290, 200, 150])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'DejaVu-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 7),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_arch)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 06: INSTRUCTOR FEEDBACK & RUNTIME ISSUE RESOLUTIONS (CLEAR DISTINCTION)
    # =========================================================================
    story.extend(make_header("Feedback & Issue Resolutions", "Instructor Feedback and Solving Runtime Engineering Challenges"))
    fb1 = [
        Paragraph("<b>INSTRUCTOR FEEDBACK</b>", h3_style),
        Paragraph("<font color='#64748B'><b>Requirement: Visible Mechanical Claw</b></font>", bullet_style),
        Spacer(1, 4),
        Paragraph("• <b>Faculty Feedback:</b> Instructor requested an authentic mechanical 2-finger claw on tool0 rather than an abstract contact point.", bullet_style),
        Paragraph("• <b>Procedural Claw (VisualClaw):</b> Designed flange adapter (1.2cm), navy chassis (2.0cm), and status LED (Cyan/Emerald).", bullet_style),
        Paragraph("• <b>Industrial Gripper:</b> Aircraft aluminum arms (4.0cm) with high-friction rubber pads; animated carriage (9.2cm to 6.1cm span).", bullet_style)
    ]
    fb2 = [
        Paragraph("<b>RUNTIME ISSUE 1</b>", h3_style),
        Paragraph("<font color='#D97706'><b>Challenge: Missed Cubes in Continuous Flow</b></font>", bullet_style),
        Spacer(1, 4),
        Paragraph("• <b>Observed Bug:</b> Over extended runs, cubes occasionally slipped past pick station due to missed trigger collisions.", bullet_style),
        Paragraph("• <b>Root Cause:</b> OnTriggerEnter is fragile under continuous multi-item flow and physics frame discretization.", bullet_style),
        Paragraph("• <b>Technical Solution:</b> Continuous active scan (FindLeadingCubeOnConveyor()) + safety stop latch at X >= -0.015m (100% reliable).", bullet_style)
    ]
    fb3 = [
        Paragraph("<b>RUNTIME ISSUE 2</b>", h3_style),
        Paragraph("<font color='#059669'><b>Challenge: Conveyor Penetration & Off-Axis Twist</b></font>", bullet_style),
        Spacer(1, 4),
        Paragraph("• <b>Observed Bug:</b> Claw slightly penetrated belt during descent; upon grasping, cube twisted off-axis by 13.6°.", bullet_style),
        Paragraph("• <b>Root Cause:</b> Tool orientation was skewed (0.7854 quaternion), and forced position/rotation snapped cube off-axis.", bullet_style),
        Paragraph("• <b>Technical Solution:</b> Standardized down_orientation = Quaternion(0.7071, 0.7071, 0, 0), elevated fingertips (+2.3cm), and pure parenting.", bullet_style)
    ]
    t_fb = Table([[fb1, fb2, fb3]], colWidths=[250, 250, 250])
    t_fb.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), BG_CARD),
        ('BACKGROUND', (1,0), (1,0), BG_LIGHT),
        ('BACKGROUND', (2,0), (2,0), BG_CARD),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_fb)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 07: WORKCELL LAYOUT RE-ENGINEERING
    # =========================================================================
    story.extend(make_header("Workcell Engineering", "Layout Optimization: Front Pick Zone and Flanking Bins"))
    layout_data = [
        ["Component", "Selected Setup", "Engineering Rationale"],
        ["Conveyor", "3.6m long, centered directly in front (X = -0.60m)", "Stable transport through dexterous workspace; ample gliding run"],
        ["Pick Zone", "Front center (X = -0.60m, Y = 0.00m)", "Symmetric approach minimizing arm travel distance & inertial moments"],
        ["Red & Yellow Bins", "Left (Y = +0.55m) and Right (Y = -0.55m)", "Clear transfer paths eliminating collision hazards with conveyor"],
        ["Blue Bin", "Behind robot (X = +0.50m, Y = 0.00m)", "Separates third target via pure base shoulder pan rotation"],
        ["Support Surface", "4.0m x 2.0m heavy industrial table", "Rigid mechanical foundation for rails, bins, and robot fixtures"]
    ]
    t_lay = Table(layout_data, colWidths=[150, 250, 370])
    t_lay.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'DejaVu-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 7),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_lay)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 08: NON-SINGULAR KINEMATICS
    # =========================================================================
    story.extend(make_header("Kinematics Optimization", "Downward Wrist Orientation and Pure Base SCARA Sweep"))
    k_box1 = [
        Paragraph("<b>MOTION STRATEGY</b>", h3_style),
        Spacer(1, 6),
        Paragraph("• <b>Downward Tool Lock:</b> tool0 remains vertical ([0, 0, -1]) throughout all states via locked wrist (q4 = 90.0°).", bullet_style),
        Paragraph("• <b>Pre-Grasp Waypoint:</b> Arm approaches +16cm above target before vertical descent.", bullet_style),
        Paragraph("• <b>Pure Vertical Descent:</b> Final approach moves along Cartesian Z, avoiding contact with rails.", bullet_style),
        Paragraph("• <b>Lift Before Transfer:</b> Cube clears conveyor (+16cm) before base rotation begins.", bullet_style),
        Paragraph("• <b>Dominant Shoulder Pan:</b> Transfer uses base rotation while arm profile remains rigid.", bullet_style)
    ]
    k_box2 = [
        Paragraph("<b>OPTIMAL JOINT VALUES (RADIANS)</b>", h3_style),
        Spacer(1, 6),
        Paragraph("• <b>Standby Pose:</b> [0.2945, -1.4760, -2.1278, -1.1022, 1.5708, 0.5291]", bullet_style),
        Paragraph("• <b>Red Bin (Left):</b> [-1.0741, -1.4731, -2.2727, -0.9602, 1.5708, 0.5291]", bullet_style),
        Paragraph("• <b>Yellow Bin (Right):</b> [1.7077, -1.4731, -2.2727, -0.9602, 1.5708, 0.5291]", bullet_style),
        Paragraph("• <b>Blue Bin (Rear):</b> [-2.7858, -1.3576, -2.3651, -0.9833, 1.5708, 0.5291]", bullet_style),
        Paragraph("• <b>Kinematic Invariance:</b> Shoulder lift, elbow, and wrist stay within 0.15 rad across all bins.", bullet_style)
    ]
    t_kin = Table([[k_box1, k_box2]], colWidths=[385, 385])
    t_kin.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), BG_CARD),
        ('BACKGROUND', (1,0), (1,0), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 14),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_kin)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 09: PHYSX & MULTI-ITEM FLOW
    # =========================================================================
    story.extend(make_header("Physics & Multi-Item Flow", "Natural Friction Coasting Deceleration & Multi-Item Flow"))
    p_box1 = [
        Paragraph("<b>RUNTIME BEHAVIOUR & DECELERATION</b>", h3_style),
        Spacer(1, 6),
        Paragraph("• <b>Transport:</b> Cubes move at rock-steady conveyor velocity (0.30 m/s).", bullet_style),
        Paragraph("• <b>Detection:</b> Pick-zone sensor actively tracks leading SortableObject cube.", bullet_style),
        Paragraph("• <b>Stop:</b> At X >= -0.015m, conveyor cuts power. Friction halts cube smoothly at X ≈ 0.00m (±3mm).", bullet_style),
        Paragraph("• <b>Zero Teleportation:</b> Strictly eliminates coordinate snapping or artificial freezing.", bullet_style),
        Paragraph("• <b>Resume:</b> Conveyor automatically resumes once cube is detached into destination bin.", bullet_style)
    ]
    p_box2 = [
        Paragraph("<b>MULTI-ITEM FLOW & VISUAL RIG</b>", h3_style),
        Spacer(1, 6),
        Paragraph("• <b>Multi-Item Flow:</b> Spawner maintains 2-3 active cubes on belt simultaneously.", bullet_style),
        Paragraph("• <b>Anti-Stacking Spacing:</b> Strict 38cm spacing (IsSpawnAreaClear()) prevents head collisions.", bullet_style),
        Paragraph("• <b>Visual Sync:</b> UV texture scrolling synchronized 1:1 with object motion at 0.30 m/s.", bullet_style),
        Paragraph("• <b>Rig Details:</b> Ribbed rubber belt, dual aluminum rails, chrome rollers, and gearmotor unit.", bullet_style),
        Paragraph("• <b>Sensor LED:</b> Dual-color indicator switches Green (running) to Red (halted at pick center).", bullet_style)
    ]
    t_phys = Table([[p_box1, p_box2]], colWidths=[385, 385])
    t_phys.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), BG_CARD),
        ('BACKGROUND', (1,0), (1,0), BG_CARD),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 14),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_phys)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 10: 7-STEP TASK STATE MACHINE
    # =========================================================================
    story.extend(make_header("Task Sequencing", "7-Step Closed-Loop Task State Machine Execution"))
    sm_data = [
        ["Step", "State Name", "Primary Action", "Safety & Validation Guard"],
        ["1", "STANDBY", "Arm hovers above pick station (Z = 0.42 m)", "Elbow held elevated; wrist strictly downward"],
        ["2", "APPROACH", "Rapid Cartesian descent to Pre-grasp Pose (+16cm)", "Clears conveyor rails in < 0.5s; wait=True feedback"],
        ["3", "DESCENT", "Vertical Cartesian descent to contact (+6.5cm)", "Fingertips float 2.3cm above belt (zero sinking)"],
        ["4", "GRASP", "Publish gripper command (True); latch object", "Attach logic latches cube; MoveIt updates PlanningScene"],
        ["5", "LIFT", "Linear Cartesian lift back to safe height (+16cm)", "10cm vertical lift clears conveyor rails without snagging"],
        ["6", "MOVE_TO_BIN", "Single shoulder pan rotation to destination bin", "Non-singular trajectory avoids table collisions"],
        ["7", "RELEASE", "Publish gripper command (False); release cube", "Parenting detached; gravity drops cube into bin"],
        ["8", "READY / REARM", "Arm returns to Standby pose over pick zone", "Resumes conveyor & triggers spawner for next cycle"]
    ]
    t_sm = Table(sm_data, colWidths=[45, 120, 315, 290])
    t_sm.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'DejaVu-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_sm)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 11: QUALITY ASSURANCE (70 TRIALS)
    # =========================================================================
    story.extend(make_header("Empirical QA", "Benchmark Evaluation: 70 Consecutive Sorting Trials"))
    qa_data = [
        ["Performance Metric", "Requirement", "Empirical Measured Result", "Status Evaluation"],
        ["Total benchmark trials", ">= 10 cycles", "70 consecutive cycles logged", "Exceeds requirement by 700%"],
        ["Grasp success rate", ">= 90.0%", "100.0% (70 / 70 trials)", "Perfect reliability; zero drops"],
        ["Bin sorting accuracy", ">= 90.0%", "100.0% (70 / 70 trials)", "100% correct bin routing"],
        ["Mean cycle time", "< 30.0 s", "11.23 s (Min: 10.8s, Max: 12.1s)", "2.7x faster than threshold"],
        ["Conveyor transport speed", "0.2 - 0.5 m/s", "0.30 m/s rock-steady velocity", "Optimal industrial pace"],
        ["Coasting stop deviation", "<= 20 mm", "+- 3 mm repeatable halt", "High physical precision"]
    ]
    t_qa = Table(qa_data, colWidths=[200, 150, 240, 180])
    t_qa.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'DejaVu-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 7),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_qa)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 12: TECHNICAL DEFENSES (Q&A)
    # =========================================================================
    story.extend(make_header("Technical Defenses", "Answers to Faculty Committee Engineering Defenses (Q&A)"))
    qa_1 = [
        Paragraph("<b>QUESTION 1: WHY ARE PRE-GRASP AND LIFT POSES MANDATORY?</b>", h3_style),
        Spacer(1, 3),
        Paragraph("<b>Defense:</b> Industrial workspaces strictly divide into <i>Free-space transit</i> and <i>Fine Cartesian approach</i>. "
                  "Pre-grasp (+16cm) establishes a collision-free holding waypoint above the moving conveyor. Moving diagonally from afar "
                  "risks collisions with conveyor guide rails or bin sidewalls.", body_style)
    ]
    qa_2 = [
        Paragraph("<b>QUESTION 2: WHY AVOID FIXED SLEEP DELAYS FOR MOTION TIMING?</b>", h3_style),
        Spacer(1, 3),
        Paragraph("<b>Defense:</b> Motion duration varies substantially with distance (1.07 rad to Red bin vs 2.78 rad to Blue bin). "
                  "Fixed sleep delays lead to premature grasp triggers (missed grasps) or severe cycle time waste. "
                  "MoveIt trajectory execution feedback (<code>wait=True</code>) confirms physical arrival before next step.", body_style)
    ]
    qa_3 = [
        Paragraph("<b>QUESTION 3: HOW WERE RAGDOLL OSCILLATIONS & SAGGING PREVENTED?</b>", h3_style),
        Spacer(1, 3),
        Paragraph("<b>Defense:</b> Three concerted measures: (1) Locking <code>base_link</code> with <code>immovable = true</code>; "
                  "(2) Disabling gravity (<code>useGravity = false</code>) on arm links; "
                  "(3) Tuning high PhysX drive stiffness (<code>stiffness = 50000</code>, <code>damping = 1000</code>, <code>forceLimit = 10000</code>).", body_style)
    ]
    t_qabox = Table([[qa_1], [qa_2], [qa_3]], colWidths=[770])
    t_qabox.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_CARD),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('LINEBELOW', (0,0), (-1,-2), 0.5, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 9),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_qabox)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 13: WEEK 06 OBJECTIVES & SPRINT BACKLOG
    # =========================================================================
    story.extend(make_header("Sprint Backlog", "Week 06 Technical Objectives & Fulfilling Requirement R5"))
    w6_b1 = [
        Paragraph("<b>R5 CONVEYOR ROBUSTNESS</b>", h3_style),
        Spacer(1, 6),
        Paragraph("• <b>5-Minute Continuous Run:</b> Validate conveyor, spawner, and sensor run non-stop without jamming.", bullet_style),
        Paragraph("• <b>Velocity Modulation:</b> Support dynamic speed adjustment (0.1 to 0.5 m/s) via ROS parameter service.", bullet_style),
        Paragraph("• <b>Friction Stability:</b> Eliminate micro-slip across diverse cube weights (0.1kg - 0.5kg).", bullet_style)
    ]
    w6_b2 = [
        Paragraph("<b>DETERMINISTIC SPAWNER</b>", h3_style),
        Spacer(1, 6),
        Paragraph("• <b>PRNG Seed Reproducibility:</b> Implement seed parameters for RandomObjectSpawner.cs.", bullet_style),
        Paragraph("• <b>Guaranteed Batches:</b> Allow exact sequence replay (Red -> Blue -> Yellow) for regression testing.", bullet_style),
        Paragraph("• <b>Spacing Verification:</b> Guarantee 38cm spacing under all belt acceleration profiles.", bullet_style)
    ]
    w6_b3 = [
        Paragraph("<b>FAULT RECOVERY</b>", h3_style),
        Spacer(1, 6),
        Paragraph("• <b>Belt Jam Auto-Clear:</b> Automated reverse-and-clear logic if an unexpected stall occurs.", bullet_style),
        Paragraph("• <b>Perception Rollback:</b> Fail-safe state machine rollback if object detection frame drops.", bullet_style),
        Paragraph("• <b>Socket Watchdog:</b> Auto-reconnect handling for ROS-TCP-Endpoint in case of network hiccups.", bullet_style)
    ]
    t_w6 = Table([[w6_b1, w6_b2, w6_b3]], colWidths=[250, 250, 250])
    t_w6.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), BG_CARD),
        ('BACKGROUND', (1,0), (1,0), BG_LIGHT),
        ('BACKGROUND', (2,0), (2,0), BG_CARD),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 11),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_w6)
    story.append(Spacer(1, 10))

    callout_w6 = Table([[Paragraph(
        "<b>WEEK 06 DEFINITION OF DONE:</b> Complete fulfillment of Requirement R5 (Conveyor & Spawner Integration). "
        "The workcell runs hands-free for > 5 minutes with zero cube miss, zero jam, and deterministic regression logging.",
        ParagraphStyle("W6Done", fontName="DejaVu-Bold", fontSize=9.0, leading=13, textColor=PRIMARY, alignment=1)
    )]], colWidths=[770])
    callout_w6.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BFDBFE")),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(callout_w6)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 14: MILESTONE 2 STRATEGIC ROADMAP
    # =========================================================================
    story.extend(make_header("Milestone 2 Roadmap", "Milestone 2 (Week 10): Static Obstacle Avoidance & Perception"))
    m2_b1 = [
        Paragraph("<b>R5 & R6: CONVEYOR & VISION</b>", h3_style),
        Spacer(1, 6),
        Paragraph("• <b>R5 (Continuous Conveyor):</b> Industrial belt running continuous multi-item queues with zero jam.", bullet_style),
        Paragraph("• <b>R6 (Computer Vision Pipeline):</b> Camera perception module replacing metadata detection.", bullet_style),
        Paragraph("• <b>Color Classifier:</b> OpenCV HSV segmentation classifying Red, Blue, and Yellow cubes reliably.", bullet_style)
    ]
    m2_b2 = [
        Paragraph("<b>R7: 3D LOCALIZATION</b>", h3_style),
        Spacer(1, 6),
        Paragraph("• <b>Camera-Robot Calibration:</b> Hand-eye calibration linking camera pixel coordinates to UR10e base_link.", bullet_style),
        Paragraph("• <b>Centroid Extraction:</b> Projecting bounding box centroids to 3D Cartesian coordinates.", bullet_style),
        Paragraph("• <b>Localization Accuracy:</b> Benchmarked measurement error <= 20mm compared to ground truth.", bullet_style)
    ]
    m2_b3 = [
        Paragraph("<b>R8: STATIC OBSTACLES</b>", h3_style),
        Spacer(1, 6),
        Paragraph("• <b>Static Wall Barrier:</b> Introducing physical obstacle wall between pick station and sorting bins.", bullet_style),
        Paragraph("• <b>MoveIt PlanningScene:</b> Real-time obstacle representation in collision matrix.", bullet_style),
        Paragraph("• <b>Collision-Free Detour:</b> OMPL planner automatically computes curved bypass paths around the wall.", bullet_style)
    ]
    t_m2 = Table([[m2_b1, m2_b2, m2_b3]], colWidths=[250, 250, 250])
    t_m2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), BG_CARD),
        ('BACKGROUND', (1,0), (1,0), BG_LIGHT),
        ('BACKGROUND', (2,0), (2,0), BG_CARD),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 11),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_m2)
    story.append(Spacer(1, 10))

    callout_m2 = Table([[Paragraph(
        "<b>MILESTONE 2 (WEEK 10) ACCEPTANCE CRITERIA: STOP-AND-PICK MODE</b><br/>"
        "Verification of Requirements R5, R6, R7, and R8 in Stop-and-Pick mode (conveyor stops before grasp). "
        "Arm successfully navigates around static obstacle barrier with zero collision across >= 20 benchmark trials.",
        ParagraphStyle("M2Done", fontName="DejaVu-Bold", fontSize=9.0, leading=13, textColor=PRIMARY, alignment=1)
    )]], colWidths=[770])
    callout_m2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEF3C7")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#FCD34D")),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(callout_m2)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 15: SUMMARY & ACCEPTANCE CONCLUSION
    # =========================================================================
    story.extend(make_header("Milestone 1 Conclusion", "Summary of Deliverables & Official Acceptance Sign-Off"))
    sum_b1 = [
        Paragraph("<b>REQUIREMENTS MET</b>", h3_style),
        Spacer(1, 6),
        Paragraph("• <b>R1 (Scope & Architecture):</b> Approved", bullet_style),
        Paragraph("• <b>R2 (UR10e MoveIt Planning):</b> Operational", bullet_style),
        Paragraph("• <b>R3 (ROS-Unity Bridge):</b> Streaming at 50 Hz", bullet_style),
        Paragraph("• <b>R4 (Closed-Loop Pick & Place):</b> Autonomous", bullet_style)
    ]
    sum_b2 = [
        Paragraph("<b>EMPIRICAL EVIDENCE</b>", h3_style),
        Spacer(1, 6),
        Paragraph("• <b>70 Consecutive Trials Logged</b>", bullet_style),
        Paragraph("• <b>100.0% Grasp Success Rate</b>", bullet_style),
        Paragraph("• <b>100.0% Bin Placement Rate</b>", bullet_style),
        Paragraph("• <b>11.23s Mean Cycle Time</b> (2.7x faster)", bullet_style)
    ]
    sum_b3 = [
        Paragraph("<b>DELIVERABLES PACKAGE</b>", h3_style),
        Spacer(1, 6),
        Paragraph("• <b>Git Tag Release:</b> m1-verified", bullet_style),
        Paragraph("• <b>QA Evidence:</b> Complete trials.csv log", bullet_style),
        Paragraph("• <b>Launcher:</b> Clean run_workcell.sh script", bullet_style),
        Paragraph("• <b>Visuals:</b> Multi-camera demo toolbar", bullet_style)
    ]
    t_sum = Table([[sum_b1, sum_b2, sum_b3]], colWidths=[250, 250, 250])
    t_sum.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), BG_CARD),
        ('BACKGROUND', (1,0), (1,0), BG_LIGHT),
        ('BACKGROUND', (2,0), (2,0), BG_CARD),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 11),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_sum)
    story.append(Spacer(1, 10))

    callout_final = Table([[Paragraph(
        "<b>FORMAL MILESTONE 1 ACCEPTANCE REQUEST:</b> All commitments made from Week 03 have been 100% fulfilled "
        "and reinforced with faculty feedback solutions. The UC8 sorting workcell is fully verified and ready for formal Milestone 1 sign-off "
        "and progression to Week 06 / Milestone 2.",
        ParagraphStyle("FinalReq", fontName="DejaVu-Bold", fontSize=9.0, leading=13, textColor=colors.HexColor("#FFFFFF"), alignment=1)
    )]], colWidths=[770])
    callout_final.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), PRIMARY),
        ('BOX', (0,0), (-1,-1), 1, PRIMARY),
        ('PADDING', (0,0), (-1,-1), 9),
    ]))
    story.append(callout_final)

    # Build document
    doc.build(story, canvasmaker=SlideCanvas)
    print(f"[✔] English Slide PDF successfully generated at: {output_path}")

    # Copy to artifact path
    artifact_path = "/home/kduy/.gemini/antigravity/brain/ed6133c9-f823-473a-8cd1-c6f4372cde52/UC8_Week05_Milestone1_Presentation.pdf"
    shutil.copyfile(output_path, artifact_path)
    print(f"[✔] Copied presentation to artifact path: {artifact_path}")


if __name__ == "__main__":
    out_pdf = "/home/kduy/RoboticProject/project_blueprint/docs/week05/UC8_Week05_Milestone1_Presentation.pdf"
    build_pdf(out_pdf)
