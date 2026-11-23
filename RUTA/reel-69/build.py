# -*- coding: utf-8 -*-
"""Reel 69 — «Які автоматизації зробити відеографці?». Batch 2026-11-20
(raw 20261120_140030). STYLE.md §00 + her review of reel 61 (2026-11-23):
natural editing, few graphics, reel-61's skeleton and idioms.

A list reel. The numbered heading of each item rises through one slot over her
head (shuffle), and each item gets ONE real moment:

  behind «Claude» (the cover) -> 1 AI-монтаж: FULL 1 Claude Code as a 3D
  window, the skill's todo list ticks on «склейку / субтитри / рілси» -> behind
  «CapCut» -> HALF 1 the scheme Claude (нарізав) -> CapCut (доредагувати) ->
  2 бриф: FULL 2 the project folder in Google Drive, «Шот-лист» lands on
  «кладе», then the same shot list opened on a phone -> 3 фінплан: the cost
  categories shuffle through the slot (words only, no figures), a glass card
  «збережено в Google Drive» -> 4 колір: HALF 2 the scheme two cameras ->
  Claude Code (скрипт) -> LUT -> як одна камера -> CTA pill in the subtitle
  band «Збережи і перешли колезі».

usage: python3 build.py   (then: sfx mix, mattes, check, render — see the brief)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
from gstyle import G, Words, load_caps, mark  # noqa: E402

NN = "69"
DUR = float(open(os.path.join(HERE, "DUR")).read())
g = G(dur=DUR, reel=NN)
g.PANEL_TOP = 820

# whisper's token -> what she said (captions.json from tools/align.py)
FIX = {
    u"до": u"До", u"речі": u"речі!", u"то": u"ти", u"колесі.": u"колезі.", u"Збережи,": u"збережи,",
    u"кладі,": u"Claude,", u"капкад.": u"CapCut.", u"передплата,": u"передоплата,", u"щось": u"його",
}
CAPS = load_caps(NN, FIX)

# spans where the aligner merged or shifted her words: rebuilt from words.json
# timings (what she said, re-heard with a solo whisper pass on the plate)
REPL = [
    (1.30, 3.53, [(u"в тредс:", 1.39), (u"які", 1.85), (u"автоматизації", 2.27), (u"з Claude", 3.09)]),
    (6.30, 9.50, [(u"Перше", 6.40), (u"—", None), (u"це", 6.96), (u"звичайний", 7.10), (u"AI-монтаж.", 7.78),
                  (u"Claude", 8.87), (u"Code", 9.28)]),
    (20.30, 21.60, [(u"Claude", 20.39), (u"і", 20.87), (u"CapCut,", 21.22)]),
    (33.00, 35.90, [(u"і", 33.04), (u"шот-лист.", 33.44), (u"Це", 34.30), (u"має", 34.57), (u"бути", 34.73),
                    (u"скіл", 35.05), (u"у Claude,", 35.55)]),
    (46.60, 47.60, [(u"кошторис:", 46.66)]),
    (60.10, 60.50, [(u"Claude", 60.14), (u"Code", 60.30)]),
    (67.50, 68.00, [(u"кольорокорекція.", 67.53)]),
]


def apply_repl(caps, repl):
    out = list(caps)
    for a, b, toks in repl:
        out = [c for c in out if not (a <= c["s"] < b)]
        for w, s in toks:
            if s is None:
                continue
            out.append({"w": w, "s": s, "e": s + 0.3})
    out.sort(key=lambda c: c["s"])
    for x, y in zip(out, out[1:]):
        x["e"] = round(max(x["s"] + 0.10, min(x["e"], y["s"] - 0.02)), 3)
    return out


CAPS = apply_repl(CAPS, REPL)
W = Words(CAPS)
S, E = W.s, W.e
g.cta_start = S(u"Тому", 68.37)      # the CTA line («Тому збережи…») — no meme from here

B, P, F, C, J = [], [], [], [], []
BLACKOUT, PLACE, HALF = [], [], []


def js(s):
    J.append(s)


P.append(u'<svg class="sk" id="skP" data-layout-allow-occlusion width="1080" height="1240" viewBox="0 0 1080 1240"></svg>')

EXTRA = u'''
    /* the running list: a numbered heading through the shuffle slot */
    .shuf .chip { font-size: 42px; }
    .shuf .chip b { display: inline-flex; align-items: center; justify-content: center; width: 56px; height: 56px;
                    border-radius: 50%; background: #7A1424; color: #fff; font-size: 32px; font-weight: 700;
                    margin-left: -8px; }
    .shuf.cat .chip { font-size: 46px; padding: 18px 34px; }
    #cover { background: radial-gradient(120% 80% at 50% 35%, #FFFFFF 0%, #F6EFEF 70%, #F1E7E7 100%); }
    .stage { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; perspective: 2400px; }
    .win { position: absolute; left: 0; top: 0; border-radius: 14px; font-family: "Google Sans", sans-serif;
           box-shadow: 0 2px 6px rgba(36,25,25,.10), 0 30px 80px rgba(36,25,25,.22);
           transform-origin: 0 0; will-change: transform; overflow: hidden; }
    .win > div { position: absolute; }
'''

# ---------------------------------------------------------------- 1 · BEHIND «Claude» (cover)
e_cl = E(u"з Claude", 3.09)
B.append(u'        <div id="bw1" class="big hid" data-layout-allow-occlusion style="top:470px; font-size:230px">Claude</div>')
g.matte("b1", 0.0, round(e_cl + 0.7, 3))
js(u'  rise("#bw1", 0.10); sink("#bw1", %.3f);' % (e_cl + 0.25))
g.sfx("whoosh-short", 0.10)
BLACKOUT.append((S(u"з Claude", 3.09) - 0.03, e_cl))

# ---------------------------------------------------------------- the running list: headings
HEAD = []      # (id, html, t_in, t_out)


def heading(i, n, txt, t_in, t_out):
    F.append(u'        <div id="hd%d" class="shuf hid"><span class="chip"><b>%d</b>%s</span></div>' % (i, n, txt))
    HEAD.append(("#hd%d" % i, t_in, t_out))
    g.sfx("pop", t_in)


def slot_in(sel, t):
    js(u'  tl.fromTo("%s", {autoAlpha: 0, y: 90, scale: .92, rotationX: -35}, X({autoAlpha: 1, y: 0, scale: 1, rotationX: 0, duration: .55, ease: "back.out(1.4)"}), %.3f);' % (sel, t))


def slot_out(sel, t):
    js(u'  tl.to("%s", {autoAlpha: 0, y: -80, scale: .92, rotationX: 35, duration: .4, ease: "power2.in"}, %.3f);' % (sel, t))


# ---------------------------------------------------------------- 2 · item 1 + FULL 1 Claude Code
# Platform-ad sequence (reel-64 sizing): the terminal is 980 x 1000 at scale 1 on
# the wide view (91 % of the frame width, y 330-1330, clear of the caption band);
# body text 34-38 px, labels >= 26 px. «Skill(монтаж)» appears on «скіл», the
# todos on «робить», each ticks on its word; the camera zooms into the todos.
t_p1 = S(u"Перше", 6.40)
heading(1, 1, u"AI-монтаж", t_p1 - 0.05, S(u"Claude", 8.87) - 0.45)

f0 = S(u"Claude", 8.87) - 0.15
f1 = E(u"відео.", 14.70) + 0.15
t_skil, t_rob = S(u"скіл", 9.78), S(u"робить", 10.50)
t_skl, t_sub, t_ril = S(u"склейку,", 11.36), S(u"субтитри", 12.34), S(u"рілси", 13.72)
C.append(u"""
        <div class="stage" id="st1">
          <div id="cc" class="win">
            <div class="cc-bar"><i></i><i></i><i></i><span>claude — ~/projects/video</span></div>
            <div class="cc-hi" style="left:36px;top:92px">
              <div><b>✻</b> Welcome to <strong>Claude Code</strong>!</div>
              <div class="cc-dim">/help for help, /status for your current setup</div>
              <div class="cc-dim">cwd: ~/projects/video</div></div>
            <div class="cc-ln" style="left:40px;top:340px"><span class="cc-g">&gt;</span> /монтаж</div>
            <div class="cc-ln" id="cs1" style="left:40px;top:418px"><span class="cc-o">⏺</span> Skill(монтаж)</div>
            <div class="cc-ln" id="cs2" style="left:40px;top:496px"><span class="cc-o">⏺</span> Update Todos</div>
            <div class="cc-td" id="td1" style="left:92px;top:568px"><u>☐</u><s>чорнова склейка</s></div>
            <div class="cc-td" id="td2" style="left:92px;top:640px"><u>☐</u><s>субтитри</s></div>
            <div class="cc-td" id="td3" style="left:92px;top:712px"><u>☐</u><s>рілси з довгого відео</s></div>
            <div class="cc-in" style="left:36px;top:840px"><span class="cc-g">&gt;</span> <i class="cur"></i></div>
            <div class="cc-hint" style="left:52px;top:944px">? for shortcuts</div>
          </div>
        </div>""")
EXTRA += u"""
    #cc { width: 980px; height: 1000px; background: #262624; color: #E8E4DE; border-radius: 24px;
          font-family: "DejaVu Sans Mono", Menlo, monospace; }
    .cc-bar { left: 0; top: 0; width: 980px; height: 60px; background: #1E1D1B; }
    .cc-bar i { position: absolute; top: 21px; width: 18px; height: 18px; border-radius: 50%; background: #4A4844; }
    .cc-bar i:nth-child(1) { left: 24px; } .cc-bar i:nth-child(2) { left: 52px; } .cc-bar i:nth-child(3) { left: 80px; }
    .cc-bar span { position: absolute; left: 0; right: 0; top: 14px; text-align: center; font-size: 26px; color: #9A958E;
                   font-family: "Google Sans", sans-serif; }
    .cc-hi { width: 908px; border: 2px solid #D97757; border-radius: 16px; padding: 26px 28px; font-size: 34px; }
    .cc-hi b { color: #D97757; font-weight: 400; margin-right: 8px; } .cc-hi strong { font-weight: 700; }
    .cc-hi > div { line-height: 1.2; }
    .cc-hi > div + div { margin-top: 14px; }
    .cc-dim { font-size: 26px; color: #9A958E; }
    .cc-ln { font-size: 36px; white-space: nowrap; } .cc-g { color: #9A958E; } .cc-o { color: #D97757; }
    .cc-td { font-size: 36px; white-space: nowrap; color: #E8E4DE; }
    .cc-td u { text-decoration: none; display: inline-block; width: 56px; color: #9A958E; }
    .cc-td s { text-decoration: none; }
    .cc-td.on u { color: #D97757; } .cc-td.on s { color: #9A958E; text-decoration: line-through; }
    .cc-in { width: 908px; height: 84px; border: 2px solid #4A4844; border-radius: 16px; padding: 18px 24px; font-size: 36px; }
    .cc-hint { font-size: 26px; color: #9A958E; }
    .cur { display: inline-block; width: 18px; height: 38px; background: #E8E4DE; vertical-align: -6px; }
"""


def cam(px, py, sc, w, h, cx=540, cy=830):
    # the window scales about its own centre O = (w/2, h/2): a point p lands at
    # O + s*(p - O) + (x, y); put p at (cx, cy)
    ox, oy = w / 2.0, h / 2.0
    return (sc, round(cx - ox - sc * (px - ox), 1), round(cy - oy - sc * (py - oy), 1))


W1 = cam(490, 500, 1.0, 980, 1000)                    # wide: y 330-1330
T1 = cam(330, 640, 1.55, 980, 1000, cx=540, cy=830)    # the todos
js(u"""
  gsap.set("#cc", {transformOrigin: "490px 500px"});
  gsap.set(["#cs1", "#cs2", "#td1", "#td2", "#td3"], {autoAlpha: 0});
  gsap.set("#cc", {x: %(wx)s, y: %(wy)s + 240, scale: %(ws)s * .86, rotationX: 24, rotationY: -18, rotationZ: 4});
  tl.to("#cc", {x: %(wx)s, y: %(wy)s, scale: %(ws)s, rotationX: 6, rotationY: -8, rotationZ: 1, duration: 1.2, ease: "power3.out"}, %(f0)s + .1);
  tl.fromTo("#cs1", {autoAlpha: 0, x: -20}, X({autoAlpha: 1, x: 0, duration: .3}), %(skil)s);
  tl.fromTo(["#cs2", "#td1", "#td2", "#td3"], {autoAlpha: 0, y: 14}, X({autoAlpha: 1, y: 0, duration: .3, stagger: .08}), %(rob)s);
  tl.to("#cc", {x: %(tx)s, y: %(ty)s, scale: %(ts)s, rotationX: 3, rotationY: 6, rotationZ: 0, duration: 1.1, ease: "power3.inOut"}, %(skl)s - 1.0);
  tl.set("#td1", {className: "cc-td on"}, %(skl)s);
  tl.fromTo("#td1 u", {scale: 1.6}, X({scale: 1, duration: .3, ease: "back.out(2)"}), %(skl)s);
  tl.set("#td2", {className: "cc-td on"}, %(sub)s);
  tl.fromTo("#td2 u", {scale: 1.6}, X({scale: 1, duration: .3, ease: "back.out(2)"}), %(sub)s);
  tl.set("#td3", {className: "cc-td on"}, %(ril)s);
  tl.fromTo("#td3 u", {scale: 1.6}, X({scale: 1, duration: .3, ease: "back.out(2)"}), %(ril)s);
  tl.to("#cc", {x: %(wx)s, y: %(wy)s, scale: %(ws)s, rotationX: 7, rotationY: 10, rotationZ: -1, duration: .8, ease: "power3.inOut"}, %(ril)s + .35);
  full(%(f0)s, %(f1)s);
""" % {"wx": W1[1], "wy": W1[2], "ws": W1[0], "tx": T1[1], "ty": T1[2], "ts": T1[0],
       "f0": "%.3f" % f0, "f1": "%.3f" % f1, "skil": "%.3f" % t_skil, "rob": "%.3f" % t_rob,
       "skl": "%.3f" % t_skl, "sub": "%.3f" % t_sub, "ril": "%.3f" % t_ril})
g.sfx("whoosh-short", f0); g.sfx("click-soft", t_skil); g.sfx("whoosh-short", t_skl - 1.0)
g.sfx("click", t_skl); g.sfx("click", t_sub); g.sfx("click", t_ril); g.sfx("whoosh-short", f1)
# ---------------------------------------------------------------- MEME 01 «ЦИТЬ» after «Я про це рідко кажу,»
# a clear stretch: FULL 1 is gone, «CapCut» rises at 20.3
g.meme(F, J, "01", round(E(u"кажу,", 16.97) + 0.1, 3), dur=1.2, slot="r")

# ---------------------------------------------------------------- 3 · BEHIND «CapCut» -> HALF 1 Claude -> CapCut
t_cc, e_cc = S(u"CapCut,", 21.22), E(u"CapCut,", 21.22)
B.append(u'        <div id="bw2" class="big hid" data-layout-allow-occlusion style="top:470px; font-size:230px">CapCut</div>')
js(u'  rise("#bw2", %.3f); sink("#bw2", %.3f);' % (S(u"Claude", 20.39) - 0.1, e_cc + 0.25))
g.sfx("whoosh-short", S(u"Claude", 20.39) - 0.1)
BLACKOUT.append((S(u"Claude", 20.39) - 0.03, e_cc))

k0 = e_cc + 0.35
k1 = E(u"CapCut.", 26.63) + 0.35
HALF.append((k0, k1))
t_nar, t_dor = S(u"нарізав", 22.94), S(u"доредагувати", 25.51)
js(u'''
  sketch("a1", "skP"); box("a1", 110, 400, 330, 140, {seed: 3, fill: true});
  label("a1", 275, 486, "Claude", {size: 62});
  label("a1", 275, 640, "нарізав", {size: 50});
  draw("a1", %.3f);
  sketch("a2", "skP"); arrow("a2", 460, 470, 630, 470, {seed: 5, bend: -.12});
  box("a2", 650, 400, 330, 140, {seed: 7}); label("a2", 815, 486, "CapCut", {size: 62});
  label("a2", 815, 640, "доредагувати", {size: 50});
  draw("a2", %.3f);
  erase("a1", %.3f); erase("a2", %.3f);
''' % (t_nar - 0.4, t_nar + 0.8, k1, k1))
g.sfx("whoosh-short", k0); g.sfx("click-soft", t_nar); g.sfx("click-soft", t_dor)
g.matte("h1", round(S(u"Claude", 20.39) - 0.4, 3), round(k1 + 1.2 - (S(u"Claude", 20.39) - 0.4), 3))
PLACE.append((k0 + 0.4, k1 + 0.2, "bottom", 938))
js("  half(%.3f, %.3f);" % (k0, k1))

# ---------------------------------------------------------------- 4 · item 2 + FULL 2 Google Drive -> phone
# Drive: 980 x 740 at scale 1 (y 460-1200), text >= 30 px; «Шот-лист» lands in
# the project folder on «кладе» (camera zoomed onto the file list). On «зйомці»
# Drive flies off and a phone (600 x 1080, y 310-1390) brings the same shot list;
# rows tick on «щоб нічого не забути».
t_p2 = S(u"Друге", 29.97)
d0 = S(u"скіл", 35.05) - 0.2
heading(2, 2, u"бриф → сценарій і шот-лист", t_p2 - 0.05, S(u"Це", 34.30) + 0.1)
d1 = E(u"забути.", 43.20) + 0.1
t_gdr, t_kl, t_zy = S(u"Google", 36.89), S(u"кладе", 37.93), S(u"зйомці", 40.64)
t_nich = S(u"щоб нічого", 42.60)
ROWS = u"".join(u'<div class="ph-r"><span class="check" id="pc%d"></span><b>Кадр %d</b><i class="line"></i></div>' % (i, i)
                for i in range(1, 7))
C.append(u"""
        <div class="stage" id="st2">
          <div id="gd" class="win">
            <div class="gd-top"><span class="gd-logo">%(drive)s</span>Диск<div class="gd-q">Пошук на Диску</div></div>
            <div class="gd-new">＋ Створити</div>
            <div class="gd-nav on" style="top:236px">Мій диск</div>
            <div class="gd-nav" style="top:306px">Спільні зі мною</div>
            <div class="gd-nav" style="top:376px">Нещодавні</div>
            <div class="gd-crumb">Мій диск <span>›</span> Проєкт</div>
            <div class="gd-head">Назва</div>
            <div class="gd-row" style="top:290px"><i class="doc"></i>Бриф</div>
            <div class="gd-row" style="top:400px"><i class="doc"></i>Сценарій</div>
            <div class="gd-row" id="gsl" style="top:510px"><i class="doc"></i>Шот-лист</div>
          </div>
          <div id="ph">
            <div class="ph-scr">
              <div class="ph-t">Шот-лист</div>
              <div class="ph-s">%(drive2)s Проєкт</div>
              %(rows)s
            </div>
          </div>
        </div>""" % {"drive": mark("googledrive", 44), "drive2": mark("googledrive", 30), "rows": ROWS})
EXTRA += u"""
    #gd { width: 980px; height: 740px; background: #F8FAFD; color: #1F1F1F; border-radius: 28px; }
    .gd-top { left: 0; top: 0; width: 980px; height: 104px; padding: 28px 30px; font-size: 38px; color: #444746;
              display: flex; align-items: center; gap: 14px; }
    .gd-logo .mark { color: #7A1424; }
    .gd-q { position: absolute; left: 260px; top: 20px; width: 690px; height: 64px; border-radius: 32px;
            background: #E9EEF6; font-size: 30px; color: #5f6368; padding: 14px 32px; }
    .gd-new { left: 24px; top: 128px; height: 78px; border-radius: 22px; background: #fff;
              box-shadow: 0 1px 3px rgba(0,0,0,.18); font-size: 30px; font-weight: 500; padding: 20px 28px; }
    .gd-nav { left: 12px; width: 280px; height: 58px; border-radius: 29px; font-size: 30px; padding: 11px 26px;
              color: #1f1f1f; white-space: nowrap; }
    .gd-nav.on { background: #F2DADD; font-weight: 700; }
    .gd-crumb { left: 330px; top: 136px; font-size: 40px; color: #1f1f1f; } .gd-crumb span { color: #5f6368; margin: 0 8px; }
    .gd-head { left: 330px; top: 222px; width: 620px; font-size: 26px; font-weight: 500; color: #444746;
               border-bottom: 2px solid #E1E3E1; padding-bottom: 16px; }
    .gd-row { left: 330px; width: 620px; height: 110px; font-size: 36px; padding: 32px 14px; border-bottom: 2px solid #E1E3E1;
              background: #F8FAFD; }
    .gd-row i.doc { display: inline-block; width: 30px; height: 38px; border-radius: 5px; background: #7A1424;
                    margin-right: 24px; vertical-align: -6px; }
    #ph { position: absolute; left: 240px; top: 310px; width: 600px; height: 1080px; border-radius: 80px;
          background: #1F1B1B; padding: 20px; box-shadow: 0 2px 6px rgba(36,25,25,.12), 0 40px 90px rgba(36,25,25,.28);
          will-change: transform; }
    .ph-scr { width: 560px; height: 1040px; border-radius: 62px; background: #fff; padding: 96px 44px 0; }
    .ph-t { font-size: 58px; font-weight: 700; color: #241919; letter-spacing: -0.02em; }
    .ph-s { display: flex; align-items: center; gap: 12px; font-size: 30px; color: #574142; margin: 10px 0 26px; }
    .ph-s .mark { color: #7A1424; }
    .ph-r { display: flex; align-items: center; gap: 22px; height: 118px; border-bottom: 2px solid #F1E7E7; }
    .ph-r b { font-size: 38px; font-weight: 500; color: #241919; white-space: nowrap; }
    .ph-r .line { flex: 1; height: 18px; }
    .ph-r .check { width: 52px; height: 52px; }
    .ph-r .check.on::after { left: 15px; top: 5px; width: 12px; height: 25px; border-width: 0 5px 5px 0; }
"""
W2 = cam(490, 370, 1.0, 980, 740)                    # wide: y 460-1200
R2 = cam(640, 420, 1.4, 980, 740, cx=540, cy=820)    # the file list
js(u"""
  gsap.set("#gd", {transformOrigin: "490px 370px"});
  gsap.set("#gsl", {autoAlpha: 0, y: -30});
  gsap.set("#st2", {autoAlpha: 0});
  gsap.set("#ph", {autoAlpha: 0, transformOrigin: "50%% 50%%"});
  tl.set("#st1", {autoAlpha: 0}, %(d0)s - .05);
  tl.set("#st2", {autoAlpha: 1}, %(d0)s - .05);
  gsap.set("#gd", {x: %(wx)s, y: %(wy)s + 240, scale: %(ws)s * .86, rotationX: 24, rotationY: 18, rotationZ: -4});
  tl.to("#gd", {x: %(wx)s, y: %(wy)s, scale: %(ws)s, rotationX: 6, rotationY: 8, rotationZ: -1, duration: 1.2, ease: "power3.out"}, %(d0)s + .1);
  tl.to("#gd", {x: %(rx)s, y: %(ry)s, scale: %(rs)s, rotationX: 3, rotationY: -5, rotationZ: 0, duration: 1.1, ease: "power3.inOut"}, %(kl)s - 1.15);
  tl.to("#gsl", {autoAlpha: 1, y: 0, duration: .45, ease: "back.out(1.6)", immediateRender: false}, %(kl)s);
  tl.fromTo("#gsl", {backgroundColor: "#F8FAFD"}, X({backgroundColor: "#F2DADD", duration: .3}), %(kl)s + .1);
  tl.to("#gd", {x: %(wx)s - 300, y: %(wy)s - 160, scale: %(ws)s * .7, rotationY: 24, autoAlpha: 0, duration: .8, ease: "power3.inOut"}, %(zy)s - .3);
  tl.fromTo("#ph", {autoAlpha: 0, y: 800, rotationX: 26, rotationY: -14, scale: 1}, X({autoAlpha: 1, y: 0, rotationX: 5, rotationY: -7, duration: 1.0, ease: "power3.out"}), %(zy)s - .2);
  tl.to("#ph", {rotationX: 2, rotationY: 5, scale: 1.04, duration: 2.0, ease: "sine.inOut"}, %(zy)s + .8);
  tl.set("#pc1", {className: "check on"}, %(n1)s);
  tl.set("#pc2", {className: "check on"}, %(n2)s);
  tl.set("#pc3", {className: "check on"}, %(n3)s);
  tl.set("#pc4", {className: "check on"}, %(n4)s);
  full(%(d0)s, %(d1)s);
""" % {"wx": W2[1], "wy": W2[2], "ws": W2[0], "rx": R2[1], "ry": R2[2], "rs": R2[0],
       "d0": "%.3f" % d0, "d1": "%.3f" % d1, "kl": "%.3f" % t_kl, "zy": "%.3f" % t_zy,
       "n1": "%.3f" % t_nich, "n2": "%.3f" % (t_nich + 0.22), "n3": "%.3f" % (t_nich + 0.44),
       "n4": "%.3f" % (t_nich + 0.66)})
g.sfx("whoosh-short", d0); g.sfx("whoosh-short", t_kl - 1.15); g.sfx("pop", t_kl)
g.sfx("whoosh-short", t_zy - 0.3); g.sfx("click-soft", t_nich); g.sfx("click-soft", t_nich + 0.22)
g.sfx("click-soft", t_nich + 0.44); g.sfx("click-soft", t_nich + 0.66); g.sfx("whoosh-short", d1)
# ---------------------------------------------------------------- 5 · item 3: фінплан, the cost categories through the slot
t_p3 = S(u"Третє", 43.63)
CAT = [(u"техніка", S(u"техніка,", 47.67)), (u"дорога", S(u"дорога,", 48.37)),
       (u"асистент", S(u"асистент,", 48.83)), (u"передоплата", S(u"передоплата,", 49.87)),
       (u"податок ФОП", S(u"податок", 50.47)), (u"скільки лишається тобі", S(u"скільки", 51.35))]
heading(3, 3, u"фінплан на проєкт", t_p3 - 0.05, CAT[0][1] - 0.1)
for i, (txt, t) in enumerate(CAT):
    F.append(u'        <div id="ct%d" class="shuf cat hid"><span class="chip">%s</span></div>' % (i, txt))
    g.sfx("click-soft" if i else "pop", t)
t_zb, t_gd = S(u"зберігає", 53.55), S(u"Google", 55.55)
t_ruky = E(u"руки,", 52.89)
for i, (txt, t) in enumerate(CAT):
    slot_in("#ct%d" % i, t - 0.1)
    slot_out("#ct%d" % i, (CAT[i + 1][1] - 0.1 if i + 1 < len(CAT) else t_ruky - 0.35) - 0.05)
# MEME 14 (shocked cat) on «скільки реально залишається тобі на руки» — the reveal
g.meme(F, J, "14", round(t_ruky + 0.1, 3), dur=1.1, slot="r")
t_tab = S(u"таблицю,", 54.39)

F.append(u'''
        <div id="sv" class="glass hid" style="left:0; right:0; margin:auto; width:max-content; top:320px; padding:26px 34px;
             display:flex; align-items:center; gap:22px">
          <span class="svic">%s</span>
          <div><div class="svt">Фінплан</div><div class="svs">збережено в Google Drive</div></div>
          <span class="svok"></span>
        </div>''' % "")
EXTRA += u"""
    .svic { width: 64px; height: 64px; border-radius: 16px; background: #7A1424; position: relative; flex: none; }
    .svic::before { content: ""; position: absolute; left: 14px; top: 16px; width: 36px; height: 32px;
                    background: linear-gradient(#fff 0 0) 0 0/100% 3px no-repeat,
                                linear-gradient(#fff 0 0) 0 14px/100% 3px no-repeat,
                                linear-gradient(#fff 0 0) 0 29px/100% 3px no-repeat,
                                linear-gradient(#fff 0 0) 0 0/3px 100% no-repeat,
                                linear-gradient(#fff 0 0) 16px 0/3px 100% no-repeat,
                                linear-gradient(#fff 0 0) 33px 0/3px 100% no-repeat; }
    .svt { font-size: 40px; font-weight: 700; color: #241919; letter-spacing: -0.02em; }
    .svs { font-size: 30px; font-weight: 500; color: #574142; margin-top: 4px; }
    .svok { width: 52px; height: 52px; border-radius: 50%; background: #7A1424; position: relative; flex: none; margin-left: 8px; }
    .svok::after { content: ""; position: absolute; left: 18px; top: 9px; width: 12px; height: 24px;
                   border: solid #fff; border-width: 0 5px 5px 0; transform: rotate(45deg); }
"""
t_p4 = S(u"Четверте", 56.37)
js(u'  rise("#sv", %.3f); pop("#sv .svok", %.3f); sink("#sv", %.3f);' % (t_tab - 0.05, t_gd, t_p4 - 0.45))
g.sfx("pop", t_tab - 0.05); g.sfx("ping", t_gd)

# ---------------------------------------------------------------- 6 · item 4 + HALF 2 the LUT scheme
heading(4, 4, u"однаковий колір з різних камер", t_p4 - 0.05, S(u"Кидаєш", 59.53) - 0.2)
h0 = S(u"Кидаєш", 59.53) - 0.15
h1 = E(u"камерою.", 66.53) + 0.3
HALF.append((h0, h1))
t_kad, t_pyshe, t_lut, t_odn = S(u"кадри", 60.56), S(u"пише", 61.80), S(u"LUT,", 63.18), S(u"однією", 66.22)
js(u'''
  sketch("c1", "skP"); box("c1", 430, 440, 260, 120, {seed: 29, fill: true}); label("c1", 560, 512, "Claude Code", {size: 42});
  draw("c1", %.3f, .4);
  sketch("c2", "skP"); box("c2", 90, 320, 230, 110, {seed: 21}); label("c2", 205, 390, "камера 1", {size: 42});
  box("c2", 90, 560, 230, 110, {seed: 23}); label("c2", 205, 630, "камера 2", {size: 42});
  arrow("c2", 330, 380, 420, 470, {seed: 25, bend: .1}); arrow("c2", 330, 615, 420, 530, {seed: 27, bend: -.1});
  draw("c2", %.3f, .35);
  sketch("c3", "skP"); label("c3", 560, 615, "скрипт", {size: 44});
  draw("c3", %.3f);
  sketch("c4", "skP"); arrow("c4", 700, 500, 790, 500, {seed: 31}); box("c4", 800, 440, 190, 120, {seed: 33});
  label("c4", 895, 512, "LUT", {size: 58});
  draw("c4", %.3f, .35);
  sketch("c5", "skP"); label("c5", 870, 640, "як одна камера", {size: 44, stroke: "#7A1424", fill: "#7A1424"});
  draw("c5", %.3f);
  erase("c1", %.3f); erase("c2", %.3f); erase("c3", %.3f); erase("c4", %.3f); erase("c5", %.3f);
''' % (h0 + 0.75, t_kad - 0.05, t_pyshe - 0.1, t_lut - 0.8, t_odn - 0.2, h1, h1, h1, h1, h1))
g.sfx("whoosh-short", h0); g.sfx("click-soft", t_kad); g.sfx("click-soft", t_pyshe); g.sfx("click", t_lut)
g.matte("h2", round(h0 - 0.1, 3), round(h1 - h0 + 1.2, 3))
PLACE.append((h0 + 0.4, h1 + 0.2, "bottom", 938))
js("  half(%.3f, %.3f);" % (h0, h1))

# ---------------------------------------------------------------- headings into the slot
for sel, a, b in HEAD:
    slot_in(sel, a)
    slot_out(sel, b)

# ---------------------------------------------------------------- 7 · CTA pill in the subtitle band
t_zber = S(u"збережи,", 68.72)
F.append(u'''        <div id="ctp" class="pill hid" style="left:0; right:0; margin:auto; width:max-content; top:1404px;
             font-size:46px; padding:28px 56px">Збережи і перешли колезі</div>''')
js(u'  pop("#ctp", %.3f);' % (t_zber - 0.1))
g.sfx("pop", t_zber)
BLACKOUT.append((t_zber - 0.05, DUR))


def main():
    chunks = g.chunks(CAPS, place=PLACE)
    doc = g.document(title=u"Reel 69 — автоматизації для відеографки", plate="assets/base.mp4",
                     behind="\n".join(B), panel="\n".join(P), front="\n".join(F), cover="\n".join(C),
                     js="\n".join(J), chunks=chunks, blackout=BLACKOUT, extra_css=EXTRA)
    g.write(HERE, doc)
    print("index.html  %d caption chunks, %d sfx cues, %d mattes" % (len(chunks), len(g.cues), len(g.mattes)))
    if "--words" in sys.argv:
        print(" ".join("%s/%.2f" % (c["w"], c["s"]) for c in CAPS))


main()
