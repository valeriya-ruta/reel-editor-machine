# -*- coding: utf-8 -*-
"""Reel 51 — «Твій стиль з першого дня». Posts 2026-10-25.

Google style + Excalidraw (STYLE.md §00), the reel-41 skeleton, her review of
reel 41 applied (word-rail captions, stickers / halos over the footage, long
arrows, the comment pointer points down).

The one object is **the two reels** — «1» and «2», a blind test. They are
dealt above her on the hook, come back small for the verdict (2 is wrong, 1 is
the AI, 2 the editor), multiply into «any editing» and her style, and return
once more for the answer to «AI can't edit as well» (≠ turns into =).

THE PAUSE (5.233–15.233 on the plate, the empty-text clip of cut.json) is
EMPTY — her call: she drops the two comparison reels in herself, in her
editor. Nothing of ours is on screen or in the sfx there: no cover, no frames,
no captions, no plaque, no cues. Only the plate (and the kit's slow push).

  above   two phones «1» «2», a muted speaker, «?» — gone before the pause
  —       the pause: her plate only
  above   verdict: 2 ringed, crossed; 1 ringed → «штучний інтелект»,
          2 → «монтажерка»; arrow 2 → 1 on «відтворити»; four edit styles,
          one ringed → «твій стиль»
  behind  «200 €»
  above   card: платити монтажеру / чекати на відео / залежати від її часу й
          хвороб — each struck on its noun
  half    зняти рілс → Claude → 20 хв → готовий результат
  above   1 and 2 again: a speech bubble, ≠ on «не може», = on «так само добре»
  half    ліміти: справжній креатив above the line; «креатив» below it —
          red subtitles, CapCut €
  above   CTA — блогерка / СММниця / підприємиця / продюсерка, 24/7 + a full
          battery, «Став + в коментарі», a pointer down to the comments

usage: python build.py [--words]   (then mattes; render is the orchestrator's)
"""
import io
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
from gstyle import G, Words, load_caps, mark, esc  # noqa: E402

NN = "51"
CUT = json.load(io.open(os.path.join(ROOT, "work", "r" + NN, "cut.json"), encoding="utf-8"))
DUR = 70.516           # (2116 plate frames - 0.5) / 30

# the pause: clip 1 of cut.json, the only clip with no text — left EMPTY
HOLD = [c for c in CUT["clips"] if not c["text"].strip()][0]
H0, H1 = HOLD["tl"], HOLD["tl"] + HOLD["dur"]            # 5.233 – 15.233


class G51(G):
    """The kit's word rail ends each word where the next begins: «ІНТЕЛЕКТ.»
    would then sit on her plate through the whole 10 s pause. A word followed
    by a silence over 1 s leaves 0.3 s after she stops — and the word before
    the pause leaves as she stops, before the plate cuts into it."""

    def words(self, chunks, js, blackout=()):
        html, j = G.words(self, chunks, js, blackout)
        ws = [w for c in chunks for w in c["words"]]
        for i, (a, b) in enumerate(zip(ws, ws[1:])):
            if b["s"] - a["e"] > 1.0:
                end = a["e"] + 0.3
                if a["s"] < H0 <= b["s"]:
                    end = min(end, H0 - 0.02)
                j = re.sub(r'(tl\.set\("#w%d", \{autoAlpha: 0\}, )[\d.]+\)' % i, r'\g<1>%.3f)' % end, j)
        # the plaque coming back after a blackout and standing down for a half
        # screen 0.1 s later is a blink (37.85 → 37.99): it holds under the white
        # words in between («Вона може») and leaves as the panel's ink words take over
        sc = sorted((float(m.group(2)), int(m.group(1)), m.group(0)) for m in
                    re.finditer(r'tl\.to\("#scrim", \{autoAlpha: ([01]), duration: [\d.]+\}, ([\d.]+)\)', j))
        for (t1, v1, _), (t2, v2, s2) in zip(sc, sc[1:]):
            if v1 == 1 and v2 == 0 and t2 < t1 + 0.25:
                j = j.replace(s2, s2.replace("%.3f)" % t2, "%.3f)" % (t1 + 0.40)))
        return html, j


g = G51(dur=DUR, reel=NN)

# whisper's spelling of what she plainly said -> her word (re-heard on the plate)
FIX = {
    u"надварив": u"на два рілси", u"себе": u"без",
    u"Клоді": u"стилі.",                 # she said «в твоєму стилі» (script: «у твоєму Клоді»)
    (u"місяць,", 32.0): None,                    # aligner echo at the 32.0 join
    (u"стосуються", 52.1): None,                 # aligner echo at the 52.13 join
    u"ліміти": u"Ліміти",
    u"натормити": u"отримати",
    u"мірілся": u"мій рілс — це",               # re-heard: «Тому мій рілс — це відповідь»
    (u"що", 46.5): None, u"читаєте": u"штучний", u"лайк,": u"інтелект",   # re-heard: «штучне талак»
    (u"другий", 20.4): u"другий —",
    u"SMM": u"СММниця,", u"нація,": None, u"підприємуця": u"підприємиця",
}
CAPS = load_caps(NN, FIX)


def one_word(caps):
    """The rail shows one word at a time: whisper's merged tokens («то став»,
    «а не») and FIX's «на два рілси» are split, the time shared by letters;
    a bare dash stays with its word."""
    out = []
    for c in caps:
        parts = []
        for p in c["w"].split():
            if parts and not any(ch.isalnum() for ch in p):
                parts[-1] += u" " + p
            else:
                parts.append(p)
        if len(parts) == 1:
            out.append(c)
            continue
        n = float(sum(len(p) for p in parts))
        t, d = c["s"], c["e"] - c["s"]
        for p in parts:
            dd = d * len(p) / n
            out.append(dict(c, w=p, s=round(t, 3), e=round(t + dd - 0.02, 3)))
            t += dd
    return out


CAPS = one_word(CAPS)
# «інтелект.» is stretched over the pause by the aligner; she stops at 5.23
for _c in CAPS:
    if _c["w"] == u"інтелект." and _c["s"] < H0:
        _c["e"] = round(H0 - 0.02, 3)
W = Words(CAPS)
S, E = W.s, W.e

# ---------------------------------------------------------------- the beats
B, P, F, C, J = [], [], [], [], []     # behind / panel / front / cover html, js
BLACKOUT = []
PLACE = []                             # caption placement over the half screens
HALF = []


def js(s):
    J.append(s)


EXTRA_CSS = u"""
    /* a phone: a reel in a bezel */
    .ph { position: absolute; box-sizing: border-box; background: #fff; border: 6px solid #241919;
          border-radius: 30px; overflow: hidden;
          box-shadow: 0 1px 3px rgba(36,25,25,.10), 0 10px 30px rgba(36,25,25,.10); }
    .ph .scr { position: absolute; left: 0; top: 0; width: 100%; height: 100%; background: #FFF0F0; }
    .ph .n { position: absolute; left: 0; width: 100%; top: 50%; margin-top: -60px; text-align: center;
             font-family: "Pangolin", cursive; font-size: 110px; line-height: 120px; color: #1E1E1E; }
    .ph .b { position: absolute; display: block; }
    .ctr { position: absolute; display: flex; justify-content: center; }
    /* a strike across a chip on the white card: an HTML bar in her red, not a
       sketch — a haloed ink line wiped the chip text out (snapshot 37.5) */
    .strk { position: absolute; left: -8px; right: -8px; top: 50%; height: 6px; margin-top: -1px;
            border-radius: 3px; background: #7A1424; transform-origin: 0 50%; transform: scaleX(0); }
"""

# sketch helpers on top of gstyle's (open strokes only: a closed outline over
# the footage goes through the kit's blob(), which makes it a sticker)
js(u'''
  function cross(name, x1, y1, x2, y2, o) {
    var o2 = {}; for (var k in (o || {})) o2[k] = o[k]; o2.seed = ((o && o.seed) || 81) + 2;
    ln(name, x1, y1, x2, y2, o); ln(name, x2, y1, x1, y2, o2); }
  function tick(name, x, y, o) { var s = SK[name], k = (o && o.k) || 1;
    _add(s, s.rc.linearPath([[x - 34 * k, y], [x - 8 * k, y + 28 * k], [x + 40 * k, y - 34 * k]], opt(o, (o && o.seed) || 71))); }
''')


def path_d(pts):
    return u"M" + u" L".join(u"%g %g" % p for p in pts) + u" Z"


def bubble_d(cx, cy, rx, ry, tip, a1=100, a2=125):
    """A speech bubble as ONE closed outline (an oval with a tail at the lower
    left), so over the footage the kit makes it a single white sticker."""
    p = lambda a: (round(cx + rx * math.cos(math.radians(a)), 1), round(cy + ry * math.sin(math.radians(a)), 1))
    (x1, y1), (x2, y2) = p(a1), p(a2)
    return u"M%g %g L%g %g L%g %g A%g %g 0 1 1 %g %g Z" % (x1, y1, tip[0], tip[1], x2, y2, rx, ry, x1, y1)


def phone(pid, left, top, inner, w=150, h=267, extra=u""):
    return (u'<div id="%s" class="ph hid" style="left:%dpx; top:%dpx; width:%dpx; height:%dpx;%s">'
            u'<div class="scr">%s</div></div>' % (pid, left, top, w, h, extra, inner))


def blk(x, y, w, h, bg, r=8, more=u""):
    return (u'<span class="b" style="left:%dpx; top:%dpx; width:%dpx; height:%dpx; background:%s; '
            u'border-radius:%s;%s"></span>' % (x, y, w, h, bg, r if isinstance(r, str) else "%dpx" % r, more))


# the mini phones «1» / «2» above her (hook, verdict, answer): 150 x 267, centres x 340 / 740
MP_TOP = 305
F.append(phone("mp1", 265, MP_TOP, u'<span class="n">1</span>'))
F.append(phone("mp2", 665, MP_TOP, u'<span class="n">2</span>'))
F.append(u'''
        <div class="ctr" style="left:140px; top:612px; width:400px"><span class="chip on hid" id="mc1"
             style="font-size:30px; padding:10px 20px"><i></i>штучний інтелект</span></div>
        <div class="ctr" style="left:540px; top:612px; width:400px"><span class="chip hid" id="mc2"
             style="font-size:30px; padding:10px 20px"><i></i>монтажерка</span></div>''')

# 1 · ABOVE — two reels, no sound, guess ----------------------------------------
# everything is gone before the plate cuts into the pause at H0
t_dva, t_bez = S(u"два", 0.85), S(u"без", 1.27)
t_vga = S(u"вгадай,", 2.17)
x_out = H0 - 0.42
# a loudspeaker (a closed outline: a sticker) with a cross beside it — «без звуку»
SPK = path_d([(470, 378), (500, 378), (542, 343), (542, 457), (500, 422), (470, 422)])
js(u'''
  pop("#mp1", %.3f); pop("#mp2", %.3f);
  sketch("h1", "skF"); blob("h1", "%s", [470, 343, 72, 114], {seed: 103});
  cross("h1", 564, 374, 610, 426, {strokeWidth: 5, seed: 113});
  draw("h1", %.3f, .45);
  sketch("h2", "skF"); label("h2", 540, 585, "?", {size: 130});
  draw("h2", %.3f);
  sink("#mp1, #mp2", %.3f); erase("h1", %.3f); erase("h2", %.3f);
''' % (t_dva, t_dva + 0.22, SPK, t_bez - 0.2, t_vga - 0.05, x_out, x_out, x_out))
g.sfx("pop", t_dva); g.sfx("click-soft", t_bez + 0.2); g.sfx("pop", t_vga)

# 2 · THE PAUSE (H0–H1) — empty: her plate only. The caption plaque stands down
# over it too (a blackout span with no words in it).
BLACKOUT.append((H0, H1))

# 3 · ABOVE — the verdict -------------------------------------------------------
t_yak = S(u"Якщо", 15.3)                 # the plate is back on her at H1
t_dru, t_pom = S(u"другий,", 16.2), S(u"помилилась.", 17.2)
t_per, t_sht = S(u"Перший", 18.04), S(u"штучний", 19.3)
t_mon = S(u"монтажерка,", 20.88)
t_vid, t_bud = S(u"відтворити", 24.21), S(u"будь-який", 24.81)
t_tv, t_st = S(u"твоєму", 27.15), S(u"стилі.", 27.55)
r0 = max(t_yak - 0.02, H1 + 0.03)
# the rings are 260 wide so their haloed line clears the phone's corners (a
# 236 ring cut through the bezel); the cross lies on the white phone, so no
# halo — the kit's white halo erased the «2» under it
js(u'''
  rise("#mp1", %.3f); rise("#mp2", %.3f);
  sketch("v1", "skF"); ell("v1", 740, 438, 260, 326, {strokeWidth: 5, seed: 151, fill: false});
  draw("v1", %.3f, .5);
  sketch("v2", "skF"); cross("v2", 680, 350, 800, 530, {strokeWidth: 7, seed: 153, halo: false});
  draw("v2", %.3f, .28);
  erase("v1", %.3f); erase("v2", %.3f);
  sketch("v3", "skF"); ell("v3", 340, 438, 260, 326, {strokeWidth: 5, seed: 155, fill: false});
  draw("v3", %.3f, .5);
  pop("#mc1", %.3f);
  pop("#mc2", %.3f); erase("v3", %.3f);
  sketch("v4", "skF"); arrow("v4", 650, 400, 430, 400, {strokeWidth: 5, seed: 157, bend: -.18});
  draw("v4", %.3f, .5);
  sink("#mp1, #mp2, #mc1, #mc2", %.3f); erase("v4", %.3f);
''' % (r0, r0 + 0.12, t_dru - 0.1, t_pom, t_per - 0.12, t_per - 0.12, t_per - 0.05, t_sht,
       t_mon, t_mon - 0.05, t_vid - 0.4, t_bud - 0.3, t_bud - 0.3))
g.sfx("pop", r0); g.sfx("click-soft", t_dru); g.sfx("click-soft", t_pom)
g.sfx("pop", t_sht); g.sfx("pop", t_mon)
# «штучний інтелект, а другий — монтажерка,»: chip 1, phone 2 and chip 2 say it
BLACKOUT.append((t_sht - 0.05, S(u"ще", 21.4) - 0.01))

# 3b · ABOVE — any editing, in your style: four reels, each cut another way -----
PERSON = blk(47, 146, 44, 44, "#DEBFBF", "50%") + blk(24, 196, 90, 70, "#DEBFBF", "45px 45px 0 0")
TILES = [
    # captions: a white box with a key-word pill
    PERSON + blk(12, 206, 114, 30, "#fff", 9, u" box-shadow:0 1px 3px rgba(36,25,25,.18)") + blk(52, 213, 40, 16, "#7A1424", 8),
    # a big title on top
    PERSON + blk(16, 28, 104, 22, "#7A1424", 6) + blk(16, 58, 70, 22, "#7A1424", 6),
    # a half screen: white panel, a sketched box, her pushed down
    blk(0, 0, 138, 118, "#fff") + blk(22, 26, 94, 64, "transparent", 12, u" border:4px solid #1E1E1E")
    + blk(47, 160, 44, 44, "#DEBFBF", "50%") + blk(24, 206, 90, 60, "#DEBFBF", "45px 45px 0 0"),
    # a card above her
    PERSON + blk(14, 34, 110, 78, "#fff", 14, u" box-shadow:0 1px 3px rgba(36,25,25,.18)")
    + blk(26, 50, 60, 12, "#7A1424", 6) + blk(26, 74, 86, 12, "#EFE3E3", 6),
]
# 80 px between tiles (x 120-960, centred): the ring round tile 2 needs room
# on both sides — at 40 px its haloed line ran over both neighbours' bezels
for i, inner in enumerate(TILES):
    F.append(phone("tl%d" % i, 120 + i * 230, 312, inner))
F.append(u'''
        <div class="ctr" style="left:455px; top:624px; width:400px"><span class="chip on hid" id="tsc"
             style="font-size:30px; padding:10px 20px"><i></i>твій стиль</span></div>''')
js(u'''
  %s
  sketch("v5", "skF"); ell("v5", 655, 445, 250, 330, {strokeWidth: 5, seed: 159, fill: false});
  draw("v5", %.3f, .5); pop("#tsc", %.3f);
  sink("#tl0, #tl1, #tl2, #tl3, #tsc", %.3f); erase("v5", %.3f);
''' % (u" ".join(u'pop("#tl%d", %.3f);' % (i, t_bud - 0.05 + i * 0.16) for i in range(4)),
       t_tv - 0.3, t_tv, E(u"стилі.", 27.55) + 0.1, E(u"стилі.", 27.55) + 0.1))
g.sfx("pop", t_bud); g.sfx("click-soft", t_tv)
BLACKOUT.append((t_tv - 0.05, S(u"І", 28.0) - 0.01))      # «твоєму стилі.»: the chip says it

# 4 · BEHIND — «200 €» -----------------------------------------------------------
t_200, t_ne1 = S(u"200", 30.67), S(u"не", 32.26)
m0, m1 = t_200 - 0.2, t_ne1 - 0.05
B.append(u'<div id="bw1" class="big hid" style="top:530px; font-size:300px">200 €</div>')
g.matte("eur", round(m0, 3), round(m1 - m0 + 0.45, 3))
js(u'''
  rise("#bw1", %.3f);
  sink("#bw1", %.3f);
''' % (t_200 - 0.12, m1 - 0.3))
g.sfx("kaching", t_200)
BLACKOUT.append((t_200 - 0.05, S(u"на", 31.4) - 0.01))     # «200 євро»: the big word says it

# 5 · ABOVE — what she no longer has: each one popped on its verb, struck on its noun
t_pla, t_mzh = S(u"платячи", 32.38), S(u"монтажеру,", 32.88)
t_che, t_vio = S(u"чекаючи", 33.96), S(u"відео", 34.54)
t_zal, t_hv = S(u"залежачи", 35.78), S(u"хвороб.", 37.18)
ROWS = [u"платити монтажеру", u"чекати на відео", u"залежати від її часу й хвороб"]
F.append(u'<div id="b5" class="card hid" style="left:150px; top:300px; width:780px; height:330px; padding:0"></div>')
for i, txt in enumerate(ROWS):
    F.append(u'<span class="chip hid" id="b5r%d" style="position:absolute; left:195px; top:%dpx; width:690px; '
             u'font-size:38px; padding:12px 26px"><i></i><span style="position:relative">%s<span class="strk" id="b5k%d"></span></span></span>'
             % (i, 330 + i * 92, esc(txt), i))
x_b5 = E(u"хвороб.", 37.18) + 0.05
js(u'''
  rise("#b5", %.3f);
  pop("#b5r0", %.3f); pop("#b5r1", %.3f); pop("#b5r2", %.3f);
  [%.3f, %.3f, %.3f].forEach(function (t, k) {
    tl.fromTo("#b5k" + k, {scaleX: 0, rotation: -.6}, X({scaleX: 1, rotation: -.6, duration: .35, ease: "power1.inOut"}), t);
    tl.to("#b5r" + k, {color: "#574142", duration: .3}, t);
  });
  sink("#b5, #b5r0, #b5r1, #b5r2", %.3f);
''' % (t_ne1 + 0.02, t_pla, t_che, t_zal, t_mzh, t_vio, t_hv, x_b5))
for t in (t_mzh, t_vio, t_hv):
    g.sfx("click-soft", t)
BLACKOUT.append((t_ne1 - 0.05, x_b5))      # the three struck chips say it

# 6 · HALF — shoot → Claude → 20 min → a finished reel ---------------------------
# it leaves in her pause before «Тому», so no rail word straddles the exit
h0, h1 = S(u"Вона", 37.89) - 0.15, S(u"Тому", 43.7) - 0.4
HALF.append((h0, h1))
# her cut-out sits above the panel by design (§00.3.3, the head overlaps the
# panel edge): the panel content is marked as intentional layering for check
P.append(u'<svg class="sk" id="skP" data-layout-allow-occlusion width="1080" height="1240" viewBox="0 0 1080 1240"></svg>')
P.append(u'''
        <div id="pcl" class="hid" data-layout-allow-occlusion style="position:absolute; left:405px; top:560px; width:250px; height:180px;
             display:flex; flex-direction:column; align-items:center; justify-content:center; gap:10px;
             color:#7A1424">%s<span style="font-weight:500; font-size:44px; color:#241919">Claude</span></div>''' % mark("claude", 70))
t_mom, t_zn = S(u"момент", 38.93), S(u"зняти", 39.17)
t_vid2, t_kl = S(u"віддати", 40.22), S(u"Клоду", 40.86)
t_20, t_got = S(u"20", 41.56), S(u"готовий", 42.62)
# The phones' labels are sketches of their own, drawn ON their words: queued
# after the phone strokes they landed 0.6 s late, and «готовий результат» only
# 0.1 s before the panel left (the caption was blacked out — it never read).
# «20 хв» lands on «20». The content rides out with the panel (erase at h1 + .4).
hx = h1 + 0.4
js(u'''
  sketch("p1", "skP"); box("p1", 100, 315, 150, 267, {seed: 171, r: 26}); ln("p1", 155, 342, 195, 342, {seed: 173});
  ell("p1", 175, 545, 32, 32, {stroke: "#7A1424", fill: "#7A1424", fillStyle: "solid", seed: 175});
  draw("p1", %.3f, .55);
  sketch("p1l", "skP"); label("p1l", 175, 650, "зняти", {size: 44}); label("p1l", 175, 698, "рілс", {size: 44});
  draw("p1l", %.3f);
  sketch("p2", "skP"); arrow("p2", 262, 470, 392, 600, {seed: 177, bend: .14}); box("p2", 405, 560, 250, 180, {seed: 179, r: 30});
  draw("p2", %.3f, .45); fadein("#pcl", %.3f);
  sketch("p3", "skP"); arrow("p3", 668, 600, 798, 470, {stroke: "#7A1424", seed: 181, bend: .14});
  label("p3", 730, 440, "20 хв", {size: 50, color: "#7A1424"});
  draw("p3", %.3f, .4);
  sketch("p4", "skP"); box("p4", 805, 315, 150, 267, {seed: 183, r: 26}); ln("p4", 860, 342, 900, 342, {seed: 185});
  tick("p4", 878, 456, {stroke: "#7A1424", strokeWidth: 7, k: 1.2, seed: 187});
  draw("p4", %.3f, .5);
  sketch("p4l", "skP"); label("p4l", 880, 650, "готовий", {size: 44}); label("p4l", 880, 698, "результат", {size: 44});
  draw("p4l", %.3f);
  erase("p1", %.3f); erase("p1l", %.3f); erase("p2", %.3f); erase("p3", %.3f); erase("p4", %.3f); erase("p4l", %.3f);
  out("#pcl", %.3f);
''' % (t_mom - 0.35, t_zn - 0.05, t_vid2 - 0.05, t_kl, t_20 - 0.55, t_got - 0.62, t_got - 0.05,
       hx, hx, hx, hx, hx, hx, hx))
BLACKOUT.append((t_zn - 0.05, S(u"рілс,", 39.57) + 0.05))                   # «зняти рілс» label
BLACKOUT.append((t_kl - 0.05, S(u"і", 41.2) - 0.01))                        # «Клоду»: the Claude box
BLACKOUT.append((t_20 - 0.05, S(u"отримати", 42.2) - 0.01))                 # «20 хвилин»: «20 хв»
BLACKOUT.append((t_got - 0.05, S(u"результат.", 43.0) + 0.05))              # «готовий результат» label
g.sfx("click-soft", t_zn); g.sfx("pop", t_kl); g.sfx("pop", t_got)
g.sfx("whoosh-short", h0); g.sfx("whoosh-short", h1)

# 7 · ABOVE — the answer: 1 and 2 again; «≠» becomes «=» --------------------------
t_tomu, t_kaz = S(u"Тому", 43.7), S(u"каже,", 45.41)
t_ni, t_dob = S(u"ні,", 46.1), S(u"так", 48.22)
t_lim = S(u"Ліміти", 50.1)
BUB = bubble_d(540, 410, 105, 80, (470, 530))
# «≠» is written on «ні» (on «не може» the bubble stood empty for 2 s); the
# strokes lie on the white bubble, so no halo — the slash's halo cut the «=»
js(u'''
  rise("#mp1, #mc1", %.3f); rise("#mp2, #mc2", %.3f);
  sketch("a1", "skF"); blob("a1", "%s", [435, 330, 210, 200], {seed: 191});
  draw("a1", %.3f, .5);
  sketch("a2", "skF"); ln("a2", 500, 396, 580, 396, {seed: 193, halo: false}); ln("a2", 500, 428, 580, 428, {seed: 195, halo: false});
  draw("a2", %.3f, .3);
  sketch("a3", "skF"); ln("a3", 562, 366, 518, 458, {seed: 197, halo: false}); draw("a3", %.3f, .25);
  erase("a2", %.3f); erase("a3", %.3f);
  sketch("a4", "skF"); ln("a4", 494, 394, 586, 394, {strokeWidth: 8, seed: 199, halo: false});
  ln("a4", 494, 430, 586, 430, {strokeWidth: 8, seed: 201, halo: false});
  draw("a4", %.3f, .3);
  sink("#mp1, #mp2, #mc1, #mc2", %.3f); erase("a4", %.3f); erase("a1", %.3f);
''' % (t_tomu, t_tomu + 0.12, BUB, t_kaz - 0.2, t_ni - 0.1, t_ni + 0.2, t_dob - 0.1, t_dob - 0.1,
       t_dob - 0.05, t_lim - 0.4, t_lim - 0.4, t_lim - 0.4))
g.sfx("pop", t_tomu + 0.05); g.sfx("click-soft", t_ni); g.sfx("pop", t_dob)
# «штучний інтелект» again: chip 1 is on screen and says it
BLACKOUT.append((S(u"штучний", 46.6) - 0.05, S(u"не", 47.35) - 0.01))

# 8 · HALF — the limits: real creativity above the line, «creativity» below ------
# it leaves as «капкаті» ends (blacked out: the CapCut chip says it), so «Тому» is white on the plaque
h2, h3 = t_lim - 0.15, S(u"капкаті.", 58.89) + 0.06
HALF.append((h2, h3))
t_spr, t_kr2 = S(u"справжнього", 52.28), S(u"креативу,", 54.55)
t_cher, t_pl = S(u"червоному", 56.11), S(u"платній", 57.81)
# «субтитри» drawn as a caption: upper case, Product Sans Black, in her red
P.append(u'''
        <div id="psub" class="hid" data-layout-allow-occlusion style="position:absolute; left:190px; top:660px; padding:12px 28px; border-radius:22px;
             background:#fff; box-shadow:0 2px 10px rgba(36,25,25,.16); font-family:'ProductSans', sans-serif;
             font-weight:900; font-size:46px; letter-spacing:-0.015em; color:#7A1424">СУБТИТРИ</div>
        <div id="pcap" class="hid" data-layout-allow-occlusion style="position:absolute; left:560px; top:662px; display:flex; align-items:center; gap:14px;
             border:2px solid #DEBFBF; border-radius:16px; padding:12px 24px; background:#FFF8F7">
          <span style="font-weight:700; font-size:44px; letter-spacing:-0.02em; color:#241919">CapCut</span>
          <span style="display:inline-flex; width:56px; height:56px; border-radius:50%; background:#7A1424; color:#fff;
                font-weight:700; font-size:34px; align-items:center; justify-content:center">€</span>
        </div>''')
js(u'''
  sketch("q1", "skP"); ln("q1", 110, 512, 970, 506, {stroke: "#7A1424", strokeWidth: 6, seed: 211});
  draw("q1", %.3f, .6);
  sketch("q1l", "skP"); label("q1l", 112, 492, "ліміти", {size: 46, color: "#7A1424", anchor: "start"});
  draw("q1l", %.3f); erase("q1l", %.3f);
  sketch("q2", "skP"); box("q2", 300, 320, 570, 150, {seed: 213, r: 30, fill: true});
  label("q2", 585, 412, "справжній креатив", {size: 54});
  draw("q2", %.3f, .6);
  sketch("q3", "skP"); box("q3", 170, 560, 740, 225, {seed: 215, r: 30});
  label("q3", 540, 630, "«креатив»", {size: 52});
  draw("q3", %.3f, .6);
  pop("#psub", %.3f); pop("#pcap", %.3f);
  erase("q1", %.3f); erase("q2", %.3f); erase("q3", %.3f); out("#psub, #pcap", %.3f);
''' % (t_lim - 0.15, t_lim - 0.05, h3, t_spr - 0.3, t_kr2 - 0.3, t_cher, t_pl, h3, h3, h3, h3))
# no blackout on «Ліміти»: the panel is still sliding in, its label only shows from ≈ 50.4
BLACKOUT.append((t_spr - 0.05, t_kr2 + 0.05))                      # «справжній креатив» / «креатив» boxes
BLACKOUT.append((S(u"субтитрів", 57.1) - 0.05, S(u"і", 57.6) - 0.01))   # «СУБТИТРИ» says it
BLACKOUT.append((S(u"капкаті.", 58.89) - 0.05, S(u"капкаті.", 58.89) + 0.05))   # the «CapCut» chip
g.sfx("pop", t_spr); g.sfx("pop", t_kr2); g.sfx("pop", t_pl)
g.sfx("whoosh-short", h2); g.sfx("whoosh-short", h3)

# 9 · ABOVE — CTA -----------------------------------------------------------------
t_blog, t_smm = S(u"блогерка,", 60.04), S(u"СММниця,", 60.78)
t_pid, t_pro = S(u"підприємиця", 61.3), S(u"продюсерка", 62.42)
t_24, t_vt = S(u"24", 65.42), S(u"втомлюється", 67.33)
t_stav = S(u"то", 69.0)
F.append(u'''
        <div id="b9" class="hid" style="position:absolute; left:120px; top:310px; width:840px;
             display:flex; gap:14px; justify-content:center; flex-wrap:wrap">
          <span class="chip hid" id="b9a"><i></i>блогерка</span>
          <span class="chip hid" id="b9b"><i></i>СММниця</span>
          <span class="chip hid" id="b9c"><i></i>підприємиця</span>
          <span class="chip hid" id="b9d"><i></i>продюсерка</span>
        </div>
        <div id="b9n" class="pill light hid" style="left:300px; top:318px; font-weight:700; font-size:72px;
             padding:18px 50px; color:#7A1424">24/7</div>
        <div id="b9cta" class="pill hid" style="left:270px; top:478px;">Став + в коментарі</div>''')
js(u'''
  fadein("#b9", %.3f, .01); pop("#b9a", %.3f); pop("#b9b", %.3f); pop("#b9c", %.3f); pop("#b9d", %.3f);
  sink("#b9", %.3f);
  pop("#b9n", %.3f);
  // a full battery: case and nub are stickers, the charge inside is the kit's hatch
  sketch("e1", "skF"); box("e1", 640, 348, 160, 84, {seed: 221, r: 18}); box("e1", 800, 374, 16, 32, {seed: 223, r: 6});
  box("e1", 654, 362, 132, 56, {seed: 225, r: 10, fill: true, strokeWidth: 3});
  draw("e1", %.3f, .45);
  pop("#b9cta", %.3f, .6);
  // comments are down at the right of the IG rail, so the pointer goes down to
  // them — never up at the pill (her review of 41). Tip stays left of x 900.
  sketch("e2", "skF"); label("e2", 800, 730, "сюди!", {size: 52});
  arrow("e2", 820, 760, 880, 975, {strokeWidth: 5, seed: 227, bend: -.25});
  draw("e2", %.3f, .5);
''' % (t_blog - 0.05, t_blog, t_smm, t_pid, t_pro, t_24 - 0.35, t_24, t_vt - 0.35, t_stav, t_stav + 0.15))
g.sfx("pop", t_blog); g.sfx("pop", t_pro); g.sfx("pop", t_24); g.sfx("click-soft", t_vt); g.sfx("pop", t_stav)
BLACKOUT.append((t_blog - 0.05, S(u"і", 63.1) - 0.01))     # the four chips say «блогерка … продюсерка»
BLACKOUT.append((t_24 - 0.05, S(u"яка", 66.4) - 0.01))     # «24 на 7»: the pill says it
BLACKOUT.append((t_stav - 0.05, DUR + 1.0))     # the pill says it (to the end: the plaque never returns)

# ---------------------------------------------------------------- mattes for the half screens
for i, (a, b) in enumerate(HALF):
    g.matte("half%d" % (i + 1), round(a - 0.1, 3), round(b - a + 1.2, 3))
    js("  half(%.3f, %.3f);" % (a, b))
    PLACE.append((a + 0.4, b + 0.2, "bottom", 980))

F.append(u'<svg class="sk" id="skF" width="1080" height="1920" viewBox="0 0 1080 1920"></svg>')

# the pause carries nothing of ours, sound included
assert not [c for c in g.cues if H0 - 0.05 < c["t"] < H1 + 0.03], [c for c in g.cues if H0 - 0.05 < c["t"] < H1 + 0.03]


def main():
    if "--words" in sys.argv:
        print(" ".join("%s/%.1f" % (c["w"], c["s"]) for c in CAPS))
    chunks = g.chunks(CAPS, place=PLACE)          # the kit turns them into the old word rail
    doc = g.document(title=u"Reel 51 — Твій стиль з першого дня", plate="assets/base.mp4",
                     behind="\n".join(B), panel="\n".join(P), front="\n".join(F), cover="\n".join(C),
                     js="\n".join(J), chunks=chunks, blackout=BLACKOUT, extra_css=EXTRA_CSS)
    g.write(HERE, doc)
    print("index.html  %d caption chunks, %d sfx cues, %d mattes" % (len(chunks), len(g.cues), len(g.mattes)))


main()
