# -*- coding: utf-8 -*-
"""Reel 60 — «Скільки ти насправді платиш за монтаж за місяць?» (монтаж з Клодом).
Batch 2026-11-20 (raw 20261120_134134). STYLE.md §00 + her review of reel 61
(2026-11-23): natural editing, one meaningful moment per sentence group, her
punch-ins carry the rest. Skeleton and idioms copied from reel-61/build.py.
The ТЕСТ CTA is cut out (work/r60/cut-fix.json): the reel ends on her.

The one object: the 5-hour limit bar. It comes back three times — five reels
fill it on $20, only three long reels fill it, and on €100 it barely moves.
Only numbers she says: $20, 5 годин, 5 рілсів, 2-3 хв, 5-6 хв, 3 рілси,
€100, 10-15.

Beats: behind «Claude» (cover) -> meme 12 on «непередбачувана» -> HALF 1 the scheme: two equal tasks, very
different token bars -> FULL 1 the Claude limit window: $20, zoom into the
5-hour bar, five reels fill it -> shuffle: експертні відео / з суфлера /
2-3 хвилини -> meme 35 «більше, ніж пʼять» -> shuffle: 5-6 хвилин / багато вставок / помилки
-> FULL 2 the same window, three reels fill the bar -> glass card: «Оптимізація
токенів» switches on -> HALF 2 the scheme: шаблон анімації -> рілс, «з нуля»
struck -> glass pill «Claude · €100» -> behind «10–15» -> glass limit card: the
bar is a sliver, barely moves -> ends on her.

usage: python3 build.py   (then: RUTA/BUILD-BRIEF.md steps 6-10)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
from gstyle import G, Words, load_caps, mark  # noqa: E402

NN = "60"
DUR = 68.550           # (2057 plate frames - 0.5) / 30
g = G(dur=DUR, reel=NN)
g.cta_start = DUR - 2.0   # no CTA line left (ТЕСТ is cut); her rule for this reel: memes off the last 2 s
g.PANEL_TOP = 820      # panel captions: bottom 938, her pushed hair below

FIX = {
    u"досправлі": u"насправді", u"часу,": u"чесно,", u"то переховати": u"то порахувати",
    u"юзич": u"юсадж",
    u"дідати": u"витрачати", u"абсолютну": u"абсолютно", u"стокенів.": u"токенів.",
    u"в 5": u"пʼять", u"RealSafe.": u"рілсів.", (u"якщо", 26.3): u"Якщо",
    (u"б", 30.4): None, (u"дві", 30.9): u"дві-три", (u"три", 31.1): None, u"хвилини": u"хвилини,",
    u"більше.": u"більше,", u"п'ять.": u"пʼять.",
    (u"тоді", 38.5): u"Тоді", u"сьогодні!": u"десь", u"Туреріал": u"три", u"СИЗ": u"рілси",
    (u"5", 40.3): u"пʼятигодинний", u"годинний": None,
    u"Коли": u"коли", u"клієнкам,": u"клієнткам,", u"токенів,": u"токенів.",
    u"нуля.": u"нуля,", (u"І", 56.5): u"і", u"може": u"можна",
    u"євро,": u"євро.", (u"я", 62.6): u"Я", u"витрачалось": u"витрачалось.",
}
CAPS = load_caps(NN, FIX)
W = Words(CAPS)
S, E = W.s, W.e

B, P, F, C, J = [], [], [], [], []
BLACKOUT, PLACE, HALF = [], [], []


def js(s):
    J.append(s)


P.append(u'<svg class="sk" id="skP" data-layout-allow-occlusion width="1080" height="1240" viewBox="0 0 1080 1240"></svg>')

EXTRA = u'''
    .gcard { left: 0; right: 0; margin: auto; width: 720px; top: 320px; padding: 28px 34px; }
    .gcard .hd { display: flex; align-items: center; gap: 14px; font-size: 28px; font-weight: 500;
                 color: #574142; margin-bottom: 18px; }
    .gcard .hd svg path { fill: #7A1424; }
    .tgl { display: flex; align-items: center; gap: 20px; font-size: 44px; font-weight: 500; color: #241919; }
    .tgl span { flex: 1; }
    .sw { width: 96px; height: 54px; border-radius: 27px; background: #C9C1C1; position: relative; flex: none; }
    .sw i { position: absolute; left: 6px; top: 6px; width: 42px; height: 42px; border-radius: 50%;
            background: #fff; box-shadow: 0 1px 3px rgba(0,0,0,.25); }
    .gbar { height: 34px; border-radius: 17px; background: rgba(122,20,36,.12); overflow: hidden; }
    .gbar i { display: block; height: 100%; width: 0; border-radius: 17px; background: #7A1424; }
    .eur { left: 0; right: 0; margin: auto; width: max-content; top: 330px; padding: 22px 40px;
           display: flex; align-items: center; gap: 18px; font-size: 48px; font-weight: 700; color: #241919;
           border-radius: 999px; }
    .eur svg path { fill: #7A1424; }
    .eur b { color: #7A1424; }
    /* as reel-57: the plain white card in the shuffle slot, a size up */
    .shuf .chip { font-size: 48px; padding: 18px 34px; }
'''

# 1 · BEHIND — «Claude» (the cover frame: the hook word that attracts) -------------
t_kl = S(u"з клодом", 2.25)
B.append(u'        <div id="bw1" class="big hid" data-layout-allow-occlusion style="top:440px; font-size:230px">Claude</div>')
e_bw1 = E(u"місяць?", 2.93) + 0.25
g.matte("b1", 0.0, round(e_bw1 + 0.5, 3))
js(u'  rise("#bw1", 0.05); sink("#bw1", %.3f);' % e_bw1)
g.sfx("whoosh-short", 0.05)
BLACKOUT.append((t_kl - 0.03, E(u"з клодом", 2.25)))

# 2 · HALF 1 — the scheme: two equal tasks, very different token bars ---------------
k0 = S(u"навіть", 13.07) - 0.1
k1 = E(u"токенів.", 18.36) + 0.25
HALF.append((k0, k1))
t_dvi, t_odn, t_zad = S(u"дві", 13.48), S(u"однакові", 13.90), S(u"задачі", 14.48)
t_abs, t_rizn, t_kilk = S(u"абсолютно", 16.66), S(u"різну", 17.52), S(u"кількість", 17.94)
js(u'''
  sketch("a1", "skP"); box("a1", 90, 330, 360, 140, {seed: 3}); label("a1", 270, 418, "задача", {size: 56});
  draw("a1", %.3f);
  sketch("a2", "skP"); ln("a2", 500, 385, 580, 385, {seed: 5, strokeWidth: 6}); ln("a2", 500, 415, 580, 415, {seed: 6, strokeWidth: 6});
  draw("a2", %.3f, .35);
  sketch("a3", "skP"); box("a3", 630, 330, 360, 140, {seed: 7}); label("a3", 810, 418, "задача", {size: 56});
  draw("a3", %.3f);
  sketch("a4", "skP"); box("a4", 90, 560, 110, 90, {seed: 9, fill: true, r: 20});
  draw("a4", %.3f);
  sketch("a5", "skP"); box("a5", 630, 560, 360, 90, {seed: 11, fill: true, r: 20});
  draw("a5", %.3f, .9);
  sketch("a6", "skP"); label("a6", 540, 740, "токени", {size: 54, color: "#7A1424"});
  draw("a6", %.3f);
  erase("a1", %.3f); erase("a2", %.3f); erase("a3", %.3f); erase("a4", %.3f); erase("a5", %.3f); erase("a6", %.3f);
''' % (t_dvi - 0.2, t_odn, t_zad - 0.25, t_abs, t_rizn - 0.1, t_kilk, k1, k1, k1, k1, k1, k1))
g.sfx("whoosh-short", k0); g.sfx("click-soft", t_odn); g.sfx("click-soft", t_rizn)

# 3 · FULL 1 + 2 — the Claude limit window as a platform-ad sequence ---------------
# No screenshot of her Claude limits in app-screenshots/, so a clean product
# window with only what she says: Claude, $20, the 5-hour limit, the reels.
# No percentages, no made-up usage numbers.
f0 = S(u"На", 20.13) - 0.15
f1 = E(u"рілсів.", 25.71) + 0.15
t_20, t_5h, t_zmon, t_5r = S(u"20", 21.20), S(u"пʼятигодинний", 22.50), S(u"змонтуєш", 24.85), S(u"пʼять", 25.43)
g0 = S(u"Тоді", 38.47) - 0.2
g1 = E(u"ліміт.", 40.85) + 0.1
t_tri, t_5h2 = S(u"три", 39.11), S(u"пʼятигодинний", 40.27)
REEL = u'<i class="rl"><svg viewBox="0 0 24 24" width="40" height="40"><path d="M8 5v14l11-7z" fill="#fff"/></svg></i>'
SEGA = u"".join(u'<div class="sg" id="sa%d">%s</div>' % (i, REEL) for i in range(5))
SEGB = u"".join(u'<div class="sg" id="sb%d">%s</div>' % (i, REEL) for i in range(3))
C.append(u"""
        <div id="stage">
          <div id="win">
            <div class="cw-top">%(mk)s<span>Claude</span></div>
            <div class="cw-plan" id="plan"><span class="cw-l">Підписка</span><b>$20</b><span class="cw-m">/ місяць</span></div>
            <div class="cw-lim">
              <div class="cw-l2">Ліміт · 5 годин</div>
              <div class="cw-bar"><div class="segs" id="segA">%(a)s</div><div class="segs" id="segB">%(b)s</div></div>
              <div class="cw-n"><span id="nA">5 рілсів</span><span id="nB">3 рілси</span></div>
            </div>
          </div>
        </div>""" % {"mk": mark("claude", 54), "a": SEGA, "b": SEGB})
EXTRA += u"""
    #cover { background: radial-gradient(120% 80% at 50% 35%, #FFFFFF 0%, #F6EFEF 70%, #F1E7E7 100%); }
    #stage { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; perspective: 2200px; }
    #win { position: absolute; left: 0; top: 0; width: 840px; height: 600px; background: #fff;
           border-radius: 22px; font-family: "Google Sans", sans-serif; color: #1f1f1f;
           box-shadow: 0 2px 6px rgba(36,25,25,.10), 0 30px 80px rgba(36,25,25,.22);
           transform-origin: 0 0; will-change: transform; padding: 36px 42px; }
    .cw-top { display: flex; align-items: center; gap: 14px; font-size: 42px; font-weight: 700; }
    .cw-top svg path { fill: #7A1424; }
    .cw-plan { margin-top: 28px; display: flex; align-items: baseline; gap: 14px; padding: 18px 22px;
               border: 2px solid #ECE6E6; border-radius: 16px; }
    .cw-l { font-size: 32px; color: #574142; flex: 1; }
    .cw-plan b { font-size: 66px; color: #241919; letter-spacing: -0.02em; }
    .cw-m { font-size: 28px; color: #574142; }
    .cw-lim { margin-top: 26px; padding: 20px 22px; background: #FBF6F6; border-radius: 16px; }
    .cw-l2 { font-size: 36px; font-weight: 700; color: #241919; margin-bottom: 16px; }
    .cw-bar { position: relative; height: 92px; border-radius: 14px; background: #EFE3E3; overflow: hidden; }
    .segs { position: absolute; inset: 4px; display: flex; gap: 4px; }
    .sg { flex: 1; border-radius: 10px; background: #7A1424; transform-origin: 0 50%; transform: scaleX(0);
          display: flex; align-items: center; justify-content: center; }
    .rl { display: block; line-height: 0; }
    .cw-n { position: relative; height: 54px; margin-top: 14px; font-size: 42px; font-weight: 700; color: #7A1424; }
    .cw-n span { position: absolute; left: 0; top: 0; opacity: 0; }
"""
# camera: the window turns and scales about its centre (380, 260); a point p of
# it lands at O + s*(p - O) + (x, y). Wide = whole window; BAR = the limit block.
def cam(px, py, sc, cx=540, cy=830):
    return (round(cx - 420 - sc * (px - 420), 1), round(cy - 300 - sc * (py - 300), 1))
WIDE = (1.08,) + cam(420, 300, 1.08)
PLAN = (1.22,) + cam(420, 200, 1.22)
BAR = (1.26,) + cam(420, 420, 1.26)
seg_a = u"\n".join(u'  tl.to("#sa%d", {scaleX: 1, duration: .25, ease: "power2.out"}, %.3f);' % (i, t_zmon + 0.12 * i + 0.15) for i in range(5))
seg_b = u"\n".join(u'  tl.to("#sb%d", {scaleX: 1, duration: .35, ease: "power2.out"}, %.3f);' % (i, t_tri + 0.22 * i) for i in range(3))
js(u"""
  gsap.set("#win", {transformOrigin: "420px 300px"});
  gsap.set("#segB, #nB", {autoAlpha: 0});
  gsap.set("#win", {x: %(wx)s, y: %(wy)s + 220, scale: %(ws)s * .86, rotationX: 24, rotationY: -20, rotationZ: 5});
  tl.to("#win", {x: %(px)s, y: %(py)s, scale: %(ps)s, rotationX: 8, rotationY: -10, rotationZ: 2, duration: 1.2, ease: "power3.out"}, %(f0)s + .15);
  tl.fromTo("#plan", {borderColor: "#ECE6E6"}, X({borderColor: "#7A1424", duration: .25}), %(t20)s);
  tl.to("#win", {x: %(bx)s, y: %(by)s, scale: %(bs)s, rotationX: 3, rotationY: 7, rotationZ: 0, duration: 1.2, ease: "power3.inOut"}, %(t5h)s - .45);
%(sega)s
  tl.to("#nA", {opacity: 1, duration: .3}, %(t5r)s);
  full(%(f0)s, %(f1)s);
  // between the two: the bar empties, three wider slots instead of five
  tl.set("#segA, #nA", {autoAlpha: 0}, %(mid)s); tl.set("#segB, #nB", {autoAlpha: 1}, %(mid)s);
  tl.set("#nB", {opacity: 0}, %(mid)s);
  tl.set("#win", {x: %(bx)s, y: %(by)s + 200, scale: %(bs)s * .88, rotationX: -18, rotationY: 16, rotationZ: -3}, %(mid)s);
  tl.to("#win", {x: %(bx)s, y: %(by)s, scale: %(bs)s, rotationX: -3, rotationY: -6, rotationZ: 0, duration: 1.1, ease: "power3.out"}, %(g0)s + .15);
%(segb)s
  tl.to("#nB", {opacity: 1, duration: .3}, %(t5h2)s - .4);
  tl.to("#win", {x: %(wx)s, y: %(wy)s, scale: %(ws)s, rotationX: 8, rotationY: 10, rotationZ: -1, duration: 1.0, ease: "power3.inOut"}, %(t5h2)s);
  full(%(g0)s, %(g1)s);
""" % {"wx": WIDE[1], "wy": WIDE[2], "ws": WIDE[0], "px": PLAN[1], "py": PLAN[2], "ps": PLAN[0],
       "bx": BAR[1], "by": BAR[2], "bs": BAR[0], "f0": "%.3f" % f0, "f1": "%.3f" % f1,
       "g0": "%.3f" % g0, "g1": "%.3f" % g1, "t20": "%.3f" % t_20, "t5h": "%.3f" % t_5h,
       "t5r": "%.3f" % t_5r, "t5h2": "%.3f" % t_5h2, "mid": "%.3f" % ((f1 + g0) / 2),
       "sega": seg_a, "segb": seg_b})
g.sfx("whoosh-short", f0); g.sfx("click-soft", t_20); g.sfx("whoosh-short", t_5h - 0.45)
g.sfx("pop", t_zmon + 0.15); g.sfx("whoosh-short", f1)
g.sfx("whoosh-short", g0); g.sfx("pop", t_tri); g.sfx("whoosh-short", g1)

# 4 · SHUFFLE — what kind of video gets five, what kind gets three -----------------
L1 = [(u"експертні відео", S(u"експертні", 27.19)), (u"з суфлера", S(u"з суфлера,", 29.37)),
      (u"2–3 хвилини", S(u"дві-три", 30.92))]   # «більше, ніж пʼять» is the meme's beat, not a chip
L2 = [(u"5–6 хвилин", S(u"5-6,", 35.60)), (u"багато вставок", S(u"багато", 36.42)),
      (u"помилки", S(u"помилок.", 37.82))]
for tag, lst, end in (("p", L1, S(u"більше,", 32.92) - 0.1), ("q", L2, g0)):
    for i, (txt, t) in enumerate(lst):
        F.append(u'        <div id="%s%d" class="shuf hid"><span class="chip"><i></i>%s</span></div>' % (tag, i, txt))
        g.sfx("pop", t - 0.1)
    js(u'  shuffle([%s], [%s], %.3f);' % (", ".join('"#%s%d"' % (tag, i) for i in range(len(lst))),
                                         ", ".join("%.3f" % (t - 0.1) for _, t in lst), end))

# 5 · ABOVE — glass card: token optimisation switches on ---------------------------
t_nal, t_opt, t_nap = S(u"налаштовую", 46.58), S(u"оптимізую", 49.64), S(u"Наприклад,", 51.61)
F.append(u'''
        <div id="opt" class="glass gcard hid">
          <div class="hd">%s Система монтажу</div>
          <div class="tgl"><span>Оптимізація токенів</span><div class="sw" id="osw"><i></i></div></div>
        </div>''' % mark("claude", 30))
js(u'''
  rise("#opt", %.3f);
  tl.to("#osw", {backgroundColor: "#7A1424", duration: .2}, %.3f);
  tl.to("#osw i", {x: 42, duration: .3, ease: "back.out(2)"}, %.3f);
  sink("#opt", %.3f);
''' % (t_nal - 0.2, t_opt, t_opt, t_nap - 0.45))
g.sfx("pop", t_nal - 0.2); g.sfx("click", t_opt)

# 6 · HALF 2 — the scheme: a template goes straight into the reel -----------------
h0 = t_nap - 0.1
h1 = E(u"вставити.", 58.05) + 0.3
HALF.append((h0, h1))
t_shab, t_zn, t_vz = S(u"шаблони", 52.55), S(u"нуля,", 56.13), S(u"взяти", 57.57)
t_kozh = S(u"кожен", 55.09)
js(u'''
  sketch("c1", "skP"); box("c1", 90, 330, 420, 150, {seed: 21, fill: true}); label("c1", 300, 424, "шаблон анімації", {size: 46});
  draw("c1", %.3f);
  sketch("c2", "skP"); box("c2", 630, 330, 340, 150, {seed: 23}); label("c2", 800, 424, "з нуля", {size: 54});
  draw("c2", %.3f);
  sketch("c3", "skP"); ln("c3", 650, 350, 950, 460, {stroke: "#7A1424", strokeWidth: 7, seed: 25});
  ln("c3", 650, 460, 950, 350, {stroke: "#7A1424", strokeWidth: 7, seed: 27});
  draw("c3", %.3f, .3);
  sketch("c4", "skP"); arrow("c4", 300, 500, 470, 660, {seed: 29, bend: .2});
  box("c4", 490, 600, 300, 140, {seed: 31}); label("c4", 640, 690, "рілс", {size: 58});
  draw("c4", %.3f);
  erase("c1", %.3f); erase("c2", %.3f); erase("c3", %.3f); erase("c4", %.3f);
''' % (t_shab - 0.15, t_kozh - 0.1, t_zn - 0.05, S(u"просто", 57.07) - 0.3, h1, h1, h1, h1))
g.sfx("whoosh-short", h0); g.sfx("click", t_zn); g.sfx("click-soft", t_vz)

# 7 · ABOVE — glass pill «Claude · €100» ---------------------------------------------
t_kld, t_100, t_ya = S(u"Клод", 61.12), S(u"100", 61.76), S(u"Я", 62.59)
F.append(u'        <div id="eur" class="glass eur hid">%s Claude · <b>€100</b></div>' % mark("claude", 44))
js(u'  pop("#eur", %.3f); sink("#eur", %.3f);' % (t_kld - 0.1, t_ya - 0.05))
g.sfx("pop", t_kld - 0.1); g.sfx("kaching", t_100)
BLACKOUT.append((t_kld - 0.03, E(u"євро.", 62.02)))

# 8 · BEHIND — «10–15» ------------------------------------------------------------------
t_1015, e_raz = S(u"10-15", 63.91), E(u"раз", 65.34)
B.append(u'        <div id="bw2" class="big hid" data-layout-allow-occlusion style="top:420px; font-size:250px">10–15</div>')
g.matte("b2", round(t_1015 - 0.6, 3), round(e_raz - t_1015 + 1.1, 3))
js(u'  rise("#bw2", %.3f); sink("#bw2", %.3f);' % (t_1015 - 0.35, e_raz + 0.2))
g.sfx("whoosh-short", t_1015 - 0.35)
BLACKOUT.append((t_1015 - 0.03, E(u"10-15", 63.91)))

# 9 · ABOVE — the limit bar again: a sliver that barely moves; then just her -------
t_ne = S(u"не", 66.47)
F.append(u'''
        <div id="lim" class="glass gcard hid" style="top:330px">
          <div class="hd">%s Ліміт · 5 годин</div>
          <div class="gbar"><i id="sliv"></i></div>
        </div>''' % mark("claude", 30))
js(u'''
  rise("#lim", %.3f);
  tl.fromTo("#sliv", {width: "2%%"}, X({width: "4%%", duration: 1.4, ease: "power1.inOut"}), %.3f);
  sink("#lim", %.3f);
''' % (t_ne - 0.35, t_ne + 0.3, DUR - 0.45))
g.sfx("pop", t_ne - 0.35)

# 10 · MEMES — comic relief (assets/memes/MEMES.md), slapped on above her head ---------
# 12 hamster praying: «юсадж це штука непередбачувана» — you can't know, you hope.
# 35 hamster in sunglasses: «тоді можна навіть і більше, ніж пʼять» — the win.
g.meme(F, J, "12", round(E(u"непередбачувана,", 7.93) + 0.1, 3), dur=1.2, slot="top")
g.meme(F, J, "35", round(E(u"пʼять.", 33.48) + 0.1, 3), dur=1.2, slot="top")

# ---------------------------------------------------------------- half screens + their mattes
for i, (a, b) in enumerate(HALF):
    g.matte("h%d" % (i + 1), round(a - 0.1, 3), round(b - a + 1.2, 3))
    js("  half(%.3f, %.3f);" % (a, b))
    PLACE.append((a + 0.4, b + 0.2, "bottom", 938))


def main():
    chunks = g.chunks(CAPS, place=PLACE)
    doc = g.document(title=u"Reel 60 — скільки коштує монтаж з Клодом", plate="assets/base.mp4",
                     behind="\n".join(B), panel="\n".join(P), front="\n".join(F), cover="\n".join(C),
                     js="\n".join(J), chunks=chunks, blackout=BLACKOUT, extra_css=EXTRA)
    g.write(HERE, doc)
    print("index.html  %d caption chunks, %d sfx cues, %d mattes" % (len(chunks), len(g.cues), len(g.mattes)))


if __name__ == "__main__":
    main()
