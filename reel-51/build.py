# -*- coding: utf-8 -*-
"""Reel 51 — «Твій стиль з першого дня». Posts 2026-10-25.

Google style + Excalidraw (STYLE.md §00), the reel-41 skeleton.

The one object is **the two reels** — «1» and «2», a blind test. They are
dealt above her on the hook, played big side by side through her 10 s silent
hold (full screen), come back small for the verdict (2 is wrong, 1 is the AI,
2 the editor), multiply into «any editing» and her style, and return once more
for the answer to «AI can't edit as well» (≠ turns into =).

  above   two phones «1» «2», a muted speaker, «?»
  full    THE HOLD (5.23–15.23 on the plate, she is silent): two big phone
          frames #cmp1 / #cmp2 side by side — placeholders until her two reels
          arrive (see SWAP below)
  above   verdict: 2 ringed, crossed; 1 ringed → «штучний інтелект»,
          2 → «монтажерка»; arrow 2 → 1 on «відтворити»; four edit styles,
          one ringed → «твій стиль»
  behind  «200 €»
  above   card: платити монтажеру / чекати на відео / її час і хвороби — struck
  half    зняти рілс → Claude → 20 хв → готовий результат
  above   1 and 2 again: a speech bubble, ≠ on «не може», = on «так само добре»
  half    ліміти: справжній креатив above the line; «креатив» below it —
          red subtitles, CapCut €
  above   CTA — блогерка / СММниця / підприємиця / продюсерка, 24/7 + a full
          battery, «Став + в коментарі»

usage: python build.py [--words] [--chunks]   (then mattes; render is the orchestrator's)
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
from gstyle import G, Words, load_caps, mark, esc  # noqa: E402

NN = "51"
CUT = json.load(io.open(os.path.join(ROOT, "work", "r" + NN, "cut.json"), encoding="utf-8"))
DUR = 70.516           # (2116 plate frames - 0.5) / 30
g = G(dur=DUR, reel=NN)

# the silent hold: clip 1 of cut.json, the only clip with no text
HOLD = [c for c in CUT["clips"] if not c["text"].strip()][0]
H0, H1 = HOLD["tl"], HOLD["tl"] + HOLD["dur"]            # 5.233 – 15.233

# whisper's spelling of what she plainly said -> her word (re-heard on the plate)
FIX = {
    u"надварив": u"на два рілси", u"себе": u"без",
    u"Клоді": u"стилі.",                 # she said «в твоєму стилі» (script: «у твоєму Клоді»)
    (u"місяць,", 32.0): None,                    # aligner echo at the 32.0 join
    (u"стосуються", 52.1): None,                 # aligner echo at the 52.13 join
    u"ліміти": u"Ліміти",
    u"натормити": u"отримати",
    (u"другий", 20.4): u"другий —",
    u"SMM": u"СММниця,", u"нація,": None, u"підприємуця": u"підприємиця",
}
CAPS = load_caps(NN, FIX)
# «інтелект.» is stretched over the silent hold by the aligner; she stops at 5.23
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
    /* the two big frames of the hold: 9:16, inside the safe box */
    .bph { position: absolute; box-sizing: border-box; background: #fff; border: 10px solid #241919;
           border-radius: 56px; overflow: hidden;
           box-shadow: 0 1px 3px rgba(36,25,25,.10), 0 10px 30px rgba(36,25,25,.10); }
    .cmp { position: absolute; left: 0; top: 0; width: 100%; height: 100%; display: block;
           object-fit: cover; background: #FFF0F0; border-radius: 46px; }
    .ctr { position: absolute; display: flex; justify-content: center; }
"""

# sketch helpers on top of gstyle's
js(u'''
  function poly(name, pts, o) { var s = SK[name];
    var oo = opt(o, (o && o.seed) || 101);
    if (o && o.fill) { var f = hatch(o.fill === true ? {} : {fill: o.fill}); for (var k in f) oo[k] = f[k]; }
    _add(s, s.rc.polygon(pts, oo)); }
  function cross(name, x1, y1, x2, y2, o) {
    var o2 = {}; for (var k in (o || {})) o2[k] = o[k]; o2.seed = ((o && o.seed) || 81) + 2;
    ln(name, x1, y1, x2, y2, o); ln(name, x2, y1, x1, y2, o2); }
  function tick(name, x, y, o) { var s = SK[name], k = (o && o.k) || 1;
    _add(s, s.rc.linearPath([[x - 34 * k, y], [x - 8 * k, y + 28 * k], [x + 40 * k, y - 34 * k]], opt(o, (o && o.seed) || 71))); }
  // a loudspeaker, muted: body + cone, a red cross beside it
  function spk(name, x, y, o) {
    poly(name, [[x, y - 18], [x + 24, y - 18], [x + 58, y - 46], [x + 58, y + 46], [x + 24, y + 18], [x, y + 18]], o);
    cross(name, x + 78, y - 24, x + 122, y + 24, {stroke: "#7A1424", strokeWidth: 5, seed: 113});
  }
  // a speech bubble: an oval with a tail
  function bubble(name, cx, cy, w, h, o) { var s = SK[name];
    ell(name, cx, cy, w, h, o);
    _add(s, s.rc.linearPath([[cx - 34, cy + h / 2 - 8], [cx - 58, cy + h / 2 + 46], [cx + 6, cy + h / 2 - 4]], opt(o, 117)));
  }
''')


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
t_dva, t_bez = S(u"на два рілси", 0.77), S(u"без", 1.27)
t_vga = S(u"вгадай,", 2.17)
js(u'''
  pop("#mp1", %.3f); pop("#mp2", %.3f);
  sketch("h1", "skF"); spk("h1", 478, 400, {seed: 103});
  draw("h1", %.3f, .45);
  sketch("h2", "skF"); label("h2", 540, 585, "?", {size: 130, color: "#7A1424"});
  draw("h2", %.3f);
  tl.set("#mp1, #mp2", {autoAlpha: 0}, %.3f); tl.set("#sk-h1, #sk-h2", {autoAlpha: 0}, %.3f);
''' % (t_dva, t_dva + 0.22, t_bez - 0.2, t_vga - 0.05, H0 + 0.1, H0 + 0.1))
g.sfx("pop", t_dva); g.sfx("click-soft", t_bez + 0.2); g.sfx("pop", t_vga)

# 2 · FULL — THE HOLD: her two reels side by side, she is silent ----------------
# Two 9:16 frames, 390 x 693 each (inner 370 x 673), x 93–483 and 507–897: two
# 430 px frames (860 px) do not fit between the left edge zone (x 90) and the
# action column (x 900), so they are 390 wide — the most the safe box allows.
c0, c1 = E(u"штучний", 3.87) + 0.05, H1 - 0.03
#
# SWAP — once her two reels arrive (reel-51/assets/cmp1.mp4 = the AI reel «1»,
# cmp2.mp4 = the editor's reel «2»), replace each CMP line below with:
#   CMP1 = u'<video id="cmp1" class="cmp" src="assets/cmp1.mp4" data-start="%.3f" data-duration="%.3f" data-media-start="0" muted playsinline></video>' % (c0, c1 + 0.85 - c0)
#   CMP2 = u'<video id="cmp2" class="cmp" src="assets/cmp2.mp4" data-start="%.3f" data-duration="%.3f" data-media-start="0" muted playsinline></video>' % (c0, c1 + 0.85 - c0)
# (they play from the moment the white starts to rise until it has gone; the
# play-triangle sketch is skipped by itself once #skCmp1 / #skCmp2 are gone)
CMP1 = u'<div id="cmp1" class="cmp"><svg class="sk" id="skCmp1" width="370" height="673" viewBox="0 0 370 673"></svg></div>'
CMP2 = u'<div id="cmp2" class="cmp"><svg class="sk" id="skCmp2" width="370" height="673" viewBox="0 0 370 673"></svg></div>'
BPH_TOP = 630
C.append(u'''
        <div class="hand" style="left:93px; width:390px; top:%dpx; text-align:center; font-size:96px; line-height:120px">1</div>
        <div class="hand" style="left:507px; width:390px; top:%dpx; text-align:center; font-size:96px; line-height:120px">2</div>
        <div class="bph" style="left:93px; top:%dpx; width:390px; height:693px">
          %s
        </div>
        <div class="bph" style="left:507px; top:%dpx; width:390px; height:693px">
          %s
        </div>
        <svg class="sk" id="skC" width="1080" height="1920" viewBox="0 0 1080 1920"></svg>''' % (
    BPH_TOP - 158, BPH_TOP - 158, BPH_TOP, CMP1, BPH_TOP, CMP2))
js(u'''
  full(%.3f, %.3f);
  sketch("c1", "skC"); ell("c1", 288, %d, 150, 138, {seed: 121}); ell("c1", 702, %d, 150, 138, {seed: 123});
  draw("c1", %.3f, .5);
  [1, 2].forEach(function (k) {
    if (!document.getElementById("skCmp" + k)) return;      // her video is in: no placeholder
    sketch("pl" + k, "skCmp" + k);
    ell("pl" + k, 185, 336, 200, 200, {seed: 130 + k});
    poly("pl" + k, [[158, 290], [158, 382], [236, 336]], {seed: 140 + k, fill: true});
    draw("pl" + k, %.3f + (k - 1) * .25, .55);
  });
''' % (c0, c1, BPH_TOP - 98, BPH_TOP - 98, H0 + 0.15, H0 + 0.5))
g.sfx("whoosh-short", c0); g.sfx("whoosh-short", c1)

# 3 · ABOVE — the verdict -------------------------------------------------------
t_dru, t_pom = S(u"другий,", 16.2), S(u"помилилась.", 17.2)
t_per, t_sht = S(u"Перший", 18.04), S(u"штучний", 19.3)
t_mon = S(u"монтажерка,", 20.88)
t_vid, t_bud = S(u"відтворити", 24.21), S(u"будь-який", 24.81)
t_tv, t_st = S(u"твоєму", 27.15), S(u"стилі.", 27.55)
js(u'''
  rise("#mp1", %.3f); rise("#mp2", %.3f);
  sketch("v1", "skF"); ell("v1", 740, 438, 236, 320, {stroke: "#7A1424", strokeWidth: 5, seed: 151});
  draw("v1", %.3f, .5);
  sketch("v2", "skF"); cross("v2", 680, 350, 800, 530, {stroke: "#7A1424", strokeWidth: 7, seed: 153});
  draw("v2", %.3f, .28);
  erase("v1", %.3f); erase("v2", %.3f);
  sketch("v3", "skF"); ell("v3", 340, 438, 236, 320, {stroke: "#7A1424", strokeWidth: 5, seed: 155});
  draw("v3", %.3f, .5);
  pop("#mc1", %.3f);
  pop("#mc2", %.3f); erase("v3", %.3f);
  sketch("v4", "skF"); arrow("v4", 650, 400, 430, 400, {stroke: "#7A1424", strokeWidth: 5, seed: 157, bend: -.22});
  draw("v4", %.3f, .5);
  sink("#mp1, #mp2, #mc1, #mc2", %.3f); erase("v4", %.3f);
''' % (c1 + 0.1, c1 + 0.2, t_dru - 0.1, t_pom, t_per - 0.12, t_per - 0.12, t_per - 0.05, t_sht,
       t_mon, t_mon - 0.05, t_vid - 0.4, t_bud - 0.3, t_bud - 0.3))
g.sfx("pop", c1 + 0.15); g.sfx("click-soft", t_dru); g.sfx("click-soft", t_pom); g.sfx("click-soft", t_per)
g.sfx("pop", t_sht); g.sfx("pop", t_mon); g.sfx("whoosh-short", t_vid - 0.3)

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
for i, inner in enumerate(TILES):
    F.append(phone("tl%d" % i, 180 + i * 190, 312, inner))
F.append(u'''
        <div class="ctr" style="left:435px; top:612px; width:400px"><span class="chip on hid" id="tsc"
             style="font-size:30px; padding:10px 20px"><i></i>твій стиль</span></div>''')
js(u'''
  %s
  sketch("v5", "skF"); ell("v5", 635, 445, 230, 320, {stroke: "#7A1424", strokeWidth: 5, seed: 159});
  draw("v5", %.3f, .5); pop("#tsc", %.3f);
  sink("#tl0, #tl1, #tl2, #tl3, #tsc", %.3f); erase("v5", %.3f);
''' % (u" ".join(u'pop("#tl%d", %.3f);' % (i, t_bud - 0.05 + i * 0.16) for i in range(4)),
       t_tv - 0.3, t_st, E(u"стилі.", 27.55) + 0.1, E(u"стилі.", 27.55) + 0.1))
g.sfx("pop", t_bud); g.sfx("click-soft", t_st)

# 4 · BEHIND — «200 €» -----------------------------------------------------------
t_200, t_ne1 = S(u"200", 30.67), S(u"не", 32.26)
m0, m1 = t_200 - 0.2, t_ne1 - 0.05
B.append(u'<div id="bw1" class="big hid" style="top:500px; font-size:300px">200 €</div>')
g.matte("eur", round(m0, 3), round(m1 - m0 + 0.45, 3))
js(u'''
  rise("#bw1", %.3f);
  sink("#bw1", %.3f);
''' % (t_200 - 0.12, m1 - 0.3))
g.sfx("kaching", t_200)

# 5 · ABOVE — what she no longer has: each one struck on its word ----------------
t_pla, t_mzh = S(u"платячи", 32.38), S(u"монтажеру,", 32.88)
t_che, t_vio = S(u"чекаючи", 33.96), S(u"відео", 34.54)
t_zal, t_hv = S(u"залежачи", 35.78), S(u"хвороб.", 37.18)
ROWS = [u"платити монтажеру", u"чекати на відео", u"її час і хвороби"]
F.append(u'<div id="b5" class="card hid" style="left:150px; top:300px; width:780px; height:330px; padding:0"></div>')
for i, txt in enumerate(ROWS):
    F.append(u'<span class="chip hid" id="b5r%d" style="position:absolute; left:240px; top:%dpx; width:600px; '
             u'font-size:40px; padding:12px 26px"><i></i>%s</span>' % (i, 330 + i * 92, esc(txt)))
js(u'''
  rise("#b5", %.3f);
  pop("#b5r0", %.3f); pop("#b5r1", %.3f); pop("#b5r2", %.3f);
  sketch("s0", "skF"); ln("s0", 255, 368, 825, 362, {stroke: "#7A1424", strokeWidth: 7, seed: 161}); draw("s0", %.3f, .35);
  sketch("s1", "skF"); ln("s1", 255, 460, 825, 455, {stroke: "#7A1424", strokeWidth: 7, seed: 163}); draw("s1", %.3f, .35);
  sketch("s2", "skF"); ln("s2", 255, 552, 825, 548, {stroke: "#7A1424", strokeWidth: 7, seed: 165}); draw("s2", %.3f, .35);
  sink("#b5, #b5r0, #b5r1, #b5r2", %.3f); erase("s0", %.3f); erase("s1", %.3f); erase("s2", %.3f);
''' % (t_ne1 + 0.02, t_pla, t_che, t_zal, t_mzh, t_vio, t_hv,
       E(u"хвороб.", 37.18) + 0.05, E(u"хвороб.", 37.18) + 0.05, E(u"хвороб.", 37.18) + 0.05, E(u"хвороб.", 37.18) + 0.05))
for t in (t_pla, t_che, t_zal):
    g.sfx("pop", t)
for t in (t_mzh, t_vio, t_hv):
    g.sfx("click-soft", t)
BLACKOUT.append((t_ne1 - 0.05, E(u"хвороб.", 37.18) + 0.05))      # the three struck chips say it

# 6 · HALF — shoot → Claude → 20 min → a finished reel ---------------------------
h0, h1 = S(u"Вона", 37.89) - 0.15, S(u"Тому", 43.7) - 0.25
HALF.append((h0, h1))
P.append(u'<svg class="sk" id="skP" width="1080" height="1240" viewBox="0 0 1080 1240"></svg>')
P.append(u'''
        <div id="pcl" class="hid" style="position:absolute; left:400px; top:392px; width:260px; height:196px;
             display:flex; flex-direction:column; align-items:center; justify-content:center; gap:10px;
             color:#7A1424">%s<span style="font-weight:500; font-size:44px; color:#241919">Claude</span></div>''' % mark("claude", 70))
t_mom, t_zn = S(u"момент", 38.93), S(u"зняти", 39.17)
t_vid2, t_kl = S(u"віддати", 40.22), S(u"Клоду", 40.86)
t_20, t_got = S(u"20", 41.56), S(u"готовий", 42.62)
js(u'''
  sketch("p1", "skP"); box("p1", 110, 330, 180, 320, {seed: 171, r: 28}); ln("p1", 175, 360, 225, 360, {seed: 173});
  ell("p1", 200, 590, 36, 36, {stroke: "#7A1424", fill: "#7A1424", fillStyle: "solid", seed: 175});
  label("p1", 200, 715, "зняти рілс", {size: 44});
  draw("p1", %.3f, .55);
  sketch("p2", "skP"); arrow("p2", 300, 490, 388, 490, {seed: 177, bend: 0}); box("p2", 400, 392, 260, 196, {seed: 179, r: 30});
  draw("p2", %.3f, .45); fadein("#pcl", %.3f);
  sketch("p3", "skP"); arrow("p3", 672, 490, 788, 490, {stroke: "#7A1424", seed: 181, bend: 0});
  label("p3", 730, 452, "20 хв", {size: 50, color: "#7A1424"});
  draw("p3", %.3f, .4);
  sketch("p4", "skP"); box("p4", 800, 330, 180, 320, {seed: 183, r: 28}); ln("p4", 865, 360, 915, 360, {seed: 185});
  tick("p4", 888, 492, {stroke: "#7A1424", strokeWidth: 7, k: 1.3, seed: 187});
  label("p4", 890, 712, "готовий", {size: 44}); label("p4", 890, 762, "результат", {size: 44});
  draw("p4", %.3f, .5);
  erase("p1", %.3f); erase("p2", %.3f); erase("p3", %.3f); erase("p4", %.3f); out("#pcl", %.3f);
''' % (t_mom - 0.35, t_vid2 - 0.05, t_kl, t_20 - 0.3, t_got - 0.45, h1, h1, h1, h1, h1))
BLACKOUT.append((t_zn - 0.05, t_zn + 0.05))                        # «зняти рілс» label
BLACKOUT.append((S(u"отримати", 42.22) - 0.05, S(u"отримати", 42.22) + 0.05))   # «готовий результат» label
g.sfx("click-soft", t_zn); g.sfx("pop", t_kl); g.sfx("click-soft", t_20); g.sfx("pop", t_got)
g.sfx("whoosh-short", h0); g.sfx("whoosh-short", h1)

# 7 · ABOVE — the answer: 1 and 2 again; «≠» becomes «=» --------------------------
t_tomu, t_kaz = S(u"Тому", 43.7), S(u"каже,", 45.41)
t_nm, t_dob = S(u"не", 47.35), S(u"так", 48.22)
t_lim = S(u"Ліміти", 50.1)
js(u'''
  rise("#mp1, #mc1", %.3f); rise("#mp2, #mc2", %.3f);
  sketch("a1", "skF"); bubble("a1", 540, 410, 210, 160, {seed: 191});
  draw("a1", %.3f, .5);
  sketch("a2", "skF"); ln("a2", 500, 398, 580, 398, {seed: 193}); ln("a2", 500, 430, 580, 430, {seed: 195});
  draw("a2", %.3f, .3);
  sketch("a3", "skF"); ln("a3", 560, 368, 520, 462, {seed: 197}); draw("a3", %.3f, .25);
  erase("a2", %.3f); erase("a3", %.3f); erase("a1", %.3f);
  sketch("a4", "skF"); ln("a4", 486, 396, 594, 396, {stroke: "#7A1424", strokeWidth: 9, seed: 199});
  ln("a4", 486, 436, 594, 436, {stroke: "#7A1424", strokeWidth: 9, seed: 201});
  draw("a4", %.3f, .3);
  sink("#mp1, #mp2, #mc1, #mc2", %.3f); erase("a4", %.3f);
''' % (t_tomu, t_tomu + 0.12, t_kaz - 0.2, t_nm, t_nm + 0.3, t_dob - 0.1, t_dob - 0.1, t_dob - 0.1,
       t_dob - 0.05, t_lim - 0.4, t_lim - 0.4))
g.sfx("whoosh-short", t_tomu); g.sfx("click-soft", t_kaz); g.sfx("click-soft", t_nm); g.sfx("pop", t_dob)

# 8 · HALF — the limits: real creativity above the line, «creativity» below ------
h2, h3 = t_lim - 0.15, S(u"Тому", 59.43) - 0.25
HALF.append((h2, h3))
t_spr, t_kr2 = S(u"справжнього", 52.28), S(u"креативу,", 54.55)
t_cher, t_pl = S(u"червоному", 56.11), S(u"платній", 57.81)
P.append(u'''
        <div id="psub" class="hid" style="position:absolute; left:205px; top:660px; padding:12px 28px; border-radius:22px;
             background:#fff; box-shadow:0 2px 10px rgba(36,25,25,.16); font-weight:700; font-size:46px;
             color:#E0262F">субтитри</div>
        <div id="pcap" class="hid" style="position:absolute; left:560px; top:662px; display:flex; align-items:center; gap:14px;
             border:2px solid #DEBFBF; border-radius:16px; padding:12px 24px; background:#FFF8F7">
          <span style="font-weight:700; font-size:44px; letter-spacing:-0.02em; color:#241919">CapCut</span>
          <span style="display:inline-flex; width:56px; height:56px; border-radius:50%; background:#7A1424; color:#fff;
                font-weight:700; font-size:34px; align-items:center; justify-content:center">€</span>
        </div>''')
js(u'''
  sketch("q1", "skP"); ln("q1", 110, 512, 970, 506, {stroke: "#7A1424", strokeWidth: 6, seed: 211});
  label("q1", 118, 490, "ліміти", {size: 46, color: "#7A1424", anchor: "start"});
  draw("q1", %.3f, .6);
  sketch("q2", "skP"); box("q2", 230, 320, 620, 150, {seed: 213, r: 30, fill: true});
  label("q2", 540, 412, "справжній креатив", {size: 54});
  draw("q2", %.3f, .6);
  sketch("q3", "skP"); box("q3", 170, 560, 740, 225, {seed: 215, r: 30});
  label("q3", 540, 630, "«креатив»", {size: 52});
  draw("q3", %.3f, .6);
  pop("#psub", %.3f); pop("#pcap", %.3f);
  erase("q1", %.3f); erase("q2", %.3f); erase("q3", %.3f); out("#psub, #pcap", %.3f);
''' % (t_lim - 0.15, t_spr - 0.3, t_kr2 - 0.3, t_cher, t_pl, h3, h3, h3, h3))
BLACKOUT.append((t_spr - 0.05, S(u"а не", 54.34) + 0.05))          # «справжній креатив» / «креатив» boxes
g.sfx("click-soft", t_lim); g.sfx("pop", t_spr); g.sfx("pop", t_kr2); g.sfx("pop", t_cher); g.sfx("pop", t_pl)
g.sfx("whoosh-short", h2); g.sfx("whoosh-short", h3)

# 9 · ABOVE — CTA -----------------------------------------------------------------
t_blog, t_smm = S(u"блогерка,", 60.04), S(u"СММниця,", 60.78)
t_pid, t_pro = S(u"підприємиця", 61.3), S(u"продюсерка", 62.42)
t_24, t_vt = S(u"24", 65.42), S(u"втомлюється", 67.33)
t_stav = S(u"то став", 69.0)
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
  sketch("e1", "skF"); box("e1", 640, 348, 160, 84, {seed: 221, r: 18}); box("e1", 800, 374, 16, 32, {seed: 223, r: 6});
  box("e1", 654, 362, 132, 56, {seed: 225, r: 10, stroke: "#7A1424", fill: "#7A1424", strokeWidth: 3});
  draw("e1", %.3f, .45);
  pop("#b9cta", %.3f, .6);
  sketch("e2", "skF"); arrow("e2", 925, 695, 805, 592, {stroke: "#7A1424", strokeWidth: 5, seed: 227, bend: -.18});
  draw("e2", %.3f, .45);
''' % (t_blog - 0.05, t_blog, t_smm, t_pid, t_pro, t_24 - 0.35, t_24, t_vt - 0.35, t_stav, t_stav + 0.5))
g.sfx("pop", t_blog); g.sfx("pop", t_pro); g.sfx("pop", t_24); g.sfx("click-soft", t_vt); g.sfx("pop", t_stav)
BLACKOUT.append((t_stav - 0.05, DUR))     # the pill says it

# ---------------------------------------------------------------- mattes for the half screens
for i, (a, b) in enumerate(HALF):
    g.matte("half%d" % (i + 1), round(a - 0.1, 3), round(b - a + 1.2, 3))
    js("  half(%.3f, %.3f);" % (a, b))
    PLACE.append((a + 0.4, b + 0.2, "bottom", 980))

F.append(u'<svg class="sk" id="skF" width="1080" height="1920" viewBox="0 0 1080 1920"></svg>')

# caption phrases: where her phrasing breaks, not where 40 characters run out
SPLITS = [1.95, 3.21, 24.81, 25.75, 34.8, 39.17, 40.22, 41.16, 42.22, 54.34, 57.57, 63.14, 64.32, 69.0]
JOINS = [23.81, 25.95, 35.64, 37.18, 39.57, 41.56, 57.09, 63.56, 64.8, 68.17]
KEYS = {1.55: True, 16.2: True, 18.04: True, 24.21: True, 27.55: True, 29.57: True, 30.67: True,
        38.59: True, 40.86: True, 41.56: True, 50.1: True, 52.28: True, 56.11: True, 57.81: True,
        62.42: True, 65.42: True, 67.33: True}


def rechunk(chunks):
    near = lambda t, ts: any(abs(t - x) < 0.06 for x in ts)
    for t in SPLITS + JOINS:
        assert any(abs(w["s"] - t) < 0.06 for c in chunks for w in c["words"]), t
    groups = []
    for c in chunks:
        for i, w in enumerate(c["words"]):
            start = (i == 0 and not near(w["s"], JOINS)) or (i > 0 and near(w["s"], SPLITS))
            if start or not groups:
                groups.append([])
            groups[-1].append(w)
    out = []
    for n, ch in enumerate(groups):
        s = ch[0]["s"]
        nxt = groups[n + 1][0]["s"] if n + 1 < len(groups) else DUR
        pos = ("bottom", 1920 - 1520)
        for a, b, how, y in PLACE:
            if a <= s < b:
                pos = (how, y if how == "top" else 1920 - y)
        out.append({"s": round(s, 3), "e": round(min(nxt, ch[-1]["e"] + 0.6), 3), "words": ch,
                    "key": g._key(ch, KEYS), "pos": pos})
    return out


def main():
    if "--words" in sys.argv:
        print(" ".join("%s/%.1f" % (c["w"], c["s"]) for c in CAPS))
    chunks = rechunk(g.chunks(CAPS, keys=KEYS, place=PLACE))
    if "--chunks" in sys.argv:
        for c in chunks:
            print("%6.2f-%6.2f %s%s" % (c["s"], c["e"], " ".join(w["w"] for w in c["words"]),
                                        "  [%s]" % c["words"][c["key"]]["w"] if c["key"] is not None else ""))
    doc = g.document(title=u"Reel 51 — Твій стиль з першого дня", plate="assets/base.mp4",
                     behind="\n".join(B), panel="\n".join(P), front="\n".join(F), cover="\n".join(C),
                     js="\n".join(J), chunks=chunks, blackout=BLACKOUT, extra_css=EXTRA_CSS)
    g.write(HERE, doc)
    print("index.html  %d caption chunks, %d sfx cues, %d mattes" % (len(chunks), len(g.cues), len(g.mattes)))


main()
