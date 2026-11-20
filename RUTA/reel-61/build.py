# -*- coding: utf-8 -*-
"""Reel 61 — «Як зробити, щоб АІ-агент нічого не вигадував?». Posts 2026-11-21.
Batch 2026-11-20 (raw 20261120_134413), STYLE.md §00 look (her call that day:
"lets go back to the style that we always had, the one with the dark red").

The one object is **her real SendPulse agent screen** (Drive, 2026-11-20): the
DM goes wrong above her -> «одна штука» -> HALF 1: the screen, «Інструкція для
бота» boxed («інструкції й скрипти»), «Веб-пошук» looped -> above: агент ->
інтернет, «іноді корисно», then «шанс помилки» -> HALF 2: the same screen,
Веб-пошук struck «вимкнено», the instruction box drawn red «тільки скрипти»,
a loop round it on «ніколи» -> above: «SendPulse» pill, «геніально» -> the DM
again: a question it can't answer, «Не знаю — передаю менеджеру», «менеджер»
-> CTA chips, «Пиши + в коментарях», an arrow down to the comments.

usage: python3 build.py   (then: sh work/b1021/mattes.sh 61; python3 tools/sfx.py mix 61)
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
from gstyle import G, Words, load_caps  # noqa: E402

NN = "61"
DUR = 68.417           # (2053 plate frames - 0.5) / 30
g = G(dur=DUR, reel=NN)
# her plate: hair top ≈ y 650 on the wide shot, so pushed 330 it is at ≈ 980;
# on the panel the word captions sit with their bottom at ≈ 930
g.PANEL_TOP = 820

# whisper's spelling of what she said -> her word (checked against the script)
FIX = {
    u"Небільше": u"Найбільший", u"страт": u"страх", u"будь": u"будь-яким", u"яким": None,
    u"дурнетю.": u"дурницю.", u"Штукав.": u"штуку.", u"таку": u"такого",
    u"синпуївсь,": u"SendPulse,", u"Туму!": u"Тому", (u"Я", 35.1): u"якщо", (u"ще", 35.3): u"цю",
    u"концюю": None, u"виділяв": u"відійде", u"Сенпульс.": u"SendPulse.", (u"Якщо", 47.9): u"якщо",
    u"Йв": u"І", u"сссссссссссссс": u"все.", (u"Якщо", 60.2): u"якщо", u"пишу": u"пиши",
    u"плюсів": u"плюсик", u"ми...": u"ми", (u"по", 67.6): u"поспілкуємось.", u"спілкуємось.": None,
}
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
EXTRA = u'''
    .dm { position: absolute; left: 110px; top: 300px; width: 860px; padding: 30px 36px; }
    .dm .lbl { margin-bottom: 18px; }
    .bub { display: inline-block; border-radius: 28px; padding: 18px 28px; font-size: 36px;
           font-weight: 500; line-height: 1.25; }
    .bub.in { background: #F4EDED; color: #241919; border-bottom-left-radius: 8px; }
    .bub.me { background: #7A1424; color: #fff; border-bottom-right-radius: 8px; }
    .rowr { display: flex; justify-content: flex-end; margin-top: 16px; }
    .shot { position: absolute; left: 160px; top: 290px; width: 760px; border-radius: 16px;
            box-shadow: 0 1px 3px rgba(36,25,25,.12), 0 10px 30px rgba(36,25,25,.14); }
'''

# 1 · ABOVE — the DM goes wrong -------------------------------------------------
t_strakh, t_ahent, t_prydum = S(u"страх", 0.75), S(u"агентом,", 2.11), S(u"придумає", 5.45)
t_durn, t_skladno = S(u"дурницю.", 7.39), S(u"складно", 8.97)
F.append(u'''
        <div id="d1" class="card dm hid">
          <span class="lbl">Direct · AI-агент</span>
          <div><span class="bub in hid" id="d1q">Скільки коштує і коли можна почати?</span></div>
          <div class="rowr"><span class="bub me hid" id="d1a">Звісно! Усе безкоштовно, почнемо вчора</span></div>
        </div>''')
js(u'''
  pop("#d1", %.3f); pop("#d1q", %.3f);
  pop("#d1a", %.3f);
  sketch("x1", "skF"); ln("x1", 520, 470, 920, 560, {stroke: "#7A1424", strokeWidth: 7, seed: 5, halo: false});
  ln("x1", 520, 560, 920, 470, {stroke: "#7A1424", strokeWidth: 7, seed: 9, halo: false});
  draw("x1", %.3f, .25);
  sketch("x1t", "skF"); label("x1t", 720, 640, "дурниця!", {size: 52, color: "#7A1424"});
  draw("x1t", %.3f);
  sink("#d1", %.3f); erase("x1", %.3f); erase("x1t", %.3f);
''' % (t_strakh, t_strakh + 0.4, t_prydum, t_durn - 0.1, t_durn + 0.2, t_skladno, t_skladno, t_skladno))
g.sfx("pop", t_strakh); g.sfx("notification", t_prydum); g.sfx("click", t_durn)

# 2 · ABOVE — «одну штуку» ---------------------------------------------------------
t_odnu = S(u"одну", 11.20)
F.append(u'<div id="one" class="pill hid" style="left:0; right:0; margin:auto; width:max-content; top:300px;">'
         u'<span class="num" style="color:#fff; font-size:60px">1</span> штука</div>')
js(u'  pop("#one", %.3f); sink("#one", %.3f);' % (t_odnu - 0.05, S(u"Коли", 12.27) - 0.2))
g.sfx("pop", t_odnu)

# 3 · HALF 1 — her real SendPulse screen: the instructions, the web button --------
h0 = S(u"Коли", 12.27) - 0.1
h1 = S(u"Ця", 22.48) - 0.25
HALF.append((h0, h1))
# the screen: 760 px wide (scale .958) at (160, 290); the instruction field is
# x 177-601 y 355-520, ВЕБ-ПОШУК x 622-903 y 451-509; the screen's lower left
# (x 177-601, y 577-788) is empty — the labels go there
P.append(u'<img class="shot hid" id="shot" src="assets/shots/sendpulse-agent.png">')
P.append(u'<svg class="sk" id="skP" data-layout-allow-occlusion width="1080" height="1240" viewBox="0 0 1080 1240"></svg>')
t_pole, t_instr = S(u"поле,", 15.62), S(u"інструкції", 17.14)
t_knopka, t_web = S(u"кнопка", 19.17), S(u"веб", 20.56)
js(u'''
  fadein("#shot", %.3f, .35);
  sketch("p1", "skP"); box("p1", 168, 345, 444, 186, {seed: 3, stroke: "#7A1424", strokeWidth: 5, fill: false});
  draw("p1", %.3f);
  sketch("p1a", "skP"); label("p1a", 390, 650, "інструкції й скрипти", {size: 46});
  draw("p1a", %.3f);
  sketch("p2", "skP"); ell("p2", 762, 480, 330, 92, {seed: 11, stroke: "#7A1424", strokeWidth: 5, fill: false});
  draw("p2", %.3f);
  sketch("p2a", "skP"); label("p2a", 360, 750, "кнопка «Веб»", {size: 46});
  arrow("p2a", 500, 735, 720, 528, {seed: 13, bend: -.12});
  draw("p2a", %.3f);
  erase("p1"); erase("p1a"); erase("p2"); erase("p2a");
'''.replace("erase(\"p1\"); erase(\"p1a\"); erase(\"p2\"); erase(\"p2a\");",
            "erase(\"p1\", %.3f); erase(\"p1a\", %.3f); erase(\"p2\", %.3f); erase(\"p2a\", %.3f);" % ((h1,) * 4))
   % (h0 + 0.5, t_pole - 0.1, t_instr - 0.3, t_knopka - 0.1, t_web - 0.4))
g.sfx("whoosh-short", h0); g.sfx("click-soft", t_pole); g.sfx("click-soft", t_knopka)

# 4 · ABOVE — what the button means: агент -> інтернет, useful, but risky ----------
t_ahent2, t_internet = S(u"агент", 23.84), S(u"інтернет", 25.36)
t_keisy, t_korysno = S(u"кейси,", 28.72), S(u"корисно.", 29.84)
t_ale, t_shans, t_te = S(u"Але", 30.64), S(u"шанс,", 32.28), S(u"те.", 34.06)
F.append(u'''
        <div id="a1" class="pill light hid" style="left:120px; top:330px;">агент</div>
        <div id="a2" class="pill light hid" style="left:640px; top:330px;">інтернет</div>
        <div id="a3" class="chip hid" style="position:absolute; left:0; right:0; margin:auto; width:max-content; top:500px;"><i></i>іноді корисно</div>
        <div id="a4" class="pill hid" style="left:0; right:0; margin:auto; width:max-content; top:470px;">шанс помилки ↑</div>''')
js(u'''
  pop("#a1", %.3f);
  sketch("a12", "skF"); arrow("a12", 400, 390, 625, 390, {seed: 21, bend: .1});
  draw("a12", %.3f, .45);
  pop("#a2", %.3f);
  pop("#a3", %.3f); out("#a3", %.3f);
  pop("#a4", %.3f);
  sink("#a1, #a2, #a4", %.3f); erase("a12", %.3f);
''' % (t_ahent2 - 0.05, t_internet - 0.55, t_internet, t_korysno - 0.1, t_ale - 0.1,
       t_shans - 0.1, t_te + 0.15, t_te + 0.15))
g.sfx("pop", t_ahent2); g.sfx("pop", t_internet); g.sfx("click-soft", t_korysno); g.sfx("pop", t_shans)
BLACKOUT.append((t_internet - 0.05, E(u"інтернет", 25.36) + 0.05))
BLACKOUT.append((t_shans - 0.05, E(u"шанс,", 32.28) + 0.05))

# 5 · HALF 2 — the button off, only the scripts ------------------------------------
k0 = S(u"Тому", 34.43) - 0.1
k1 = E(u"інструкції.", 41.47) + 0.3
HALF.append((k0, k1))
t_vmyk, t_propys, t_nikoly = S(u"вмикати,", 36.96), S(u"прописати", 38.60), S(u"ніколи", 40.33)
js(u'''
  sketch("q1", "skP"); ln("q1", 625, 448, 900, 512, {stroke: "#7A1424", strokeWidth: 7, seed: 31});
  ln("q1", 625, 512, 900, 448, {stroke: "#7A1424", strokeWidth: 7, seed: 33});
  draw("q1", %.3f, .3);
  sketch("q1t", "skP"); label("q1t", 360, 750, "не вмикаю", {size: 46, color: "#7A1424"});
  arrow("q1t", 500, 735, 720, 528, {seed: 35, bend: -.12, stroke: "#7A1424"});
  draw("q1t", %.3f);
  sketch("q2", "skP"); box("q2", 168, 345, 444, 186, {seed: 37, fill: true});
  draw("q2", %.3f);
  sketch("q2t", "skP"); label("q2t", 390, 650, "тільки скрипти", {size: 46});
  draw("q2t", %.3f);
  sketch("q3", "skP"); ell("q3", 390, 438, 520, 250, {seed: 41, stroke: "#7A1424", strokeWidth: 6, fill: false});
  draw("q3", %.3f, .6);
  erase("q1", %.3f); erase("q1t", %.3f); erase("q2", %.3f); erase("q2t", %.3f); erase("q3", %.3f);
''' % (t_vmyk - 0.1, t_vmyk + 0.3, t_propys - 0.2, t_propys + 0.3, t_nikoly - 0.1, k1, k1, k1, k1, k1))
g.sfx("whoosh-short", k0); g.sfx("click", t_vmyk); g.sfx("click-soft", t_propys); g.sfx("click-soft", t_nikoly)

# 6 · ABOVE — «геніально … SendPulse» -----------------------------------------------
t_gen, t_sp = S(u"геніально,", 43.00), S(u"SendPulse.", 46.38)
F.append(u'''
        <div id="g1" class="pill light hid" style="left:0; right:0; margin:auto; width:max-content; top:330px;
             font-size:56px; font-weight:700">SendPulse</div>''')
js(u'''
  sketch("g1t", "skF"); label("g1t", 540, 520, "геніально", {size: 58, color: "#7A1424"});
  under("g1t", 400, 545, 680, {stroke: "#7A1424", seed: 45});
  draw("g1t", %.3f);
  pop("#g1", %.3f);
  sink("#g1", %.3f); erase("g1t", %.3f);
''' % (t_gen - 0.05, t_sp - 0.1, t_sp + 0.75, t_sp + 0.75))
g.sfx("click-soft", t_gen); g.sfx("pop", t_sp)
BLACKOUT.append((t_sp - 0.05, E(u"SendPulse.", 46.38) + 0.05))

# 7 · ABOVE — the DM again: a question it can't answer ------------------------------
t_pyt, t_znaie = S(u"питання,", 48.48), S(u"знає,", 50.10)
t_skazhe, t_men, t_nich, t_mozhe = S(u"скаже,", 53.44), S(u"менеджеру.", 55.58), S(u"нічого", 57.05), S(u"може.", 59.59)
F.append(u'''
        <div id="d2" class="card dm hid">
          <span class="lbl">Direct · AI-агент</span>
          <div><span class="bub in hid" id="d2q">А ви робите доставку в Канаду?</span></div>
          <div class="rowr"><span class="bub me hid" id="d2a">Не знаю відповіді. Передаю вас менеджеру</span></div>
        </div>
        <div id="d2m" class="chip on hid" style="position:absolute; left:130px; top:640px;"><i></i>менеджер</div>''')
js(u'''
  pop("#d2", %.3f); pop("#d2q", %.3f);
  pop("#d2a", %.3f);
  pop("#d2m", %.3f);
  sketch("d2k", "skF"); label("d2k", 720, 690, "нічого не вигадує", {size: 50, color: "#7A1424"});
  draw("d2k", %.3f);
  sink("#d2, #d2m", %.3f); erase("d2k", %.3f);
''' % (t_pyt - 0.4, t_pyt, t_skazhe, t_men - 0.05, t_nich, t_mozhe + 0.2, t_mozhe + 0.2))
g.sfx("pop", t_pyt - 0.4); g.sfx("notification", t_skazhe); g.sfx("pop", t_men)

# 8 · CTA — who it is for, «Пиши + в коментарях», pointer down ------------------------
t_mal, t_kom, t_men2, t_zai = S(u"малий", 60.76), S(u"команда,", 62.32), S(u"менеджери,", 62.83), S(u"заявок,", 63.53)
t_pyshy = S(u"пиши", 65.80)
F.append(u'''
        <div id="c" style="position:absolute; left:90px; width:900px; top:300px; display:flex; flex-wrap:wrap;
             gap:14px; justify-content:center">
          <span class="chip hid" id="c1"><i></i>малий чи середній бізнес</span>
          <span class="chip hid" id="c2"><i></i>команда</span>
          <span class="chip hid" id="c3"><i></i>менеджери</span>
          <span class="chip hid" id="c4"><i></i>багато заявок</span>
        </div>
        <div id="cp" class="pill hid" style="left:0; right:0; margin:auto; width:max-content; top:470px;">Пиши + в коментарях</div>''')
js(u'''
  pop("#c1", %.3f); pop("#c2", %.3f); pop("#c3", %.3f); pop("#c4", %.3f);
  pop("#cp", %.3f, .6);
  sketch("ca", "skF"); arrow("ca", 840, 560, 880, 1450, {strokeWidth: 5, seed: 97, bend: -.12});
  draw("ca", %.3f, .55);
''' % (t_mal, t_kom, t_men2, t_zai, t_pyshy - 0.1, t_pyshy + 0.3))
g.sfx("pop", t_mal); g.sfx("click-soft", t_kom); g.sfx("click-soft", t_men2); g.sfx("click-soft", t_zai)
g.sfx("pop", t_pyshy)
BLACKOUT.append((t_pyshy - 0.05, DUR))     # the pill says it

# ---------------------------------------------------------------- mattes for the half screens
for i, (a, b) in enumerate(HALF):
    g.matte("half%d" % (i + 1), round(a - 0.1, 3), round(b - a + 1.2, 3))
    js("  half(%.3f, %.3f);" % (a, b))
    PLACE.append((a + 0.4, b + 0.2, "bottom", 938))


def main():
    chunks = g.chunks(CAPS, place=PLACE)
    doc = g.document(title=u"Reel 61 — агент нічого не вигадує", plate="assets/base.mp4",
                     behind="\n".join(B), panel="\n".join(P), front="\n".join(F), cover="\n".join(C),
                     js="\n".join(J), chunks=chunks, blackout=BLACKOUT, extra_css=EXTRA)
    g.write(HERE, doc)
    print("index.html  %d caption chunks, %d sfx cues, %d mattes" % (len(chunks), len(g.cues), len(g.mattes)))


main()
