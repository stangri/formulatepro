#!/usr/bin/env python3
"""Generate a FormulatePro Usage Guide PDF for App Store screenshots."""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.enums import TA_LEFT, TA_CENTER

OUTPUT = "/Users/stangri/development/formulatepro/FormulatePro_Guide.pdf"

# Colors
BLUE_DARK = HexColor("#1a3a5c")
BLUE_MED = HexColor("#2c5f8a")
BLUE_LIGHT = HexColor("#e8f0f8")
BLUE_ACCENT = HexColor("#3a7cc2")
ORANGE = HexColor("#e8763a")
GRAY_DARK = HexColor("#333333")
GRAY_MED = HexColor("#666666")
GRAY_LIGHT = HexColor("#f5f5f5")
GREEN = HexColor("#2e7d32")

W, H = letter  # 612 x 792


def draw_header(c, title, subtitle=None):
    """Draw a page header bar."""
    # Header background
    c.setFillColor(BLUE_DARK)
    c.rect(0, H - 80, W, 80, fill=1, stroke=0)

    # App name
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(50, H - 52, "FormulatePro")

    # Section title
    c.setFont("Helvetica", 14)
    c.drawString(50, H - 72, title)

    if subtitle:
        c.setFillColor(HexColor("#aaccee"))
        c.setFont("Helvetica-Oblique", 11)
        c.drawRightString(W - 50, H - 52, subtitle)


def draw_footer(c, page_num, total_pages):
    """Draw page footer."""
    c.setFillColor(BLUE_DARK)
    c.rect(0, 0, W, 30, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica", 9)
    c.drawCentredString(W / 2, 10, f"Page {page_num} of {total_pages}")
    c.drawString(50, 10, "FormulatePro User Guide")
    c.drawRightString(W - 50, 10, "formulatepro.app")


def draw_tool_icon(c, x, y, tool_type, size=28):
    """Draw a simple icon representation for a tool."""
    c.saveState()
    # Icon background circle
    c.setFillColor(BLUE_ACCENT)
    c.circle(x + size / 2, y + size / 2, size / 2, fill=1, stroke=0)

    c.setStrokeColor(white)
    c.setFillColor(white)
    c.setLineWidth(1.5)

    cx, cy = x + size / 2, y + size / 2
    r = size / 2 - 6

    if tool_type == "arrow":
        # Arrow pointer
        c.line(cx - r, cy - r, cx + r / 2, cy + r / 2)
        c.line(cx + r / 2, cy + r / 2, cx, cy + r / 4)
        c.line(cx + r / 2, cy + r / 2, cx + r / 4, cy)
    elif tool_type == "ellipse":
        c.ellipse(cx - r, cy - r * 0.7, cx + r, cy + r * 0.7, fill=0, stroke=1)
    elif tool_type == "rectangle":
        c.rect(cx - r, cy - r * 0.7, r * 2, r * 1.4, fill=0, stroke=1)
    elif tool_type == "squiggle":
        p = c.beginPath()
        p.moveTo(cx - r, cy)
        p.curveTo(cx - r / 2, cy + r, cx, cy - r, cx + r, cy)
        c.drawPath(p, fill=0, stroke=1)
    elif tool_type == "text":
        c.setFont("Helvetica-Bold", size * 0.5)
        c.drawCentredString(cx, cy - size * 0.15, "T")
    elif tool_type == "checkmark":
        p = c.beginPath()
        p.moveTo(cx - r, cy)
        p.lineTo(cx - r / 3, cy - r)
        p.lineTo(cx + r, cy + r)
        c.drawPath(p, fill=0, stroke=1)
    elif tool_type == "stamp":
        c.rect(cx - r * 0.6, cy - r * 0.3, r * 1.2, r * 0.6, fill=0, stroke=1)
        c.line(cx, cy + r * 0.3, cx, cy + r)
        c.circle(cx, cy + r, 2, fill=1, stroke=0)

    c.restoreState()


def draw_section_box(c, x, y, w, h, title, body_lines, icon=None):
    """Draw a styled section box with title and content."""
    # Box background
    c.setFillColor(GRAY_LIGHT)
    c.roundRect(x, y, w, h, 6, fill=1, stroke=0)

    # Title bar
    c.setFillColor(BLUE_MED)
    c.roundRect(x, y + h - 30, w, 30, 6, fill=1, stroke=0)
    # Cover bottom corners of title bar
    c.rect(x, y + h - 30, w, 15, fill=1, stroke=0)

    # Title text
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 12)
    title_x = x + 12
    if icon:
        draw_tool_icon(c, x + 8, y + h - 27, icon, 22)
        title_x = x + 36
    c.drawString(title_x, y + h - 22, title)

    # Body text
    c.setFillColor(GRAY_DARK)
    c.setFont("Helvetica", 10)
    text_y = y + h - 48
    for line in body_lines:
        if line.startswith("*"):
            c.setFont("Helvetica-Bold", 10)
            c.drawString(x + 14, text_y, line[1:])
            c.setFont("Helvetica", 10)
        elif line.startswith(">"):
            c.setFillColor(BLUE_ACCENT)
            c.setFont("Helvetica-Bold", 10)
            c.drawString(x + 14, text_y, line[1:])
            c.setFillColor(GRAY_DARK)
            c.setFont("Helvetica", 10)
        else:
            c.drawString(x + 14, text_y, line)
        text_y -= 16

    return text_y


def draw_tip_box(c, x, y, w, tip_text, number=None):
    """Draw a highlighted tip box."""
    h = 40
    c.setFillColor(HexColor("#fff8e1"))
    c.setStrokeColor(ORANGE)
    c.setLineWidth(1)
    c.roundRect(x, y, w, h, 4, fill=1, stroke=1)

    if number:
        c.setFillColor(ORANGE)
        c.circle(x + 18, y + h / 2, 10, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 10)
        c.drawCentredString(x + 18, y + h / 2 - 4, str(number))

    c.setFillColor(GRAY_DARK)
    c.setFont("Helvetica", 9.5)
    text_x = x + 34 if number else x + 12
    # Simple word wrap
    words = tip_text.split()
    line = ""
    line_y = y + h - 13
    for word in words:
        test = line + " " + word if line else word
        if c.stringWidth(test, "Helvetica", 9.5) < w - (text_x - x) - 12:
            line = test
        else:
            c.drawString(text_x, line_y, line)
            line_y -= 13
            line = word
    if line:
        c.drawString(text_x, line_y, line)


def draw_shortcut_row(c, x, y, key, description):
    """Draw a keyboard shortcut row."""
    # Key box
    c.setFillColor(white)
    c.setStrokeColor(HexColor("#cccccc"))
    c.setLineWidth(0.5)
    key_w = max(c.stringWidth(key, "Helvetica-Bold", 11) + 14, 28)
    c.roundRect(x, y - 4, key_w, 20, 3, fill=1, stroke=1)
    c.setFillColor(GRAY_DARK)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(x + key_w / 2, y, key)

    # Description
    c.setFont("Helvetica", 10)
    c.setFillColor(GRAY_MED)
    c.drawString(x + key_w + 10, y, description)


# ============================================================
# Create PDF
# ============================================================
TOTAL_PAGES = 5
c = canvas.Canvas(OUTPUT, pagesize=letter)
c.setTitle("FormulatePro User Guide")
c.setAuthor("Melmac Network")
c.setSubject("Usage instructions and tips for FormulatePro")

# ============================================================
# PAGE 1 — Welcome / Overview
# ============================================================
draw_header(c, "User Guide", "Version 1.0")
draw_footer(c, 1, TOTAL_PAGES)

# Welcome text
y = H - 120
c.setFillColor(BLUE_DARK)
c.setFont("Helvetica-Bold", 22)
c.drawString(50, y, "Welcome to FormulatePro")
y -= 28
c.setFont("Helvetica", 12)
c.setFillColor(GRAY_MED)
c.drawString(50, y, "The easy way to annotate and mark up your PDF documents on macOS.")

y -= 45
c.setFillColor(GRAY_DARK)
c.setFont("Helvetica", 11)
overview_lines = [
    "FormulatePro lets you open any PDF and add annotations directly",
    "on top of it. Draw shapes, write text, place checkmarks, and more.",
    "",
    "Whether you're filling out forms, grading papers, reviewing",
    "documents, or marking up blueprints — FormulatePro gives you",
    "the tools you need in a clean, native macOS interface.",
]
for line in overview_lines:
    c.drawString(50, y, line)
    y -= 17

# Feature highlights
y -= 100
features = [
    ("Draw & Annotate", "Add rectangles, ellipses, freehand\ndrawings, and text to any PDF."),
    ("Fill Out Forms", "Use the text and checkmark tools\nto fill in PDF forms by hand."),
    ("Customize Appearance", "Set stroke and fill colors, line\nwidth, and fonts to your liking."),
    ("Export to PDF", "Print or export your annotated\ndocument as a standard PDF."),
]

col_w = (W - 100 - 20) / 2
for i, (feat_title, feat_desc) in enumerate(features):
    fx = 50 + (i % 2) * (col_w + 20)
    fy = y - (i // 2) * 110
    # Feature card
    c.setFillColor(BLUE_LIGHT)
    c.roundRect(fx, fy - 10, col_w, 95, 6, fill=1, stroke=0)
    c.setFillColor(BLUE_DARK)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(fx + 14, fy + 65, feat_title)
    c.setFillColor(GRAY_DARK)
    c.setFont("Helvetica", 10)
    desc_y = fy + 48
    for dl in feat_desc.split("\n"):
        c.drawString(fx + 14, desc_y, dl)
        desc_y -= 14

# Getting started box at bottom
gs_y = 120
c.setFillColor(GREEN)
c.roundRect(50, gs_y, W - 100, 50, 6, fill=1, stroke=0)
c.setFillColor(white)
c.setFont("Helvetica-Bold", 13)
c.drawString(70, gs_y + 28, "Getting Started")
c.setFont("Helvetica", 11)
c.drawString(70, gs_y + 10, "Open a PDF with File \u2192 Open, then select a tool from the Tool Palette to begin annotating.")

c.showPage()

# ============================================================
# PAGE 2 — Tools Guide
# ============================================================
draw_header(c, "Drawing Tools", "Your annotation toolkit")
draw_footer(c, 2, TOTAL_PAGES)

y = H - 110

tools = [
    ("Arrow / Selection Tool", "arrow", [
        "Select, move, and resize annotations.",
        "Click an object to select it. Drag to move.",
        "Use the handles to resize any selected object.",
        ">Shortcut: M",
    ]),
    ("Ellipse Tool", "ellipse", [
        "Draw circles and ovals on your PDF.",
        "Click and drag to create an ellipse.",
        "Hold Shift for a perfect circle.",
        ">Shortcut: E",
    ]),
    ("Rectangle Tool", "rectangle", [
        "Draw rectangles and squares.",
        "Click and drag to create a rectangle.",
        "Hold Shift for a perfect square.",
        ">Shortcut: U",
    ]),
    ("Freehand / Squiggle Tool", "squiggle", [
        "Draw freehand lines and curves.",
        "Click and drag to draw freely.",
        "Great for signatures and handwritten notes.",
        ">Shortcut: P",
    ]),
    ("Text Area Tool", "text", [
        "Add multi-line text boxes to your PDF.",
        "Click to place, then type your text.",
        "Use the Font panel to change font and size.",
        ">Shortcut: T",
    ]),
    ("Checkmark Tool", "checkmark", [
        "Place checkmarks on forms and documents.",
        "Click anywhere to place a checkmark.",
        "Perfect for filling out checklists and forms.",
        ">Shortcut: X",
    ]),
    ("Stamp Tool", "stamp", [
        "Place image stamps on your document.",
        "Use for logos, signatures, or custom marks.",
        "Stamps can be resized after placement.",
    ]),
]

box_h = 100
col_w = (W - 110) / 2

for i, (name, icon, lines) in enumerate(tools):
    col = i % 2
    row = i // 2
    bx = 50 + col * (col_w + 10)
    by = y - row * (box_h + 10) - box_h
    draw_section_box(c, bx, by, col_w, box_h, name, lines, icon=icon)

# Bottom note
note_y = y - 4 * (box_h + 10) - box_h - 15
c.setFillColor(GRAY_MED)
c.setFont("Helvetica-Oblique", 10)
c.drawCentredString(W / 2, note_y, "Tip: Press Cmd+Option and drag to temporarily switch to the Arrow tool from any other tool.")

c.showPage()

# ============================================================
# PAGE 3 — Inspector & Customization
# ============================================================
draw_header(c, "Inspector & Customization", "Tailor your annotations")
draw_footer(c, 3, TOTAL_PAGES)

y = H - 120

c.setFillColor(BLUE_DARK)
c.setFont("Helvetica-Bold", 16)
c.drawString(50, y, "The Inspector Panel")
y -= 22
c.setFillColor(GRAY_DARK)
c.setFont("Helvetica", 11)
insp_lines = [
    "The Inspector panel lets you customize the appearance of your",
    "annotations. Select any graphic and adjust its properties.",
]
for line in insp_lines:
    c.drawString(50, y, line)
    y -= 16

y -= 15

# Inspector properties
props = [
    ("Stroke", "Enable or disable the outline of shapes. Choose a stroke\ncolor and adjust the line width using the stepper control."),
    ("Fill", "Enable or disable the fill color of shapes. Choose any\ncolor from the macOS color picker."),
    ("Line Width", "Control the thickness of shape outlines.\nUse the stepper or type a specific value."),
    ("Hide When Printing", "Mark annotations as non-printing. These will\nappear on screen but won't show up when you print or export."),
]

for title, desc in props:
    # Property card
    c.setFillColor(BLUE_LIGHT)
    c.roundRect(50, y - 10, W - 100, 52, 5, fill=1, stroke=0)

    c.setFillColor(BLUE_DARK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(65, y + 24, title)

    c.setFillColor(GRAY_DARK)
    c.setFont("Helvetica", 10)
    desc_y = y + 8
    for dl in desc.split("\n"):
        c.drawString(65, desc_y, dl)
        desc_y -= 14
    y -= 68

# Fonts & Colors section
y -= 15
c.setFillColor(BLUE_DARK)
c.setFont("Helvetica-Bold", 16)
c.drawString(50, y, "Fonts & Colors")
y -= 22
c.setFont("Helvetica", 11)
c.setFillColor(GRAY_DARK)

font_lines = [
    "Access the Font panel via Edit \u2192 Font \u2192 Show Fonts to change",
    "the typeface, size, and style of your text annotations.",
    "",
    "Access the Color picker via Edit \u2192 Font \u2192 Show Colors to set",
    "colors for shapes and text.",
]
for line in font_lines:
    c.drawString(50, y, line)
    y -= 16

y -= 25
# Default settings tip
draw_tip_box(c, 50, y - 10, W - 100,
    "Tip: Choose a font or color with nothing selected to set the default for all new annotations.", 1)

c.showPage()

# ============================================================
# PAGE 4 — Tips & Tricks
# ============================================================
draw_header(c, "Tips & Tricks", "Work smarter with FormulatePro")
draw_footer(c, 4, TOTAL_PAGES)

y = H - 115

tips = [
    "To move text while editing, hold down Command (Cmd) and Option and drag the text box to reposition it without losing your cursor.",
    "If you pick a font from the Font panel (Edit \u2192 Font \u2192 Show Fonts) while not editing text, it will be used as the default font for all new text entries.",
    "To export a FormulatePro document as a standard PDF, choose File \u2192 Print, click the PDF button in the lower-left, and choose Save As PDF.",
    "If you pick a color from the Color picker (Edit \u2192 Font \u2192 Show Colors) when nothing is selected and text isn't being edited, the color will be the default for new shapes and text.",
    "Use the Delete key to quickly remove any selected annotations. Select multiple items by Shift-clicking, then delete them all at once.",
    "The Zoom In and Zoom Out buttons in the toolbar let you examine fine details or get an overview of the whole page.",
    "Use the Page Navigation buttons (Next/Previous) in the toolbar to quickly move between pages in multi-page documents.",
    "Press Cmd+Option and drag to temporarily switch to the Arrow tool from any other tool \u2014 release to return to your previous tool.",
]

for i, tip in enumerate(tips):
    draw_tip_box(c, 50, y - 10, W - 100, tip, i + 1)
    y -= 56

c.showPage()

# ============================================================
# PAGE 5 — Keyboard Shortcuts & Workflow
# ============================================================
draw_header(c, "Keyboard Shortcuts & Workflow", "Speed up your workflow")
draw_footer(c, 5, TOTAL_PAGES)

y = H - 120

c.setFillColor(BLUE_DARK)
c.setFont("Helvetica-Bold", 16)
c.drawString(50, y, "Keyboard Shortcuts")
y -= 30

shortcuts = [
    ("T", "Text Area tool"),
    ("M", "Arrow / Selection tool (Move)"),
    ("E", "Ellipse tool"),
    ("U", "Rectangle tool"),
    ("P", "Freehand / Squiggle tool (Pen)"),
    ("X", "Checkmark tool"),
    ("Cmd+O", "Open a PDF document"),
    ("Cmd+S", "Save your document"),
    ("Cmd+P", "Print / Export to PDF"),
    ("Cmd+Z", "Undo last action"),
    ("Shift+Cmd+Z", "Redo last action"),
    ("Cmd+Opt", "Quick-switch to Arrow tool (hold)"),
    ("Delete", "Remove selected annotations"),
]

for key, desc in shortcuts:
    draw_shortcut_row(c, 65, y, key, desc)
    y -= 28

# Workflow section
y -= 20
c.setFillColor(BLUE_DARK)
c.setFont("Helvetica-Bold", 16)
c.drawString(50, y, "Typical Workflow")
y -= 25

steps = [
    ("1", "Open", "Open a PDF document with File \u2192 Open (Cmd+O)."),
    ("2", "Annotate", "Select tools from the Tool Palette and add your annotations."),
    ("3", "Customize", "Use the Inspector to adjust colors, line width, and fill."),
    ("4", "Save", "Save as a .formulate file to preserve editability (Cmd+S)."),
    ("5", "Export", "Print or export as PDF via File \u2192 Print \u2192 PDF \u2192 Save As PDF."),
]

for num, title, desc in steps:
    # Step number circle
    c.setFillColor(BLUE_ACCENT)
    c.circle(68, y + 4, 12, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(68, y, num)

    # Step content
    c.setFillColor(BLUE_DARK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(90, y + 4, title)
    c.setFillColor(GRAY_DARK)
    c.setFont("Helvetica", 10)
    c.drawString(90, y - 10, desc)

    # Connecting line (except last)
    if num != "5":
        c.setStrokeColor(HexColor("#cccccc"))
        c.setLineWidth(1)
        c.line(68, y - 10, 68, y - 25)

    y -= 42

# Support footer
y -= 10
c.setFillColor(BLUE_LIGHT)
c.roundRect(50, y - 5, W - 100, 40, 6, fill=1, stroke=0)
c.setFillColor(BLUE_DARK)
c.setFont("Helvetica-Bold", 11)
c.drawCentredString(W / 2, y + 16, "Thank you for using FormulatePro!")
c.setFont("Helvetica", 10)
c.setFillColor(GRAY_MED)
c.drawCentredString(W / 2, y + 1, "Distributed with care by Melmac Network")

c.save()
print(f"PDF created: {OUTPUT}")
