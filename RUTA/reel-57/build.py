# -*- coding: utf-8 -*-
"""Reel 57 — «Скільки заробляє RUTA». Batch 2026-11-20 (raw 20261120_133314).
STYLE.md §00 with her review of reel 61 (natural editing, fewer graphics).
reel-61/build.py is the skeleton.

The one object is HER GUESS: плюс / мінус / нуль at the start, answered at the
end («мінус» behind her, «нуль» with one more paying user). Only numbers she
says: 70, 100, 35, 20, 55, 15–20, 1,50, 70, 60.

Beats: behind «RUTA» (cover) -> shuffle плюс / мінус / нуль -> FULL 1 her
current app: her real site screen recordings in a phone, cut on her words
(home, braindump, stories, reel, carousels) -> behind: the 10 real reviews pile up -> shuffle каруселі / 8 шаблонів /
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

# 3 · FULL 1 — her CURRENT RUTA app as a platform ad ----------------------------
# The UI is her own screen recordings from ruta.media/ruta-app
# (app-screenshots/site-2026-11/vid-*.mp4, re-encoded by work/r57/appvids.sh to
# reel-57/assets/app/: 30 fps, a keyframe every 15 frames, sped up as named).
# A clean phone floats in 3D; each recording cuts in on her word:
#   home («продюсер в телефоні») -> braindump («думок, голосових») ->
#   stories («сторітели») -> reel («рілси») -> carousel types («каруселі»).
# Nothing is rebuilt or invented: the recordings ARE the UI.
f0 = S(u"Для", 17.93) - 0.15
f1 = E(u"каруселі,", 28.22) + 0.25
c1 = S(u"думок,", 21.78) - 0.08
c2 = S(u"сторітели", 24.50) - 0.08
c3 = S(u"рілси", 26.23) - 0.08
c4 = S(u"каруселі,", 28.22) - 0.08
f_end = f1 + 0.9
# (name, cut in, cut out, where in the re-encoded file it starts)
APPV = [("home", f0, c1, 0.0), ("braindump", c1, c2, 1.6), ("stories", c2, c3, 0.4),
        ("reel", c3, c4, 0.8), ("car-types", c4, f_end, 0.4)]
_LEN = {"home": 7.0, "braindump": 7.9, "stories": 8.03, "reel": 4.83, "car-types": 6.0}
for n, a, b, m in APPV:
    assert m + (b - a) + 0.05 <= _LEN[n], (n, m, b - a)
vids = u"\n".join(
    u'              <video id="av-%s" class="av" src="assets/app/%s.mp4" data-start="%.3f" data-duration="%.3f" '
    u'data-media-start="%.3f" muted playsinline></video>' % (n, n, a, b - a + 0.04, m) for n, a, b, m in APPV)
C.append(u"""
        <div id="stage">
          <div id="win" data-layout-allow-overflow>
            <div id="scr">
%s
            </div>
          </div>
        </div>""" % vids)
EXTRA += u"""
    #cover { background: radial-gradient(120% 80% at 50% 35%, #FFFFFF 0%, #F6EFEF 70%, #F1E7E7 100%); }
    #stage, #stage2 { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; perspective: 2600px; }
    /* a clean phone: thin dark bezel, rounded screen, soft cast */
    #win { position: absolute; left: 0; top: 0; width: 780px; height: 1688px; padding: 16px; border-radius: 104px;
           background: #1d1818; transform-origin: 406px 860px;
           box-shadow: 0 0 0 2px rgba(255,255,255,.35) inset, 0 3px 8px rgba(36,25,25,.14),
                       0 40px 110px rgba(36,25,25,.30); }
    #scr { position: relative; width: 780px; height: 1688px; border-radius: 88px; overflow: hidden; background: #fff; }
    .av { position: absolute; left: 0; top: 0; width: 780px; height: 1688px; object-fit: cover; }
"""
for n, a, b, m in APPV:
    js(u'  tl.set("#av-%s", {autoAlpha: 0}, 0); tl.set("#av-%s", {autoAlpha: 1}, %.3f); tl.set("#av-%s", {autoAlpha: 0}, %.3f);'
       % (n, n, a, n, b + 0.02))


def cam(px, py, sc, cx=540, cy=830):
    # the phone turns and scales about its own centre (406, 860): a point p of
    # it lands at O + s*(p - O) + (x, y)
    return (sc, round(cx - 406 - sc * (px - 406), 1), round(cy - 860 - sc * (py - 860), 1))


def to(t, c, rx, ry, rz, d, ease="power3.inOut"):
    js(u'  tl.to("#win", {x: %s, y: %s, scale: %s, rotationX: %s, rotationY: %s, rotationZ: %s, duration: %s, ease: "%s"}, %.3f);'
       % (c[1], c[2], c[0], rx, ry, rz, d, ease, t))


def bot(sc, cx=540, b=1380):
    # the phone's bottom edge rests at y b, just above the caption band, so a
    # zoom crops its top and never puts her captions over the app
    return cam(406, 860, sc, cx=cx, cy=b - 860 * sc)


WIDE = bot(0.64)
js(u'  gsap.set("#win", {x: %s, y: %s, scale: %s, rotationX: 26, rotationY: -24, rotationZ: 6});'
   % (WIDE[1], WIDE[2] + 300, round(WIDE[0] * .86, 3)))
to(f0 + 0.12, WIDE, 10, -14, 2, 1.3, "power3.out")
to(f0 + 1.45, bot(0.72), 6, -8, 1, 2.0, "sine.inOut")                    # drift in on her home
to(c1 - 0.45, bot(0.92), 3, 7, 0, 0.9)                                    # into the text she speaks
to(c1 + 0.6, bot(0.98), 2, 4, 0, 1.6, "sine.inOut")
to(c2 - 0.45, bot(0.88, cx=560), 5, -9, 1, 0.85)                          # the stories, swing left
to(c3 - 0.45, bot(0.94, cx=520), 3, 8, -1, 0.85)                          # the reel script, swing right
to(c4 - 0.35, bot(0.76), 9, 13, -2, 0.85)                                 # out on the carousel templates
js(u'  full(%.3f, %.3f);' % (f0, f1))
g.sfx("whoosh-short", f0); g.sfx("whoosh-short", c1 - 0.45); g.sfx("click-soft", c1)
g.sfx("whoosh-short", c2 - 0.45); g.sfx("click-soft", c2); g.sfx("click-soft", c3)
g.sfx("click-soft", c4); g.sfx("whoosh-short", f1)

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

# 5b · BEHIND — her ask: "on second 40 just add the reviews behind me so it looks
# like a lot". The 10 real replies (app-screenshots/site-2026-11/r01-r10.webp,
# untouched) pile up behind her head and shoulders from «одноголосно», one every
# ≈0.3 s, and clear before «То скільки ж коштує». Her matte keeps her in front.
t_odn = S(u"одноголосно", 38.09)
t_rv_out = S(u"То", 46.33) - 0.85
# (file, centre x, centre y, width, rotation) — the first ones land clear of the «70+» card
RV = [("r03", 230, 560, 440, -5), ("r04", 840, 520, 470, 4), ("r06", 190, 960, 420, 3),
      ("r07", 880, 900, 410, -4), ("r02", 540, 450, 500, -2), ("r01", 300, 370, 450, 5),
      ("r05", 860, 1170, 420, 6), ("r10", 175, 1250, 380, -6), ("r08", 760, 370, 540, -3),
      ("r09", 540, 600, 560, 2)]
for i, (f, cx, cy, w, rot) in enumerate(RV):
    B.append(u'        <img id="rv%d" class="rv hid" data-layout-allow-occlusion data-layout-allow-overlap src="assets/reviews/%s.webp" '
             u'style="left:%dpx; top:%dpx; width:%dpx">' % (i, f, cx - w // 2, cy, w))
    t = t_odn + 0.02 + i * 0.3
    js(u'  gsap.set("#rv%d", {yPercent: -50, rotation: %d});' % (i, rot))
    js(u'  tl.fromTo("#rv%d", {autoAlpha: 0, scale: .72}, X({autoAlpha: 1, scale: 1, duration: .45, ease: POP}), %.3f);' % (i, t))
    js(u'  tl.to("#rv%d", {autoAlpha: 0, scale: .9, duration: .25, ease: "power2.in"}, %.3f);' % (i, t_rv_out + (9 - i) * 0.035))
    g.sfx("pop", t, db=-6)
EXTRA += u"""
    .rv { position: absolute; border-radius: 18px; background: #fff;
          box-shadow: 0 2px 6px rgba(36,25,25,.12), 0 18px 44px rgba(36,25,25,.22); }
"""
g.matte("rv", round(t_odn - 0.1, 3), round(t_rv_out + 0.65 - (t_odn - 0.1), 3))

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
