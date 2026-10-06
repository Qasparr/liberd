#!/usr/bin/env python3
# ============================================================================
#  LIBER XXXII — THE BOOK OF THE CELL — ILLUMINATED EDITION BUILDER
#  "And God saw every thing that he had made, and, behold, it was very good."
#   — Genesis 1:31 (KJV)
#
#  Date:   2026-10-06 (Tuesday)
#  93.
#
#  Authorship: Johnathan 'Qasparr' (Κασπάρρ) Monroe, Keeper of the Secret Treasure
#  Method:     Scientific Illuminism — the Book dressed for keeping.
#
#  MECHANISM: This script sets Liber Cell as an illuminated edition. The
#             Markdown text is poured chapter by chapter; the frontispiece,
#             the three commemorative plates, the Renaissance accompaniments,
#             and the three microscopy witnesses are interleaved at their
#             stations, each with a caption, and every borrowed photograph
#             carries its provenance. WebP art is converted to PNG via PIL
#             because the PDF writer wants raster it can trust.
#  DOCTRINE:  An illuminated book teaches twice — once in the word, once in
#             the image. The plates argue; the Renaissance pieces adore; the
#             micrographs witness. None is decoration. The captions are part
#             of the argument, and the attributions are part of the honesty.
#
#  "Live, Love, and let Love, Live." — 93.
# ============================================================================

import os
import re
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from PIL import Image

# MECHANISM: all paths resolve against the liber's own directory, so the
# Book carries its illustrations with it wherever the canon goes.
_HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(_HERE, "Liber_Cell.md")
DST = os.path.join(_HERE, "Liber_Cell_Illuminated.pdf")
FIG = os.path.join(_HERE, "figs")
REN = os.path.join(FIG, "renaissance")
PLT = os.path.join(FIG, "plates")
MIC = os.path.join(FIG, "microscopy")

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

FRONTISPIECE = (os.path.join(REN, "frontispiece.webp"),
                "Frontispiece — the dividing cell under divine light")
EVE = None  # superseded by the author's ruling — Lilith holds the seat
LILITH = (os.path.join(REN, "lilith-maternal.webp"),
          "Lilith, the Mother of Hvmanity")
RIB = (os.path.join(REN, "rib-coincidence.webp"),
       "The deep sleep — the rib unfolded into dividing cells")
MANY = (os.path.join(REN, "many-as-one.webp"),
        "The many becoming the one — Many == Elohim")
CHARIOT = (os.path.join(REN, "chariot-kaos.webp"),
           "The Chariot — the Mother is the vehicle, the Father drives into Kaos")
RE_OOCYTE = (os.path.join(REN, "oocyte-states.webp"),
             "Reimagined I — the egg in its two states: fertilized (sun) and dormant (moon)")
RE_MICRO = (os.path.join(REN, "oocyte-microscopy.webp"),
            "Reimagined II — the microscopy of the egg, as a natural-philosophy plate")
RE_MOON = (os.path.join(REN, "moon.webp"),
           "Reimagined III — the moon in her crescent, measurer of months")
RE_PENTA = (os.path.join(REN, "pentagram.webp"),
            "Reimagined IV — the pentagram of numbers, 111 through 999")
RE_LILITH = (os.path.join(REN, "lilith-throned.webp"),
             "Reimagined V — Lilith enthroned, the Mother in her dark majesty")
RE_REDMOTHER = (os.path.join(REN, "red-mother.webp"),
                "Reimagined VI — the Red Mother under the blood moon")
RE_EAGLE = (os.path.join(REN, "double-eagle.webp"),
            "Reimagined VII — the double eagle, the two the one became")
RE_SIGIL = (os.path.join(REN, "sigil-scales.webp"),
            "Reimagined VIII — the sigil of the scales between the pillars 11 and 22")
PLATE1 = (os.path.join(PLT, "The-Unified-Syntax-Fig1-Mitosis-Plate.png"),
          "Plate I — Mitosis: the one becomes two")
PLATE2 = (os.path.join(PLT, "The-Unified-Syntax-Fig2-Meiosis-Plate.png"),
          "Plate II — Meiosis: the halving that assigns")
PLATE3 = (os.path.join(PLT, "The-Unified-Syntax-Fig3-Mitochondria-Plate.png"),
          "Plate III — The splitting of the mitochondria")
WITNESSES = [
    (os.path.join(MIC, "mitosis-onion.jpg"),
     "Witness I — Mitosis in onion skin cells, 20x magnification. Via Wikimedia Commons."),
    (os.path.join(MIC, "meiosis.jpg"),
     "Witness II — Meiosis, light micrograph. Via Wikimedia Commons."),
    (os.path.join(MIC, "mitochondria-tem.png"),
     "Witness III — Mitochondria, transmission electron micrograph (MEF cells). Via Wikimedia Commons."),
]


def as_png(path):
    # MECHANISM: normalize every illustration to PNG on a scratch copy.
    # DOCTRINE: the builder never mutates the archive's originals.
    if path.lower().endswith(".png"):
        return path
    im = Image.open(path).convert("RGB")
    out = path + ".print.png"
    im.save(out)
    return out


class LiberPDF(FPDF):
    def footer(self):
        # MECHANISM: every page declares the Book it belongs to.
        if self.page_no() <= 2:
            return
        self.set_y(-15)
        self.set_font("DejaVu", "", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, "LIBER XXXII — Liber Cell — The Book of the Cell",
                  align="C", new_x="LMARGIN", new_y="NEXT")


def image_page(pdf, path, caption):
    # MECHANISM: one illustration per page, centered, captioned beneath.
    # DOCTRINE: an image given its own page is an image taken seriously.
    pdf.add_page()
    png = as_png(path)
    pdf.ln(6)
    max_w = pdf.w - pdf.l_margin - pdf.r_margin
    max_h = pdf.h - pdf.t_margin - pdf.b_margin - 30
    with Image.open(png) as im:
        iw, ih = im.size
    scale = min(max_w / iw, max_h / ih)
    w, h = iw * scale, ih * scale
    x = (pdf.w - w) / 2
    pdf.image(png, x=x, y=pdf.get_y(), w=w, h=h)
    pdf.set_y(pdf.get_y() + h + 4)
    pdf.set_font("DejaVu", "", 9)
    pdf.set_text_color(90, 90, 90)
    pdf.multi_cell(0, 6, caption, new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.set_text_color(0, 0, 0)


def _set(pdf, line, size, bold=False):
    # MECHANISM: the ∴ glyph lives in DejaVu Sans, not Serif — any line
    # carrying it is set in Sans so the A∴A∴ sigil never prints as tofu.
    # DOCTRINE: the sigil must print.
    fam = "DejaVuSans" if "∴" in line else "DejaVu"
    pdf.set_font(fam, "B" if bold else "", size)


def pour_text(pdf, text):
    for raw in text.splitlines():
        s = raw.rstrip()
        if s.startswith("## "):
            pdf.ln(4)
            _set(pdf, s, 14, bold=True)
            pdf.multi_cell(0, 9, s[3:].strip(), new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)
        elif s.startswith("# "):
            continue
        elif s.startswith("> "):
            pdf.set_font("DejaVu", "", 10)
            pdf.set_x(pdf.l_margin + 8)
            pdf.multi_cell(pdf.w - pdf.l_margin - pdf.r_margin - 8, 6,
                           s[2:].replace("**", ""), new_x="LMARGIN", new_y="NEXT")
        elif s.startswith("---"):
            pdf.ln(4)
        elif not s.strip():
            pdf.ln(3)
        elif re.match(r"^\d+\.\s", s):
            _set(pdf, s, 10.5)
            pdf.multi_cell(0, 6, s.replace("**", ""), new_x="LMARGIN", new_y="NEXT")
        else:
            _set(pdf, s, 10.5)
            pdf.multi_cell(0, 6, s.replace("**", "").replace("*", ""),
                           new_x="LMARGIN", new_y="NEXT", align="J")


def build():
    with open(SRC, encoding="utf-8") as f:
        md = f.read()

    pdf = LiberPDF()
    pdf.set_auto_page_break(True, margin=20)
    pdf.add_font("DejaVu", "", SERIF)
    pdf.add_font("DejaVu", "B", SERIF_B)
    pdf.add_font("DejaVuSans", "", SANS)
    pdf.add_font("DejaVuSans", "B", SANS_B)
    pdf.set_margins(22, 20, 22)

    # -- Title page ------------------------------------------------------
    pdf.add_page()
    pdf.ln(45)
    pdf.set_font("DejaVu", "B", 30)
    pdf.multi_cell(0, 14, "LIBER XXXII", align="C",
                   new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("DejaVu", "B", 20)
    pdf.multi_cell(0, 11, "Liber Cell", align="C",
                   new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("DejaVu", "", 13)
    pdf.multi_cell(0, 8, "The Book of the Cell \u00b7 The Genesis Code",
                   align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_font("DejaVu", "", 10)
    for t in ["CELL = 32 \u2014 the number of the Book",
              "Johnathan 'Qasparr' (\u039a\u03b1\u03c3\u03c0\u03ac\u03c1\u03c1) Monroe, Keeper of the Secret Treasure",
              "2026-10-06 \u2014 Method: Scientific Illuminism. 93.",
              "All Rights Reserved, Without Prejudice.",
              "Illuminated edition \u2014 with plates, Renaissance accompaniments,",
              "and three microscopy witnesses."]:
        pdf.multi_cell(0, 7, t, align="C", new_x="LMARGIN", new_y="NEXT")

    # -- Frontispiece ----------------------------------------------------
    image_page(pdf, *FRONTISPIECE)

    # -- Body: split at chapter headings; preamble first -----------------
    # MECHANISM: chapters are delimited by "## I." style headings; each
    # chapter pours its text, then its station image follows.
    # DOCTRINE: the image answers the chapter — never precedes it.
    chunks = re.split(r"(?m)^(## [IVX]+\..*)$", md)
    # chunks[0] = preamble (title block + epigraph + doctrine statement)
    pdf.add_page()
    pour_text(pdf, chunks[0])

    stations = {1: (PLATE1, RIB), 2: (PLATE2,), 3: (PLATE3, LILITH),
                4: (MANY,), 5: (), 6: (), 7: (), 8: (CHARIOT,),
                9: (RE_OOCYTE, RE_MICRO, RE_MOON, RE_PENTA),
                10: (),
                11: (RE_LILITH, RE_REDMOTHER, RE_EAGLE, RE_SIGIL)}
    ci = 0
    for j in range(1, len(chunks), 2):
        heading, body = chunks[j], chunks[j + 1] if j + 1 < len(chunks) else ""
        ci += 1
        pdf.add_page()
        pour_text(pdf, heading + "\n" + body)
        for path, caption in stations.get(ci, ()):
            image_page(pdf, path, caption)

    # -- The Witnesses ---------------------------------------------------
    pdf.add_page()
    pdf.set_font("DejaVu", "B", 14)
    pdf.multi_cell(0, 9, "THE WITNESSES", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_font("DejaVu", "", 10.5)
    pdf.multi_cell(0, 6,
                   "The doctrine is the author's; the mechanisms are not. "
                   "These three photographs are the public record — what the "
                   "instruments saw, independent of any reading. Mitosis, "
                   "meiosis, and the mitochondrion, as the microscopes found them.",
                   new_x="LMARGIN", new_y="NEXT", align="J")
    for path, caption in WITNESSES:
        image_page(pdf, path, caption)

    # -- Colophon ---------------------------------------------------------
    pdf.add_page()
    pdf.ln(60)
    pdf.set_font("DejaVu", "", 11)
    for t in ["Here ends the illuminated edition of",
              "LIBER XXXII — Liber Cell, the Book of the Cell,",
              "set down 2026-10-06 by the order of the author.",
              "",
              "93. \"Live, Love, and let Love, Live.\"",
              "",
              "Johnathan 'Qasparr' (\u039a\u03b1\u03c3\u03c0\u03ac\u03c1\u03c1) Monroe,",
              "Keeper of the Secret Treasure",
              "All Rights Reserved, Without Prejudice."]:
        pdf.multi_cell(0, 8, t, align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.output(DST)
    print("wrote %s (%d pages)" % (DST, pdf.page_no()))


if __name__ == "__main__":
    build()
