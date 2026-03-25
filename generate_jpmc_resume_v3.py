"""
FINAL v3 — JPMorgan Chase Transactions Specialist II
Restructured to lead with compliance/reconciliation strength, not retail.
Monroe campus = collateral review, document custody, vault management for
home loans, auto loans, securities. Lead with what matches THAT.
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
import os

OUT = "/home/user/claude"

SIDEBAR_BG = HexColor("#8899A6")
SIDEBAR_HEADER = HexColor("#2A2A2A")
GOLD_LINE = HexColor("#C8A951")
GRAY_BAR = HexColor("#D8D8D8")
DARK_TEXT = HexColor("#1A1A1A")
SIDEBAR_TEXT = HexColor("#F0F0F0")
GRAY_CAPTION = HexColor("#555555")
PAGE_W, PAGE_H = letter
SIDEBAR_WIDTH = 2.0 * inch


def draw_sidebar_bg(c):
    c.setFillColor(SIDEBAR_BG)
    c.rect(0, 0, SIDEBAR_WIDTH, PAGE_H, fill=1, stroke=0)

def draw_sidebar_section(c, title, y):
    c.setFillColor(SIDEBAR_HEADER); c.setFont("Helvetica-Bold", 8)
    c.drawString(14, y, "   ".join(list(title)))
    return y - 14

def draw_sidebar_item(c, text, y, bold=False):
    c.setFillColor(SIDEBAR_TEXT)
    font = "Helvetica-Bold" if bold else "Helvetica"
    c.setFont(font, 7.5)
    for line in simpleSplit(text, font, 7.5, SIDEBAR_WIDTH - 28):
        c.drawString(16, y, line); y -= 11
    return y

def draw_sidebar_arrow(c, text, y):
    c.setFillColor(SIDEBAR_TEXT); c.setFont("Helvetica", 7.5)
    lines = simpleSplit(text, "Helvetica", 7.5, SIDEBAR_WIDTH - 36)
    for i, line in enumerate(lines):
        c.drawString(16 if i == 0 else 26, y, ("\u00BB " + line) if i == 0 else line); y -= 11
    return y

def draw_main_section(c, title, y, mx, mw):
    c.setFont("Helvetica-Bold", 11); c.setFillColor(DARK_TEXT)
    c.drawString(mx, y, title); y -= 4
    c.setStrokeColor(GOLD_LINE); c.setLineWidth(1.5)
    c.line(mx, y, mx + mw, y)
    return y - 12

def draw_subsection_bar(c, title, y, mx, mw):
    c.setFillColor(GRAY_BAR)
    c.rect(mx - 4, y - 3, mw + 8, 14, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 9); c.setFillColor(DARK_TEXT)
    c.drawString(mx, y, title)
    return y - 16

def draw_bullet(c, text, x, y, max_width):
    c.setFillColor(DARK_TEXT); c.setFont("Helvetica", 8.5)
    c.drawString(x, y, "\u2022")
    text_x = x + 10
    lines = simpleSplit(text, "Helvetica", 8.5, max_width - 10)
    for i, line in enumerate(lines):
        if y < 40: c.showPage(); y = PAGE_H - 40; draw_sidebar_bg(c)
        c.setFont("Helvetica", 8.5); c.setFillColor(DARK_TEXT)
        c.drawString(text_x if i == 0 else text_x + 4, y, line); y -= 12
    return y

def draw_wrapped(c, text, x, y, max_width, font="Helvetica", size=8.5, leading=12, color=DARK_TEXT):
    c.setFont(font, size); c.setFillColor(color)
    for line in simpleSplit(text, font, size, max_width):
        if y < 40: c.showPage(); y = PAGE_H - 40; draw_sidebar_bg(c)
        c.setFont(font, size); c.setFillColor(color)
        c.drawString(x, y, line); y -= leading
    return y


def make_resume_pdf():
    fp = os.path.join(OUT, "Chase_Kinslow_Resume_JPMorganChase.pdf")
    c = canvas.Canvas(fp, pagesize=letter)
    draw_sidebar_bg(c)

    # ── SIDEBAR ──
    sy = PAGE_H - 40

    sy = draw_sidebar_section(c, "CONTACT", sy)
    sy = draw_sidebar_item(c, "(501) 707-7779", sy)
    sy = draw_sidebar_item(c, "chasekn30@yahoo.com", sy)
    sy = draw_sidebar_item(c, "Monroe, LA 71201", sy)
    sy -= 10

    sy = draw_sidebar_section(c, "CORE COMPETENCIES", sy)
    for comp in [
        "Collateral Document Review",
        "Regulatory Compliance & Auditing",
        "Reconciliation & Data Integrity",
        "Transaction Processing & Clearing",
        "Production & Quality Standards",
        "Customer Inquiry Resolution",
        "Issue Escalation & Judgment",
        "Process Optimization",
        "Agency/Investor Guidelines",
    ]:
        sy = draw_sidebar_arrow(c, comp, sy)
    sy -= 10

    sy = draw_sidebar_section(c, "CREDENTIALS", sy)
    sy = draw_sidebar_item(c, "Licensed CPA", sy, bold=True)
    sy = draw_sidebar_item(c, "Arkansas & Louisiana", sy)
    sy -= 4
    sy = draw_sidebar_item(c, "Arkansas Bar License", sy, bold=True)
    sy -= 10

    sy = draw_sidebar_section(c, "EDUCATION", sy)
    sy = draw_sidebar_item(c, "Juris Doctor (J.D.)", sy, bold=True)
    sy = draw_sidebar_item(c, "University of Arkansas", sy)
    sy -= 4
    sy = draw_sidebar_item(c, "Bachelor of Accountancy", sy, bold=True)
    sy = draw_sidebar_item(c, "University of Mississippi", sy)
    sy -= 10

    sy = draw_sidebar_section(c, "ADDITIONAL", sy)
    for item in [
        "GAAP, HUD & LIHTC Compliance",
        "Advanced Excel & Financial Modeling",
        "QuickBooks Desktop & Online",
        "POS Systems & Cash Management",
        "Digital Inventory Tracking",
        "Microsoft Office Suite",
        "ADP Workforce Now",
        "Available for Extended Hours",
    ]:
        sy = draw_sidebar_arrow(c, item, sy)

    # ── MAIN CONTENT ──
    mx = SIDEBAR_WIDTH + 20
    mw = PAGE_W - mx - 28
    my = PAGE_H - 38

    c.setFont("Helvetica-Bold", 24); c.setFillColor(DARK_TEXT)
    c.drawString(mx, my, "CHASE KINSLOW"); my -= 16

    c.setFont("Helvetica", 9); c.setFillColor(GRAY_CAPTION)
    c.drawString(mx, my, "Compliance & Transaction Processing Professional"); my -= 20

    # ── PROFESSIONAL SUMMARY ──
    my = draw_main_section(c, "PROFESSIONAL SUMMARY", my, mx, mw)
    summary = (
        "CPA-licensed compliance and operations professional with a Juris Doctor, Bachelor of "
        "Accountancy, and three years of experience managing audit-ready documentation, financial "
        "reconciliations, and regulatory submissions in environments where a single error could "
        "disqualify an entire file. Proven track record building reconciliation models, executing "
        "GAAP-compliant audit fieldwork, and maintaining zero-error production standards across "
        "high-volume transaction processing. Combines the document precision required for collateral "
        "review and custody operations with hands-on experience in daily cash reconciliation, "
        "inventory tracking, and cross-departmental coordination."
    )
    my = draw_wrapped(c, summary, mx, my, mw); my -= 8

    # ── KEY ACHIEVEMENTS & SKILLS ──
    my = draw_main_section(c, "KEY ACHIEVEMENTS & SKILLS", my, mx, mw)

    # LEAD: Compliance, Reconciliation & Document Review (Little & Associates)
    my = draw_subsection_bar(c, "Compliance, Reconciliation & Document Review", my, mx, mw)
    for b in [
        "Developed proprietary parallel reconciliation models in Excel to track comprehensive project data sets, ensuring total eligible basis integrity by reconciling cumulative construction draws and recommending variance-correcting adjustments for Final Cost Certifications",
        "Managed comprehensive LIHTC audit fieldwork \u2014 substantive testing, GAAP-compliant adjustments, final adjusted trial balances, and HUD-tailored supplemental schedules requiring zero-error precision across multiple client portfolios",
        "Co-administered end-to-end regulatory application preparation, auditing project budgets for DSCR compliance through Year 15 and maximizing competitive scoring by optimizing FMR tiers, flood mitigation, and set-aside inputs",
    ]:
        my = draw_bullet(c, b, mx, my, mw); my -= 2
    my -= 4

    # SECOND: Transaction Processing & Production Standards (Office Depot)
    my = draw_subsection_bar(c, "Transaction Processing & Production Standards", my, mx, mw)
    for b in [
        "Process high-volume transactions daily on POS systems with zero-error accuracy, managing cash handling, register reconciliation, and payment processing across a fast-paced retail operation",
        "Reduced cash-handling discrepancies by 15% through disciplined daily reconciliation procedures and adherence to standard operating protocols",
        "Maintained inventory control systems using digital tracking, reducing stockouts by 10% and ensuring accurate record-keeping across all product categories",
    ]:
        my = draw_bullet(c, b, mx, my, mw); my -= 2
    my -= 4

    # THIRD: Operations, Escalation & Coordination (Bayou DeSiard)
    my = draw_subsection_bar(c, "Operations Coordination & Issue Resolution", my, mx, mw)
    for b in [
        "Managed daily equipment logistics, tracked supply levels, and reported shortages to management, reducing service disruptions by 20% through proactive escalation",
        "Coordinated across departments to fulfill member requests and resolve non-routine service issues, improving resolution time by 10%",
        "Maintained organized operational records, equipment rotation schedules, and condition documentation with consistent attention to detail and accuracy",
    ]:
        my = draw_bullet(c, b, mx, my, mw); my -= 2
    my -= 8

    # ── EMPLOYMENT HISTORY ──
    my = draw_main_section(c, "EMPLOYMENT HISTORY", my, mx, mw)
    for title, company, dates in [
        ("Operations & Logistics", "Bayou DeSiard Country Club", "2025"),
        ("Accountant", "Little and Associates, LLC", "2020 \u2013 2023"),
        ("Sales Associate", "Office Depot", "2020 \u2013 Present"),
    ]:
        c.setFont("Helvetica-Bold", 8.5); c.setFillColor(DARK_TEXT)
        c.drawString(mx, my, title)
        tw = c.stringWidth(title, "Helvetica-Bold", 8.5)
        c.setFont("Helvetica-Oblique", 8.5); c.setFillColor(GRAY_CAPTION)
        c.drawString(mx + tw, my, f" | {company}")
        c.setFont("Helvetica", 8.5)
        dw = c.stringWidth(dates, "Helvetica", 8.5)
        c.drawString(mx + mw - dw, my, dates)
        my -= 14

    c.save()
    print(f"Resume PDF: {fp} ({os.path.getsize(fp):,} bytes)")


def make_resume_docx():
    from docx import Document
    from docx.shared import Pt, Inches, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement

    doc = Document()
    style = doc.styles['Normal']; style.font.name = 'Calibri'; style.font.size = Pt(10)
    for s in doc.sections:
        s.top_margin = Inches(0.5); s.bottom_margin = Inches(0.5)
        s.left_margin = Inches(0.6); s.right_margin = Inches(0.6)

    D = RGBColor(0x1A, 0x1A, 0x1A); G = RGBColor(0x55, 0x55, 0x55)

    def gold_line(doc):
        p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(4)
        pPr = p._element.get_or_add_pPr(); pBdr = OxmlElement('w:pBdr')
        b = OxmlElement('w:bottom'); b.set(qn('w:val'), 'single'); b.set(qn('w:sz'), '6')
        b.set(qn('w:space'), '1'); b.set(qn('w:color'), 'C8A951')
        pBdr.append(b); pPr.append(pBdr)

    def sec(doc, t):
        p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(10); p.paragraph_format.space_after = Pt(0)
        r = p.add_run(t); r.font.size = Pt(11); r.bold = True; r.font.color.rgb = D; gold_line(doc)

    def subsec(doc, t):
        p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(6); p.paragraph_format.space_after = Pt(2)
        pPr = p._element.get_or_add_pPr()
        shd = OxmlElement('w:shd'); shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto'); shd.set(qn('w:fill'), 'D8D8D8')
        pPr.append(shd)
        r = p.add_run(t); r.font.size = Pt(9.5); r.bold = True; r.font.color.rgb = D

    def bul(doc, t):
        p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(2); p.paragraph_format.left_indent = Pt(18)
        r = p.add_run("\u2022  " + t); r.font.size = Pt(9); r.font.color.rgb = D

    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.LEFT; p.paragraph_format.space_after = Pt(0)
    r = p.add_run("CHASE KINSLOW"); r.font.size = Pt(22); r.bold = True; r.font.color.rgb = D

    p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(2)
    r = p.add_run("Compliance & Transaction Processing Professional"); r.font.size = Pt(9); r.font.color.rgb = G

    p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(8)
    r = p.add_run("(501) 707-7779  |  chasekn30@yahoo.com  |  Monroe, LA 71201"); r.font.size = Pt(8.5); r.font.color.rgb = G

    sec(doc, "PROFESSIONAL SUMMARY")
    p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(4)
    r = p.add_run(
        "CPA-licensed compliance and operations professional with a Juris Doctor, Bachelor of "
        "Accountancy, and three years of experience managing audit-ready documentation, financial "
        "reconciliations, and regulatory submissions in environments where a single error could "
        "disqualify an entire file. Proven track record building reconciliation models, executing "
        "GAAP-compliant audit fieldwork, and maintaining zero-error production standards across "
        "high-volume transaction processing. Combines the document precision required for collateral "
        "review and custody operations with hands-on experience in daily cash reconciliation, "
        "inventory tracking, and cross-departmental coordination."
    ); r.font.size = Pt(9)

    sec(doc, "KEY ACHIEVEMENTS & SKILLS")

    subsec(doc, "Compliance, Reconciliation & Document Review")
    for b in [
        "Developed proprietary parallel reconciliation models in Excel to track comprehensive project data sets, ensuring total eligible basis integrity by reconciling cumulative construction draws and recommending variance-correcting adjustments for Final Cost Certifications",
        "Managed comprehensive LIHTC audit fieldwork \u2014 substantive testing, GAAP-compliant adjustments, final adjusted trial balances, and HUD-tailored supplemental schedules requiring zero-error precision across multiple client portfolios",
        "Co-administered end-to-end regulatory application preparation, auditing project budgets for DSCR compliance through Year 15 and maximizing competitive scoring by optimizing FMR tiers, flood mitigation, and set-aside inputs",
    ]: bul(doc, b)

    subsec(doc, "Transaction Processing & Production Standards")
    for b in [
        "Process high-volume transactions daily on POS systems with zero-error accuracy, managing cash handling, register reconciliation, and payment processing across a fast-paced retail operation",
        "Reduced cash-handling discrepancies by 15% through disciplined daily reconciliation procedures and adherence to standard operating protocols",
        "Maintained inventory control systems using digital tracking, reducing stockouts by 10% and ensuring accurate record-keeping across all product categories",
    ]: bul(doc, b)

    subsec(doc, "Operations Coordination & Issue Resolution")
    for b in [
        "Managed daily equipment logistics, tracked supply levels, and reported shortages to management, reducing service disruptions by 20% through proactive escalation",
        "Coordinated across departments to fulfill member requests and resolve non-routine service issues, improving resolution time by 10%",
        "Maintained organized operational records, equipment rotation schedules, and condition documentation with consistent attention to detail and accuracy",
    ]: bul(doc, b)

    sec(doc, "EMPLOYMENT HISTORY")
    for title, company, dates in [
        ("Operations & Logistics", "Bayou DeSiard Country Club", "2025"),
        ("Accountant", "Little and Associates, LLC", "2020 \u2013 2023"),
        ("Sales Associate", "Office Depot", "2020 \u2013 Present"),
    ]:
        p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(2)
        r = p.add_run(title); r.bold = True; r.font.size = Pt(9); r.font.color.rgb = D
        r = p.add_run(f" | {company}"); r.font.size = Pt(9); r.font.color.rgb = G
        r = p.add_run(f"    {dates}"); r.font.size = Pt(9); r.font.color.rgb = G

    sec(doc, "CREDENTIALS & EDUCATION")
    p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(4)
    r = p.add_run("Licensed CPA (Arkansas & Louisiana)  \u2022  Arkansas Bar License  \u2022  J.D., University of Arkansas  \u2022  B.Accy., University of Mississippi")
    r.font.size = Pt(8.5)

    fp2 = os.path.join(OUT, "Chase_Kinslow_Resume_JPMorganChase.docx")
    doc.save(fp2)
    print(f"Resume DOCX: {fp2} ({os.path.getsize(fp2):,} bytes)")


if __name__ == "__main__":
    make_resume_pdf()
    make_resume_docx()
    print("Done!")
