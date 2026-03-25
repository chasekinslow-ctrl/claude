"""
Cover letter + cold email for JPMorgan Chase Transactions Specialist II.
Updated: Bayou DeSiard is a PAST role, not current.
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
import os

OUT = "/home/user/claude"
DARK_TEXT = HexColor("#1A1A1A")
PAGE_W, PAGE_H = letter

COVER_LETTER = """Chase Kinslow
Monroe, LA 71201
(501) 707-7779 | chasekn30@yahoo.com

March 25, 2026

JPMorgan Chase & Co.
Hiring Manager — Transactions Specialist II
Monroe, LA

Dear Hiring Manager,

I am writing to apply for the Transactions Specialist II position at JPMorgan Chase in Monroe. With a Bachelor of Accountancy from the University of Mississippi, a CPA license in Arkansas and Louisiana, and direct experience processing high-volume transactions, managing zero-error documentation workflows, and maintaining compliance in deadline-driven environments, I am ready to contribute to your operations team immediately.

At Little and Associates, LLC, I spent three years managing reconciliations, workpapers, and client submissions where zero-error precision was non-negotiable — a single discrepancy could disqualify an entire project file. I ran monthly close procedures across multiple client portfolios, directed inventory tracking to maintain accurate records, and built the kind of disciplined, systematic work habits that transaction processing demands. At Bayou DeSiard Country Club, I managed daily operations and logistics — equipment rotation, supply distribution, cross-departmental coordination — all under production pressure with no room for error.

That combination of accounting rigor and operational execution is exactly what this role requires: processing and clearing transactions accurately, handling customer inquiries, escalating non-routine issues with good judgment, and maintaining compliance with internal procedures and industry regulations.

What draws me to this role specifically is Chase's deep investment in North Louisiana. Nearly 1,000 employees at the Monroe campus and the recent opening of the $31 million Ruston Operations Center make it clear this is a company building something long-term here. I want to be part of that. I am also eager to develop proficiency with the AI and automation tools JPMorgan Chase is deploying across transaction processing — the JD mentions this as a key capability, and I am excited to grow in that direction.

I am local, available immediately, and comfortable with the physical requirements of the role. I would welcome the chance to discuss how my background fits your team's needs.

Thank you for your consideration.

Sincerely,
Chase Kinslow"""


EMAIL_TEXT = """Subject: Congratulations on Business Leader of the Year — and a Question About Your Monroe Team

Mr. Roop,

First, congratulations on being named the Greater Shreveport Chamber's 2025 Business Leader of the Year. That recognition — after 40+ years of leadership in financial services and the kind of civic investment you've made across North Louisiana, from the Ark-La-Tex Air Service Alliance to your Honorary Commander role with the 307th Bomb Wing — is well deserved.

I'm reaching out because I live in Monroe and recently applied for the Transactions Specialist II position at the Monroe Operations Center. I wanted to introduce myself directly.

I have a Bachelor of Accountancy from Ole Miss and a CPA license in Arkansas and Louisiana. I spent three years at an accounting firm managing zero-error reconciliations, workpapers, and client submissions where a single discrepancy could disqualify an entire project file. Most recently I ran daily operations and logistics at Bayou DeSiard Country Club — equipment rotation, supply coordination, cross-departmental problem-solving under production pressure. That combination of accounting precision and operational execution is exactly what your transaction processing team needs.

What excites me most about this opportunity is Chase's long-term commitment to North Louisiana. Nearly 1,000 employees at the Monroe campus, the new $31 million Ruston Operations Center now open and growing toward 200 jobs — this isn't a company passing through. I want to build a career here, contribute to the team's production and accuracy standards, and grow with the operation as JPMorgan Chase continues to invest in this region.

I've attached my resume for your reference. If there's someone specific on the Monroe operations team you'd recommend I connect with, I'd be grateful for the introduction. Either way, thank you for your time and for everything you do for this community.

Respectfully,
Chase Kinslow
(501) 707-7779
chasekn30@yahoo.com
Monroe, LA 71201"""


def make_cover_letter_pdf():
    filepath = os.path.join(OUT, "Chase_Kinslow_CoverLetter_JPMorganChase.pdf")
    c = canvas.Canvas(filepath, pagesize=letter)
    x, y = 72, PAGE_H - 72
    mw = PAGE_W - 144

    def wl(text, font="Helvetica", size=10.5, spacing=14, color=DARK_TEXT):
        nonlocal y
        c.setFont(font, size); c.setFillColor(color)
        if not text.strip():
            y -= spacing; return
        for line in simpleSplit(text, font, size, mw):
            c.drawString(x, y, line); y -= spacing

    wl("Chase Kinslow", "Helvetica-Bold", 14, 16)
    wl("Monroe, LA 71201", "Helvetica", 9.5, 13, HexColor("#555555"))
    wl("(501) 707-7779  |  chasekn30@yahoo.com", "Helvetica", 9.5, 13, HexColor("#555555"))
    y -= 16
    wl("March 25, 2026"); y -= 8
    wl("JPMorgan Chase & Co.")
    wl("Hiring Manager \u2014 Transactions Specialist II")
    wl("Monroe, LA"); y -= 8
    wl("Dear Hiring Manager,"); y -= 4

    paragraphs = [
        "I am writing to apply for the Transactions Specialist II position at JPMorgan Chase in Monroe. With a Bachelor of Accountancy from the University of Mississippi, a CPA license in Arkansas and Louisiana, and direct experience processing high-volume transactions, managing zero-error documentation workflows, and maintaining compliance in deadline-driven environments, I am ready to contribute to your operations team immediately.",

        "At Little and Associates, LLC, I spent three years managing reconciliations, workpapers, and client submissions where zero-error precision was non-negotiable \u2014 a single discrepancy could disqualify an entire project file. I ran monthly close procedures across multiple client portfolios, directed inventory tracking to maintain accurate records, and built the kind of disciplined, systematic work habits that transaction processing demands. At Bayou DeSiard Country Club, I managed daily operations and logistics \u2014 equipment rotation, supply distribution, cross-departmental coordination \u2014 all under production pressure with no room for error.",

        "That combination of accounting rigor and operational execution is exactly what this role requires: processing and clearing transactions accurately, handling customer inquiries, escalating non-routine issues with good judgment, and maintaining compliance with internal procedures and industry regulations.",

        "What draws me to this role specifically is Chase\u2019s deep investment in North Louisiana. Nearly 1,000 employees at the Monroe campus and the recent opening of the $31 million Ruston Operations Center make it clear this is a company building something long-term here. I want to be part of that. I am also eager to develop proficiency with the AI and automation tools JPMorgan Chase is deploying across transaction processing \u2014 the JD mentions this as a key capability, and I am excited to grow in that direction.",

        "I am local, available immediately, and comfortable with the physical requirements of the role. I would welcome the chance to discuss how my background fits your team\u2019s needs.",

        "Thank you for your consideration.",
    ]
    for para in paragraphs:
        wl(para); y -= 6

    y -= 4
    wl("Sincerely,")
    wl("Chase Kinslow", "Helvetica-Bold", 10.5)

    c.save()
    print(f"Cover Letter PDF: {filepath} ({os.path.getsize(filepath):,} bytes)")


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
        if line == "Chase Kinslow":
            p.runs[0].bold = True; p.runs[0].font.size = Pt(14)

    fp = os.path.join(OUT, "Chase_Kinslow_CoverLetter_JPMorganChase.docx")
    doc.save(fp)
    print(f"Cover Letter DOCX: {fp} ({os.path.getsize(fp):,} bytes)")


def write_email():
    fp = os.path.join(OUT, "Cold_Email_Steve_Roop.txt")
    with open(fp, 'w') as f:
        f.write(EMAIL_TEXT.strip())
    print(f"Email: {fp} ({os.path.getsize(fp):,} bytes)")


if __name__ == "__main__":
    make_cover_letter_pdf()
    make_cover_letter_docx()
    write_email()
    print("Done!")
