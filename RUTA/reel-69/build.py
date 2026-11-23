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
from gstyle import G, Words, load_caps  # noqa: E402

NN = "69"
DUR = float(open(os.path.join(HERE, "DUR")).read())
g = G(dur=DUR, reel=NN)
g.PANEL_TOP = 820

# whisper's token -> what she said (captions.json from tools/align.py)
FIX = {
    u"до": u"До", u"речі": u"речі!", u"то": u"ти", u"колесі.": u"колезі.", u"Збережи,": u"збережи,",
    u"кладі,": u"Claude,", u"капкад.": u"CapCut.", u"передплата,": u"передоплата,",
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
    #root .cover-bg { position: absolute; inset: 0;
                      background: radial-gradient(120% 80% at 50% 35%, #FFFFFF 0%, #F6EFEF 70%, #F1E7E7 100%); }
    .stage { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; perspective: 2200px; }
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
t_p1 = S(u"Перше", 6.40)
heading(1, 1, u"AI-монтаж", t_p1 - 0.05, S(u"Claude", 8.87) - 0.45)

f0 = S(u"Claude", 8.87) - 0.15
f1 = E(u"відео.", 14.70) + 0.15
t_skl, t_sub, t_ril = S(u"склейку,", 11.36), S(u"субтитри", 12.34), S(u"рілси", 13.72)
C.append(u"""
        <div class="cover-bg" id="bg1"></div>
        <div class="stage" id="st1">
          <div id="cc" class="win">
            <div class="cc-bar"><i></i><i></i><i></i><span>claude — ~/projects/video</span></div>
            <div class="cc-hi" style="left:26px;top:58px">
              <b>✻</b> Welcome to <strong>Claude Code</strong>!</div>
            <div class="cc-ln" style="left:26px;top:150px"><span class="cc-g">&gt;</span> /монтаж</div>
            <div class="cc-ln" style="left:26px;top:198px"><span class="cc-o">⏺</span> Skill(монтаж)</div>
            <div class="cc-ln" style="left:26px;top:240px"><span class="cc-o">⏺</span> Update Todos</div>
            <div class="cc-td" id="td1" style="left:58px;top:282px"><u>☐</u><s>чорнова склейка</s></div>
            <div class="cc-td" id="td2" style="left:58px;top:322px"><u>☐</u><s>субтитри</s></div>
            <div class="cc-td" id="td3" style="left:58px;top:362px"><u>☐</u><s>рілси з довгого відео</s></div>
            <div class="cc-in" style="left:20px;top:440px"><span class="cc-g">&gt;</span> <i class="cur"></i></div>
          </div>
        </div>""")
EXTRA += u"""
    #cc { width: 800px; height: 520px; background: #262624; color: #E8E4DE;
          font-family: "SF Mono", "DejaVu Sans Mono", Menlo, monospace; }
    .cc-bar { left: 0; top: 0; width: 800px; height: 34px; background: #1E1D1B; }
    .cc-bar i { position: absolute; top: 11px; width: 12px; height: 12px; border-radius: 50%; background: #4A4844; }
    .cc-bar i:nth-child(1) { left: 14px; } .cc-bar i:nth-child(2) { left: 34px; } .cc-bar i:nth-child(3) { left: 54px; }
    .cc-bar span { position: absolute; left: 0; right: 0; top: 8px; text-align: center; font-size: 13px; color: #8E8A84; }
    .cc-hi { width: 748px; border: 1.5px solid #D97757; border-radius: 10px; padding: 18px 20px; font-size: 19px; }
    .cc-hi b { color: #D97757; font-weight: 400; margin-right: 6px; } .cc-hi strong { font-weight: 700; }
    .cc-ln { font-size: 19px; white-space: nowrap; } .cc-g { color: #8E8A84; } .cc-o { color: #D97757; }
    .cc-td { font-size: 19px; white-space: nowrap; color: #E8E4DE; }
    .cc-td u { text-decoration: none; display: inline-block; width: 30px; color: #8E8A84; }
    .cc-td s { text-decoration: none; }
    .cc-td.on u { color: #D97757; } .cc-td.on s { color: #8E8A84; text-decoration: line-through; }
    .cc-in { width: 760px; height: 46px; border: 1.5px solid #4A4844; border-radius: 10px; padding: 10px 14px; font-size: 19px; }
    .cur { display: inline-block; width: 10px; height: 20px; background: #E8E4DE; vertical-align: -3px; }
"""


def cam(px, py, sc, ox, oy, cx=540, cy=760):
    # the window turns and scales about its own centre O: a point p of it lands
    # at O + s*(p - O) + (x, y); place p at (cx, cy)
    return (sc, round(cx - ox - sc * (px - ox), 1), round(cy - oy - sc * (py - oy), 1))


O1 = (400, 260)
W1 = cam(400, 260, 1.25, *O1)
T1 = cam(250, 325, 2.1, *O1, cx=540, cy=780)
js(u"""
  gsap.set("#cc", {transformOrigin: "400px 260px"});
  gsap.set("#cc", {x: %(wx)s, y: %(wy)s + 220, scale: %(ws)s * .86, rotationX: 24, rotationY: -20, rotationZ: 5});
  tl.to("#cc", {x: %(wx)s, y: %(wy)s, scale: %(ws)s, rotationX: 9, rotationY: -12, rotationZ: 2, duration: 1.2, ease: "power3.out"}, %(f0)s + .15);
  tl.to("#cc", {x: %(tx)s, y: %(ty)s, scale: %(ts)s, rotationX: 3, rotationY: 7, rotationZ: 0, duration: 1.2, ease: "power3.inOut"}, %(skl)s - 1.25);
  tl.set("#td1", {className: "cc-td on"}, %(skl)s);
  tl.fromTo("#td1 u", {scale: 1.6}, X({scale: 1, duration: .3, ease: "back.out(2)"}), %(skl)s);
  tl.set("#td2", {className: "cc-td on"}, %(sub)s);
  tl.fromTo("#td2 u", {scale: 1.6}, X({scale: 1, duration: .3, ease: "back.out(2)"}), %(sub)s);
  tl.set("#td3", {className: "cc-td on"}, %(ril)s);
  tl.fromTo("#td3 u", {scale: 1.6}, X({scale: 1, duration: .3, ease: "back.out(2)"}), %(ril)s);
  tl.to("#cc", {x: %(wx)s, y: %(wy)s, scale: %(ws)s, rotationX: 10, rotationY: 14, rotationZ: -2, duration: 1.0, ease: "power3.inOut"}, %(ril)s + .45);
  full(%(f0)s, %(f1)s);
""" % {"wx": W1[1], "wy": W1[2], "ws": W1[0], "tx": T1[1], "ty": T1[2], "ts": T1[0],
       "f0": "%.3f" % f0, "f1": "%.3f" % f1, "skl": "%.3f" % t_skl, "sub": "%.3f" % t_sub, "ril": "%.3f" % t_ril})
g.sfx("whoosh-short", f0); g.sfx("whoosh-short", t_skl - 1.25)
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
t_p2 = S(u"Друге", 29.97)
d0 = S(u"скіл", 35.05) - 0.2
heading(2, 2, u"бриф → сценарій і шот-лист", t_p2 - 0.05, S(u"Це", 34.30) + 0.1)
d1 = E(u"забути.", 43.20) + 0.1
t_kl, t_zy, t_tel = S(u"кладе", 37.93), S(u"зйомці", 40.64), S(u"телефона,", 42.14)
t_nich = S(u"щоб нічого", 42.60)
C.append(u"""
        <div class="stage" id="st2">
          <div id="gd" class="win">
            <div class="gd-top"><span class="gd-logo"></span>Диск<div class="gd-q">Пошук на Диску</div></div>
            <div class="gd-new">＋ Створити</div>
            <div class="gd-nav on" style="top:128px">Мій диск</div>
            <div class="gd-nav" style="top:166px">Спільні зі мною</div>
            <div class="gd-nav" style="top:204px">Нещодавні</div>
            <div class="gd-crumb">Мій диск <span>›</span> Проєкт</div>
            <div class="gd-head">Назва</div>
            <div class="gd-row" style="top:198px"><i class="doc"></i>Бриф</div>
            <div class="gd-row" style="top:246px"><i class="doc"></i>Сценарій</div>
            <div class="gd-row gd-new-row" id="gsl" style="top:294px"><i class="doc"></i>Шот-лист</div>
          </div>
          <div id="ph">
            <div class="ph-scr">
              <div class="ph-t">Шот-лист</div>
              <div class="ph-r"><span class="check" id="pc1"></span><b>Кадр 1</b><i class="line"></i></div>
              <div class="ph-r"><span class="check" id="pc2"></span><b>Кадр 2</b><i class="line"></i></div>
              <div class="ph-r"><span class="check" id="pc3"></span><b>Кадр 3</b><i class="line"></i></div>
              <div class="ph-r"><span class="check" id="pc4"></span><b>Кадр 4</b><i class="line"></i></div>
              <div class="ph-r"><span class="check" id="pc5"></span><b>Кадр 5</b><i class="line"></i></div>
            </div>
          </div>
        </div>""")
EXTRA += u"""
    #gd { width: 800px; height: 500px; background: #F8FAFD; color: #1F1F1F; }
    .gd-top { left: 0; top: 0; width: 800px; height: 64px; padding: 18px 22px; font-size: 22px; color: #444746; }
    .gd-logo { display: inline-block; width: 30px; height: 26px; margin-right: 12px; vertical-align: -5px;
               background: conic-gradient(from 30deg, #7A1424 0 120deg, #B04A58 0 240deg, #D98C96 0);
               clip-path: polygon(50% 0, 100% 86%, 0 86%); }
    .gd-q { position: absolute; left: 220px; top: 12px; width: 520px; height: 40px; border-radius: 20px;
            background: #E9EEF6; font-size: 15px; color: #5f6368; padding: 10px 20px; }
    .gd-new { left: 16px; top: 72px; width: 130px; height: 44px; border-radius: 14px; background: #fff;
              box-shadow: 0 1px 3px rgba(0,0,0,.18); font-size: 15px; font-weight: 500; padding: 12px 16px; }
    .gd-nav { left: 8px; width: 180px; height: 32px; border-radius: 16px; font-size: 14px; padding: 7px 18px; color: #1f1f1f; }
    .gd-nav.on { background: #F2DADD; font-weight: 700; }
    .gd-crumb { left: 210px; top: 80px; font-size: 22px; color: #1f1f1f; } .gd-crumb span { color: #5f6368; margin: 0 6px; }
    .gd-head { left: 210px; top: 156px; width: 570px; font-size: 13px; font-weight: 500; color: #444746;
               border-bottom: 1px solid #E1E3E1; padding-bottom: 10px; }
    .gd-row { left: 210px; width: 570px; height: 48px; font-size: 16px; padding: 14px 8px; border-bottom: 1px solid #E1E3E1;
              background: #F8FAFD; }
    .gd-row i.doc { display: inline-block; width: 16px; height: 20px; border-radius: 3px; background: #7A1424;
                    margin-right: 14px; vertical-align: -4px; }
    #ph { position: absolute; left: 330px; top: 420px; width: 420px; height: 860px; border-radius: 64px;
          background: #1F1B1B; padding: 18px; box-shadow: 0 2px 6px rgba(36,25,25,.12), 0 40px 90px rgba(36,25,25,.28);
          will-change: transform; }
    .ph-scr { width: 384px; height: 824px; border-radius: 48px; background: #fff; padding: 84px 30px; }
    .ph-t { font-size: 40px; font-weight: 700; color: #241919; margin-bottom: 34px; letter-spacing: -0.02em; }
    .ph-r { display: flex; align-items: center; gap: 14px; height: 92px; border-bottom: 2px solid #F1E7E7; }
    .ph-r b { font-size: 24px; font-weight: 500; color: #574142; white-space: nowrap; }
    .ph-r .line { flex: 1; height: 14px; }
    .ph-r .check { width: 38px; height: 38px; }
    .ph-r .check.on::after { left: 11px; top: 3px; width: 9px; height: 19px; border-width: 0 4px 4px 0; }
"""
O2 = (400, 250)
W2 = cam(400, 250, 1.3, *O2)
R2 = cam(380, 318, 2.3, *O2, cx=560, cy=760)
js(u"""
  gsap.set("#gd", {transformOrigin: "400px 250px"});
  gsap.set("#gsl", {autoAlpha: 0, y: -30});
  gsap.set("#ph", {autoAlpha: 0});
  gsap.set("#st2", {autoAlpha: 0});
  gsap.set("#ph", {transformOrigin: "50%% 50%%", scale: 1.2});
  tl.set("#st1", {autoAlpha: 0}, %(d0)s - .05);
  tl.set("#st2", {autoAlpha: 1}, %(d0)s - .05);
  gsap.set("#gd", {x: %(wx)s, y: %(wy)s + 220, scale: %(ws)s * .86, rotationX: 24, rotationY: 20, rotationZ: -5});
  tl.to("#gd", {x: %(wx)s, y: %(wy)s, scale: %(ws)s, rotationX: 9, rotationY: 12, rotationZ: -2, duration: 1.2, ease: "power3.out"}, %(d0)s + .15);
  tl.to("#gd", {x: %(rx)s, y: %(ry)s, scale: %(rs)s, rotationX: 3, rotationY: -6, rotationZ: 0, duration: 1.2, ease: "power3.inOut"}, %(kl)s - 1.0);
  tl.to("#gsl", {autoAlpha: 1, y: 0, duration: .45, ease: "back.out(1.6)", immediateRender: false}, %(kl)s);
  tl.fromTo("#gsl", {backgroundColor: "#F8FAFD"}, X({backgroundColor: "#F2DADD", duration: .3}), %(kl)s + .1);
  tl.to("#gd", {x: %(wx)s - 260, y: %(wy)s - 120, scale: %(ws)s * .7, rotationY: 24, autoAlpha: 0, duration: .9, ease: "power3.inOut"}, %(zy)s - .3);
  tl.fromTo("#ph", {autoAlpha: 0, y: 700, rotationX: 28, rotationY: -16}, X({autoAlpha: 1, y: 0, rotationX: 6, rotationY: -8, duration: 1.0, ease: "power3.out"}), %(zy)s - .2);
  tl.to("#ph", {rotationX: 2, rotationY: 4, duration: 2.2, ease: "sine.inOut"}, %(zy)s + .8);
  tl.set("#pc1", {className: "check on"}, %(n1)s);
  tl.set("#pc2", {className: "check on"}, %(n2)s);
  tl.set("#pc3", {className: "check on"}, %(n3)s);
  full(%(d0)s, %(d1)s);
""" % {"wx": W2[1], "wy": W2[2], "ws": W2[0], "rx": R2[1], "ry": R2[2], "rs": R2[0],
       "d0": "%.3f" % d0, "d1": "%.3f" % d1, "kl": "%.3f" % t_kl, "zy": "%.3f" % t_zy,
       "n1": "%.3f" % (t_nich), "n2": "%.3f" % (t_nich + 0.3), "n3": "%.3f" % (t_nich + 0.6)})
g.sfx("whoosh-short", d0); g.sfx("whoosh-short", t_kl - 1.0); g.sfx("pop", t_kl)
g.sfx("whoosh-short", t_zy - 0.3); g.sfx("click-soft", t_nich); g.sfx("click-soft", t_nich + 0.3)
g.sfx("click-soft", t_nich + 0.6); g.sfx("whoosh-short", d1)

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
  sketch("c1", "skP"); box("c1", 90, 320, 230, 110, {seed: 21}); label("c1", 205, 390, "камера 1", {size: 42});
  box("c1", 90, 560, 230, 110, {seed: 23}); label("c1", 205, 630, "камера 2", {size: 42});
  draw("c1", %.3f, .4);
  sketch("c2", "skP"); arrow("c2", 330, 380, 420, 470, {seed: 25, bend: .1}); arrow("c2", 330, 615, 420, 530, {seed: 27, bend: -.1});
  box("c2", 430, 440, 260, 120, {seed: 29, fill: true}); label("c2", 560, 512, "Claude Code", {size: 42});
  label("c2", 560, 615, "скрипт", {size: 44});
  draw("c2", %.3f, .4);
  sketch("c3", "skP"); arrow("c3", 700, 500, 790, 500, {seed: 31}); box("c3", 800, 440, 190, 120, {seed: 33});
  label("c3", 895, 512, "LUT", {size: 58});
  draw("c3", %.3f, .4);
  sketch("c4", "skP"); label("c4", 870, 640, "як одна камера", {size: 44, stroke: "#7A1424", fill: "#7A1424"});
  draw("c4", %.3f);
  erase("c1", %.3f); erase("c2", %.3f); erase("c3", %.3f); erase("c4", %.3f);
''' % (h0 + 0.5, t_kad + 0.2, t_lut - 0.6, t_odn - 0.2, h1, h1, h1, h1))
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
