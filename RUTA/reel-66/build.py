# -*- coding: utf-8 -*-
"""Reel 66 — «Як АІ змонтує рілс як твої референси, а не «як у всіх»?».
Batch 2026-11-20 (raw 20261120_135523). STYLE.md §00 + her review of reel 61
(2026-11-23): natural editing, one meaningful moment per sentence group.
The ТЕСТ CTA is cut out (work/r66/cut-fix.json); the reel ends on her.

Chain: behind «Claude» -> glass chat: «Змонтуй відео» -> a default-style reply
-> HALF: two reels, two looks (мої / клієнтки) -> «референс -> Claude, зроби як
тут» struck -> FULL 1: dozens of identical reels (her own frame) in a tilted
wall -> shuffle checklist (тексти / елементи / вставки й меми) -> FULL 2: the
media library as a platform-ad sequence (access on, pick the best, rename one,
add to the library) -> glass card: tuning the style is the long bar, the launch
the short one -> behind «твій стиль» -> she ends clean.

usage: python3 build.py   (then: sh work/b1021/mattes.sh 66; python3 tools/sfx.py mix 66)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
from gstyle import G, Words, load_caps, mark  # noqa: E402

NN = "66"
DUR = float(open(os.path.join(HERE, "DUR")).read()) if os.path.exists(os.path.join(HERE, "DUR")) else 60.316
g = G(dur=DUR, reel=NN)
g.PANEL_TOP = 820      # panel captions: bottom 938, her pushed hair at ≈ 980

FIX = {
    u"змонтується": u"«змонтуй", u"відео.": u"відео»,",
    u"кожену": u"кожну", (u"І", 44.8): u"і",
    u"Налаштувати": u"налаштувати", u"монтажу": u"монтажу.",
    u"вона": u"а", (u"до", 59.2): u"не", u"полно": u"повно-", u"значить": u"значить,", u"суті": u"суті,",
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
    .dm { left: 150px; top: 300px; width: 780px; padding: 24px 28px; }
    .bub { display: inline-block; border-radius: 26px; padding: 16px 26px; font-size: 36px;
           font-weight: 500; line-height: 1.25; }
    .bub.in { background: rgba(255,255,255,.94); color: #241919; border-bottom-left-radius: 8px; }
    .bub.me { background: #7A1424; color: #fff; border-bottom-right-radius: 8px; }
    .rowr { display: flex; justify-content: flex-end; }
    .rowl { display: flex; align-items: flex-end; gap: 14px; margin-top: 16px; }
    .av { width: 54px; height: 54px; border-radius: 50%; background: #fff; color: #D97757;
          display: flex; align-items: center; justify-content: center; flex: none;
          box-shadow: 0 1px 3px rgba(36,25,25,.12); }
    .rep { display: flex; align-items: center; gap: 18px; }
    .vt { width: 50px; height: 80px; border-radius: 10px; flex: none;
          background: linear-gradient(160deg, #E9DADA, #C9B4B5); position: relative; }
    .vt::after { content: ""; position: absolute; left: 19px; top: 30px; border-style: solid;
                 border-width: 10px 0 10px 16px; border-color: transparent transparent transparent #fff; }

    /* the long bar and the short one */
    .bars { left: 150px; top: 300px; width: 780px; padding: 30px 34px; }
    .bars .r { display: flex; align-items: center; gap: 22px; height: 64px; }
    .bars .r + .r { margin-top: 14px; }
    .bars .l { width: 330px; white-space: nowrap; font-size: 32px; font-weight: 500; color: #241919; flex: none; }
    .bars .tr { flex: 1; height: 26px; border-radius: 13px; background: rgba(122,20,36,.10); position: relative; overflow: hidden; }
    .bars .tr i { position: absolute; left: 0; right: 0; top: 0; bottom: 0; border-radius: 13px; background: #7A1424;
                  transform-origin: 0 50%; transform: scaleX(0); }

    /* checklist through the shuffle slot */
    .shuf .chip .cb { width: 42px; height: 42px; border-radius: 11px; border: 3px solid #DEBFBF;
                      background: #fff; position: relative; flex: none; }
    .shuf .chip .cb b { position: absolute; left: -3px; top: -3px; width: 42px; height: 42px; border-radius: 11px;
                        background: #7A1424; opacity: 0; }
    .shuf .chip .cb b::after { content: ""; position: absolute; left: 14px; top: 6px; width: 10px; height: 20px;
                               border: solid #fff; border-width: 0 5px 5px 0; transform: rotate(45deg); }
'''

# 1 · BEHIND — «Claude» (the cover frame) ----------------------------------------
t_kl, e_kl = S(u"Клоду", 1.15), E(u"Клоду", 1.15)
B.append(u'        <div id="bw1" class="big hid" data-layout-allow-occlusion style="top:450px; font-size:220px">Claude</div>')
g.matte("b1", 0.0, 2.95)
js(u'  rise("#bw1", 0.05); sink("#bw1", %.3f);' % (E(u"відео»,", 2.31) + 0.05))
g.sfx("whoosh-short", 0.05)
BLACKOUT.append((t_kl - 0.03, e_kl))

# 2 · ABOVE — a glass chat: «Змонтуй відео» -> the default reply ----------------
t_to, t_def, t_kld, t_ale = S(u"то", 2.73), S(u"дефолту,", 3.85), S(u"клодівському", 5.81), S(u"Але", 7.10)
F.append(u'''
        <div id="c1" class="glass dm hid">
          <div class="rowr"><span class="bub me">Змонтуй відео</span></div>
          <div class="rowl hid" id="c1a"><span class="av">%s</span>
            <span class="bub in rep"><i class="vt"></i>Готово · стиль за замовчуванням</span></div>
        </div>''' % mark("claude", 34))
js(u'''
  rise("#c1", %.3f);
  pop("#c1a", %.3f);
  sink("#c1", %.3f);
''' % (t_to - 0.05, t_def - 0.05, t_ale - 0.25))
g.sfx("pop", t_to - 0.05); g.sfx("notification", t_def - 0.05)

# 3 · HALF — two reels, two looks; then «референс -> Claude» struck --------------
h0 = t_ale - 0.1
h1 = S(u"Я", 16.47) - 0.05
HALF.append((h0, h1))
t_moi, t_kli, t_ref, t_zrob, t_tut = S(u"мої", 8.01), S(u"клієнтки", 10.78), S(u"референси", 14.54), S(u"«зроби", 15.50), S(u"тут».", 16.00)
t_riz = S(u"різниця", 12.68)
js(u'''
  sketch("p1", "skP"); box("p1", 170, 300, 260, 430, {seed: 3});
  ln("p1", 215, 380, 385, 380, {seed: 4, strokeWidth: 14, stroke: "#7A1424"});
  ell("p1", 300, 540, 120, 120, {seed: 5, fill: false});
  box("p1", 210, 640, 180, 46, {seed: 6, r: 14, fill: true});
  label("p1", 300, 790, "мої", {size: 52});
  draw("p1", %.3f, .45);
  sketch("p2", "skP"); box("p2", 650, 300, 260, 430, {seed: 7});
  box("p2", 670, 320, 220, 190, {seed: 8, r: 18, fill: true});
  ell("p2", 780, 610, 100, 100, {seed: 9, fill: false});
  ln("p2", 690, 680, 870, 680, {seed: 10}); ln("p2", 720, 708, 840, 708, {seed: 11});
  label("p2", 780, 790, "клієнтки", {size: 52});
  draw("p2", %.3f, .45);
  erase("p1", %.3f); erase("p2", %.3f);
  sketch("r1", "skP"); box("r1", 80, 400, 320, 140, {seed: 21, fill: true});
  label("r1", 240, 485, "референс", {size: 50});
  arrow("r1", 410, 470, 660, 470, {seed: 22, bend: .12});
  box("r1", 670, 400, 320, 140, {seed: 23}); label("r1", 830, 485, "Claude", {size: 54});
  draw("r1", %.3f, .5);
  sketch("r2", "skP"); label("r2", 540, 640, "«зроби як тут»", {size: 54});
  draw("r2", %.3f);
  sketch("r3", "skP"); ln("r3", 340, 650, 740, 610, {stroke: "#7A1424", strokeWidth: 8, seed: 27});
  draw("r3", %.3f, .3);
  erase("r1", %.3f); erase("r2", %.3f); erase("r3", %.3f);
''' % (t_moi - 0.15, t_kli - 0.2, t_riz - 0.2, t_riz - 0.2, t_ref - 0.35, t_zrob - 0.1,
       t_tut - 0.15, h1, h1, h1))
g.sfx("whoosh-short", h0); g.sfx("click-soft", t_moi); g.sfx("click-soft", t_kli)
g.sfx("click-soft", t_ref); g.sfx("click", t_tut)

# 4 · FULL 1 — dozens of the same reel ---------------------------------------
a0 = S(u"переглянути", 25.17) - 0.45
a1 = E(u"рілсів.", 28.55) + 0.3
t_des, t_odn = S(u"десятки", 26.23), S(u"однакових", 27.97)
cards = []
for r in range(7):
    for c in range(5):
        cards.append(u'<div class="rc"><img src="assets/thumb.jpg"><i></i><u></u></div>')
C.append(u'''
        <div id="wall" class="hid"><div id="grid">%s</div></div>''' % u"".join(cards))
EXTRA += u"""
    #cover { background: radial-gradient(120% 80% at 50% 35%, #FFFFFF 0%, #F6EFEF 70%, #F1E7E7 100%); overflow: hidden; }
    #wall { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; perspective: 2000px; }
    #grid { position: absolute; left: 42px; top: -230px; width: 996px; display: grid;
            grid-template-columns: repeat(5, 180px); gap: 24px; transform-origin: 50% 50%; }
    .rc { width: 180px; height: 320px; border-radius: 18px; overflow: hidden; position: relative; background: #ddd;
          box-shadow: 0 2px 6px rgba(36,25,25,.12), 0 14px 30px rgba(36,25,25,.16); }
    .rc img { width: 180px; height: 320px; object-fit: cover; display: block; }
    .rc i { position: absolute; left: 64px; top: 130px; border-style: solid; border-width: 26px 0 26px 44px;
            border-color: transparent transparent transparent rgba(255,255,255,.92); }
    #wall::after { content: ""; position: absolute; left: 0; right: 0; top: 1180px; height: 740px;
                   background: linear-gradient(to bottom, rgba(246,239,239,0), rgba(246,239,239,.92) 32%, #F4ECEC 100%); }
    .rc u { position: absolute; left: 0; top: 0; right: 0; bottom: 0; border-radius: 18px;
            box-shadow: inset 0 0 0 6px #7A1424; opacity: 0; }
"""
js(u'''
  tl.set("#wall", {autoAlpha: 1}, %(a0)s);
  gsap.set("#grid", {rotationX: 34, rotationZ: -14, rotationY: 8, scale: 1.05, y: 160});
  tl.fromTo("#grid .rc", {autoAlpha: 0, scale: .7, y: 60}, X({autoAlpha: 1, scale: 1, y: 0, duration: .45, ease: "back.out(1.5)",
            stagger: {each: .045, from: "start"}}), %(a0)s + .25);
  tl.fromTo("#grid", {y: 160}, X({y: -420, rotationZ: -8, scale: 1.12, duration: %(span)s, ease: "sine.inOut"}), %(a0)s + .2);
  tl.to("#grid .rc u", {opacity: 1, duration: .25, stagger: {each: .012, from: "center"}}, %(odn)s);
  tl.set("#wall", {autoAlpha: 0}, %(a1)s + .9);
  full(%(a0)s, %(a1)s);
''' % {"a0": "%.3f" % a0, "a1": "%.3f" % a1, "span": "%.3f" % (a1 - a0 + 0.6), "odn": "%.3f" % (t_odn - 0.05)})
g.sfx("whoosh-short", a0); g.sfx("click", t_odn); g.sfx("whoosh-short", a1)

# 5 · ABOVE — the checklist, through the shuffle slot -------------------------
CK = [(u"тексти відображаються правильно", S(u"тексти", 30.20) - 0.1),
      (u"елементи як на референсі", S(u"елементи", 32.14) - 0.1),
      (u"вставки й меми", S(u"вставки", 35.26) - 0.1)]
ck_end = S(u"і,", 36.34) + 0.05
for i, (txt, t) in enumerate(CK):
    F.append(u'        <div id="ck%d" class="shuf hid"><span class="chip"><i class="cb"><b></b></i>%s</span></div>' % (i, txt))
js(u'  shuffle(["#ck0", "#ck1", "#ck2"], [%s], %.3f);' % (", ".join("%.3f" % t for _, t in CK), ck_end))
for i, (txt, t) in enumerate(CK):
    js(u'  tl.fromTo("#ck%d .cb b", {opacity: 0, scale: .5}, X({opacity: 1, scale: 1, duration: .35, ease: POP}), %.3f);' % (i, t + 0.5))
    g.sfx("pop", t); g.sfx("click-soft", t + 0.5)

# 6 · FULL 2 — the media library, a platform-ad sequence ----------------------
u0 = S(u"налаштувати", 36.85) - 0.4
u1 = E(u"систему.", 46.14) + 0.1
t_dost, t_kart = S(u"доступ", 37.75), S(u"картинок", 38.95)
t_prod, t_vidb, t_kozh, t_naz = S(u"продивляюсь", 41.26), S(u"відбираю", 42.58), S(u"кожну", 43.82), S(u"називаю", 44.18)
t_dod, t_sys = S(u"додаю", 45.12), S(u"окрему", 45.72)
# 12 tiles, 4 x 3; tiles 0, 5, 10 get picked; tile 5 is renamed
COLS = [u"#E8D3D4", u"#D9C7C8", u"#F0E3E3", u"#CDB6B8", u"#E2CFCF", u"#D4BEBF"]
tiles = []
for k in range(12):
    r, c = divmod(k, 4)
    x, y = 200 + c * 146, 64 + r * 140
    tiles.append(u'<div class="tl" id="tl%d" style="left:%dpx;top:%dpx"><div class="im" style="background:%s"><s></s><em></em>'
                 u'<b class="ok"></b></div><div class="nm"><span class="n0">IMG_%d.png</span>%s</div></div>'
                 % (k, x, y, COLS[k % len(COLS)], 2041 + k,
                    u'<span class="n1">реакція-вау.png<i class="car"></i></span>' if k == 5 else u""))
C.append(u'''
        <div id="stage" class="hid">
          <div id="win">
            <div class="mt-bar"><i></i><i></i><i></i><span>Медіа для монтажу</span>
              <div class="mt-acc">Доступ для Claude<em id="acc"><u></u></em></div></div>
            <div class="mt-side">
              <div class="si">Усі файли</div><div class="si">Картинки</div><div class="si">Меми</div>
              <div class="si" id="lib">Бібліотека стилю<b id="libn">3</b></div>
            </div>
            %s
          </div>
        </div>''' % u"\n            ".join(tiles))
EXTRA += u"""
    #stage { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; perspective: 2200px; }
    #win { position: absolute; left: 0; top: 0; width: 800px; height: 520px; background: #fff;
           border-radius: 16px; font-family: "Google Sans", sans-serif; color: #1f1f1f; overflow: hidden;
           box-shadow: 0 2px 6px rgba(36,25,25,.10), 0 30px 80px rgba(36,25,25,.22);
           transform-origin: 400px 260px; will-change: transform; }
    .mt-bar { position: absolute; left: 0; top: 0; width: 800px; height: 46px; border-bottom: 1px solid #EEE6E6;
              display: flex; align-items: center; padding: 0 16px; gap: 7px; font-size: 15px; font-weight: 500; }
    .mt-bar > i { width: 11px; height: 11px; border-radius: 50%; background: #E3D5D5; display: block; }
    .mt-bar > span { margin-left: 14px; }
    .mt-acc { margin-left: auto; display: flex; align-items: center; gap: 10px; font-size: 13px; color: #574142; }
    .mt-acc em { width: 34px; height: 18px; border-radius: 9px; background: #C9C1C1; position: relative; display: block; }
    .mt-acc em u { position: absolute; left: 2px; top: 2px; width: 14px; height: 14px; border-radius: 50%;
                   background: #fff; box-shadow: 0 1px 2px rgba(0,0,0,.25); }
    .mt-side { position: absolute; left: 0; top: 46px; width: 184px; height: 474px; background: #FBF7F7;
               border-right: 1px solid #EEE6E6; padding: 14px 10px; }
    .si { height: 34px; line-height: 34px; padding: 0 12px; border-radius: 17px; font-size: 13px; color: #3c3434;
          margin-bottom: 6px; position: relative; }
    .si b { position: absolute; right: 10px; top: 8px; height: 18px; min-width: 18px; padding: 0 5px; border-radius: 9px;
            background: #7A1424; color: #fff; font-size: 11px; line-height: 18px; text-align: center; opacity: 0; }
    .tl { position: absolute; width: 132px; height: 128px; }
    .tl .im { width: 132px; height: 98px; border-radius: 10px; position: relative; overflow: hidden; }
    .tl .im s { position: absolute; left: 22px; bottom: -6px; border-style: solid; border-width: 0 34px 46px 34px;
                border-color: transparent transparent rgba(255,255,255,.75) transparent; }
    .tl .im em { position: absolute; right: 22px; top: 18px; width: 20px; height: 20px; border-radius: 50%;
                 background: rgba(255,255,255,.8); }
    .tl .ok { position: absolute; left: 8px; top: 8px; width: 22px; height: 22px; border-radius: 50%;
              background: #7A1424; opacity: 0; }
    .tl .ok::after { content: ""; position: absolute; left: 8px; top: 4px; width: 5px; height: 10px;
                     border: solid #fff; border-width: 0 2px 2px 0; transform: rotate(45deg); }
    .tl .im::after { content: ""; position: absolute; inset: 0; border-radius: 10px; box-shadow: inset 0 0 0 0 #7A1424; }
    .tl .nm { position: relative; height: 24px; margin-top: 6px; font-size: 11.5px; color: #3c3434; }
    .tl .nm span { position: absolute; left: 0; top: 0; white-space: nowrap; }
    .tl .n1 { opacity: 0; color: #241919; font-weight: 500; }
    .car { display: inline-block; width: 1.5px; height: 13px; background: #7A1424; margin-left: 1px; vertical-align: -2px; }
"""


def cam(px, py, sc, cx=540, cy=760):
    # the window turns and scales about its own centre (400, 260)
    return (sc, round(cx - 400 - sc * (px - 400), 1), round(cy - 260 - sc * (py - 260), 1))


V = {"WIDE": cam(400, 260, 1.22), "ACC": cam(690, 24, 2.6), "GRID": cam(500, 250, 1.55),
     "GRID2": cam(560, 300, 1.7), "TILE": cam(410, 262, 3.1), "LIB": cam(280, 240, 1.5)}


def at(name, t, d, rx, ry, rz, ease="power3.inOut"):
    s, x, y = V[name]
    return (u'  tl.to("#win", {x: %s, y: %s, scale: %s, rotationX: %s, rotationY: %s, rotationZ: %s, duration: %s, ease: "%s"}, %.3f);'
            % (x, y, s, rx, ry, rz, d, ease, t))


s, x, y = V["WIDE"]
js(u'''
  tl.set("#stage", {autoAlpha: 1}, %(u0)s);
  gsap.set("#win", {x: %(x)s, y: %(y)s + 240, scale: %(s)s * .85, rotationX: 26, rotationY: -20, rotationZ: 5});
  tl.to("#win", {x: %(x)s, y: %(y)s, scale: %(s)s, rotationX: 9, rotationY: -12, rotationZ: 2, duration: 1.2, ease: "power3.out"}, %(u0)s + .15);
''' % {"u0": "%.3f" % u0, "x": x, "y": y, "s": s})
js(at("ACC", t_dost - 0.75, 1.0, 4, 8, 0))
js(u'  tl.to("#acc", {backgroundColor: "#7A1424", duration: .2}, %.3f); tl.to("#acc u", {x: 16, duration: .3, ease: "back.out(2)"}, %.3f);' % (t_dost + 0.1, t_dost + 0.1))
js(at("GRID", t_kart - 0.45, 1.2, 6, -6, 1))
js(at("GRID2", t_prod - 0.1, 1.6, 3, 7, -1, "sine.inOut"))
for i, k in enumerate((0, 5, 10)):
    tt = t_vidb + 0.05 + i * 0.28
    js(u'  tl.to("#tl%d .ok", {opacity: 1, duration: .2}, %.3f); tl.fromTo("#tl%d .im", {boxShadow: "inset 0 0 0 0 #7A1424"}, X({boxShadow: "inset 0 0 0 4px #7A1424", duration: .25}), %.3f);'
       % (k, tt, k, tt))
    js(u'  tl.fromTo("#tl%d", {scale: 1}, X({scale: .94, duration: .12, yoyo: true, repeat: 1}), %.3f);' % (k, tt))
js(at("TILE", t_kozh - 0.45, 1.1, 2, -5, 0))
js(u'''
  tl.to("#tl5 .n0", {opacity: 0, duration: .12}, %(n)s);
  tl.fromTo("#tl5 .n1", {opacity: 0, clipPath: "inset(0 100%% 0 0)"}, X({opacity: 1, clipPath: "inset(0 0%% 0 0)", duration: .55, ease: "steps(14)"}), %(n)s + .05);
  tl.to("#tl5 .car", {opacity: 0, duration: .05, repeat: 3, yoyo: true}, %(n)s + .65);
''' % {"n": "%.3f" % t_naz})
js(at("LIB", t_dod - 0.4, 0.9, 6, 4, -1))
for i, k in enumerate((0, 5, 10)):
    r, c = divmod(k, 4)
    tx, ty = 200 + c * 146 + 66, 64 + r * 140 + 49      # tile centre
    dx, dy = 92 - tx, 46 + 14 + 3 * 40 + 17 - ty         # to «Бібліотека стилю»
    js(u'  tl.to("#tl%d", {x: %d, y: %d, scale: .18, autoAlpha: 0, duration: .55, ease: "power2.in"}, %.3f);'
       % (k, dx, dy, t_dod + 0.15 + i * 0.12))
js(u'  tl.to("#lib", {backgroundColor: "#F6E3E4", color: "#7A1424", duration: .25}, %.3f);' % (t_sys - 0.05))
js(u'  tl.fromTo("#libn", {opacity: 0, scale: .4}, X({opacity: 1, scale: 1, duration: .4, ease: POP}), %.3f);' % (t_sys))
js(u'  tl.set("#stage", {autoAlpha: 0}, %.3f);' % (u1 + 0.9))
js(u'  full(%.3f, %.3f);' % (u0, u1))
g.sfx("whoosh-short", u0); g.sfx("click", t_dost + 0.1); g.sfx("whoosh-short", t_kart - 0.45)
g.sfx("click-soft", t_vidb + 0.05); g.sfx("whoosh-short", t_kozh - 0.45); g.sfx("typing", t_naz)
g.sfx("whoosh-short", t_dod + 0.1); g.sfx("pop", t_sys); g.sfx("whoosh-short", u1)

# 7 · ABOVE — the glass card: tuning is the long bar, the launch the short one ---
t_saме, t_naib, t_zap, t_tomu = S(u"саме", 48.50), S(u"найбільше", 49.76), S(u"запуск", 51.35), S(u"Тому", 52.46)
F.append(u'''
        <div id="bc" class="glass bars hid">
          <div class="r"><span class="l">налаштування стилю</span><span class="tr"><i id="bar1"></i></span></div>
          <div class="r"><span class="l">запуск монтажу</span><span class="tr"><i id="bar2"></i></span></div>
        </div>''')
js(u'''
  rise("#bc", %.3f);
  tl.fromTo("#bar1", {scaleX: 0}, X({scaleX: 1, duration: 1.0, ease: "power2.out"}), %.3f);
  tl.fromTo("#bar2", {scaleX: 0}, X({scaleX: .16, duration: .35, ease: "power2.out"}), %.3f);
  sink("#bc", %.3f);
''' % (t_saме - 0.1, t_naib - 0.05, t_zap, t_tomu + 0.15))
g.sfx("pop", t_saме - 0.1); g.sfx("click-soft", t_zap)

# 8 · BEHIND — «твій стиль», then she ends clean --------------------------------
t_tv, e_st = S(u"твій", 58.17), E(u"стиль,", 58.66)
B.append(u'        <div id="bw2" class="big hid" data-layout-allow-occlusion style="top:455px; font-size:178px">твій стиль</div>')
g.matte("b2", round(t_tv - 0.6, 3), 2.2)
js(u'  rise("#bw2", %.3f); sink("#bw2", %.3f);' % (t_tv - 0.3, S(u"повно-", 59.35) - 0.05))
g.sfx("whoosh-short", t_tv - 0.3)
BLACKOUT.append((t_tv - 0.03, e_st))

# ---------------------------------------------------------------- half screen + its matte
for i, (a, b) in enumerate(HALF):
    g.matte("half1", round(a - 0.1, 3), round(b - a + 1.2, 3))
    js("  half(%.3f, %.3f);" % (a, b))
    PLACE.append((a + 0.4, b + 0.2, "bottom", 938))


def main():
    chunks = g.chunks(CAPS, place=PLACE)
    doc = g.document(title=u"Reel 66 — твій стиль, а не клодівський", plate="assets/base.mp4",
                     behind="\n".join(B), panel="\n".join(P), front="\n".join(F), cover="\n".join(C),
                     js="\n".join(J), chunks=chunks, blackout=BLACKOUT, extra_css=EXTRA)
    g.write(HERE, doc)
    print("index.html  %d caption chunks, %d sfx cues, %d mattes" % (len(chunks), len(g.cues), len(g.mattes)))
    if "-v" in sys.argv:
        print(" ".join("%s/%.1f" % (c["w"], c["s"]) for c in CAPS))


main()
