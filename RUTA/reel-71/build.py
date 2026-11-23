# -*- coding: utf-8 -*-
"""Reel 71 — «Скільки хвилин займає один рілс, коли система вже налаштована?».
Batch 2026-11-20 (raw 20261120_140447). STYLE.md §00 + her review of reel 61
(2026-11-23): natural editing, few graphics, reel-61's idioms.

The ТЕСТ CTA is cut out (work/r71/cut-fix.json drops raw 97.0 s -> end): the
reel ends on her «…бо все монтується в хмарі», no graphic.

Chain: behind «Монтаж» (cover) -> a card «10–15 хв», struck on «правдива»,
a «?» on «залежить» -> HALF 1, the scheme: сире відео «2–3 хв» -> Клод «15–20 хв»
-> HALF 2, the same scheme, the long video: «5–6 хв», red crosses (помилки),
a cut, «3 хв» -> Клод «30 хв», «1 год» -> shuffle: швидше, ніж самій / швидше,
ніж чекати монтажера / безкоштовно / лише підписка на Клод -> FULL, the phone as
a platform-ad sequence: 10 рілсів go into монтаж, 10 come back ready -> she ends
it on her own («з телефона… в хмарі»).

usage: python3 build.py   (then: sh work/b1021/mattes.sh 71; python3 tools/sfx.py mix 71)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
from gstyle import G, Words, load_caps, mark  # noqa: E402

NN = "71"
DUR = 76.583           # (2298 plate frames - 0.5) / 30
g = G(dur=DUR, reel=NN)
g.cta_start = round(DUR - 2.0, 3)   # no CTA (the ТЕСТ CTA is cut): memes stay off the last 2 s
g.PANEL_TOP = 826      # panel captions: bottom 944, her pushed hair at ≈ 1000

FIX = {
    (u"підтримку!", 0.0): None,          # whisper's «Дякую за підтримку!» over silence — not her
    u"ділса.": u"рілса.", u"сказати": u"сказати,",
    u"тексту": u"текст", u"Флера,": u"з суфлера,", u"понвілок": u"помилок,",
    u"Такі": u"такі", u"анімацій": u"анімацій,", u"менше": u"менше,",
    u"і що,": u"і ще", u"всі": u"в", u"хвилини": u"хвилини,",
    (u"не", 48.5): u"навіть", u"біддак!": u"так!", u"одно": u"одно,",
    (u"Мені", 59.3): u"мені", u"кривосів": u"рілсів,", u"Ви": u"віддати", u"дати": None,
    u"Клоді?": u"Клоді,", u"телефона": u"телефона,", u"пам'ять": u"пам'ять,",
    u"перегріється.": u"перегріється,", u"Повся": u"бо все", u"хмарій.": u"в хмарі.",
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
    .tcard { left: 0; right: 0; margin: auto; width: max-content; top: 330px; padding: 30px 56px;
             display: flex; align-items: center; gap: 30px; }
    .tcard .num { font-size: 120px; position: relative; }
    .tcard .st { position: absolute; left: -10px; right: -10px; top: 52%; height: 12px; margin-top: -6px;
                 border-radius: 6px; background: #241919; transform-origin: 0 50%; transform: scaleX(0); }
    .q { width: 120px; height: 120px; border-radius: 50%; background: #7A1424; color: #fff;
         font-weight: 700; font-size: 84px; line-height: 120px; text-align: center; flex: none; }
'''

# 1 · BEHIND — «Монтаж», the cover frame ----------------------------------------
t_mon, e_mon = S(u"монтаж", 2.1), E(u"монтаж", 2.1)
t_koly = S(u"коли", 3.5)
B.append(u'        <div id="bw1" class="big hid" data-layout-allow-occlusion style="top:540px; font-size:230px">Монтаж</div>')
g.matte("b1", 0.0, round(t_koly + 0.4, 3))
js(u'  rise("#bw1", 0.10); sink("#bw1", %.3f);' % (t_koly - 0.05))
g.sfx("whoosh-short", 0.10)
BLACKOUT.append((t_mon - 0.03, e_mon))

# 2 · ABOVE — «10–15 хв», struck on «правдива», a «?» on «залежить» --------------
t_1015, e_1015 = S(u"10-15", 8.5), E(u"10-15", 8.5)
t_prav, t_zal, e_rils = S(u"правдива,", 12.4), S(u"залежить", 15.4), E(u"рілса.", 16.8)
F.append(u'''
        <div id="tc" class="card tcard hid">
          <span class="num">10–15 хв<i class="st"></i></span><span id="tq" class="q hid">?</span>
        </div>''')
js(u'''
  pop("#tc", %.3f);
  tl.fromTo("#tc .st", {scaleX: 0}, X({scaleX: 1, duration: .35, ease: "power2.out"}), %.3f);
  tl.to("#tc .num", {opacity: .45, duration: .3}, %.3f);
  pop("#tq", %.3f);
  sink("#tc", %.3f);
''' % (t_1015 - 0.08, t_prav, t_prav + 0.2, t_zal, e_rils + 0.1))
g.sfx("pop", t_1015 - 0.08); g.sfx("click", t_prav); g.sfx("pop", t_zal)
BLACKOUT.append((t_1015 - 0.03, e_1015))

# 3 · HALF 1 — the scheme: a short raw video -> Клод -> 15–20 хв -------------------
t_syre, t_23, t_klod, t_1520 = S(u"сире", 24.5), S(u"2-3", 26.6), S(u"Клод", 28.8), S(u"15-20", 29.5)
h1a, h1b = t_syre - 0.45, S(u"Чим", 30.9) + 0.1
HALF.append((h1a, h1b))
js(u'''
  sketch("a1", "skP"); box("a1", 90, 340, 360, 190, {seed: 3}); label("a1", 270, 452, "сире відео", {size: 54});
  draw("a1", %.3f);
  sketch("a2", "skP"); label("a2", 270, 620, "2–3 хв", {size: 72, color: "#7A1424"}); draw("a2", %.3f);
  sketch("a3", "skP"); arrow("a3", 470, 435, 615, 435, {seed: 5, bend: -.12});
  box("a3", 630, 340, 360, 190, {seed: 7, fill: true}); label("a3", 810, 452, "Клод", {size: 60});
  draw("a3", %.3f);
  sketch("a4", "skP"); label("a4", 810, 620, "15–20 хв", {size: 72, color: "#7A1424"}); draw("a4", %.3f);
  erase("a1", %.3f); erase("a2", %.3f); erase("a3", %.3f); erase("a4", %.3f);
''' % (h1a + 0.45, t_23 - 0.05, t_klod - 0.75, t_1520 - 0.05, h1b, h1b, h1b, h1b))
g.sfx("whoosh-short", h1a); g.sfx("click-soft", t_23); g.sfx("click-soft", t_1520)

# 4 · HALF 2 — the same scheme, the long video ------------------------------------
t_yakscho, t_56, t_pom = S(u"А якщо", 33.7), S(u"5-6,", 35.6), S(u"помилок,", 36.6)
t_vyriz, t_try = S(u"вирізати", 37.8), S(u"три", 39.3)
t_zain, t_30, t_god = S(u"зайняти", 40.8), S(u"30", 41.4), S(u"годину.", 42.5)
h2a, h2b = t_yakscho - 0.35, E(u"годину.", 42.5) + 0.35
HALF.append((h2a, h2b))
js(u'''
  sketch("b1", "skP"); box("b1", 90, 340, 360, 190, {seed: 31}); label("b1", 270, 420, "сире відео", {size: 54});
  draw("b1", %.3f);
  sketch("b2", "skP"); label("b2", 270, 620, "5–6 хв", {size: 72, color: "#7A1424"}); draw("b2", %.3f);
  sketch("b3", "skP");
  [175, 270, 365].forEach(function (x, i) {
    ln("b3", x - 18, 468, x + 18, 504, {stroke: "#7A1424", strokeWidth: 6, seed: 40 + i});
    ln("b3", x + 18, 468, x - 18, 504, {stroke: "#7A1424", strokeWidth: 6, seed: 50 + i}); });
  draw("b3", %.3f, .22);
  sketch("b4", "skP"); ln("b4", 425, 310, 425, 560, {stroke: "#7A1424", strokeWidth: 6, seed: 61});
  draw("b4", %.3f, .45);
  sketch("b5", "skP"); ln("b5", 180, 600, 360, 600, {stroke: "#241919", strokeWidth: 6, seed: 63});
  label("b5", 270, 730, "3 хв", {size: 72, color: "#7A1424"}); draw("b5", %.3f, .3);
  sketch("b6", "skP"); arrow("b6", 470, 435, 615, 435, {seed: 65, bend: -.12});
  box("b6", 630, 340, 360, 190, {seed: 67, fill: true}); label("b6", 810, 452, "Клод", {size: 60});
  draw("b6", %.3f);
  sketch("b7", "skP"); label("b7", 810, 620, "30 хв", {size: 72, color: "#7A1424"}); draw("b7", %.3f);
  sketch("b8", "skP"); label("b8", 810, 730, "1 год", {size: 72, color: "#7A1424"});
  ell("b8", 810, 708, 230, 110, {seed: 69, stroke: "#7A1424", strokeWidth: 5, fill: false}); draw("b8", %.3f, .5);
  ["b1", "b2", "b3", "b4", "b5", "b6", "b7", "b8"].forEach(function (n) { erase(n, %.3f); });
''' % (h2a + 0.45, t_56 - 0.05, t_pom, t_vyriz, t_try - 0.3, t_zain - 0.6, t_30 - 0.05, t_god - 0.05, h2b))
g.sfx("whoosh-short", h2a); g.sfx("click-soft", t_56); g.sfx("click", t_pom); g.sfx("click", t_vyriz)
g.sfx("click-soft", t_30); g.sfx("click-soft", t_god)

# 5 · SHUFFLE — why it is worth it, one card at a time ------------------------------
CH = [(u"швидше, ніж самій", S(u"самій,", 52.2) - 0.35),
      (u"швидше, ніж чекати монтажера", S(u"чекати", 53.7) - 0.1),
      (u"безкоштовно", S(u"безкоштовно,", 55.3) - 0.05),
      (u"лише підписка на Клод", S(u"підписку", 57.1) - 0.1)]
sh_end = E(u"Клод.", 57.8) + 0.25
for i, (txt, _) in enumerate(CH):
    F.append(u'        <div id="sh%d" class="shuf hid"><span class="chip"><i></i>%s</span></div>' % (i, txt))
js(u'  shuffle([%s], [%s], %.3f);' % (", ".join('"#sh%d"' % i for i in range(len(CH))),
                                      ", ".join("%.3f" % t for _, t in CH), sh_end))
for _, t in CH:
    g.sfx("pop", t)

# 6 · FULL — her phone as a platform-ad sequence: 10 in, 10 back ready -------------
f0 = S(u"мені", 59.3) - 0.15
t_10a, t_vidd, t_montazh = S(u"10", 61.4), S(u"віддати", 62.6), S(u"монтаж", 63.3)
t_kilka, t_10b, t_hotov = S(u"кілька", 64.7), S(u"10", 66.2), S(u"готових", 66.5)
t_sprav, t_tel = S(u"справами.", 68.4), S(u"телефона,", 70.6)
f1 = S(u"не", 71.1) - 0.1
rows = []
for i in range(10):
    rows.append(u'''            <div class="r" id="r%d"><b class="th"></b><span class="nm">Рілс %02d</span>
              <span class="stt s0">сире відео</span><span class="stt s1">монтаж<em><i></i><i></i><i></i></em></span><span class="stt s2"><span class="check on"></span></span></div>''' % (i, i + 1))
C.append(u"""
        <div id="stage">
          <div id="ph"><div id="scr">
            <div class="hd">%s<span>Claude</span></div>
            <div id="rows">
%s
            </div>
          </div></div>
        </div>""" % (mark("claude", 40), "\n".join(rows)))
EXTRA += u"""
    #cover { background: radial-gradient(120% 80% at 50% 35%, #FFFFFF 0%, #F6EFEF 70%, #F1E7E7 100%); }
    #stage { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; perspective: 2200px; }
    #ph { position: absolute; left: 0; top: 0; width: 440px; height: 820px; border-radius: 60px;
          background: #1E1717; padding: 14px; transform-origin: 0 0; will-change: transform;
          box-shadow: 0 2px 6px rgba(36,25,25,.14), 0 40px 90px rgba(36,25,25,.28); }
    #scr { position: relative; width: 412px; height: 792px; border-radius: 47px; background: #fff;
           overflow: hidden; font-family: "Google Sans", sans-serif; color: #241919; }
    #scr .hd { display: flex; align-items: center; gap: 12px; padding: 50px 26px 16px; font-size: 27px;
               font-weight: 700; color: #7A1424; border-bottom: 1px solid #F0E4E4; }
    #scr .hd span { color: #241919; }
    #rows { padding: 8px 18px; }
    .r { position: relative; display: flex; align-items: center; height: 66px; border-bottom: 1px solid #F4EBEB; }
    .r .th { width: 38px; height: 50px; border-radius: 8px; background: #E9DCDC; flex: none; margin-right: 16px;
             position: relative; }
    .r .th::after { content: ""; position: absolute; left: 14px; top: 17px; border-left: 12px solid #fff;
                    border-top: 8px solid transparent; border-bottom: 8px solid transparent; }
    .r .nm { font-size: 22px; font-weight: 500; }
    .r .stt { position: absolute; right: 4px; top: 0; height: 66px; display: flex; align-items: center;
              font-size: 17px; font-weight: 500; }
    .r .s0 { color: #8A7373; } .r .s1 { color: #7A1424; opacity: 0; } .r .s2 { opacity: 0; }
    .r .s1 em { display: inline-flex; gap: 4px; margin-left: 6px; }
    .r .s1 em i { width: 6px; height: 6px; border-radius: 50%; background: #7A1424; display: block; }
    .r .check { width: 34px; height: 34px; border-radius: 10px; }
    .r .check.on::after { left: 10px; top: 3px; width: 9px; height: 18px; border-width: 0 4px 4px 0; }
"""


def cam(px, py, sc, cx=540, cy=800):
    # the phone turns and scales about its own centre (220, 410): a point p of
    # it lands at O + s*(p - O) + (x, y); put p at (cx, cy)
    return (round(cx - 220 - sc * (px - 220), 1), round(cy - 410 - sc * (py - 410), 1))


WIDE = (1.3,) + cam(220, 410, 1.3)
LIST = (1.8,) + cam(170, 300, 1.8, cy=900)
STAT = (2.1,) + cam(330, 380, 2.1, cy=960)
js(u"""
  gsap.set("#ph", {transformOrigin: "220px 410px"});
  gsap.set("#ph", {x: %(wx)s, y: %(wy)s + 240, scale: %(ws)s * .86, rotationX: 24, rotationY: 20, rotationZ: -5});
  gsap.set(".r", {autoAlpha: 0, x: 40});
  tl.to("#ph", {x: %(wx)s, y: %(wy)s, scale: %(ws)s, rotationX: 8, rotationY: 12, rotationZ: -2, duration: 1.3, ease: "power3.out"}, %(f0)s + .15);
  tl.to("#ph", {x: %(lx)s, y: %(ly)s, scale: %(ls)s, rotationX: 3, rotationY: -6, rotationZ: 0, duration: 1.2, ease: "power3.inOut"}, %(t10a)s - .9);
  tl.to(".r", {autoAlpha: 1, x: 0, duration: .35, ease: "power2.out", stagger: .07}, %(t10a)s - .05);
  tl.to("#ph", {x: %(sx)s, y: %(sy)s, scale: %(ss)s, rotationX: -2, rotationY: 7, duration: 1.2, ease: "power3.inOut"}, %(vidd)s - .4);
  tl.to(".r .s0", {opacity: 0, duration: .2, stagger: .05}, %(mont)s);
  tl.to(".r .s1", {opacity: 1, duration: .2, stagger: .05}, %(mont)s + .1);
  tl.fromTo(".r .s1 em i", {opacity: .25}, X({opacity: 1, duration: .3, repeat: 7, yoyo: true, stagger: .1, ease: "sine.inOut"}), %(mont)s + .4);
  tl.to("#ph", {x: %(wx)s, y: %(wy)s, scale: %(ws)s, rotationX: 6, rotationY: -12, rotationZ: 2, duration: 1.3, ease: "power3.inOut"}, %(kilka)s - .3);
  tl.to(".r .s1", {opacity: 0, duration: .15, stagger: .08}, %(hotov)s - .2);
  tl.fromTo(".r .s2", {opacity: 0, scale: .4}, X({opacity: 1, scale: 1, duration: .35, ease: POP, stagger: .08}), %(hotov)s - .1);
  tl.to("#ph", {rotationX: 10, rotationY: 14, rotationZ: -2, y: %(wy)s - 30, duration: 2.6, ease: "sine.inOut"}, %(sprav)s - .4);
  full(%(f0)s, %(f1)s);
""" % {"wx": WIDE[1], "wy": WIDE[2], "ws": WIDE[0], "lx": LIST[1], "ly": LIST[2], "ls": LIST[0],
       "sx": STAT[1], "sy": STAT[2], "ss": STAT[0], "f0": "%.3f" % f0, "f1": "%.3f" % f1,
       "t10a": "%.3f" % t_10a, "vidd": "%.3f" % t_vidd, "mont": "%.3f" % t_montazh,
       "kilka": "%.3f" % t_kilka, "hotov": "%.3f" % t_hotov, "sprav": "%.3f" % t_sprav})
g.sfx("whoosh-short", f0); g.sfx("whoosh-short", t_10a - 0.9); g.sfx("click-soft", t_10a)
g.sfx("whoosh-short", t_vidd - 0.4); g.sfx("click", t_montazh); g.sfx("whoosh-short", t_kilka - 0.3)
g.sfx("chime", t_hotov - 0.1); g.sfx("whoosh-short", f1)

# 7 · MEMES — comic relief, slapped straight on, in the free stretches ---------------
# 30 «НІХУЯ СОБІ» — the long video can take «навіть годину» (right after half 2 leaves)
g.meme(F, J, "30", round(h2b + 0.05, 3), dur=1.2, slot="top")
# 35 hamster in sunglasses — «Але навіть так!»: still faster, deal with it
g.meme(F, J, "35", round(E(u"так!", 48.7) + 0.1, 3), dur=1.2, slot="r")
# 59 «алівідерчі» — «не прив'язана до комп'ютера»: bye, computer
g.meme(F, J, "59", round(E(u"комп'ютера,", 71.9) + 0.1, 3), dur=1.2, slot="top")

# ---------------------------------------------------------------- half screens + their mattes
for i, (a, b) in enumerate(HALF):
    g.matte("half%d" % (i + 1), round(a - 0.1, 3), round(b - a + 1.2, 3))
    js("  half(%.3f, %.3f);" % (a, b))
    PLACE.append((a + 0.4, b + 0.2, "bottom", 944))


def main():
    chunks = g.chunks(CAPS, place=PLACE)
    doc = g.document(title=u"Reel 71 — скільки хвилин займає один рілс", plate="assets/base.mp4",
                     behind="\n".join(B), panel="\n".join(P), front="\n".join(F), cover="\n".join(C),
                     js="\n".join(J), chunks=chunks, blackout=BLACKOUT, extra_css=EXTRA)
    g.write(HERE, doc)
    print("index.html  %d caption chunks, %d sfx cues, %d mattes" % (len(chunks), len(g.cues), len(g.mattes)))
    print("memes", [(m[0], round(m[1], 2), round(m[2], 2)) for m in g.memes])
    print("half spans", [(round(a, 2), round(b, 2)) for a, b in HALF], "full", round(f0, 2), round(f1, 2))
    print(" ".join("%s/%.1f" % (c["w"], c["s"]) for c in CAPS))


main()
