# -*- coding: utf-8 -*-
"""Reel 57 — «Скільки заробляє RUTA». Batch 2026-11-20 (raw 20261120_133314).
STYLE.md §00 with her review of reel 61 (natural editing, fewer graphics).
reel-61/build.py is the skeleton.

The one object is HER GUESS: плюс / мінус / нуль at the start, answered at the
end («мінус» behind her, «нуль» with one more paying user). Only numbers she
says: 70, 100, 35, 20, 55, 15–20, 1,50, 70, 60.

Beats: behind «RUTA» (cover) -> shuffle плюс / мінус / нуль -> FULL 1 her real
RUTA home screen rebuilt 1:1 as a platform ad (zoom to «+» on «голосових»,
«Сторіс» on «сторітели», «Рілс» on «рілси») -> shuffle каруселі / 8 шаблонів /
тредси -> glass «70+ людей» -> HALF 1 scheme: Claude $100 struck, розробка /
робота -> glass hosting card: Supabase / Vercel, Free struck, $35 $20 = $55 ->
HALF 2 scheme: голосове -> текст; голосове / памʼять / аналітика -> сценарій ->
shuffle ШІ $15–20 / 1 юзер ≈ $1,50 -> glass scraper card (Meta API чекаю,
безкоштовно) -> FULL 2 the month: витрати ≈ $70 vs заробляє $60 -> behind
«мінус» -> shuffle +1 людина / нуль -> CTA: comment types RUTA, pill.

usage: python3 build.py   (then: sh work/b1021/mattes.sh 57; python3 tools/sfx.py mix 57)
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
from gstyle import G, Words, load_caps, mark  # noqa: E402

NN = "57"
DUR = 134.283          # (4029 plate frames - 0.5) / 30
g = G(dur=DUR, reel=NN)
g.PANEL_TOP = 820      # panel captions: bottom 938, her pushed hair at ≈ 960

FIX = {
    u"більшість": u"більше", (u"це", 1.6): u"70", u"видастся": None,
    (u"як", 11.5): u"Як", u"ноль.": u"нуль?",
    u"Рута": u"RUTA", (u"твій", 22.3): u"твоїх", u"Перепустив": u"переписує", u"декілька": u"кілька",
    (u"на", 27.8): u"не", u"коросалі.": u"каруселі,", u"«Коросели»": u"каруселей",
    (u"по", 33.8): u"пише", u"шатраці.": u"тредси.",
    u"корисують": u"користуються", (u"це", 35.8): None,
    (u"для", 57.6): u"для...", u"Взагалі,": u"взагалі", u"роботи,": u"роботи.",
    u"Versal.": u"Vercel.", u"Versal": u"Vercel", u"20,": u"20.", (u"За", 76.0): u"за",
    u"це власне": u"це, власне,",
    (u"На", 93.8): u"на", u"штучне": u"штучний", u"теле": u"інтелект", (u"15", 95.5): u"15–20",
    (u"20", 96.3): None, (u"доларів", 97.1): u"доларів.", u"кожен": u"Кожен",
    u"$1": u"долар", u".50,": u"пʼятдесят,",
    (u"на", 109.7): u"до", u"API,": u"API.",
    u"Загалом": u"Загалом,", (u"мінусі,", 123.3): u"мінусі.", (u"але", 123.7): u"Але", (u"б", 124.4): None,
}
CAPS = load_caps(NN, FIX)
# the CTA: the aligner laid the script's words over what she said — rebuild it
# from the cut's own word timings (as the old build did)
_words = json.load(io.open(os.path.join(ROOT, "work", "r" + NN, "words.json"), encoding="utf-8"))["words"]
CAPS = [c for c in CAPS if c["s"] < 127.85]
SPELL = {u"пишу": u"пиши", u"додаток,": u"додаток.", u"а": u"А"}
for w in [w for w in _words if w["s"] >= 127.85]:
    t = SPELL.get(w["w"], w["w"])
    if t == u"Словерута,":
        m = round((w["s"] + w["e"]) / 2, 3)
        CAPS.append({"w": u"слово", "s": w["s"], "e": m})
        CAPS.append({"w": u"«RUTA»,", "s": m, "e": w["e"]})
        continue
    CAPS.append({"w": t, "s": w["s"], "e": w["e"]})
W = Words(CAPS)
S, E = W.s, W.e

B, P, F, C, J = [], [], [], [], []
BLACKOUT, PLACE, HALF = [], [], []


def js(s):
    J.append(s)


P.append(u'<svg class="sk" id="skP" data-layout-allow-occlusion width="1080" height="1240" viewBox="0 0 1080 1240"></svg>')

EXTRA = u'''
    /* her note on 61: the plain white card in the shuffle slot, no glass */
    .shuf .chip { font-size: 48px; padding: 18px 34px; }
    .shuf .chip b { width: 46px; height: 46px; border-radius: 50%; background: #7A1424; color: #fff;
                    display: inline-flex; align-items: center; justify-content: center;
                    font-size: 38px; font-weight: 700; line-height: 1; flex: none; }
    .shuf .ncard { background: #fff; border-radius: 32px; padding: 22px 40px; text-align: center;
                   box-shadow: 0 1px 3px rgba(36,25,25,.10), 0 10px 30px rgba(36,25,25,.14); }
    .ncard .lb { display: block; font-size: 30px; font-weight: 500; color: #574142; margin-bottom: 4px; }
    .ncard .nv { display: block; font-size: 84px; font-weight: 700; letter-spacing: -0.03em; color: #7A1424; line-height: 1.05; }

    .gl { left: 110px; width: 860px; padding: 24px 34px; }
    .gl .hd { display: flex; align-items: center; gap: 14px; font-size: 28px; font-weight: 500; color: #574142; }
    .gl .bn { font-size: 64px; font-weight: 700; letter-spacing: -0.03em; color: #7A1424; }
    .rw { display: flex; align-items: center; gap: 14px; height: 70px; font-size: 38px; white-space: nowrap; font-weight: 500; color: #241919; }
    .rw .sub { color: #574142; font-weight: 400; }
    .rw .pr { margin-left: auto; position: relative; display: flex; align-items: center; gap: 12px; }
    .rw .pr .v { font-weight: 700; font-size: 40px; color: #7A1424; min-width: 90px; text-align: right; }
    .free { position: relative; border-radius: 12px; padding: 4px 14px; font-size: 26px; font-weight: 500;
            background: #fff; color: #574142; border: 2px solid #DEBFBF; }
    .free .st { position: absolute; left: 8px; right: 8px; top: 50%; height: 4px; margin-top: -2px; border-radius: 2px;
                background: #7A1424; transform-origin: 0 50%; transform: scaleX(0); }
    .rule { height: 2px; background: rgba(36,25,25,.14); margin: 6px 0; }
    .meta { width: 40px; height: 40px; color: #7A1424; }
    .dots i { display: inline-block; width: 10px; height: 10px; margin-left: 6px; border-radius: 50%; background: #7A1424; }

    .cmt { left: 150px; top: 330px; width: 780px; height: 112px; border-radius: 56px; padding: 0 22px;
           display: flex; align-items: center; gap: 20px; font-size: 38px; color: #241919; }
    .cmt .av { width: 66px; height: 66px; border-radius: 50%; background: #DEBFBF; flex: none; }
    .cmt .ph { color: #8a7576; }
    .cmt .ty { font-weight: 700; letter-spacing: .02em; }
    .cmt .ty span { opacity: 0; }
    .cmt .send { margin-left: auto; font-weight: 500; font-size: 32px; color: #7A1424; }
'''

# 1 · BEHIND — «RUTA» (the cover frame: «Скільки заробляє RUTA») ---------------
t_kor = E(u"користувачів,", 2.17)
B.append(u'        <div id="bw1" class="big" data-layout-allow-occlusion style="top:440px; font-size:250px">RUTA</div>')
g.matte("b1", 0.0, round(t_kor + 0.9, 3))
js(u'  tl.set("#bw1", {autoAlpha: 1}, 0); sink("#bw1", %.3f);' % (t_kor + 0.35))

# 2 · ABOVE — the guess: плюс / мінус / нуль through one slot -------------------
GUESS = [(u"+", u"плюс", S(u"плюс,", 12.94)), (u"−", u"мінус", S(u"мінусі,", 13.78)),
         (u"0", u"нуль", S(u"нуль?", 14.79))]
for i, (sg, txt, t) in enumerate(GUESS):
    F.append(u'        <div id="gs%d" class="shuf hid"><span class="chip"><b>%s</b>%s</span></div>' % (i, sg, txt))
    g.sfx("pop", t - 0.1)
js(u'  shuffle(["#gs0", "#gs1", "#gs2"], [%s], %.3f);'
   % (", ".join("%.3f" % (t - 0.1) for _, _, t in GUESS), S(u"Запамʼятай", 15.09) + 0.9))

# 3 · FULL 1 — her RUTA home screen as a platform ad ---------------------------
# Rebuilt 1:1 from app-screenshots/app-ruta.jpg (coordinates are the screenshot's
# own pixels at 1028 x 2000), so the zooms stay crisp. Nothing on it is invented:
# the texts, the two reels and their numbers are her real screen.
f0 = S(u"Для", 17.93) - 0.15
f1 = E(u"каруселі,", 28.22) + 0.25
NAV_ICONS = {
    "home": u'<path d="M4 11 L14 3 L24 11 V24 H17 V16 H11 V24 H4 Z"/>',
    "cal": u'<rect x="4" y="6" width="20" height="18" rx="3"/><path d="M4 11 H24 M9 3 V8 M19 3 V8"/>',
    "bars": u'<path d="M5 24 H25 M8 20 V12 M13 20 V6 M18 20 V10 M23 20 V14"/>',
    "user": u'<circle cx="14" cy="9" r="5"/><path d="M4 25 C5 18 23 18 24 25"/>',
}


def ico(k, col):
    return (u'<svg width="52" height="52" viewBox="0 0 28 28" fill="none" stroke="%s" stroke-width="2.2" '
            u'stroke-linecap="round" stroke-linejoin="round">%s</svg>' % (col, NAV_ICONS[k]))


C.append(u"""
        <div id="stage">
          <div id="win" class="app" data-layout-allow-overlap data-layout-allow-overflow>
            <div class="a-h1" style="left:44px;top:52px">Добрий день, Рута</div>
            <div class="a-sub" style="left:44px;top:150px">Готова створювати?</div>
            <div class="a-ring" style="left:838px;top:58px">15</div>
            <div class="a-cap" style="left:48px;top:300px">СЬОГОДНІ</div>
            <div class="a-plus" style="left:905px;top:280px">+</div>
            <div class="a-card" style="left:44px;top:383px;width:939px;height:207px">
              <i class="pie" style="left:46px;top:50px;background:conic-gradient(#C87533 0 62%%, #F6E3D3 62%% 100%%)"></i>
              <div class="a-t" style="left:162px;top:42px">Ти шукаєш ідею для свого</div>
              <div class="a-m" style="left:162px;top:120px"><span style="color:#C87533">Змонтувати</span> · <span id="lbR" class="a-tag">Рілс</span></div>
              <div class="a-date" style="left:741px;top:112px">▦&nbsp; 8 ВЕР</div>
            </div>
            <div class="a-card" style="left:44px;top:620px;width:939px;height:307px">
              <i class="pie" style="left:46px;top:50px;background:conic-gradient(#7BBF5A 0 70%%, #E4F2DA 70%% 100%%)"></i>
              <div class="a-t" style="left:162px;top:42px">Система, яка сама розбирає дз...</div>
              <div class="a-badge" style="left:828px;top:48px">1/2</div>
              <div class="a-body" style="left:162px;top:98px;width:640px">Знаєте, що займає в мене мінімум 30%% робочого часу?</div>
              <div class="a-m" style="left:162px;top:220px"><span style="color:#6BB04A">Готово</span> · <span id="lbS" class="a-tag">Сторіс</span></div>
              <div class="a-date" style="left:741px;top:212px">▦&nbsp; 8 ВЕР</div>
            </div>
            <div class="a-btn" style="left:43px;top:1004px;width:724px">✦&nbsp; Дай мені ідеї</div>
            <div class="a-ghost" style="left:790px;top:1004px;width:193px">Глянути</div>
            <div class="a-cap" style="left:48px;top:1228px">СТАТИСТИКА</div>
            <div class="a-more" style="left:822px;top:1222px">більше ›</div>
            <div class="a-card" style="left:44px;top:1302px;width:939px;height:455px">
              <img src="assets/shots/thumb1.jpg" style="left:44px;top:48px;width:117px;height:147px">
              <div class="a-t2" style="left:194px;top:40px">А на годиннику перша ночі і ...</div>
              <div class="a-hit" style="left:786px;top:33px">↗ ХІТ</div>
              <div class="a-st" style="left:196px;top:92px"><b>14 752</b> переглядів&nbsp;&nbsp; 58 вподобань</div>
              <div class="a-m2" style="left:194px;top:166px">9 коментарів</div>
              <div style="left:44px;top:241px;width:852px;height:2px;background:#ECEAEA"></div>
              <img src="assets/shots/thumb2.jpg" style="left:44px;top:276px;width:117px;height:144px">
              <div class="a-t2" style="left:194px;top:290px">Підписуйся, щоб не пропуст...</div>
              <div class="a-hit" style="left:786px;top:288px">↗ ХІТ</div>
              <div class="a-st" style="left:196px;top:344px"><b>3 178</b> переглядів&nbsp; 53 вподобань&nbsp; 3 коментарів</div>
            </div>
            <div class="a-card" style="left:44px;top:1945px;width:939px;height:200px">
              <i class="pie" style="left:46px;top:30px;background:#fff;border:3px solid #DADADA"></i>
              <div class="a-t" style="left:162px;top:18px">Є одна система, яку я налаштувала ...</div></div>
            <div class="a-nav" style="left:35px;top:1818px;width:958px;height:147px">
              <div class="a-ni" style="left:46px;color:#1F4FA3">%(home)s<span>Головна</span></div>
              <div class="a-ni" style="left:248px">%(cal)s<span>План</span></div>
              <div class="a-ni" style="left:600px">%(bars)s<span>Інсайти</span></div>
              <div class="a-ni" style="left:790px">%(user)s<span>Профіль</span></div>
            </div>
            <div id="fab" class="a-fab" style="left:449px;top:1821px">+</div>
            <div id="rip" class="a-rip" style="left:449px;top:1821px"></div>
          </div>
        </div>""" % {"home": ico("home", "#1F4FA3"), "cal": ico("cal", "#6b6b6b"),
                     "bars": ico("bars", "#6b6b6b"), "user": ico("user", "#6b6b6b")})
# her real screen layers on purpose (the last card scrolls under the nav bar; the
# 3D tilt projects rows over each other) — tell the layout check it is intended
C[-1] = C[-1].replace(u'<div class="', u'<div data-layout-allow-overlap class="').replace(
    u'<div id="', u'<div data-layout-allow-overlap id="').replace(u'<span class="', u'<span data-layout-allow-overlap class="')
EXTRA += u"""
    #cover { background: radial-gradient(120% 80% at 50% 35%, #FFFFFF 0%, #F6EFEF 70%, #F1E7E7 100%); }
    #stage, #stage2 { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; perspective: 2600px; }
    #win { position: absolute; left: 0; top: 0; width: 1028px; height: 2000px; background: #F6F6F4; overflow: hidden;
           border-radius: 64px; font-family: "Google Sans", sans-serif; color: #1f1f1f;
           box-shadow: 0 2px 6px rgba(36,25,25,.10), 0 40px 110px rgba(36,25,25,.26);
           transform-origin: 514px 1000px; }
    #win div, #win img, #win i { position: absolute; }
    #win img { border-radius: 16px; object-fit: cover; }
    .a-h1 { font-size: 66px; font-weight: 700; letter-spacing: -0.01em; white-space: nowrap; }
    .a-sub { font-size: 33px; color: #6f6f6f; }
    .a-ring { width: 146px; height: 146px; border-radius: 50%; border: 8px solid #1F4FA3; text-align: center;
              line-height: 130px; font-size: 52px; font-weight: 700; }
    .a-cap { font-size: 30px; font-weight: 500; letter-spacing: .12em; color: #7a7a7a; }
    .a-plus { width: 74px; height: 74px; border-radius: 50%; background: #1F4FA3; color: #fff; text-align: center;
              line-height: 70px; font-size: 56px; }
    .a-card { background: #fff; border-radius: 42px; border: 1px solid #ECE6E6; box-shadow: 0 2px 6px rgba(0,0,0,.05); }
    .pie { width: 78px; height: 78px; border-radius: 50%; }
    .a-t { font-size: 38px; font-weight: 700; white-space: nowrap; }
    .a-t2 { font-size: 36px; font-weight: 500; white-space: nowrap; }
    .a-m { font-size: 31px; color: #8a8a8a; white-space: nowrap; }
    .a-m2 { font-size: 30px; color: #8a8a8a; white-space: nowrap; }
    .a-tag { position: relative !important; border-radius: 12px; padding: 2px 8px; margin-left: -8px; }
    .a-body { font-size: 31px; color: #6f6f6f; line-height: 1.55; }
    .a-date { height: 56px; padding: 0 22px; border-radius: 28px; background: #F1F1F1; color: #6f6f6f;
              font-size: 28px; line-height: 56px; white-space: nowrap; }
    .a-badge { padding: 2px 16px; border-radius: 10px; background: #F1F1F1; font-size: 27px; color: #6f6f6f; }
    .a-btn { height: 138px; border-radius: 30px; background: #1F4FA3; color: #fff; text-align: center;
             line-height: 138px; font-size: 36px; font-weight: 500; }
    .a-ghost { height: 138px; border-radius: 69px; background: #fff; border: 1px solid #E6E6E6; text-align: center;
               line-height: 136px; font-size: 33px; color: #3c3c3c; }
    .a-more { font-size: 33px; font-weight: 500; color: #1F4FA3; }
    .a-hit { padding: 6px 16px; border-radius: 26px; background: #E5F3E8; color: #3D9A55; font-size: 26px; font-weight: 700; }
    .a-st { font-size: 28px; color: #8a8a8a; white-space: nowrap; }
    .a-st b { font-size: 50px; color: #1f1f1f; font-weight: 700; margin-right: 8px; }
    .a-nav { background: #fff; border-radius: 74px; box-shadow: 0 6px 24px rgba(0,0,0,.10); }
    .a-ni { top: 26px; width: 140px; text-align: center; font-size: 27px; color: #6b6b6b; }
    .a-ni svg { display: block; margin: 0 auto 6px; }
    .a-fab { width: 128px; height: 128px; border-radius: 50%; background: #2A5BB0; color: #fff; text-align: center;
             line-height: 118px; font-size: 84px; box-shadow: 0 10px 30px rgba(31,79,163,.35); }
    .a-rip { width: 128px; height: 128px; border-radius: 50%; border: 6px solid #7A1424; opacity: 0; }
"""
t_dumok, t_hol = S(u"думок,", 21.78), S(u"голосових,", 22.48)
t_stor, t_rils, t_navit = S(u"сторітели", 24.50), S(u"рілси", 26.23), S(u"навіть", 27.60)


def cam(px, py, sc, cx=540, cy=830):
    # the window turns and scales about its own centre (514, 1000): a point p
    # of it lands at O + s*(p - O) + (x, y)
    return (round(cx - 514 - sc * (px - 514), 1), round(cy - 1000 - sc * (py - 1000), 1))


WIDE = (0.55,) + cam(514, 1000, 0.55)
FAB = (1.25,) + cam(513, 1830, 1.25, cy=1040)
STO = (1.15,) + cam(520, 770, 1.15, cy=760)
RIL = (1.15,) + cam(520, 490, 1.15, cy=760)
js(u"""
  gsap.set("#win", {x: %(wx)s, y: %(wy)s + 260, scale: %(ws)s * .86, rotationX: 26, rotationY: -22, rotationZ: 5});
  tl.to("#win", {x: %(wx)s, y: %(wy)s, scale: %(ws)s, rotationX: 10, rotationY: -14, rotationZ: 2, duration: 1.3, ease: "power3.out"}, %(f0)s + .12);
  tl.to("#win", {rotationX: 6, rotationY: -8, rotationZ: 1, duration: 2.2, ease: "sine.inOut"}, %(f0)s + 1.42);
  tl.to("#win", {x: %(ax)s, y: %(ay)s, scale: %(as)s, rotationX: 4, rotationY: 6, rotationZ: 0, duration: 1.1, ease: "power3.inOut"}, %(dumok)s - .55);
  tl.fromTo("#fab", {scale: 1}, X({scale: .86, duration: .14, yoyo: true, repeat: 1, ease: "power2.out"}), %(hol)s);
  tl.fromTo("#rip", {autoAlpha: .9, scale: 1}, X({autoAlpha: 0, scale: 1.9, duration: .6, ease: "power2.out"}), %(hol)s + .05);
  tl.to("#win", {x: %(sx)s, y: %(sy)s, scale: %(ss)s, rotationX: -3, rotationY: -6, duration: 1.1, ease: "power3.inOut"}, %(stor)s - .6);
  tl.to("#lbS", {backgroundColor: "#7A1424", color: "#fff", duration: .25}, %(stor)s);
  tl.to("#win", {x: %(rx)s, y: %(ry)s, scale: %(rs)s, rotationX: 4, rotationY: 5, duration: .9, ease: "power3.inOut"}, %(rils)s - .55);
  tl.to("#lbR", {backgroundColor: "#7A1424", color: "#fff", duration: .25}, %(rils)s);
  tl.to("#win", {x: %(wx)s, y: %(wy)s, scale: %(ws)s, rotationX: 10, rotationY: 14, rotationZ: -2, duration: 1.1, ease: "power3.inOut"}, %(navit)s - .3);
  full(%(f0)s, %(f1)s);
""" % {"wx": WIDE[1], "wy": WIDE[2], "ws": WIDE[0], "ax": FAB[1], "ay": FAB[2], "as": FAB[0],
       "sx": STO[1], "sy": STO[2], "ss": STO[0], "rx": RIL[1], "ry": RIL[2], "rs": RIL[0],
       "f0": "%.3f" % f0, "f1": "%.3f" % f1, "dumok": "%.3f" % t_dumok, "hol": "%.3f" % t_hol,
       "stor": "%.3f" % t_stor, "rils": "%.3f" % t_rils, "navit": "%.3f" % t_navit})
g.sfx("whoosh-short", f0); g.sfx("whoosh-short", t_dumok - 0.55); g.sfx("click", t_hol)
g.sfx("whoosh-short", t_stor - 0.6); g.sfx("click-soft", t_stor); g.sfx("click-soft", t_rils)
g.sfx("whoosh-short", f1)

# 4 · ABOVE — the rest of the list through the slot ----------------------------
OUT = [(u"дизайн каруселей", S(u"дизайн", 29.58)), (u"8 шаблонів", S(u"восьми", 31.26)),
       (u"тредси", S(u"тредси.", 33.90))]
for i, (txt, t) in enumerate(OUT):
    F.append(u'        <div id="ou%d" class="shuf hid"><span class="chip"><i></i>%s</span></div>' % (i, txt))
    g.sfx("pop", t - 0.1)
js(u'  shuffle(["#ou0", "#ou1", "#ou2"], [%s], %.3f);'
   % (", ".join("%.3f" % (t - 0.1) for _, t in OUT), S(u"Цим", 34.50) + 0.4))

# 5 · ABOVE — 70+ людей ------------------------------------------------------------
t_70 = S(u"70", 36.55)
F.append(u'''        <div id="us" class="glass gl hid" style="top:320px; left:0; right:0; margin:auto; width:max-content;
             display:flex; align-items:center; gap:22px; padding:20px 40px">
          <span class="bn">70+</span><span style="font-size:36px; font-weight:500">людей у RUTA</span></div>''')
js(u'  pop("#us", %.3f); sink("#us", %.3f);' % (t_70 - 0.05, S(u"одноголосно", 38.09) + 0.6))
g.sfx("pop", t_70 - 0.05)

# 6 · HALF 1 — Claude: $100 a month, not counted --------------------------------
h0 = S(u"Клод,", 50.6) - 0.3
h1 = E(u"оминаю.", 61.40) + 0.15
HALF.append((h0, h1))
t_100, t_ner, t_rozr, t_rob = S(u"100", 51.95), S(u"рахую,", 54.48), S(u"розробки,", 56.70), S(u"роботи.", 58.64)
js(u'''
  sketch("c1", "skP"); box("c1", 370, 320, 340, 140, {seed: 3, fill: true});
  label("c1", 540, 410, "Claude", {size: 64});
  draw("c1", %.3f);
  sketch("c2", "skP"); label("c2", 540, 560, "$100 / міс", {size: 66, color: "#7A1424"});
  draw("c2", %.3f);
  sketch("c3", "skP"); ln("c3", 380, 548, 700, 530, {stroke: "#7A1424", strokeWidth: 8, seed: 9});
  draw("c3", %.3f, .35);
  sketch("c4", "skP"); arrow("c4", 400, 470, 220, 640, {seed: 5, bend: -.12});
  box("c4", 60, 650, 320, 120, {seed: 7}); label("c4", 220, 726, "розробка", {size: 52});
  draw("c4", %.3f, .5);
  sketch("c5", "skP"); arrow("c5", 680, 470, 860, 640, {seed: 15, bend: .12});
  box("c5", 700, 650, 320, 120, {seed: 17}); label("c5", 860, 726, "робота", {size: 52});
  draw("c5", %.3f, .5);
  erase("c1", %.3f); erase("c2", %.3f); erase("c3", %.3f); erase("c4", %.3f); erase("c5", %.3f);
''' % (h0 + 0.5, t_100 - 0.1, t_ner - 0.05, t_rozr - 0.8, t_rob - 0.8, h1, h1, h1, h1, h1))
g.sfx("whoosh-short", h0); g.sfx("kaching", t_100); g.sfx("click", t_ner)
g.sfx("click-soft", t_rozr); g.sfx("click-soft", t_rob)

# 7 · ABOVE — the hosting card: Supabase + Vercel, free tiers gone, $35 + $20 = $55
t_sb, t_vc = S(u"Supabase", 66.10), S(u"Vercel.", 68.00)
t_free, t_pidh = S(u"на безкоштовному", 69.74), S(u"підходять.", 75.12)
t_35, t_20, t_55 = S(u"35", 77.28), S(u"20.", 79.73), S(u"55", 81.45)
F.append(u'''
        <div id="hc" class="glass gl hid" style="top:300px">
          <div id="hr1" class="rw hid">Supabase <span class="sub">· база даних</span>
            <span class="pr"><span id="fr1" class="free hid">Free<i class="st"></i></span><span id="p35" class="v hid">$35</span></span></div>
          <div id="hr2" class="rw hid">Vercel <span class="sub">· хостинг</span>
            <span class="pr"><span id="fr2" class="free hid">Free<i class="st"></i></span><span id="p20" class="v hid">$20</span></span></div>
          <div id="hr3" class="hid"><div class="rule"></div>
            <div class="rw"><span class="sub">разом на місяць</span><span class="pr"><span class="v">$55</span></span></div></div>
        </div>''')
js(u'''
  rise("#hc", %(sb)s - .35); fadein("#hr1", %(sb)s - .1, .3);
  rise("#hr2", %(vc)s - .1, 30);
  pop("#fr1", %(free)s); pop("#fr2", %(free)s + .12);
  tl.fromTo("#fr1 .st, #fr2 .st", {scaleX: 0}, X({scaleX: 1, duration: .35, ease: "power2.out"}), %(pidh)s);
  tl.to("#fr1, #fr2", {autoAlpha: 0, duration: .3}, %(t35)s - .3);
  pop("#p35", %(t35)s); pop("#p20", %(t20)s);
  gsap.set("#hr3", {maxHeight: 0, overflow: "hidden"});
  tl.fromTo("#hr3", {autoAlpha: 0, maxHeight: 0}, X({autoAlpha: 1, maxHeight: 120, duration: .5, ease: RISE}), %(t55)s - .05);
  sink("#hc", %(end)s);
''' % {"sb": "%.3f" % t_sb, "vc": "%.3f" % t_vc, "free": "%.3f" % t_free, "pidh": "%.3f" % t_pidh,
       "t35": "%.3f" % t_35, "t20": "%.3f" % t_20, "t55": "%.3f" % t_55,
       "end": "%.3f" % (E(u"доларів.", 82.13) + 0.15)})
g.sfx("pop", t_sb - 0.35); g.sfx("pop", t_vc - 0.1); g.sfx("click-soft", t_free); g.sfx("click", t_pidh)
g.sfx("kaching", t_35); g.sfx("kaching", t_20); g.sfx("pop", t_55)

# 8 · HALF 2 — what the AI does: voice -> text; voice / memory / analytics -> script
k0 = S(u"Наступна", 82.73) - 0.1
k1 = E(u"і на аналітиці.", 91.70) + 0.35
HALF.append((k0, k1))
t_hv, t_tx, t_sc = S(u"голосові,", 86.40), S(u"текст,", 87.80), S(u"сценаріїв,", 88.80)
t_hv2, t_pm, t_an = S(u"голосовому,", 90.18), S(u"памʼяті,", 91.18), S(u"і на аналітиці.", 91.70)
js(u'''
  sketch("a1", "skP"); box("a1", 80, 310, 330, 120, {seed: 3}); label("a1", 245, 388, "голосове", {size: 54});
  draw("a1", %.3f, .5);
  sketch("a2", "skP"); arrow("a2", 425, 370, 655, 370, {seed: 5, bend: .05});
  box("a2", 670, 310, 330, 120, {seed: 7}); label("a2", 835, 388, "текст", {size: 54});
  draw("a2", %.3f, .5);
  sketch("a3", "skP"); box("a3", 670, 580, 330, 130, {seed: 11, fill: true}); label("a3", 835, 664, "сценарій", {size: 56});
  draw("a3", %.3f, .5);
  sketch("a4", "skP"); arrow("a4", 330, 440, 660, 600, {seed: 13, bend: -.08});
  draw("a4", %.3f, .45);
  sketch("a5", "skP"); box("a5", 80, 520, 330, 110, {seed: 17}); label("a5", 245, 592, "памʼять", {size: 52});
  arrow("a5", 420, 580, 655, 635, {seed: 19, bend: .04});
  draw("a5", %.3f, .4);
  sketch("a6", "skP"); box("a6", 80, 680, 330, 110, {seed: 23}); label("a6", 245, 752, "аналітика", {size: 52});
  arrow("a6", 420, 735, 655, 680, {seed: 29, bend: -.04});
  draw("a6", %.3f, .4);
  erase("a1", %.3f); erase("a2", %.3f); erase("a3", %.3f); erase("a4", %.3f); erase("a5", %.3f); erase("a6", %.3f);
''' % (t_hv - 0.3, t_tx - 0.75, t_sc - 0.3, t_hv2 - 0.2, t_pm - 0.45, t_an - 0.3, k1, k1, k1, k1, k1, k1))
g.sfx("whoosh-short", k0); g.sfx("click-soft", t_hv); g.sfx("click-soft", t_tx); g.sfx("pop", t_sc)
g.sfx("click-soft", t_pm); g.sfx("click-soft", t_an)

# 9 · ABOVE — what the AI costs: $15–20 for the whole life, ≈ $1,50 per user ----
AI = [(u"ШІ за весь час", u"$15–20", S(u"15–20", 95.50)), (u"1 юзер", u"≈ $1,50", S(u"долар", 100.35))]
for i, (lb, nv, t) in enumerate(AI):
    F.append(u'        <div id="ai%d" class="shuf hid" style="top:320px"><div class="ncard"><span class="lb">%s</span><span class="nv">%s</span></div></div>'
             % (i, lb, nv))
    g.sfx("kaching", t)
js(u'  shuffle(["#ai0", "#ai1"], [%.3f, %.3f], %.3f);' % (AI[0][2] - 0.1, AI[1][2] - 0.1, S(u"круто.", 102.11) + 0.05))

# 10 · ABOVE — the scraper: waits for Meta's API, free for now ------------------
t_skr, t_meta, t_bezk = S(u"скрейпер,", 103.94), S(u"Мета", 108.55), S(u"безкоштовно,", 111.64)
F.append(u'''
        <div id="sc" class="glass gl hid" style="top:300px">
          <div class="rw">Скрейпер <span class="sub">· статистика</span>
            <span class="pr"><span id="scf" class="v hid" style="font-size:34px">безкоштовно</span></span></div>
          <div id="scm" class="rw hid"><span class="meta">%s</span>Meta API <span class="sub">· чекаю доступ</span>
            <span class="pr dots"><i></i><i></i><i></i></span></div>
        </div>''' % mark("meta", 40))
js(u'''
  rise("#sc", %.3f);
  rise("#scm", %.3f, 30);
  tl.fromTo("#scm .dots i", {opacity: .25}, X({opacity: 1, duration: .3, stagger: .15, repeat: 3, yoyo: true}), %.3f);
  pop("#scf", %.3f);
  sink("#sc", %.3f);
''' % (t_skr - 0.2, t_meta - 0.1, t_meta + 0.2, t_bezk, S(u"платформу", 113.54) + 0.3))
g.sfx("pop", t_skr - 0.2); g.sfx("notification", t_meta - 0.1); g.sfx("pop", t_bezk)

# 11 · FULL 2 — the month: costs ≈ $70 vs earnings $60 ---------------------------
m0 = S(u"Загалом,", 116.00) - 0.15
m1 = S(u"Тобто", 122.39) - 0.05
t_70b, t_zar, t_60 = S(u"70", 118.93), S(u"заробляє", 120.23), S(u"60.", 121.30)
C.append(u"""
        <div id="stage2">
          <div id="win2">
            <div class="m-hd"><b>RUTA</b> · за місяць</div>
            <div class="m-row"><span>Витрати</span><span id="mv1" class="m-v hid">≈ $70</span></div>
            <div class="m-tr"><i id="mb1"></i></div>
            <div class="m-row"><span>Заробляє</span><span id="mv2" class="m-v hid">$60</span></div>
            <div class="m-tr"><i id="mb2"></i><u id="mgap"></u></div>
          </div>
        </div>""")
EXTRA += u"""
    #win2 { position: absolute; left: 90px; top: 430px; width: 900px; padding: 56px 60px 64px; background: #fff;
            border-radius: 48px; font-family: "Google Sans", sans-serif; color: #241919;
            box-shadow: 0 2px 6px rgba(36,25,25,.10), 0 40px 110px rgba(36,25,25,.24); transform-origin: 50% 50%; }
    .m-hd { font-size: 40px; color: #574142; margin-bottom: 40px; } .m-hd b { color: #241919; letter-spacing: .02em; }
    .m-row { display: flex; align-items: baseline; justify-content: space-between; font-size: 50px; font-weight: 500; margin-top: 26px; }
    .m-v { font-size: 92px; font-weight: 700; letter-spacing: -0.03em; color: #7A1424; }
    .m-tr { position: relative; height: 44px; border-radius: 22px; background: #F3EAEA; margin-top: 14px; overflow: hidden; }
    .m-tr i, .m-tr u { position: absolute; left: 0; top: 0; height: 44px; border-radius: 22px; transform-origin: 0 50%; transform: scaleX(0); }
    #mb1 { width: 100%; background: #7A1424; }
    #mb2 { width: 85.7%; background: #C98A93; }
    #mgap { left: 85.7%; width: 14.3%; border-radius: 0 22px 22px 0; background: repeating-linear-gradient(-45deg, #7A1424 0 6px, transparent 6px 16px); opacity: 0; transform: none; }
"""
js(u"""
  gsap.set("#stage2", {autoAlpha: 0}); tl.set("#stage2", {autoAlpha: 1}, %(m0)s); tl.set("#stage", {autoAlpha: 0}, %(m0)s);
  gsap.set("#win2", {y: 240, scale: .82, rotationX: 28, rotationY: 18, rotationZ: -4});
  tl.to("#win2", {y: 0, scale: 1, rotationX: 8, rotationY: 10, rotationZ: -1, duration: 1.2, ease: "power3.out"}, %(m0)s + .1);
  tl.to("#win2", {rotationX: 3, rotationY: -6, rotationZ: 0, scale: 1.04, duration: 3.6, ease: "sine.inOut"}, %(m0)s + 1.3);
  tl.to("#mb1", {scaleX: 1, duration: .8, ease: "power3.out"}, %(t70)s - .2); pop("#mv1", %(t70)s);
  tl.to("#mb2", {scaleX: 1, duration: .8, ease: "power3.out"}, %(t60)s - .25); pop("#mv2", %(t60)s);
  tl.to("#mgap", {opacity: 1, duration: .3}, %(t60)s + .5);
  full(%(m0)s, %(m1)s);
""" % {"m0": "%.3f" % m0, "m1": "%.3f" % m1, "t70": "%.3f" % t_70b, "t60": "%.3f" % t_60})
g.sfx("whoosh-short", m0); g.sfx("kaching", t_70b); g.sfx("kaching", t_60); g.sfx("whoosh-short", m1)

# 12 · BEHIND — «мінус», the answer ----------------------------------------------
t_min, e_min = S(u"мінусі.", 123.33), E(u"мінусі.", 123.33)
B.append(u'        <div id="bw2" class="big hid" data-layout-allow-occlusion style="top:440px; font-size:250px">мінус</div>')
g.matte("b2", round(t_min - 0.7, 3), round(e_min - t_min + 1.4, 3))
js(u'  rise("#bw2", %.3f); sink("#bw2", %.3f);' % (t_min - 0.3, e_min + 0.35))
g.sfx("whoosh-short", t_min - 0.3)
BLACKOUT.append((t_min - 0.03, e_min))

# 13 · ABOVE — one more paying user -> нуль (the guess chip comes back) ----------
t_odna, t_nul = S(u"б одна додаткова", 125.23), S(u"нуль.", 127.55)
F.append(u'        <div id="z0" class="shuf hid"><span class="chip"><b>+1</b>людина на тарифі</span></div>')
F.append(u'        <div id="z1" class="shuf hid"><span class="chip"><b>0</b>нуль</span></div>')
EXTRA += u"    #z0 .chip b { width: auto; padding: 0 12px; border-radius: 23px; font-size: 32px; }\n"
js(u'  shuffle(["#z0", "#z1"], [%.3f, %.3f], %.3f);' % (t_odna - 0.1, t_nul - 0.1, t_nul + 0.75))
g.sfx("pop", t_odna - 0.1); g.sfx("pop", t_nul - 0.1)

# 14 · CTA — the comment types RUTA; «Пиши RUTA в коментарях» in the subtitle band
t_pyshy, t_ruta = S(u"пиши", 128.99), S(u"«RUTA»,", 129.5)
t_shukai = S(u"шукай", 132.46)
F.append(u'''
        <div id="cm" class="glass cmt hid"><span class="av"></span>
          <span class="ph" id="cph">Додай коментар…</span>
          <span class="ty hid" id="cty"><span>R</span><span>U</span><span>T</span><span>A</span></span>
          <span class="send">Опублікувати</span></div>''')
F.append(u'''        <div id="ctp" class="pill hid" style="left:0; right:0; margin:auto; width:max-content; top:1404px;
             font-size:46px; padding:28px 56px">Пиши «RUTA» в коментарях</div>''')
F.append(u'''        <div id="ctq" class="pill hid" style="left:0; right:0; margin:auto; width:max-content; top:1404px;
             font-size:46px; padding:28px 56px">Посилання — у профілі</div>''')
js(u'''
  rise("#cm", %(cm)s);
  tl.set("#cph", {display: "none"}, %(ruta)s - .12); tl.set("#cty", {autoAlpha: 1}, %(ruta)s - .12);
  tl.to("#cty span", {opacity: 1, duration: .01, stagger: .11}, %(ruta)s - .1);
  pop("#ctp", %(pyshy)s);
  out("#ctp", %(sh)s - .1); pop("#ctq", %(sh)s + .1);
  sink("#cm", %(sh)s);
''' % {"cm": "%.3f" % (t_pyshy - 0.4), "ruta": "%.3f" % t_ruta, "pyshy": "%.3f" % (t_pyshy - 0.1),
       "sh": "%.3f" % t_shukai})
g.sfx("pop", t_pyshy - 0.1); g.sfx("typing", t_ruta - 0.1); g.sfx("pop", t_shukai + 0.1)
BLACKOUT.append((t_pyshy - 0.15, DUR))

# 15 · MEMES — comic relief after the beat lands (assets/memes/MEMES.md), off every
# other graphic. 52 «gossip»: she is about to spill what the app earns; 14 «and the
# price was…»: right on her question; 35 «deal with it»: $1,50 a user, «дуже круто».
g.cta_start = S(u"Тому", 127.9)
g.meme(F, J, "52", round(E(u"витрати.", 9.1) + 0.1, 3), dur=1.2, slot="top")
g.meme(F, J, "14", round(E(u"додаток?", 48.2) + 0.1, 3), dur=1.15, slot="r")
g.meme(F, J, "35", round(E(u"круто.", 102.1) + 0.1, 3), dur=1.0, slot="r")

# ---------------------------------------------------------------- half screens + their mattes
for i, (a, b) in enumerate(HALF):
    g.matte("half%d" % (i + 1), round(a - 0.1, 3), round(b - a + 1.2, 3))
    js("  half(%.3f, %.3f);" % (a, b))
    PLACE.append((a + 0.4, b + 0.2, "bottom", 938))


def main():
    chunks = g.chunks(CAPS, place=PLACE)
    doc = g.document(title=u"Reel 57 — скільки заробляє RUTA", plate="assets/base.mp4",
                     behind="\n".join(B), panel="\n".join(P), front="\n".join(F), cover="\n".join(C),
                     js="\n".join(J), chunks=chunks, blackout=BLACKOUT, extra_css=EXTRA)
    g.write(HERE, doc)
    print("index.html  %d caption chunks, %d sfx cues, %d mattes" % (len(chunks), len(g.cues), len(g.mattes)))
    if "--words" in sys.argv:
        print(" ".join(u"%s/%.1f" % (c["w"], c["s"]) for c in CAPS))


main()
