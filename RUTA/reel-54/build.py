# -*- coding: utf-8 -*-
"""Reel 54 — «Це відео змонтував мій Клод». The 22 s closer, her second take
(2026-10-27 15:11), in the Google style + Excalidraw look (STYLE.md §00).

The morning's build of the first take (branch ccr-8db4e5ef, «reel 41» there)
was refined glass; she asked for this take in the look of reels 41–52.

The one object is **the two things that ran at once**: the reel on her phone
and the long video she recorded. The phone reel is named on top, then the half
screen draws it as two lanes — «цей рілс → Клод монтує» over «я: довге відео
з поясненнями» — tied by one bracket, «15 хв». Then what to invest in: the
system, against a course / SMM / lost time, struck one by one. CTA: the button
under the video, a long arrow straight down.

Her plate is framed close (glasses top ≈ y 420–600), so the above-me band is a
single row at y 280–390 on the «in» clips, and the half screen's captions sit
higher than the kit's default (PANEL_TOP 690: her pushed head starts ≈ y 875).

usage: python3 build.py
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
from gstyle import G, Words, load_caps, mark  # noqa: E402

NN = "54"
DUR = 18.816           # (565 plate frames - 0.5) / 30
g = G(dur=DUR, reel=NN)
g.PANEL_TOP = 690      # captions on the panel: bottom 808, clear of her pushed head

# whisper's spelling of what she plainly said -> her word (checked on the plate)
FIX = {u"Ріос": u"рілс"}
CAPS = load_caps(NN, FIX)
W = Words(CAPS)
S, E = W.s, W.e

B, P, F, C, J = [], [], [], [], []     # behind / panel / front / cover html, js
BLACKOUT = []
PLACE = []
HALF = []


def js(s):
    J.append(s)


F.append(u'<svg class="sk" id="skF" width="1080" height="1920" viewBox="0 0 1080 1920"></svg>')

# 1 · ABOVE — the reel on her phone -------------------------------------------
t_zap, t_rils = S(u"записала", 1.41), S(u"рілс", 1.89)
t_tse = S(u"це відео", 3.65)
F.append(u'''
        <div id="b1" class="pill light hid" style="left:0; right:0; margin:auto; width:max-content;
             top:282px; padding:26px 52px; font-size:52px;">
          <svg width="38" height="62" viewBox="0 0 34 56"><rect x="3" y="3" width="28" height="50" rx="8"
               fill="none" stroke="#241919" stroke-width="5"/><circle cx="17" cy="45" r="3" fill="#241919"/></svg>
          рілс на телефоні
          <span id="b1d" style="width:22px; height:22px; border-radius:50%; background:#7A1424; display:inline-block"></span>
        </div>''')
js(u'''
  pop("#b1", %.3f);
  tl.to("#b1d", {opacity: .15, duration: .3, yoyo: true, repeat: 3, ease: "sine.inOut"}, %.3f);
  sink("#b1", %.3f);
''' % (t_zap, t_zap + 0.5, t_tse - 0.05))
g.sfx("pop", t_zap)
BLACKOUT.append((t_rils - 0.05, E(u"телефоні.", 2.29) + 0.05))

# 2 · HALF — two lanes at once, one bracket: 15 хв ----------------------------
h0, h1 = S(u"Так", 3.03) - 0.1, S(u"І якщо", 9.57) - 0.3
HALF.append((h0, h1))
P.append(u'<svg class="sk" id="skP" data-layout-allow-occlusion width="1080" height="1240" viewBox="0 0 1080 1240"></svg>')
t_zmon, t_klod = S(u"змонтоване", 4.25), S(u"Клодом", 5.25)
t_15, t_poky, t_dov = S(u"15", 5.99), S(u"поки я", 7.21), S(u"довге", 8.01)
js(u'''
  sketch("p1", "skP"); box("p1", 90, 300, 260, 140, {seed: 3});
  label("p1", 220, 388, "цей рілс", {size: 54});
  draw("p1", %.3f);
  sketch("p2", "skP"); arrow("p2", 362, 370, 522, 370, {seed: 7, bend: .08});
  box("p2", 530, 300, 355, 140, {seed: 9, fill: true});
  label("p2", 707, 386, "Клод монтує", {size: 48});
  draw("p2", %.3f - .55);
  sketch("p3", "skP"); ln("p3", 920, 310, 920, 630, {stroke: "#7A1424", strokeWidth: 5, seed: 11});
  ln("p3", 898, 310, 920, 310, {stroke: "#7A1424", strokeWidth: 5, seed: 13});
  ln("p3", 898, 630, 920, 630, {stroke: "#7A1424", strokeWidth: 5, seed: 15});
  label("p3", 978, 468, "15", {size: 76, color: "#7A1424"});
  label("p3", 978, 530, "хв", {size: 56, color: "#7A1424"});
  draw("p3", %.3f - .3, .5);
  sketch("p4", "skP"); box("p4", 90, 490, 780, 140, {seed: 17});
  label("p4", 480, 578, "я: довге відео з поясненнями", {size: 50});
  draw("p4", %.3f);
  erase("p1", %.3f); erase("p2", %.3f); erase("p3", %.3f); erase("p4", %.3f);
''' % (t_tse, t_klod, t_15, t_poky, h1, h1, h1, h1))
g.sfx("whoosh-short", h0); g.sfx("whoosh-short", h1)
for t in (t_tse, t_klod, t_15, t_poky):
    g.sfx("click-soft", t)
BLACKOUT.append((t_klod - 0.05, E(u"Клодом", 5.25) + 0.05))
BLACKOUT.append((t_15 - 0.05, E(u"хвилин,", 6.45) + 0.05))
BLACKOUT.append((t_dov - 0.05, E(u"поясненнями.", 8.81) + 0.05))

# 3 · ABOVE — the system, against a course, SMM, lost time ---------------------
t_inv, t_sys = S(u"інвестувати", 10.96), S(u"систему,", 11.86)
t_kurs, t_smm, t_chas = S(u"курс", 13.46), S(u"SMM", 14.58), S(u"профукати", 15.64)
t_to = S(u"то", 16.73)
CH = u'style="font-size:34px; padding:12px 20px"'
F.append(u'''
        <div id="b3" style="position:absolute; left:90px; width:900px; top:288px;
             display:flex; gap:16px; justify-content:center; align-items:center">
          <span class="chip hid" id="b3a" style="font-size:42px; padding:14px 26px"><i></i>інвестувати</span>
          <svg id="b3r" class="hid" width="70" height="40" viewBox="0 0 70 40"><path d="M4 20 H58 M44 6 L60 20 L44 34"
               fill="none" stroke="#7A1424" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>
          <span class="chip on hid" id="b3b" style="font-size:42px; padding:14px 26px; gap:12px">%s в систему</span>
        </div>
        <div id="b4" style="position:absolute; left:90px; width:900px; top:400px;
             display:flex; gap:14px; justify-content:center">
          <span class="chip hid" id="b4a" %s><i></i>курс по блогінгу<b class="st"></b></span>
          <span class="chip hid" id="b4b" %s><i></i>SMM<b class="st"></b></span>
          <span class="chip hid" id="b4c" %s><i></i>профукати час<b class="st"></b></span>
        </div>''' % (mark("claude", 40), CH, CH, CH))
js(u'''
  pop("#b3a", %.3f); pop("#b3r", %.3f, .4); pop("#b3b", %.3f);
  pop("#b4a", %.3f); pop("#b4b", %.3f); pop("#b4c", %.3f);
  tl.fromTo("#b4a .st", {scaleX: 0}, X({scaleX: 1, duration: .3, ease: "power2.out"}), %.3f);
  tl.fromTo("#b4b .st", {scaleX: 0}, X({scaleX: 1, duration: .3, ease: "power2.out"}), %.3f);
  tl.fromTo("#b4c .st", {scaleX: 0}, X({scaleX: 1, duration: .3, ease: "power2.out"}), %.3f);
  sink("#b3a, #b3r, #b3b, #b4a, #b4b, #b4c", %.3f);
''' % (t_inv, t_sys - 0.3, t_sys, t_kurs, t_smm, t_chas,
       t_kurs + 0.6, t_smm + 0.35, E(u"час,", 16.22) - 0.1, t_to - 0.2))
g.sfx("pop", t_inv); g.sfx("pop", t_sys)
for t in (t_kurs, t_smm, t_chas):
    g.sfx("click-soft", t)
BLACKOUT.append((t_inv - 0.05, E(u"систему,", 11.86) + 0.05))
BLACKOUT.append((t_kurs - 0.05, E(u"час,", 16.22) + 0.05))
STRIKE_CSS = u'''
    .chip { position: relative; }
    .chip .st { position: absolute; left: 10px; right: 10px; top: 50%; height: 5px; margin-top: -2px;
                border-radius: 3px; background: #7A1424; transform-origin: 0 50%; transform: scaleX(0); }'''

# 4 · ABOVE — CTA: the button under this video ---------------------------------
t_nat, t_knop = S(u"натискай", 16.85), S(u"кнопку", 17.53)
F.append(u'''
        <div id="b5" class="pill hid" style="left:0; right:0; margin:auto; width:max-content; top:282px;
             padding:28px 54px; font-size:50px;">Натискай кнопку під відео</div>''')
js(u'''
  pop("#b5", %.3f, .6);
  // the button is under the video: the pointer goes straight down, left of her
  sketch("a5", "skF"); arrow("a5", 215, 440, 185, 1490, {strokeWidth: 5, seed: 97, bend: -.06});
  draw("a5", %.3f, .55);
  sketch("a5t", "skF"); label("a5t", 300, 1460, "тут", {size: 56, anchor: "start"});
  draw("a5t", %.3f);
''' % (t_nat, t_knop - 0.5, t_knop + 0.1))
g.sfx("pop", t_nat); g.sfx("whoosh-short", t_knop - 0.5)
BLACKOUT.append((t_nat - 0.05, DUR))     # the pill says it

# ---------------------------------------------------------------- mattes for the half screens
for i, (a, b) in enumerate(HALF):
    g.matte("half%d" % (i + 1), round(a - 0.1, 3), round(b - a + 1.2, 3))
    js("  half(%.3f, %.3f);" % (a, b))
    PLACE.append((a + 0.4, b + 0.2, "bottom", 980))


def main():
    chunks = g.chunks(CAPS, place=PLACE)
    doc = g.document(title=u"Reel 54 — Це відео змонтував мій Клод", plate="assets/base.mp4",
                     behind="\n".join(B), panel="\n".join(P), front="\n".join(F), cover="\n".join(C),
                     js="\n".join(J), chunks=chunks, blackout=BLACKOUT, extra_css=STRIKE_CSS)
    g.write(HERE, doc)
    print("index.html  %d caption chunks, %d sfx cues, %d mattes" % (len(chunks), len(g.cues), len(g.mattes)))


main()
