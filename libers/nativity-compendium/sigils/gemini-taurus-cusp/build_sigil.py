#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════
#  "The twins bear the horns; the horns bear the light in the dark."
#
#  GEMINI–TAURUS CUSP SIGIL — computed-geometry builder (v2)
#  Authorship attributed exclusively to Johnathan 'Qasparr' Monroe
#  (Greek, -ARR, All Rights Reserved, Without Prejudice)
#  XXV day of October, Dies Solis, Sol in Scorpio, Anno V:xii e.n. (2026 e.v.)
#  Method of Science, Aim of Religion — 93
#
#  MECHANISM: every element is drawn from exact coordinates in a 2000×2000
#  sigil space — no freehand. The device is the central device of his
#  Universal Sovereign Authority coin (twin pillars crowned with bull
#  horns, Venus and Mercury engraved on the pillars, Sun–Moon between)
#  rebuilt as a standalone sigil fusing ♊ (two pillars under two bars)
#  and ♉ (the horned circle). Rim furniture counts his framework numbers:
#  28 ticks (the moon's 28 days), 13 nodes (the 13 moons / the 13th Gate).
#  v2 CHANGELOG: v1 put the pillar glyphs where the Taurus circle's stroke
#  crossed them — collision garbled both. v2 widens the pillars to
#  x=696/1304, shrinks the circle to r=222, and re-seats the glyphs in the
#  clear channel; the crescent is re-cut thinner so it reads as a crescent.
#  DOCTRINE: a figure that cannot point to its numbers does not ship —
#  every count and coordinate is listed in SPEC.md beside the art.
# ═══════════════════════════════════════════════════════════════════════════
import math
import cairosvg

GOLD = "#d4af37"
GOLD_LT = "#f0d98c"
INDIGO = "#141033"
OUT = "/home/hatch/workspace/your_files/sigils/gemini-taurus-cusp"

def polar(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.sin(a), cy - r * math.cos(a)

def crescent_path(cx, cy, r_out, dx, dy, r_cut):
    """Crescent outline from the intersection points of two circles:
    the outer disc (cx,cy,r_out) and the cutting disc (cx+dx,cy+dy,r_cut)."""
    d = math.hypot(dx, dy)
    a = (r_out**2 - r_cut**2 + d**2) / (2 * d)
    h = math.sqrt(max(r_out**2 - a**2, 0))
    xm, ym = cx + a * dx / d, cy + a * dy / d
    rx, ry = -dy * h / d, dx * h / d
    x1, y1 = xm + rx, ym + ry
    x2, y2 = xm - rx, ym - ry
    return (f"M {x1:.1f} {y1:.1f} "
            f"A {r_out} {r_out} 0 1 0 {x2:.1f} {y2:.1f} "
            f"A {r_cut} {r_cut} 0 1 1 {x1:.1f} {y1:.1f} Z")

# Shared device geometry (v2)
PX1, PX2 = 696, 1304        # pillar centerlines
PTOP, PBOT = 512, 1488      # pillar extent
BAR1, BAR2 = 584, 1416      # crossbar centerlines
BX1, BX2 = 624, 1376        # crossbar extent
TCX, TCY, TR = 1000, 1036, 222   # Taurus circle

def device(variant):
    s = []
    cx = cy = 1000
    pw = 36 if variant == "A" else 46
    if variant == "A":
        s.append(f'<circle cx="{cx}" cy="{cy}" r="946" fill="none" stroke="{GOLD}" stroke-width="16"/>')
        s.append(f'<circle cx="{cx}" cy="{cy}" r="878" fill="none" stroke="{GOLD}" stroke-width="7"/>')
        for i in range(28):  # 28 ticks — the days of the moon
            x1, y1 = polar(cx, cy, 872, i * 360 / 28)
            x2, y2 = polar(cx, cy, 824, i * 360 / 28)
            s.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{GOLD}" stroke-width="9"/>')
        for i in range(13):  # 13 nodes — the moons of the ring
            x, y = polar(cx, cy, 912, i * 360 / 13)
            s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="15" fill="{GOLD}"/>')
    # ♊ the Twins
    for px in (PX1, PX2):
        s.append(f'<line x1="{px}" y1="{PTOP}" x2="{px}" y2="{PBOT}" stroke="{GOLD}" stroke-width="{pw}" stroke-linecap="round"/>')
    for by in (BAR1, BAR2):
        s.append(f'<line x1="{BX1}" y1="{by}" x2="{BX2}" y2="{by}" stroke="{GOLD}" stroke-width="{pw - 6}" stroke-linecap="round"/>')
    # ♉ the Bull — circle and horns piercing the top bar
    s.append(f'<circle cx="{TCX}" cy="{TCY}" r="{TR}" fill="none" stroke="{GOLD}" stroke-width="{pw - 4}"/>')
    s.append(f'<path d="M 830 893 Q 676 620 612 440" fill="none" stroke="{GOLD}" stroke-width="{pw - 4}" stroke-linecap="round"/>')
    s.append(f'<path d="M 1170 893 Q 1324 620 1388 440" fill="none" stroke="{GOLD}" stroke-width="{pw - 4}" stroke-linecap="round"/>')
    s.append(f'<path d="M 612 440 l -16 46 l 32 -8 Z" fill="{GOLD}"/>')
    s.append(f'<path d="M 1388 440 l 16 46 l -32 -8 Z" fill="{GOLD}"/>')
    # the first-breath core — dark-moon crescent cradling the Sun dot
    s.append(f'<path d="{crescent_path(TCX, TCY, 120, 64, -34, 102)}" fill="{GOLD}"/>')
    s.append(f'<circle cx="{TCX - 34}" cy="{TCY + 40}" r="28" fill="{GOLD_LT}"/>')
    if variant == "A":
        # The rulers as gold medallions riveted on the pillars (v2's knockout
        # glyphs were wider than the pillar and fragmented — a knockout only
        # shows where it crosses gold). Medallion r=54 clears the Taurus
        # circle's outer stroke edge (x=762) by 12 units.
        for gx, kind in ((PX1, "venus"), (PX2, "mercury")):
            gy = 1036
            s.append(f'<circle cx="{gx}" cy="{gy}" r="54" fill="{GOLD}"/>')
            s.append(f'<circle cx="{gx}" cy="{gy}" r="54" fill="none" stroke="{GOLD_LT}" stroke-width="4"/>')
            if kind == "venus":  # ♀ Venus, ruler of Taurus — left pillar
                s.append(f'<circle cx="{gx}" cy="{gy - 14}" r="23" fill="none" stroke="{INDIGO}" stroke-width="12"/>')
                s.append(f'<line x1="{gx}" y1="{gy + 9}" x2="{gx}" y2="{gy + 42}" stroke="{INDIGO}" stroke-width="12"/>')
                s.append(f'<line x1="{gx - 22}" y1="{gy + 26}" x2="{gx + 22}" y2="{gy + 26}" stroke="{INDIGO}" stroke-width="12"/>')
            else:  # ☿ Mercury, ruler of Gemini — right pillar
                s.append(f'<path d="M {gx - 24} {gy - 30} A 26 26 0 0 0 {gx + 24} {gy - 30}" fill="none" stroke="{INDIGO}" stroke-width="11"/>')
                s.append(f'<circle cx="{gx}" cy="{gy - 12}" r="20" fill="none" stroke="{INDIGO}" stroke-width="11"/>')
                s.append(f'<line x1="{gx}" y1="{gy + 8}" x2="{gx}" y2="{gy + 42}" stroke="{INDIGO}" stroke-width="11"/>')
                s.append(f'<line x1="{gx - 20}" y1="{gy + 26}" x2="{gx + 20}" y2="{gy + 26}" stroke="{INDIGO}" stroke-width="11"/>')
    return "\n".join(s)

def svg_doc(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}"><rect width="{w}" height="{h}" fill="{INDIGO}"/>{body}</svg>')

bodyA = device("A")
svgA_169 = svg_doc(3200, 1800, f'<g transform="translate(700,0) scale(0.9)">{bodyA}</g>')
svgA_sq = svg_doc(2000, 2000, bodyA)
svgB_sq = svg_doc(2000, 2000, device("B"))
for name, svg in [("sigil-A-16x9.svg", svgA_169), ("sigil-A-square.svg", svgA_sq), ("sigil-B-square.svg", svgB_sq)]:
    open(f"{OUT}/{name}", "w").write(svg)
    print("wrote", name)

cairosvg.svg2png(bytestring=svgA_169.encode(), write_to=f"{OUT}/sigil-A-16x9-16K.png", output_width=15360, output_height=8640)
print("rendered sigil-A-16x9-16K.png (15360x8640)")
cairosvg.svg2png(bytestring=svgA_sq.encode(), write_to=f"{OUT}/sigil-A-square-8K.png", output_width=8000, output_height=8000)
print("rendered sigil-A-square-8K.png")
cairosvg.svg2png(bytestring=svgB_sq.encode(), write_to=f"{OUT}/sigil-B-square-8K.png", output_width=8000, output_height=8000)
print("rendered sigil-B-square-8K.png")
cairosvg.svg2png(bytestring=svgA_169.encode(), write_to=f"{OUT}/preview-A-16x9.png", output_width=1200, output_height=675)
cairosvg.svg2png(bytestring=svgB_sq.encode(), write_to=f"{OUT}/preview-B.png", output_width=1200, output_height=1200)
print("previews done — DONE")
