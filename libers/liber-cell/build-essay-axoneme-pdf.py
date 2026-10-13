#!/usr/bin/env python3
"""Build the PDF twin of the axoneme-pattern essay (fpdf2, DejaVu Sans)."""
import re
from fpdf import FPDF

SRC = "/home/hatch/workspace/your_files/axoneme-essay/essay-axoneme-pattern.md"
OUT = "/home/hatch/workspace/your_files/axoneme-essay/essay-axoneme-pattern.pdf"

def clean(t):
    t = t.replace("❌", "✗").replace("✅", "✓").replace("🔬", "")
    return t

pdf = FPDF(orientation="P", unit="mm", format="A4")
pdf.set_auto_page_break(True, margin=22)
pdf.add_font("dejavu", "", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
pdf.add_font("dejavu", "B", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
pdf.add_font("dejavu", "I", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")  # no oblique file; reuse

W = pdf.w - pdf.l_margin - pdf.r_margin

def para(text, size=10.5, style="", align="L", space_after=4, color=(0,0,0), indent=0):
    pdf.set_font("dejavu", style if style in ("", "B") else "", size)
    pdf.set_text_color(*color)
    x0 = pdf.l_margin + indent
    pdf.set_x(x0)
    try:
        pdf.multi_cell(W - indent, 6, clean(text), markdown=True, align=align,
                       new_x="LMARGIN", new_y="NEXT")
    except Exception:
        pdf.multi_cell(W - indent, 6, clean(text), align=align,
                       new_x="LMARGIN", new_y="NEXT")
    pdf.ln(space_after)

lines = open(SRC).read().split("\n")
pdf.add_page()
i = 0
while i < len(lines):
    ln = lines[i].rstrip()
    if not ln.strip():
        pdf.ln(3); i += 1; continue
    if ln.startswith("# "):
        para(ln[2:], size=20, style="B", align="C", space_after=6)
    elif ln.startswith("## "):
        pdf.ln(4)
        para(ln[3:], size=14, style="B", space_after=4)
    elif ln.startswith("> "):
        # blockquote: gather consecutive quote lines, strip emphasis markers
        qs = []
        while i < len(lines) and lines[i].strip().startswith(">"):
            q = lines[i].strip()[2:].strip()
            q = re.sub(r"^\*+|\*+$", "", q).strip()
            q = re.sub(r"^_+|_+$", "", q).strip()
            qs.append(q)
            i += 1
        para("\n".join(qs), size=11, align="C", color=(60,60,60), space_after=2)
        continue
    elif ln.strip() == "---":
        pdf.ln(4)
        x = pdf.l_margin + W/2 - 20
        pdf.line(x, pdf.get_y(), x+40, pdf.get_y())
        pdf.ln(6)
    elif ln.startswith("- "):
        para("\u2022  " + ln[2:], size=10.5, indent=6, space_after=2)
    elif ln.startswith("*") and ln.endswith("*") and len(ln) > 2 and not ln.startswith("**"):
        para(ln.strip("*"), size=10.5, align="C", color=(70,70,70), space_after=2)
    else:
        para(ln, size=10.5, space_after=3)
    i += 1

pdf.output(OUT)
print("wrote", OUT)
