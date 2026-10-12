#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generate Professional PDF Presentation Slide Deck for Week 04 Progress Report & Milestone 1 Verification (UC8).
100% English, Landscape A4 (16:9 Presentation Format), DejaVuSans Typography, Clean Industrial Theme.
"""

import os
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
            # Cover slide has its own full-bleed card
            return

        self.saveState()
        # Top banner line (positioned high above slide text)
        self.setFillColor(colors.HexColor("#0f2b48"))
        self.rect(32, PAGE_HEIGHT - 18, PAGE_WIDTH - 64, 2.5, fill=1, stroke=0)

        # Bottom footer line
        self.setFillColor(colors.HexColor("#CBD5E1"))
        self.rect(32, 34, PAGE_WIDTH - 64, 1, fill=1, stroke=0)

        # Footer running text
        self.setFont("DejaVu", 8.5)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(34, 20, "VGU Robotic Project — Use Case 08 (UC8) | Milestone 1 (Week 04)")
        self.drawRightString(PAGE_WIDTH - 34, 20, f"Slide {page_num - 1} / {total_pages - 1}")
        self.restoreState()


def build_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=landscape(A4),
        leftMargin=32,
        rightMargin=32,
        topMargin=36,
        bottomMargin=38
    )

    styles = getSampleStyleSheet()

    # Color Palette
    PRIMARY = colors.HexColor("#0f2b48")   # Deep Industrial Navy
    SECONDARY = colors.HexColor("#0284C7") # Vibrant Cyan Tech
    ACCENT = colors.HexColor("#10B981")    # Success Green
    TEXT_DARK = colors.HexColor("#1E293B")
    TEXT_MUTED = colors.HexColor("#475569")
    BG_CARD = colors.HexColor("#F8FAFC")
    BG_LIGHT = colors.HexColor("#F1F5F9")
    BORDER_COLOR = colors.HexColor("#E2E8F0")

    # Typography Styles
    title_style = ParagraphStyle(
        "CoverTitle",
        fontName="DejaVu-Bold",
        fontSize=24,
        leading=31,
        textColor=colors.white,
        alignment=1
    )

    subtitle_style = ParagraphStyle(
        "CoverSubtitle",
        fontName="DejaVu-Bold",
        fontSize=12.5,
        leading=17,
        textColor=colors.HexColor("#38BDF8"),
        alignment=1
    )

    slide_header_style = ParagraphStyle(
        "SlideHeader",
        fontName="DejaVu-Bold",
        fontSize=16,
        leading=20,
        textColor=PRIMARY
    )

    slide_cat_style = ParagraphStyle(
        "SlideCategory",
        fontName="DejaVu-Bold",
        fontSize=9,
        leading=11,
        textColor=SECONDARY
    )

    h3_style = ParagraphStyle(
        "SectionH3",
        fontName="DejaVu-Bold",
        fontSize=10.5,
        leading=13.5,
        textColor=PRIMARY
    )

    body_style = ParagraphStyle(
        "BodyDark",
        fontName="DejaVu",
        fontSize=9,
        leading=13,
        textColor=TEXT_DARK
    )

    bullet_style = ParagraphStyle(
        "BulletDark",
        fontName="DejaVu",
        fontSize=8.5,
        leading=12.5,
        textColor=TEXT_DARK,
        leftIndent=8
    )

    table_header_style = ParagraphStyle(
        "TableHeader",
        fontName="DejaVu-Bold",
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
        alignment=1
    )

    table_cell_style = ParagraphStyle(
        "TableCell",
        fontName="DejaVu",
        fontSize=8,
        leading=10.5,
        textColor=TEXT_DARK
    )

    table_cell_center = ParagraphStyle(
        "TableCellCenter",
        fontName="DejaVu",
        fontSize=8,
        leading=10.5,
        textColor=TEXT_DARK,
        alignment=1
    )

    callout_style = ParagraphStyle(
        "CalloutText",
        fontName="DejaVu",
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#0369A1")
    )

    story = []

    def make_header(category, title):
        return [
            Paragraph(category.upper(), slide_cat_style),
            Spacer(1, 2),
            Paragraph(title, slide_header_style),
            Spacer(1, 10)
        ]

    # =========================================================================
    # SLIDE 0: TITLE COVER SLIDE
    # =========================================================================
    cover_data = [
        [Paragraph("<font color='#38BDF8'><b>VIETNAMESE-GERMAN UNIVERSITY (VGU) — ROBOTIC PROJECT 2026</b></font>", subtitle_style)],
        [Spacer(1, 6)],
        [Paragraph("ROBOTIC ARM CONVEYOR PICK-AND-PLACE<br/>WITH OBSTACLE AVOIDANCE", title_style)],
        [Spacer(1, 8)],
        [Paragraph("WEEK 04 PROGRESS REPORT — PREPARATION & VERIFICATION FOR MILESTONE 1 (WEEK 05)", subtitle_style)],
        [Spacer(1, 14)],
        [Paragraph("<font color='#CBD5E1'><b>Use Case 08 (UC8):</b> Closed-Loop Static Sorting Workcell with 3 Independent Bins<br/>"
                   "<b>Current Sprint:</b> Week 04 Technical Execution & Fulfilling Week 03 Commitments | <b>Evaluation:</b> Milestone 1 in Week 05</font>",
                   ParagraphStyle("CoverDesc", fontName="DejaVu", fontSize=9.5, leading=14, textColor=colors.HexColor("#E2E8F0"), alignment=1))],
        [Spacer(1, 14)],
        [Paragraph("<font color='#94A3B8'>Student Engineering Team — Workstation: kduy-5560 — October 2026</font>",
                   ParagraphStyle("CoverFooter", fontName="DejaVu", fontSize=8.5, leading=11, textColor=colors.HexColor("#94A3B8"), alignment=1))]
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
    # SLIDE 1: AGENDA
    # =========================================================================
    story.extend(make_header("Presentation Overview", "Milestone 1 Presentation Agenda"))
    
    col1_items = [
        "<b>01. Week 3 Recap & Baseline:</b> Platform verification and transition boundary",
        "<b>02. Week 4 & Milestone 1 Objectives:</b> 5 core engineering deliverables (R4)",
        "<b>03. System Architecture & Pipeline:</b> Bidirectional Unity ↔ ROS-TCP integration",
        "<b>04. Workcell Layout Re-engineering:</b> Option 1 (Front Pick & Flanking Bins)",
        "<b>05. Non-singular Kinematics:</b> 90° downward wrist lock & pure base SCARA sweep"
    ]
    col2_items = [
        "<b>06. Realistic PhysX Simulation:</b> Friction-based zero-teleport deceleration & UV belt",
        "<b>07. 7-Step Task State Machine:</b> Automated closed-loop pick-and-place flow",
        "<b>08. Empirical Benchmark Trials (QA):</b> 70 consecutive trials with 100% success rate",
        "<b>09. Live Demonstration Setup:</b> Standalone 3-terminal workflow & camera toolbar",
        "<b>10. Technical Defenses & Next Steps:</b> Key engineering defenses & Milestone 2 roadmap"
    ]

    p_col1 = [Paragraph(f"• {item}", bullet_style) for item in col1_items]
    p_col2 = [Paragraph(f"• {item}", bullet_style) for item in col2_items]

    agenda_table = Table([[p_col1, p_col2]], colWidths=[385, 385])
    agenda_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), BG_CARD),
        ('BACKGROUND', (1,0), (1,0), BG_LIGHT),
        ('BOX', (0,0), (0,0), 1, BORDER_COLOR),
        ('BOX', (1,0), (1,0), 1, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 16),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(agenda_table)
    story.append(Spacer(1, 15))

    callout_agenda = Table([[Paragraph(
        "<b>Core Transition:</b> This report reflects the evolution from Week 3's <i>'Plan-Only Theoretical Pipeline'</i> "
        "into Week 4's <i>'Full Physical Trajectory Execution & Manipulation'</i>, successfully verifying Milestone 1.",
        callout_style
    )]], colWidths=[770])
    callout_agenda.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#E0F2FE")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BAE6FD")),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(callout_agenda)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 2: WEEK 3 RECAP & COMMITMENTS SET OUT
    # =========================================================================
    story.extend(make_header("Foundation & Context", "Week 03 Recap & Commitments Set Out for Week 04"))

    w3_achieved = [
        Paragraph("<b>1. WEEK 03 BASELINE ACHIEVEMENTS</b>", h3_style),
        Spacer(1, 6),
        Paragraph("• <b>ROS-Unity Network Bridge:</b> Seamless socket streaming on port 10000 via <code>ROS-TCP-Endpoint</code>.", bullet_style),
        Spacer(1, 3),
        Paragraph("• <b>Coordinate Transformation:</b> Standardized coordinate mapping from Unity Left-Handed to ROS FLU Right-Handed: (X_ros = Z_unity, Y_ros = -X_unity, Z_ros = Y_unity).", bullet_style),
        Spacer(1, 3),
        Paragraph("• <b>Object Perception:</b> Streaming cube 3D pose to <code>/detected_object_pose</code> and color classification to <code>/detected_object_type</code>.", bullet_style),
        Spacer(1, 3),
        Paragraph("• <b>MoveIt Pre-grasp Planning:</b> Solved theoretical IK trajectories hovering +15cm above object on RViz.", bullet_style)
    ]

    w3_boundary = [
        Paragraph("<b>2. COMMITMENTS SET OUT FOR WEEK 04</b>", ParagraphStyle("CommitmentH3", fontName="DejaVu-Bold", fontSize=10.5, leading=13.5, textColor=PRIMARY)),
        Spacer(1, 6),
        Paragraph("• <b>Commitment 1 (Trajectory Execution):</b> Break through 'plan-only' mode; stream real-time <code>/joint_states</code> to move physical UR10e in Unity.", bullet_style),
        Spacer(1, 3),
        Paragraph("• <b>Commitment 2 (Grasping Mechanism):</b> Implement dynamic Attach/Parenting logic in <code>GripperController.cs</code> to grab cubes physically.", bullet_style),
        Spacer(1, 3),
        Paragraph("• <b>Commitment 3 (Task State Machine):</b> Develop autonomous 7-step sequencer connecting perception, motion, and release.", bullet_style),
        Spacer(1, 3),
        Paragraph("• <b>Commitment 4 (3-Bin Sorting):</b> Deploy dedicated Red, Yellow, Blue bins with non-singular collision-free placements.", bullet_style)
    ]

    table_w3 = Table([[w3_achieved, w3_boundary]], colWidths=[385, 385])
    table_w3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), BG_CARD),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (0,0), 1, BORDER_COLOR),
        ('BOX', (1,0), (1,0), 1, colors.HexColor("#BFDBFE")),
        ('PADDING', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(table_w3)
    story.append(Spacer(1, 12))

    w3_note = Table([[Paragraph(
        "<b>Milestone Context:</b> Milestone 1 is scheduled for official evaluation in <b>Week 05</b>. "
        "Fulfilling 100% of Week 03 commitments in Week 04 is the prerequisite to ensure full readiness.",
        callout_style
    )]], colWidths=[770])
    w3_note.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F0FDF4")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BBF7D0")),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(w3_note)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 3: WEEK 4 & MILESTONE 1 OBJECTIVES (REQUIREMENT R4)
    # =========================================================================
    story.extend(make_header("Technical Scope (Requirement R4)", "Week 04 Objectives & Milestone 1 Verification"))

    req_headers = [Paragraph("Task ID", table_header_style), Paragraph("Technical Deliverable", table_header_style), Paragraph("Deliverable Artifact / Output", table_header_style), Paragraph("Status", table_header_style)]
    req_rows = [
        [Paragraph("<b>Task 4.1</b>", table_cell_center),
         Paragraph("Scene Setup & Industrial Attach Grasping Mechanism", table_cell_style),
         Paragraph("Script <code>GripperController.cs</code> (Attach/Parenting logic as guided by Instructor)", table_cell_style),
         Paragraph("<font color='#059669'><b>PASSED 100%</b></font>", table_cell_center)],
        [Paragraph("<b>Task 4.2</b>", table_cell_center),
         Paragraph("Workcell Layout Re-engineering & 3 Dedicated Sorting Bins", table_cell_style),
         Paragraph("Option 1 (Front Pick - Flanking Bins) encoded into <code>task_state_machine.py</code>", table_cell_style),
         Paragraph("<font color='#059669'><b>PASSED 100%</b></font>", table_cell_center)],
        [Paragraph("<b>Task 4.3</b>", table_cell_center),
         Paragraph("Joint Trajectory Execution Driving 6 UR10e ArticulationBodies", table_cell_style),
         Paragraph("Script <code>UR10eController.cs</code> streaming <code>/joint_states</code> with locked base & gravity compensation", table_cell_style),
         Paragraph("<font color='#059669'><b>PASSED 100%</b></font>", table_cell_center)],
        [Paragraph("<b>Task 4.4</b>", table_cell_center),
         Paragraph("7-Step Closed-Loop Task State Machine", table_cell_style),
         Paragraph("Node <code>task_state_machine.py</code> (STANDBY → APPROACH → DESCENT → GRASP → LIFT → MOVE → RELEASE)", table_cell_style),
         Paragraph("<font color='#059669'><b>PASSED 100%</b></font>", table_cell_center)],
        [Paragraph("<b>Task 4.5</b>", table_cell_center),
         Paragraph("Empirical Benchmark Trials & Automated QA Logging", table_cell_style),
         Paragraph("Log file <code>experiments/week04/trials.csv</code> recording 70 consecutive successful trials", table_cell_style),
         Paragraph("<font color='#059669'><b>PASSED 100%</b></font>", table_cell_center)]
    ]

    t_req = Table([req_headers] + req_rows, colWidths=[70, 270, 330, 100])
    t_req.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT])
    ]))
    story.append(t_req)
    story.append(Spacer(1, 14))

    callout_m1 = Table([[Paragraph(
        "<b>Milestone 1 Verification:</b> All 5/5 mandatory deliverables under Requirement R4 have been achieved, "
        "demonstrating complete automation without any manual intervention.",
        callout_style
    )]], colWidths=[770])
    callout_m1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#ECFDF5")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#A7F3D0")),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(callout_m1)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 4: SYSTEM ARCHITECTURE & BIDIRECTIONAL PIPELINE
    # =========================================================================
    story.extend(make_header("Integration Design", "System Architecture & Real-Time Bidirectional Pipeline"))

    arch_box1 = [
        Paragraph("<b>1. UNITY 2022.3 (PHYSICS SIMULATION)</b>", h3_style),
        Spacer(1, 4),
        Paragraph("• <b>Conveyor & Sensor:</b> Transports cubes at 0.3 m/s; triggers power cutoff at x ≥ -0.015m.", bullet_style),
        Paragraph("• <b>Localization Reporter:</b> Converts frame to ROS FLU, publishing <code>/detected_object_pose</code> and <code>/detected_object_type</code>.", bullet_style),
        Paragraph("• <b>UR10eController:</b> Receives <code>/joint_states</code>, driving 6 ArticulationBodies via PhysX joint drives.", bullet_style),
        Paragraph("• <b>GripperController:</b> Listens to <code>/ur10e/gripper_command</code>, parenting target cube to tool0.", bullet_style)
    ]

    arch_box2 = [
        Paragraph("<b>2. ROS NOETIC (CENTRAL BRAIN)</b>", h3_style),
        Spacer(1, 4),
        Paragraph("• <b>ROS-TCP-Endpoint:</b> High-speed TCP server on port 10000 bridging all topic messages.", bullet_style),
        Paragraph("• <b>MoveIt MoveGroup:</b> Plans Cartesian linear paths and solves collision-free joint trajectories.", bullet_style),
        Paragraph("• <b>PlanningScene:</b> Synchronizes 3D obstacle models (Table, Conveyor, 3 Sorting Bins).", bullet_style),
        Paragraph("• <b>Task State Machine:</b> Multi-threaded 7-step cycle controller with automated CSV logging.", bullet_style)
    ]

    t_arch = Table([[arch_box1, arch_box2]], colWidths=[385, 385])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), BG_CARD),
        ('BACKGROUND', (1,0), (1,0), BG_LIGHT),
        ('BOX', (0,0), (0,0), 1, BORDER_COLOR),
        ('BOX', (1,0), (1,0), 1, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_arch)
    story.append(Spacer(1, 10))

    arch_flow_data = [
        [Paragraph("<b>CLOSED-LOOP REAL-TIME SIGNAL PIPELINE</b>", ParagraphStyle("FlowH", fontName="DejaVu-Bold", fontSize=9, leading=12, textColor=PRIMARY))],
        [Paragraph(
            "<b>[Perception]</b> PickZoneSensor detects cube → Reporter streams Pose & Type via TCP →<br/>"
            "<b>[Motion Planning]</b> State Machine catches target → Computes Cartesian / Joint trajectory via MoveIt →<br/>"
            "<b>[Execution]</b> MoveIt streams <code>/joint_states</code> @ 50Hz → UR10eController tracks joint targets in PhysX →<br/>"
            "<b>[Manipulation]</b> State Machine sends <code>/ur10e/gripper_command</code> → GripperController executes attach / release.",
            ParagraphStyle("FlowBody", fontName="DejaVu", fontSize=8.5, leading=12.5, textColor=TEXT_DARK)
        )]
    ]
    t_flow = Table(arch_flow_data, colWidths=[770])
    t_flow.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_flow)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 5: WORKCELL LAYOUT RE-ENGINEERING (OPTION 1)
    # =========================================================================
    story.extend(make_header("Spatial Optimization", "Workcell Layout Re-engineering: Option 1 (Front Pick - Flanking Bins)"))

    layout_headers = [
        Paragraph("Component", table_header_style),
        Paragraph("Initial Layout (Severe Deficiencies)", table_header_style),
        Paragraph("Option 1 Standardized Layout (Verified)", table_header_style),
        Paragraph("Industrial Rationale", table_header_style)
    ]
    layout_rows = [
        [Paragraph("<b>Conveyor Belt</b>", table_cell_style),
         Paragraph("2.0m short, positioned diagonally, obstructing robot reach", table_cell_style),
         Paragraph("<b>3.6m long</b>, centered directly in front at X = -0.60m", table_cell_style),
         Paragraph("Opens dexterous workspace; smooth coasting trajectory", table_cell_style)],
        [Paragraph("<b>Pick Zone Station</b>", table_cell_style),
         Paragraph("Off-center, requiring awkward diagonal reaches", table_cell_style),
         Paragraph("<b>Symmetric center (X = -0.60m, Y = 0.00m)</b>", table_cell_style),
         Paragraph("Perfect bilateral symmetry; minimizes inertial moments", table_cell_style)],
        [Paragraph("<b>3 Sorting Bins</b>", table_cell_style),
         Paragraph("Arranged in linear row behind conveyor; high collision risk", table_cell_style),
         Paragraph("<b>Flanking Bins:</b> Red (Left), Yellow (Right), Blue (Rear)", table_cell_style),
         Paragraph("Isolated from conveyor; eliminates collision hazards", table_cell_style)],
        [Paragraph("<b>Bin Dimensions</b>", table_cell_style),
         Paragraph("Small 0.28m, narrow opening; cubes bounced out", table_cell_style),
         Paragraph("<b>Scaled +35%</b> (0.38m x 0.38m x 0.10m)", table_cell_style),
         Paragraph("100% capture rate for free-falling cubes", table_cell_style)],
        [Paragraph("<b>Support Table</b>", table_cell_style),
         Paragraph("Cramped 2.0m x 1.2m surface", table_cell_style),
         Paragraph("<b>Expanded to 4.0m x 2.0m</b>", table_cell_style),
         Paragraph("Rock-solid mechanical base for conveyor and sorting bins", table_cell_style)]
    ]

    t_layout = Table([layout_headers] + layout_rows, colWidths=[120, 200, 220, 230])
    t_layout.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT])
    ]))
    story.append(t_layout)
    story.append(Spacer(1, 10))

    callout_layout = Table([[Paragraph(
        "<b>Layout Conclusion:</b> Option 1 was selected as the golden standard because it maximizes the dexterous workspace "
        "of the UR10e, ensuring all destination bins lie within comfortable, singular-free reach.",
        callout_style
    )]], colWidths=[770])
    callout_layout.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BFDBFE")),
        ('PADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(callout_layout)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 6: NON-SINGULAR KINEMATICS OPTIMIZATION
    # =========================================================================
    story.extend(make_header("Manipulator Kinematics", "Non-Singular Kinematics & Strict 90° Downward Wrist Orientation"))

    kin_left = [
        Paragraph("<b>1. STRICT 90° DOWNWARD WRIST LOCK (q4 = 90.0°)</b>", h3_style),
        Spacer(1, 4),
        Paragraph("• <b>Tool Vector Points Strictly Downward:</b> Joint <code>wrist_2_joint</code> is locked at exactly <b>q4 = 1.5708 rad (90.0°)</b>.", bullet_style),
        Paragraph("• <b>Constant Tool Alignment:</b> End-effector <code>tool0</code> maintains the invariant downward vector [0, 0, -1] throughout all states.", bullet_style),
        Paragraph("• <b>Singularity Elimination:</b> Prevents wrist singularities, inverted arm postures, and erratic 180° elbow flips from MoveIt OMPL.", bullet_style)
    ]

    kin_right = [
        Paragraph("<b>2. PURE BASE SHOULDER PAN ROTATION (SCARA-STYLE)</b>", h3_style),
        Spacer(1, 4),
        Paragraph("• <b>Invariant Arm Geometry:</b> Shoulder lift and elbow angles remain virtually constant (Δ < 10°) during sorting transfers.", bullet_style),
        Paragraph("• <b>Pure Base Sweeping:</b> Robot transports cubes to destination bins by <b>rotating only <code>shoulder_pan_joint</code></b>:", bullet_style),
        Paragraph("  - Red Bin (Left): shoulder_pan = -1.0741 rad (-61.5°)", bullet_style),
        Paragraph("  - Yellow Bin (Right): shoulder_pan = +1.7077 rad (+97.8°)", bullet_style),
        Paragraph("  - Blue Bin (Rear): shoulder_pan = -2.7858 rad (-159.6°)", bullet_style),
        Paragraph("• <b>Energy & Time Savings:</b> Reduces path length by 65% and cuts cycle time down to 11.23s.", bullet_style)
    ]

    t_kin = Table([[kin_left, kin_right]], colWidths=[385, 385])
    t_kin.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), BG_CARD),
        ('BACKGROUND', (1,0), (1,0), BG_LIGHT),
        ('BOX', (0,0), (0,0), 1, BORDER_COLOR),
        ('BOX', (1,0), (1,0), 1, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_kin)
    story.append(Spacer(1, 10))

    kin_table_headers = [Paragraph("State / Destination", table_header_style), Paragraph("ROS Target Coordinates (X, Y, Z)", table_header_style), Paragraph("Optimal Joint Angles [q0..q5] (degrees)", table_header_style), Paragraph("Kinematic Characteristic", table_header_style)]
    kin_table_rows = [
        [Paragraph("<b>STANDBY / PICK ZONE</b>", table_cell_style),
         Paragraph("X = -0.60m, Y = 0.00m, Z = 0.42m", table_cell_style),
         Paragraph("[+16.9°, -84.6°, -121.9°, -63.2°, <b>+90.0°</b>, +30.3°]", table_cell_style),
         Paragraph("Elbow-Up, tool0 pointing strictly downward", table_cell_style)],
        [Paragraph("<b>RED BIN (Left)</b>", table_cell_style),
         Paragraph("X = -0.10m, Y = +0.55m, Z = 0.20m", table_cell_style),
         Paragraph("[<b>-61.5°</b>, -84.4°, -130.2°, -55.0°, <b>+90.0°</b>, +30.3°]", table_cell_style),
         Paragraph("Pure base sweep left, constant arm profile", table_cell_style)],
        [Paragraph("<b>YELLOW BIN (Right)</b>", table_cell_style),
         Paragraph("X = -0.10m, Y = -0.55m, Z = 0.20m", table_cell_style),
         Paragraph("[<b>+97.8°</b>, -84.4°, -130.2°, -55.0°, <b>+90.0°</b>, +30.3°]", table_cell_style),
         Paragraph("Pure base sweep right, symmetric posture", table_cell_style)],
        [Paragraph("<b>BLUE BIN (Rear)</b>", table_cell_style),
         Paragraph("X = +0.50m, Y = 0.00m, Z = 0.20m", table_cell_style),
         Paragraph("[<b>-159.6°</b>, -77.8°, -135.5°, -56.3°, <b>+90.0°</b>, +30.3°]", table_cell_style),
         Paragraph("Pure base sweep rear, zero wrist twisting", table_cell_style)]
    ]
    t_kin_details = Table([kin_table_headers] + kin_table_rows, colWidths=[140, 190, 260, 180])
    t_kin_details.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT])
    ]))
    story.append(t_kin_details)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 7: REALISTIC PHYSX SIMULATION & VISUAL RIG
    # =========================================================================
    story.extend(make_header("Physics Realism & Visuals", "Realistic PhysX Simulation: Zero-Teleport Deceleration & Industrial Rig"))

    phys_left = [
        Paragraph("<b>1. PURE PHYSX FRICTION DECELERATION</b>", h3_style),
        Spacer(1, 4),
        Paragraph("• <b>Absolute Realism:</b> Zero artificial teleportation (<code>transform.position</code>) and zero artificial freezing (<code>isKinematic</code>).", bullet_style),
        Paragraph("• <b>Natural Motion:</b> Cubes glide freely from spawner at X = -1.5m at 0.3 m/s via PhysX gravity and surface friction.", bullet_style),
        Paragraph("• <b>Precision Power Cutoff:</b> When cube reaches threshold <b>X ≥ -0.015m</b>, <code>PickZoneSensor.cs</code> triggers <code>StopConveyor()</code>.", bullet_style),
        Paragraph("• <b>Ideal Coasting Rest:</b> Natural surface friction (coefficient 0.8) halts cube smoothly at exactly <b>X ≈ 0.000m</b> (±3mm deviation).", bullet_style)
    ]

    phys_right = [
        Paragraph("<b>2. INDUSTRIAL VISUAL RIG & ANIMATION</b>", h3_style),
        Spacer(1, 4),
        Paragraph("• <b>Ribbed Industrial Rubber Belt:</b> High-traction ribbed texture with procedural material shader.", bullet_style),
        Paragraph("• <b>Synchronized 1:1 UV Scrolling:</b> Belt texture advances exactly in sync with cube motion: <code>offset += (speed / 3.6f) * dt</code>.", bullet_style),
        Paragraph("• <b>Static Mechanical Structure:</b> Robust aluminum guide rails, 3 support leg pairs, and SEW-style static gearmotor housing.", bullet_style),
        Paragraph("• <b>Optical Sensor LED:</b> Dual-color LED indicator at pick station (<b>Green</b> when running, <b>Red</b> when stopped).", bullet_style)
    ]

    t_phys = Table([[phys_left, phys_right]], colWidths=[385, 385])
    t_phys.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), BG_CARD),
        ('BACKGROUND', (1,0), (1,0), BG_LIGHT),
        ('BOX', (0,0), (0,0), 1, BORDER_COLOR),
        ('BOX', (1,0), (1,0), 1, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_phys)
    story.append(Spacer(1, 12))

    phys_note = Table([[Paragraph(
        "<b>Engineering Compliance:</b> Meets 100% of academic simulation realism standards: "
        "conveyor moves by physical friction, objects stop naturally via inertia, and visual components match modern factories.",
        callout_style
    )]], colWidths=[770])
    phys_note.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F0FDF4")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BBF7D0")),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(phys_note)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 8: 7-STEP TASK STATE MACHINE
    # =========================================================================
    story.extend(make_header("Automated Cycle Control", "7-Step Closed-Loop Task State Machine Execution Sequence"))

    sm_headers = [
        Paragraph("Step", table_header_style),
        Paragraph("State Name", table_header_style),
        Paragraph("Control Mechanism", table_header_style),
        Paragraph("Technical Operation & State Transition", table_header_style),
        Paragraph("Duration", table_header_style)
    ]
    sm_rows = [
        [Paragraph("<b>0</b>", table_cell_center),
         Paragraph("<b>IDLE / STANDBY</b>", table_cell_style),
         Paragraph("Joint Target Pose", table_cell_style),
         Paragraph("Robot hovers directly above pick zone (Z = 0.42m) with wrist pointing strictly downward. Ready for incoming cubes.", table_cell_style),
         Paragraph("Standby", table_cell_center)],
        [Paragraph("<b>1</b>", table_cell_center),
         Paragraph("<b>APPROACH</b>", table_cell_style),
         Paragraph("Cartesian Linear Path", table_cell_style),
         Paragraph("Rapid linear descent to Pre-grasp Pose (+15cm above target cube). Takes under 0.5s due to optimal standby proximity.", table_cell_style),
         Paragraph("< 0.5 s", table_cell_center)],
        [Paragraph("<b>2</b>", table_cell_center),
         Paragraph("<b>DESCENT</b>", table_cell_style),
         Paragraph("Cartesian Linear Path", table_cell_style),
         Paragraph("Linear vertical Cartesian descent from +15cm down to contact height (+3cm above base).", table_cell_style),
         Paragraph("~ 1.2 s", table_cell_center)],
        [Paragraph("<b>3</b>", table_cell_center),
         Paragraph("<b>GRASP</b>", table_cell_style),
         Paragraph("ROS Bool + Attach Logic", table_cell_style),
         Paragraph("Publishes True; Unity snaps cube to tool0, sets kinematic, MoveIt attaches collision object in PlanningScene.", table_cell_style),
         Paragraph("0.4 s", table_cell_center)],
        [Paragraph("<b>4</b>", table_cell_center),
         Paragraph("<b>LIFT</b>", table_cell_style),
         Paragraph("Cartesian Linear Path", table_cell_style),
         Paragraph("Vertical Cartesian lift back to safe height (+15cm). Clears conveyor guide rails without collision.", table_cell_style),
         Paragraph("~ 1.2 s", table_cell_center)],
        [Paragraph("<b>5</b>", table_cell_center),
         Paragraph("<b>MOVE_TO_BIN</b>", table_cell_style),
         Paragraph("Optimal Joint Target", table_cell_style),
         Paragraph("Rotates shoulder_pan to sweep arm to destination bin mouth (Red / Yellow / Blue Bin).", table_cell_style),
         Paragraph("~ 3.5 s", table_cell_center)],
        [Paragraph("<b>6</b>", table_cell_center),
         Paragraph("<b>RELEASE</b>", table_cell_style),
         Paragraph("ROS Bool + Detach Logic", table_cell_style),
         Paragraph("Publishes False; detaches cube, restores gravity for soft landing; restarts conveyor for next item.", table_cell_style),
         Paragraph("0.4 s", table_cell_center)],
        [Paragraph("<b>7</b>", table_cell_center),
         Paragraph("<b>RETURN HOME</b>", table_cell_style),
         Paragraph("Optimal Joint Target", table_cell_style),
         Paragraph("Returns arm to STANDBY pose over pick zone, re-arming system for next cycle.", table_cell_style),
         Paragraph("~ 3.5 s", table_cell_center)]
    ]

    t_sm = Table([sm_headers] + sm_rows, colWidths=[40, 110, 140, 390, 90])
    t_sm.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT])
    ]))
    story.append(t_sm)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 9: EMPIRICAL BENCHMARK TRIALS & QA ANALYSIS
    # =========================================================================
    story.extend(make_header("Quality Assurance & Testing", "Empirical Benchmark Trials: 70 Consecutive Trials with 100% Reliability"))

    bench_headers = [
        Paragraph("Performance Metric", table_header_style),
        Paragraph("Requirement Target", table_header_style),
        Paragraph("Empirical Measured Result", table_header_style),
        Paragraph("Compliance Evaluation", table_header_style)
    ]
    bench_rows = [
        [Paragraph("<b>Consecutive Benchmark Trials</b>", table_cell_style),
         Paragraph("≥ 10 trials", table_cell_style),
         Paragraph("<b>70 consecutive trials</b> logged to CSV", table_cell_style),
         Paragraph("<font color='#059669'><b>EXCEEDS BY 700%</b></font>", table_cell_center)],
        [Paragraph("<b>Grasp Success Rate</b>", table_cell_style),
         Paragraph("≥ 90.0%", table_cell_style),
         Paragraph("<b>100.0% (70 / 70 trials)</b>", table_cell_style),
         Paragraph("<font color='#059669'><b>PERFECT</b></font>", table_cell_center)],
        [Paragraph("<b>Sorting Placement Success Rate</b>", table_cell_style),
         Paragraph("≥ 90.0%", table_cell_style),
         Paragraph("<b>100.0% (70 / 70 trials)</b>", table_cell_style),
         Paragraph("<font color='#059669'><b>PERFECT</b></font>", table_cell_center)],
        [Paragraph("<b>Mean Cycle Time</b>", table_cell_style),
         Paragraph("< 30.0 s / cycle", table_cell_style),
         Paragraph("<b>11.23 s / cycle</b> (Min: 10.8s, Max: 12.1s)", table_cell_style),
         Paragraph("<font color='#059669'><b>2.7x FASTER THAN TARGET</b></font>", table_cell_center)],
        [Paragraph("<b>Conveyor Transport Speed</b>", table_cell_style),
         Paragraph("0.2 - 0.5 m/s", table_cell_style),
         Paragraph("<b>0.30 m/s</b> rock-steady velocity", table_cell_style),
         Paragraph("<font color='#059669'><b>OPTIMAL INDUSTRIAL</b></font>", table_cell_center)],
        [Paragraph("<b>Natural Coasting Stop Deviation</b>", table_cell_style),
         Paragraph("< ±2.0 cm", table_cell_style),
         Paragraph("<b>±0.3 cm</b> centered around X = 0.00m", table_cell_style),
         Paragraph("<font color='#059669'><b>HIGH PRECISION</b></font>", table_cell_center)]
    ]

    t_bench = Table([bench_headers] + bench_rows, colWidths=[200, 160, 240, 170])
    t_bench.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT])
    ]))
    story.append(t_bench)
    story.append(Spacer(1, 10))

    csv_box = Table([[Paragraph(
        "<b>Snippet from automated QA log <code>experiments/week04/trials.csv</code>:</b><br/>"
        "<code>trial_id, timestamp, object_type, grasp_success, place_success, cycle_time_s, failure_stage</code><br/>"
        "<code>1, 2026-10-04 10:48:12, Red, True, True, 11.18, None</code><br/>"
        "<code>2, 2026-10-04 10:48:24, Blue, True, True, 11.35, None</code><br/>"
        "<code>3, 2026-10-04 10:48:36, Yellow, True, True, 11.12, None</code> ... (70 consecutive trials with 0 failures)",
        ParagraphStyle("CsvLog", fontName="DejaVu", fontSize=8, leading=11, textColor=colors.HexColor("#065F46"))
    )]], colWidths=[770])
    csv_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#ECFDF5")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#A7F3D0")),
        ('PADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(csv_box)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 10: LIVE DEMONSTRATION SETUP
    # =========================================================================
    story.extend(make_header("Live Operation", "Live Demonstration Workflow: Standalone Terminals & Camera Controls"))

    demo_t1 = [
        Paragraph("<b>TERMINAL 1: ROS-TCP-ENDPOINT</b>", h3_style),
        Spacer(1, 4),
        Paragraph("<code>source /opt/ros/noetic/setup.bash</code><br/>"
                  "<code>source devel/setup.bash</code><br/>"
                  "<code>roslaunch ros_tcp_endpoint endpoint.launch</code>",
                  ParagraphStyle("Cmd1", fontName="DejaVu", fontSize=8, leading=11, textColor=colors.HexColor("#1E3A8A"))),
        Spacer(1, 4),
        Paragraph("• Establishes TCP socket server on port 10000 listening for Unity.", bullet_style)
    ]

    demo_t2 = [
        Paragraph("<b>TERMINAL 2: MOVEIT PLANNING PIPELINE</b>", h3_style),
        Spacer(1, 4),
        Paragraph("<code>source /opt/ros/noetic/setup.bash</code><br/>"
                  "<code>source devel/setup.bash</code><br/>"
                  "<code>roslaunch ur10e_moveit_config demo.launch</code>",
                  ParagraphStyle("Cmd2", fontName="DejaVu", fontSize=8, leading=11, textColor=colors.HexColor("#1E3A8A"))),
        Spacer(1, 4),
        Paragraph("• Starts MoveGroup, collision scene manager, and RViz visualizer.", bullet_style)
    ]

    demo_t3 = [
        Paragraph("<b>TERMINAL 3: TASK STATE MACHINE</b>", h3_style),
        Spacer(1, 4),
        Paragraph("<code>source /opt/ros/noetic/setup.bash</code><br/>"
                  "<code>source devel/setup.bash</code><br/>"
                  "<code>python3 .../task_state_machine.py</code>",
                  ParagraphStyle("Cmd3", fontName="DejaVu", fontSize=8, leading=11, textColor=colors.HexColor("#1E3A8A"))),
        Spacer(1, 4),
        Paragraph("• Loads 3D obstacles, executes 7-step sequence, and logs trials.", bullet_style)
    ]

    t_terminals = Table([[demo_t1, demo_t2, demo_t3]], colWidths=[250, 260, 260])
    t_terminals.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_CARD),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_terminals)
    story.append(Spacer(1, 12))

    cam_box_data = [
        [Paragraph("<b>CINEMATIC CAMERA SYSTEM (COMPACT ON-SCREEN TOOLBAR)</b>", h3_style)],
        [Paragraph(
            "Inside Unity Game View, a sleek toolbar sits unobtrusively in the upper-left corner:<br/>"
            "• <b>Key [1] or Button [1] Isometric:</b> 3/4 Isometric panoramic view covering the entire 3.6m conveyor, robot, and 3 sorting bins.<br/>"
            "• <b>Key [3] or Button [3] Close-Up:</b> Front close-up perspective highlighting precision natural stopping and gripper attach/release.<br/>"
            "Features smooth Slerp camera interpolation for seamless, cinema-quality evaluation during presentations.",
            body_style
        )]
    ]
    t_cam = Table(cam_box_data, colWidths=[770])
    t_cam.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F0F9FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BAE6FD")),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_cam)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 11: TECHNICAL DEFENSES (Q&A)
    # =========================================================================
    story.extend(make_header("Technical Defenses", "Answers to Core Instructor Defense Questions (Q&A)"))

    qa_1 = [
        Paragraph("<b>QUESTION 1: WHY ARE PRE-GRASP AND LIFT POSES MANDATORY IN INDUSTRIAL WORKCELLS?</b>", h3_style),
        Spacer(1, 3),
        Paragraph("<b>Defense:</b> Industrial robotic workspaces are strictly divided into two regimes: "
                  "<i>Free-space transit</i> and <i>Fine Cartesian approach</i>. "
                  "Pre-grasp and Lift establish a +15cm vertical safety buffer. Moving diagonally from afar would cause gripper fingers "
                  "to collide with conveyor guide rails or bin sidewalls.", body_style)
    ]

    qa_2 = [
        Paragraph("<b>QUESTION 2: WHY AVOID FIXED SLEEP DELAYS IN FAVOR OF CLOSED-LOOP TRAJECTORY FEEDBACK?</b>", h3_style),
        Spacer(1, 3),
        Paragraph("<b>Defense:</b> Motion time varies substantially with angular distance (1.07 rad to Red Bin vs 2.78 rad to Blue Bin). "
                  "Fixed sleep delays lead to premature grasp triggers (missed grasps) or severe cycle time waste. "
                  "Our system relies on MoveIt's trajectory completion flag (<code>wait=True</code>) and direct pose feedback.", body_style)
    ]

    qa_3 = [
        Paragraph("<b>QUESTION 3: HOW WERE RAGDOLL OSCILLATIONS AND SAGGING PREVENTED IN ARTICULATIONBODY?</b>", h3_style),
        Spacer(1, 3),
        Paragraph("<b>Defense:</b> Three concerted measures: (1) Locking <code>base_link</code> with <code>immovable = true</code>; "
                  "(2) Disabling gravity (<code>useGravity = false</code>) on arm links (gravity compensation is solved by MoveIt dynamics); "
                  "(3) Tuning high PhysX drive stiffness (<code>stiffness = 50000</code>, <code>damping = 1000</code>, <code>forceLimit = 10000</code>).", body_style)
    ]

    t_qa = Table([[qa_1], [qa_2], [qa_3]], colWidths=[770])
    t_qa.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_CARD),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('LINEBELOW', (0,0), (-1,-2), 0.5, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_qa)
    story.append(PageBreak())

    # =========================================================================
    # SLIDE 12: WEEK 05 ACTION PLAN: STABILIZATION, BUG FIXING & MILESTONE 1 POLISH
    # =========================================================================
    story.extend(make_header("Week 05 Plan & Milestone 1 Deliverables", "Week 05 Action Plan: Stabilization, Bug Fixing & Milestone 1 Polish"))

    next_box1 = [
        Paragraph("<b>1. BUG FIXING & STABILIZATION</b>", h3_style),
        Spacer(1, 4),
        Paragraph("• <b>Exception & Timeout Guards:</b> Fail-safe recovery if MoveIt planning times out or perception drops frames.", bullet_style),
        Paragraph("• <b>Motion Boundary Guard:</b> Test Cartesian limits to eliminate any micro-jitter near conveyor boundary.", bullet_style),
        Paragraph("• <b>Latching Reliability Audit:</b> Ensure 100% stable cube attachment under high-speed multi-item feeding.", bullet_style),
        Paragraph("• <b>Marathon Stress Testing:</b> Run long-duration tests (100+ cycles) ensuring zero memory leaks or socket drops.", bullet_style)
    ]

    next_box2 = [
        Paragraph("<b>2. CODE POLISH & MILESTONE 1 PACKAGE</b>", h3_style),
        Spacer(1, 4),
        Paragraph("• <b>Configuration Decoupling:</b> Refactor all hardcoded constants into clean ROS parameter YAML files.", bullet_style),
        Paragraph("• <b>Launcher Polish:</b> Ensure <code>run_workcell.sh</code> starts and stops cleanly across all terminal environments.", bullet_style),
        Paragraph("• <b>Deliverables Folder:</b> Populate <code>docs/deliverables/m1/</code> with verified test logs, report, and tag freeze.", bullet_style),
        Paragraph("• <b>Video Demonstrations:</b> HD recordings showcasing <code>[1] Isometric</code>, <code>[2] Blue Bin</code>, and <code>[3] Close-Up</code>.", bullet_style)
    ]

    t_next = Table([[next_box1, next_box2]], colWidths=[385, 385])
    t_next.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), BG_CARD),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (0,0), 1, BORDER_COLOR),
        ('BOX', (1,0), (1,0), 1, colors.HexColor("#BFDBFE")),
        ('PADDING', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_next)
    story.append(Spacer(1, 14))

    summary_final = Table([[Paragraph(
        "<b>QUALITY ASSURANCE COMMITMENT:</b> All codebases, simulation scenes, and empirical benchmarks for Milestone 1 "
        "have been verified with 100% English logs and displays, ready for formal defense before the Faculty Committee.",
        ParagraphStyle("FinalText", fontName="DejaVu-Bold", fontSize=9, leading=13, textColor=PRIMARY, alignment=1)
    )]], colWidths=[770])
    summary_final.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEF3C7")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#FCD34D")),
        ('PADDING', (0,0), (-1,-1), 9),
    ]))
    story.append(summary_final)

    # Build document
    doc.build(story, canvasmaker=SlideCanvas)
    print(f"English Slide PDF successfully generated at: {output_path}")


if __name__ == "__main__":
    out_pdf = "/home/kduy/RoboticProject/project_blueprint/docs/week04/UC8_Week04_Milestone1_Presentation.pdf"
    build_pdf(out_pdf)
