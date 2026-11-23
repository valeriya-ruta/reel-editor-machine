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
B.append(u'        <div id="bw1" class="big hid" data-layout-allow-occlusion style="top:490px; font-size:250px">Claude</div>')
g.matte("b1", 0.0, 4.95)
js(u'  rise("#bw1", 0.05); sink("#bw1", %.3f);' % (E(u"налаштувала", 4.51) + 0.05))
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
CLM = mark("claude", 22)
CAL = mark("googlecalendar", 20)
C.append(u"""
        <div id="stage">
          <div id="win">
            <div class="cw-bar"><i></i><i></i><i></i><span>%(clm)s Claude</span></div>
            <div class="cw-side">
              <div class="cw-card" id="cA">
                <div class="cw-h">Конектори</div>
                <div class="cw-row" id="rCal"><span class="cw-ic">%(cal)s</span>Google Calendar<em id="tgc"><u></u></em></div>
              </div>
              <div class="cw-card" id="cB">
                <div class="cw-h">Запланована задача</div>
                <div class="cw-tt">Перед зйомкою</div>
                <div class="cw-l">Коли</div>
                <div class="cw-f" id="fW">Ввечері перед зйомкою</div>
                <div class="cw-l">Звідки</div>
                <div class="cw-f"><span class="cw-ic">%(cal)s</span>Google Calendar</div>
              </div>
            </div>
            <div class="cw-chat">
              <div class="cw-ct">Перед зйомкою <span>· запланована задача</span></div>
              <div class="cw-step hid" id="st1"><b></b>Дивиться локацію<s></s></div>
              <div class="cw-step hid" id="st2"><b></b>Шукає погоду<s></s></div>
              <div class="cw-step hid" id="st3"><b></b>Золота година<s></s></div>
              <div class="cw-msg hid" id="msg">
                <div class="cw-who">%(clm)s Claude</div>
                <div class="cw-ln hid" id="m1">Виїжджай о 13:20</div>
                <div class="cw-ln hid" id="m2">Найкраще світло о 17:40</div>
                <div class="cw-ln hid" id="m3">Візьми рефлектор</div>
              </div>
            </div>
          </div>
        </div>""" % {"clm": CLM, "cal": CAL})
EXTRA += u"""
    #cover { background: radial-gradient(120% 80% at 50% 35%, #FFFFFF 0%, #F6EFEF 70%, #F1E7E7 100%); }
    #stage { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; perspective: 2200px; }
    #win { position: absolute; left: 0; top: 0; width: 800px; height: 520px; background: #FAF9F5;
           border-radius: 14px; font-family: "Google Sans", sans-serif; color: #1F1E1D; overflow: hidden;
           box-shadow: 0 2px 6px rgba(36,25,25,.10), 0 30px 80px rgba(36,25,25,.22);
           transform-origin: 0 0; will-change: transform; }
    #win .mark path { fill: #D97757; }
    .cw-bar { height: 38px; border-bottom: 1px solid #E8E4DA; display: flex; align-items: center;
              padding: 0 14px; gap: 7px; background: #F3F1EA; }
    .cw-bar i { width: 11px; height: 11px; border-radius: 50%; background: #DAD6CC; display: block; }
    .cw-bar span { margin-left: 260px; display: inline-flex; align-items: center; gap: 8px;
                   font-size: 15px; font-weight: 700; }
    .cw-side { position: absolute; left: 16px; top: 54px; width: 340px; }
    .cw-card { background: #fff; border: 1px solid #E8E4DA; border-radius: 12px; padding: 14px 16px;
               margin-bottom: 14px; }
    .cw-h { font-size: 11px; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; color: #6B6A65;
            margin-bottom: 10px; }
    .cw-row { display: flex; align-items: center; gap: 10px; font-size: 15px; font-weight: 500;
              padding: 8px 10px; border-radius: 9px; background: #F6F4EE; position: relative; }
    .cw-ic { width: 22px; height: 22px; display: inline-flex; align-items: center; justify-content: center; }
    .cw-ic .mark path { fill: #1F1E1D !important; }
    .cw-row em { margin-left: auto; width: 34px; height: 19px; border-radius: 10px; background: #C9C6BD;
                 position: relative; flex: none; }
    .cw-row em u { position: absolute; left: 2px; top: 2px; width: 15px; height: 15px; border-radius: 50%;
                   background: #fff; box-shadow: 0 1px 2px rgba(0,0,0,.25); }
    .cw-tt { font-size: 19px; font-weight: 700; margin-bottom: 10px; }
    .cw-l { font-size: 11px; font-weight: 700; color: #6B6A65; margin: 8px 0 5px; }
    .cw-f { font-size: 14px; border: 1px solid #DAD6CC; border-radius: 8px; padding: 8px 10px;
            display: flex; align-items: center; gap: 8px; background: #fff; }
    .cw-chat { position: absolute; left: 372px; top: 54px; width: 412px; height: 450px; background: #fff;
               border: 1px solid #E8E4DA; border-radius: 12px; padding: 16px 18px; }
    .cw-ct { font-size: 15px; font-weight: 700; margin-bottom: 14px; }
    .cw-ct span { font-weight: 400; color: #6B6A65; }
    .cw-step { display: flex; align-items: center; gap: 10px; font-size: 14px; color: #3D3C38;
               padding: 7px 10px; border: 1px solid #E8E4DA; border-radius: 9px; margin-bottom: 8px;
               background: #FAF9F5; }
    .cw-step b { width: 14px; height: 14px; border-radius: 50%; border: 2px solid #D97757; flex: none; }
    .cw-step s { margin-left: auto; width: 16px; height: 16px; border-radius: 50%; background: #1EA672;
                 position: relative; opacity: 0; text-decoration: none; }
    .cw-step s::after { content: ""; position: absolute; left: 5px; top: 2px; width: 4px; height: 8px;
                        border: solid #fff; border-width: 0 2px 2px 0; transform: rotate(45deg); }
    .cw-msg { margin-top: 16px; background: #F6F4EE; border-radius: 14px; padding: 14px 16px 10px; }
    .cw-who { display: flex; align-items: center; gap: 8px; font-size: 13px; font-weight: 700;
              color: #6B6A65; margin-bottom: 8px; }
    .cw-ln { font-size: 20px; font-weight: 500; line-height: 1.35; padding: 5px 0; color: #1F1E1D; }
"""
t_kon, t_goo = S(u"конектор", 8.80), S(u"Google", 9.34)
t_plan, t_vve = S(u"плануєш", 10.20), S(u"ввечері", 11.55)
t_dyv, t_pog, t_zol = S(u"дивиться", 13.31), S(u"погоду", 14.95), S(u"і золоту", 15.31)
t_sam, t_vy, t_svit, t_vzia = S(u"сам", 16.67), S(u"виїжджай", 17.77), S(u"найкраще", 19.77), S(u"взяти", 21.98)
OX, OY = 400, 260   # the window's own centre


def cam(px, py, sc, cx=540, cy=760):
    """the window turns and scales about its centre: a point p of it lands at
    O + s*(p - O) + (x, y); this centres p at (cx, cy)"""
    return (sc, round(cx - OX - sc * (px - OX), 1), round(cy - OY - sc * (py - OY), 1))


WIDE = cam(400, 260, 1.22)
CON = cam(190, 118, 2.4)       # the connector row
TSK = cam(190, 300, 2.1)       # the scheduled task card
STP = cam(560, 170, 2.05)      # the steps
MSG = cam(578, 330, 2.0)       # the message


def at(c, rx, ry, rz, d, ease, t):
    return (u'  tl.to("#win", {x: %s, y: %s, scale: %s, rotationX: %s, rotationY: %s, rotationZ: %s, '
            u'duration: %s, ease: "%s"}, %.3f);' % (c[1], c[2], c[0], rx, ry, rz, d, ease, t))


js(u'  gsap.set("#win", {transformOrigin: "%dpx %dpx"});' % (OX, OY))
js(u'  gsap.set("#win", {x: %s, y: %s, scale: %s, rotationX: 24, rotationY: -20, rotationZ: 5});'
   % (WIDE[1], WIDE[2] + 220, WIDE[0] * 0.86))
js(at(WIDE, 9, -12, 2, 0.9, "power3.out", f0 + 0.12))
js(at(CON, 4, 8, 0, 1.0, "power3.inOut", t_kon - 0.25))
js(u'  tl.to("#tgc", {backgroundColor: "#D97757", duration: .2}, %.3f);' % t_goo)
js(u'  tl.to("#tgc u", {x: 15, duration: .3, ease: "back.out(2)"}, %.3f);' % t_goo)
js(u'  tl.fromTo("#rCal", {boxShadow: "0 0 0 0 rgba(217,119,87,0)"}, X({boxShadow: "0 0 0 4px rgba(217,119,87,.28)", duration: .35, yoyo: true, repeat: 1}), %.3f);' % (t_goo + 0.1))
js(at(TSK, -3, -8, 0, 1.1, "power3.inOut", t_plan - 0.35))
js(u'  tl.to("#fW", {borderColor: "#D97757", boxShadow: "0 0 0 3px rgba(217,119,87,.20)", duration: .3}, %.3f);' % t_vve)
js(at(STP, 3, 9, -1, 1.1, "power3.inOut", t_dyv - 0.45))
for i, t in enumerate((t_dyv, t_pog, t_zol)):
    js(u'  rise("#st%d", %.3f, 16); tl.to("#st%d s", {opacity: 1, duration: .2}, %.3f);' % (i + 1, t, i + 1, t + 0.45))
    g.sfx("click-soft", t + 0.45)
js(at(MSG, -2, -7, 0, 1.0, "power3.inOut", t_sam - 0.35))
js(u'  rise("#msg", %.3f, 20);' % (t_sam - 0.1))
for i, t in enumerate((t_vy, t_svit, t_vzia)):
    js(u'  rise("#m%d", %.3f, 14);' % (i + 1, t - 0.05))
js(at(WIDE, 10, 14, -2, 1.0, "power3.inOut", t_vzia + 0.3))
js(u'  full(%.3f, %.3f);' % (f0, f1))
g.sfx("whoosh-short", f0); g.sfx("whoosh-short", t_kon - 0.25); g.sfx("click", t_goo)
g.sfx("whoosh-short", t_plan - 0.35); g.sfx("whoosh-short", t_dyv - 0.45)
g.sfx("notification", t_sam - 0.1); g.sfx("whoosh-short", f1)

# 4 · list 2 -----------------------------------------------------------------------
t_dr = S(u"Друга", 24.80)
slot("l2", u'<b class="n">2</b>LUT з референсу', t_dr - 0.05, S(u"Ти", 27.02) - 0.1)

# 5 · HALF 1 — the LUT scheme ----------------------------------------------------------
k0 = S(u"Ти", 27.02) - 0.05
k1 = E(u"у Lightroom.", 35.40) + 0.35
HALF.append((k0, k1))
t_foto, t_skr, t_cube, t_lr = S(u"фото,", 27.88), S(u"скрипт", 31.59), S(u".cube", 33.11), S(u"у Lightroom.", 35.40)
js(u'''
  sketch("a1", "skP"); box("a1", 70, 330, 250, 170, {seed: 3, fill: true});
  label("a1", 195, 432, "фото", {size: 54});
  draw("a1", %.3f);
  sketch("a2", "skP"); arrow("a2", 330, 415, 405, 415, {seed: 5, bend: 0});
  box("a2", 415, 330, 250, 170, {seed: 7}); label("a2", 540, 432, "Claude", {size: 54});
  draw("a2", %.3f);
  sketch("a3", "skP"); label("a3", 540, 560, "пише скрипт", {size: 44, color: "#7A1424"});
  draw("a3", %.3f);
  sketch("a4", "skP"); arrow("a4", 675, 415, 750, 415, {seed: 9, bend: 0});
  box("a4", 760, 330, 250, 170, {seed: 11, fill: true}); label("a4", 885, 432, ".cube", {size: 58});
  draw("a4", %.3f);
  sketch("a5", "skP"); arrow("a5", 885, 510, 720, 680, {seed: 13, bend: -.2});
  box("a5", 380, 630, 330, 130, {seed: 15}); label("a5", 545, 712, "Lightroom", {size: 54});
  draw("a5", %.3f);
  erase("a1", %.3f); erase("a2", %.3f); erase("a3", %.3f); erase("a4", %.3f); erase("a5", %.3f);
''' % (t_foto - 0.45, t_foto + 0.35, t_skr - 0.2, t_cube - 0.55, t_lr - 1.05, k1, k1, k1, k1, k1))
g.sfx("whoosh-short", k0); g.sfx("click-soft", t_skr); g.sfx("pop", t_cube); g.sfx("click-soft", t_lr)

# 6 · list 3, its «Claude» tag struck, then the two platforms through the slot ------------
t_tr, t_ni = S(u"Третє", 36.00), S(u"ні", 39.82)
t_af, t_im = S(u"Aftershoot", 42.27), S(u"Imagen,", 43.34)
slot("l3", u'<b class="n">3</b>Відбір і обробка<span class="tag">Claude<i class="st"></i></span>',
     t_tr - 0.05, S(u"але", 40.52) + 0.4)
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
  sketch("b1", "skP"); box("b1", 80, 320, 270, 140, {seed: 21, fill: true});
  label("b1", 215, 380, "бриф", {size: 50}); label("b1", 215, 430, "Google Form", {size: 34});
  draw("b1", %.3f);
  sketch("b2", "skP"); arrow("b2", 360, 390, 425, 390, {seed: 23, bend: 0});
  box("b2", 435, 320, 220, 140, {seed: 25}); label("b2", 545, 405, "Claude", {size: 50});
  draw("b2", %.3f);
  sketch("b3", "skP"); arrow("b3", 665, 390, 725, 390, {seed: 27, bend: 0});
  box("b3", 735, 320, 265, 140, {seed: 29, fill: true});
  label("b3", 867, 380, "мудборд", {size: 46}); label("b3", 867, 432, "+ план зйомки", {size: 34});
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
js(u'  rise("#tk", %.3f); fadein("#tkr", %.3f); sink("#tk", %.3f);' % (t_zap - 0.3, t_dyv2 - 0.1, E(u"календар.", 70.0) + 0.2))
g.sfx("pop", t_zap - 0.3); g.sfx("click-soft", t_dyv2)

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
