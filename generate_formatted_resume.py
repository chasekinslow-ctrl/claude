from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
import os

OUT = "/home/user/claude"

# Colors matching the template
NAVY = HexColor("#2B3544")
ORANGE = HexColor("#E8872B")
DARK_TEXT = HexColor("#1A1A1A")
WHITE = white
SIDEBAR_WIDTH = 2.1 * inch
PAGE_W, PAGE_H = letter  # 612 x 792

def draw_wrapped(c, text, x, y, max_width, font_name, font_size, leading, color=DARK_TEXT):
    """Draw wrapped text and return new y position."""
    c.setFont(font_name, font_size)
    c.setFillColor(color)
    lines = simpleSplit(text, font_name, font_size, max_width)
    for line in lines:
        if y < 40:
            c.showPage()
            y = PAGE_H - 40
            # Redraw sidebar on new page
            draw_sidebar_bg(c)
        c.setFont(font_name, font_size)
        c.setFillColor(color)
        c.drawString(x, y, line)
        y -= leading
    return y

def draw_bullet(c, text, x, y, max_width, indent=12):
    """Draw an orange-dash bullet point with wrapped text."""
    c.setFillColor(ORANGE)
    c.setFont("Helvetica", 10)
    c.drawString(x, y, "\u2014")  # em dash

    c.setFillColor(DARK_TEXT)
    c.setFont("Helvetica", 9.5)
    text_x = x + indent
    lines = simpleSplit(text, "Helvetica", 9.5, max_width - indent)
    for i, line in enumerate(lines):
        if y < 40:
            c.showPage()
            y = PAGE_H - 40
            draw_sidebar_bg(c)
        c.setFont("Helvetica", 9.5)
        c.setFillColor(DARK_TEXT)
        if i == 0:
            c.drawString(text_x, y, line)
        else:
            c.drawString(text_x + 4, y, line)
        y -= 13
    return y

def draw_sidebar_bg(c):
    """Draw the navy sidebar background."""
    c.setFillColor(NAVY)
    c.rect(0, 0, SIDEBAR_WIDTH, PAGE_H, fill=1, stroke=0)

def draw_sidebar_section(c, title, y):
    """Draw an orange section header in the sidebar."""
    c.setFillColor(ORANGE)
    c.setFont("Helvetica-Bold", 9.5)
    c.drawString(18, y, title)
    return y - 16

def draw_sidebar_item(c, text, y, bold=False):
    """Draw a sidebar list item."""
    c.setFillColor(WHITE)
    font = "Helvetica-Bold" if bold else "Helvetica"
    c.setFont(font, 8.5)
    lines = simpleSplit(text, font, 8.5, SIDEBAR_WIDTH - 36)
    for line in lines:
        c.drawString(22, y, line)
        y -= 12
    return y

def draw_sidebar_bullet(c, text, y):
    """Draw a bullet item in the sidebar."""
    c.setFillColor(WHITE)
    c.setFont("Helvetica", 8.5)
    lines = simpleSplit(text, "Helvetica", 8.5, SIDEBAR_WIDTH - 44)
    for i, line in enumerate(lines):
        if i == 0:
            c.drawString(22, y, "\u2022  " + line)
        else:
            c.drawString(32, y, line)
        y -= 12
    return y

def make_resume():
    filepath = os.path.join(OUT, "Chase_Kinslow_Resume.pdf")
    c = canvas.Canvas(filepath, pagesize=letter)

    # ── Sidebar background ──
    draw_sidebar_bg(c)

    # ── SIDEBAR CONTENT ──
    sy = PAGE_H - 50

    # Contact
    sy = draw_sidebar_section(c, "CONTACT", sy)
    sy = draw_sidebar_item(c, "(501) 707-7779", sy)
    sy = draw_sidebar_item(c, "chasekn30@yahoo.com", sy)
    sy = draw_sidebar_item(c, "Monroe, LA 71201", sy)
    sy -= 10

    # Core Competencies
    sy = draw_sidebar_section(c, "CORE COMPETENCIES", sy)
    competencies = [
        "Vehicle Cleaning & Detailing",
        "Facility Sanitation & Maintenance",
        "Safety Inspections & Audits",
        "Equipment Operation & Care",
        "POS & Cash Handling",
        "Inventory Control",
        "Customer Service & Support",
        "Workspace Organization",
        "Conflict Resolution",
        "Compliance & Documentation",
        "Computer Proficiency",
    ]
    for comp in competencies:
        sy = draw_sidebar_bullet(c, comp, sy)
    sy -= 10

    # Education
    sy = draw_sidebar_section(c, "EDUCATION", sy)
    sy = draw_sidebar_item(c, "Bachelor's Degree", sy, bold=True)
    sy = draw_sidebar_item(c, "University of Mississippi", sy)
    sy -= 4
    sy = draw_sidebar_item(c, "High School Diploma", sy, bold=True)
    sy = draw_sidebar_item(c, "Pulaski Academy", sy)
    sy -= 10

    # Tools
    sy = draw_sidebar_section(c, "TOOLS", sy)
    tools = [
        "Microsoft Office Suite",
        "QuickBooks Desktop & Online",
        "POS Systems",
        "Digital Inventory Tracking",
        "Carpet Shampoo Machines",
        "Air Purifiers & Detailing Tools",
    ]
    for tool in tools:
        sy = draw_sidebar_bullet(c, tool, sy)

    # ── MAIN CONTENT ──
    mx = SIDEBAR_WIDTH + 24  # main content x start
    mw = PAGE_W - mx - 30   # main content width
    my = PAGE_H - 48

    # Name
    c.setFont("Helvetica-Bold", 26)
    c.setFillColor(DARK_TEXT)
    c.drawString(mx, my, "CHASE KINSLOW")
    my -= 22

    # Subtitle
    c.setFont("Helvetica-Oblique", 11)
    c.setFillColor(ORANGE)
    c.drawString(mx, my, "Operations & Facility Maintenance Professional")
    my -= 28

    # ── PROFESSIONAL SUMMARY ──
    c.setFont("Helvetica-Bold", 11.5)
    c.setFillColor(DARK_TEXT)
    c.drawString(mx, my, "PROFESSIONAL SUMMARY")
    my -= 4
    c.setStrokeColor(ORANGE)
    c.setLineWidth(1.5)
    c.line(mx, my, mx + mw, my)
    my -= 14

    summary = (
        "Dedicated operations professional with hands-on experience in facility maintenance, "
        "sanitation, logistics, and customer service. Background spans daily facility upkeep, "
        "equipment inspections, cleaning protocol execution, and cross-functional coordination "
        "to ensure safe, clean environments that exceed standards. Detail-oriented, organized, "
        "and proactive \u2014 equally comfortable washing and prepping vehicles, maintaining "
        "workspaces, or assisting customers with a professional, team-first approach."
    )
    my = draw_wrapped(c, summary, mx, my, mw, "Helvetica", 9.5, 13, DARK_TEXT)
    my -= 10

    # ── KEY ACHIEVEMENTS & SKILLS ──
    c.setFont("Helvetica-Bold", 11.5)
    c.setFillColor(DARK_TEXT)
    c.drawString(mx, my, "KEY ACHIEVEMENTS & SKILLS")
    my -= 4
    c.setStrokeColor(ORANGE)
    c.line(mx, my, mx + mw, my)
    my -= 16

    # Sub-section: Facility Operations
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(DARK_TEXT)
    c.drawString(mx, my, "Facility Operations, Maintenance & Inspections")
    my -= 14

    bullets_facility = [
        "Performed rigorous opening and closing facility maintenance, applying systematic inspection protocols to ensure the physical environment exceeded brand standards, safety requirements, and cleanliness benchmarks",
        "Orchestrated daily equipment logistics and staging operations, managing rotation, maintenance tracking, and supply distribution to maintain 100% operational readiness",
        "Maintained clean, organized work environments through daily cleaning routines, supply restocking, and proactive identification of maintenance needs before they became issues",
    ]
    for b in bullets_facility:
        my = draw_bullet(c, b, mx, my, mw)
        my -= 2
    my -= 6

    # Sub-section: Customer Service & Operations
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(DARK_TEXT)
    c.drawString(mx, my, "Customer Service, Sales & Operations")
    my -= 14

    bullets_customer = [
        "Executed high-volume POS transactions with zero-error accuracy, managing daily cash handling and register reconciliation while delivering consultative customer service across multiple product categories",
        "Conducted walk-in consultations and product recommendations, closing sales by matching customer needs to available solutions directly applicable to guest service and occupancy-building initiatives",
        "Cross-trained across all departments to provide coverage wherever needed, ensuring uninterrupted service during peak periods and staff absences",
    ]
    for b in bullets_customer:
        my = draw_bullet(c, b, mx, my, mw)
        my -= 2
    my -= 6

    # Sub-section: Documentation & Compliance
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(DARK_TEXT)
    c.drawString(mx, my, "Documentation, Compliance & Accuracy")
    my -= 14

    bullets_doc = [
        "Managed comprehensive documentation workflows requiring zero-error precision \u2014 reconciliations, workpapers, and submissions where a single discrepancy disqualified an entire project file",
        "Directed inventory control using digital tracking systems to prevent shrink, maintain accurate stock levels, and ensure supplies were distributed across all operational areas",
        "Orchestrated monthly close procedures with rigorous reconciliation of accounts and records to maintain total data integrity across multiple client portfolios",
    ]
    for b in bullets_doc:
        my = draw_bullet(c, b, mx, my, mw)
        my -= 2
    my -= 10

    # ── EMPLOYMENT HISTORY ──
    c.setFont("Helvetica-Bold", 11.5)
    c.setFillColor(DARK_TEXT)
    c.drawString(mx, my, "EMPLOYMENT HISTORY")
    my -= 4
    c.setStrokeColor(ORANGE)
    c.line(mx, my, mx + mw, my)
    my -= 16

    jobs = [
        ("Operations & Logistics", "Bayou DeSiard Country Club", "2025"),
        ("Operations & Compliance Associate", "Little and Associates, LLC", "2020 \u2013 2025"),
        ("Sales Associate", "Office Depot", "2020"),
    ]
    for title, company, dates in jobs:
        c.setFont("Helvetica-Bold", 9.5)
        c.setFillColor(DARK_TEXT)
        line_text = f"{title}  |  "
        c.drawString(mx, my, line_text)
        tw = c.stringWidth(line_text, "Helvetica-Bold", 9.5)
        c.setFont("Helvetica-Oblique", 9.5)
        c.drawString(mx + tw, my, f"{company}")
        tw2 = c.stringWidth(f"{company}", "Helvetica-Oblique", 9.5)
        c.setFont("Helvetica", 9.5)
        c.drawString(mx + tw + tw2, my, f"  |  {dates}")
        my -= 16

    c.save()
    print(f"Resume PDF: {os.path.getsize(filepath):,} bytes")

    # ── Also make Word version with same structure ──
    make_resume_docx()


def make_resume_docx():
    from docx import Document
    from docx.shared import Pt, Inches, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement

    doc = Document()
    style = doc.styles['Normal']
    style.font.name = 'Calibri'
    style.font.size = Pt(10)
    for section in doc.sections:
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.6)
        section.right_margin = Inches(0.6)

    ORANGE_RGB = RGBColor(0xE8, 0x87, 0x2B)
    DARK_RGB = RGBColor(0x1A, 0x1A, 0x1A)

    def add_orange_line(doc):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        pPr = p._element.get_or_add_pPr()
        pBdr = OxmlElement('w:pBdr')
        bottom = OxmlElement('w:bottom')
        bottom.set(qn('w:val'), 'single')
        bottom.set(qn('w:sz'), '6')
        bottom.set(qn('w:space'), '1')
        bottom.set(qn('w:color'), 'E8872B')
        pBdr.append(bottom)
        pPr.append(pBdr)

    def section_header(doc, text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(text)
        run.font.size = Pt(12)
        run.bold = True
        run.font.color.rgb = DARK_RGB
        add_orange_line(doc)

    def subsection_header(doc, text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(text)
        run.font.size = Pt(10.5)
        run.bold = True
        run.font.color.rgb = DARK_RGB

    def add_bullet_text(doc, text):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.left_indent = Pt(18)
        run = p.add_run("\u2014  " + text)
        run.font.size = Pt(9.5)
        run.font.color.rgb = DARK_RGB

    # Name
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run("CHASE KINSLOW")
    run.font.size = Pt(24)
    run.bold = True
    run.font.color.rgb = DARK_RGB

    # Subtitle
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run("Operations & Facility Maintenance Professional")
    run.font.size = Pt(11)
    run.italic = True
    run.font.color.rgb = ORANGE_RGB

    # Contact line
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(8)
    run = p.add_run("(501) 707-7779  |  chasekn30@yahoo.com  |  Monroe, LA 71201")
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    # Professional Summary
    section_header(doc, "PROFESSIONAL SUMMARY")
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(
        "Dedicated operations professional with hands-on experience in facility maintenance, "
        "sanitation, logistics, and customer service. Background spans daily facility upkeep, "
        "equipment inspections, cleaning protocol execution, and cross-functional coordination "
        "to ensure safe, clean environments that exceed standards. Detail-oriented, organized, "
        "and proactive \u2014 equally comfortable washing and prepping vehicles, maintaining "
        "workspaces, or assisting customers with a professional, team-first approach."
    )
    run.font.size = Pt(9.5)

    # Key Achievements & Skills
    section_header(doc, "KEY ACHIEVEMENTS & SKILLS")

    subsection_header(doc, "Facility Operations, Maintenance & Inspections")
    for b in [
        "Performed rigorous opening and closing facility maintenance, applying systematic inspection protocols to ensure the physical environment exceeded brand standards, safety requirements, and cleanliness benchmarks",
        "Orchestrated daily equipment logistics and staging operations, managing rotation, maintenance tracking, and supply distribution to maintain 100% operational readiness",
        "Maintained clean, organized work environments through daily cleaning routines, supply restocking, and proactive identification of maintenance needs before they became issues",
    ]:
        add_bullet_text(doc, b)

    subsection_header(doc, "Customer Service, Sales & Operations")
    for b in [
        "Executed high-volume POS transactions with zero-error accuracy, managing daily cash handling and register reconciliation while delivering consultative customer service across multiple product categories",
        "Conducted walk-in consultations and product recommendations, closing sales by matching customer needs to available solutions directly applicable to guest service and occupancy-building initiatives",
        "Cross-trained across all departments to provide coverage wherever needed, ensuring uninterrupted service during peak periods and staff absences",
    ]:
        add_bullet_text(doc, b)

    subsection_header(doc, "Documentation, Compliance & Accuracy")
    for b in [
        "Managed comprehensive documentation workflows requiring zero-error precision \u2014 reconciliations, workpapers, and submissions where a single discrepancy disqualified an entire project file",
        "Directed inventory control using digital tracking systems to prevent shrink, maintain accurate stock levels, and ensure supplies were distributed across all operational areas",
        "Orchestrated monthly close procedures with rigorous reconciliation of accounts and records to maintain total data integrity across multiple client portfolios",
    ]:
        add_bullet_text(doc, b)

    # Employment History
    section_header(doc, "EMPLOYMENT HISTORY")

    jobs = [
        ("Operations & Logistics", "Bayou DeSiard Country Club", "2025"),
        ("Operations & Compliance Associate", "Little and Associates, LLC", "2020 \u2013 2025"),
        ("Sales Associate", "Office Depot", "2020"),
    ]
    for title, company, dates in jobs:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(f"{title}")
        run.bold = True
        run.font.size = Pt(9.5)
        run.font.color.rgb = DARK_RGB
        run = p.add_run(f"  |  ")
        run.font.size = Pt(9.5)
        run = p.add_run(f"{company}")
        run.italic = True
        run.font.size = Pt(9.5)
        run = p.add_run(f"  |  {dates}")
        run.font.size = Pt(9.5)

    # Core Competencies (at bottom or as keyword section)
    section_header(doc, "CORE COMPETENCIES")
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    comps = [
        "Vehicle Cleaning & Detailing", "Facility Sanitation & Maintenance",
        "Safety Inspections & Audits", "Equipment Operation & Care",
        "POS & Cash Handling", "Inventory Control",
        "Customer Service & Support", "Workspace Organization",
        "Compliance & Documentation", "Computer Proficiency",
    ]
    run = p.add_run("  \u2022  ".join(comps))
    run.font.size = Pt(9)

    filepath = os.path.join(OUT, "Chase_Kinslow_Resume.docx")
    doc.save(filepath)
    print(f"Resume DOCX: {os.path.getsize(filepath):,} bytes")


if __name__ == "__main__":
    make_resume()
    print("Done!")
