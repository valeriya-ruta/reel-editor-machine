# -*- coding: utf-8 -*-
"""Reel 67 — «Що робити, якщо менеджерка відповідає клієнтам по 5 годин?».
Batch 2026-11-20 (raw 20261120_135706). STYLE.md §00 + her review of reel 61
(2026-11-23): natural editing, one meaningful moment per sentence group, big
words behind her, the real-UI moment as a full-screen platform ad, Excalidraw
only for the scheme (the half screen), a little glass, no arrows over her
footage, the CTA pill in the subtitle band.

Beats: behind «менеджерка» -> glass DM, she answers -> glass DM 2, offline,
«ок.» struck, the card drops on «дно» -> behind «AI-агент» -> FULL the agent's
inbox (asks, the client card fills, «Передати менеджеру» -> «Передано») ->
HALF the three modes (24/7 · manager first, else agent · only at night) ->
glass DM 3, the agent answers at once -> CTA pill.

usage: python3 build.py   (then: sh work/b1021/mattes.sh 67; python3 tools/sfx.py mix 67)
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
from gstyle import G, Words, load_caps  # noqa: E402

NN = "67"


def plate_dur():
    n = int(subprocess.check_output(
        ["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v", "-show_entries",
         "stream=nb_read_packets", "-of", "csv=p=0", os.path.join(HERE, "assets", "voice.mp4")]).strip())
    return int((n - 0.5) / 30.0 * 1000) / 1000.0, n


DUR, FRAMES = plate_dur()
g = G(dur=DUR, reel=NN)
g.PANEL_TOP = 820      # panel captions: bottom 938, her pushed hair below

FIX = {
    u"кажуть": u"каже", u"друсла!": u"доросла!", (u"мене", 8.7): None, u"журку,": u"менеджерку,",
    u"вона вона буде": u"вона буде", (u"А", 19.3): u"я", u"і всіх": u"у всіх",
    u"третць": u"треш,", u"«Пробувай": u"«пробиває",
    (u"і", 33.7): None, u"яй": u"AI-агента.", u"агенти.": None, u"Не": u"не",
    (u"по", 45.9): u"по-різному,", u"різному,": None, u"побачила": u"побачила,",
    u"Якщо": u"якщо", (u"тобі", 56.8): u"тебе", (u"ай", 57.9): u"AI-агент", (u"ай", 58.1): None, (u"агент", 58.3): None,
    u"в дирекці.": u"в директ.", u"далі.": u"деталі.",
}
CAPS = load_caps(NN, FIX)
W = Words(CAPS)
S, E = W.s, W.e

B, P, F, C, J = [], [], [], [], []
BLACKOUT, PLACE, HALF = [], [], []
g.cta_start = S(u"Тому", 56.3)      # «Тому якщо тебе зацікавив…» — no meme from here on


def js(s):
    J.append(s)


P.append(u'<svg class="sk" id="skP" data-layout-allow-occlusion width="1080" height="1240" viewBox="0 0 1080 1240"></svg>')

EXTRA = u'''
    .dm { left: 150px; top: 300px; width: 780px; padding: 26px 28px; }
    .dm .hd { display: flex; align-items: center; gap: 14px; font-size: 26px; font-weight: 500;
              color: #574142; margin-bottom: 18px; }
    .dm .hd b { width: 40px; height: 40px; border-radius: 50%; background: #7A1424; display: inline-block; }
    .dm .hd em { margin-left: auto; font-style: normal; font-size: 24px; color: #574142;
                 display: inline-flex; align-items: center; gap: 8px; }
    .dm .hd em i { width: 12px; height: 12px; border-radius: 50%; background: #9E9E9E; display: inline-block; }
    .bub { display: inline-block; border-radius: 26px; padding: 16px 24px; font-size: 34px;
           font-weight: 500; line-height: 1.25; position: relative; }
    .bub.in { background: rgba(255,255,255,.92); color: #241919; border-bottom-left-radius: 8px; }
    .bub.me { background: #7A1424; color: #fff; border-bottom-right-radius: 8px; }
    .bub .st { position: absolute; left: 18px; right: 18px; top: 50%; height: 4px; margin-top: -2px;
               border-radius: 2px; background: #fff; transform-origin: 0 50%; transform: scaleX(0); }
    .rowr { display: flex; justify-content: flex-end; margin-top: 14px; }
'''

# 1 · BEHIND — «менеджерка» (the hire) ------------------------------------------------
t_men, e_klient = S(u"менеджерку,", 8.9), E(u"клієнтам.", 11.6)
B.append(u'        <div id="bw1" class="big hid" data-layout-allow-occlusion style="top:545px; font-size:165px">менеджерка</div>')
js(u'  rise("#bw1", %.3f); sink("#bw1", %.3f);' % (t_men - 0.15, e_klient + 0.1))
g.matte("b1", round(t_men - 0.4, 3), round(e_klient + 0.5 - (t_men - 0.4), 3))
g.sfx("whoosh-short", t_men - 0.15)
BLACKOUT.append((t_men - 0.03, E(u"менеджерку,", 8.9)))

# 2 · ABOVE — glass DM: a good manager answers ----------------------------------------
t_buvaie, t_vidp, t_bude = S(u"Буває,", 13.7), S(u"відповідає.", 17.3), E(u"буде.", 20.5)
F.append(u'''
        <div id="d1" class="glass dm hid">
          <div class="hd"><b></b>Direct · Менеджерка</div>
          <div><span class="bub in">Добрий день! Скільки коштує?</span></div>
          <div class="rowr"><span class="bub me hid" id="d1a">Добрий день! Зараз усе розповім</span></div>
        </div>''')
js(u'''
  rise("#d1", %.3f);
  pop("#d1a", %.3f);
  sink("#d1", %.3f);
''' % (t_buvaie, t_vidp, t_bude + 0.15))
g.sfx("pop", t_buvaie); g.sfx("notification", t_vidp)

# 3 · ABOVE — the same chat on a bad day: offline -> «ок.» -> it falls on «дно» --------
t_ale, t_zakh, t_fign, t_dno = S(u"Але", 21.3), S(u"захворіла,", 22.4), S(u"фігню", 25.9), S(u"дно».", 29.0)
F.append(u'''
        <div id="d2" class="glass dm hid">
          <div class="hd"><b></b>Direct · Менеджерка<em id="d2o" class="hid"><i></i>не в мережі</em></div>
          <div><span class="bub in">А доставка у вас є?</span></div>
          <div class="rowr"><span class="bub me hid" id="d2a">ок.<i class="st"></i></span></div>
        </div>''')
js(u'''
  rise("#d2", %.3f);
  fadein("#d2o", %.3f);
  pop("#d2a", %.3f);
  tl.fromTo("#d2a .st", {scaleX: 0}, X({scaleX: 1, duration: .3, ease: "power2.out"}), %.3f);
  tl.to("#d2a", {keyframes: {x: [0, -8, 7, -4, 2, 0]}, duration: .35, ease: "none"}, %.3f);
  tl.to("#d2", {y: 1300, rotation: 8, autoAlpha: 0, duration: .8, ease: "power3.in"}, %.3f);
''' % (t_ale, t_zakh, t_fign, t_fign + 0.45, t_fign + 0.45, t_dno - 0.35))
g.sfx("pop", t_ale); g.sfx("click-soft", t_zakh); g.sfx("notification", t_fign)
g.sfx("click", t_fign + 0.45); g.sfx("whoosh-short", t_dno - 0.35)

# 4 · BEHIND — «AI-агент» (the cover frame) ---------------------------------------------
t_ai, e_ai = S(u"AI-агента.", 34.0), E(u"AI-агента.", 34.0)
t_rob = E(u"роботу.", 36.7)
B.append(u'        <div id="bw2" class="big hid" data-layout-allow-occlusion style="top:470px; font-size:240px">AI-агент</div>')
js(u'  rise("#bw2", %.3f); sink("#bw2", %.3f);' % (t_ai - 0.25, t_rob - 0.2))
g.matte("b2", round(t_ai - 0.5, 3), round(t_rob + 0.3 - (t_ai - 0.5), 3))
g.sfx("whoosh-short", t_ai - 0.25)
BLACKOUT.append((t_ai - 0.03, e_ai))

# 5 · FULL — the agent's inbox as a platform ad -----------------------------------------
# No screenshot of hers for this one: a clean, plausible inbox with only what she
# names — it asks (кваліфікує), the client card fills (збирає інформацію), the
# hand-off button flips (передає менеджеру). Window coordinates are its own px.
f0 = S(u"Він", 37.1) - 0.15
f1 = E(u"опрацювання.", 43.8) + 0.2
t_kval, t_zbyr, t_info = S(u"кваліфікує,", 38.8), S(u"збирає", 39.9), S(u"інформацію", 40.3)
t_pered, t_menedzh, t_fin = S(u"передає", 41.3), S(u"менеджеру", 42.3), S(u"фінальне", 43.3)
C.append(u"""
        <div id="stage">
          <div id="win">
            <div class="ib-top"><b></b>Direct<span class="ib-ag"><i></i>AI-агент</span></div>
            <div class="ib-chat">
              <div class="ib-m in">Добрий день! Хочу дізнатись про ваші послуги</div>
              <div class="ib-m me hid" id="m1">Вітаю! Підкажіть, будь ласка, яка у вас ніша?</div>
              <div class="ib-m in hid" id="m2">Салон краси</div>
              <div class="ib-m me hid" id="m3">Дякую! Що хочете покращити?</div>
            </div>
            <div class="ib-card" id="card">
              <div class="ib-h">Картка клієнта</div>
              <div class="ib-f"><span>Ніша</span><em id="v1">Салон краси</em></div>
              <div class="ib-f"><span>Запит</span><em id="v2">Послуги</em></div>
              <div class="ib-f"><span>Статус</span><em id="v3">Кваліфіковано</em></div>
              <div class="ib-btn" id="btn"><span id="bt0">Передати менеджеру</span><span id="bt1" class="hid">✓ Передано менеджеру</span></div>
            </div>
          </div>
        </div>""")
EXTRA += u"""
    #cover { background: radial-gradient(120% 80% at 50% 35%, #FFFFFF 0%, #F6EFEF 70%, #F1E7E7 100%); }
    #stage { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; perspective: 2200px; }
    #win { position: absolute; left: 0; top: 0; width: 800px; height: 560px; background: #fff;
           border-radius: 16px; font-family: "Google Sans", sans-serif; color: #1f1f1f; overflow: hidden;
           box-shadow: 0 2px 6px rgba(36,25,25,.10), 0 30px 80px rgba(36,25,25,.22);
           transform-origin: 0 0; will-change: transform; }
    #win > div { position: absolute; }
    .ib-top { left: 0; top: 0; width: 800px; height: 56px; border-bottom: 1px solid #ECE6E6;
              display: flex; align-items: center; gap: 12px; padding: 0 20px; font-size: 18px; font-weight: 700; }
    .ib-top b { width: 30px; height: 30px; border-radius: 50%; background: #7A1424; display: inline-block; }
    .ib-ag { margin-left: auto; font-size: 13px; font-weight: 500; color: #574142; background: #F4F1F1;
             border-radius: 14px; padding: 6px 12px; display: inline-flex; align-items: center; gap: 7px; }
    .ib-ag i { width: 8px; height: 8px; border-radius: 50%; background: #1EA672; display: inline-block; }
    .ib-chat { left: 20px; top: 76px; width: 440px; display: flex; flex-direction: column; gap: 10px; }
    .ib-m { max-width: 330px; border-radius: 16px; padding: 10px 14px; font-size: 14px; line-height: 1.35; }
    .ib-m.in { background: #F1EEEE; color: #241919; align-self: flex-start; border-bottom-left-radius: 5px; }
    .ib-m.me { background: #7A1424; color: #fff; align-self: flex-end; border-bottom-right-radius: 5px; }
    .ib-card { left: 484px; top: 76px; width: 296px; height: 400px; border: 1px solid #ECE6E6; border-radius: 14px;
               padding: 16px; background: #FCFAFA; }
    .ib-h { font-size: 15px; font-weight: 700; margin-bottom: 14px; }
    .ib-f { border: 1px solid #E3DCDC; border-radius: 10px; background: #fff; padding: 8px 12px; margin-bottom: 10px;
            height: 54px; }
    .ib-f span { display: block; font-size: 11px; color: #6f6363; margin-bottom: 3px; }
    .ib-f em { display: block; font-style: normal; font-size: 14px; color: #241919; opacity: 0; }
    .ib-btn { position: absolute; left: 16px; right: 16px; bottom: 16px; height: 46px; border-radius: 23px;
              background: #7A1424; color: #fff; font-size: 14px; font-weight: 500; text-align: center; line-height: 46px; }
    .ib-btn span { position: absolute; left: 0; right: 0; }
"""
# camera: the window turns and scales about its own centre (400, 280); a point p of
# it lands at O + s*(p - O) + (x, y). Each shot centres a point at (cx, cy).
def cam(px, py, sc, cx=540, cy=760):
    return (round(cx - 400 - sc * (px - 400), 1), round(cy - 280 - sc * (py - 280), 1))
WIDE = (1.25,) + cam(400, 280, 1.25)
CHAT = (2.05,) + cam(240, 190, 2.05)
CARD = (2.3,) + cam(632, 210, 2.3)
BTN = (2.9,) + cam(632, 440, 2.9)
js(u"""
  gsap.set("#win", {transformOrigin: "400px 280px"});
  gsap.set("#win", {x: %(wx)s, y: %(wy)s + 220, scale: %(ws)s * .86, rotationX: 24, rotationY: -20, rotationZ: 5});
  tl.to("#win", {x: %(wx)s, y: %(wy)s, scale: %(ws)s, rotationX: 9, rotationY: -12, rotationZ: 2, duration: 1.2, ease: "power3.out"}, %(f0)s + .15);
  tl.to("#win", {x: %(cx)s, y: %(cy)s, scale: %(cs)s, rotationX: 4, rotationY: 8, rotationZ: 0, duration: 1.0, ease: "power3.inOut"}, %(kval)s - .55);
  pop("#m1", %(kval)s);
  pop("#m2", %(kval)s + .55);
  tl.to("#win", {x: %(dx)s, y: %(dy)s, scale: %(ds)s, rotationX: 2, rotationY: -8, duration: 1.0, ease: "power3.inOut"}, %(zbyr)s - .45);
  tl.to("#v1", {opacity: 1, duration: .25}, %(info)s);
  tl.to("#v2", {opacity: 1, duration: .25}, %(info)s + .3);
  tl.to("#v3", {opacity: 1, duration: .25}, %(info)s + .6);
  pop("#m3", %(info)s + .2);
  tl.to("#win", {x: %(bx)s, y: %(by)s, scale: %(bs)s, rotationX: -3, rotationY: 6, duration: 1.0, ease: "power3.inOut"}, %(pered)s - .45);
  tl.to("#btn", {backgroundColor: "#1EA672", duration: .25}, %(men)s);
  tl.to("#bt0", {autoAlpha: 0, duration: .15}, %(men)s);
  tl.to("#bt1", {autoAlpha: 1, duration: .2}, %(men)s + .05);
  tl.fromTo("#btn", {scale: 1}, X({scale: 1.06, duration: .18, yoyo: true, repeat: 1, ease: "power2.out"}), %(men)s);
  tl.to("#win", {x: %(wx)s, y: %(wy)s, scale: %(ws)s, rotationX: 10, rotationY: 14, rotationZ: -2, duration: 1.1, ease: "power3.inOut"}, %(fin)s - .35);
  full(%(f0)s, %(f1)s);
""" % {"wx": WIDE[1], "wy": WIDE[2], "ws": WIDE[0], "cx": CHAT[1], "cy": CHAT[2], "cs": CHAT[0],
       "dx": CARD[1], "dy": CARD[2], "ds": CARD[0], "bx": BTN[1], "by": BTN[2], "bs": BTN[0],
       "f0": "%.3f" % f0, "f1": "%.3f" % f1, "kval": "%.3f" % t_kval, "zbyr": "%.3f" % t_zbyr,
       "info": "%.3f" % t_info, "pered": "%.3f" % t_pered, "men": "%.3f" % t_menedzh, "fin": "%.3f" % t_fin})
g.sfx("whoosh-short", f0); g.sfx("notification", t_kval); g.sfx("whoosh-short", t_zbyr - 0.45)
g.sfx("typing", t_info); g.sfx("whoosh-short", t_pered - 0.45); g.sfx("click", t_menedzh)
g.sfx("whoosh-short", f1)

# 6 · HALF — the scheme (Excalidraw): three ways it works --------------------------------
k0 = S(u"працювати", 44.9) - 0.25
k1 = E(u"сплять.", 55.8) + 0.15
HALF.append((k0, k1))
t_tsil, t_shans, t_ne, t_sam, t_vnochi = (S(u"цілодобово,", 46.9), S(u"шанс", 49.0), S(u"побачила,", 51.9),
                                          S(u"сам,", 53.2), S(u"вночі,", 54.7))
js(u'''
  sketch("h1", "skP"); box("h1", 360, 380, 360, 170, {seed: 3, fill: true});
  label("h1", 540, 488, "24/7", {size: 84});
  draw("h1", %(tsil)s - .5);
  erase("h1", %(shans)s - .45);
  sketch("h2", "skP"); box("h2", 70, 330, 280, 120, {seed: 5});
  label("h2", 210, 406, "клієнт", {size: 50});
  arrow("h2", 365, 390, 700, 390, {seed: 7, bend: -.12});
  box("h2", 715, 330, 300, 120, {seed: 9}); label("h2", 865, 406, "менеджерка", {size: 46});
  draw("h2", %(shans)s - .3, .45);
  sketch("h3", "skP"); ln("h3", 480, 330, 590, 450, {stroke: "#7A1424", strokeWidth: 7, seed: 11});
  ln("h3", 480, 450, 590, 330, {stroke: "#7A1424", strokeWidth: 7, seed: 13});
  draw("h3", %(ne)s - .1, .3);
  sketch("h4", "skP"); arrow("h4", 230, 465, 700, 680, {seed: 15, bend: .25});
  box("h4", 715, 620, 300, 120, {seed: 17, fill: true}); label("h4", 865, 696, "агент", {size: 52});
  draw("h4", %(sam)s - .55, .4);
  erase("h2", %(vn)s - .4); erase("h3", %(vn)s - .4); erase("h4", %(vn)s - .4);
  sketch("h5", "skP"); box("h5", 300, 380, 480, 170, {seed: 19, fill: true});
  label("h5", 540, 485, "тільки вночі", {size: 64});
  draw("h5", %(vn)s - .3, .4);
  erase("h5", %(k1)s);
''' % {"tsil": "%.3f" % t_tsil, "shans": "%.3f" % t_shans, "ne": "%.3f" % t_ne, "sam": "%.3f" % t_sam,
       "vn": "%.3f" % t_vnochi, "k1": "%.3f" % k1})
g.sfx("whoosh-short", k0); g.sfx("click-soft", t_tsil); g.sfx("click", t_ne)
g.sfx("click-soft", t_sam); g.sfx("click-soft", t_vnochi)

# 7 · ABOVE — glass DM 3: now the agent answers at once ----------------------------------
t_tomu, t_dopom = S(u"Тому", 56.3), E(u"допоможе,", 60.1)
F.append(u'''
        <div id="d3" class="glass dm hid">
          <div class="hd"><b></b>Direct · AI-агент<em><i style="background:#1EA672"></i>онлайн</em></div>
          <div><span class="bub in">А доставка у вас є?</span></div>
          <div class="rowr"><span class="bub me hid" id="d3a">Так! Підкажіть, у яке місто?</span></div>
        </div>''')
js(u'''
  rise("#d3", %.3f);
  pop("#d3a", %.3f);
  sink("#d3", %.3f);
''' % (t_tomu + 0.1, t_tomu + 0.9, t_dopom + 0.25))
g.sfx("pop", t_tomu + 0.1); g.sfx("notification", t_tomu + 0.9)

# 7b · MEMES (assets/memes/MEMES.md) — comic relief, after the beat lands --------------
# 35 hamster in sunglasses on «я доросла!» (deal-with-it cool), top band, gone
# before «менеджерка» rises behind her; 15 «хуже вже не буде» right after the
# card falls through on «пробиває дно» (doom, resigned), in the free stretch
# «Так от, щоб такого не було» before «AI-агент».
g.meme(F, J, "35", round(E(u"доросла!", 7.2) + 0.1, 3), dur=0.9, slot="top")
g.meme(F, J, "15", round(E(u"дно».", 29.0) + 0.1, 3), dur=1.3, slot="top")

# 8 · CTA — the pill in the subtitle band (the blackout from «став» frees it) -------------
t_stav = S(u"став", 61.1)
F.append(u'''        <div id="ctp" class="pill hid" style="left:0; right:0; margin:auto; width:max-content; top:1404px;
             font-size:46px; padding:28px 56px">Став + або пиши в Direct</div>''')
js(u'  pop("#ctp", %.3f);' % (t_stav - 0.1))
g.sfx("pop", t_stav)
BLACKOUT.append((t_stav - 0.05, DUR))

# ---------------------------------------------------------------- half screens + their mattes
for i, (a, b) in enumerate(HALF):
    g.matte("half%d" % (i + 1), round(a - 0.1, 3), round(b - a + 1.2, 3))
    js("  half(%.3f, %.3f);" % (a, b))
    PLACE.append((a + 0.4, b + 0.2, "bottom", 938))


def main():
    chunks = g.chunks(CAPS, place=PLACE)
    doc = g.document(title=u"Reel 67 — AI-агент замість менеджерки", plate="assets/base.mp4",
                     behind="\n".join(B), panel="\n".join(P), front="\n".join(F), cover="\n".join(C),
                     js="\n".join(J), chunks=chunks, blackout=BLACKOUT, extra_css=EXTRA)
    g.write(HERE, doc)
    print("DUR %.3f (%d frames)  %d caption chunks, %d sfx cues, %d mattes" % (
        DUR, FRAMES, len(chunks), len(g.cues), len(g.mattes)))
    if "--words" in sys.argv:
        print(" ".join("%s/%.1f" % (c["w"], c["s"]) for c in CAPS))


main()
