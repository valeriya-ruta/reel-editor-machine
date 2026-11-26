# -*- coding: utf-8 -*-
"""Reel 65 — «Які автоматизації зробити фотографці?». Batch 2026-11-20
(raw 20261120_135335). STYLE.md §00 + her review of reel 61 (2026-11-23):
natural editing, one meaningful moment per sentence group, a list through
ONE shuffle slot, real UI as a full-screen platform-ad sequence, Excalidraw
only for the two schemes, no arrows over her footage, head room.

Chain: behind «Claude» (the hook / cover) -> list card 1 «Розклад: дорога +
погода» -> FULL: Claude, rebuilt in HTML, 3D camera: the Google Calendar
connector switches on, the scheduled task «ввечері перед зйомкою» lights, the
three steps tick (локація, погода, золота година), Claude's message lands and
its three lines arrive on her words -> list card 2 «LUT з референсу» -> HALF 1
the scheme фото -> Claude (скрипт) -> .cube -> Lightroom -> list card 3
«Відбір і обробка», its «Claude» tag struck on «ні до чого» -> Aftershoot,
Imagen through the same slot -> list card 4 «Клієнтський флоу» -> HALF 2 the
flow: Google Form -> Claude -> мудборд + план, a timeline: за день SendPulse
«що взяти», після зйомки Google Drive «галерея» -> slot: «через тиждень —
відгук» -> glass card: the same scheduled task from the full screen, «дивиться
в календар» -> CTA chips (Збережи / Перешли колезі) + the pill in the band.

usage: python3 build.py   (then: sfx mix, mattes — see AGENT-BRIEF)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
from gstyle import G, Words, load_caps, mark  # noqa: E402

NN = "65"
DUR = 73.550           # (plate frames - 0.5) / 30, set from the plate below
g = G(dur=DUR, reel=NN)
g.PANEL_TOP = 820      # panel captions: bottom 938, above her pushed-down hair

FIX = {
    (u"Як", 0.0): u"Якби", (u"би", 0.3): None, u"з клод": u"з Claude",
    u"Ставиш": u"ставиш", (u"Claude", 12.9): None, u"пишу": u"пише", u"виїжджаю": u"виїжджай",
    u"в 13": u"в 13:20,", u".20,": None, u"у 17": u"у 17:40.", u".40": None,
    u"рефлектор.": u"рефлектор,", u"Кидаєш": u"кидаєш", u"часто": u"чесно",
    u"І": u"і", u"Imagine,": u"Imagen,", (u"в", 44.4): u"вчаться", (u"чаті", 44.6): None,
    u"твої": u"твоєї", u"Бриф": u"бриф", (u"Claude", 52.6): None,
    u"Клод": u"Claude", u"Синьпус,": u"SendPulse,", u"Захаліто": u"за",
    u"нацилаю": u"надсилає", u"Ачори,": u"а через", u"сніждень": u"тиждень", u"видок.": u"відгук.", u"Тобі": u"Тож", u"своїх": u"своїй", u"колезій.": u"колезі.", u"як ви": u"як він", u"називаєте.": u"називається.",
    (u"в", 47.7): u"всі", u"сеті": u"ці",
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
    /* the list slot: plain white cards, a number in a red disc */
    .shuf .chip { font-size: 42px; padding: 18px 30px 18px 18px; gap: 18px; }
    .shuf .chip .n { width: 58px; height: 58px; border-radius: 50%; background: #7A1424; color: #fff;
                     font-weight: 700; font-size: 32px; display: inline-flex; align-items: center;
                     justify-content: center; flex: none; }
    .shuf .chip .tag { margin-left: 6px; font-size: 30px; font-weight: 500; color: #574142;
                       border: 2px solid #DEBFBF; border-radius: 12px; padding: 4px 14px; position: relative; }
    .shuf .chip .tag .st { position: absolute; left: 8px; right: 8px; top: 50%; height: 4px; margin-top: -2px;
                           border-radius: 2px; background: #7A1424; transform-origin: 0 50%; transform: scaleX(0); }
    .shuf .chip .ic { width: 44px; height: 44px; flex: none; color: #7A1424; }
    .shuf .chip.wm { font-weight: 700; letter-spacing: -0.01em; padding: 18px 34px; }
'''

# 1 · BEHIND — «Claude»: the hook word and the cover frame -------------------------
t_cl = S(u"з Claude", 3.55)
B.append(u'        <div id="bw1" class="big hid" data-layout-allow-occlusion style="top:420px; font-size:250px">Claude</div>')
t_sink = E(u"з Claude", 3.55) + 0.15
g.matte("b1", 0.0, round(t_sink + 0.4, 3))
js(u'  rise("#bw1", 0.05); sink("#bw1", %.3f);' % t_sink)
g.sfx("whoosh-short", 0.05)
BLACKOUT.append((t_cl - 0.03, E(u"з Claude", 3.55)))


# the list: one slot, cards rise in on their word and leave upward ------------------
def slot(name, html, t_in, t_out, cls=""):
    F.append(u'        <div id="%s" class="shuf hid"><span class="chip %s">%s</span></div>' % (name, cls, html))
    js(u'  shuffle(["#%s"], [%.3f], %.3f);' % (name, t_in, t_out))
    g.sfx("pop", t_in)


# 2 · list 1 -----------------------------------------------------------------------
t_p1 = S(u"Перша", 5.27)
slot("l1", u'<b class="n">1</b>Розклад: дорога + погода', t_p1 - 0.05, S(u"Ти", 8.17) - 0.05)

# 3 · FULL — Claude, rebuilt in HTML, as a platform-ad sequence -----------------------
# No screenshot of hers for this one: a clean, plausible Claude desktop window
# with only what she names (the Google Calendar connector, the scheduled task
# «ввечері перед зйомкою», локація / погода / золота година, the message).
f0 = S(u"Ти", 8.17) - 0.05
f1 = E(u"рефлектор,", 22.32) + 0.15      # out before her «рефрактор» joke
# Sizing as reel-60 (the quality bar): a 900x1150 window, ~88 % of the frame
# width zoomed out and y 240-1450, body text 40-46 px, labels 28 px (x1.05 on
# screen). The camera never leaves background below the window: every shot
# keeps the window from the top zone down to the caption band.
CLM = mark("claude", 46)
CAL = mark("googlecalendar", 40)
CLK = (u'<svg class="ck" viewBox="0 0 24 24" width="40" height="40"><circle cx="12" cy="12" r="9" fill="none" '
       u'stroke="#7A1424" stroke-width="2.2"/><path d="M12 7v5l3.5 2" fill="none" stroke="#7A1424" '
       u'stroke-width="2.2" stroke-linecap="round"/></svg>')
STEPS = [u"Дивиться локацію", u"Шукає погоду", u"Золота година"]
C.append(u"""
        <div id="stage">
          <div id="win">
            <div class="cw-bar">%(clm)s<span>Claude</span></div>
            <div class="cw-card" id="cA" style="top:120px">
              <div class="cw-h">Конектор</div>
              <div class="cw-row" id="rCal"><span class="cw-ic">%(cal)s</span>Google Calendar<em id="tgc"><u></u></em></div>
            </div>
            <div class="cw-card" id="cB" style="top:300px">
              <div class="cw-h">Запланована задача</div>
              <div class="cw-row" id="fW"><span class="cw-ic">%(clk)s</span>Ввечері перед зйомкою</div>
            </div>
            <div class="cw-steps">%(steps)s</div>
            <div class="cw-msg" id="msg">
              <div class="cw-who">%(clm2)s Claude</div>
              <div class="cw-ln hid" id="m1">Виїжджай о 13:20</div>
              <div class="cw-ln hid" id="m2">Найкраще світло о 17:40</div>
              <div class="cw-ln hid" id="m3">Візьми рефлектор</div>
            </div>
          </div>
        </div>""" % {"clm": CLM, "cal": CAL, "clk": CLK, "clm2": mark("claude", 32),
                     "steps": u"".join(u'<div class="cw-step" id="st%d"><b><i></i></b><span>%s</span></div>' % (i + 1, s)
                                       for i, s in enumerate(STEPS))})
EXTRA += u"""
    #cover { background: radial-gradient(120% 80% at 50% 35%, #FFFFFF 0%, #F6EFEF 70%, #F1E7E7 100%); }
    #stage { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; perspective: 2200px; }
    #win { position: absolute; left: 0; top: 0; width: 900px; height: 1150px; background: #fff;
           border-radius: 28px; font-family: "Google Sans", sans-serif; color: #241919; overflow: hidden;
           box-shadow: 0 2px 6px rgba(36,25,25,.10), 0 30px 80px rgba(36,25,25,.22);
           transform-origin: 0 0; will-change: transform; }
    #win .mark path { fill: #7A1424; }
    .cw-bar { position: absolute; left: 0; top: 0; width: 900px; height: 96px; box-sizing: border-box;
              border-bottom: 2px solid #F1E7E7; display: flex; align-items: center; gap: 16px; padding: 0 40px;
              font-size: 44px; font-weight: 700; }
    .cw-card { position: absolute; left: 40px; width: 820px; height: 160px; box-sizing: border-box;
               padding: 20px 24px; border: 3px solid #ECE6E6; border-radius: 24px; }
    .cw-h { font-size: 28px; font-weight: 700; letter-spacing: .04em; text-transform: uppercase; color: #574142;
            margin-bottom: 12px; }
    .cw-row { display: flex; align-items: center; gap: 18px; font-size: 42px; font-weight: 500; height: 76px;
              padding: 0 18px; border-radius: 16px; background: #FBF6F6; position: relative; }
    .cw-ic { width: 44px; height: 44px; display: inline-flex; align-items: center; justify-content: center; flex: none; }
    .cw-row em { margin-left: auto; width: 88px; height: 50px; border-radius: 25px; background: #C9C1C1;
                 position: relative; flex: none; }
    .cw-row em u { position: absolute; left: 5px; top: 5px; width: 40px; height: 40px; border-radius: 50%;
                   background: #fff; box-shadow: 0 1px 3px rgba(0,0,0,.25); }
    .cw-steps { position: absolute; left: 40px; top: 490px; width: 820px; }
    .cw-step { display: flex; align-items: center; gap: 20px; height: 74px; box-sizing: border-box; padding: 0 22px;
               margin-bottom: 14px; border: 3px solid #ECE6E6; border-radius: 18px; font-size: 40px; color: #A8999A; }
    .cw-step b { width: 34px; height: 34px; border-radius: 50%; border: 3px solid #DEBFBF; flex: none;
                 box-sizing: border-box; position: relative; }
    .cw-step b i { position: absolute; left: 9px; top: 3px; width: 8px; height: 16px; display: block;
                   border: solid #fff; border-width: 0 4px 4px 0; transform: rotate(45deg); opacity: 0; }
    .cw-msg { position: absolute; left: 40px; top: 770px; width: 820px; height: 340px; box-sizing: border-box;
              background: #FFF0F0; border-radius: 24px; padding: 26px 32px; }
    .cw-who { display: flex; align-items: center; gap: 12px; font-size: 32px; font-weight: 700; color: #574142;
              height: 56px; margin-bottom: 8px; }
    .cw-ln { font-size: 48px; font-weight: 500; line-height: 76px; color: #241919; }
"""
t_kon, t_goo = S(u"конектор", 8.80), S(u"Google", 9.34)
t_plan, t_vve = S(u"плануєш", 10.20), S(u"ввечері", 11.55)
t_dyv, t_pog, t_zol = S(u"дивиться", 13.31), S(u"погоду", 14.95), S(u"і золоту", 15.31)
t_sam, t_vy, t_svit, t_vzia = S(u"сам", 16.67), S(u"виїжджай", 17.77), S(u"найкраще", 19.77), S(u"взяти", 21.98)
OX, OY = 450, 575   # the window's own centre


def cam(sc, top):
    """the window turns and scales about its centre O; centred in x, its top
    edge lands at y = top (so a push is a scale + a vertical travel)"""
    return (sc, 540 - OX, round(top - OY + sc * OY, 1))


WIDE = cam(1.05, 240)    # 945 x 1208: ~88 % of the width, y 240-1448
# pushes stay <= 1.14: with the tilt's perspective the near edge grows ~5 %,
# and the rows' text must never touch the frame edge
CON = cam(1.12, 250)     # the connector card at y 385-565, window down to 1538
TSK = cam(1.14, 170)     # the scheduled task card at y 510-695
STP = cam(1.14, 60)      # the three steps at y 620-890, window down to 1371
MSG = cam(1.12, 112)     # Claude's message at y 975-1355, window bottom 1400


def at(c, rx, ry, rz, d, ease, t):
    return (u'  tl.to("#win", {x: %s, y: %s, scale: %s, rotationX: %s, rotationY: %s, rotationZ: %s, '
            u'duration: %s, ease: "%s"}, %.3f);' % (c[1], c[2], c[0], rx, ry, rz, d, ease, t))


js(u'  gsap.set("#win", {transformOrigin: "%dpx %dpx"});' % (OX, OY))
js(u'  gsap.set("#win", {x: %s, y: %s, scale: %s, rotationX: 24, rotationY: -20, rotationZ: 5});'
   % (WIDE[1], WIDE[2] + 220, WIDE[0] * 0.86))
js(at(WIDE, 6, -6, 1, 0.75, "power3.out", f0 + 0.1))
js(at(CON, 4, 4, 0, 0.9, "power3.inOut", f0 + 0.87))
js(u'  tl.to("#tgc", {backgroundColor: "#7A1424", duration: .2}, %.3f);' % t_goo)
js(u'  tl.to("#tgc u", {x: 38, duration: .3, ease: "back.out(2)"}, %.3f);' % t_goo)
js(u'  tl.fromTo("#rCal", {boxShadow: "0 0 0 0 rgba(122,20,36,0)"}, X({boxShadow: "0 0 0 6px rgba(122,20,36,.18)", duration: .35, yoyo: true, repeat: 1}), %.3f);' % (t_goo + 0.1))
js(at(TSK, -3, -4, 0, 1.0, "power3.inOut", t_plan - 0.35))
js(u'  tl.fromTo("#cB", {borderColor: "#ECE6E6"}, X({borderColor: "#7A1424", duration: .3}), %.3f);' % t_vve)
js(at(STP, 3, 4, -1, 1.0, "power3.inOut", t_dyv - 0.6))
for i, t in enumerate((t_dyv, t_pog, t_zol)):
    js(u'  tl.to("#st%d", {color: "#241919", borderColor: "#DEBFBF", duration: .2}, %.3f);' % (i + 1, t + 0.25))
    js(u'  tl.to("#st%d b", {backgroundColor: "#7A1424", borderColor: "#7A1424", duration: .2}, %.3f);' % (i + 1, t + 0.25))
    js(u'  tl.to("#st%d b i", {opacity: 1, duration: .2}, %.3f);' % (i + 1, t + 0.3))
    js(u'  tl.fromTo("#st%d b", {scale: .6}, X({scale: 1, duration: .35, ease: POP}), %.3f);' % (i + 1, t + 0.25))
    g.sfx("click-soft", t + 0.25)
js(at(MSG, -2, -4, 0, 1.0, "power3.inOut", t_sam - 0.4))
js(u'  tl.fromTo("#msg", {backgroundColor: "#FBF6F6"}, X({backgroundColor: "#FFF0F0", duration: .3}), %.3f);' % (t_sam - 0.1))
for i, t in enumerate((t_vy, t_svit, t_vzia)):
    js(u'  rise("#m%d", %.3f, 14);' % (i + 1, t - 0.05))
js(at(WIDE, 6, 6, -1, 0.8, "power3.inOut", t_vzia + 0.15))
js(u'  full(%.3f, %.3f);' % (f0, f1))
g.sfx("whoosh-short", f0); g.sfx("click", t_goo)
g.sfx("whoosh-short", t_plan - 0.35); g.sfx("whoosh-short", t_dyv - 0.6)
g.sfx("notification", t_sam - 0.1); g.sfx("whoosh-short", f1)

# 4 · list 2 -----------------------------------------------------------------------
t_dr = S(u"Друга", 24.80)
# on «LUT»: the meme for «як він там називається» has the top band until then
slot("l2", u'<b class="n">2</b>LUT з референсу', S(u"LUT", 25.85) - 0.05, S(u"Ти", 27.02) - 0.1)

# 5 · HALF 1 — the LUT scheme ----------------------------------------------------------
k0 = S(u"Ти", 27.02) - 0.05
k1 = E(u"у Lightroom.", 35.40) + 0.15
HALF.append((k0, k1))
t_foto, t_skr, t_cube, t_lr = S(u"фото,", 27.88), S(u"скрипт", 31.59), S(u".cube", 33.11), S(u"у Lightroom.", 35.40)
js(u'''
  sketch("a1", "skP"); box("a1", 100, 330, 220, 150, {seed: 3, fill: true});
  label("a1", 210, 425, "фото", {size: 54});
  draw("a1", %.3f);
  sketch("a2", "skP"); arrow("a2", 335, 405, 495, 405, {seed: 5, bend: .06});
  box("a2", 505, 330, 260, 150, {seed: 7}); label("a2", 635, 425, "Claude", {size: 54});
  draw("a2", %.3f);
  sketch("a3", "skP"); label("a3", 635, 545, "пише скрипт", {size: 44, color: "#7A1424"});
  draw("a3", %.3f);
  sketch("a4", "skP"); arrow("a4", 785, 400, 862, 612, {seed: 9, bend: -.18});
  box("a4", 740, 625, 240, 135, {seed: 11, fill: true}); label("a4", 860, 712, ".cube", {size: 58});
  draw("a4", %.3f);
  sketch("a5", "skP"); arrow("a5", 728, 692, 528, 692, {seed: 13, bend: .06});
  box("a5", 180, 625, 335, 135, {seed: 15}); label("a5", 347, 712, "Lightroom", {size: 54});
  draw("a5", %.3f);
  erase("a1", %.3f); erase("a2", %.3f); erase("a3", %.3f); erase("a4", %.3f); erase("a5", %.3f);
''' % (t_foto - 0.45, t_foto + 0.35, t_skr - 0.2, t_cube - 0.55, t_lr - 1.05, k1, k1, k1, k1, k1))
g.sfx("whoosh-short", k0); g.sfx("click-soft", t_skr); g.sfx("pop", t_cube); g.sfx("click-soft", t_lr)

# 6 · list 3, its «Claude» tag struck, then the two platforms through the slot ------------
t_tr, t_ni = S(u"Третє", 36.00), S(u"ні", 39.82)
t_af, t_im = S(u"Aftershoot", 42.27), S(u"Imagen,", 43.34)
slot("l3", u'<b class="n">3</b>Відбір і обробка<span class="tag">Claude<i class="st"></i></span>',
     t_tr + 0.3, E(u"чого.", 40.08) + 0.05)   # after the half screen's panel has lifted
js(u'  tl.fromTo("#l3 .st", {scaleX: 0}, X({scaleX: 1, duration: .3, ease: "power2.out"}), %.3f);' % (t_ni - 0.1))
js(u'  tl.to("#l3 .tag", {opacity: .55, duration: .3}, %.3f);' % (t_ni + 0.2))
g.sfx("click", t_ni - 0.1)
slot("l3a", u'Aftershoot', t_af - 0.05, t_im - 0.05, cls="wm")
slot("l3b", u'Imagen', t_im - 0.05, S(u"обробки,", 45.38) + 0.6, cls="wm")

# 7 · list 4 -----------------------------------------------------------------------
t_ch = S(u"четверте,", 48.84)
slot("l4", u'<b class="n">4</b>Клієнтський флоу', t_ch - 0.05, S(u"тобто", 51.08) + 0.2)

# 8 · HALF 2 — the client flow --------------------------------------------------------
h0 = S(u"Google", 52.12) - 0.4
h1 = h0 + 12.0
HALF.append((h0, h1))
t_form, t_cl2, t_mud = S(u"Form,", 52.42), S(u"Claude", 53.76), S(u"мудборд", 54.32)
t_sp, t_den, t_vz = S(u"SendPulse,", 55.77), S(u"день", 56.93), S(u"що взяти", 58.03)
t_pis, t_gal = S(u"після", 61.34), S(u"галерею", 63.42)
js(u'''
  sketch("b1", "skP"); box("b1", 95, 320, 185, 135, {seed: 21, fill: true});
  label("b1", 187, 380, "бриф", {size: 48}); label("b1", 187, 428, "Google Form", {size: 28});
  draw("b1", %.3f);
  sketch("b2", "skP"); arrow("b2", 290, 388, 440, 388, {seed: 23, bend: .06});
  box("b2", 450, 320, 185, 135, {seed: 25}); label("b2", 542, 402, "Claude", {size: 46});
  draw("b2", %.3f);
  sketch("b3", "skP"); arrow("b3", 645, 388, 795, 388, {seed: 27, bend: .06});
  box("b3", 805, 320, 185, 135, {seed: 29, fill: true});
  label("b3", 897, 380, "мудборд", {size: 40}); label("b3", 897, 428, "+ план", {size: 32});
  draw("b3", %.3f);
  sketch("b4", "skP"); ln("b4", 100, 600, 980, 600, {seed: 31, strokeWidth: 5});
  draw("b4", %.3f, .9);
  sketch("b5", "skP"); ln("b5", 300, 575, 300, 625, {seed: 33, strokeWidth: 6});
  label("b5", 300, 555, "за день", {size: 38, color: "#7A1424"});
  box("b5", 160, 645, 280, 100, {seed: 35}); label("b5", 300, 710, "SendPulse", {size: 42});
  draw("b5", %.3f);
  sketch("b6", "skP"); label("b6", 300, 790, "«що взяти з собою»", {size: 34});
  draw("b6", %.3f);
  sketch("b7", "skP"); ln("b7", 760, 575, 760, 625, {seed: 37, strokeWidth: 6});
  label("b7", 760, 555, "після зйомки", {size: 38, color: "#7A1424"});
  box("b7", 610, 645, 300, 100, {seed: 39}); label("b7", 760, 710, "Google Drive", {size: 42});
  draw("b7", %.3f);
  sketch("b8", "skP"); label("b8", 760, 790, "галерея", {size: 34});
  draw("b8", %.3f);
  erase("b1", %.3f); erase("b2", %.3f); erase("b3", %.3f); erase("b4", %.3f);
  erase("b5", %.3f); erase("b6", %.3f); erase("b7", %.3f); erase("b8", %.3f);
''' % ((t_form - 0.45, t_cl2 - 0.5, t_mud - 0.4, t_sp - 0.7, t_den - 0.5, t_vz, t_pis - 0.2, t_gal - 0.2)
       + (h1,) * 8))
g.sfx("whoosh-short", h0); g.sfx("click-soft", t_cl2); g.sfx("click-soft", t_mud)
g.sfx("click-soft", t_den); g.sfx("click-soft", t_pis)

# 9 · slot: the last step, then the glass card — it is all one scheduled task ----------
t_ach, t_vid = S(u"а через", 64.43), S(u"відгук.", 65.56)
slot("l5", u'Через тиждень — відгук', t_ach - 0.05, S(u"все", 66.30) - 0.1)
t_vse, t_zap, t_dyv2 = S(u"все", 66.30), S(u"запланованою", 67.88), S(u"дивиться", 69.52)
F.append(u'''
        <div id="tk" class="glass hid">
          <div class="tk-h">%s Запланована задача</div>
          <div class="tk-r hid" id="tkr">%s дивиться в календар</div>
        </div>''' % (mark("claude", 34), mark("googlecalendar", 32)))
EXTRA += u"""
    #tk { left: 0; right: 0; margin: auto; width: max-content; top: 320px; padding: 26px 34px; }
    #tk .mark path { fill: #7A1424; }
    .tk-h { display: flex; align-items: center; gap: 16px; font-size: 44px; font-weight: 700; color: #241919; }
    .tk-r { display: flex; align-items: center; gap: 14px; margin-top: 16px; font-size: 34px; font-weight: 500;
            color: #574142; }
"""
js(u'  rise("#tk", %.3f); fadein("#tkr", %.3f); sink("#tk", %.3f);' % (t_zap - 0.3, t_dyv2 - 0.1, E(u"календар.", 70.0) + 0.02))
g.sfx("pop", t_zap - 0.3); g.sfx("click-soft", t_dyv2)

# MEMES (assets/memes/MEMES.md) — comic relief after the beat lands ---------------------
g.cta_start = S(u"Тож", 70.53)
# 56 «Цей во… Забув…»: she can't remember what the thing is called (рефлектор /
# рефрактор, як він там називається); right after the line, before list card 2
g.meme(F, J, "56", E(u"називається.", 24.1) + 0.1, dur=1.0, slot="top")
# 59 «алівідерчі»: «Claude вже ні до чого» — Claude leaves the list
g.meme(F, J, "59", E(u"чого.", 40.08) + 0.1, dur=1.2, slot="r")

# 10 · CTA — two chips through the slot, the pill in the subtitle band ----------------------
t_zb, t_per = S(u"збережеш,", 70.82), S(u"перешли", 72.34)
BM = (u'<svg class="ic" viewBox="0 0 24 24"><path d="M6 3h12a1 1 0 0 1 1 1v17l-7-4.5L5 21V4a1 1 0 0 1 1-1z" '
      u'fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/></svg>')
PL = (u'<svg class="ic" viewBox="0 0 24 24"><path d="M21.5 2.5 10.5 13.5M21.5 2.5 14.5 21.5l-4-8-8-4z" '
      u'fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/></svg>')
slot("c1", BM + u'Збережи', t_zb - 0.1, t_per - 0.1)
slot("c2", PL + u'Перешли колезі', t_per - 0.1, DUR + 1)
F.append(u'''        <div id="ctp" class="pill hid" style="left:0; right:0; margin:auto; width:max-content; top:1404px;
             font-size:46px; padding:28px 56px">Збережи і перешли колезі</div>''')
js(u'  pop("#ctp", %.3f);' % (S(u"Тож", 70.53) - 0.05))
BLACKOUT.append((S(u"Тож", 70.53) - 0.08, DUR))

# ---------------------------------------------------------------- half screens + their mattes
for i, (a, b) in enumerate(HALF):
    g.matte("half%d" % (i + 1), round(a - 0.1, 3), round(b - a + 1.2, 3))
    js("  half(%.3f, %.3f);" % (a, b))
    PLACE.append((a + 0.4, b + 0.2, "bottom", 938))


def main():
    chunks = g.chunks(CAPS, place=PLACE)
    doc = g.document(title=u"Reel 65 — автоматизації фотографки", plate="assets/base.mp4",
                     behind="\n".join(B), panel="\n".join(P), front="\n".join(F), cover="\n".join(C),
                     js="\n".join(J), chunks=chunks, blackout=BLACKOUT, extra_css=EXTRA)
    g.write(HERE, doc)
    print("index.html  %d caption chunks, %d sfx cues, %d mattes" % (len(chunks), len(g.cues), len(g.mattes)))
    if "--words" in sys.argv:
        print(" ".join(u"%s/%.1f" % (c["w"], c["s"]) for c in CAPS))


main()
