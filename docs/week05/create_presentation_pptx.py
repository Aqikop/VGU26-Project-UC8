#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generate Professional Widescreen 16:9 PowerPoint Presentation (.pptx)
Milestone 1 Defense & Verification — Autonomous Closed-Loop Sorting Workcell & Future Roadmap.
100% Data Filled In — Zero Image Placeholders.
Project: UC8 - Robotic Arm Conveyor Pick-and-Place with Obstacle Avoidance
Course: Robotic Project — Vietnamese-German University (VGU)
"""

import sys
import os

pylib_dir = "/home/kduy/RoboticProject/project_blueprint/docs/week04/pylib"
if os.path.exists(pylib_dir):
    sys.path.insert(0, pylib_dir)

import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

# Color Palette
COLOR_DARK_BG = RGBColor(15, 23, 42)       # Slate 900 #0F172A
COLOR_LIGHT_BG = RGBColor(248, 250, 252)   # Slate 50  #F8FAFC
COLOR_CARD_BG = RGBColor(255, 255, 255)    # White
COLOR_BORDER = RGBColor(226, 232, 240)     # Slate 200 #E2E8F0
COLOR_PRIMARY = RGBColor(15, 43, 72)       # Deep Navy #0F2B48
COLOR_ACCENT = RGBColor(2, 132, 199)       # Sky Blue  #0284C7
COLOR_SUCCESS = RGBColor(5, 150, 105)      # Green 600 #059669
COLOR_WARNING = RGBColor(217, 119, 6)      # Amber 600 #D97706
COLOR_TEXT_MAIN = RGBColor(30, 41, 59)     # Slate 800 #1E293B
COLOR_TEXT_MUTED = RGBColor(100, 116, 139) # Slate 500 #64748B
COLOR_TEXT_LIGHT = RGBColor(241, 245, 249) # Slate 100 #F1F5F9
COLOR_TABLE_HEADER = RGBColor(15, 43, 72)  # #0F2B48
COLOR_TABLE_ALT = RGBColor(241, 245, 249)  # #F1F5F9


def set_shape_flat(shape, fill_color, border_color=None, border_width=1):
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(border_width)
    else:
        shape.line.fill.background()


def add_header(slide, category, title, slide_label=None):
    # Category tag
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(10), Inches(0.3))
    tf_c = cat_box.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = tf_c.margin_bottom = 0
    p_c = tf_c.paragraphs[0]
    p_c.text = category.upper()
    p_c.font.size = Pt(10)
    p_c.font.bold = True
    p_c.font.color.rgb = COLOR_ACCENT

    # Title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.68), Inches(11.5), Inches(0.6))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    p_t.text = title
    p_t.font.size = Pt(20)
    p_t.font.bold = True
    p_t.font.color.rgb = COLOR_PRIMARY

    # Header horizontal line
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.32), Inches(11.733), Inches(0.02))
    set_shape_flat(line, COLOR_BORDER)

    # Footer
    footer_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.9), Inches(11.733), Inches(0.015))
    set_shape_flat(footer_line, COLOR_BORDER)

    ft_box = slide.shapes.add_textbox(Inches(0.8), Inches(6.95), Inches(8.0), Inches(0.35))
    tf_f = ft_box.text_frame
    tf_f.margin_left = tf_f.margin_right = tf_f.margin_top = tf_f.margin_bottom = 0
    p_f = tf_f.paragraphs[0]
    p_f.text = "UC8 Robotic Sorting Workcell | Milestone 1 Defense | Vietnamese-German University"
    p_f.font.size = Pt(9)
    p_f.font.color.rgb = COLOR_TEXT_MUTED

    if slide_label:
        pg_box = slide.shapes.add_textbox(Inches(10.533), Inches(6.95), Inches(2.0), Inches(0.35))
        tf_p = pg_box.text_frame
        tf_p.margin_left = tf_p.margin_right = tf_p.margin_top = tf_p.margin_bottom = 0
        p_p = tf_p.paragraphs[0]
        p_p.text = slide_label
        p_p.font.size = Pt(9)
        p_p.font.bold = True
        p_p.font.color.rgb = COLOR_ACCENT
        p_p.alignment = PP_ALIGN.RIGHT


def add_card(slide, left, top, width, height, fill_color=COLOR_CARD_BG, border_color=COLOR_BORDER):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    set_shape_flat(shape, fill_color, border_color)
    shape.adjustments[0] = 0.03
    return shape


def add_table(slide, left, top, width, height, headers, data, col_widths=None):
    rows = len(data) + 1
    cols = len(headers)
    table_shape = slide.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table

    if col_widths and len(col_widths) == cols:
        for idx, w in enumerate(col_widths):
            table.columns[idx].width = w

    for idx, header in enumerate(headers):
        cell = table.cell(0, idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_TABLE_HEADER
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]
        p.text = header
        p.font.bold = True
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_TEXT_LIGHT

    for row_idx, row_data in enumerate(data):
        is_even = (row_idx % 2 == 0)
        bg = COLOR_CARD_BG if is_even else COLOR_TABLE_ALT
        for col_idx, cell_value in enumerate(row_data):
            cell = table.cell(row_idx + 1, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            p.text = str(cell_value)
            p.font.size = Pt(9.5)
            p.font.color.rgb = COLOR_TEXT_MAIN
            if col_idx == 0:
                p.font.bold = True


def main():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 01: TITLE COVER SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    set_shape_flat(bg1, COLOR_DARK_BG)

    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(0.9), Inches(1.2), Inches(0.08))
    set_shape_flat(bar, COLOR_ACCENT)

    tbox = s1.shapes.add_textbox(Inches(1.0), Inches(1.15), Inches(11.333), Inches(2.2))
    tf = tbox.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "UC8: ROBOTIC ARM CONVEYOR PICK-AND-PLACE"
    p1.font.size = Pt(28)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_TEXT_LIGHT

    p2 = tf.add_paragraph()
    p2.text = "WITH OBSTACLE AVOIDANCE"
    p2.font.size = Pt(28)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_ACCENT

    p3 = tf.add_paragraph()
    p3.text = "Milestone 1 Defense & Performance Verification (UR10e Workcell)"
    p3.font.size = Pt(16)
    p3.font.color.rgb = RGBColor(148, 163, 184)

    # Left Card: Meta Information
    add_card(s1, Inches(1.0), Inches(3.6), Inches(5.5), Inches(3.2), fill_color=RGBColor(30, 41, 59), border_color=RGBColor(51, 65, 85))
    mtf = s1.shapes.add_textbox(Inches(1.25), Inches(3.8), Inches(5.0), Inches(2.8)).text_frame
    mtf.word_wrap = True
    p = mtf.paragraphs[0]
    p.text = "PROJECT METADATA"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT
    p.space_after = Pt(8)

    meta_items = [
        ("Course:", "Robotic Project — Vietnamese-German University"),
        ("System:", "UR10e, 3.6m Conveyor, 2-Finger Claw, MoveIt & Unity"),
        ("Evaluation:", "Milestone 1 Official Defense (Requirements R1 - R4)"),
        ("Next Phase:", "Week 06 Sprint & Milestone 2 (Static Obstacle Avoidance)"),
        ("Status:", "100% Verified Closed-Loop Sequencer (70/70 Trials OK)")
    ]
    for lbl, val in meta_items:
        p = mtf.add_paragraph()
        r1 = p.add_run()
        r1.text = f"• {lbl:<15} "
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = COLOR_TEXT_LIGHT
        r2 = p.add_run()
        r2.text = val
        r2.font.size = Pt(10)
        r2.font.color.rgb = RGBColor(203, 213, 225)
        p.space_after = Pt(4)

    # Right Card: Verified Highlights
    add_card(s1, Inches(6.8), Inches(3.6), Inches(5.5), Inches(3.2), fill_color=RGBColor(30, 41, 59), border_color=RGBColor(51, 65, 85))
    atf = s1.shapes.add_textbox(Inches(7.05), Inches(3.8), Inches(5.0), Inches(2.8)).text_frame
    atf.word_wrap = True
    p = atf.paragraphs[0]
    p.text = "MILESTONE 1 VERIFIED HIGHLIGHTS"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = COLOR_SUCCESS
    p.space_after = Pt(8)

    arch_items = [
        ("UR10e Motion Streaming:", "50 Hz /joint_states driving 6 ArticulationBodies"),
        ("Procedural 2-Finger Claw:", "Flange mount, status LED, aluminum arms, rubber pads"),
        ("Autonomous Sequencer:", "7-step closed-loop state machine (zero human input)"),
        ("Zero-Teleport Physics:", "Pure friction coasting stop halting cubes with ±3mm precision"),
        ("Quality Assurance:", "70 consecutive trials logged with 100% success rate")
    ]
    for lbl, val in arch_items:
        p = atf.add_paragraph()
        r1 = p.add_run()
        r1.text = f"✔ {lbl} "
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = COLOR_SUCCESS
        r2 = p.add_run()
        r2.text = val
        r2.font.size = Pt(10)
        r2.font.color.rgb = RGBColor(203, 213, 225)
        p.space_after = Pt(4)

    # =========================================================================
    # SLIDE 02: OVERVIEW / AGENDA
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Presentation Structure", "Agenda of Milestone 1 Defense & Roadmap", "Slide 02")

    agenda_headers = ["No.", "Topic", "Core Content & Engineering Focus"]
    agenda_data = [
        ["01-02", "Project Title & Agenda", "Context, requirements, and presentation structure"],
        ["03-04", "Baseline Recap & Scope Fulfillment", "100% completion of Week 03 commitments (R1-R4)"],
        ["05", "System Architecture", "Bidirectional closed loop: Unity 2022.3 <-> ROS-TCP <-> ROS Noetic"],
        ["06", "Instructor Feedback & Resolutions", "Industrial 2-finger claw, anti-miss scanner, orthogonal zero-sink grasp"],
        ["07-08", "Workcell Layout & Kinematics", "Option 1 bilateral symmetry, 90° wrist lock, pure base SCARA sweep"],
        ["09-10", "PhysX Simulation & State Machine", "Friction deceleration, multi-item flow, 7-step sequencer"],
        ["11-12", "Benchmark QA & Technical Defenses", "70 empirical trials, 100% success rate, answers to faculty committee"],
        ["13-14", "Week 06 Objectives & Milestone 2 Roadmap", "R5 conveyor robustness, vision classification, static obstacle avoidance"],
        ["15", "Summary & M1 Acceptance Conclusion", "Milestone 1 criteria sign-off and transition to Milestone 2 development"]
    ]
    add_table(s2, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.0), agenda_headers, agenda_data,
              [Inches(1.2), Inches(3.6), Inches(6.933)])

    # =========================================================================
    # SLIDE 03: BASELINE ACHIEVED IN WEEK 03 & COMMITMENTS
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Baseline vs Commitments", "Week 03 Baseline and Commitments Set Out for Milestone 1", "Slide 03")

    add_card(s3, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.0), fill_color=COLOR_CARD_BG)
    f_tf = s3.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.3), Inches(4.6)).text_frame
    f_tf.word_wrap = True
    p = f_tf.paragraphs[0]
    p.text = "Baseline Achieved in Week 03"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(10)

    f_items = [
        ("ROS-Unity bridge:", "TCP communication available on port 10000 via ros_tcp_endpoint."),
        ("Coordinate conversion:", "Unity coordinates mapped to ROS FLU: X_ROS = Z_Unity, Y_ROS = -X_Unity, Z_ROS = Y_Unity."),
        ("Object topics:", "/detected_object_pose (Pose) and /detected_object_type (String) published at 10 Hz."),
        ("MoveIt planning:", "Pre-grasp feasibility verified in RViz (+15cm hover pose above detected cube base).")
    ]
    for lbl, desc in f_items:
        p = f_tf.add_paragraph()
        r1 = p.add_run()
        r1.text = "✔ " + lbl + " "
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = COLOR_SUCCESS
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(6)

    add_card(s3, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.0), fill_color=COLOR_CARD_BG)
    c_tf = s3.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.6)).text_frame
    c_tf.word_wrap = True
    p = c_tf.paragraphs[0]
    p.text = "Commitments Set Out for Milestone 1"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT
    p.space_after = Pt(10)

    c_items = [
        ("Trajectory execution:", "Overcome 'plan-only' barrier; stream real-time joint-states to drive physical UR10e in Unity."),
        ("Grasping mechanism:", "Implement attach/parenting logic linking target cube to tool0 upon arrival."),
        ("Task controller:", "Construct autonomous closed-loop sequencer connecting perception, motion, and release."),
        ("Multi-bin sorting:", "Route red, yellow, and blue cubes to dedicated destination bins without collision."),
        ("Milestone 1 Context:", "Fulfilling 100% of these commitments in Week 04 is the prerequisite for Milestone 1 evaluation.")
    ]
    for lbl, desc in c_items:
        p = c_tf.add_paragraph()
        r1 = p.add_run()
        r1.text = "🎯 " + lbl + " "
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = COLOR_PRIMARY
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(6)

    # =========================================================================
    # SLIDE 04: EXECUTION AND SCOPE
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Execution and Scope", "Milestone 1 Scope: 100% Commitment Fulfillment Status", "Slide 04")

    add_card(s4, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.0), fill_color=COLOR_CARD_BG)
    e_tf = s4.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.3), Inches(4.6)).text_frame
    e_tf.word_wrap = True
    p = e_tf.paragraphs[0]
    p.text = "100% Commitment Fulfillment Status"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_SUCCESS
    p.space_after = Pt(10)

    e_items = [
        ("Trajectory Execution (R2/R3):", "Streamed /joint_states at 50 Hz to 6 ArticulationBodies with zero sagging and smooth tracking (100% DONE)."),
        ("Grasping Mechanism (R4):", "Implemented industrial Attach/Parenting logic in GripperController.cs with instant latching (100% DONE)."),
        ("Closed-Loop State Machine (R4):", "Constructed 7-step autonomous sequencer (task_state_machine.py) with zero human intervention (100% DONE)."),
        ("3-Bin Sorting System (R4):", "Deployed Red (Left), Yellow (Right), and Blue (Rear) bins with dedicated non-singular trajectories (100% DONE).")
    ]
    for lbl, desc in e_items:
        p = e_tf.add_paragraph()
        r1 = p.add_run()
        r1.text = "✔ " + lbl + " "
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = COLOR_PRIMARY
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(6)

    add_card(s4, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.0), fill_color=COLOR_CARD_BG)
    p_tf = s4.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.6)).text_frame
    p_tf.word_wrap = True
    p = p_tf.paragraphs[0]
    p.text = "Milestone 1 High-Value Enhancements"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT
    p.space_after = Pt(10)

    p_items = [
        ("Kinematic Optimization:", "Locked wrist strictly downward (q4 = 90.0°) & implemented pure base SCARA sweep, cutting cycle time by 65%."),
        ("Realistic PhysX Deceleration:", "Replaced artificial freezing with pure friction coasting (StopConveyor()) halting cubes at X ≈ 0.00 m (± 3 mm)."),
        ("Continuous Multi-Item Flow:", "Upgraded Spawner to maintain 2-3 items on conveyor simultaneously with safe 38cm spacing."),
        ("Empirical QA Logging:", "Integrated automated CSV logger recording 70 consecutive trials with 100% reliability for Milestone 1 defense.")
    ]
    for lbl, desc in p_items:
        p = p_tf.add_paragraph()
        r1 = p.add_run()
        r1.text = "⚙ " + lbl + " "
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = COLOR_PRIMARY
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(6)

    # =========================================================================
    # SLIDE 05: ARCHITECTURE
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Architecture", "System Architecture: Bidirectional Communication Pipeline", "Slide 05")

    pipe_headers = ["Layer", "Key Responsibility", "Topic / Protocol", "Direction"]
    pipe_data = [
        ["Unity Perception", "Detects cube, halts conveyor, converts frame to ROS FLU", "/detected_object_pose, /detected_object_type", "Unity -> ROS (10 Hz)"],
        ["ROS-TCP-Endpoint", "Low-latency network bridge brokering serialised ROS messages", "TCP Port 10000 Socket Streaming", "Bidirectional (Real-time)"],
        ["State Machine", "Closed-loop task logic sequencing 7 execution states", "task_state_machine.py orchestrator", "Internal ROS Node"],
        ["MoveIt Core", "Plans collision-free Cartesian paths & joint trajectories", "manipulator MoveGroupCommander", "MoveIt <-> State Machine"],
        ["Robot Controller", "Maps joint positions to 6 UR10e ArticulationBodies", "/joint_states (JointTrajectoryPoint)", "ROS -> Unity (50 Hz)"],
        ["Gripper Controller", "Parenting attach logic; animates fingers and clamps cube", "/ur10e/gripper_command, /gripper_status", "ROS <-> Unity (Event-driven)"]
    ]
    add_table(s5, Inches(0.8), Inches(1.6), Inches(11.733), Inches(3.8), pipe_headers, pipe_data,
              [Inches(2.0), Inches(4.333), Inches(3.2), Inches(2.2)])

    add_card(s5, Inches(0.8), Inches(5.6), Inches(11.733), Inches(1.15), fill_color=COLOR_CARD_BG)
    btf = s5.shapes.add_textbox(Inches(1.0), Inches(5.68), Inches(11.333), Inches(0.98)).text_frame
    btf.word_wrap = True
    p = btf.paragraphs[0]
    p.text = "CORE INTERFACE SPECIFICATIONS & STANDARDS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(4)

    p_spec = btf.add_paragraph()
    p_spec.text = "• Coordinate Mapping: X_ROS = Z_Unity, Y_ROS = -X_Unity, Z_ROS = Y_Unity\n" \
                  "• Planning Group: manipulator | Planning Frame: base_link | End Effector: tool0\n" \
                  "• Streaming Topics: /detected_object_pose (Pose), /detected_object_type (String), /joint_states @ 50 Hz, /ur10e/gripper_command (Bool)"
    p_spec.font.size = Pt(9.5)
    p_spec.font.color.rgb = COLOR_TEXT_MAIN

    # =========================================================================
    # SLIDE 06: INSTRUCTOR FEEDBACK & RESOLUTIONS (NEW HIGH-VALUE SLIDE)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Instructor Feedback & Resolutions", "Addressing Faculty Feedback with Rapid Technical Solutions", "Slide 06")

    feedback_cards = [
        ("Feedback 1: 2-Finger Claw", COLOR_PRIMARY, [
            ("Requested:", "Instructor recommended adding a visible mechanical gripper claw instead of an abstract suction point."),
            ("Solution:", "Built procedural industrial 2-finger claw (VisualClaw): Flange adapter (1.2cm), navy housing chassis (2.0cm), and status LED."),
            ("Fingers:", "Aircraft aluminum arms (4.0cm) with high-friction black rubber pads, driven by kinematic carriage animation.")
        ]),
        ("Feedback 2: Missed Cubes", COLOR_WARNING, [
            ("Issue:", "During continuous multi-item flow, cubes were occasionally missed due to missed OnTriggerEnter events."),
            ("Solution:", "Replaced passive trigger collisions with continuous active scanning (FindLeadingCubeOnConveyor())."),
            ("Safety Latch:", "Conveyor remains halted if a cube is waiting at pick station (X >= -0.015m), achieving 100% capture reliability.")
        ]),
        ("Feedback 3: Anti-Sink & Twist", COLOR_SUCCESS, [
            ("Issue:", "Claw slightly penetrated conveyor belt during descent; upon grasping, cube twisted off-axis (13.6° skew)."),
            ("Orthogonalization:", "Standardized down_orientation = Quaternion(0.7071, 0.7071, 0, 0), locking tool0 strictly square to belt."),
            ("Anti-Sink Clearance:", "Set grasp_offset_z = 0.065m (fingertips clear belt by 2.3cm). Pure parenting preserves natural cube pose.")
        ])
    ]

    for idx, (title, color, items_list) in enumerate(feedback_cards):
        x = Inches(0.8 + idx * 4.0)
        add_card(s6, x, Inches(1.6), Inches(3.733), Inches(5.0), fill_color=COLOR_CARD_BG)
        ftf = s6.shapes.add_textbox(x + Inches(0.2), Inches(1.8), Inches(3.333), Inches(4.6)).text_frame
        ftf.word_wrap = True
        p = ftf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = color
        p.space_after = Pt(10)

        for lbl, desc in items_list:
            p = ftf.add_paragraph()
            r1 = p.add_run()
            r1.text = "• " + lbl + " "
            r1.font.bold = True
            r1.font.size = Pt(9.5)
            r1.font.color.rgb = COLOR_PRIMARY
            r2 = p.add_run()
            r2.text = desc
            r2.font.size = Pt(9.0)
            r2.font.color.rgb = COLOR_TEXT_MAIN
            p.space_after = Pt(6)

    # =========================================================================
    # SLIDE 07: LAYOUT OPTIMIZATION
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Layout Optimization", "Workcell Layout: Front Pick Zone and Flanking Bins", "Slide 07")

    layout_headers = ["Component", "Selected Setup", "Engineering Reason"]
    layout_data = [
        ["Conveyor", "3.6 m, centered (X = -0.60 m)", "Stable transport through robot workspace; ample gliding run"],
        ["Pick zone", "Front center (X = -0.60 m, Y = 0.00 m)", "Short, symmetric approach minimizing arm travel distance & inertia"],
        ["Red and yellow bins", "Left (Y = +0.55 m) and right (Y = -0.55 m)", "Clear transfer paths eliminating collision hazards with conveyor"],
        ["Blue bin", "Behind robot (X = +0.50 m, Y = 0.00 m)", "Separates third sorting target via pure base pan rotation"],
        ["Support surface", "4.0 m × 2.0 m heavy industrial table", "Rigid foundation for rails, bins and robot base fixtures"]
    ]
    add_table(s7, Inches(0.8), Inches(1.6), Inches(11.733), Inches(3.8), layout_headers, layout_data,
              [Inches(2.4), Inches(3.8), Inches(5.533)])

    add_card(s7, Inches(0.8), Inches(5.6), Inches(11.733), Inches(1.15), fill_color=COLOR_CARD_BG)
    ltf = s7.shapes.add_textbox(Inches(1.0), Inches(5.68), Inches(11.333), Inches(0.98)).text_frame
    ltf.word_wrap = True
    p = ltf.paragraphs[0]
    p.text = "SPATIAL CLEARANCE & SAFETY DIMENSIONS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(4)

    p_geo = ltf.add_paragraph()
    p_geo.text = "• Bin Mouth Enlargement: Expanded +35% to 0.38 m × 0.38 m × 0.10 m for 100% free-fall capture rate.\n" \
                 "• Vertical Safety Envelopes: +16 cm Pre-grasp & Lift altitude completely clears conveyor aluminum rails (Z = +0.10 m) with zero contact."
    p_geo.font.size = Pt(9.5)
    p_geo.font.color.rgb = COLOR_TEXT_MAIN

    # =========================================================================
    # SLIDE 08: KINEMATICS
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Kinematics", "Downward Wrist Orientation and Transfer Motion", "Slide 08")

    add_card(s8, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.0), fill_color=COLOR_CARD_BG)
    k1 = s8.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.3), Inches(4.6)).text_frame
    k1.word_wrap = True
    p = k1.paragraphs[0]
    p.text = "Motion Strategy"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(10)

    strat_pts = [
        ("Downward tool orientation:", "tool0 remains vertical ([0, 0, -1]) during approach, grasp and release via locked wrist (q4 = 90.0°)."),
        ("Pre-grasp waypoint:", "The robot approaches above the target (+16cm) before descending."),
        ("Vertical descent:", "The final approach moves along pure Cartesian Z, avoiding contact with conveyor rails."),
        ("Lift before transfer:", "The cube clears the conveyor (+16cm) before base rotation begins."),
        ("Dominant shoulder pan:", "The transfer uses a large base rotation while other joints remain stable like a SCARA crane.")
    ]
    for lbl, desc in strat_pts:
        p = k1.add_paragraph()
        r1 = p.add_run()
        r1.text = "✔ " + lbl + " "
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = COLOR_PRIMARY
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(6)

    add_card(s8, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.0), fill_color=COLOR_CARD_BG)
    k2 = s8.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.6)).text_frame
    k2.word_wrap = True
    p = k2.paragraphs[0]
    p.text = "Joint Values across Poses (Radians)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT
    p.space_after = Pt(10)

    joint_pts = [
        ("Standby:", "[0.2945, -1.4760, -2.1278, -1.1022, 1.5708, 0.5291]"),
        ("Red bin (left):", "[-1.0741, -1.4731, -2.2727, -0.9602, 1.5708, 0.5291]"),
        ("Yellow bin (right):", "[1.7077, -1.4731, -2.2727, -0.9602, 1.5708, 0.5291]"),
        ("Blue bin (rear):", "[-2.7858, -1.3576, -2.3651, -0.9833, 1.5708, 0.5291]"),
        ("Observation:", "Shoulder lift, elbow, and wrist joints stay within 0.15 rad of each other across all three bin targets; only shoulder pan swings widely.")
    ]
    for lbl, desc in joint_pts:
        p = k2.add_paragraph()
        r1 = p.add_run()
        r1.text = "⚙ " + lbl + " "
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = COLOR_PRIMARY
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(6)

    # =========================================================================
    # SLIDE 09: PHYSICS AND VISUALS
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Physics and Visuals", "Conveyor Motion and Pick-Zone Stopping", "Slide 09")

    add_card(s9, Inches(0.8), Inches(1.6), Inches(5.7), Inches(5.0), fill_color=COLOR_CARD_BG)
    pv1 = s9.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(5.3), Inches(4.6)).text_frame
    pv1.word_wrap = True
    p = pv1.paragraphs[0]
    p.text = "Runtime Behaviour & Natural Friction Deceleration"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_SUCCESS
    p.space_after = Pt(10)

    run_pts = [
        ("Transport:", "Objects move at configured conveyor speed (rock-steady 0.30 m/s)."),
        ("Detection:", "Pick-zone optical sensor actively identifies every SortableObject cube."),
        ("Stop:", "At X >= -0.015 m, conveyor cuts power (StopConveyor()). Friction halts cube smoothly at X ≈ 0.000 m (± 3 mm)."),
        ("Zero Teleportation:", "Eliminates artificial coordinate snapping or kinematic freezing."),
        ("Resume:", "Conveyor restarts automatically after cube handling and release into bin.")
    ]
    for lbl, desc in run_pts:
        p = pv1.add_paragraph()
        r1 = p.add_run()
        r1.text = "✔ " + lbl + " "
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = COLOR_PRIMARY
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(6)

    add_card(s9, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.0), fill_color=COLOR_CARD_BG)
    pv2 = s9.shapes.add_textbox(Inches(7.0), Inches(1.8), Inches(5.3), Inches(4.6)).text_frame
    pv2.word_wrap = True
    p = pv2.paragraphs[0]
    p.text = "Multi-Item Flow & Visual Rig Consistency"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_ACCENT
    p.space_after = Pt(10)

    vis_pts = [
        ("Continuous Multi-Item Flow:", "Upgraded Spawner maintains 2-3 active cubes on belt simultaneously, providing continuous sorting."),
        ("Anti-Stacking Spacing:", "Strict 38 cm minimum spacing (IsSpawnAreaClear()) prevents any cube collisions at spawn head."),
        ("Visual consistency:", "Belt texture scrolling is synchronized 1:1 with physical object motion at 0.30 m/s."),
        ("Mechanical Rig Structure:", "Ribbed rubber belt, dual aluminum guide rails, dual chrome rollers, and gearmotor unit."),
        ("Optical Sensor LED:", "Dual-color indicator displays Green when running, switching to Red when cube stops at pick center.")
    ]
    for lbl, desc in vis_pts:
        p = pv2.add_paragraph()
        r1 = p.add_run()
        r1.text = "⚙ " + lbl + " "
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = COLOR_PRIMARY
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = COLOR_TEXT_MAIN
        p.space_after = Pt(6)

    # =========================================================================
    # SLIDE 10: AUTOMATION PIPELINE
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Automation Pipeline", "7-Step Closed-Loop Task State Machine", "Slide 10")

    step_headers = ["Step", "State Name", "Primary Action", "Safety & Validation Guard"]
    step_data = [
        ["1", "STANDBY", "Arm hovers above pick station (Z = 0.42 m)", "Elbow held elevated; wrist strictly downward"],
        ["2", "APPROACH", "Rapid Cartesian descent to Pre-grasp Pose (+16cm)", "Clears conveyor rails in < 0.5s; wait=True feedback"],
        ["3", "DESCENT", "Vertical Cartesian descent to contact (+6.5cm)", "Fingertips float 2.3cm above belt (zero sinking)"],
        ["4", "GRASP", "Publish gripper command (True); latch object", "Attach logic latches cube; MoveIt updates PlanningScene"],
        ["5", "LIFT", "Linear Cartesian lift back to safe height (+16cm)", "10cm vertical lift clears conveyor rails without snagging"],
        ["6", "MOVE_TO_BIN", "Single shoulder pan rotation to destination bin", "Non-singular trajectory avoids table collisions"],
        ["7", "RELEASE", "Publish gripper command (False); release cube", "Parenting detached; gravity drops cube into bin"],
        ["8", "READY / REARM", "Arm returns to Standby pose over pick zone", "Resumes conveyor & triggers spawner for next cycle"]
    ]
    add_table(s10, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.0), step_headers, step_data,
              [Inches(0.8), Inches(2.2), Inches(4.733), Inches(4.0)])

    # =========================================================================
    # SLIDE 11: QUALITY ASSURANCE
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Quality Assurance", "Empirical Test Benchmark: 70 Consecutive Trials", "Slide 11")

    qa_headers = ["Performance Metric", "Requirement", "Empirical Result", "Status Evaluation"]
    qa_data = [
        ["Total benchmark trials", ">= 10 cycles", "70 consecutive cycles logged", "Exceeds requirement by 700%"],
        ["Grasp success rate", ">= 90.0%", "100.0% (70 / 70 trials)", "Perfect reliability; zero drops"],
        ["Bin sorting accuracy", ">= 90.0%", "100.0% (70 / 70 trials)", "100% correct bin routing"],
        ["Mean cycle time", "< 30.0 s", "11.23 s (Min: 10.8s, Max: 12.1s)", "2.7x faster than threshold"],
        ["Conveyor transport speed", "0.2 - 0.5 m/s", "0.30 m/s rock-steady velocity", "Optimal industrial pace"],
        ["Coasting stop deviation", "<= 20 mm", "+- 3 mm repeatable halt", "High physical precision"]
    ]
    add_table(s11, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.0), qa_headers, qa_data,
              [Inches(3.2), Inches(2.2), Inches(3.6), Inches(2.733)])

    # =========================================================================
    # SLIDE 12: TECHNICAL DEFENSE
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Technical Defense", "Faculty Committee Engineering Defenses", "Slide 12")

    qa_cards = [
        ("Why are Pre-grasp and Lift poses necessary?", [
            "Industrial workcells divide workspace into Free-space transit and Fine Cartesian approach.",
            "Pre-grasp (+16cm) establishes a collision-free holding waypoint above the moving conveyor.",
            "Moving directly on diagonal paths risks collision with conveyor rails or bin edges."
        ]),
        ("Why avoid fixed sleep delays for motion timing?", [
            "Motion time varies with distance (1.07 rad to Red bin vs 2.78 rad to Blue bin).",
            "Fixed sleep delays cause premature grasp triggers (dropped objects) or unnecessary idle time.",
            "MoveIt trajectory execution feedback (wait=True) confirms physical arrival before next step."
        ]),
        ("How were ragdoll sagging & oscillations eliminated?", [
            "1. base_link locked with immovable = true in ArticulationBody.",
            "2. Gravity disabled (useGravity = false) on arm links; gravity compensation handled by MoveIt dynamics.",
            "3. Tuned high PhysX drive stiffness (stiffness = 50000, damping = 1000, forceLimit = 10000)."
        ])
    ]
    for idx, (title, points) in enumerate(qa_cards):
        x = Inches(0.8 + idx * 4.0)
        add_card(s12, x, Inches(1.6), Inches(3.733), Inches(5.0), fill_color=COLOR_CARD_BG)
        qtf = s12.shapes.add_textbox(x + Inches(0.2), Inches(1.8), Inches(3.333), Inches(4.6)).text_frame
        qtf.word_wrap = True
        p = qtf.paragraphs[0]
        p.text = title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = COLOR_PRIMARY
        p.space_after = Pt(10)

        for pt in points:
            p = qtf.add_paragraph()
            p.text = "• " + pt
            p.font.size = Pt(9.5)
            p.font.color.rgb = COLOR_TEXT_MAIN
            p.space_after = Pt(6)

    # =========================================================================
    # SLIDE 13: WEEK 06 OBJECTIVES & SPRINT BACKLOG (NEW DEDICATED SLIDE)
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Week 06 Objectives", "Week 06 Sprint: Fulfilling Requirement R5 & Robustness", "Slide 13")

    w6_cols = [
        ("R5 Conveyor Robustness", COLOR_PRIMARY, [
            "5-Minute Continuous Operation: Validate that conveyor, spawner, and sensor run non-stop without jamming.",
            "Variable Velocity Modulation: Support dynamic speed adjustment (0.1 to 0.5 m/s) via ROS parameter service.",
            "PhysX Friction Stability: Eliminate micro-slip across diverse cube weights (0.1kg - 0.5kg)."
        ]),
        ("Deterministic Spawner", COLOR_ACCENT, [
            "PRNG Seed Reproducibility: Implement seed parameters for RandomObjectSpawner.cs.",
            "Guaranteed Test Batches: Allow exact sequence replay (e.g. Red -> Blue -> Yellow) for automated regression.",
            "Spacing Latch Verification: Guarantee 38cm spacing under all belt acceleration profiles."
        ]),
        ("Fault Recovery", COLOR_SUCCESS, [
            "Belt Jam Auto-Recovery: Automated reverse-and-clear logic if an unexpected stall occurs.",
            "Perception Timeout Guard: Fail-safe state machine rollback if object detection frame drops.",
            "Socket Watchdog: Auto-reconnect handling for ROS-TCP-Endpoint in case of network hiccups."
        ])
    ]

    for idx, (title, color, items_list) in enumerate(w6_cols):
        x = Inches(0.8 + idx * 4.0)
        add_card(s13, x, Inches(1.6), Inches(3.733), Inches(4.0), fill_color=COLOR_CARD_BG)
        ptf = s13.shapes.add_textbox(x + Inches(0.2), Inches(1.8), Inches(3.333), Inches(3.6)).text_frame
        ptf.word_wrap = True
        p = ptf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = color
        p.space_after = Pt(12)

        for itm in items_list:
            p = ptf.add_paragraph()
            p.text = "• " + itm
            p.font.size = Pt(9.5)
            p.font.color.rgb = COLOR_TEXT_MAIN
            p.space_after = Pt(6)

    # Bottom Target Summary
    add_card(s13, Inches(0.8), Inches(5.8), Inches(11.733), Inches(0.95), fill_color=COLOR_CARD_BG)
    w6_btf = s13.shapes.add_textbox(Inches(1.0), Inches(5.88), Inches(11.333), Inches(0.8)).text_frame
    w6_btf.word_wrap = True
    p = w6_btf.paragraphs[0]
    p.text = "WEEK 06 DEFINITION OF DONE"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(3)

    p_w6 = w6_btf.add_paragraph()
    p_w6.text = "• Complete fulfillment of Requirement R5 (Conveyor & Spawner Integration).\n" \
                "• The workcell runs hands-free for > 5 minutes with zero cube miss, zero jam, and deterministic regression logging."
    p_w6.font.size = Pt(9.5)
    p_w6.font.color.rgb = COLOR_TEXT_MAIN

    # =========================================================================
    # SLIDE 14: MILESTONE 2 STRATEGIC ROADMAP (NEW DEDICATED SLIDE)
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "Milestone 2 Strategic Roadmap", "Milestone 2 (Week 10): Static Obstacle Avoidance & Perception", "Slide 14")

    m2_cols = [
        ("R5 & R6: Conveyor & Vision", COLOR_PRIMARY, [
            "R5 (Continuous Conveyor): Industrial belt running continuous multi-item queues with zero jam.",
            "R6 (Computer Vision Pipeline): Camera perception module replacing metadata detection.",
            "Color Classifier: OpenCV HSV segmentation classifying Red, Blue, and Yellow cubes under varying lighting."
        ]),
        ("R7: 3D Localization", COLOR_ACCENT, [
            "Camera-to-Robot Calibration: Hand-eye calibration linking camera pixel coordinates to UR10e base_link.",
            "Centroid Extraction: Projecting bounding box centroids to 3D Cartesian coordinates.",
            "Localization Accuracy: Benchmarked measurement error <= 20mm compared to ground truth."
        ]),
        ("R8: Static Obstacle Avoidance", COLOR_WARNING, [
            "Static Wall Barrier: Introducing physical obstacle wall between pick station and sorting bins.",
            "MoveIt PlanningScene: Real-time obstacle representation in collision matrix.",
            "Collision-Free Detour: OMPL planner automatically computes curved bypass paths around the wall."
        ])
    ]

    for idx, (title, color, items_list) in enumerate(m2_cols):
        x = Inches(0.8 + idx * 4.0)
        add_card(s14, x, Inches(1.6), Inches(3.733), Inches(4.0), fill_color=COLOR_CARD_BG)
        ptf = s14.shapes.add_textbox(x + Inches(0.2), Inches(1.8), Inches(3.333), Inches(3.6)).text_frame
        ptf.word_wrap = True
        p = ptf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = color
        p.space_after = Pt(12)

        for itm in items_list:
            p = ptf.add_paragraph()
            p.text = "• " + itm
            p.font.size = Pt(9.5)
            p.font.color.rgb = COLOR_TEXT_MAIN
            p.space_after = Pt(6)

    # Bottom M2 Acceptance Card
    add_card(s14, Inches(0.8), Inches(5.8), Inches(11.733), Inches(0.95), fill_color=RGBColor(254, 243, 199), border_color=RGBColor(252, 211, 77))
    m2_btf = s14.shapes.add_textbox(Inches(1.0), Inches(5.88), Inches(11.333), Inches(0.8)).text_frame
    m2_btf.word_wrap = True
    p = m2_btf.paragraphs[0]
    p.text = "MILESTONE 2 (WEEK 10) ACCEPTANCE CRITERIA: STOP-AND-PICK MODE"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(3)

    p_m2 = m2_btf.add_paragraph()
    p_m2.text = "• Verification of Requirements R5, R6, R7, and R8 in Stop-and-Pick mode (conveyor stops before grasp).\n" \
                "• Arm successfully navigates around static obstacle barrier with zero collision across >= 20 benchmark trials."
    p_m2.font.size = Pt(9.5)
    p_m2.font.color.rgb = COLOR_TEXT_MAIN

    # =========================================================================
    # SLIDE 15: SUMMARY & MILESTONE 1 ACCEPTANCE CONCLUSION
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "Milestone 1 Conclusion", "Summary of Deliverables & Official Acceptance Sign-Off", "Slide 15")

    # 3 Summary Cards
    sum_cols = [
        ("Requirements Met", COLOR_SUCCESS, [
            "R1 (Architecture & Scope): 100% Approved",
            "R2 (UR10e MoveIt Planning): 100% Operational",
            "R3 (ROS-Unity Bridge): 100% Low-Latency Streaming",
            "R4 (Closed-Loop Pick & Place): 100% Autonomous"
        ]),
        ("Empirical Evidence", COLOR_PRIMARY, [
            "70 Consecutive Trials Logged",
            "100.0% Grasp Success Rate",
            "100.0% Multi-Bin Placement Rate",
            "11.23s Mean Cycle Time (2.7x faster)"
        ]),
        ("Deliverables Package", COLOR_ACCENT, [
            "Git Tag Release: m1-verified",
            "Complete trials.csv QA Evidence",
            "Clean run_workcell.sh Launcher",
            "Multi-Camera Demo Visuals"
        ])
    ]

    for idx, (title, color, items_list) in enumerate(sum_cols):
        x = Inches(0.8 + idx * 4.0)
        add_card(s15, x, Inches(1.6), Inches(3.733), Inches(3.8), fill_color=COLOR_CARD_BG)
        ptf = s15.shapes.add_textbox(x + Inches(0.2), Inches(1.8), Inches(3.333), Inches(3.4)).text_frame
        ptf.word_wrap = True
        p = ptf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = color
        p.space_after = Pt(12)

        for itm in items_list:
            p = ptf.add_paragraph()
            p.text = "✔ " + itm
            p.font.size = Pt(10)
            p.font.color.rgb = COLOR_TEXT_MAIN
            p.space_after = Pt(6)

    # Bottom Acceptance Box
    add_card(s15, Inches(0.8), Inches(5.6), Inches(11.733), Inches(1.15), fill_color=COLOR_DARK_BG)
    c_btf = s15.shapes.add_textbox(Inches(1.0), Inches(5.68), Inches(11.333), Inches(0.98)).text_frame
    c_btf.word_wrap = True
    p = c_btf.paragraphs[0]
    p.text = "FORMAL MILESTONE 1 ACCEPTANCE REQUEST"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_SUCCESS
    p.space_after = Pt(3)

    p_c = c_btf.add_paragraph()
    p_c.text = "• All commitments made from Week 03 have been 100% fulfilled and reinforced with faculty feedback solutions.\n" \
               "• The UC8 sorting workcell is fully verified and ready for formal Milestone 1 sign-off and progression to Week 06 / Milestone 2."
    p_c.font.size = Pt(9.5)
    p_c.font.color.rgb = COLOR_TEXT_LIGHT

    # Save presentation
    output_path = "/home/kduy/RoboticProject/project_blueprint/docs/week05/UC8_Week05_Milestone1_Presentation.pptx"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    prs.save(output_path)
    print(f"[✔] PowerPoint presentation saved successfully to: {output_path}")

    # Copy to artifact path
    artifact_path = "/home/kduy/.gemini/antigravity/brain/ed6133c9-f823-473a-8cd1-c6f4372cde52/UC8_Week05_Milestone1_Presentation.pptx"
    import shutil
    shutil.copyfile(output_path, artifact_path)
    print(f"[✔] Copied presentation to artifact path: {artifact_path}")


if __name__ == "__main__":
    main()
