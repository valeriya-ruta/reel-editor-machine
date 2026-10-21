# -*- coding: utf-8 -*-
"""Reel 44 — «Дзвінок → пропозиція». Posts 2026-10-20.

Google style + Excalidraw (STYLE.md §00), cut from her raw take by tools/cut.py
(work/r44/cut-fix.json). She rewrote the close on camera: a €15 instruction and
«пиши слово «дзвінок»» — her wording stands.

The one object is **the call**: a video-call card with her and a client in it.
The AI tools get crossed out, «дзвінки» stands behind her, the call opens, the
client's questions pop out of it, one question becomes many people becomes a
topic; the content plan has holes, a weekly routine eats content, competitors
and the calls, and the holes fill with call ideas that underline the strategy.
Then: all her clients have it, the €15 instruction, and the CTA.

  above   ideas card: ChatGPT / Claude / Manus light up and get struck out
  behind  «дзвінки» (she leans in)
  above   the call card: Рута + клієнтка, Fathom REC; консультація, велкам-дзвінок;
          question bubbles from the client; «?!» on her side
  half    one person asks -> many people -> «ідеальна тема»
  above   content plan: strategy reels with CTA, empty «?» days
  above   a thought cloud over her head, crossed out
  half    the routine, weekly; my content, competitors, the calls
  above   the plan again: the holes fill with call ideas, a red underline
          under the strategy
  above   all her clients: checks, hearts
  above   the instruction card, €15, two steps
  above   CTA chips -> «Пиши «дзвінок»» pill + pointer -> instruction chip

usage: python build.py
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
from gstyle import G, Words, load_caps, mark, esc  # noqa: E402

NN = "44"
DUR = 59.550           # (1787 plate frames - 0.5) / 30
g = G(dur=DUR, reel=NN)

# whisper's spelling of what she plainly said -> her word (re-heard on the plate)
FIX = {
    (u"великим", 9.3): u"велкам", u"на великим": u"на велкам", u"З консультацій": u"З консультацією,", u"і вони": u"вони",
    u"б,": u"б", u"саджу": u"сиджу", u"Усім": u"усім", u"інструція": u"інструкція",
    u"15 євро.": u"15 євро,", (u"А", 49.3): u"я", u"консультації": u"консультації,",
    u"Тобі": u"тобі", u"«цвінок».": u"«дзвінок»,", (u"в", 58.7): None,
}
CAPS = load_caps(NN, FIX)
W = Words(CAPS)
S, E = W.s, W.e

# Material icons (24-grid), filled in currentColor
ICON = {
    "call": "M20.01 15.38c-1.23 0-2.42-.2-3.53-.56-.35-.12-.74-.03-1.01.24l-1.57 1.97c-2.83-1.35-5.48-3.9-6.89-6.83"
            "l1.95-1.66c.27-.28.35-.67.24-1.02-.37-1.11-.56-2.3-.56-3.53 0-.54-.45-.99-.99-.99H4.19C3.65 3 3 3.24 3 3.99"
            " 3 13.28 10.73 21 20.01 21c.71 0 .99-.63.99-1.18v-3.45c0-.54-.45-.99-.99-.99z",
    "doc": "M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2z"
           "m-3-5V3.5L18.5 9H13z",
    "heart": "M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3"
             " 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z",
    "person": "M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z",
    "play": "M8 5v14l11-7z",
    "bulb": "M9 21c0 .55.45 1 1 1h4c.55 0 1-.45 1-1v-1H9v1zm3-19C8.14 2 5 5.14 5 9c0 2.38 1.19 4.47 3 5.74V17c0 .55.45 1"
            " 1 1h6c.55 0 1-.45 1-1v-2.26c1.81-1.27 3-3.36 3-5.74 0-3.86-3.14-7-7-7z",
}


def ico(name, size, color="currentColor", extra=""):
    return ('<svg width="%d" height="%d" viewBox="0 0 24 24" style="flex:none;%s"><path fill="%s" d="%s"/></svg>'
            % (size, size, extra, color, ICON[name]))


EXTRA_CSS = u"""
    .chip.ghost { opacity: .32; filter: grayscale(1); }
    .tile { position: relative; border-radius: 26px; background: #FFF0F0; overflow: hidden; }
    .tile .nm { position: absolute; left: 18px; bottom: 14px; font-size: 26px; font-weight: 500;
                color: #574142; background: rgba(255,255,255,.85); border-radius: 10px; padding: 2px 12px; }
    .tile .av { position: absolute; left: 50%; top: 50%; width: 112px; height: 112px; margin: -64px 0 0 -56px;
                border-radius: 50%; background: #fff; display: flex; align-items: center; justify-content: center;
                color: #7A1424; }
    .bub { position: absolute; width: 78px; height: 66px; border-radius: 22px 22px 22px 6px; background: #fff;
           box-shadow: 0 1px 3px rgba(36,25,25,.12), 0 6px 16px rgba(36,25,25,.14);
           font-weight: 700; font-size: 44px; color: #7A1424; display: flex; align-items: center;
           justify-content: center; }
    .rec { display: inline-flex; align-items: center; gap: 10px; font-size: 26px; font-weight: 500; color: #7A1424; }
    .rec b { width: 16px; height: 16px; border-radius: 50%; background: #7A1424; display: inline-block; }
    .day { position: relative; width: 98px; height: 150px; border-radius: 20px; border: 3px dashed #DEBFBF;
           background: #fff; display: flex; flex-direction: column; align-items: center; padding-top: 12px;
           font-size: 26px; font-weight: 500; color: #574142; }
    .day .q { margin-top: 18px; font-size: 52px; font-weight: 700; color: #DEBFBF; line-height: 1; }
    .day .st, .day .ex { position: absolute; inset: -3px; border-radius: 20px; display: flex; flex-direction: column;
                         align-items: center; padding-top: 15px; font-size: 26px; font-weight: 500; }
    .day .st { background: #7A1424; color: #fff; }
    .day .ex { background: #FFF0F0; color: #7A1424; border: 3px solid #7A1424; }
    .day .tag { margin-top: 14px; font-size: 20px; font-weight: 700; letter-spacing: .04em; border-radius: 8px;
                padding: 3px 8px; background: #fff; color: #7A1424; }
    .day .ex .tag { background: #7A1424; color: #fff; }
    .avc { width: 118px; height: 118px; border-radius: 50%; background: #FFF0F0; display: flex; align-items: center;
           justify-content: center; color: #7A1424; position: relative; }
    .avc .check { position: absolute; right: -8px; bottom: -8px; }
    .avc .hrt { position: absolute; left: 50%; top: -58px; margin-left: -22px; }
"""

# ---------------------------------------------------------------- the beats
B, P, F, C, J = [], [], [], [], []     # behind / panel / front / cover html, js
BLACKOUT = []
PLACE = []                             # caption placement over the half screens
HALF = []


def js(s):
    J.append(s)


F.append(u'<svg class="sk" id="skF" width="1080" height="1920" viewBox="0 0 1080 1920"></svg>')

# 1 · ABOVE — the best ideas are not from ChatGPT, Claude or Manus -------------
t_id, t_gpt, t_cl, t_man = S(u"ідеї", 0.89), S(u"GPT,", 2.72), S(u"Клода", 3.59), S(u"Мануса.", 4.29)
t_ya = S(u"Я", 5.0)
BR = [(u"gpt", mark("openai", 36) + u"ChatGPT"), (u"cl", mark("claude", 36) + u"Claude"),
      (u"man", u'<b style="font-weight:700;letter-spacing:-0.02em">Manus</b>')]
F.append(u'''
        <div id="b1" class="card hid" style="left:120px; top:312px; width:840px; padding:34px 36px;">
          <span class="lbl">Ідеї для контенту</span>
          <div class="chips" style="justify-content:center; flex-wrap:nowrap">%s</div>
        </div>''' % u"".join(
    u'<span class="chip ghost" id="b1%s" style="position:relative; width:244px; justify-content:center; font-size:34px">%s'
    u'<svg class="sk" id="skx%s" width="244" height="80" viewBox="0 0 244 80" style="left:-2px; top:-4px"></svg></span>'
    % (k, h, k) for k, h in BR))
js(u'''
  rise("#b1", %.3f);
  function lit(sel, t) { tl.to(sel, {opacity: 1, filter: "grayscale(0)", duration: .2}, t);
    tl.fromTo(sel, {scale: .82}, X({scale: 1, duration: .5, ease: POP}), t); }
  lit("#b1gpt", %.3f); lit("#b1cl", %.3f); lit("#b1man", %.3f);
  sketch("xgpt", "skxgpt"); ln("xgpt", 14, 58, 232, 22, {stroke: "#7A1424", strokeWidth: 6, seed: 3}); draw("xgpt", %.3f, .3);
  sketch("xcl", "skxcl"); ln("xcl", 14, 56, 232, 24, {stroke: "#7A1424", strokeWidth: 6, seed: 5}); draw("xcl", %.3f, .3);
  sketch("xman", "skxman"); ln("xman", 14, 58, 232, 20, {stroke: "#7A1424", strokeWidth: 6, seed: 9}); draw("xman", %.3f, .3);
  sink("#b1", %.3f);
''' % (t_id - 0.3, t_gpt - 0.35, t_cl - 0.1, t_man - 0.1,
       t_gpt + 0.2, t_cl + 0.35, t_man + 0.4, t_ya - 0.3))
g.sfx("pop", t_id - 0.3)
g.sfx("click-soft", t_gpt + 0.2); g.sfx("click-soft", t_man + 0.4)

# 2 · BEHIND — «дзвінки» (she leans in, hair top 556-590 here: one line at top 400
#     puts the baseline at ≈ 590, so her hair takes the bottom ~15 % of the letters)
t_dz = S(u"з дзвінків", 5.7)
bw0, bw1 = t_dz - 0.35, t_dz + 0.85
B.append(u'<div id="bw" class="big hid" style="top:400px; font-size:240px">дзвінки</div>')
g.matte("dzv", round(bw0 - 0.05, 3), round(bw1 - bw0 + 0.5, 3))
js(u'''
  rise("#bw", %.3f, 80);
  sink("#bw", %.3f);
''' % (bw0, bw1))
g.sfx("whoosh-short", bw0)
BLACKOUT.append((S(u"Я", 5.0) - 0.05, S(u"Я", 5.0) + 0.05))     # «дзвінки» stands behind her

# 3 · ABOVE — the call: her and a client, recorded; consultations, welcome calls --
t_pro, t_kli = S(u"проводжу", 6.77), S(u"клієнтками.", 7.43)
t_kons, t_vel, t_vel2 = S(u"З консультацією,", 8.19), S(u"велкам", 9.27), S(u"на велкам", 11.63)
t_zad, t_pyt = S(u"мені задають", 12.55), S(u"питання,", 12.91)
t_nik, t_dod = S(u"ніколи", 15.31), E(u"додумалась.", 15.83)
F.append(u'''
        <div id="b3" class="card hid" style="left:120px; top:292px; width:840px; padding:26px 36px 28px;">
          <div class="row" style="justify-content:space-between; margin-bottom:18px">
            <span class="row" style="gap:12px; font-size:32px; font-weight:700; color:#241919">%s Дзвінок</span>
            <span class="rec"><b></b>REC · %s Fathom</span>
          </div>
          <div class="row" style="gap:24px">
            <div class="tile" style="width:372px; height:176px"><span class="av">%s</span><span class="nm">Рута</span></div>
            <div class="tile" style="width:372px; height:176px"><span class="av hid" id="b3av">%s</span>
              <span class="nm hid" id="b3nm">клієнтка</span></div>
          </div>
          <div class="chips" style="margin-top:18px; justify-content:center">
            <span class="chip hid" id="b3k" style="font-size:30px; padding:10px 20px"><i></i>консультація</span>
            <span class="chip hid" id="b3w" style="font-size:30px; padding:10px 20px"><i></i>велкам-дзвінок</span>
          </div>
        </div>
        <div id="b3q1" class="bub hid" style="left:818px; top:388px">?</div>
        <div id="b3q2" class="bub hid" style="left:836px; top:466px">?</div>
        <div id="b3q3" class="bub hid" style="left:574px; top:394px">?</div>
        <div id="b3x" class="hand hid" style="left:404px; top:378px; font-size:64px; color:#7A1424">?!</div>''' % (
    ico("call", 34, "#7A1424"), mark("fathom", 26), ico("person", 84), ico("person", 84)))
js(u'''
  rise("#b3", %.3f);
  pop("#b3av", %.3f); fadein("#b3nm", %.3f);
  pop("#b3k", %.3f); pop("#b3w", %.3f);
  sketch("c3", "skF"); ell("c3", 682, 606, 340, 100, {stroke: "#7A1424", strokeWidth: 5, seed: 23});
  draw("c3", %.3f, .55);
  tl.set("#b3w", {className: "chip on"}, %.3f);
  pop("#b3q1", %.3f); pop("#b3q2", %.3f); pop("#b3q3", %.3f);
  erase("c3", %.3f);
  pop("#b3x", %.3f, .5);
  sink("#b3, #b3q1, #b3q2, #b3q3, #b3x", %.3f);
''' % (t_pro - 0.25, t_kli, t_kli + 0.1, t_kons, t_vel, t_vel2 - 0.35, t_vel2,
       t_zad, t_pyt, t_pyt + 0.4, t_zad - 0.1, t_nik, t_dod + 0.05))
g.sfx("pop", t_pro - 0.25); g.sfx("click-soft", t_vel)
g.sfx("notification", t_zad); g.sfx("pop", t_nik)

# 4 · HALF — one person asks -> it is many people -> the ideal topic -----------
h0, h1 = S(u"Але", 16.6) - 0.1, S(u"Тому", 23.58) - 0.1
HALF.append((h0, h1))
P.append(u'<svg class="sk" id="skP" width="1080" height="1240" viewBox="0 0 1080 1240"></svg>')
t_raz, t_tak = S(u"раз", 17.02), S(u"такі", 17.96)
t_tsik, t_odnu, t_lud = S(u"цікавить", 19.12), S(u"одну", 19.98), S(u"людину,", 20.18)
t_vyh, t_ide, t_tema = S(u"виходить", 21.26), S(u"ідеальна", 21.86), S(u"тема", 22.56)


def bust(x, y, s=1.0):
    """a person: a round head and a shoulders arc, as one rough path"""
    r, w, h = 30 * s, 62 * s, 74 * s
    return (u"M%.0f %.0f a%.0f %.0f 0 1 0 %.0f 0 a%.0f %.0f 0 1 0 %.0f 0 "
            u"M%.0f %.0f C%.0f %.0f %.0f %.0f %.0f %.0f" % (
                x - r, y, r, r, 2 * r, r, r, -2 * r,
                x - w, y + h + 36 * s, x - w, y + 40 * s, x + w, y + 40 * s, x + w, y + h + 36 * s))


js(u'''
  sketch("p1", "skP");
  _add(SK.p1, SK.p1.rc.path("%s", opt({seed: 31}, 31)));
  draw("p1", %.3f, .7);
  sketch("p2", "skP"); box("p2", 250, 300, 96, 84, {seed: 33, r: 26}); label("p2", 298, 362, "?", {size: 56, color: "#7A1424"});
  draw("p2", %.3f, .45);
  sketch("p3", "skP"); ell("p3", 180, 430, 220, 260, {stroke: "#7A1424", strokeWidth: 5, seed: 35});
  draw("p3", %.3f, .5);
  sketch("p4", "skP"); arrow("p4", 330, 440, 460, 440, {seed: 37, bend: .08});
  %s
  label("p4", 560, 372, "?", {size: 48, color: "#7A1424"}); label("p4", 665, 372, "?", {size: 48, color: "#7A1424"});
  label("p4", 770, 372, "?", {size: 48, color: "#7A1424"}); label("p4", 875, 372, "?", {size: 48, color: "#7A1424"});
  draw("p4", %.3f, .3);
  sketch("p5", "skP"); arrow("p5", 717, 545, 620, 640, {seed: 41, bend: -.1});
  box("p5", 260, 650, 560, 160, {seed: 43, fill: true, r: 30});
  label("p5", 540, 722, "ідеальна тема", {size: 56, color: "#7A1424"});
  label("p5", 540, 782, "для контенту", {size: 44});
  draw("p5", %.3f, .5);
  erase("p1", %.3f); erase("p2", %.3f); erase("p3", %.3f); erase("p4", %.3f); erase("p5", %.3f);
''' % (bust(180, 410, 1.15), t_raz - 0.1, t_tak, t_odnu - 0.45,
       u"\n  ".join(u'_add(SK.p4, SK.p4.rc.path("%s", opt({seed: %d}, %d)));' % (bust(x, 420, .85), 50 + i, 50 + i)
                    for i, x in enumerate((560, 665, 770, 875))),
       t_lud - 0.6, t_vyh - 0.2, h1, h1, h1, h1, h1))
g.sfx("click-soft", t_lud); g.sfx("pop", t_ide)
g.sfx("whoosh-short", h0); g.sfx("whoosh-short", h1)

# 5 · ABOVE — the content plan: strategy reels with a CTA, empty days ----------
t_nap, t_kp, t_chy = S(u"наповнити", 24.48), S(u"контент-план", 24.92), S(u"чимось,", 25.48)
t_ril, t_str, t_zak = S(u"рілсів", 26.18), S(u"стратегії", 26.84), S(u"закликами", 27.74)
DAYS = [u"Пн", u"Вт", u"Ср", u"Чт", u"Пт", u"Сб", u"Нд"]
STRAT = (0, 2, 4)


def plan_html(pid):
    tiles = []
    for i, d in enumerate(DAYS):
        if i in STRAT:
            inner = (u'<span class="st hid" id="%sst%d">%s%s<span class="tag hid" id="%sct%d">CTA</span></span>'
                     % (pid, i, d, ico("play", 40, "#fff", "margin-top:6px"), pid, i))
        else:
            inner = (u'<span class="q hid" id="%sq%d">?</span>'
                     u'<span class="ex hid" id="%sex%d">%s%s<span class="tag">ідея</span></span>'
                     % (pid, i, pid, i, d, ico("call", 34, "#7A1424", "margin-top:8px")))
        tiles.append(u'<div class="day" id="%sd%d">%s%s</div>' % (pid, i, d, inner))
    return (u'''
        <div id="%s" class="card hid" style="left:120px; top:312px; width:840px; padding:30px 40px 32px;">
          <span class="lbl">Контент-план</span>
          <div class="row" style="gap:12px">%s</div>
          <div class="chips" style="margin-top:36px; justify-content:center">
            <span class="chip hid" id="%sls" style="font-size:28px; padding:8px 18px"><i></i>стратегія з CTA</span>
            <span class="chip hid" id="%slx" style="font-size:28px; padding:8px 18px">%s ідеї з дзвінків</span>
          </div>
        </div>''' % (pid, u"".join(tiles), pid, pid, ico("call", 26, "#7A1424")))


F.append(plan_html(u"b5"))
js(u'''
  rise("#b5", %.3f);
  %s
  %s
  %s
  pop("#b5ls", %.3f);
  sink("#b5", %.3f);
''' % (t_nap - 0.2,
       u" ".join(u'pop("#b5q%d", %.3f, .45);' % (i, t_chy + 0.08 * n) for n, i in enumerate((1, 3, 5, 6))),
       u" ".join(u'pop("#b5st%d", %.3f, .5);' % (i, t_ril - 0.1 + 0.18 * n) for n, i in enumerate(STRAT)),
       u" ".join(u'pop("#b5ct%d", %.3f, .45);' % (i, t_zak + 0.12 * n) for n, i in enumerate(STRAT)),
       t_str, E(u"дії,", 28.44) + 0.15))
g.sfx("pop", t_nap - 0.2); g.sfx("pop", t_ril); g.sfx("click-soft", t_zak)

# 6 · ABOVE — not out of my head: a thought cloud over her, crossed out --------
t_sy, t_vyg, t_hol = S(u"сиджу", 29.23), S(u"вигадую", 29.71), E(u"голови.", 30.18)
js(u'''
  sketch("cl6", "skF");
  _add(SK.cl6, SK.cl6.rc.path("M400 560 C330 560 320 480 395 468 C390 400 480 375 525 420 C555 350 680 355 700 425 C770 400 840 455 805 515 C860 540 830 600 760 590 C730 625 640 620 615 590 C580 625 470 620 450 585 C430 590 410 580 400 560 Z", opt({seed: 61}, 61)));
  ell("cl6", 560, 640, 46, 34, {seed: 63}); ell("cl6", 540, 688, 26, 20, {seed: 65});
  label("cl6", 590, 520, "?", {size: 72});
  draw("cl6", %.3f, .55);
  sketch("x6", "skF"); ln("x6", 390, 390, 830, 620, {stroke: "#7A1424", strokeWidth: 7, seed: 67});
  ln("x6", 830, 380, 400, 630, {stroke: "#7A1424", strokeWidth: 7, seed: 69});
  draw("x6", %.3f, .3);
  erase("cl6", %.3f); erase("x6", %.3f);
''' % (t_sy - 0.45, t_vyg, t_hol + 0.12, t_hol + 0.12))
g.sfx("click-soft", t_vyg)

# 7 · HALF — the routine, weekly: my content, competitors, and the calls --------
h2, h3 = S(u"У", 30.68) - 0.15, S(u"І", 36.6) - 0.1
HALF.append((h2, h3))
t_rut, t_tyzh, t_ana = S(u"рутина,", 31.2), S(u"кожного", 32.28), S(u"аналізує", 33.14)
t_kont, t_konk, t_dzv = S(u"контент", 34.06), S(u"конкурентів,", 34.9), S(u"дзвінки.", 35.95)
P.append(u'''
        <div id="p7f" class="hid" style="position:absolute; left:740px; top:686px; color:#7A1424">%s</div>''' % mark("fathom", 40))
js(u'''
  sketch("r1", "skP"); ell("r1", 540, 410, 400, 190, {seed: 71});
  arrow("r1", 700, 500, 625, 512, {seed: 73, bend: .05});
  label("r1", 540, 428, "рутина", {size: 56});
  draw("r1", %.3f, .7);
  sketch("r2", "skP"); label("r2", 860, 330, "щотижня", {size: 46, color: "#7A1424"});
  under("r2", 770, 348, 950, {stroke: "#7A1424", seed: 75});
  draw("r2", %.3f, .45);
  sketch("r3", "skP"); box("r3", 95, 640, 270, 130, {seed: 77}); label("r3", 230, 720, "мій контент", {size: 44});
  arrow("r3", 260, 630, 380, 500, {seed: 79});
  draw("r3", %.3f, .45);
  sketch("r4", "skP"); box("r4", 405, 640, 270, 130, {seed: 81}); label("r4", 540, 720, "конкуренти", {size: 44});
  arrow("r4", 540, 630, 540, 520, {seed: 83, bend: 0});
  draw("r4", %.3f, .45);
  sketch("r5", "skP"); box("r5", 715, 640, 270, 130, {seed: 85, stroke: "#7A1424", strokeWidth: 5.5, fill: true});
  label("r5", 875, 722, "дзвінки", {size: 50, color: "#7A1424"});
  arrow("r5", 820, 630, 700, 505, {seed: 87, stroke: "#7A1424"});
  draw("r5", %.3f, .45);
  fadein("#p7f", %.3f);
  erase("r1", %.3f); erase("r2", %.3f); erase("r3", %.3f); erase("r4", %.3f); erase("r5", %.3f);
  tl.to("#p7f", {autoAlpha: 0, duration: .3}, %.3f);
''' % (t_rut - 0.35, t_tyzh, t_kont - 0.35, t_konk - 0.35, t_dzv - 0.4, t_dzv + 0.1,
       h3, h3, h3, h3, h3, h3))
g.sfx("whoosh-short", h2); g.sfx("whoosh-short", h3)
g.sfx("click-soft", t_konk)
g.sfx("pop", t_dzv)

# 8 · ABOVE — the plan again: the empty days fill with call ideas; the strategy
#     gets underlined («підкреслює») -----------------------------------------
t_stv, t_dod2 = S(u"створює", 37.39), S(u"додатковий", 37.85)
t_pid, t_mst = S(u"підкреслює", 38.95), S(u"стратегію.", 40.13)
F.append(plan_html(u"b8"))
js(u'''
  %s %s %s
  tl.set("#b8ls", {autoAlpha: 1}, 0);
  rise("#b8", %.3f);
  %s
  pop("#b8lx", %.3f);
  sketch("u8", "skF");
  under("u8", 154, 566, 264, {stroke: "#7A1424", strokeWidth: 7, seed: 91});
  under("u8", 374, 568, 484, {stroke: "#7A1424", strokeWidth: 7, seed: 93});
  under("u8", 594, 566, 704, {stroke: "#7A1424", strokeWidth: 7, seed: 95});
  draw("u8", %.3f, .3);
  %s
  sink("#b8", %.3f); erase("u8", %.3f);
''' % (u" ".join(u'tl.set("#b8st%d, #b8ct%d", {autoAlpha: 1}, 0);' % (i, i) for i in STRAT),
       u" ".join(u'tl.set("#b8q%d", {autoAlpha: 1}, 0);' % i for i in (1, 3, 5, 6)), u"",
       h3 + 0.35,
       u" ".join(u'tl.set("#b8q%d", {autoAlpha: 0}, %.3f); pop("#b8ex%d", %.3f, .5);'
                 % (i, t_dod2 - 0.05 + 0.15 * n, i, t_dod2 - 0.05 + 0.15 * n) for n, i in enumerate((1, 3, 5, 6))),
       t_dod2 + 0.3, t_pid - 0.1,
       u" ".join(u'pop("#b8st%d", %.3f, .45);' % (i, t_mst - 0.15 + 0.1 * n) for n, i in enumerate(STRAT)),
       E(u"стратегію.", 40.13) + 0.2, E(u"стратегію.", 40.13) + 0.2))
g.sfx("click-soft", t_dod2); g.sfx("click-soft", t_pid)

# 9 · ABOVE — all her clients have it, and love it -----------------------------
t_usim, t_klk = S(u"усім", 41.29), S(u"клієнткам", 41.73)
t_vpr, t_nal, t_zakh = S(u"впроваджую", 42.69), S(u"налаштування,", 43.49), S(u"захваті.", 44.85)
NCL = 5
F.append(u'''
        <div id="b9" class="card hid" style="left:120px; top:320px; width:840px; padding:30px 40px 40px;">
          <span class="lbl">Мої клієнтки</span>
          <div class="row" style="gap:36px; justify-content:center; margin-top:62px">%s</div>
        </div>''' % u"".join(
    u'<div class="avc hid" id="b9a%d">%s<span class="check hid" id="b9k%d"></span>'
    u'<span class="hrt hid" id="b9h%d">%s</span></div>' % (i, ico("person", 76), i, i, ico("heart", 44, "#7A1424"))
    for i in range(NCL)))
js(u'''
  rise("#b9", %.3f);
  %s
  %s
  %s
  sink("#b9", %.3f);
''' % (t_usim - 0.3,
       u" ".join(u'pop("#b9a%d", %.3f, .45);' % (i, t_klk - 0.2 + 0.1 * i) for i in range(NCL)),
       u" ".join(u'tl.set("#b9k%d", {className: "check on"}, 0); pop("#b9k%d", %.3f, .4);'
                 % (i, i, t_vpr + 0.2 + 0.15 * i) for i in range(NCL)),
       u" ".join(u'pop("#b9h%d", %.3f, .5);' % (i, t_zakh - 0.2 + 0.08 * i) for i in range(NCL)),
       E(u"захваті.", 44.85) + 0.2))
g.sfx("pop", t_usim - 0.3); g.sfx("click-soft", t_vpr + 0.2); g.sfx("pop", t_zakh - 0.2)

# 10 · ABOVE — the instruction, €15, how to set it up and connect it -----------
t_tsil, t_15 = S(u"ціла", 46.44), S(u"15 євро,", 48.52)
t_pok, t_nl, t_pk = S(u"показую,", 49.51), S(u"налаштувати", 50.23), S(u"підключити", 50.97)
F.append(u'''
        <div id="b10" class="card hid" style="left:120px; top:312px; width:840px; padding:34px 40px;">
          <div class="row" style="gap:18px">%s<span class="ttl" style="font-size:58px">Інструкція</span></div>
          <div class="row" style="margin-top:30px"><span class="check" id="b10k1"></span>
            <span style="font-size:40px; font-weight:500">налаштувати</span></div>
          <div class="row" style="margin-top:18px"><span class="check" id="b10k2"></span>
            <span style="font-size:40px; font-weight:500">підключити для себе</span></div>
        </div>
        <div id="b10p" class="pill hid" style="left:690px; top:276px; font-weight:700; font-size:56px; padding:22px 44px">€15</div>''' % ico("doc", 64, "#7A1424"))
js(u'''
  rise("#b10", %.3f);
  pop("#b10p", %.3f, .6);
  tl.set("#b10k1", {className: "check on"}, %.3f); pop("#b10k1", %.3f, .4);
  tl.set("#b10k2", {className: "check on"}, %.3f); pop("#b10k2", %.3f, .4);
  sink("#b10, #b10p", %.3f);
''' % (t_tsil - 0.3, t_15, t_nl, t_nl, t_pk, t_pk, E(u"себе.", 51.67) + 0.2))
g.sfx("pop", t_tsil - 0.3); g.sfx("kaching", t_15); g.sfx("click-soft", t_nl)

# 11 · ABOVE — CTA: if you run consultations and need ideas -> write «дзвінок» --
t_kons2, t_idei2 = S(u"консультації,", 54.29), S(u"ідеї", 55.99)
t_pys, t_dzv2, t_instr = S(u"то пиши", 56.89), S(u"«дзвінок»,", 57.35), S(u"інструкцію.", 58.84)
F.append(u'''
        <div id="b11" style="position:absolute; left:110px; top:318px; width:860px;
             display:flex; gap:14px; justify-content:center">
          <span class="chip hid" id="b11a">%s консультації</span>
          <span class="chip hid" id="b11b">%s ідеї для контенту</span>
        </div>
        <div id="b11cta" class="pill hid" style="left:0; top:430px; left:50%%; margin-left:-265px; width:530px;
             justify-content:center; font-size:54px; padding:28px 40px">Пиши «дзвінок»</div>
        <div id="b11i" class="pill light hid" style="left:50%%; margin-left:-170px; width:340px; top:572px;
             justify-content:center; font-size:38px; padding:18px 30px">%s інструкція</div>''' % (
    ico("call", 34, "#7A1424"), ico("bulb", 36, "#7A1424"), ico("doc", 40, "#7A1424")))
js(u'''
  pop("#b11a", %.3f); pop("#b11b", %.3f);
  pop("#b11cta", %.3f, .6);
  sketch("a11", "skF"); arrow("a11", 930, 690, 840, 545, {stroke: "#7A1424", strokeWidth: 5.5, seed: 97});
  draw("a11", %.3f, .45);
  pop("#b11i", %.3f, .55);
''' % (t_kons2 - 0.1, t_idei2 - 0.1, t_dzv2 - 0.2, t_dzv2 + 0.4, S(u"отримати", 58.32)))
g.sfx("pop", t_kons2 - 0.1); g.sfx("pop", t_dzv2 - 0.2); g.sfx("pop", S(u"отримати", 58.32))
BLACKOUT.append((t_pys - 0.05, DUR))     # the pill and the chip say it

# ---------------------------------------------------------------- mattes for the half screens
for i, (a, b) in enumerate(HALF):
    g.matte("half%d" % (i + 1), round(a - 0.1, 3), round(b - a + 1.2, 3))
    js("  half(%.3f, %.3f);" % (a, b))
    PLACE.append((a + 0.4, b, "bottom", 980))     # not past the exit: she rises into it


def glue(chunks):
    """a lone last word («Мануса.», «голови.», «себе.») goes back on the line it ends"""
    out = []
    for c in chunks:
        p = out[-1] if out else None
        if p and len(c["words"]) == 1 and not re.search(u"[.,!?:;…»]$", p["words"][-1]["w"]) \
                and len(" ".join(w["w"] for w in p["words"] + c["words"])) <= 46:
            p["words"] = p["words"] + c["words"]
            p["e"] = c["e"]
            continue
        out.append(c)
    return out


def main():
    if "--words" in sys.argv:
        print(" ".join(u"%s/%.1f" % (c["w"], c["s"]) for c in CAPS))
    keys = {S(u"ідеї", 0.89): True, S(u"велкам", 9.27): True, S(u"питання,", 12.91): True, S(u"питання,", 18.22): True,
            S(u"одну", 19.98): True, S(u"ідеальна", 21.86): True, S(u"тижня", 32.64): True,
            S(u"дзвінки.", 35.95): True, S(u"впроваджую", 42.69): True, S(u"ідеї", 55.99): True}
    chunks = glue(g.chunks(CAPS, keys=keys, place=PLACE))
    if "--chunks" in sys.argv:
        for n, c in enumerate(chunks):
            print(n, "%.2f-%.2f" % (c["s"], c["e"]), " ".join(w["w"] for w in c["words"]),
                  "| key:", c["words"][c["key"]]["w"] if c["key"] is not None else "-", c["pos"])
    doc = g.document(title=u"Reel 44 — Дзвінок → пропозиція", plate="assets/base.mp4",
                     behind="\n".join(B), panel="\n".join(P), front="\n".join(F), cover="\n".join(C),
                     js="\n".join(J), chunks=chunks, blackout=BLACKOUT, extra_css=EXTRA_CSS)
    g.write(HERE, doc)
    print("index.html  %d caption chunks, %d sfx cues, %d mattes" % (len(chunks), len(g.cues), len(g.mattes)))


main()
