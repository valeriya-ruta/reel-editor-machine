# -*- coding: utf-8 -*-
"""Reel 68 — «Які скіли потрібні Claude, щоб він сам монтував відео?».
Batch 2026-11-20 (raw 20261120_135854). STYLE.md §00 + her review of reel 61
(natural editing: one meaningful moment per sentence group).

Chain: behind «Claude» (cover) -> FULL the «шалений список скілів»: a Claude
skills screen floats in 3D and scrolls an endless list, toggles flicking on ->
her cuts carry «кожен рекомендує щось своє» / «насправді ні» -> behind
«Hyperframes» on «один скіл» -> what it does, through one shuffle slot
(дивиться відео · монтує · відеовставки · музика на фон · аудіовставки ·
вжухи і піньки) ending on the same skills row, «hyperframes» switched on, on
«один скіл» -> HALF the scheme: two parts — 1 стиль, 2 хмара -> телефон, the
laptop struck on «без прив'язки» -> «$5–10» pill on her number -> CTA pill
«Підпишись» in the subtitle band.

usage: python3 build.py   (then: sh work/b1021/mattes.sh 68; python3 tools/sfx.py mix 68)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
from gstyle import G, Words, load_caps  # noqa: E402

NN = "68"
DUR = 55.816           # (1675 plate frames - 0.5) / 30
g = G(dur=DUR, reel=NN)
g.PANEL_TOP = 820      # panel captions: bottom 938, her pushed hair below ≈ 980

FIX = {
    u"февна,": u"певна,",
    u"заходом,": u"загалом,", u"якщо...": u"якщо", u"подчитати": u"почитати",
    u"Насправді": u"насправді", u"Коли": u"коли", u"клієнкам": u"клієнткам",
    u"скіл.": u"скіл", u"Hyperframes.": u"Hyperframes.",
    u"дивить": u"дивиться", (u"це", 23.4): None,
    (u"аудіо", 28.2): u"аудіовставки,", (u"вставки,", 28.7): None,
    u"текст.": u"текст,",
    # she said «це дві частини. Перша — це», the aligner put the script's words there
    (u"вже", 35.7): u"дві", (u"не", 36.1): u"частини.", (u"скіли,", 36.4): u"Перша", (u"а", 37.1): u"це",
    u"правильно,": u"правильно.", (u"і", 40.2): u"І", u"вивезти": u"вивести",
    u"хмару": u"хмару,", u"гроші.": u"гроші,",
    (u"5", 50.7): u"5–10", (u"10", 50.9): None,
    u"Якщо": u"якщо", u"корисно": u"корисно,", u"об'яско": u"обов'язково", u"підпишись,": u"підпишись.",
}
CAPS = load_caps(NN, FIX)
W = Words(CAPS)
S, E = W.s, W.e

B, P, F, C, J = [], [], [], [], []
BLACKOUT, PLACE, HALF = [], [], []


def js(s):
    J.append(s)


P.append(u'<svg class="sk" id="skP" data-layout-allow-occlusion width="1080" height="1240" viewBox="0 0 1080 1240"></svg>')
EXTRA = u""

# 1 · BEHIND — «Claude» (the hook and the cover frame) ------------------------------
B.append(u'        <div id="bw1" class="big hid" data-layout-allow-occlusion style="top:530px; font-size:240px">Claude</div>')
g.matte("b1", 0.2, 3.6)
js(u'  rise("#bw1", 0.25); sink("#bw1", %.3f);' % (S(u"шалений", 3.9) - 0.45))
g.sfx("whoosh-short", 0.25)

# 2 · FULL — «шалений список скілів»: a Claude skills screen, an endless list -----------
# No screenshot of hers for this, so a clean plausible settings screen with only
# the labels she says (Claude, Skills) — the rows are grey ghosts, no invented names.
f0 = S(u"шалений", 3.9) - 0.25
f1 = E(u"відео.", 9.2) + 0.05
ROWS = 26
ROW_H = 96
import random
rnd = random.Random(68)
rows = []
for i in range(ROWS):
    tint = ["#F3E6E6", "#ECEFF3", "#EFE9F5", "#E8F1EC", "#F5EFE4"][i % 5]
    rows.append(u'<div class="sr" style="top:%dpx"><i style="background:%s"></i><b style="width:%dpx"></b>'
                u'<s style="width:%dpx"></s><em id="t%d"><u></u></em></div>'
                % (i * ROW_H, tint, rnd.randint(150, 300), rnd.randint(260, 440), i))
C.append(u"""
        <div id="stage">
          <div id="win">
            <div class="cw-top"><span class="cw-dot"></span><span class="cw-dot"></span><span class="cw-dot"></span>
              <span class="cw-app">Claude</span></div>
            <div class="cw-h">Skills</div>
            <div class="cw-search">Search</div>
            <div class="cw-add">+</div>
            <div id="lv"><div id="ls">%s</div></div>
          </div>
        </div>""" % u"".join(rows))
EXTRA += u"""
    #cover { background: radial-gradient(120%% 80%% at 50%% 35%%, #FFFFFF 0%%, #F6EFEF 70%%, #F1E7E7 100%%); }
    #stage { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; perspective: 2200px; }
    #win { position: absolute; left: 0; top: 0; width: 720px; height: 1080px; background: #fff;
           border-radius: 26px; font-family: "Google Sans", sans-serif; color: #1f1f1f; overflow: hidden;
           box-shadow: 0 2px 6px rgba(36,25,25,.10), 0 30px 80px rgba(36,25,25,.22);
           transform-origin: 0 0; will-change: transform; }
    #win > div { position: absolute; }
    .cw-top { left: 0; top: 0; width: 720px; height: 64px; background: #F7F4F2; border-bottom: 1px solid #ECE6E6; }
    .cw-dot { display: inline-block; width: 14px; height: 14px; border-radius: 50%%; background: #DDD5D3;
              margin: 25px 0 0 12px; vertical-align: top; }
    .cw-dot:first-child { margin-left: 26px; }
    .cw-app { position: absolute; left: 0; right: 0; top: 16px; text-align: center; font-size: 26px; font-weight: 500; color: #3c3c3c; }
    .cw-h { left: 40px; top: 96px; font-size: 48px; font-weight: 700; letter-spacing: -0.02em; }
    .cw-search { left: 40px; top: 176px; width: 560px; height: 64px; border-radius: 32px; background: #F4F1F0;
                 font-size: 26px; color: #8a8080; line-height: 64px; padding-left: 34px; }
    .cw-add { left: 616px; top: 176px; width: 64px; height: 64px; border-radius: 50%%; background: #7A1424;
              color: #fff; font-size: 40px; line-height: 60px; text-align: center; }
    #lv { left: 0; top: 270px; width: 720px; height: 810px; overflow: hidden; }
    #ls { position: absolute; left: 0; top: 0; width: 720px; }
    .sr { position: absolute; left: 40px; width: 640px; height: %(rh)dpx; border-bottom: 1px solid #F0EBEA; }
    .sr i { position: absolute; left: 0; top: 22px; width: 52px; height: 52px; border-radius: 14px; }
    .sr b { position: absolute; left: 76px; top: 28px; height: 16px; border-radius: 8px; background: #D9D2D1; }
    .sr s { position: absolute; left: 76px; top: 56px; height: 12px; border-radius: 6px; background: #ECE7E6; text-decoration: none; }
    .sr em { position: absolute; left: 572px; top: 32px; width: 64px; height: 34px; border-radius: 17px; background: #CFC8C7; }
    .sr em u { position: absolute; left: 3px; top: 3px; width: 28px; height: 28px; border-radius: 50%%; background: #fff;
               box-shadow: 0 1px 3px rgba(0,0,0,.25); }
""" % {"rh": ROW_H}
SCROLL = ROWS * ROW_H - 810


def cam(px, py, sc, cx=540, cy=900):
    # the window turns and scales about its own centre (360, 540)
    return (round(cx - 360 - sc * (px - 360), 1), round(cy - 540 - sc * (py - 540), 1))


WIDE = (1.3,) + cam(360, 540, 1.3)
LIST = (1.6,) + cam(360, 640, 1.6)
t_spys, t_klod, t_mont = S(u"список", 4.4), S(u"Клода,", 7.1), S(u"монтувати", 8.7)
js(u"""
  gsap.set("#win", {transformOrigin: "360px 540px"});
  gsap.set("#win", {x: %(wx)s, y: %(wy)s + 240, scale: %(ws)s * .86, rotationX: 26, rotationY: -20, rotationZ: 5});
  tl.to("#win", {x: %(wx)s, y: %(wy)s, scale: %(ws)s, rotationX: 10, rotationY: -12, rotationZ: 2, duration: 1.2, ease: "power3.out"}, %(f0)s + .1);
  tl.to("#win", {x: %(lx)s, y: %(ly)s, scale: %(ls)s, rotationX: 4, rotationY: 8, rotationZ: 0, duration: 1.6, ease: "power3.inOut"}, %(spys)s + .4);
  tl.fromTo("#ls", {y: 0}, X({y: -%(scroll)d, duration: %(sd).3f, ease: "power1.in"}), %(spys)s);
  tl.to("#win", {x: %(wx)s, y: %(wy)s, scale: %(ws)s * .96, rotationX: 12, rotationY: 14, rotationZ: -2, duration: 1.3, ease: "power3.inOut"}, %(mont)s - .9);
  full(%(f0)s, %(f1)s);
""" % {"wx": WIDE[1], "wy": WIDE[2], "ws": WIDE[0], "lx": LIST[1], "ly": LIST[2], "ls": LIST[0],
       "f0": "%.3f" % f0, "f1": "%.3f" % f1, "spys": "%.3f" % t_spys, "mont": "%.3f" % t_mont,
       "scroll": SCROLL, "sd": f1 - t_spys})
# the toggles flick on as their rows pass the middle of the screen — one more, one more
sd = f1 - t_spys
for i in range(ROWS):
    # power1.in: y(t) = SCROLL * u^2; a row reaches 400 px into the view when SCROLL*u^2 = i*ROW_H - 400
    need = i * ROW_H - 400
    u = (max(need, 0) / float(SCROLL)) ** 0.5 if need > 0 else 0.25 + i * 0.12
    if u > 1:
        continue
    t = t_spys + u * sd
    js(u'  tl.to("#t%d", {backgroundColor: "#7A1424", duration: .15}, %.3f); tl.to("#t%d u", {x: 30, duration: .2, ease: "back.out(2)"}, %.3f);'
       % (i, t, i, t))
g.sfx("whoosh-short", f0); g.sfx("whoosh-short", t_spys + 0.4); g.sfx("whoosh-short", f1)
for k in range(5):
    g.sfx("click-soft", t_spys + 0.5 + k * 0.85, db=-4)

# 3 · BEHIND — «Hyperframes», on «один скіл — це hyperframes» -------------------------
t_odyn, t_hf, e_hf = S(u"один", 20.1), S(u"Hyperframes.", 20.9), E(u"Hyperframes.", 20.9)
B.append(u'        <div id="bw2" class="big hid" data-layout-allow-occlusion style="top:590px; font-size:150px">Hyperframes</div>')
g.matte("b2", round(t_odyn - 0.4, 3), round(e_hf - t_odyn + 1.1, 3))
js(u'  rise("#bw2", %.3f); sink("#bw2", %.3f);' % (t_odyn - 0.15, e_hf + 0.35))
g.sfx("whoosh-short", t_odyn - 0.15)
BLACKOUT.append((t_hf - 0.03, e_hf))

# 4 · ABOVE — what the one skill does, through one shuffle slot; it ends on the
# skills row from the screen, «hyperframes», switched on at «один скіл» ------------
LIST_ITEMS = [(u"дивиться відео", S(u"дивиться", 23.1)), (u"монтує", S(u"монтує", 24.3)),
              (u"відеовставки", S(u"відеовставки,", 25.3)), (u"музика на фон", S(u"музику", 26.4)),
              (u"аудіовставки", S(u"аудіовставки,", 28.2)), (u"вжухи і піньки", S(u"вжухи", 29.3))]
sels, times = [], []
for i, (txt, t) in enumerate(LIST_ITEMS):
    F.append(u'        <div id="sh%d" class="shuf hid"><span class="chip"><i></i>%s</span></div>' % (i, txt))
    sels.append("#sh%d" % i); times.append(t - 0.1)
    g.sfx("pop", t - 0.1, db=-2)
t_odyn2 = S(u"один", 32.4)
F.append(u'''        <div id="shH" class="shuf hid"><span class="chip hfrow"><b class="hi"></b>hyperframes<em id="tH"><u></u></em></span></div>''')
sels.append("#shH"); times.append(S(u"робить", 31.9) - 0.1)
EXTRA += u"""
    .hfrow { gap: 20px !important; }
    .hfrow .hi { width: 46px; height: 46px; border-radius: 13px; background: #F3E6E6; display: inline-block; }
    .hfrow em { position: relative; width: 64px; height: 34px; border-radius: 17px; background: #CFC8C7; margin-left: 10px; }
    .hfrow em u { position: absolute; left: 3px; top: 3px; width: 28px; height: 28px; border-radius: 50%; background: #fff;
                  box-shadow: 0 1px 3px rgba(0,0,0,.25); }
"""
shuf_end = E(u"скіл.", 32.8) + 0.45
js(u'  shuffle(%s, [%s], %.3f);' % (str(sels).replace("'", '"'), ", ".join("%.3f" % t for t in times), shuf_end))
js(u'  tl.to("#tH", {backgroundColor: "#7A1424", duration: .15}, %.3f); tl.to("#tH u", {x: 30, duration: .25, ease: "back.out(2)"}, %.3f);'
   % (t_odyn2, t_odyn2))
g.sfx("pop", times[-1]); g.sfx("click", t_odyn2)

# 5 · HALF — the scheme: two parts. 1 стиль; 2 хмара -> телефон, the laptop struck --
k0 = S(u"це", 35.6) - 0.15
k1 = E(u"комп'ютера.", 46.2) + 0.05
HALF.append((k0, k1))
t_dvi, t_instr, t_garno = S(u"дві", 35.7), S(u"інструкції", 37.2), S(u"гарно", 39.2)
t_druhe, t_hmaru, t_tel = S(u"друге", 40.5), S(u"хмару,", 42.1), S(u"телефона,", 43.8)
t_bez, t_komp = S(u"без", 45.2), S(u"комп'ютера.", 46.2)
CLOUD = (u"M650 470 C600 470 590 410 640 400 C640 350 710 340 735 375 C760 330 840 335 850 385 "
         u"C900 380 925 440 880 470 Z")
js(u'''
  sketch("s1", "skP");
  box("s1", 90, 310, 430, 230, {seed: 3}); label("s1", 128, 372, "1", {size: 60, anchor: "start", color: "#7A1424"});
  box("s1", 560, 310, 430, 230, {seed: 5}); label("s1", 598, 372, "2", {size: 60, anchor: "start", color: "#7A1424"});
  draw("s1", %(dvi).3f, .6);
  sketch("s2", "skP");
  box("s2", 160, 400, 290, 110, {seed: 7, fill: true, r: 20});
  label("s2", 305, 472, "стиль", {size: 56});
  draw("s2", %(instr).3f, .55);
  sketch("s2b", "skP"); under("s2b", 170, 528, 440, {stroke: "#7A1424", strokeWidth: 6, seed: 8});
  draw("s2b", %(garno).3f, .5);
  sketch("s3", "skP"); blob("s3", "%(cloud)s", [590, 335, 335, 140], {seed: 11});
  label("s3", 760, 448, "хмара", {size: 52});
  draw("s3", %(hmaru).3f, .7);
  sketch("s4", "skP");
  arrow("s4", 690, 545, 540, 690, {seed: 15, bend: -.18});
  box("s4", 400, 620, 120, 200, {seed: 17, r: 22});
  ln("s4", 440, 798, 480, 798, {seed: 18, strokeWidth: 5});
  label("s4", 375, 735, "телефон", {size: 46, anchor: "end"});
  draw("s4", %(tel).3f, .55);
  sketch("s5", "skP");
  box("s5", 740, 640, 210, 125, {seed: 19, r: 14}); ln("s5", 700, 785, 990, 785, {seed: 21, strokeWidth: 6});
  draw("s5", %(bez).3f, .5);
  sketch("s6", "skP");
  ln("s6", 715, 620, 975, 800, {stroke: "#7A1424", strokeWidth: 8, seed: 23});
  ln("s6", 715, 800, 975, 620, {stroke: "#7A1424", strokeWidth: 8, seed: 25});
  draw("s6", %(komp).3f, .3);
  ["s1", "s2", "s2b", "s3", "s4", "s5", "s6"].forEach(function (n) { erase(n, %(k1).3f); });
''' % {"dvi": t_dvi - 0.1, "instr": t_instr - 0.2, "garno": t_garno, "cloud": CLOUD, "hmaru": t_hmaru - 0.5,
       "tel": t_tel - 0.5, "bez": t_bez - 0.2, "komp": S(u"прив'язки", 45.7) + 0.1, "k1": k1})
g.sfx("whoosh-short", k0); g.sfx("click-soft", t_dvi); g.sfx("click-soft", t_instr)
g.sfx("click-soft", t_hmaru); g.sfx("click-soft", t_tel); g.sfx("click", S(u"прив'язки", 45.7) + 0.1)

# 6 · ABOVE — her number: «5–10 доларів я вам зекономила» ----------------------------
t_510, t_tomu = S(u"5–10", 50.7), S(u"Тому", 52.7)
F.append(u'''        <div id="usd" class="pill light hid" style="left:0; right:0; margin:auto; width:max-content; top:360px;
             font-size:52px; padding:24px 48px"><b style="color:#7A1424; font-weight:700">$5–10</b>&nbsp;зекономлено</div>''')
js(u'  pop("#usd", %.3f); out("#usd", %.3f);' % (t_510 - 0.05, t_tomu - 0.2))
g.sfx("kaching", t_510)

# 7 · CTA — «Підпишись», the pill in the subtitle band --------------------------------
t_ob = S(u"обов'язково", 54.6)
F.append(u'''        <div id="ctp" class="pill hid" style="left:0; right:0; margin:auto; width:max-content; top:1404px;
             font-size:52px; padding:28px 64px">Підпишись</div>''')
js(u'  pop("#ctp", %.3f);' % (t_ob - 0.05))
g.sfx("pop", t_ob - 0.05)
BLACKOUT.append((t_ob - 0.08, DUR))

# ---------------------------------------------------------------- half screen + its matte
for i, (a, b) in enumerate(HALF):
    g.matte("half1", round(a - 0.1, 3), round(b - a + 1.2, 3))
    js("  half(%.3f, %.3f);" % (a, b))
    PLACE.append((a + 0.4, b + 0.2, "bottom", 938))


def main():
    chunks = g.chunks(CAPS, place=PLACE)
    doc = g.document(title=u"Reel 68 — один скіл", plate="assets/base.mp4",
                     behind="\n".join(B), panel="\n".join(P), front="\n".join(F), cover="\n".join(C),
                     js="\n".join(J), chunks=chunks, blackout=BLACKOUT, extra_css=EXTRA)
    g.write(HERE, doc)
    print("index.html  %d caption chunks, %d sfx cues, %d mattes" % (len(chunks), len(g.cues), len(g.mattes)))


if __name__ == "__main__" or True:
    main()
