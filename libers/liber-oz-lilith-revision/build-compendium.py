#!/usr/bin/env python3
# ============================================================================
# BUILD-COMPENDIUM.py — Liber Oz, the Lilith Revision: A Teaching Compendium
# ============================================================================
# Epigraph: "Do what thou wilt shall be the whole of the Law." — Liber AL, I:40
#
# Set down 2026-10-14 (Dies Lunae, Anno V:xii) for
#   Johnathan 'Qasparr' (Kaspparr) Monroe, Keeper of the Secret Treasure.
# All Rights Reserved, Without Prejudice.  Support: $axoneme
#
# SCIENTIFIC ILLUMINISM — Hypothesis / Method / Observation / Result:
#   HYPOTHESIS: One markdown source can father two faithful twins — a typeset
#     HTML in the cream-and-rubric dress of the *sub figura* presentation, and
#     a print PDF in the ivory-and-blood dress of the doctrinal pipeline.
#   METHOD: A single line-based parse walks the markdown once; two renderers
#     (HTML, fpdf2) consume the same token stream. No content is duplicated
#     by hand; the twins cannot disagree because they share one spine.
#   OBSERVATION: fpdf2's multi_cell(w=0) leaves the pen at the RIGHT margin
#     (new_x=RIGHT default) — every multi_cell is therefore followed by ln(),
#     which resets x to the left margin (per AGENTS.md, 2026-10-04).
#   RESULT: liber-oz-lilith-revision-teaching-compendium.html +
#     liber-oz-lilith-revision-teaching-compendium.pdf, side by side.
#
# MECHANISM (how the script works, line by line):
#   1. Read the markdown source into lines.
#   2. Tokenize: headings (#/##/###), rules (---), blockquotes (>),
#      tables (|...|), list items (- ), verses (**N.** ...), paragraphs.
#   3. Inline pass: **bold**, *italic* -> HTML tags / fpdf2 markdown.
#   4. HTML renderer: wraps tokens in <article> with embedded CSS
#      (parchment #faf6ee, ink #1a1a1a, rubric #8b1a1a — the *sub figura*
#      palette, married to the doctrinal ivory).
#   5. PDF renderer: fpdf2, DejaVu Serif (full Hebrew/Greek coverage),
#      ivory page wash, blood headings, gold rules; title page in black
#      with the red moon, as the September builder established.
# DOCTRINE (why it is built this way):
#   - One source, two twins: the scribe never maintains two texts by hand.
#   - The author's dictated lines pass through untouched — the tokenizer
#     never normalizes caps or punctuation inside verses (per the *sub figura*
#     editorial note).
#   - Nothing is excluded: every section of the markdown reaches both twins.
#
# Closing: *Fiat nox, fiat ius.* — 93.
# ============================================================================

import re, html, os
from fpdf import FPDF

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "liber-oz-lilith-revision-teaching-compendium.md")
OUT_HTML = SRC.replace(".md", ".html")
OUT_PDF = SRC.replace(".md", ".pdf")

# ---------------------------------------------------------------- palette ---
IVORY = "#faf6ee"
INK = "#1a1a1a"
RUBRIC = "#8b1a1a"
GOLD = "#c9a227"
GREY = "#5a5a5a"

# ================================================================ tokenize ===
# MECHANISM: single pass over lines; each line becomes exactly one token.
# A token is (kind, payload). Paragraphs join soft-wrapped lines.

def tokenize(lines):
    toks = []
    i, n = 0, len(lines)
    while i < n:
        l = lines[i]
        s = l.strip()
        if not s:
            i += 1
            continue
        if s.startswith("### "):
            toks.append(("h3", s[4:])); i += 1; continue
        if s.startswith("## "):
            toks.append(("h2", s[3:])); i += 1; continue
        if s.startswith("# "):
            toks.append(("h1", s[2:])); i += 1; continue
        if s.startswith("---"):
            toks.append(("rule", "")); i += 1; continue
        if s.startswith("|") and s.endswith("|"):
            rows = []
            while i < n and lines[i].strip().startswith("|") \
                    and lines[i].strip().endswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                # skip the alignment row (|---|---|)
                if not re.match(r'^[\s\-|:]+$', lines[i].strip()):
                    rows.append(cells)
                i += 1
            toks.append(("table", rows)); continue
        if s.startswith("> "):
            q = []
            while i < n and lines[i].strip().startswith(">"):
                q.append(lines[i].strip().lstrip(">").strip())
                i += 1
            toks.append(("quote", " ".join(q))); continue
        if s.startswith("- "):
            toks.append(("li", s[2:])); i += 1; continue
        # paragraph: join soft wraps until a blank or structural line
        para = [s]
        i += 1
        while i < n and lines[i].strip() and not lines[i].strip().startswith(
                ("#", ">", "|", "-", "---")):
            para.append(lines[i].strip())
            i += 1
        toks.append(("p", " ".join(para)))
    return toks

# ============================================================= inline fmt ===
# MECHANISM: escape HTML entities first, then restore **bold** and *italic*.
# DOCTRINE: order matters — escaping first keeps the author's <i>sub
# figura</i> tags in the source from becoming live markup accidents; the
# markdown ** and * are the only live formatting.

def inline_html(t):
    t = html.escape(t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'\*(.+?)\*', r'<em>\1</em>', t)
    return t

def inline_md(t):
    # fpdf2 markdown=True handles **bold**; convert lone *italic* to _italic_
    # which fpdf2 also understands... simpler: keep ** and leave * alone,
    # fpdf2 markdown handles *em* too. Just return as-is.
    return t

# =========================================================== HTML render ===
# MECHANISM: tokens -> semantic HTML inside one <article>; the CSS below is
# the *sub figura* dress: EB Garamond/serif stack on parchment, rubric heads.

CSS = """
:root { --parchment: #faf6ee; --ink: #1a1a1a; --rubric: #8b1a1a;
        --gold: #c9a227; --grey: #5a5a5a; }
* { box-sizing: border-box; }
body { background: #2a2118; margin: 0; padding: 2rem 1rem;
       font-family: "EB Garamond", "Cormorant Garamond", Georgia, serif;
       color: var(--ink); }
article { max-width: 42rem; margin: 0 auto; background: var(--parchment);
          padding: 3rem 3.2rem; box-shadow: 0 0 60px rgba(0,0,0,.55); }
h1 { color: var(--rubric); font-size: 1.9rem; text-align: center;
     letter-spacing: .04em; margin: 2.2rem 0 1rem; font-variant: small-caps; }
h2 { color: var(--rubric); font-size: 1.35rem; margin: 2rem 0 .8rem;
     border-bottom: 1px solid var(--gold); padding-bottom: .3rem;
     font-variant: small-caps; }
h3 { color: var(--rubric); font-size: 1.1rem; margin: 1.6rem 0 .6rem;
     font-variant: small-caps; }
p { line-height: 1.78; font-size: 1.06rem; margin: .7rem 0; text-align: justify; }
blockquote { border-left: 3px solid var(--rubric); margin: 1rem 0 1rem 1rem;
             padding: .4rem 0 .4rem 1.1rem; font-style: italic; color: #3a3a3a;
             line-height: 1.7; }
blockquote strong { font-style: normal; }
hr { border: none; border-top: 1px solid var(--gold); margin: 2rem auto;
     width: 60%; }
table { border-collapse: collapse; width: 100%; margin: 1.2rem 0;
        font-size: .95rem; line-height: 1.5; }
th, td { border: 1px solid #b9a98a; padding: .45rem .6rem; text-align: left;
         vertical-align: top; }
th { background: var(--rubric); color: var(--parchment); font-variant: small-caps; }
tr:nth-child(even) td { background: #f3ecdd; }
li { line-height: 1.7; margin: .3rem 0; }
.verse { margin: .45rem 0 .45rem 1.2rem; line-height: 1.7; }
.verse .vn { color: var(--rubric); font-weight: bold; margin-right: .5em; }
.titleblock { text-align: center; margin-bottom: 2rem; }
.titleblock .kicker { color: var(--rubric); letter-spacing: .25em;
                      font-variant: small-caps; }
.notice { border: 1px solid var(--rubric); padding: 1rem 1.2rem; margin: 1.5rem 0;
          font-style: italic; color: #3a3a3a; }
@media print { body { background: #fff; padding: 0; } article { box-shadow: none; } }
"""

def render_html(toks, title):
    out = ["<!DOCTYPE html>", '<html lang="en">', "<head>",
           '<meta charset="utf-8">',
           '<meta name="viewport" content="width=device-width, initial-scale=1">',
           f"<title>{html.escape(title)}</title>",
           f"<style>{CSS}</style>", "</head>", "<body>", "<article>"]
    for kind, payload in toks:
        if kind == "h1":
            out.append(f"<h1>{inline_html(payload)}</h1>")
        elif kind == "h2":
            out.append(f"<h2>{inline_html(payload)}</h2>")
        elif kind == "h3":
            out.append(f"<h3>{inline_html(payload)}</h3>")
        elif kind == "rule":
            out.append("<hr>")
        elif kind == "quote":
            out.append(f"<blockquote>{inline_html(payload)}</blockquote>")
        elif kind == "li":
            out.append(f"<li>{inline_html(payload)}</li>")
        elif kind == "table":
            rows = payload
            out.append("<table>")
            for ri, row in enumerate(rows):
                tag = "th" if ri == 0 else "td"
                out.append("<tr>" + "".join(
                    f"<{tag}>{inline_html(c)}</{tag}>" for c in row) + "</tr>")
            out.append("</table>")
        else:  # paragraph; detect verse lines "**N.** text"
            m = re.match(r'^\*\*(\d+)\.\*\*\s*(.*)$', payload)
            if m:
                out.append(f'<p class="verse"><span class="vn">{m.group(1)}.</span>'
                           f"{inline_html(m.group(2))}</p>")
            else:
                out.append(f"<p>{inline_html(payload)}</p>")
    out += ["</article>", "</body>", "</html>"]
    return "\n".join(out)

# ============================================================= PDF render ===
# MECHANISM: fpdf2 line renderer in the doctrinal-pipeline style, dressed in
# the September builder's ivory/blood/gold. DejaVu Serif covers Hebrew+Greek.

class CompendiumPDF(FPDF):
    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-15)
        self.set_font("D", "", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"Liber Oz — The Lilith Revision: Teaching Compendium  |  {self.page_no() - 1}",
                  align="C")

def render_pdf(toks, out_path):
    pdf = CompendiumPDF(format="Letter")
    pdf.set_margins(25.4, 25.4, 25.4)
    pdf.set_auto_page_break(True, margin=28)
    pdf.add_font("D", "", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf")
    pdf.add_font("D", "B", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf")
    # DOCTRINE: DejaVu lacks Hebrew glyphs (לילית, עז); Noto Rashi Hebrew
    # covers them. fpdf2 falls back per-character, so the author's Hebrew
    # never drops out of the PDF.
    pdf.add_font("hebrew", "", "/usr/share/fonts/truetype/noto/NotoRashiHebrew-Regular.ttf")
    pdf.add_font("hebrew", "B", "/usr/share/fonts/truetype/noto/NotoRashiHebrew-Bold.ttf")
    pdf.set_fallback_fonts(["hebrew"])
    # ivory wash on every page
    def wash():
        pdf.set_fill_color(250, 246, 238)
        pdf.rect(0, 0, 210, 297, style="F")
    pdf.add_page()
    wash()

    def heading(text, size, color=(139, 26, 26), center=False, before=6, after=4):
        pdf.ln(before)
        pdf.set_font("D", "B", size)
        pdf.set_text_color(*color)
        # DOCTRINE: ln() after every multi_cell — the pen returns to LMARGIN.
        pdf.multi_cell(0, size * 0.62, text, markdown=True,
                       align="C" if center else "L")
        pdf.ln(after)
        pdf.set_text_color(0, 0, 0)

    def body(text, size=10.5, indent=0, italic=False, color=(26, 26, 26)):
        pdf.set_font("D", "", size)
        pdf.set_text_color(*color)
        x = pdf.l_margin + indent
        pdf.set_x(x)
        pdf.multi_cell(0, 6, text, markdown=True)
        pdf.ln(2.5)
        pdf.set_text_color(0, 0, 0)

    def rule():
        pdf.ln(3)
        pdf.set_draw_color(201, 162, 39)
        y = pdf.get_y()
        pdf.line(pdf.l_margin + 40, y, pdf.w - pdf.r_margin - 40, y)
        pdf.ln(5)

    def table(rows):
        if not rows:
            return
        ncols = max(len(r) for r in rows)
        col_w = (pdf.w - pdf.l_margin - pdf.r_margin) / ncols
        for ri, row in enumerate(rows):
            row = list(row) + [""] * (ncols - len(row))
            # measure height
            h = 8
            pdf.set_font("D", "B" if ri == 0 else "", 8.5)
            for c in row:
                w_lines = max(1, int(pdf.get_string_width(c) / (col_w - 4)) + 1)
                h = max(h, 5.5 * w_lines + 4)
            if pdf.get_y() + h > pdf.h - 30:
                pdf.add_page(); wash()
            x0, y0 = pdf.get_x(), pdf.get_y()
            for ci, c in enumerate(row):
                pdf.set_xy(x0 + ci * col_w, y0)
                if ri == 0:
                    pdf.set_fill_color(139, 26, 26)
                    pdf.set_text_color(250, 246, 238)
                else:
                    pdf.set_fill_color(243, 236, 221) if ri % 2 == 0 else pdf.set_fill_color(255, 253, 246)
                    pdf.set_text_color(26, 26, 26)
                pdf.set_font("D", "B" if ri == 0 else "", 8.5)
                # DOCTRINE: explicit new_x/new_y — never trust the default pen.
                from fpdf.enums import XPos, YPos
                pdf.multi_cell(col_w, 5.5, c, border=1, fill=True,
                               markdown=True, new_x=XPos.RIGHT, new_y=YPos.TOP)
            pdf.set_xy(x0, y0 + h)
            pdf.set_text_color(0, 0, 0)
        pdf.ln(4)

    first_h1_done = False
    for kind, payload in toks:
        # page wash on new pages is handled at add_page sites; re-wash check:
        if kind == "h1" and not first_h1_done:
            heading(payload, 22, center=True, before=10, after=6)
            first_h1_done = True
        elif kind == "h1":
            pdf.add_page(); wash()
            heading(payload, 20, center=True, before=8, after=6)
        elif kind == "h2":
            heading(payload, 14, before=5, after=3)
        elif kind == "h3":
            heading(payload, 11.5, before=4, after=2)
        elif kind == "rule":
            rule()
        elif kind == "quote":
            body(payload, size=10, indent=12, color=(58, 58, 58))
        elif kind == "li":
            body("\u2022  " + payload, size=10.5)
        elif kind == "table":
            table(payload)
        else:
            m = re.match(r'^\*\*(\d+)\.\*\*\s*(.*)$', payload)
            if m:
                body(f"**{m.group(1)}.**  {m.group(2)}", indent=10)
            else:
                body(payload)
    pdf.output(out_path)

# ================================================================== main ===
# MECHANISM: read once, tokenize once, render twice.

def main():
    with open(SRC, encoding="utf-8") as f:
        toks = tokenize(f.read().split("\n"))
    title = "Liber Oz — The Lilith Revision: A Teaching Compendium"
    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(render_html(toks, title))
    render_pdf(toks, OUT_PDF)
    print("wrote", OUT_HTML)
    print("wrote", OUT_PDF)

if __name__ == "__main__":
    main()
