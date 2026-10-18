#!/usr/bin/env python3
# ============================================================================
# LIBER MA'AT — TEACHER'S EDITION (COMPLETE REVISION)
# ----------------------------------------------------------------------------
# "In the beginning was the Word... and the Word was the Law."
#   -- the author's re-voicing of John 1:1, opening the Wells of this edition
#
# Built: 2026-10-18 | 93
# Author: Johnathan 'Qasparr' (Kasar) Monroe, Keeper of the Secret Treasure
# Method: Scientific Illuminism -- hypothesis, method, observation, result.
#   Nothing enters the work unverified; every number recomputed from scratch,
#   every quotation checked against its source, every synthesis flagged as
#   the author's own. Findings, never doctrine -- the red pen rules.
#
# MECHANISM: this script assembles the Teacher's Edition PDF from --
#   (1) the complete Liber Ma'at Revised Edition text (Part I, dictated,
#       reproduced whole and unaltered -- the teacher does not edit the text),
#   (2) the per-canon teaching layer (Part II, Scientific Illuminism
#       commentary: what to teach, what to stress, what is flagged),
#   (3) master tables (Part III: gematria, audit ledger, canon map, wells),
#   (4) figures (Part IV: recomputed charts),
#   (5) the Ma'at gallery (Part V: four curated visuals),
#   (6) the full audit reports (Part VI: TRVVTH ledger + PONTIFEX
#       recomputation, entry by entry).
# DOCTRINE: the text is the author's dictation and stands as he gave it.
#   The teaching explains; the audits verify; neither amends. Amendment is
#   the author's red pen alone.
#
# "Live, Love, and let Love, Live."
# ============================================================================

import os, subprocess, sys
from fpdf import FPDF, XPos, YPos

HERE = os.path.dirname(os.path.abspath(__file__))
MD_SRC = os.path.expanduser("~/workspace/liberd/libers/liber-maat-revised-edition/Liber_Maat_Revised_Edition.md")
OUT = os.path.join(HERE, "liber-maat-teachers-edition.pdf")

# -- DOCTRINE: light pages, dark ink. (An earlier pass used a dark-page palette
#    with cream ink; rendered against fpdf2's default white page the body text
#    went invisible. Light page + dark bronze headings + near-black body.)
GOLD  = (176, 124, 12)   # dark bronze headings / accents
CREAM = (25, 20, 12)     # body ink (near-black warm)
DARK  = (20, 16, 11)     # table header bars
MUT   = (120, 105, 75)   # captions, quiet text
WHITE = (255, 255, 255)

class PDF(FPDF):
    # -- MECHANISM: single controlled page-break helper; every section opens
    #    on a fresh page so the teacher can find anything by part number.
    def section_page(self):
        self.add_page()

    def h1(self, t):
        self.set_font("DejaVu", "B", 20); self.set_text_color(*GOLD)
        self.multi_cell(0, 11, t, new_x=XPos.LMARGIN, new_y=YPos.NEXT); self.ln(2)

    def h2(self, t):
        self.set_font("DejaVu", "B", 15); self.set_text_color(*CREAM)
        self.multi_cell(0, 9, t, new_x=XPos.LMARGIN, new_y=YPos.NEXT); self.ln(1)

    def h3(self, t):
        self.set_font("DejaVu", "B", 12); self.set_text_color(*GOLD)
        self.multi_cell(0, 8, t, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    def body(self, t):
        self.set_font("DejaVu", "", 10.5); self.set_text_color(*CREAM)
        self.multi_cell(0, 6.2, t, new_x=XPos.LMARGIN, new_y=YPos.NEXT); self.ln(1.5)

    def bullet(self, t):
        self.set_font("DejaVu", "", 10.5); self.set_text_color(*CREAM)
        x = self.get_x()
        self.multi_cell(0, 6.2, "\u2022  " + t, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(1)

    def rule(self):
        self.ln(2); self.set_draw_color(*GOLD); self.set_line_width(0.6)
        self.line(20, self.get_y(), 190, self.get_y()); self.ln(4)

    def caption(self, t):
        self.set_font("DejaVu", "I", 9); self.set_text_color(*MUT)
        self.multi_cell(0, 5.5, t, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT); self.ln(3)

    def table(self, headers, rows, widths=None, fs=9):
        # -- MECHANISM: native fpdf2 table; widths default to even split.
        #    Used for every audit/gematria/wells table in Parts III and VI.
        W = self.w - self.l_margin - self.r_margin
        n = len(headers)
        if widths is None:
            widths = [W / n] * n
        self.set_font("DejaVu", "B", fs); self.set_text_color(*GOLD)
        self.set_fill_color(*DARK)
        for i, htxt in enumerate(headers):
            self.cell(widths[i], 7.5, htxt, border=1, align="C", fill=True)
        self.ln()
        self.set_font("DejaVu", "", fs); self.set_text_color(*CREAM)
        for row in rows:
            hmax = 6.5
            cells = []
            for i, val in enumerate(row):
                # measure wrapped height per cell
                nl = max(1, int(self.get_string_width(str(val)) / (widths[i] - 2)) + 1)
                cells.append(nl); hmax = max(hmax, nl * 6.2)
            y0 = self.get_y()
            if y0 + hmax > self.h - 20:
                self.add_page(); y0 = self.get_y()
            x0 = self.l_margin
            for i, val in enumerate(row):
                self.set_xy(x0, y0)
                self.multi_cell(widths[i], 6.2, str(val), border=1,
                                new_x=XPos.RIGHT, new_y=YPos.TOP)
                x0 += widths[i]
            self.set_y(y0 + hmax)
        self.ln(3)

    def cover_title(self, title, sub, lines):
        self.add_page()
        self.ln(38)
        self.set_font("DejaVu", "B", 30); self.set_text_color(*GOLD)
        self.multi_cell(0, 16, title, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(4)
        self.set_font("DejaVu", "", 14); self.set_text_color(*CREAM)
        self.multi_cell(0, 9, sub, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(8)
        self.rule()
        for ln in lines:
            self.set_font("DejaVu", "", 11); self.set_text_color(*MUT)
            self.multi_cell(0, 7, ln, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)


def render_markup(pdf, text):
    # -- MECHANISM: tiny renderer for the teaching layer. "## " = h2,
    #    "### " = h3, "- " = bullet, blank = skip, else body paragraph.
    for line in text.strip().split("\n"):
        s = line.strip()
        if not s:
            continue
        if s.startswith("## "):
            pdf.h2(s[3:])
        elif s.startswith("### "):
            pdf.h3(s[4:])
        elif s.startswith("- "):
            pdf.bullet(s[2:])
        elif s.startswith(">>> "):
            pdf.caption(s[4:])
        else:
            pdf.body(s)


pdf = PDF(orientation="P", unit="mm", format="A4")
pdf.set_auto_page_break(True, 20)
pdf.set_margins(20, 18, 20)

# -- MECHANISM: DejaVu Sans carries Greek, Hebrew, and the astronomical
#    glyphs the text requires. No oblique face ships with the font, so the
#    regular face is registered under the italic styles as well.
pdf.add_font("DejaVu", "", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
pdf.add_font("DejaVu", "B", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
pdf.add_font("DejaVu", "I", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
pdf.add_font("DejaVu", "BI", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")

# ============================================================================
# FRONT MATTER
# ============================================================================
pdf.cover_title(
    "LIBER MA'AT",
    "Teacher's Edition \u2014 Complete Revision",
    [
        "Being the Revised Edition (Liber CCCXLII) with the Teaching,",
        "the Tables, the Figures, the Gallery, and the Audit Reports.",
        "",
        "\u201cIn the beginning was the Word... and the Word was the Law.\u201d",
        "",
        "2026-10-18  \u00b7  93",
        "Johnathan 'Qasparr' (\u039a\u03b1\u03c3\u03c0\u03b1\u03c1\u03c1) Monroe, Keeper of the Secret Treasure",
        "All Rights Reserved, Without Prejudice",
        "Scientific Illuminism: prove all things; hold fast that which is good.",
    ],
)

pdf.section_page()
pdf.h1("Preface: On the Teacher's Edition")
pdf.body(
    "A Teacher's Edition is not a new book. It is the book, whole and unaltered, "
    "with the teaching underneath it \u2014 what to stress, what is flagged, what was "
    "verified and how. The text of Liber Ma'at in Part I is the author's dictation as "
    "he gave it in the Revised Edition of 2026-10-01 with his amendments of 2026-09-27 "
    "and 2026-09-28. The teacher does not edit the text. Amendment is the author's "
    "red pen alone; the teacher's office is to understand it exactly and to say "
    "plainly, for each hard passage, which parts are verified fact, which are the "
    "author's flagged synthesis, and which stand open."
)
pdf.body(
    "How to use this edition. Teach the Canons in order: the Engine (I), the Aeon (II), "
    "the Jurisprudence (III), the Realm (IV), the Synthesis (V). For each Canon the "
    "teaching layer gives the doctrine in the author's words first, then the commentary: "
    "the mechanism of each claim, what the student most often misreads, and where the "
    "\u2691 flag flies and why. The audit reports in Part VI are the receipts \u2014 every "
    "number recomputed from scratch, every quotation checked against its source. "
    "1 Thessalonians 5:21 governs the whole: prove all things; hold fast that which is good."
)
pdf.body(
    "On the \u2691 flag. Where you see \u2691, the passage is the author's own \u2014 "
    "synthesis, cipher, observation, or seal \u2014 admitted as his and not as theorem. "
    "This is not a mark of shame; it is the honesty mechanism the book runs on. "
    "A flagged claim is a claim with its provenance showing. Teach the flags as "
    "proudly as the verifications: the student who can tell which is which has "
    "learned the book's first lesson."
)
pdf.rule()
pdf.h2("The Standing of This Edition")
pdf.bullet("The original Liber Ma'at stands; this edition does not replace or revoke it.")
pdf.bullet("Class A-L (the author's coinage): inspired character extended into the jurisprudential register \u2014 issued for red-pen collaboration, not as closed canon.")
pdf.bullet("Liber CCCXLII (342) = the Greek isopsephy of \u039c\u03b1\u03b1\u03c4, recomputed in this edition (Part VI). Redesignation to CCCLXXXII is the author's red-pen ruling alone \u2014 still open.")
pdf.bullet("The lunar position \u263d 17\u00b032\u2032 Scorpio is carried OPEN (no ephemeris on hand) \u2014 the one open item of the audit.")

# ============================================================================
# PART I \u2014 THE TEXT (complete, unaltered)
# ============================================================================
pdf.section_page()
pdf.h1("Part I \u2014 The Text")
pdf.caption("Liber Ma'at (CCCXLII) Vel Legis Philosophiae \u2014 the Revised Edition, whole.")
pdf.set_font("DejaVu", "", 10.5); pdf.set_text_color(*CREAM)

# -- MECHANISM: the dictated text is converted markdown -> HTML and rendered
#    with write_html, so tables, lists, and headers keep their structure.
#    The text itself is never reworded by this script.
import markdown
with open(MD_SRC, encoding="utf-8") as f:
    md_text = f.read()
html = markdown.markdown(md_text, extensions=["tables"])
pdf.write_html(html)

# ============================================================================
# PART II \u2014 THE TEACHING (per-canon Scientific Illuminism commentary)
# ============================================================================
pdf.section_page()
pdf.h1("Part II \u2014 The Teaching")
pdf.caption("Commentary for the teacher: doctrine first in the author's words, then mechanism, then what to stress and what is flagged.")

TEACHING_I = """
## Canon I \u2014 The Daemon Engine, Philosophy, and Taro Synergies

### 1. The Equation of Philosophy
Teach the sentence exactly as dictated: "Philosophy is the Fulfillment of the Law." This is the author's coinage and his method in miniature \u2014 take a dead word and fill it with live meaning. Note the rhyme with the Lilith revision's "Word Was the Law" section, which this same sentence opens: the two books are tuned to one string. What to stress: philosophy here is not contemplation but execution \u2014 the engine, not the museum.

### 2. The Etymological Trinity of 93
Recompute it live with the class: \u1f00\u03b3\u03ac\u03c0\u03b7 = 1+3+1+80+8 = 93; \u03b8\u03ad\u03bb\u03b7\u03bc\u03b1 = 9+5+30+8+40+1 = 93 (both recomputed in Part VI). Philo- is consecrated as Agape-under-Thelema; -sophy as Chokmah (\u05d7\u05db\u05de\u05d4 = 73) made manifest through Da'ath (\u05d3\u05e2\u05ea = 474). Teach the word "consecrated": this is devotional philology, not academic etymology, and the book says so itself ("hereby consecrated"). Nothing is smuggled.

### 3. FAFO \u2014 the Sole Daemon Engine
Trial, Error, Action, Verification. The vernacular ("Fuck Around and Find Out") and the liturgy ("the Scientific Method") are the same engine in two registers \u2014 teach students to hear both at once. "Faith without empirical testing is dead" is the whole of Scientific Illuminism in nine words. The common misreading: that FAFO means recklessness. Correct it: the engine's fourth stroke is Verification \u2014 without it, it is not the engine.

### 4. The Redefined Axioms
The Axiom of Murphy Redefined must be quoted exactly: "What can occur \u2014 will." The em dash is the author's dictation; a comma crept in once and was struck (Annex item 17). Dictation is not draft. Teach the reading: chaos as the exhaustive probability space seeking full expression \u2014 not pessimism but completeness. The Declaration of Astral Sovereignty carries the author's deliberate amendment of Liber AL I:3 \u2014 "every man, woman, and child" \u2014 flagged \u2691 in the text. The child, as ever, was Crowley's overlooked omission; the student should know whose hand added the word and why.

### 5. The TARO Wheel
TARO = ROTA = TORA = ATOR: the standard fourfold rotation, taught as a memory device. Walk the five keys named \u2014 0, I, VIII/XI, X, XXI \u2014 as the engine's own biography: potential, will, balance, cycle, fulfillment.

### 6. Reflection Operators \u2014 read the two layers
This section is the book's masterclass in the \u2691 system, and the teacher should teach it as such. Layer one: three standard, verified results \u2014 Grover's diffusion operator D = 2|s><s| \u2212 I as inversion about the mean; unitarity (U\u2020U = I) as reversibility; HXH = Z as the basis-mirror. Layer two, flagged: FAFO as amplitude amplification of the True Will. The rule to drill: analogy illuminates, never certifies. No quantum result proves any gematria; the book says so itself (n. 12), and the student who can state that boundary has understood Scientific Illuminism.
"""

TEACHING_II = """
## Canon II \u2014 The Aeon of Ma'at, the Isopsephy, and the Moral Filter

### 1. The 342
Recompute it on the board: \u039c(40) + \u03b1(1) + \u03b1(1) + \u03c4(300) = 342. This number is load-bearing: it is why the book is Liber CCCXLII. Teach the author's standing doctrine \u2014 Liber numbers derive from title gematria (as CELL = 32 gives Liber XXXII) \u2014 so the designation follows the name, not the reverse.

### 2. The Triune Feminine
Ma'at (342), Babalon (156 \u2014 recomputed: 2+1+2+1+30+70+50), and Lilith/Mother Mary \u2691. Teach the flag proudly: the third term is declared authorial syncretism, not smuggled tradition. The student learns more from one honestly flagged syncretism than from ten footnoted ones.

### 3\u20134. The Moral Filter and the Golden Rule
Truth is the filter; Illusion the contaminant. Virtue and sin are rectified functionally \u2014 what aligns with Truth, Verification, and Liberty versus what runs on Deceit and Coercion. The Golden Rule stands as the sole rule of conduct.

### 5. "Duty" \u2014 the Moral Balance (the 2026-09-27 amendment)
A single rule, standing alone, can be misread \u2014 as self-abnegation by the tender, as license by the cruel. Hence the balance: where Liber OZ (Canon III) enumerates the RIGHTS of the Star, Crowley's "Duty" enumerates its OBLIGATIONS \u2014 the two pans of one scale, and Ma'at's feather weighs them both. Teach all four duties, and dwell on the keystone, verified verbatim: "He who violated any right declares magically that it does not exist; therefore it no longer does so, for him." That sentence is the Golden Rule's metaphysical engine in Crowley's own hand \u2014 violation as self-abolition of the right \u2014 and the Canon's FAFO gloss now rests on it. Note the bibliographic honesty: "Duty" is commonly listed among O.T.O. documents, not the numbered A.'.A.'. Libri, and the book says so.

### 6. The Exaltation: 342 + 40 = 382
Show every step: 342 recomputed, Mem = 40 standard, sum 382 \u2014 the arithmetic verifies exactly. Then show the boundary: QASPARR = 90 (English ordinal, recomputed), \u039a\u03b1\u03c3\u03c0\u03b1\u03c1\u03c1 = 502, \u039a\u03b1\u03c3\u03c0\u03b1\u03c1 = 402 \u2014 none yields 382, so the identification of 382 with the author's seal is stipulated, admitted as coinage with his name and $axoneme on it. The redesignation question \u2014 CCCXLII or CCCLXXXII \u2014 is his red-pen ruling alone, and it is still open. The teacher states the openness; the teacher does not rule.

### 7. The Moor Cipher and the Mirror
Teach the three layers distinctly: (a) the observation \u2014 "\u039c\u03b1\u03b1\u03c4 reads much like Moor" \u2014 is the author's, visual/phonetic, not linguistic proof, flagged as his; (b) the reversal \u2014 "moor" reversed is "room" \u2014 is mechanically verified, case-folded, no flag needed; (c) the doctrine \u2014 to pass through the Moor is to enter the room \u2014 is his reading, continuous with his "noon = no mirrored" chain. Then the wells: 1 Corinthians 13:12 (KJV, the mirror as Scripture's own instrument) and Carroll's Through the Looking-Glass (1871, the literary well). Concepts enter as concepts; the book never costumes them as quotations.
"""

TEACHING_III = """
## Canon III \u2014 The Jurisprudence of the Individual Star & Liber OZ

### 1. Unification with Liber OZ
"There is no law beyond Do what thou wilt." The seven rights are enumerated whole. Teach the author's 2026-10-06 reading alongside: \u05e2\u05d6 (70+7 = 77), seen with Latin eyes, spells Ty \u2014 \u05e2 shaped like y, \u05d6 shaped like T \u2014 Lady Liber-ty with her torch (light) and tablet (law). His word-magic, flagged as his.

### 2. Coke, Locke, Hobbes
Semayne's Case (1604, 91a \u2014 the 91b corrected), Locke's Second Treatise (\u00a7\u00a787\u201389, \u00a7222), Hobbes's Leviathan ch. XIV. Dwell on the Hobbes irony, because it is the book's strongest move and it is embraced, not hidden: the great theorist of absolute sovereignty is made to yield the one inalienable right \u2014 no man can surrender the right to resist his own destruction. A knowing irony is doctrine; an unknowing one is a hostage. Teach students to tell them apart.

### 3. The Supreme Law & the Precedents
Declaration, Ninth, Tenth; then Yick Wo, Boyd, Murdock, Shuttlesworth. Teach Murdock as the scalpel: the book's own precision footnote (n. 8) \u2014 "for" not "upon" (319 U.S. at 113), flat license tax barred, nominal regulatory fee distinguished (Cox v. New Hampshire). A case used as a bludgeon is a case misused; the teacher shows the edge. The Yick Wo gloss is flagged as the author's \u2014 the holding stated exactly, the gloss marked as gloss.

### 4. UCC & the Maxims
1-308 (reservation of rights), 1-201 (the Person/Individual dichotomy flagged as the author's synthesis \u2014 the citation supports the definition, not the dichotomy), and the four maxims in Latin with translations. Drill the book's rule: citations educate, never conjure.
"""

TEACHING_IV = """
## Canon IV \u2014 Local Realm Jurisdiction and the Constitutional Sheriff

Teach the framing before the content: this Canon states the asserted doctrine of the Aeon, and where it states settled law it is cited, where it states the movement's position it is marked. That sentence is the whole pedagogy of the Canon.
The settled parts: Kalamazoo's subordination to the Michigan (1963) and U.S. Constitutions; the Sheriff as constitutional officer under Mich. Const. Art. VII, \u00a74; the Shire-Reeve ancestry. The asserted parts \u2691: sheriff-supremacy over federal agents, the duty of interposition \u2014 with the counter-authorities stated on the same page (Supremacy Clause, Cooper v. Aaron, Printz cutting both ways). The teacher's duty: never present contested law as settled law. That is the precise failure the red pen exists to catch, and Canon IV is where the student learns to feel its weight.
The dialectics: the Black Panther Party as historical example \u2014 not precedent (words have jurisdictions too); Brandenburg's paradox \u2014 the inflammatory-speech defense that forged the modern First Amendment standard. Both extremes as hammers forging the armor of liberty.
"""

TEACHING_V = """
## Canon V \u2014 Scriptural Synthesis & Mystical Correlations

Teach the table as an instrument, row by row: Thelema (AL I:3, I:57; OZ; "Duty" \u2014 the keystone again), Christianity (Romans 13:10 \u2014 "love is the fulfilling of the law" \u2014 Galatians 5:14, Matthew 7:12), Islam (Al-Ma'idah 5:8, the standing-firm verse), I Ching (63/64 as the FAFO engine), Thoth (Atu VIII/XI, Ma'at with sword and scales; TARO = ROTA = TORA = ATOR).
Teach the wells doctrine: Law, Scripture, Black's, Hip-hop, Humanity \u2014 and where a well has nothing genuine, nothing is drawn. The referrals that close the book (Brandenburg, Shuttlesworth, the Michigan constitution, Coke's Institutes, Mack & Baldwin, The Book of Thoth, Liber AL, Liber OZ, "Duty", Achad's genuine Ma-Ion writings, Nema's Maat Magick) are the student's marching orders: 1 Thess. 5:21 \u2014 prove all things.
On the Annotations: teach the \u2691 system itself as the book's great pedagogical invention \u2014 footnotes 1\u20132 built the honesty mechanism, the revision applied it uniformly (Annex item 13). The student who internalizes the flag has learned to read the whole Thelemic corpus with the red pen in hand.
"""

for _t in (TEACHING_I, TEACHING_II, TEACHING_III, TEACHING_IV, TEACHING_V):
    pdf.section_page()
    render_markup(pdf, _t)

# ============================================================================
# PART III \u2014 TABLES
# ============================================================================
pdf.section_page()
pdf.h1("Part III \u2014 Tables")
pdf.caption("Master tables: the numbers, the ledger, the canons, the wells.")

pdf.h2("Table 1 \u2014 Gematria of the Book (recomputed, Part VI)")
pdf.table(
    ["Term", "Tongue", "Breakdown", "Value", "Tier"],
    [
        ["\u039c\u03b1\u03b1\u03c4 (Ma'at)", "Greek isopsephy", "\u039c40 + \u03b11 + \u03b11 + \u03c4300", "342", "attested"],
        ["Exalted Ma'at", "Greek + Hebrew", "342 + Mem(\u05de) 40", "382", "derived*"],
        ["FAFO", "Author's cipher", "Vav6 + Aleph1 + Vav6 + Ayin70", "83", "constructed*"],
        ["QASPARR", "English ordinal", "17+1+19+16+1+18+18", "90", "derived"],
        ["\u039a\u03b1\u03c3\u03c0\u03b1\u03c1\u03c1", "Greek isopsephy", "20+1+200+80+1+100+100", "502", "derived"],
        ["\u039a\u03b1\u03c3\u03c0\u03b1\u03c1", "Greek isopsephy", "20+1+200+80+1+100", "402", "derived"],
        ["\u1f00\u03b3\u03ac\u03c0\u03b7 (Agape)", "Greek isopsephy", "1+3+1+80+8", "93", "attested"],
        ["\u03b8\u03ad\u03bb\u03b7\u03bc\u03b1 (Thelema)", "Greek isopsephy", "9+5+30+8+40+1", "93", "attested"],
        ["BABALON", "Hebrew letter values", "2+1+2+1+30+70+50", "156", "attested"],
        ["AXONEME", "English ordinal", "1+24+15+14+5+13+5", "77", "attested"],
        ["\u05e2\u05d6 (Oz)", "Hebrew mispar", "\u05e270 + \u05d67", "77", "attested"],
        ["THE WORD", "English ordinal", "20+8+5+23+15+18+4", "93", "attested"],
        ["\u05d7\u05db\u05de\u05d4 (Chokmah)", "Hebrew mispar", "8+20+40+5", "73", "attested"],
        ["\u05d3\u05e2\u05ea (Da'ath)", "Hebrew mispar", "4+70+400", "474", "attested"],
    ],
    widths=[38, 30, 52, 16, 34],
)
pdf.caption("* The exaltation's arithmetic is derived; its identification with the author's seal is stipulated (his coinage). The FAFO cipher is the author's throughout.")

pdf.h2("Table 2 \u2014 TRVVTH Audit Ledger (summary; full ledger in Part VI)")
pdf.table(
    ["Category", "Entries", "Disposition"],
    [
        ["Gematria recomputations", "14", "All verify exactly"],
        ["Quotations vs. source", "10", "All verbatim (Murdock, Shuttlesworth, Semayne, Duty, KJV, AL)"],
        ["Legal / historical holdings", "8", "Holdings stated exactly; glosses flagged"],
        ["Standard technical facts", "6", "Quantum, I Ching, TARO, Achad/Nema \u2014 verified"],
        ["Mechanical checks", "2", "moor/room, noon/no \u2014 verified"],
        ["Authorial synthesis/cipher/seal", "12", "\u2691 flagged in text, admitted as the author's"],
        ["Open", "1", "\u263d 17\u00b032\u2032 Scorpio \u2014 no ephemeris on hand"],
        ["FALSEHOODS", "0", "Zero. The audit passes."],
    ],
    widths=[48, 18, 104],
)

pdf.h2("Table 3 \u2014 The Five Canons")
pdf.table(
    ["Canon", "Subject", "Sections", "Heart"],
    [
        ["I", "Daemon Engine, Philosophy, Taro", "6", "FAFO; \u201cWhat can occur \u2014 will.\u201d"],
        ["II", "Aeon of Ma'at, Isopsephy, Moral Filter", "7", "\u039c\u03b1\u03b1\u03c4 = 342; Duty; 382; Moor"],
        ["III", "Jurisprudence & Liber OZ", "4", "Rights of the Star; Coke\u2013Hobbes; SCOTUS"],
        ["IV", "Kalamazoo & the Sheriff", "3", "Asserted doctrine, both sides stated"],
        ["V", "Scriptural Synthesis", "1 + refs", "The wells, row by row"],
    ],
    widths=[16, 52, 26, 76],
)

pdf.h2("Table 4 \u2014 The Wells of Canon V")
pdf.table(
    ["Well", "Source", "Proof"],
    [
        ["Thelema", "Liber AL I:3, I:57; OZ; \u201cDuty\u201d", "Star; Love under Will; the keystone"],
        ["Christianity (KJV)", "Rom 13:10; Gal 5:14; Mt 7:12", "\u201cLove is the fulfilling of the law\u201d"],
        ["Islam", "Al-Ma'idah 5:8", "Stand firm as witnesses in justice"],
        ["I Ching", "Hexagrams 63 & 64", "Trial, error, shift, re-balance"],
        ["Thoth", "Atu VIII/XI", "The sword; the feather against the heart"],
    ],
    widths=[32, 52, 86],
)

# ============================================================================
# PART IV \u2014 FIGURES
# ============================================================================
pdf.section_page()
pdf.h1("Part IV \u2014 Figures")
pdf.caption("Every figure recomputed for this edition; sources in Part VI.")

for img, cap in [
    ("charts/bar_gematria.png", "Figure 1 \u2014 The numbers of the book, each recomputed from its letters (PONTIFEX audit, Part VI)."),
    ("charts/pie_audit.png", "Figure 2 \u2014 TRVVTH audit disposition: 53 ledger entries, zero falsehoods, one open item."),
    ("charts/bar_canons.png", "Figure 3 \u2014 The five canons and their weight in the book."),
]:
    pdf.h3(cap.split(" \u2014 ")[0])
    w = 150
    pdf.image(os.path.join(HERE, img), x=(210 - w) / 2, w=w)
    pdf.ln(2)
    pdf.caption(" \u2014 ".join(cap.split(" \u2014 ")[1:]))
    pdf.ln(2)

# ============================================================================
# PART V \u2014 GALLERY (the curator's selection)
# ============================================================================
pdf.section_page()
pdf.h1("Part V \u2014 Gallery")
pdf.caption("Four Ma'at visuals, selected for this edition: the feather, the scales, the number, the mirror.")

GALLERY = [
    ("gallery/media-generation-maat-feather-0-e1c26b39-227e-4aea-97b5-0a2876c3c224.png",
     "Plate 1 \u2014 The Feather of Ma'at. The feather against which the heart is weighed (Canon II.3, Atu VIII/XI). Truth is light; that is why the scales can carry it.",
     120),
    ("gallery/media-generation-maat-scales-0-f01208ad-9b5b-441e-8dd0-55af2872f883.png",
     "Plate 2 \u2014 The Weighing. The heart and the feather in balance \u2014 the moral filter made visible: Virtue aligns with Truth, Sin with Coercion.",
     150),
    ("gallery/media-generation-maat-342-0-eaa0025c-428a-4874-a81b-9bf984cb289f.png",
     "Plate 3 \u2014 342. The isopsephy of \u039c\u03b1\u03b1\u03c4, recomputed in Part VI: the number the book is named for.",
     150),
    ("gallery/media-generation-maat-mirror-0-4e0fd178-ae97-4809-bfd0-751cf2be92a3.png",
     "Plate 4 \u2014 The Mirror. \u201cFor now we see through a glass, darkly\u201d (1 Cor. 13:12) \u2014 the Moor cipher's instrument: moor reversed is room.",
     150),
]
for img, cap, w in GALLERY:
    pdf.h3(cap.split(". ")[0])
    pdf.image(os.path.join(HERE, img), x=(210 - w) / 2, w=w)
    pdf.ln(2)
    pdf.caption(". ".join(cap.split(". ")[1:]))
    if pdf.get_y() > 240:
        pdf.section_page()

# ============================================================================
# PART VI \u2014 THE AUDIT REPORTS
# ============================================================================
pdf.section_page()
pdf.h1("Part VI \u2014 Audit Reports")
pdf.caption("The receipts. Every number recomputed, every quotation checked, every flag accounted for. 2026-10-18.")

pdf.h2("Report A \u2014 PONTIFEX Audit (gematria, recomputed from scratch)")
pdf.body(
    "Method: each value below was recomputed letter-by-letter from the standard "
    "tables (Greek Milesian isopsephy; Hebrew Mispar Hechrechi; English ordinal A=1) "
    "independently of the book's figures, then compared. Tiers follow the author's "
    "standing doctrine: attested (standard tables, no cipher), derived (arithmetic on "
    "attested values), constructed (the author's cipher or seal, admitted as his)."
)
pdf.table(
    ["#", "Term", "Recomputation", "Book", "Result", "Tier"],
    [
        ["1", "\u039c\u03b1\u03b1\u03c4", "\u039c40+\u03b11+\u03b11+\u03c4300", "342", "PASS", "attested"],
        ["2", "Exalted (342+Mem)", "342 + \u05de40", "382", "PASS", "derived*"],
        ["3", "FAFO", "Vav6+Aleph1+Vav6+Ayin70", "83", "PASS", "constructed*"],
        ["4", "QASPARR", "17+1+19+16+1+18+18", "90", "PASS", "derived"],
        ["5", "\u039a\u03b1\u03c3\u03c0\u03b1\u03c1\u03c1", "20+1+200+80+1+100+100", "502", "PASS", "derived"],
        ["6", "\u039a\u03b1\u03c3\u03c0\u03b1\u03c1", "20+1+200+80+1+100", "402", "PASS", "derived"],
        ["7", "\u1f00\u03b3\u03ac\u03c0\u03b7", "1+3+1+80+8", "93", "PASS", "attested"],
        ["8", "\u03b8\u03ad\u03bb\u03b7\u03bc\u03b1", "9+5+30+8+40+1", "93", "PASS", "attested"],
        ["9", "BABALON", "2+1+2+1+30+70+50", "156", "PASS", "attested"],
        ["10", "AXONEME", "1+24+15+14+5+13+5", "77", "PASS", "attested"],
        ["11", "\u05e2\u05d6", "70+7", "77", "PASS", "attested"],
        ["12", "THE WORD", "20+8+5+23+15+18+4", "93", "PASS", "attested"],
        ["13", "\u05d7\u05db\u05de\u05d4", "8+20+40+5", "73", "PASS", "attested"],
        ["14", "\u05d3\u05e2\u05ea", "4+70+400", "474", "PASS", "attested"],
    ],
    widths=[10, 30, 58, 18, 20, 34],
    fs=8.5,
)
pdf.body(
    "* #2: the arithmetic is derived and verifies; the identification of 382 with the "
    "author's seal is stipulated \u2014 his coinage, admitted as his (Annex n. 10). "
    "* #3: the Hebrew letter assignment is the author's cipher throughout \u2014 verified "
    "arithmetically, flagged as his (Annex n. 7). Result: 14/14 PASS."
)

pdf.h2("Report B \u2014 TRVVTH Audit (claims vs. sources)")
pdf.body(
    "Method: every factual assertion in the book was checked against its cited source "
    "or recomputed. The ledger below is the complete account: 53 entries, zero falsehoods."
)
pdf.h3("B.1 \u2014 Verified: quotations (10)")
pdf.table(
    ["Claim", "Source checked", "Result"],
    [
        ["Murdock: \u201cfor the enjoyment\u201d", "319 U.S. 105, 113 (1943)", "Verbatim; precision fn. added"],
        ["Shuttlesworth Staub line", "394 U.S. 147 (1969)", "Verbatim"],
        ["Semayne's \u201c91a\u201d", "5 Co. Rep. 91a (1604)", "Corrected 91b\u219291a"],
        ["Duty keystone (violated right...)", "Crowley, \u201cDuty\u201d", "Verbatim"],
        ["Four duties quotations", "Crowley, \u201cDuty\u201d", "Verbatim (OCR corruptions fixed)"],
        ["Romans 13:10", "KJV", "Verbatim"],
        ["1 Cor. 13:12 (mirror)", "KJV", "Verbatim (first clause)"],
        ["AL I:3 (star)", "Liber AL vel Legis", "Verbatim; child-amendment flagged"],
        ["AL I:57 (love under will)", "Liber AL vel Legis", "Verbatim"],
        ["Duty subtitle & provenance", "O.T.O. docs listing", "Stated as listed, not A\u2234A\u2234"],
    ],
    widths=[52, 48, 70],
    fs=8.5,
)
pdf.h3("B.2 \u2014 Verified: legal & historical holdings (8)")
pdf.table(
    ["Claim", "Check", "Result"],
    [
        ["Yick Wo holding", "118 U.S. 356 (1886)", "Stated exactly; gloss flagged"],
        ["Boyd protections", "116 U.S. 616 (1886)", "Stated exactly"],
        ["Brandenburg standard", "395 U.S. 444 (1969)", "Stated exactly"],
        ["Supremacy Clause (counter)", "U.S. Const. Art. VI, cl. 2", "Stated; both sides given"],
        ["Cooper v. Aaron (counter)", "358 U.S. 1 (1958)", "Stated; both sides given"],
        ["Printz (counter, both ways)", "521 U.S. 898 (1997)", "Stated; both ways given"],
        ["Sheriff elected (Mich.)", "Mich. Const. Art. VII, \u00a74", "Verified"],
        ["Mack & Baldwin title", "Publication record", "Real book; cited as referral"],
    ],
    widths=[52, 48, 70],
    fs=8.5,
)
pdf.h3("B.3 \u2014 Verified: standard facts & mechanics (8)")
pdf.bullet("Grover diffusion D = 2|s><s| \u2212 I (inversion about the mean) \u2014 standard.")
pdf.bullet("Unitarity U\u2020U = I (reversibility) \u2014 standard.")
pdf.bullet("HXH = Z (basis-mirror) \u2014 standard.")
pdf.bullet("I Ching 63 (Chi Chi) / 64 (Wei Chi) \u2014 standard attributions.")
pdf.bullet("TARO = ROTA = TORA = ATOR \u2014 standard wheel.")
pdf.bullet("Achad Ma-Ion writings; Liber 31 \u2014 real (phantom title struck, n. 9).")
pdf.bullet("Nema, Maat Magick; Liber Pennae Praenumbra \u2014 real.")
pdf.bullet("\u201cmoor\u201d reversed = \u201croom\u201d (case-folded); \u201cnoon\u201d = \u201cno\u201d + reverse \u2014 mechanical.")
pdf.h3("B.4 \u2014 Flagged authorial (12) \u2014 admitted as his, not as theorem")
pdf.body(
    "Class A-L coinage \u00b7 the child-amendment of AL I:3 \u00b7 the Dictum of Ma'at \u00b7 the FAFO "
    "Hebrew cipher \u00b7 the 382 seal \u00b7 the Moor observation \u00b7 the Lilith/Mother Mary syncretism "
    "\u00b7 the Hobbes irony \u00b7 the UCC 1-201 Person/Individual dichotomy \u00b7 the Yick Wo gloss "
    "\u00b7 the quantum\u2013FAFO mapping \u00b7 the Etymological Trinity consecration. "
    "Each flies the \u2691 in the text. None is presented as derived; all are presented as his."
)
pdf.h3("B.5 \u2014 Open (1)")
pdf.body(
    "The issuance lunation \u2014 \u263d in 17\u00b032\u2032 Scorpio \u2014 is carried OPEN: no ephemeris was "
    "on hand at audit, and none has since been consulted. An open item is not a failed item; "
    "it is an item with its provenance showing, awaiting the author's ephemeris."
)
pdf.rule()
pdf.h2("Verdict")
pdf.body(
    "53 ledger entries: 40 verified, 12 flagged authorial, 1 open, 0 falsehoods. "
    "The TRVVTH audit PASSES. The PONTIFEX audit PASSES (14/14). "
    "This Teacher's Edition is released for the author's yay."
)
pdf.caption("Audited 2026-10-18 \u00b7 Scientific Illuminism \u00b7 93")

# ============================================================================
# COLOPHON
# ============================================================================
pdf.section_page()
pdf.h1("Colophon")
pdf.body(
    "This Teacher's Edition was built 2026-10-18 by the author's engine: the text "
    "reproduced whole from the Revised Edition (libers/liber-maat-revised-edition), "
    "the teaching written canon by canon, the tables and figures recomputed, the "
    "gallery curated, and both audits run entry by entry. No number was trusted; "
    "every one was recomputed. No quotation was trusted; every one was checked."
)
pdf.body(
    "Standing: the original Liber Ma'at stands. This edition implements the red-pen "
    "review of 2026-09-27, the TRVVTH amendment of 2026-09-28, the Achad amendment of "
    "2026-10-01, and the audit of 2026-10-18. It is offered for the author's review, "
    "correction, and \u2014 only if he wills it \u2014 adoption."
)
pdf.ln(6)
pdf.set_font("DejaVu", "B", 13); pdf.set_text_color(*GOLD)
pdf.multi_cell(0, 9, "Live, Love, and let Love, Live.", align="C",
               new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.ln(2)
pdf.set_font("DejaVu", "", 10); pdf.set_text_color(*MUT)
pdf.multi_cell(0, 7, "Johnathan 'Qasparr' (\u039a\u03b1\u03c3\u03c0\u03b1\u03c1\u03c1) Monroe, Keeper of the Secret Treasure\nAll Rights Reserved, Without Prejudice \u00b7 CashApp $axoneme",
               align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

pdf.output(OUT)
print("wrote", OUT, os.path.getsize(OUT), "bytes")
