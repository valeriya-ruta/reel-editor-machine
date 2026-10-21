# -*- coding: utf-8 -*-
"""Reel 45 — «Вчиться на статистиці». Posts 2026-10-21.

Google style + Excalidraw look (STYLE.md §00), built on reel 41's skeleton.
~34 s: one big plus of her AI system — it keeps learning from what is posted.

The one object is **the feedback loop**: a «+» opens it, the loop is drawn on
the half screen node by node as she names them (post -> w. Windsor -> report ->
Claude, ✓ worked / ✗ didn't -> back to the post, in red, on «вчиться»), the
logic becomes a rising curve over a row of posts, and the «+» comes back in the
CTA pill.

  above   «+» badge on «плюсів», «AI-система» pill, a red pointer «налаштовую я»
  half    the loop: навчається · пост · w. Windsor · звіт · Claude аналізує ·
          ✓ зайшло ✗ ні · the red return arrow on «вчиться»
  above   a card with a sketched graph: posts pile up along «контент», the
          curve «знає тебе» rises, red «краще» at its tip
  above   CTA chips блогерка / СММниця / підприємниця, a «команда» pill with
          the loop doodle on «оновлювану»
  behind  «24/7»
  above   «Команда 24/7» card: монтує / дизайнить / пише сценарії / …
  above   CTA pill «Пиши + у коментарі» + red pointer «сюди!»

usage: python build.py      (mattes: sh work/b1021/mattes.sh 45)
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
from gstyle import G, Words, load_caps, mark, esc  # noqa: E402,F401

NN = "45"
CUT = json.load(io.open(os.path.join(ROOT, "work", "r" + NN, "cut.json"), encoding="utf-8"))
DUR = 33.883           # (1017 plate frames - 0.5) / 30
g = G(dur=DUR, reel=NN)

# whisper's spelling of what she plainly said -> her word (checked on the plate)
FIX = {
    (u"один", 0.5): u"Один",
    u"IA": u"AI-системи,", u"системі": None,
    u"налаштовує": u"налаштовую",
    u"навчається.": u"навчається",
    u"Коло": u"Клод",
    u"а що ні,": u"що ні,",
    (u"чим", 18.9): u"Чим",
    u"Якщо": u"якщо",
    u"сесомевниця,": u"СММниця,",
    u"оновлювану...": u"оновлювану",
    u"дизайне,": u"дизайнить,",
}
CAPS = load_caps(NN, FIX)
W = Words(CAPS)
S, E = W.s, W.e

# ---------------------------------------------------------------- the beats
B, P, F, C, J = [], [], [], [], []     # behind / panel / front / cover html, js
BLACKOUT = []
PLACE = []                             # caption placement over the half screen
HALF = []
SKF = []                               # front sketches, drawn on top of the cards


def js(s):
    J.append(s)


# two sketch helpers this reel needs: a looping arc with a head, and an arrow
# along a hand-placed curve
js(u'''
  function headAt(s, x2, y2, ang, oo) {
    var L = 34, sp = .5;
    _add(s, s.rc.line(x2, y2, x2 - L * Math.cos(ang - sp), y2 - L * Math.sin(ang - sp), oo), "head");
    _add(s, s.rc.line(x2, y2, x2 - L * Math.cos(ang + sp), y2 - L * Math.sin(ang + sp), oo), "head");
  }
  function loopArc(name, cx, cy, w, h, a0, a1, o) {
    var s = SK[name], oo = opt(o, (o && o.seed) || 61);
    _add(s, s.rc.arc(cx, cy, w, h, a0, a1, false, oo));
    var x2 = cx + w / 2 * Math.cos(a1), y2 = cy + h / 2 * Math.sin(a1);
    headAt(s, x2, y2, Math.atan2(h / 2 * Math.cos(a1), -w / 2 * Math.sin(a1)), oo);
  }
  function parrow(name, pts, o) {
    var s = SK[name], oo = opt(o, (o && o.seed) || 67);
    _add(s, s.rc.curve(pts, oo));
    var a = pts[pts.length - 2], b = pts[pts.length - 1];
    headAt(s, b[0], b[1], Math.atan2(b[1] - a[1], b[0] - a[0]), oo);
  }
''')

# 1 · ABOVE — «+» on «плюсів», «AI-система», «налаштовую я» -> her --------------
t_plus, t_ai = S(u"плюсів", 1.65), S(u"AI-системи,", 2.11)
t_nal, t_ya = S(u"налаштовую", 3.21), E(u"я,", 4.01)
F.append(u'''
        <div id="b1p" class="hid" style="position:absolute; left:465px; top:350px; width:150px; height:150px;
             border-radius:50%%; background:#7A1424; color:#fff; display:flex; align-items:center;
             justify-content:center; font-weight:700; font-size:120px; line-height:1;
             box-shadow:0 1px 3px rgba(36,25,25,.12), 0 10px 30px rgba(122,20,36,.22)">
          <span style="margin-top:-10px">+</span></div>
        <div id="b1a" class="pill light hid" style="left:395px; top:363px; padding:26px 46px; gap:18px;
             font-weight:700; font-size:60px; letter-spacing:-0.02em">
          <span style="color:#7A1424; display:flex">%s</span>AI-система</div>''' % mark("claude", 56))
SKF.append(u'''
  sketch("h1", "skF"); parrow("h1", [[700, 512], [690, 590], [615, 668]], {stroke: "#7A1424", strokeWidth: 5, seed: 3});
  label("h1", 655, 600, "налаштовую я", {size: 46, color: "#7A1424", anchor: "end"});
  draw("h1", %.3f, .5);
  erase("h1", %.3f);''' % (t_nal - 0.15, t_ya + 0.12))
js(u'''
  pop("#b1p", %.3f, .6);
  tl.to("#b1p", {x: -260, duration: .5, ease: RISE}, %.3f);
  pop("#b1a", %.3f);
  sink("#b1p, #b1a", %.3f);
''' % (t_plus - 0.2, t_ai - 0.15, t_ai - 0.05, t_ya + 0.12))
g.sfx("pop", t_plus - 0.2); g.sfx("pop", t_ai - 0.05)

# 2 · HALF — the loop, node by node ------------------------------------------
h0, h1 = S(u"вона", 5.18) - 0.2, S(u"вчиться.", 16.24) + 0.62    # its real end is 16.84
HALF.append((h0, h1))
t_nav = S(u"навчається", 5.64)
t_kont, t_tob = S(u"контенті,", 7.91), S(u"Тобто", 9.46)
t_zvit, t_anal = S(u"звітність", 10.64), S(u"аналітики", 11.24)
t_klod, t_zai, t_ni = S(u"Клод", 12.55), S(u"зайшло,", 13.97), S(u"що ні,", 14.59)
t_dali, t_vch = S(u"і далі", 14.98), S(u"вчиться.", 16.24)
P.append(u'''<svg class="sk" id="skP" width="1080" height="1240" viewBox="0 0 1080 1240"></svg>
        <div id="pm1" class="hid" style="position:absolute; left:436px; top:334px; color:#7A1424">%s</div>
        <div id="pm3" class="hid" style="position:absolute; left:136px; top:655px; color:#7A1424">%s</div>
        <span id="pw" class="chip hid" style="position:absolute; left:786px; top:300px; font-size:30px;
              padding:10px 18px; gap:10px"><b style="font-weight:700; color:#7A1424">w.</b>Windsor</span>'''
         % (mark("instagram", 52), mark("claude", 50)))
js(u'''
  sketch("l0", "skP"); loopArc("l0", 540, 500, 112, 112, -1.75, 3.6, {seed: 5});
  label("l0", 540, 612, "навчається", {size: 46});
  draw("l0", %.3f, .7);
  sketch("n1", "skP"); box("n1", 390, 300, 300, 120, {seed: 7}); label("n1", 512, 380, "пост", {size: 52, anchor: "start"});
  draw("n1", %.3f, .6); fadein("#pm1", %.3f);
  sketch("a12", "skP"); parrow("a12", [[702, 362], [800, 420], [822, 604]], {seed: 9});
  draw("a12", %.3f, .55); pop("#pw", %.3f);
  sketch("n2", "skP"); box("n2", 670, 620, 300, 120, {seed: 11}); label("n2", 752, 698, "звіт", {size: 52});
  draw("n2", %.3f, .6);
  sketch("bars", "skP"); box("bars", 850, 680, 26, 36, {seed: 13, r: 6, fill: true});
  box("bars", 886, 660, 26, 56, {seed: 15, r: 6, fill: true}); box("bars", 922, 640, 26, 76, {seed: 17, r: 6, fill: true});
  draw("bars", %.3f, .3);
  sketch("a23", "skP"); arrow("a23", 660, 688, 422, 688, {seed: 19});
  draw("a23", %.3f, .5);
  sketch("n3", "skP"); box("n3", 110, 620, 300, 120, {seed: 21}); label("n3", 198, 697, "аналізує", {size: 46, anchor: "start"});
  draw("n3", %.3f, .6); fadein("#pm3", %.3f);
  sketch("ok", "skP"); _add(SK.ok, SK.ok.rc.linearPath([[128, 782], [146, 802], [178, 760]], opt({strokeWidth: 6}, 23)));
  label("ok", 190, 805, "зайшло", {size: 44, anchor: "start"});
  draw("ok", %.3f, .35);
  sketch("no", "skP"); ln("no", 346, 766, 374, 802, {stroke: "#7A1424", strokeWidth: 6, seed: 25});
  ln("no", 374, 766, 346, 802, {stroke: "#7A1424", strokeWidth: 6, seed: 27});
  label("no", 388, 805, "ні", {size: 44, anchor: "start", color: "#7A1424"});
  draw("no", %.3f, .25);
  sketch("a31", "skP"); parrow("a31", [[255, 606], [262, 450], [378, 368]], {stroke: "#7A1424", strokeWidth: 5.5, seed: 29});
  draw("a31", %.3f, .7);
  sketch("l1", "skP"); loopArc("l1", 540, 500, 112, 112, -1.75, 3.6, {stroke: "#7A1424", strokeWidth: 5.5, seed: 31});
  draw("l1", %.3f, .5);
  tl.to("#sk-l0 text", {fill: "#7A1424", duration: .3}, %.3f);
  %s
  out("#pm1, #pm3, #pw", %.3f);
''' % (t_nav - 0.05, t_kont - 0.1, t_kont + 0.2, t_tob + 0.3, t_tob + 0.65, t_zvit - 0.2, t_anal,
       t_klod - 0.55, t_klod - 0.05, t_klod + 0.25, t_zai - 0.05, t_ni - 0.05,
       t_dali + 0.3, t_vch - 0.2, t_vch,
       " ".join('erase("%s", %.3f);' % (n, h1) for n in ("l0", "n1", "a12", "n2", "bars", "a23", "n3", "ok", "no", "a31", "l1")),
       h1))
g.sfx("whoosh-short", h0); g.sfx("click-soft", t_nav); g.sfx("pop", t_kont)
g.sfx("pop", t_tob + 0.65); g.sfx("pop", t_klod); g.sfx("click-soft", t_zai); g.sfx("click-soft", t_vch)
g.sfx("whoosh-short", h1)

# 3 · ABOVE — the logic: posts pile up, the curve rises, «краще» ----------------
t_ale, t_prost = S(u"Але", 17.6), S(u"проста.", 18.37)
t_rob, t_kont2 = S(u"робиш", 19.35), S(u"контенту,", 19.57)
t_zna, t_kra = S(u"знає,", 21.13), S(u"краще", 21.75)
t_out3 = E(u"працює.", 22.21) + 0.08
F.append(u'''
        <div id="b3" class="card hid" style="left:110px; top:290px; width:860px; height:385px; padding:0"></div>''')
tiles = u" ".join(u'box("tl", %d, 548, 52, 64, {seed: %d, r: 12, fill: true});' % (250 + i * 100, 40 + i)
                  for i in range(6))
SKF.append(u'''
  sketch("ax", "skF"); arrow("ax", 190, 618, 190, 330, {seed: 33, bend: 0}); arrow("ax", 190, 618, 912, 618, {seed: 35, bend: 0});
  draw("ax", %.3f, .45);
  sketch("tl", "skF"); %s label("tl", 905, 664, "контент", {size: 40, anchor: "end"});
  draw("tl", %.3f, .3);
  sketch("cv", "skF"); parrow("cv", [[236, 505], [450, 490], [650, 445], [868, 352]], {seed: 37});
  label("cv", 214, 350, "знає тебе", {size: 42, anchor: "start"});
  draw("cv", %.3f, .9);
  sketch("kr", "skF"); ell("kr", 862, 362, 170, 112, {stroke: "#7A1424", strokeWidth: 5, seed: 39});
  label("kr", 752, 345, "краще", {size: 50, color: "#7A1424", anchor: "end"});
  draw("kr", %.3f, .5);
  erase("ax", %.3f); erase("tl", %.3f); erase("cv", %.3f); erase("kr", %.3f);''' % (
    t_prost - 0.4, tiles, t_rob - 0.35, t_zna - 0.9, t_kra - 0.2, t_out3, t_out3, t_out3, t_out3))
js(u'''
  rise("#b3", %.3f);
  sink("#b3", %.3f);
''' % (t_ale - 0.1, t_out3))
g.sfx("pop", t_ale - 0.1); g.sfx("click-soft", t_kra)

# 4 · ABOVE — CTA: who it is for, the same self-updating team -------------------
t_blog, t_smm, t_pid = S(u"блогерка,", 23.54), S(u"СММниця,", 24.24), S(u"підприємниця,", 24.94)
t_taku, t_onov = S(u"таку", 25.92), S(u"оновлювану", 26.54)
t_kom, t_24 = S(u"команду", 27.42), S(u"24", 28.0)
F.append(u'''
        <div id="b4" class="hid" style="position:absolute; left:120px; top:322px; width:840px;
             display:flex; gap:14px; justify-content:center">
          <span class="chip hid" id="b4a"><i></i>блогерка</span>
          <span class="chip hid" id="b4b"><i></i>СММниця</span>
          <span class="chip hid" id="b4c"><i></i>підприємниця</span>
        </div>
        <div id="b4t" class="pill light hid" style="left:358px; top:452px; padding-left:122px">команда</div>''')
SKF.append(u'''
  sketch("lp", "skF"); loopArc("lp", 420, 509, 62, 62, -1.75, 3.6, {stroke: "#7A1424", strokeWidth: 5, seed: 43});
  draw("lp", %.3f, .55);
  erase("lp", %.3f);''' % (t_onov - 0.1, t_kom + 0.33))
js(u'''
  fadein("#b4", %.3f, .01); pop("#b4a", %.3f); pop("#b4b", %.3f); pop("#b4c", %.3f);
  pop("#b4t", %.3f);
  sink("#b4, #b4t", %.3f);
''' % (t_blog - 0.15, t_blog - 0.1, t_smm - 0.1, t_pid - 0.1, t_taku - 0.1, t_kom + 0.33))
g.sfx("pop", t_blog - 0.1); g.sfx("pop", t_taku - 0.1)
BLACKOUT.append((t_smm - 0.05, t_smm + 0.05))     # the chips say «СММниця, підприємниця»

# 5 · BEHIND — «24/7» --------------------------------------------------------
m0, m1 = t_kom + 0.33, S(u"монтує,", 30.2) - 0.25
B.append(u'''
        <div id="bw" class="big hid" style="top:470px; font-size:300px">24/7</div>''')
g.matte("bw", round(m0 - 0.05, 3), round(m1 - m0 + 0.5, 3))
js(u'''
  rise("#bw", %.3f, 80);
  sink("#bw", %.3f);
''' % (m0, m1 - 0.3))
g.sfx("whoosh-short", m0)
BLACKOUT.append((t_24 - 0.05, t_24 + 0.05))       # «24/7» says it

# 6 · ABOVE — what the team does --------------------------------------------
t_mn, t_dz, t_ps, t_dal = S(u"монтує,", 30.2), S(u"дизайнить,", 30.62), S(u"пише", 31.16), S(u"так", 32.0)
t_to = S(u"то", 32.58)
F.append(u'''
        <div id="b6" class="card hid" style="left:120px; top:300px; width:840px; padding:34px 40px;">
          <span class="lbl">Команда 24/7</span>
          <div class="chips">
            <span class="chip on hid" id="b6a"><i></i>монтує</span>
            <span class="chip on hid" id="b6b"><i></i>дизайнить</span>
            <span class="chip on hid" id="b6c"><i></i>пише сценарії</span>
            <span class="chip hid" id="b6d">…</span>
          </div>
        </div>''')
js(u'''
  rise("#b6", %.3f);
  pop("#b6a", %.3f); pop("#b6b", %.3f); pop("#b6c", %.3f); pop("#b6d", %.3f);
  sink("#b6", %.3f);
''' % (m1 - 0.25, t_mn - 0.05, t_dz - 0.05, t_ps - 0.05, t_dal - 0.1, t_to - 0.2))
g.sfx("pop", m1 - 0.25)
BLACKOUT.append((t_mn - 0.05, t_mn + 0.05))       # the chips say it

# 7 · ABOVE — CTA pill + pointer --------------------------------------------
t_pyshy, t_plus2 = S(u"пиши", 32.7), S(u"плюс", 32.96)
F.append(u'''
        <div style="position:absolute; left:0; top:440px; width:1080px; display:flex; justify-content:center">
          <div id="b7" class="pill hid" style="position:relative">Пиши + у коментарі</div>
        </div>''')
SKF.append(u'''
  sketch("a7", "skF"); parrow("a7", [[800, 580], [850, 690], [872, 840]], {stroke: "#7A1424", strokeWidth: 5, seed: 47});
  label("a7", 890, 905, "сюди!", {size: 52, color: "#7A1424"});
  draw("a7", %.3f, .5);''' % (t_plus2 - 0.2))
js(u'''
  pop("#b7", %.3f, .6);
''' % (t_to - 0.12))
g.sfx("pop", t_to - 0.12)
BLACKOUT.append((t_to - 0.05, DUR))               # the pill says it

# the front sketch layer goes last so its strokes sit on top of the cards
F.append(u'<svg class="sk" id="skF" width="1080" height="1920" viewBox="0 0 1080 1920"></svg>')
J.extend(SKF)

# ---------------------------------------------------------------- mattes for the half screen
for i, (a, b) in enumerate(HALF):
    g.matte("half%d" % (i + 1), round(a - 0.1, 3), round(b - a + 1.2, 3))
    js("  half(%.3f, %.3f);" % (a, b))
    PLACE.append((a + 0.4, b + 0.2, "bottom", 980))


# captions: phrase by phrase, each break on her own phrasing; key words pinned
BREAKS = [(u"так", 2.95), (u"це", 4.23), (u"навчається", 5.64), (u"на", 7.51), (u"Тобто", 9.46),
          (u"аналітики", 11.24), (u"Клод", 12.55), (u"що", 13.81), (u"і далі", 14.98), (u"Але", 17.6),
          (u"Чим", 18.87), (u"тим більше", 20.17), (u"і", 21.51), (u"Тому", 22.87), (u"СММниця,", 24.24),
          (u"і ти", 25.52), (u"24", 28.0), (u"яка працює", 28.96), (u"монтує,", 30.2), (u"то", 32.58)]
KEYS = [(u"плюсів", 1.65), (u"налаштовую", 3.21), (u"навчається", 5.64), (u"постемо.", 8.79),
        (u"звітність", 10.64), (u"аналітики", 11.24), (u"аналізує,", 13.13), (u"зайшло,", 13.97),
        (u"вчиться.", 16.24), (u"проста.", 18.37), (u"контенту,", 19.57), (u"знає,", 21.13),
        (u"краще", 21.75), (u"блогерка,", 23.54), (u"оновлювану", 26.54), (u"контентом,", 29.6)]


def phrase_chunks():
    cut = sorted(S(w, t) for w, t in BREAKS)
    groups, cur = [], []
    for c in CAPS:
        if cur and any(abs(c["s"] - t) < 0.01 for t in cut):
            groups.append(cur)
            cur = []
        cur.append(c)
    groups.append(cur)
    keys = dict((S(w, t), True) for w, t in KEYS)
    res = []
    for grp in groups:
        res.extend(g.chunks(grp, keys=keys, place=PLACE, max_chars=44, max_words=7))
    for a, b in zip(res, res[1:]):
        a["e"] = round(min(a["e"], b["s"]), 3)
    for c in res:          # the panel's last caption leaves with the panel
        if c["s"] < h1 < c["e"]:
            c["e"] = round(h1 + 0.25, 3)
    return res


def main():
    chunks = phrase_chunks()
    if "-v" in sys.argv:
        print(" ".join(u"%s/%.1f" % (c["w"], c["s"]) for c in CAPS))
        for n, c in enumerate(chunks):
            k = c["words"][c["key"]]["w"] if c["key"] is not None else u"-"
            print(u"cap%-2d %6.2f-%6.2f  [%s]  %s" % (n, c["s"], c["e"], k, u" ".join(w["w"] for w in c["words"])))
    doc = g.document(title=u"Reel 45 — Вчиться на статистиці", plate="assets/base.mp4",
                     behind="\n".join(B), panel="\n".join(P), front="\n".join(F), cover="\n".join(C),
                     js="\n".join(J), chunks=chunks, blackout=BLACKOUT)
    g.write(HERE, doc)
    print("index.html  %d caption chunks, %d sfx cues, %d mattes" % (len(chunks), len(g.cues), len(g.mattes)))
    print("half-screen %s   matte seconds %.2f" % (
        ", ".join("%.2f-%.2f (%.2f s)" % (a, b, b - a) for a, b in HALF),
        sum(float(m.split('data-duration="')[1].split('"')[0]) for m in g.mattes)))


main()
