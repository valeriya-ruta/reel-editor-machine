# -*- coding: utf-8 -*-
"""Reel 41 — «Не просто промти». Posts 2026-10-19.

The first reel in her Google style + Excalidraw look (STYLE.md §00), cut from
a tired raw take by tools/cut.py (work/r41/cut-fix.json has every hand call).

The one object is **her setup, taken apart**: what people think it is (a card
of prompts with a price) gets crossed out, then each real part is drawn or
dealt onto the screen in the order she names it, and what is left for the
client is a three-line checklist.

  above   the «набір промтів · $1300» card — crossed out on «зовсім не так»
  half    content -> analysis -> the reels that worked -> «скіл сценариста»,
          «точніше два»
  above   the two skills as cards: carousels / reels / threads; her speech style
  above → behind   three carousel samples -> «дизайн-система» big behind her
  above   the editing card (references -> her style), a cloud, a phone
  above   ten connectors dealt as chips
  full    «проактивна» — the routine loop
  half    Sunday report: three lines, approved, then threads / carousels /
          scripts, and a calendar «наперед»
  above   her part: three checks; everything else: chips
  above   CTA — who it is for, «24/7», «Став + в коментарях»

usage: python build.py      (then render; sfx mix once the kit is here)
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
from gstyle import G, Words, load_caps, mark, esc  # noqa: E402

NN = "41"
CUT = json.load(io.open(os.path.join(ROOT, "work", "r" + NN, "cut.json"), encoding="utf-8"))
DUR = 97.017           # (2911 plate frames - 0.5) / 30
g = G(dur=DUR, reel=NN)

# whisper's spelling of what she plainly said -> her word (checked on the plate)
FIX = {
    u"Думаєш,": u"думаєш,", u"клауді?": u"Клоді,", u"RLC,": u"рілси,", u"до третів": u"до тредів",
    u"З": u"з", (u"не", 45.3): u"налаштовую", u"лоштовий": None, u"виводжився": u"виводжу все",
    u"підлічаючи": u"підключаю ще", u"кожна": u"кожну", u"драться,": u"треди,",
    u"дизайнувати": u"дизайнити", u"сценарі": u"сценарії", u"опровнити": u"опрувнути",
    u"рюсів.": u"рілсів.", u"дизайни,": u"дизайнить,", u"посить,": u"постить,",
    u"клад.": u"Клоді.", (u"і", 88.3): u"І", u"Якщо": u"якщо", u"SMM": u"СММниця",
    u"на ця": None, u"підприємеця": u"підприємиця",
}
FIX[(u"Якщо", 0.0)] = u"Якщо"
CAPS = load_caps(NN, FIX)
W = Words(CAPS)
S, E = W.s, W.e

# ---------------------------------------------------------------- the beats
B, P, F, C, J = [], [], [], [], []     # behind / panel / front / cover html, js
BLACKOUT = []
PLACE = []                             # caption placement over the half screens
HALF = []


def js(s):
    J.append(s)


# 1 · ABOVE — what people think it is ------------------------------------------
t_nab, t_1300, t_zov = S(u"набір", 1.9), S(u"1300", 3.0), S(u"зовсім", 6.85)
F.append(u'''
        <div id="b1" class="card hid" style="left:120px; top:318px; width:840px;">
          <span class="lbl">Набір промтів</span>
          <div class="chips">
            <span class="chip hid" id="b1c1"><i></i>промт для рілсів</span>
            <span class="chip hid" id="b1c2"><i></i>промт для каруселі</span>
            <span class="chip hid" id="b1c3"><i></i>промт для тредів</span>
          </div>
        </div>
        <div id="b1p" class="pill hid" style="left:640px; top:262px;">$1300</div>''')
js(u'''
  rise("#b1", %.3f);
  pop("#b1c1", %.3f); pop("#b1c2", %.3f); pop("#b1c3", %.3f);
  pop("#b1p", %.3f);
  sketch("x1", "skF"); ln("x1", 150, 340, 930, 650, {stroke: "#7A1424", strokeWidth: 6, seed: 3});
  ln("x1", 930, 330, 160, 660, {stroke: "#7A1424", strokeWidth: 6, seed: 5});
  draw("x1", %.3f, .45);
  sink("#b1, #b1p", %.3f); erase("x1", %.3f);
''' % (t_nab - 0.25, t_nab + 0.15, S(u"промтів", 2.2) + 0.05, S(u"промтів", 2.2) + 0.3, t_1300,
       t_zov, E(u"так.", 7.45) + 0.25, E(u"так.", 7.45) + 0.25))
g.sfx("pop", t_nab - 0.2); g.sfx("click-soft", t_1300); g.sfx("whoosh-short", t_zov)
BLACKOUT.append((t_nab - 0.05, t_1300 + 0.6))

# 2 · HALF — content -> analysis -> what worked -> the scriptwriter skill ------
h0, h1 = S(u"Перше,", 8.07) - 0.15, S(u"Один", 19.12) - 0.25
HALF.append((h0, h1))
P.append(u'<svg class="sk" id="skP" width="1080" height="1240" viewBox="0 0 1080 1240"></svg>')
t_kon, t_ana = S(u"контент", 9.7), S(u"аналізую", 11.6)
t_for, t_naik = S(u"формати", 13.0), S(u"найкраще,", 14.6)
t_skil, t_dva = S(u"скіл", 16.4), S(u"два", 18.1)
js(u'''
  sketch("p1", "skP"); box("p1", 90, 300, 340, 170, {seed: 3}); label("p1", 260, 380, "твій контент", {size: 48});
  label("p1", 260, 440, "2–3 місяці", {size: 40, color: "#574142"});
  draw("p1", %.3f);
  sketch("p2", "skP"); arrow("p2", 450, 385, 625, 385, {seed: 7}); box("p2", 640, 300, 350, 170, {seed: 9});
  label("p2", 815, 400, "аналіз", {size: 52});
  draw("p2", %.3f - .55);
  sketch("p3", "skP"); box("p3", 600, 520, 110, 190, {seed: 21, r: 24}); box("p3", 740, 520, 110, 190, {seed: 23, r: 24});
  box("p3", 880, 520, 110, 190, {seed: 25, r: 24, fill: true});
  label("p3", 795, 770, "формати й рілси", {size: 44});
  draw("p3", %.3f, .5);
  sketch("p4", "skP"); ell("p4", 935, 615, 190, 250, {stroke: "#7A1424", strokeWidth: 5, seed: 29});
  draw("p4", %.3f, .6);
  sketch("p5", "skP"); arrow("p5", 585, 640, 425, 640, {seed: 31}); box("p5", 90, 540, 320, 200, {seed: 33, fill: true});
  label("p5", 250, 630, "скіл", {size: 46}); label("p5", 250, 685, "сценариста", {size: 46});
  draw("p5", %.3f - .55);
  sketch("p6", "skP"); label("p6", 250, 805, "точніше — два!", {size: 50, color: "#7A1424"});
  under("p6", 95, 822, 405, {stroke: "#7A1424", seed: 37});
  draw("p6", %.3f, .5);
  erase("p1", %.3f); erase("p2", %.3f); erase("p3", %.3f); erase("p4", %.3f); erase("p5", %.3f); erase("p6", %.3f);
''' % (t_kon, t_ana, t_for, t_naik, t_skil, t_dva, h1, h1, h1, h1, h1, h1))
for t in (t_kon, t_ana, t_for, t_skil):
    g.sfx("click-soft", t)
g.sfx("whoosh-short", h0); g.sfx("whoosh-short", h1)

# 3 · ABOVE — the two skills ---------------------------------------------------
t_odyn, t_kar, t_rils, t_tred = S(u"Один", 19.12), S(u"каруселей,", 23.0), S(u"рілсів,", 23.7), S(u"до тредів", 24.9)
t_insh, t_bud = S(u"інший", 28.1), S(u"будь", 32.5)
F.append(u'''
        <div id="b3a" class="card hid" style="left:96px; top:300px; width:430px; padding:30px 30px;">
          <span class="lbl">Скіл 1</span><span class="ttl" style="font-size:44px">Сценарист</span>
          <div class="chips" style="margin-top:22px; gap:10px">
            <span class="chip hid" id="b3c1" style="font-size:30px; padding:10px 18px"><i></i>каруселі</span>
            <span class="chip hid" id="b3c2" style="font-size:30px; padding:10px 18px"><i></i>рілси</span>
            <span class="chip hid" id="b3c3" style="font-size:30px; padding:10px 18px"><i></i>треди</span>
          </div>
        </div>
        <div id="b3b" class="card hid" style="left:554px; top:300px; width:430px; padding:30px 30px;">
          <span class="lbl">Скіл 2</span><span class="ttl" style="font-size:44px">Твій стиль мовлення</span>
          <div class="chips" style="margin-top:22px">
            <span class="chip on hid" id="b3c4" style="font-size:30px; padding:10px 18px"><i></i>будь-який текст</span>
          </div>
        </div>''')
js(u'''
  rise("#b3a", %.3f); pop("#b3c1", %.3f); pop("#b3c2", %.3f); pop("#b3c3", %.3f);
  rise("#b3b", %.3f); pop("#b3c4", %.3f);
  sink("#b3a, #b3b", %.3f);
''' % (t_odyn, t_kar, t_rils, t_tred, t_insh, t_bud, E(u"стилі.", 34.4) + 0.2))
g.sfx("pop", t_odyn); g.sfx("pop", t_insh)
for t in (t_kar, t_rils, t_tred, t_bud):
    g.sfx("click-soft", t)
BLACKOUT.append((t_kar - 0.05, E(u"до тредів", 24.9) + 0.05))

# 4 · ABOVE → BEHIND — carousel samples, then «дизайн-система» behind her ------
t_diz, t_pryk = S(u"дизайном:", 36.0), S(u"приклади", 36.6)
t_zbyr = S(u"збираю", 39.6)
m0, m1 = t_zbyr - 0.35, E(u"стилі.", 41.9) + 0.6
F.append(u''.join(u'''
        <div id="b4s%d" class="card hid" style="left:%dpx; top:%dpx; width:250px; height:310px; padding:24px;
             transform: rotate(%ddeg)">
          <span style="display:block;height:26px;width:70%%;border-radius:8px;background:#7A1424"></span>
          <span class="line" style="margin-top:22px;width:92%%"></span>
          <span class="line" style="margin-top:14px;width:80%%"></span>
          <span class="line" style="margin-top:14px;width:58%%"></span>
          <span style="display:block;margin-top:24px;height:84px;border-radius:18px;background:#FFF0F0"></span>
        </div>''' % (i, x, y, r) for i, (x, y, r) in enumerate(((150, 330, -6), (415, 300, 2), (680, 330, 7)))))
B.append(u'''
        <div id="bw1" class="big hid" style="top:320px; font-size:240px">дизайн-</div>
        <div id="bw2" class="big hid" style="top:536px; font-size:240px">система</div>''')
g.matte("design", round(m0, 3), round(m1 - m0 + 0.5, 3))
js(u'''
  pop("#b4s0", %.3f); pop("#b4s1", %.3f); pop("#b4s2", %.3f);
  tl.to("#b4s0, #b4s1, #b4s2", {autoAlpha: 0, scale: .4, y: 260, duration: .45, ease: "power2.in", stagger: .06}, %.3f);
  rise("#bw1", %.3f); rise("#bw2", %.3f);
  sink("#bw1, #bw2", %.3f);
''' % (t_pryk, t_pryk + 0.25, t_pryk + 0.5, t_zbyr - 0.4, t_zbyr, t_zbyr + 0.25, m1 - 0.35))
g.sfx("pop", t_pryk); g.sfx("whoosh-short", t_zbyr - 0.3)
BLACKOUT.append((S(u"дизайн-систему,", 39.68) - 0.05, E(u"дизайн-систему,", 39.68) + 0.05))

# 5 · ABOVE — editing: references -> her style; a cloud; a phone --------------
t_mon, t_ref = S(u"монтажем", 42.9), S(u"референси,", 44.6)
t_monts = S(u"монтує", 46.3)
t_hm, t_tel = S(u"хмару,", 48.3), S(u"телефона,", 49.6)
F.append(u'''
        <div id="b5" class="card hid" style="left:120px; top:318px; width:840px;">
          <span class="lbl">Монтаж</span>
          <div class="row" style="gap:20px">
            <span class="chip hid" id="b5c1"><i></i>твої референси</span>
            <svg id="b5a" class="hid" width="70" height="40" viewBox="0 0 70 40"><path d="M4 20 H58 M44 6 L60 20 L44 34" fill="none" stroke="#7A1424" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>
            <span class="chip on hid" id="b5c2"><i></i>система монтує</span>
          </div>
        </div>''')
F.append(u'<svg class="sk" id="skF" width="1080" height="1920" viewBox="0 0 1080 1920"></svg>')
js(u'''
  rise("#b5", %.3f); pop("#b5c1", %.3f); pop("#b5a", %.3f, .4); pop("#b5c2", %.3f);
  sink("#b5", %.3f);
  sketch("cl", "skF");
  blob("cl", "M300 600 C240 600 230 520 300 505 C300 430 400 410 440 460 C470 380 610 380 630 455 C700 420 790 470 760 540 C830 560 810 640 740 630 Z", [230, 380, 600, 250], {seed: 41});
  label("cl", 530, 560, "хмара", {size: 56});
  draw("cl", %.3f, .8);
  sketch("ph", "skF"); box("ph", 870, 400, 110, 210, {seed: 43, r: 24}); ln("ph", 905, 578, 945, 578, {seed: 45});
  arrow("ph", 860, 600, 700, 640, {seed: 47, bend: -.25});
  draw("ph", %.3f, .55);
  erase("cl", %.3f); erase("ph", %.3f);
''' % (t_mon - 0.2, t_ref, t_monts - 0.2, t_monts, t_hm - 0.45, t_hm - 0.3, t_tel,
       S(u"Плюс", 51.1) - 0.1, S(u"Плюс", 51.1) - 0.1))
g.sfx("pop", t_mon - 0.2); g.sfx("click-soft", t_ref); g.sfx("click-soft", t_monts); g.sfx("whoosh-short", t_hm - 0.3)

# 6 · ABOVE — ten connectors ---------------------------------------------------
t_plus, t_kon2 = S(u"Плюс", 51.1), S(u"конекторів,", 52.6)
CON = [("notion", "Notion"), ("instagram", "Instagram"), ("telegram", "Telegram"), ("canva", "Canva"),
       ("googledrive", "Drive"), ("gmail", "Gmail"), ("googlecalendar", "Calendar"), ("fathom", "Fathom"),
       ("threads", "Threads"), (None, "Windsor")]
chips = u"".join(u'<span class="chip hid" id="b6c%d" style="font-size:30px; padding:10px 18px; gap:10px">%s%s</span>'
                 % (i, mark(s, 30) if s else u'<b style="font-weight:700;color:#7A1424">w.</b>', esc(n))
                 for i, (s, n) in enumerate(CON))
F.append(u'''
        <div id="b6" class="card hid" style="left:120px; top:300px; width:840px; padding:30px 34px;">
          <span class="lbl">Конектори</span>
          <div class="chips" style="gap:12px">%s</div>
        </div>''' % chips)
js(u'''
  rise("#b6", %.3f);
  %s
  sink("#b6", %.3f);
''' % (t_plus, " ".join('pop("#b6c%d", %.3f, .45);' % (i, t_kon2 - 0.5 + i * 0.16) for i in range(len(CON))),
       E(u"зладно.", 53.8) + 0.25))
g.sfx("pop", t_plus)
for i in range(0, len(CON), 3):
    g.sfx("click-soft", t_kon2 - 0.5 + i * 0.16)

# 7 · FULL — «проактивна», the routine loop ------------------------------------
c1 = S(u"Наприклад,", 63.84) - 0.3
t_pro, t_rut, t_per = S(u"проактивна.", 58.4), S(u"рутини,", 60.6), S(u"періодичністю.", 62.4)
c0 = t_pro - 0.6        # the cover lands with its headline (her review: no empty white)
C.append(u'''
        <div id="c7h" class="hid" style="position:absolute; left:0; width:1080px; top:430px; text-align:center;
             font-weight:700; font-size:150px; letter-spacing:-0.04em; color:#7A1424">проактивна</div>
        <svg class="sk" id="skC" width="1080" height="1920" viewBox="0 0 1080 1920"></svg>''')
js(u'''
  full(%.3f, %.3f);
  pop("#c7h", %.3f, .6);
  sketch("u7", "skC"); under("u7", 170, 640, 910, {stroke: "#7A1424", strokeWidth: 6, seed: 51});
  draw("u7", %.3f, .6);
  sketch("r7", "skC"); ell("r7", 540, 960, 520, 330, {seed: 53});
  label("r7", 540, 980, "рутини", {size: 60});
  draw("r7", %.3f - .2, .8);
  sketch("q7", "skC"); label("q7", 540, 1230, "спрацьовують самі", {size: 50, color: "#7A1424"});
  draw("q7", %.3f);
''' % (c0, c1, t_pro, t_pro + 0.25, t_rut - 0.1, S(u"самі,", 61.4)))
g.sfx("whoosh-short", c0); g.sfx("pop", t_pro); g.sfx("whoosh-short", c1)
BLACKOUT.append((t_pro - 0.05, E(u"проактивна.", 58.4) + 0.05))

# 8 · HALF — Sunday report, approved, the system does the rest -----------------
h2, h3 = S(u"Наприклад,", 63.84) - 0.1, S(u"І", 78.9) - 0.35
HALF.append((h2, h3))
t_ned, t_tk = S(u"неділю", 64.9), S(u"контенту,", 66.4)
t_konk, t_idei = S(u"конкурентів", 67.9), S(u"ідеї.", 69.1)
t_zat, t_tre = S(u"затверджуєш", 70.0), S(u"треди,", 72.0)
t_kar2, t_sc = S(u"каруселі", 73.0), S(u"сценарії", 74.2)
t_plan, t_nap = S(u"планує", 76.2), S(u"наперед.", 77.6)
js(u'''
  sketch("r1", "skP"); box("r1", 90, 300, 470, 420, {seed: 61});
  label("r1", 325, 375, "звіт · неділя", {size: 52});
  draw("r1", %.3f, .7);
  sketch("r2", "skP"); box("r2", 130, 430, 40, 40, {seed: 63, r: 10}); label("r2", 195, 465, "твій контент", {size: 44, anchor: "start"}); draw("r2", %.3f, .4);
  sketch("r3", "skP"); box("r3", 130, 520, 40, 40, {seed: 65, r: 10}); label("r3", 195, 555, "конкуренти", {size: 44, anchor: "start"}); draw("r3", %.3f, .4);
  sketch("r4", "skP"); box("r4", 130, 610, 40, 40, {seed: 67, r: 10}); label("r4", 195, 645, "нові ідеї", {size: 44, anchor: "start"}); draw("r4", %.3f, .4);
  sketch("r5", "skP"); _add(SK.r5, SK.r5.rc.curve([[400, 560], [440, 640], [540, 450]], opt({stroke: "#7A1424", strokeWidth: 9, seed: 69}, 69)));
  label("r5", 470, 770, "ок!", {size: 56, color: "#7A1424"});
  draw("r5", %.3f, .5);
  sketch("r6", "skP"); arrow("r6", 560, 560, 700, 360, {seed: 71});
  box("r6", 710, 300, 280, 110, {seed: 73, fill: true}); label("r6", 850, 370, "треди", {size: 46}); draw("r6", %.3f - .4, .55);
  sketch("r7b", "skP"); box("r7b", 710, 440, 280, 110, {seed: 75, fill: true}); label("r7b", 850, 510, "каруселі", {size: 46}); draw("r7b", %.3f, .55);
  sketch("r8", "skP"); box("r8", 710, 580, 280, 110, {seed: 77, fill: true}); label("r8", 850, 650, "сценарії", {size: 46}); draw("r8", %.3f, .55);
  erase("r1", %.3f); erase("r2", %.3f); erase("r3", %.3f); erase("r4", %.3f); erase("r5", %.3f);
  erase("r6", %.3f); erase("r7b", %.3f); erase("r8", %.3f);
  sketch("r9", "skP"); box("r9", 240, 330, 600, 420, {seed: 81});
  ln("r9", 240, 430, 840, 430, {seed: 83}); ln("r9", 440, 330, 440, 750, {seed: 85}); ln("r9", 640, 330, 640, 750, {seed: 87});
  ln("r9", 240, 590, 840, 590, {seed: 89});
  draw("r9", %.3f, .45);
  sketch("r10", "skP"); ell("r10", 340, 510, 120, 100, {stroke: "#7A1424", seed: 91}); ell("r10", 540, 670, 120, 100, {stroke: "#7A1424", seed: 93});
  ell("r10", 740, 510, 120, 100, {stroke: "#7A1424", seed: 95}); label("r10", 540, 815, "наперед", {size: 54, color: "#7A1424"});
  draw("r10", %.3f, .4);
  erase("r9", %.3f); erase("r10", %.3f);
''' % (t_ned - 0.2, t_tk, t_konk, t_idei - 0.2, t_zat, t_tre - 0.15, t_kar2 - 0.1, t_sc - 0.1,
       t_plan - 0.6, t_plan - 0.6, t_plan - 0.6, t_plan - 0.6, t_plan - 0.6, t_plan - 0.6, t_plan - 0.6, t_plan - 0.6,
       t_plan - 0.3, t_nap - 0.5, h3, h3))
g.sfx("whoosh-short", h2); g.sfx("whoosh-short", h3)
for t in (t_tk, t_konk, t_idei, t_tre, t_kar2, t_sc):
    g.sfx("click-soft", t)
g.sfx("pop", t_zat)

# 9 · ABOVE — her part, and everything else -----------------------------------
t_str, t_opr, t_zap = S(u"стратегії,", 80.9), S(u"опрувнути", 81.95), S(u"записати", 83.2)
t_vse, t_mn, t_dz, t_ps, t_cl = S(u"Все", 84.96), S(u"монтує,", 85.4), S(u"дизайнить,", 86.0), S(u"постить,", 86.6), S(u"Клоді.", 87.9)
rows = [(u"напрямок стратегії", "a"), (u"апрув тексту і плану", "b"), (u"записати відео", "c")]
F.append(u'''
        <div id="b9" class="card hid" style="left:120px; top:300px; width:840px; padding:34px 40px;">
          <span class="lbl">Твоя частина</span>
          %s
        </div>
        <div id="b9b" class="card hid" style="left:120px; top:300px; width:840px; padding:34px 40px;">
          <span class="lbl">Все інше — саме</span>
          <div class="chips">
            <span class="chip on hid" id="b9m"><i></i>монтує</span>
            <span class="chip on hid" id="b9d"><i></i>дизайнить</span>
            <span class="chip on hid" id="b9p"><i></i>постить</span>
            <span class="chip hid" id="b9c">%s Claude</span>
          </div>
        </div>''' % (u"".join(u'<div class="row" style="margin-top:%dpx"><span class="check" id="b9k%s"></span>'
                              u'<span style="font-size:40px;font-weight:500">%s</span></div>' % (0 if i == 0 else 18, k, esc(t))
                              for i, (t, k) in enumerate(rows)), mark("claude", 34)))
js(u'''
  rise("#b9", %.3f);
  tl.set("#b9ka", {className: "check on"}, %.3f); pop("#b9ka", %.3f, .45);
  tl.set("#b9kb", {className: "check on"}, %.3f); pop("#b9kb", %.3f, .45);
  tl.set("#b9kc", {className: "check on"}, %.3f); pop("#b9kc", %.3f, .45);
  sink("#b9", %.3f); rise("#b9b", %.3f);
  pop("#b9m", %.3f); pop("#b9d", %.3f); pop("#b9p", %.3f); pop("#b9c", %.3f);
  sink("#b9b", %.3f);
''' % (S(u"лишається", 80.0) - 0.3, t_str, t_str, t_opr, t_opr, t_zap, t_zap,
       t_vse - 0.35, t_vse - 0.1, t_mn, t_dz, t_ps, t_cl, E(u"Клоді.", 87.9) + 0.25))
for t in (t_str, t_opr, t_zap, t_mn, t_dz, t_ps, t_cl):
    g.sfx("click-soft", t)
BLACKOUT.append((t_mn - 0.05, E(u"постить,", 86.6) + 0.05))

# 10 · ABOVE — CTA -------------------------------------------------------------
t_blog, t_smm, t_pid = S(u"блогерка", 88.97), S(u"СММниця", 89.77), S(u"підприємиця", 90.51)
t_24, t_stav = S(u"24", 93.0), S(u"став", 95.3)
F.append(u'''
        <div id="b10" class="hid" style="position:absolute; left:120px; top:320px; width:840px;
             display:flex; gap:14px; justify-content:center; flex-wrap:wrap">
          <span class="chip hid" id="b10a"><i></i>блогерка</span>
          <span class="chip hid" id="b10b"><i></i>СММниця</span>
          <span class="chip hid" id="b10c"><i></i>підприємиця</span>
        </div>
        <div id="b10n" class="pill light hid" style="left:390px; top:450px; font-weight:700; font-size:64px;
             padding:20px 48px; color:#7A1424">24/7</div>
        <div id="b10cta" class="pill hid" style="left:230px; top:560px;">Став + в коментарях</div>''')
js(u'''
  fadein("#b10", %.3f, .01); pop("#b10a", %.3f); pop("#b10b", %.3f); pop("#b10c", %.3f);
  pop("#b10n", %.3f);
  pop("#b10cta", %.3f, .6);
  // comments are down at the right of the IG rail, so the pointer goes down to
  // them — never up at the pill (her review of 41). Tip stays left of x 900.
  sketch("a10", "skF"); label("a10", 800, 730, "сюди!", {size: 52});
  arrow("a10", 820, 760, 880, 975, {strokeWidth: 5, seed: 97, bend: -.25});
  draw("a10", %.3f, .5);
''' % (t_blog - 0.05, t_blog, t_smm, t_pid, t_24, t_stav, t_stav + 0.55))
g.sfx("pop", t_blog); g.sfx("pop", t_24); g.sfx("pop", t_stav)
BLACKOUT.append((S(u"то", 95.4) - 0.05, DUR))     # the pill says it

# ---------------------------------------------------------------- mattes for the half screens
for i, (a, b) in enumerate(HALF):
    g.matte("half%d" % (i + 1), round(a - 0.1, 3), round(b - a + 1.2, 3))
    js("  half(%.3f, %.3f);" % (a, b))
    PLACE.append((a + 0.4, b + 0.2, "bottom", 980))


def main():
    chunks = g.chunks(CAPS, place=PLACE)
    doc = g.document(title=u"Reel 41 — Не просто промти", plate="assets/base.mp4",
                     behind="\n".join(B), panel="\n".join(P), front="\n".join(F), cover="\n".join(C),
                     js="\n".join(J), chunks=chunks, blackout=BLACKOUT)
    g.write(HERE, doc)
    print("index.html  %d caption chunks, %d sfx cues, %d mattes" % (len(chunks), len(g.cues), len(g.mattes)))


main()
