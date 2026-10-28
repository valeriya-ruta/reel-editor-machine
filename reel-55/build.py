# -*- coding: utf-8 -*-
"""Reel 55 — «Plan with me»: how her AI content system plans a week.

HER cut (Drive VID_20261028_052210_749_bsl.mp4, 4769 frames) — her rule this
time: *"dont do closeups and dont change the cuts just animations and
subtitles"*. Look: STYLE.md §00, Google style + Excalidraw (tools/gstyle.py).

Her brief: candid, "here's how it actually happens", her screen on the top
half and her under it. So the middle is one long half screen: a white panel
holding her real 36-min desktop recording, cut into sped-up clips
(work/r55/clips.py) that zoom onto the moment she names — `/content-plan`, the
tool calls, her typing, «та чекай, 11 мало, треба ж 14 нам», the RUTA app.

The panel stops at y 860 and the video pushes down 280 px (not the kit's
1240 / 330): her hair is at y ≈ 620 on this plate, so this keeps her whole
face clear of the panel with no matte, and her chin (≈ y 1360 pushed) sits
right above the caption rail. `half2()` is the kit's `half()` with those two
numbers; captions stay on her rail (white on the plaque) under it.

The chain: the week (hook) → her real Instagram insights drop in on the panel
→ they slide off as the screen lands on «зверху буде екран» → the screen run
→ fourteen reels → Google Drive → link → Claude Code → laptop / phone / cloud
sketch on the panel → the evening schedule → the checklist → the week again,
every day ticked → consultation | done-for-you → «+» and an arrow down.

usage: python3 build.py   (then: python3 ../work/r55/clips.py; python3 ../tools/sfx.py mix 55)
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
W55 = os.path.join(ROOT, "work", "r55")
sys.path.insert(0, os.path.join(ROOT, "tools"))
from gstyle import G, Words, load_caps, mark  # noqa: E402

NN = "55"
DUR = 158.950          # (4769 plate frames - 0.5) / 30
g = G(dur=DUR, reel=NN)

CAPS = load_caps(NN)
W = Words(CAPS)
S, E = W.s, W.e

B, P, F, C, J = [], [], [], [], []
BLACKOUT = []


def js(s):
    J.append(s)


def bo(a, b):
    BLACKOUT.append((round(a - 0.03, 3), round(b + 0.03, 3)))


PANEL_H, PUSH_Y = 860, 280
CSS = u"""
    #panel { height: %(ph)dpx; }
    #win { position: absolute; left: 90px; top: 290px; width: 900px; height: 530px; overflow: hidden;
           border-radius: 32px; background: #FAFAFA; border: 2px solid var(--outline-var);
           box-shadow: 0 1px 3px rgba(36,25,25,.10), 0 10px 30px rgba(36,25,25,.12); }
    #zm { position: absolute; left: 0; top: 0; width: 900px; height: 670px; transform-origin: 0 0; }
    .sv { position: absolute; left: 0; top: 0; width: 900px; height: 667px; }
    #skZ { position: absolute; left: 0; top: 0; }
    #clk { position: absolute; right: 16px; top: 14px; display: inline-flex; align-items: center; gap: 10px;
           background: #fff; border: 2px solid var(--outline-var); border-radius: 16px; padding: 8px 16px;
           font-weight: 700; font-size: 30px; color: var(--primary); font-variant-numeric: tabular-nums;
           box-shadow: 0 1px 3px rgba(36,25,25,.10), 0 6px 16px rgba(36,25,25,.10); }
    #clk svg { width: 28px; height: 28px; }
    .badge { position: absolute; display: inline-flex; align-items: center; gap: 12px; }
    #gdr .chip { white-space: nowrap; }
    .badge .mark path { fill: var(--primary); }
    .shot { position: absolute; border-radius: 28px; overflow: hidden; background: #fff;
            box-shadow: 0 1px 3px rgba(36,25,25,.12), 0 14px 34px rgba(36,25,25,.16); }
    .shot img { display: block; width: 100%%; }
    .day { display: inline-flex; flex-direction: column; align-items: center; gap: 10px; width: 92px; }
    .day b { font-weight: 700; font-size: 26px; color: var(--on-surface-var); letter-spacing: .06em; }
    .day .check { width: 52px; height: 52px; }
    .bar { height: 18px; border-radius: 9px; background: #EFE3E3; overflow: hidden; position: relative; }
    .bar i { position: absolute; left: 0; top: 0; bottom: 0; width: 100%%; background: var(--primary);
             transform-origin: 0 50%%; border-radius: 9px; }
    .dot { width: 26px; height: 26px; border-radius: 50%%; background: var(--primary); display: inline-block; }
""".replace("%(ph)d", str(PANEL_H)).replace("%%", "%")

HALF2 = u'''
  function half2(t0, t1) {     // the kit's half(): panel to y %d, video down %d px
    tl.fromTo("#panel", {yPercent: -101}, X({yPercent: 0, duration: .85, ease: SLIDE}), t0);
    tl.fromTo(PUSH, {y: 0}, X({y: %d, duration: .85, ease: SLIDE}), t0);
    tl.to("#panel", {yPercent: -101, duration: .85, ease: SLIDE}, t1);
    tl.to(PUSH, {y: 0, duration: .85, ease: SLIDE}, t1);
  }
''' % (PANEL_H, PUSH_Y, PUSH_Y)
js(HALF2)

F.append(u'<svg class="sk" id="skF" width="1080" height="1920" viewBox="0 0 1080 1920"></svg>')
TICK = u'<svg class="tk" viewBox="0 0 30 30" style="position:absolute;left:8px;top:8px;width:calc(100% - 16px);height:calc(100% - 16px);opacity:0"><path d="M6 16l6 6L24 8" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>'

# 1 · ABOVE — the week, planned by her AI producer ----------------------------
t_plan, t_tyzh, t_ai = S(u"сплануємо", 0.8), S(u"тиждень", 1.8), S(u"AI-продюсеру.", 2.9)
DAYS = [u"ПН", u"ВТ", u"СР", u"ЧТ", u"ПТ", u"СБ", u"НД"]


def week(wid, top, done):
    cells = "".join(u'<span class="day"><b>%s</b><span class="check" id="%s_%d">%s</span></span>'
                    % (d, wid, i, TICK) for i, d in enumerate(DAYS))
    return (u'<div class="card hid" id="%s" style="left:0; right:0; margin:auto; width:max-content; top:%dpx;'
            u' padding:28px 34px"><div class="row" style="gap:8px">%s</div></div>' % (wid, top, cells))


F.append(week("wk1", 290, False))
F.append(u'''<div id="aiP" class="pill hid" style="left:0; right:0; margin:auto; width:max-content; top:470px;
     padding:22px 40px; font-size:44px">%s AI-продюсер</div>''' % mark("claude", 46))
js(u'''
  rise("#wk1", %.3f);
  ["#wk1_0","#wk1_1","#wk1_2","#wk1_3","#wk1_4","#wk1_5","#wk1_6"].forEach(function (s, i) {
    tl.to(s, {backgroundColor: "#7A1424", borderColor: "#7A1424", duration: .15}, %.3f + i * .12); });
  pop("#aiP", %.3f);
  sink("#wk1", %.3f); sink("#aiP", %.3f);
''' % (t_plan - 0.2, t_tyzh, t_ai - 0.05, E(u"AI-продюсеру.", 2.9) + 0.35, E(u"AI-продюсеру.", 2.9) + 0.35))
g.sfx("pop", t_plan - 0.2); g.sfx("click-soft", t_tyzh); g.sfx("pop", t_ai)
bo(t_ai, E(u"AI-продюсеру.", 2.9))

# 2 · HALF — her real insights, then the screen run ----------------------------
H0 = S(u"I", 4.0) - 0.35 if False else S(u"І", 4.0) - 0.3
H1 = S(u"Знімаю", 96.3) - 0.55
js(u"  half2(%.3f, %.3f);" % (H0, H1))
g.sfx("whoosh-short", H0); g.sfx("whoosh-short", H1)
P.append(u'''
        <div class="shot hid" id="pr1" style="left:150px; top:300px; width:780px"><img src="assets/proof/ig-insights-summary.jpg"></div>
        <div class="shot hid" id="pr2" style="left:90px; top:330px; width:900px"><img src="assets/proof/chart.png"></div>
        <svg class="sk" id="skP" width="1080" height="%d" viewBox="0 0 1080 %d"></svg>''' % (PANEL_H, PANEL_H))
t_best, t_tret, t_300 = S(u"найкраща,", 5.3), S(u"третій", 9.2), S(u"300", 11.1)
t_kupa, t_zverhu = S(u"купа", 12.8), S(u"зверху", 15.4)
js(u'''
  rise("#pr1", %.3f);
  tl.to("#pr1", {y: -40, scale: .92, autoAlpha: 0, duration: .45, ease: "power2.in"}, %.3f);
  rise("#pr2", %.3f);
  sketch("pC", "skP"); ell("pC", 900, 365, 120, 120, {stroke: "#7A1424", strokeWidth: 6, seed: 5, fill: false});
  label("pC", 790, 330, "↗ +253%%", {size: 46, color: "#7A1424", anchor: "end"});
  draw("pC", %.3f);
  sketch("pD", "skP"); under("pD", 300, 795, 780, {stroke: "#7A1424", strokeWidth: 6, seed: 9});
  label("pD", 540, 770, "+ купа запитів у директ", {size: 50});
  draw("pD", %.3f);
  erase("pC", %.3f); erase("pD", %.3f);
  tl.to("#pr2", {y: -60, autoAlpha: 0, duration: .45, ease: "power2.in"}, %.3f);
''' % (t_best - 0.3, t_tret - 0.35, t_tret - 0.15, t_300 - 0.3, t_kupa - 0.1,
       t_zverhu - 0.45, t_zverhu - 0.45, t_zverhu - 0.45))
g.sfx("pop", t_best - 0.3); g.sfx("pop", t_tret - 0.15); g.sfx("click-soft", t_300); g.sfx("click-soft", t_kupa)
bo(t_kupa, E(u"директ,", 13.7))

# the screen window: her recording, clip by clip
ANCH = [
    ("c0_home",     u"зверху", 15.4, -0.05),
    ("c1_skill",    u"Отже,", 19.7, 0.0),
    ("c2_tools",    u"Він", 22.6, 0.0),
    ("c3_hypo",     u"І", 34.9, 0.0),
    ("c3b_leads",   u"заклики", 42.7, 0.0),
    ("c4_calls",    u"Другий", 44.0, 0.0),
    ("c4c_threads", u"А", 54.7, 0.0),
    ("c5_ideas",    u"І", 58.8, 0.0),
    ("c6_list",     u"Він", 68.9, 0.0),
    ("c7_pick",     u"Я", 75.2, 0.0),
    ("c8_14",       u"14–15,", 77.9, 0.0),
    ("c9_ruta",     u"заливає", 79.5, 0.0),
    ("c10_app",     u"я", 81.7, 0.0),
    ("c11_done",    u"Вуаля,", 93.6, 0.0),
]
SLOTS = [(n, round(S(w, t) + d, 3)) for n, w, t, d in ANCH]
SLOT = {}
for i, (n, t0) in enumerate(SLOTS):
    SLOT[n] = (t0, SLOTS[i + 1][1] if i + 1 < len(SLOTS) else round(H1 + 0.9, 3))
io.open(os.path.join(W55, "slots.json"), "w", encoding="utf-8").write(
    json.dumps({n: round(b - a, 3) for n, (a, b) in SLOT.items()}, indent=1))
_CL = json.load(io.open(os.path.join(W55, "clips.json"), encoding="utf-8"))
for n, (a, b) in SLOT.items():
    if n not in _CL or abs(_CL[n][2] - (b - a)) > 0.02:
        print("STALE CLIP %s (slot %.3f) — run work/r55/clips.py" % (n, b - a))

vids = "".join(u'<video id="v_%s" class="sv" src="assets/scr/%s.mp4" data-start="%.3f" data-duration="%.3f" '
               u'data-media-start="0" muted playsinline></video>' % (n, n, a, b - a) for n, (a, b) in SLOT.items())
CLOCK = (u'<svg viewBox="0 0 28 28"><circle cx="14" cy="14" r="11" fill="none" stroke="#7A1424" stroke-width="3"/>'
         u'<path d="M14 8v6l4 3" fill="none" stroke="#7A1424" stroke-width="3" stroke-linecap="round"/></svg>')
P.append(u'''
        <div id="win" class="hid"><div id="zm">%s
          <svg class="sk" id="skZ" width="900" height="670" viewBox="0 0 900 670"></svg></div>
          <div id="clk" class="hid">%s<span id="clkT">0:00</span></div></div>
        <span class="chip badge hid" id="bF" style="left:640px; top:760px">%s Fathom</span>
        <span class="chip badge hid" id="bT" style="left:640px; top:760px">%s Threads</span>
        <span class="chip on badge hid" id="bR" style="left:700px; top:760px; font-weight:700">RUTA</span>''' % (
    vids, CLOCK, mark("fathom", 34), mark("threads", 34)))
js(u'  rise("#win", %.3f);' % (SLOT["c0_home"][0] - 0.25))
js(u'  tl.to("#win", {autoAlpha: 0, duration: .25}, %.3f);' % (H1 + 0.6))
for n, (a, b) in SLOT.items():
    js(u'  tl.set("#v_%s", {autoAlpha: 0}, 0); tl.set("#v_%s", {autoAlpha: 1}, %.3f); tl.set("#v_%s", {autoAlpha: 0}, %.3f);'
       % (n, n, a, n, b + 0.04))

VW, VH, WW, WH = 900.0, 667.0, 900.0, 530.0


def _xy(px, py, s, left):
    x = min(0.0, max(WW - VW * s, WW / 2.0 - px * s))
    if left is not None:
        x = min(0.0, max(x, 14 - left * s))
    y = min(0.0, max(WH - VH * s, WH / 2.0 - py * s))
    return x, y


def zoom(t, px, py, s, d=0.75, ease="power3.inOut", left=26):
    x, y = _xy(px, py, s, left)
    js(u'  tl.to("#zm", {x: %.1f, y: %.1f, scale: %.4f, duration: %.2f, ease: "%s"}, %.3f);' % (x, y, s, d, ease, t))


def zset(t, px, py, s, left=26):
    x, y = _xy(px, py, s, left)
    js(u'  tl.set("#zm", {x: %.1f, y: %.1f, scale: %.4f}, %.3f);' % (x, y, s, t))


def clock(t0, t1, s0, s1):
    js(u'  tl.set("#clk", {autoAlpha: 1}, %.3f); tl.set("#clk", {autoAlpha: 0}, %.3f);' % (t0, t1))
    js(u'  (function(){var o={v:%d},el=document.getElementById("clkT");'
       u'tl.fromTo(o,{v:%d},{v:%d,duration:%.3f,ease:"none",immediateRender:false,onUpdate:function(){'
       u'var v=Math.round(o.v);el.textContent=Math.floor(v/60)+":"+("0"+v%%60).slice(-2);}},%.3f);})();'
       % (s0, s0, s1, t1 - t0, t0))


def badge(bid, t, t_out):
    js(u'  pop("#%s", %.3f); sink("#%s", %.3f);' % (bid, t, bid, t_out))
    g.sfx("pop", t)


s = SLOT
INPUT, HOME, TOOLS = (450, 580), (450, 372), (312, 173)
zset(s["c0_home"][0], HOME[0], HOME[1], 1.0, left=None)
zoom(s["c0_home"][0] + 1.2, HOME[0], HOME[1], 1.45, 1.4, "power2.inOut", left=None)
# /content-plan typed and sent
zset(s["c1_skill"][0], HOME[0], HOME[1], 1.45, left=None)
zoom(s["c1_skill"][0] + 1.5, 450, 333, 1.0, 0.7)
g.sfx("typing", s["c1_skill"][0] + 0.2); g.sfx("click", s["c1_skill"][0] + 1.4)
# the tool calls ticking, on her recording's own clock
zoom(s["c2_tools"][0], TOOLS[0], TOOLS[1], 1.55)
clock(s["c2_tools"][0], s["c2_tools"][1], 11 - 6, 55 - 6)
js(u'''
  sketch("z1", "skZ"); ell("z1", 797, 31, 200, 66, {stroke: "#7A1424", strokeWidth: 5, seed: 3, fill: false});
  draw("z1", %.3f); erase("z1", %.3f);
  sketch("z2", "skZ"); under("z2", 104, 174, 300, {stroke: "#7A1424", strokeWidth: 5, seed: 7});
  draw("z2", %.3f, .5); erase("z2", %.3f);
''' % (s["c2_tools"][0] + 0.2, S(u"особливо", 26.4) - 0.4, S(u"останній", 27.7) - 0.1, S(u"тестувати", 29.0)))
zoom(S(u"останній", 27.7) - 0.3, 200, 160, 1.9, 0.6)
zoom(S(u"тестувати", 29.0), TOOLS[0], TOOLS[1] + 30, 1.55, 0.7)
zoom(S(u"останній", 34.0) - 0.3, 200, 160, 1.9, 0.5)
g.sfx("click-soft", S(u"останній", 27.7))
# what worked: the hypotheses
zset(s["c3_hypo"][0], 450, 333, 1.0)
clock(s["c3_hypo"][0], s["c3_hypo"][1], 128 - 6, 178 - 6)
zoom(S(u"гачки", 40.2) - 0.15, 407, 286, 1.3, 0.7)
# «заклики до дій» — her own reply: «так але + це мій основний дохід, мені треба ліди»
zset(s["c3b_leads"][0], 450, 147, 1.1)
# ideas from her calls (Fathom) and Threads
zset(s["c4_calls"][0], TOOLS[0], TOOLS[1] + 30, 1.55)
badge("bF", S(u"дзвінків,", 52.3) - 0.1, s["c4_calls"][1] - 0.2)
bo(S(u"дзвінків,", 52.3), E(u"дзвінків,", 52.3))
zset(s["c4c_threads"][0], 407, 333, 1.25)
badge("bT", S(u"Threads,", 55.3) - 0.05, s["c4c_threads"][1] - 0.2)
bo(S(u"Threads,", 55.3), E(u"Threads,", 55.3))
# meanwhile she types her own ideas
zset(s["c5_ideas"][0], INPUT[0], INPUT[1], 1.7)
zoom(s["c5_ideas"][0] + 4.5, INPUT[0] + 330, INPUT[1], 1.7, 2.6, "sine.inOut", left=None)
g.sfx("typing", s["c5_ideas"][0] + 0.3)
# the big numbered list, her picks, «та чекай, 11 мало, треба ж 14 нам»
zset(s["c6_list"][0], 450, 333, 1.0)
zoom(s["c6_list"][0] + 0.2, 407, 346, 1.22, 1.2, "power2.out")
zset(s["c7_pick"][0], 450, 545, 1.3)
zset(s["c8_14"][0], 724, 411, 1.0, left=None)
zoom(s["c8_14"][0] + 0.05, 724, 411, 2.0, 0.4, "power3.out", left=None)
js(u'''
  sketch("z3", "skZ"); ell("z3", 724, 411, 290, 70, {stroke: "#7A1424", strokeWidth: 4, seed: 11, fill: false});
  draw("z3", %.3f, .45); erase("z3", %.3f);
''' % (s["c8_14"][0] + 0.35, s["c8_14"][1] - 0.1))
g.sfx("click-soft", s["c8_14"][0] + 0.35)
# into RUTA
zset(s["c9_ruta"][0], 312, 286, 1.5)
badge("bR", S(u"Рута,", 81.1) - 0.15, s["c9_ruta"][1] - 0.1)
# the RUTA app: a voice note per idea, then «Зробити рілс»
zset(s["c10_app"][0], 450, 329, 1.3, left=None)
zoom(S(u"записую", 86.5) - 0.15, 760, 639, 1.9, 0.7, left=None)
zoom(S(u"тему.", 88.9), 450, 329, 1.3, 0.8, left=None)
g.sfx("click", S(u"записую", 86.5) + 0.3)
zset(s["c11_done"][0], 450, 310, 1.3, left=None)
js(u'''
  sketch("z4", "skZ"); box("z4", 560, 18, 300, 64, {stroke: "#7A1424", strokeWidth: 4, seed: 13, fill: false});
  draw("z4", %.3f, .5); erase("z4", %.3f);
''' % (S(u"Вуаля,", 93.6) + 0.1, H1 + 0.2))
g.sfx("sparkle", S(u"Вуаля,", 93.6))

# 3 · ABOVE — fourteen reels, Google Drive, the link, Claude Code ----------------
t_14 = S(u"14", 97.3)
boxes = []
for i in range(14):
    r, c = divmod(i, 7)
    boxes.append(u'box("fr", %d, %d, 92, 140, {seed: %d, r: 20});' % (128 + c * 118, 300 + r * 160, 31 + i))
js(u'''
  sketch("fr", "skF"); %s
  draw("fr", %.3f, .14);
  erase("fr", %.3f);
''' % (" ".join(boxes), t_14 - 0.3, S(u"заливаю", 100.0) - 0.1))
g.sfx("pop", t_14 - 0.3); g.sfx("whoosh-short", S(u"заливаю", 100.0) - 0.1)
t_gd, t_pos, t_cc = S(u"Google", 101.7), S(u"посилання", 102.7), S(u"Claude", 104.9)
F.append(u'''
        <div id="gdr" style="position:absolute; left:90px; width:900px; top:300px; display:flex; gap:14px;
             justify-content:center; align-items:center">
          <span class="chip hid" id="g1" style="font-size:40px">%s Google Диск</span>
          <svg id="g1a" class="hid" width="64" height="40" viewBox="0 0 64 40"><path d="M4 20 H52 M38 6 L54 20 L38 34"
               fill="none" stroke="#7A1424" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>
          <span class="chip hid" id="g2" style="font-size:40px"><i></i>посилання</span>
          <svg id="g2a" class="hid" width="64" height="40" viewBox="0 0 64 40"><path d="M4 20 H52 M38 6 L54 20 L38 34"
               fill="none" stroke="#7A1424" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>
          <span class="chip on hid" id="g3" style="font-size:40px">%s Claude Code</span>
        </div>
        <div class="card hid" id="g4" style="left:240px; width:600px; top:450px; padding:28px 36px">
          <span class="lbl">Claude Code</span>
          <div class="bar"><i id="g4i"></i></div>
        </div>''' % (mark("googledrive", 40).replace('class="mark"', 'class="mark logo"'), mark("claude", 40)))
t_mont, t_styl = S(u"монтувати", 106.8), S(u"стилі.", 107.8)
js(u'''
  pop("#g1", %.3f); fadein("#g1a", %.3f, .2); pop("#g2", %.3f); fadein("#g2a", %.3f, .2); pop("#g3", %.3f);
  rise("#g4", %.3f);
  gsap.set("#g4i", {scaleX: 0});
  tl.fromTo("#g4i", {scaleX: 0}, X({scaleX: 1, duration: %.3f, ease: "power1.inOut"}), %.3f);
  sink("#gdr", %.3f); sink("#g4", %.3f);
''' % (t_gd - 0.05, t_pos - 0.3, t_pos - 0.05, t_cc - 0.3, t_cc - 0.05,
       S(u"Клод,", 105.7) - 0.2, t_styl - t_mont + 0.4, t_mont - 0.1, E(u"стилі.", 107.8) + 0.05, E(u"стилі.", 107.8) + 0.05))
for t in (t_gd, t_pos, t_cc):
    g.sfx("pop", t)
bo(t_gd, E(u"Диск,", 102.1)); bo(t_pos, E(u"Диск", 103.8)); bo(t_cc, E(u"Code.", 105.2))

# 4 · HALF — computer or phone, «курси кажуть», not needed, the cloud ----------
H2 = S(u"Причому", 108.1) - 0.35
H3 = S(u"А", 119.5) - 0.2         # «А я знаю» + the hair flip are hers: off the panel by then
js(u"  half2(%.3f, %.3f);" % (H2, H3))
g.sfx("whoosh-short", H2); g.sfx("whoosh-short", H3)
t_komp, t_tel = S(u"комп'ютера,", 109.6), S(u"телефона.", 110.5)
t_kursy, t_vidk, t_ne, t_hm = S(u"курси,", 113.5), S(u"відкритий.", 116.1), S(u"Не", 116.8), S(u"хмарі.", 119.1)
t_von = S(u"Вони", 117.3)
CLOUD = ("M300 640 C240 640 220 580 262 556 C252 500 330 478 362 516 C392 462 486 470 494 532 "
         "C552 524 572 600 520 632 C510 650 480 652 470 640 Z")
js(u'''
  sketch("q1", "skP");
  box("q1", 150, 320, 340, 210, {seed: 41});
  ln("q1", 120, 548, 520, 548, {seed: 43, strokeWidth: 6});
  label("q1", 320, 440, "комп'ютер", {size: 52});
  draw("q1", %.3f);
  sketch("q2", "skP");
  box("q2", 610, 300, 240, 260, {seed: 47, r: 30});
  label("q2", 730, 450, "телефон", {size: 46});
  draw("q2", %.3f);
  sketch("q3", "skP");
  label("q3", 540, 640, "курси: «комп'ютер має бути відкритий»", {size: 46});
  draw("q3", %.3f);
  sketch("q4", "skP");
  ln("q4", 150, 628, 930, 650, {stroke: "#7A1424", strokeWidth: 7, seed: 51});
  draw("q4", %.3f, .4);
  erase("q1", %.3f); erase("q2", %.3f); erase("q3", %.3f); erase("q4", %.3f);
  sketch("q5", "skP");
  blob("q5", "%s", [220, 470, 360, 182], {seed: 53});
  label("q5", 400, 590, "хмара", {size: 56, color: "#7A1424"});
  arrow("q5", 600, 560, 780, 470, {seed: 55, bend: -.15});
  label("q5", 840, 450, "працює сам", {size: 46});
  draw("q5", %.3f, .6);
''' % (t_komp - 0.4, t_tel - 0.35, t_kursy - 0.1, t_ne - 0.1,
       t_von, t_von, t_von, t_von, CLOUD, t_von + 0.1))
g.sfx("click-soft", t_komp - 0.4); g.sfx("click-soft", t_tel - 0.35); g.sfx("click", t_ne); g.sfx("pop", t_von + 0.1)
bo(t_komp, E(u"комп'ютера,", 109.6)); bo(t_tel, E(u"телефона.", 110.5))
bo(S(u"комп'ютер", 115.6), t_vidk + 0.5)

# 5 · ABOVE — two a day, in the evening, Instagram and TikTok -----------------
t_plan2, t_dva, t_ig, t_tt = S(u"планує", 123.5), S(u"два", 124.1), S(u"Instagram", 125.1), S(u"TikTok.", 125.6)
rows = "".join(u'<div class="row" style="gap:22px; margin-top:14px"><b style="width:70px; font-size:30px; '
               u'color:var(--on-surface-var)">%s</b><span class="dot hid" id="sa%d"></span>'
               u'<span class="dot hid" id="sb%d"></span></div>' % (d, i, i) for i, d in enumerate(DAYS[:3]))
F.append(u'''<div class="card hid" id="sch" style="left:150px; width:420px; top:290px; padding:30px 38px">
          <span class="lbl">вечір</span>%s</div>
        <div id="schm" style="position:absolute; left:610px; top:330px; display:flex; flex-direction:column; gap:16px">
          <span class="chip hid" id="sI">%s Instagram</span>
          <span class="chip hid" id="sT">%s TikTok</span></div>''' % (rows, mark("instagram", 36), mark("tiktok", 36)))
js(u'  rise("#sch", %.3f);' % (t_plan2 - 0.2))
for i in range(3):
    js(u'  pop("#sa%d", %.3f, .4); pop("#sb%d", %.3f, .4);' % (i, t_dva + 0.08 * i, i, t_dva + 0.2 + 0.08 * i))
js(u'  pop("#sI", %.3f); pop("#sT", %.3f); sink("#sch", %.3f); sink("#schm", %.3f);'
   % (t_ig - 0.05, t_tt - 0.05, E(u"TikTok.", 125.6) + 0.4, E(u"TikTok.", 125.6) + 0.4))
g.sfx("pop", t_plan2 - 0.2); g.sfx("click-soft", t_dva); g.sfx("pop", t_ig); g.sfx("pop", t_tt)
bo(t_ig, E(u"TikTok.", 125.6))

# 6 · ABOVE — the checklist, then it posts by itself --------------------------
items = [(u"субтитри", S(u"субтитри,", 133.2)), (u"анімації", S(u"анімації,", 133.6)), (u"все як треба", S(u"все", 134.0))]
lst = "".join(u'<div class="row" style="margin-top:%dpx"><span class="check" id="ck%d">%s</span>'
              u'<span style="font-size:42px; font-weight:500">%s</span></div>' % (0 if i == 0 else 16, i, TICK, n)
              for i, (n, t) in enumerate(items))
F.append(u'<div class="card hid" id="chk" style="left:270px; width:540px; top:290px; padding:34px 40px">%s</div>' % lst)
F.append(u'<span class="chip on hid" id="auto" style="position:absolute; left:0; right:0; margin:auto; width:max-content;'
         u' top:330px; font-size:40px">%s постить сам</span>' % mark("instagram", 36).replace('<path', '<path style="fill:#fff"'))
js(u'  rise("#chk", %.3f);' % (items[0][1] - 0.6))
for i, (n, t) in enumerate(items):
    js(u'  tl.to("#ck%d", {backgroundColor: "#7A1424", borderColor: "#7A1424", duration: .12}, %.3f);'
       u' tl.to("#ck%d .tk", {opacity: 1, duration: .12}, %.3f);' % (i, t, i, t))
    g.sfx("click-soft", t)
js(u'''
  sink("#chk", %.3f);
  pop("#auto", %.3f); sink("#auto", %.3f);
''' % (E(u"треба.", 134.3) + 0.3, S(u"автоматично", 136.5) - 0.1, E(u"Instagram.", 137.8) + 0.3))
g.sfx("pop", S(u"автоматично", 136.5) - 0.1)
bo(items[0][1], E(u"треба.", 134.3)); bo(S(u"постить", 135.7), E(u"автоматично", 136.5))

# 7 · ABOVE — the week again, every day ticked --------------------------------
t_spl = S(u"спланували", 140.8)
F.append(week("wk2", 290, True))
js(u'  rise("#wk2", %.3f);' % (S(u"система,", 139.4) - 0.3))
for i in range(7):
    js(u'  tl.to("#wk2_%d", {backgroundColor: "#7A1424", borderColor: "#7A1424", duration: .12}, %.3f);'
       u' tl.to("#wk2_%d .tk", {opacity: 1, duration: .12}, %.3f);'
       % (i, t_spl + 0.12 * i, i, t_spl + 0.12 * i))
js(u'  sink("#wk2", %.3f);' % (E(u"тиждень.", 142.7) + 0.35))
g.sfx("pop", S(u"система,", 139.4) - 0.3); g.sfx("sparkle", t_spl + 0.8)

# 8 · ABOVE — CTA: consultation | done-for-you, then «+» and an arrow down -----
t_kons, t_kl, t_zav = S(u"консультація,", 145.8), S(u"під", 149.7), S(u"завтра,", 151.9)
F.append(u'''<div id="cta1" style="position:absolute; left:90px; width:900px; top:290px; display:flex; gap:24px; justify-content:center">
          <div class="card hid" id="o1" style="position:relative; width:420px"><span class="lbl">разом</span><span class="ttl">Консультація</span></div>
          <div class="card hid" id="o2" style="position:relative; width:420px"><span class="lbl">готово вже завтра</span><span class="ttl">Під ключ</span></div>
        </div>
        <div id="ctaP" class="pill hid" style="left:0; right:0; margin:auto; width:max-content; top:330px">Пиши «+» в коментарі</div>''')
t_pyshy = S(u"пиши", 157.0)
js(u'''
  rise("#o1", %.3f); rise("#o2", %.3f);
  sink("#cta1", %.3f);
  pop("#ctaP", %.3f);
  sketch("ar", "skF"); arrow("ar", 880, 420, 880, 1440, {seed: 61, bend: .05, stroke: "#7A1424", strokeWidth: 6});
  draw("ar", %.3f, .6);
''' % (t_kons - 0.25, t_kl - 0.25, E(u"завтра.", 154.1) + 0.3, t_pyshy - 0.1, t_pyshy + 0.25))
g.sfx("pop", t_kons - 0.25); g.sfx("pop", t_kl - 0.25); g.sfx("pop", t_pyshy - 0.1); g.sfx("whoosh-short", t_pyshy + 0.25)
bo(t_kons, E(u"консультація,", 145.8)); bo(S(u"разом,", 148.0), E(u"разом,", 148.0))
bo(t_kl, E(u"ключ,", 149.8)); bo(S(u"готове", 151.2), E(u"завтра,", 151.9))
bo(t_pyshy, E(u"коментарі,", 157.7))


def main():
    chunks = g.chunks(CAPS)
    doc = g.document(title=u"Reel 55 — plan with me", plate="assets/base.mp4",
                     behind="\n".join(B), panel="\n".join(P), front="\n".join(F), cover="\n".join(C),
                     js="\n".join(J), chunks=chunks, blackout=sorted(BLACKOUT), extra_css=CSS)
    g.write(HERE, doc)
    print("index.html  %d caption chunks, %d sfx cues, %d blackouts" % (len(chunks), len(g.cues), len(BLACKOUT)))


main()
