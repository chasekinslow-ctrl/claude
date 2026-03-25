"""
FINAL JPMorgan Chase Transactions Specialist II Application Materials
- Gray-blue sidebar resume format
- Correct work history (only first 3 jobs, Office Depot is CURRENT)
- Real credentials: J.D., CPA, Bar License
- Deeper research on Monroe operations (document custody, collateral review, vault mgmt)
- More insightful cold email hooks
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
import os

OUT = "/home/user/claude"

# ── Colors: gray-blue sidebar template ──
SIDEBAR_BG = HexColor("#8899A6")
SIDEBAR_HEADER = HexColor("#2A2A2A")
GOLD_LINE = HexColor("#C8A951")
GRAY_BAR = HexColor("#D8D8D8")
DARK_TEXT = HexColor("#1A1A1A")
SIDEBAR_TEXT = HexColor("#F0F0F0")
GRAY_CAPTION = HexColor("#555555")
PAGE_W, PAGE_H = letter
SIDEBAR_WIDTH = 2.0 * inch


# ═══════════════════════════════════════
# PDF HELPERS
# ═══════════════════════════════════════

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


# ═══════════════════════════════════════
# 1. RESUME PDF
# ═══════════════════════════════════════

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
        "Transaction Processing",
        "Document Handling & Data Entry",
        "Cash Handling & Reconciliation",
        "POS & Payment Systems",
        "Compliance & Regulatory Adherence",
        "Inventory Control & Tracking",
        "Customer Service & Inquiries",
        "Audit-Ready Record Keeping",
        "Problem Solving & Escalation",
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
        "Valid Driver's License \u2014 Clean MVR",
        "Reliable Personal Transportation",
        "Available for Extended Hours",
        "Advanced Excel Proficiency",
        "Microsoft Office Suite",
        "QuickBooks Desktop & Online",
        "NCR POS Systems",
        "Digital Inventory Tracking",
    ]:
        sy = draw_sidebar_arrow(c, item, sy)

    # ── MAIN CONTENT ──
    mx = SIDEBAR_WIDTH + 20
    mw = PAGE_W - mx - 28
    my = PAGE_H - 38

    c.setFont("Helvetica-Bold", 24); c.setFillColor(DARK_TEXT)
    c.drawString(mx, my, "CHASE KINSLOW"); my -= 16

    c.setFont("Helvetica", 9); c.setFillColor(GRAY_CAPTION)
    c.drawString(mx, my, "Transaction Processing & Operations Professional"); my -= 20

    # Professional Summary
    my = draw_main_section(c, "PROFESSIONAL SUMMARY", my, mx, mw)
    summary = (
        "Detail-oriented operations and compliance professional with a J.D., CPA license, and "
        "Bachelor of Accountancy. Proven track record processing high-volume transactions with "
        "zero-error accuracy, managing cash handling and daily register reconciliation, and "
        "maintaining audit-ready documentation under deadline pressure. Background combines "
        "rigorous financial compliance discipline with hands-on inventory control, customer "
        "service, and cross-departmental coordination. Local to Monroe, LA with reliable "
        "transportation and immediate availability."
    )
    my = draw_wrapped(c, summary, mx, my, mw); my -= 8

    # Key Achievements & Skills
    my = draw_main_section(c, "KEY ACHIEVEMENTS & SKILLS", my, mx, mw)

    my = draw_subsection_bar(c, "Transaction Processing, Cash Handling & Accuracy", my, mx, mw)
    for b in [
        "Operated POS systems and processed transactions with accuracy in a fast-paced retail environment, ensuring seamless customer service across high-traffic periods",
        "Managed cash handling procedures, daily register reconciliation, and sales reporting, reducing discrepancies by 15%",
        "Maintained inventory control systems and tracked stock levels, ensuring accurate record-keeping and reducing stockouts by 10%",
    ]:
        my = draw_bullet(c, b, mx, my, mw); my -= 2
    my -= 4

    my = draw_subsection_bar(c, "Documentation, Compliance & Reconciliation", my, mx, mw)
    for b in [
        "Developed proprietary parallel reconciliation models in Excel to track comprehensive project data sets, ensuring total eligible basis integrity by reconciling cumulative construction draws and recommending variance-correcting adjustments",
        "Managed comprehensive audit fieldwork \u2014 substantive testing, GAAP-compliant adjustments, final adjusted trial balances, and HUD-tailored supplemental schedules",
        "Co-administered end-to-end LIHTC application preparation, auditing project budgets for DSCR compliance and maximizing competitive scoring by optimizing FMR tiers and set-aside inputs",
    ]:
        my = draw_bullet(c, b, mx, my, mw); my -= 2
    my -= 4

    my = draw_subsection_bar(c, "Operations, Customer Service & Escalation", my, mx, mw)
    for b in [
        "Managed daily equipment inventory, tracked supply levels, and reported shortages, reducing service disruptions by 20%",
        "Coordinated across departments to fulfill member requests and resolve service issues, improving resolution time by 10%",
        "Maintained organized equipment rotation schedules and condition records with consistent attention to detail, ensuring operational efficiency",
    ]:
        my = draw_bullet(c, b, mx, my, mw); my -= 2
    my -= 8

    # Employment History
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


# ═══════════════════════════════════════
# 1b. RESUME DOCX
# ═══════════════════════════════════════

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
    r = p.add_run("Transaction Processing & Operations Professional"); r.font.size = Pt(9); r.font.color.rgb = G

    p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(8)
    r = p.add_run("(501) 707-7779  |  chasekn30@yahoo.com  |  Monroe, LA 71201"); r.font.size = Pt(8.5); r.font.color.rgb = G

    sec(doc, "PROFESSIONAL SUMMARY")
    p = doc.add_paragraph(); p.paragraph_format.space_after = Pt(4)
    r = p.add_run(
        "Detail-oriented operations and compliance professional with a J.D., CPA license, and "
        "Bachelor of Accountancy. Proven track record processing high-volume transactions with "
        "zero-error accuracy, managing cash handling and daily register reconciliation, and "
        "maintaining audit-ready documentation under deadline pressure. Background combines "
        "rigorous financial compliance discipline with hands-on inventory control, customer "
        "service, and cross-departmental coordination. Local to Monroe, LA with reliable "
        "transportation and immediate availability."
    ); r.font.size = Pt(9)

    sec(doc, "KEY ACHIEVEMENTS & SKILLS")

    subsec(doc, "Transaction Processing, Cash Handling & Accuracy")
    for b in [
        "Operated POS systems and processed transactions with accuracy in a fast-paced retail environment, ensuring seamless customer service across high-traffic periods",
        "Managed cash handling procedures, daily register reconciliation, and sales reporting, reducing discrepancies by 15%",
        "Maintained inventory control systems and tracked stock levels, ensuring accurate record-keeping and reducing stockouts by 10%",
    ]: bul(doc, b)

    subsec(doc, "Documentation, Compliance & Reconciliation")
    for b in [
        "Developed proprietary parallel reconciliation models in Excel to track comprehensive project data sets, ensuring total eligible basis integrity by reconciling cumulative construction draws and recommending variance-correcting adjustments",
        "Managed comprehensive audit fieldwork \u2014 substantive testing, GAAP-compliant adjustments, final adjusted trial balances, and HUD-tailored supplemental schedules",
        "Co-administered end-to-end LIHTC application preparation, auditing project budgets for DSCR compliance and maximizing competitive scoring by optimizing FMR tiers and set-aside inputs",
    ]: bul(doc, b)

    subsec(doc, "Operations, Customer Service & Escalation")
    for b in [
        "Managed daily equipment inventory, tracked supply levels, and reported shortages, reducing service disruptions by 20%",
        "Coordinated across departments to fulfill member requests and resolve service issues, improving resolution time by 10%",
        "Maintained organized equipment rotation schedules and condition records with consistent attention to detail, ensuring operational efficiency",
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


# ═══════════════════════════════════════
# 2. COVER LETTER
# ═══════════════════════════════════════

COVER_LETTER = """Chase Kinslow
Monroe, LA 71201
(501) 707-7779 | chasekn30@yahoo.com

March 25, 2026

JPMorgan Chase & Co.
Hiring Manager \u2014 Transactions Specialist II
Monroe, LA

Dear Hiring Manager,

I am writing to apply for the Transactions Specialist II position at the Monroe Operations Center. With a CPA license, a J.D., a Bachelor of Accountancy, and direct experience processing high-volume transactions, managing daily cash reconciliation, and maintaining audit-ready documentation in deadline-driven environments, I can contribute to your collateral review and document custody operations immediately.

I currently work as a Sales Associate at Office Depot, where I operate POS systems processing transactions all day with zero-error accuracy, manage daily register reconciliation and cash handling, and maintain inventory control systems that reduced stockouts by 10% and discrepancies by 15%. Before that, I spent three years as an Accountant at Little and Associates, LLC, where I developed parallel reconciliation models in Excel, managed comprehensive LIHTC audit fieldwork including GAAP-compliant adjustments and HUD-tailored supplemental schedules, and co-administered end-to-end compliance application preparation where a single discrepancy could disqualify an entire project file.

That combination \u2014 transaction processing speed and accuracy from retail, plus the documentation rigor and compliance discipline from public accounting \u2014 maps directly to what this role requires: processing and clearing transactions on time, handling customer inquiries, maintaining production and quality standards, and escalating non-routine issues with good judgment.

I understand the Monroe campus serves as a hub for global document custody and collateral review across home loans, auto loans, and securities, with the new Ruston Operations Center expanding that capacity. I want to be part of that operation. I am also eager to develop proficiency with the AI and automation tools JPMorgan Chase is deploying \u2014 including the LLM Suite that won American Banker\u2019s 2025 Innovation of the Year \u2014 and contribute to process optimization efforts as the firm scales toward 1,000+ AI use cases.

I am local, available immediately, and comfortable with the physical requirements of the role. I would welcome the chance to discuss how my background fits your team.

Thank you for your consideration.

Sincerely,
Chase Kinslow"""


def make_cover_letter_pdf():
    fp = os.path.join(OUT, "Chase_Kinslow_CoverLetter_JPMorganChase.pdf")
    c = canvas.Canvas(fp, pagesize=letter)
    x, y = 72, PAGE_H - 72; mw = PAGE_W - 144

    def wl(text, font="Helvetica", size=10.5, spacing=14, color=DARK_TEXT):
        nonlocal y
        c.setFont(font, size); c.setFillColor(color)
        if not text.strip(): y -= spacing; return
        for line in simpleSplit(text, font, size, mw):
            c.drawString(x, y, line); y -= spacing

    wl("Chase Kinslow", "Helvetica-Bold", 14, 16)
    wl("Monroe, LA 71201", "Helvetica", 9.5, 13, GRAY_CAPTION)
    wl("(501) 707-7779  |  chasekn30@yahoo.com", "Helvetica", 9.5, 13, GRAY_CAPTION)
    y -= 16
    wl("March 25, 2026"); y -= 8
    wl("JPMorgan Chase & Co.")
    wl("Hiring Manager \u2014 Transactions Specialist II")
    wl("Monroe, LA"); y -= 8
    wl("Dear Hiring Manager,"); y -= 4

    paragraphs = [
        "I am writing to apply for the Transactions Specialist II position at the Monroe Operations Center. With a CPA license, a J.D., a Bachelor of Accountancy, and direct experience processing high-volume transactions, managing daily cash reconciliation, and maintaining audit-ready documentation in deadline-driven environments, I can contribute to your collateral review and document custody operations immediately.",

        "I currently work as a Sales Associate at Office Depot, where I operate POS systems processing transactions all day with zero-error accuracy, manage daily register reconciliation and cash handling, and maintain inventory control systems that reduced stockouts by 10% and discrepancies by 15%. Before that, I spent three years as an Accountant at Little and Associates, LLC, where I developed parallel reconciliation models in Excel, managed comprehensive LIHTC audit fieldwork including GAAP-compliant adjustments and HUD-tailored supplemental schedules, and co-administered end-to-end compliance application preparation where a single discrepancy could disqualify an entire project file.",

        "That combination \u2014 transaction processing speed and accuracy from retail, plus the documentation rigor and compliance discipline from public accounting \u2014 maps directly to what this role requires: processing and clearing transactions on time, handling customer inquiries, maintaining production and quality standards, and escalating non-routine issues with good judgment.",

        "I understand the Monroe campus serves as a hub for global document custody and collateral review across home loans, auto loans, and securities, with the new Ruston Operations Center expanding that capacity. I want to be part of that operation. I am also eager to develop proficiency with the AI and automation tools JPMorgan Chase is deploying \u2014 including the LLM Suite that won American Banker\u2019s 2025 Innovation of the Year \u2014 and contribute to process optimization efforts as the firm scales toward 1,000+ AI use cases.",

        "I am local, available immediately, and comfortable with the physical requirements of the role. I would welcome the chance to discuss how my background fits your team.",

        "Thank you for your consideration.",
    ]
    for para in paragraphs:
        wl(para); y -= 6
    y -= 4
    wl("Sincerely,")
    wl("Chase Kinslow", "Helvetica-Bold", 10.5)

    c.save()
    print(f"Cover Letter PDF: {fp} ({os.path.getsize(fp):,} bytes)")


def make_cover_letter_docx():
    from docx import Document
    from docx.shared import Pt, Inches

    doc = Document()
    style = doc.styles['Normal']; style.font.name = 'Calibri'; style.font.size = Pt(10.5)
    for s in doc.sections:
        s.top_margin = Inches(1); s.bottom_margin = Inches(1)
        s.left_margin = Inches(1); s.right_margin = Inches(1)

    for line in COVER_LETTER.strip().split('\n'):
        p = doc.add_paragraph(line)
        p.paragraph_format.space_after = Pt(2)
        if line == "Chase Kinslow" or (line.startswith("Chase Kinslow") and "Monroe" not in line and "|" not in line):
            if p.runs:
                p.runs[0].bold = True; p.runs[0].font.size = Pt(14)

    fp = os.path.join(OUT, "Chase_Kinslow_CoverLetter_JPMorganChase.docx")
    doc.save(fp)
    print(f"Cover Letter DOCX: {fp} ({os.path.getsize(fp):,} bytes)")


# ═══════════════════════════════════════
# 3. COLD EMAIL TO STEVE ROOP
# ═══════════════════════════════════════

EMAIL_TEXT = """Subject: Congratulations on Business Leader of the Year \u2014 and a Question About the Monroe Operations Team

Mr. Roop,

Congratulations on being named the Greater Shreveport Chamber\u2019s 2025 Business Leader of the Year. After 40+ years in financial services and the kind of civic investment you\u2019ve made across North Louisiana \u2014 from the Ark-La-Tex Air Service Alliance Board to your Honorary Commander role with the 307th Bomb Wing at Barksdale \u2014 that recognition is well earned. I also saw you shared JPMorgan\u2019s $1.5 trillion Security and Resiliency Initiative announcement. It\u2019s exciting to see the firm making that level of commitment to the industries that matter most.

I\u2019m reaching out because I live in Monroe and recently applied for the Transactions Specialist II position at the Monroe Operations Center. I wanted to introduce myself directly to the person who leads this market.

A bit about me: I have a Bachelor of Accountancy from Ole Miss, a CPA license in Arkansas and Louisiana, and a J.D. from the University of Arkansas. I currently work at Office Depot, where I process high-volume transactions on POS systems every day, manage daily register reconciliation and cash handling, and maintain inventory control systems \u2014 I reduced discrepancies by 15% and stockouts by 10%. Before that, I spent three years at an accounting firm managing LIHTC audit fieldwork, building Excel reconciliation models, and handling compliance documentation where zero-error precision was non-negotiable. A single discrepancy could disqualify an entire project file.

I know the Monroe campus runs global document custody and collateral review operations for home loans, auto loans, and securities \u2014 and with the new $31 million Ruston facility now open as a vault and operations extension, it\u2019s clear Chase is scaling that capacity. I want to be part of it. The combination of transaction processing speed from retail and documentation rigor from public accounting is exactly what collateral review and custody operations demand, and I\u2019m ready to contribute from day one.

If there\u2019s someone specific on the Monroe operations team you\u2019d suggest I connect with, I\u2019d be grateful for the introduction. I\u2019ve attached my resume for reference.

Thank you for your time and for everything you do for North Louisiana.

Respectfully,
Chase Kinslow
(501) 707-7779
chasekn30@yahoo.com
Monroe, LA 71201"""


def write_email():
    fp = os.path.join(OUT, "Cold_Email_Steve_Roop.txt")
    with open(fp, 'w') as f:
        f.write(EMAIL_TEXT.strip())
    print(f"Email: {fp} ({os.path.getsize(fp):,} bytes)")


# ═══════════════════════════════════════
# MAIN
# ═══════════════════════════════════════

if __name__ == "__main__":
    make_resume_pdf()
    make_resume_docx()
    make_cover_letter_pdf()
    make_cover_letter_docx()
    write_email()
    print("\nAll materials generated!")
