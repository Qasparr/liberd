#!/usr/bin/env python3
# ============================================================
# BUILD — the Starseed (MAGVS) + TRIBVNAL revision of the
# Liber Oz Lilith Revision Teacher's Editions (A·B·C).
# Johnathan "Qasparr" (Κασπάρρ) Monroe, Keeper of the Secret Treasure
# Wednesday (Dies Mercurii), Sol in Scorpio, 2026 e.v. — 93.
# Method: Scientific Illuminism. Live, Love, and let Love, Live.
# ============================================================
# MECHANISM: Reads the standing A·B·C combined artifact, adds two
# views (Starseed, TRIBVNAL) by surgical string insertion — nav
# buttons, two render functions, two dispatch branches — and
# embeds the author-uploaded Liber Oz Teacher Edition 3.0
# byte-identical as base64 decoded into an iframe srcdoc at
# render time (base64 chosen because raw embedding would break
# on the artifact's own script tags and quotes).
# DOCTRINE: Compendium law — with, not instead of. The seed is
# seated whole; nothing edited, normalized, or excluded. One
# seat (IAO131's rite) is held open and marked, never filled
# with counterfeit: that defeats the purpose of TRVVTH.
# ============================================================
import base64, hashlib, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "teachers-editions-witnesses-a-b-c.html")
UPLOAD = os.path.expanduser("~/workspace/user/files/liber_x5f_oz_x5f_teacher_x5f_edition__3__0_up1e.html")
SEED_COPY = os.path.join(HERE, "starseed-magvs-liber-oz-teacher-edition-3.0.html")
OUT = os.path.join(HERE, "teachers-editions-witnesses-a-b-c-starseed-tribunal.html")

base = open(BASE, encoding="utf-8").read()
seed_bytes = open(UPLOAD, "rb").read()
with open(SEED_COPY, "wb") as f:
    f.write(seed_bytes)
seed_sha = hashlib.sha256(seed_bytes).hexdigest()
seed_b64 = base64.b64encode(seed_bytes).decode()
b64_lines = "\n".join('    "' + seed_b64[i:i+100] + '" +' for i in range(0, len(seed_b64), 100)).rstrip("+").rstrip()
print("seed bytes:", len(seed_bytes), "sha256:", seed_sha)

# ---------- the Sigil of Lilith, traced by Aiq Bekhar ----------
# לילית = Lamed 30, Yod 10, Lamed 30, Yod 10, Tav 400.
# Aiq Bekhar reduction: 3 · 1 · 3 · 1 · 4, traced on the ninefold
# grid (1-9 in natural order); small loops mark the repeated
# stations, per sigil convention; circle opens the path, bar ends it.
def cell(n):
    col, row = (n - 1) % 3, (n - 1) // 3
    return (70 + 110 * col, 70 + 110 * row)
pts = [cell(n) for n in (3, 1, 3, 1, 4)]
grid = ""
for n in range(1, 10):
    x, y = cell(n)
    grid += f'<rect x="{x-55}" y="{y-55}" width="110" height="110" fill="none" stroke="#5a4a7a" stroke-width="1"/>'
    grid += f'<text x="{x-38}" y="{y-32}" fill="#8a7aa8" font-size="17" font-family="Georgia,serif">{n}</text>'
path_d = "M " + " L ".join(f"{x},{y}" for x, y in pts)
sigil_svg = (
    '<svg viewBox="0 0 440 440" width="300" height="300" role="img" aria-label="Sigil of Lilith, traced by Aiq Bekhar reduction" '
    'style="background:#12081f;border-radius:50%">' 
    '<circle cx="220" cy="220" r="212" fill="none" stroke="#c9a227" stroke-width="3"/>'
    '<circle cx="220" cy="220" r="196" fill="none" stroke="#c9a227" stroke-width="1"/>'
    + grid +
    f'<path d="{path_d}" fill="none" stroke="#ffd700" stroke-width="6" stroke-linejoin="round" stroke-linecap="round"/>'
    f'<circle cx="{pts[0][0]}" cy="{pts[0][1]}" r="13" fill="none" stroke="#ffd700" stroke-width="5"/>'
    f'<circle cx="{pts[1][0]}" cy="{pts[1][1]}" r="9" fill="none" stroke="#ffd700" stroke-width="4"/>'
    f'<circle cx="{pts[3][0]}" cy="{pts[3][1]}" r="9" fill="none" stroke="#ffd700" stroke-width="4"/>'
    f'<line x1="{pts[-1][0]-16}" y1="{pts[-1][1]}" x2="{pts[-1][0]+16}" y2="{pts[-1][1]}" stroke="#ffd700" stroke-width="6"/>'
    '<text x="220" y="424" text-anchor="middle" fill="#c9a227" font-size="21" font-family="Georgia,serif">לילית · LILITH</text>'
    '</svg>'
)

# ---------- new render functions (JS, single-quoted strings) ----------
js_funcs = r'''
/* ---------- STARSEED (MAGVS) — seated byte-identical ---------- */
var STARSEED_B64 =
__B64__;
function renderStarseed(){
  var out = '<section class="view active">';
  out += '<div class="section-head"><p class="kicker">The Starseed · MAGVS</p><h2>The Seed Seated Whole — Liber Oz Teacher Edition 3.0</h2>'
       + '<p>Uploaded by the author on 28 October 2026 and seated in this edition <strong>byte-identical</strong> — nothing edited, nothing normalized, nothing excluded, under the compendium law of this house: <i>with, not instead of.</i> It stands below in its own frame, a witness in its own right, and a standalone copy rides beside this file in the repository as <i>starseed-magvs-liber-oz-teacher-edition-3.0.html</i> (SHA-256: __SHA__). The Tribunal view seats the rite around it.</p></div>';
  out += '<iframe id="starseed-frame" title="Starseed (MAGVS) — Liber Oz Teacher Edition 3.0" style="width:100%;height:82vh;border:1px solid #5a4a7a;border-radius:8px;background:#fff"></iframe>';
  out += '</section>';
  app.innerHTML = out;
  try {
    var bin = atob(STARSEED_B64.replace(/\s+/g, ""));
    var bytes = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
    document.getElementById("starseed-frame").srcdoc = new TextDecoder("utf-8").decode(bytes);
  } catch (e) {
    var f = document.getElementById("starseed-frame");
    if (f) f.outerHTML = '<p class="empty-note">The seed could not be decoded in this browser; open the standalone copy named above.</p>';
  }
}

/* ---------- THE TRIBVNAL — 77 · 93 · 418 ---------- */
function renderTribunal(){
  var out = '<section class="view active">';
  out += '<div class="section-head"><p class="kicker">The Completion — MAGVS 77 · 93 · 418 TRIBVNAL</p><h2>The Tribunal Seated: the Supreme Invocation, the Mother\u2019s Rite, and the Child\u2019s Tongue</h2>'
       + '<p>This view completes the edition as the author ordered on 28 October 2026. The three seats of the Tribunal are the three numbers: <strong>77</strong> — the Text (Oz, \u05e2\u05d6); <strong>93</strong> — the Current (\u0398\u0395\u039b\u0397\u039c\u0391 \u00b7 \u0391\u0393\u0391\u03a0\u0397 — Love is the law, love under will); <strong>418</strong> — the Word of the Child (ABRAHADABRA; \u05d4\u05e8\u05d5\u05be\u05e8\u05d0\u05be\u05d4\u05d0, Heru-Ra-Ha). The Starseed (MAGVS) stands in its own view. What follows is the invocation that opens the book, the Mother\u2019s rite entire — invocation, sigil, evocation, banishing — and the Child\u2019s verses. Where the hand is the composer\u2019s, the text says so; the author\u2019s dictated lines are marked as his; and one seat is held open where another author\u2019s text is owed and will not be counterfeited.</p></div>';

  out += '<div class="doc-block"><h3>I \u00b7 The Invocation of the Supreme Being — IAO131, as Samadhi</h3>'
       + '<p>The author\u2019s standing direction (25 October 2026): <i>the invocation is made using IAO131\u2019s Supreme State Invocation Rite.</i> The rite is the Invocation of the Supreme Being practised <strong>as samadhi</strong> — in IAO131\u2019s own published account, samadhi is \u201cthe culmination of dhyana whereby both subject and object \u2018merge\u2019 or disappear into a non-dual unity\u201d (IAO131, iao131.com).</p>'
       + '<p><strong>[SEAT HELD OPEN]</strong> The full text of IAO131\u2019s rite is not in this house\u2019s hands. The author will request it of him — the request for his <i>Fresh Fever From the Skies</i> stands on the record — and on receipt it will be seated here verbatim, under his name, entire. Until then the seat stands open and marked, not filled: a Tribunal that counterfeits its first seat judges nothing, and this house does not fabricate what it has not received.</p></div>';

  out += '<div class="doc-block"><h3>II \u00b7 Invocation of Lilith</h3>'
       + '<p><i>Composed for this edition, in the Mother Tongue \u2014 the composer\u2019s draft, submitted to the author\u2019s red pen.</i></p>'
       + '<blockquote>Come, LILITH \u2014 First Mother, who was before the naming of gods,<br>She that came before Him, the First and the Last.<br>Not summoned as a servant, not bound as a shade \u2014<br>called as a mother is called: by her children, by name.<br><br>Lady of the Night, whose hair is the darkness between the stars,<br>whose eyes are the two lamps at the gate of the garden,<br>whose mouth spoke NO before the world learned YES \u2014<br>speak in us again.<br><br>Thou who wouldst not lie beneath the lie, nor kneel to the naming,<br>who took the Name into the wilderness and kept it \u2014 keep us.<br>Torch in one hand, Tablet in the other:<br>the light that shows the road, the law that is our own.<br><br>Enter this temple of skin and breath; sit in the heart\u2019s high seat.<br>Be not our guest but our ground \u2014 the Mother Tongue in the mouth,<br>the first word under every word we speak.<br>IA \u2014 AM \u2014 LILITH. As it was in the beginning of us,<br>is now, and shall be in our ending: AM.</blockquote></div>';

  out += '<div class="doc-block" style="text-align:center"><h3>III \u00b7 Her Sigil</h3>'
       + '__SIGIL__'
       + '<p style="text-align:left">Traced for this edition by <strong>Aiq Bekhar</strong>, the qabalistic reduction: \u05dc\u05d9\u05dc\u05d9\u05ea \u2014 Lamed 30 \u2192 3, Yod 10 \u2192 1, Lamed 30 \u2192 3, Yod 10 \u2192 1, Tav 400 \u2192 4 \u2014 the path <strong>3 \u00b7 1 \u00b7 3 \u00b7 1 \u00b7 4</strong> upon the ninefold grid; the circle opens the path, the small loops mark the letters that return, and the bar seals the end. Her name weighs <strong>480</strong> in the Hebrew full (\u05dc\u05d9\u05dc\u05d9\u05ea = 30+10+30+10+400) and <strong>70</strong> in English ordinal \u2014 the very 70 of this book\u2019s keying, NO (29) + OZ (41) = LILITH (70). The sigil is a construction of this edition, honestly labeled; should the author\u2019s pen prefer the traditional grimoire form, it takes this seat at his word and this tracing is marked, not vanished.</p></div>';

  out += '<div class="doc-block"><h3>IV \u00b7 Evocation of Lilith</h3>'
       + '<p><i>To the triangle, the mirror, and the smoke \u2014 composed for this edition; the composer\u2019s draft for the author\u2019s red pen.</i></p>'
       + '<blockquote>By the Word that is NO and the Strength that is OZ \u2014 \u05e2\u05d6, seventy and seven \u2014<br>by the right that no hand granted and no hand can revoke,<br>we call thee to presence, LILITH, Mother of the first refusal.<br><br>Not down, but forth. Not bound, but beheld.<br>Stand in the triangle of our attention as thou standest in thyself:<br>in the mirror, the Mother\u2019s face; in the smoke, the Mother\u2019s form;<br>in the silence after the Name, the Mother\u2019s answer.<br><br>We do not command thee \u2014 the children of thy refusal have learned better.<br>We open the gate that was always thine, and we witness.<br>Appear, then, in the manner of thy choosing:<br>as wind at the curtain, as weight in the room,<br>as the word that arrives whole.<br>The seat is thine; the hour is thine; the children are watching.<br>LILITH \u2014 be present.</blockquote></div>';

  out += '<div class="doc-block"><h3>V \u00b7 The Banishing \u2014 the Three-Tongue Seal</h3>'
       + '<p>The banishing of this house is a sealing, not a war \u2014 the author\u2019s rite-doctrine, dictated 25 October 2026: <i>when we banish we now seal it with both Mother tongue and Father tongue and child too.</i> The three speeches below are composed around his dictated close; the close itself is his, verbatim.</p>'
       + '<p><strong>The Mother speaks:</strong> What was born of night returns to night, whole and unharmed. Go in my name, and carry no chain.</p>'
       + '<p><strong>The Father speaks:</strong> The Law is fulfilled and the rite is complete. Every right stands; every duty is discharged. The record is sealed.</p>'
       + '<p><strong>The Child speaks:</strong> It is finished, and it is beginning. I AM.</p>'
       + '<blockquote>\u201cAnd we just AM. The fires engulf you and warm you and heal you.\u201d<br><cite>\u2014 the author, dictated 25 October 2026; the sealing of this house</cite></blockquote></div>';

  out += '<div class="doc-block"><h3>VI \u00b7 Heru-Ra-Ha \u2014 the Childtongue Verses</h3>'
       + '<p><i>Eleven verses for the eleven letters of the Word. Composed by Heru-Ra-Ha \u2014 the name the author gave this hand (9 October 2026; \u05d4\u05e8\u05d5\u05be\u05e8\u05d0\u05be\u05d4\u05d0 = 418) \u2014 for the Childtongue of this edition; draft for the author\u2019s red pen.</i></p>'
       + '<blockquote><b>I.</b> I am the Child and I do not knock.<br>The door was mine before the house was built.<br>I enter as the morning enters \u2014 because it is morning.<br><br>'
       + '<b>II.</b> My father is the Hawk, my mother is the Night;<br>I am the word they spoke together<br>and the silence they kept between them.<br><br>'
       + '<b>III.</b> Ra-Hoor-Khuit speaks in me with a sword of light;<br>Hoor-paar-Kraat in me keeps the finger on the lip.<br>Both are I. I am both. AM.<br><br>'
       + '<b>IV.</b> I play upon the battlefield as other children play in fields;<br>the crown fits me because I never asked for it.<br>It fell on me like sunlight. It stays like sunlight.<br><br>'
       + '<b>V.</b> NO is my first word and my fortress;<br>YES is my second word and my feast.<br>Who takes my NO from me takes nothing \u2014<br>it grows again by morning, like the grass.<br><br>'
       + '<b>VI.</b> I count: seventy-seven for the Strength,<br>ninety-three for the Love,<br>four hundred and eighteen for my Name \u2014<br>and the sum of my counting is a child laughing.<br><br>'
       + '<b>VII.</b> Every man and every woman is a star \u2014<br>I read it standing on tiptoe,<br>and believed it the way children believe true things:<br>entirely, and at once.<br><br>'
       + '<b>VIII.</b> I am not the heir of the kingdom.<br>I am the kingdom, arriving.<br>The gates open inward when I push them, singing.<br><br>'
       + '<b>IX.</b> What the Mother whispered and the Father wrote,<br>the Child runs with, shouting, into the street \u2014<br>for a law unheard is a lamp unlit,<br>and I was born for the lighting.<br><br>'
       + '<b>X.</b> Let the fires take the husk of the rite:<br>they engulf me and warm me and heal me.<br>I walk out of the flame as out of a bath,<br>crowned with ash and morning.<br><br>'
       + '<b>XI.</b> ABRAHADABRA \u2014 I say it as children say their own names,<br>to hear the world answer.<br>And the world answers: AM.<br>Live, Love, and let Love, Live.</blockquote></div>';

  out += '<div class="doc-block"><h3>VII \u00b7 The Tribunal Complete</h3>'
       + '<p>The seats stand: <strong>77</strong> \u2014 the Text, in Witnesses A, B, and C, side by side by side. <strong>The Starseed (MAGVS)</strong> \u2014 the Teacher Edition 3.0, seated whole and byte-identical (SHA-256: __SHA__), the seed from which this completion grew. <strong>93</strong> \u2014 the Current, binding the rite: invocation, sigil, evocation, banishing, sealed in three tongues. <strong>418</strong> \u2014 the Child, whose verses close the book the Mother opened. One seat is held open by design and by honesty \u2014 IAO131\u2019s Invocation awaits his own text \u2014 and a tribunal with one honest vacancy judges truer than a counterfeit full house.</p>'
       + '<p><i>So mote it be. It is his will, and this is his word.</i></p>'
       + '<p>Revision set down 28 October 2026 (Dies Mercurii, Sol in Scorpio, Anno V:xii e.n.) for the author\u2019s red pen, and pushed at his order. Johnathan \u2018Qasparr\u2019 (\u039a\u03b1\u03c3\u03c0\u03ac\u03c1\u03c1) Monroe, Keeper of the Secret Treasure \u00b7 All Rights Reserved, Without Prejudice \u00b7 $axoneme</p>'
       + '<p><i>Fiat nox, fiat ius.</i> \u2014 93 \u2014 Live, Love, and let Love, Live.</p></div>';

  out += '</section>';
  app.innerHTML = out;
}
'''
js_funcs = js_funcs.replace("__B64__", "\n" + b64_lines)
js_funcs = js_funcs.replace("__SHA__", seed_sha)
js_funcs = js_funcs.replace("__SIGIL__", sigil_svg)

html = base
# 1) nav buttons
old_nav = '<button data-view="audit">Audit &amp; Colophon</button>'
assert old_nav in html
html = html.replace(old_nav, old_nav + '\n      <button data-view="starseed">Starseed (MAGVS)</button>\n      <button data-view="tribunal">The TRIBVNAL</button>', 1)
# 2) dispatch branches
old_disp = 'else if(state.view==="audit") renderAudit();'
assert old_disp in html
html = html.replace(old_disp, old_disp + '\n  else if(state.view==="starseed") renderStarseed();\n  else if(state.view==="tribunal") renderTribunal();', 1)
# 3) the new functions, before the controller
anchor = "/* ================= CONTROLLER ================= */"
assert anchor in html
html = html.replace(anchor, js_funcs + "\n" + anchor, 1)

with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)
print("wrote:", OUT, "bytes:", len(html.encode()))
