# -*- coding: utf-8 -*-
"""Reel 72 — «Чим АІ-агент відрізняється від звичайного чат-бота з кнопками?».
Batch 2026-11-20 (raw 20261120_140714). STYLE.md §00 + her review of reel 61
(2026-11-23): natural editing, few graphics, reel-61's skeleton and idioms.

Chain: behind «AI-агент» (the cover) -> behind «хардкод-бот» -> FULL 1 the
button bot as a 3D chat window: a message, two buttons, А pressed -> its
branch, Б pressed -> its branch, zoom out on «самодіяльності» -> shuffle of
what a webinar registration collects (ім'я / номер телефону / інфо про
вебінар) -> FULL 2 the same window, now the bag shop's AI agent: the client
writes, the agent asks back, a manager joins -> shuffle послуги / продукти ->
HALF the scheme: кнопки -> AI-агент in one chain (базові дані under the
buttons, деталі запиту under the agent) -> CTA pill in the subtitle band:
«Пиши + у коментарях», then «або в Direct: розкажи про свій бізнес».

usage: python3 build.py   (then: sfx mix, mattes, check, render — see the brief)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
from gstyle import G, Words, load_caps  # noqa: E402

NN = "72"
DUR = float(open(os.path.join(HERE, "DUR")).read())
g = G(dur=DUR, reel=NN)
g.PANEL_TOP = 820

FIX = {}
exec(open(os.path.join(HERE, "fix.py"), encoding="utf-8").read())
CAPS = load_caps(NN, FIX)
W = Words(CAPS)
S, E = W.s, W.e
g.cta_start = S(u"Якщо", 91.87)     # the CTA line's first word: no meme from here on

# MEMES (her rule 2026-11-23: comic relief, after the beat lands; MEMES.md)
F_M, J_M = [], []
# 51 Shrek side-look: "they all just added AI and raised the price" -> you know what I mean
g.meme(F_M, J_M, "51", round(E(u"ціну.", 8.8) + 0.1, 3), dur=1.2, slot="top")
# 01 ЦИТЬ: "we don't need the bot to add anything of its own, right?" -> shh, bot
g.meme(F_M, J_M, "01", round(E(u"правильно?", 40.1) + 0.1, 3), dur=1.2, slot="l")

B, P, F, C, J = [], [], [], [], []
F += F_M; J += J_M
BLACKOUT, PLACE, HALF = [], [], []


def js(s):
    J.append(s)


P.append(u'<svg class="sk" id="skP" data-layout-allow-occlusion width="1080" height="1240" viewBox="0 0 1080 1240"></svg>')

EXTRA = u'''
    /* the chat window of both full screens: a clean Direct-style thread, sized per the
       full-screen bar (reel-67): 960 px wide at rest, body 36 px, labels >= 28 px */
    #cover { background: radial-gradient(120% 80% at 50% 35%, #FFFFFF 0%, #F6EFEF 70%, #F1E7E7 100%); }
    #stage { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; perspective: 2400px; }
    .win { position: absolute; left: 0; top: 0; width: 960px; background: #fff;
           border-radius: 36px; font-family: "Google Sans", sans-serif; color: #1f1f1f; overflow: hidden;
           box-shadow: 0 2px 6px rgba(36,25,25,.10), 0 30px 80px rgba(36,25,25,.22);
           will-change: transform; }
    .win .hd { position: absolute; left: 0; top: 0; width: 960px; height: 140px; background: #fff; z-index: 2; border-bottom: 2px solid #ECE6E6;
               box-sizing: border-box; display: flex; align-items: center; gap: 22px; padding: 0 40px; }
    .win .av { width: 72px; height: 72px; border-radius: 50%; background: #7A1424; flex: none;
               color: #fff; font-weight: 700; font-size: 34px; display: flex; align-items: center; justify-content: center; }
    .win .nm { font-size: 44px; font-weight: 700; line-height: 1.1; }
    .win .st { font-size: 28px; color: #6f6363; }
    .win .tag { margin-left: auto; font-size: 30px; font-weight: 700; letter-spacing: .03em; color: #7A1424;
                background: #FFF0F0; border-radius: 30px; padding: 12px 26px; }
    .win .th { position: absolute; left: 0; top: 140px; width: 960px; padding: 32px 40px; box-sizing: border-box; }
    .m { display: flex; margin-bottom: 18px; }
    .m.r { justify-content: flex-end; }
    .b { max-width: 760px; border-radius: 32px; padding: 20px 30px; font-size: 40px; line-height: 1.3; }
    .m.l .b { background: #F1EEEE; color: #241919; border-bottom-left-radius: 10px; }
    .m.r .b { background: #7A1424; color: #fff; border-bottom-right-radius: 10px; }
    .btns { display: flex; gap: 20px; margin: 0 0 22px 0; }
    .bt { width: 360px; height: 100px; border-radius: 24px; border: 3px solid #7A1424; color: #7A1424; box-sizing: border-box;
          font-size: 38px; font-weight: 500; display: flex; align-items: center; justify-content: center; background: #fff; }
    .sysm { text-align: center; font-size: 30px; color: #6f6363; margin: 10px 0 14px; }
    .dots { display: inline-flex; gap: 10px; padding: 26px 30px; }
    .dots i { width: 16px; height: 16px; border-radius: 50%; background: #9c8b8b; display: block; }
    .prof { text-align: center; padding: 6px 0 28px; }
    .pav { width: 120px; height: 120px; border-radius: 50%; background: #7A1424; color: #fff; margin: 0 auto 14px;
           font-size: 56px; font-weight: 700; display: flex; align-items: center; justify-content: center; }
    .pnm { font-size: 40px; font-weight: 700; }
    .pst { font-size: 28px; color: #6f6363; margin-top: 4px; }
    .shuf .chip { font-size: 46px; padding: 18px 32px; }
'''

# 1 · BEHIND — «AI-агент», the hook word and the cover frame ----------------------
t_ai = S(u"AI-агент", 0.53)
B.append(u'        <div id="bw1" class="big hid" data-layout-allow-occlusion style="top:520px; font-size:210px">AI-агент</div>')
g.matte("b1", 0.0, 3.2)
js(u'  rise("#bw1", 0.05); sink("#bw1", 2.75);')
g.sfx("whoosh-short", 0.1)
BLACKOUT.append((0.0, E(u"AI-агент", 0.53) + 0.02))

# 2 · BEHIND — «хардкод-бот» ----------------------------------------------------
t_hk, e_hk = S(u"хардкод-бот.", 16.63), E(u"хардкод-бот.", 16.63)
B.append(u'        <div id="bw2" class="big hid" data-layout-allow-occlusion style="top:545px; font-size:165px">хардкод-бот</div>')
g.matte("b2", round(t_hk - 0.6, 3), round(e_hk - t_hk + 1.3, 3))
js(u'  rise("#bw2", %.3f); sink("#bw2", %.3f);' % (t_hk - 0.3, e_hk + 0.35))
g.sfx("whoosh-short", t_hk - 0.3)
BLACKOUT.append((t_hk - 0.03, e_hk))

# 3 · FULL 1 — the button bot, a platform-ad sequence ---------------------------
H1, H2, SCROLL2 = 860, 1000, 120
f0 = S(u"скрипт:", 19.59) - 0.45
t_pov, t_knop = S(u"повідомлення,", 20.32), S(u"кнопки,", 21.60)
t_a, t_tudy = S(u"А", 22.57), S(u"туди,", 23.33)
t_b, t_suda = S(u"на Б", 24.15) + 0.12, S(u"сюди.", 24.93)
t_sam = S(u"Ніякої", 25.43)
f1 = E(u"самодіяльності.", 26.18) + 0.2
C.append(u"""
        <div id="stage">
          <div id="w1" class="win" style="height:%(h1)dpx">
            <div class="hd"><div class="av">Б</div><div><div class="nm">Чат-бот</div><div class="st">Direct</div></div><span class="tag">КНОПКИ</span></div>
            <div class="th">
              <div class="m l" id="w1d"><div class="b dots"><i></i><i></i><i></i></div></div>
              <div class="m l hid" id="w1m"><div class="b">Привіт! Обери, що тебе цікавить:</div></div>
              <div class="btns hid" id="w1k"><div class="bt" id="w1a">Варіант А</div><div class="bt" id="w1b">Варіант Б</div></div>
              <div class="m r hid" id="w1ra"><div class="b">Варіант А</div></div>
              <div class="m l hid" id="w1sa"><div class="b">Сценарій А</div></div>
              <div class="m r hid" id="w1rb"><div class="b">Варіант Б</div></div>
              <div class="m l hid" id="w1sb"><div class="b">Сценарій Б</div></div>
            </div>
          </div>
          <div id="w2" class="win" style="height:%(h2)dpx; visibility:hidden">
            <div class="hd"><div class="av">С</div><div><div class="nm">Магазин сумок</div><div class="st">Direct</div></div><span class="tag">AI-АГЕНТ</span></div>
            <div class="th" id="w2th">
              <div class="prof"><div class="pav">С</div><div class="pnm">Магазин сумок</div><div class="pst">Instagram</div></div>
              <div class="m r hid" id="w2c1"><div class="b">Привіт! Хочу сумку</div></div>
              <div class="m l hid" id="w2d"><div class="b dots"><i></i><i></i><i></i></div></div>
              <div class="m l hid" id="w2a1"><div class="b">Привіт! На щодень чи на вихід? Що має в неї влазити?</div></div>
              <div class="m r hid" id="w2c2"><div class="b">На щодень, і щоб влазив ноутбук</div></div>
              <div class="m l hid" id="w2a2"><div class="b">Зрозуміла! Передаю менеджерці, вона підбере моделі</div></div>
              <div class="sysm hid" id="w2s">Менеджерка приєдналась до чату</div>
            </div>
          </div>
        </div>""" % {"h1": H1, "h2": H2})


def at(sc, py, cy, H):
    """camera: window (960 x H) turns and scales about its centre (480, H/2); window row py
    lands at frame y cy, horizontally centred. Returns the gsap props + its frame top/bottom."""
    o = H / 2.0
    x = round(540 - 480, 1)
    y = round(cy - o - sc * (py - o), 1)
    top, bot = cy - sc * py, cy + sc * (H - py)
    SHOTS.append((sc, py, cy, H, round(top), round(bot)))
    return "x: %s, y: %s, scale: %s" % (x, y, sc)


SHOTS = []
W1_OPEN, W1_WIDE = at(1.12, 220, 600, H1), at(1.0, H1 / 2, 820, H1)
W1_BTN, W1_DOWN = at(1.1, 300, 640, H1), at(1.06, 520, 820, H1)
js(u"""
  gsap.set("#w1", {transformOrigin: "480px %(o1)dpx"});
  gsap.set("#w1", {%(open)s, rotationX: 24, rotationY: -20, rotationZ: 5});
  gsap.set("#w1", {y: "+=220", scale: .96});
  tl.to("#w1", {%(open)s, rotationX: 9, rotationY: -10, rotationZ: 2, duration: 1.3, ease: "power3.out"}, %(f0).3f + .15);
  tl.to("#w1d i", {y: -6, duration: .25, stagger: .1, yoyo: true, repeat: 3, ease: "sine.inOut"}, %(f0).3f + .4);
  tl.set("#w1d", {display: "none"}, %(pov).3f - .1);
  fadein("#w1m", %(pov).3f - .1, .3); tl.fromTo("#w1m", {y: 20}, X({y: 0, duration: .4, ease: RISE}), %(pov).3f - .1);
  tl.to("#w1", {%(btn)s, rotationX: 4, rotationY: -5, rotationZ: 1, duration: 1.1, ease: "power3.inOut"}, %(knop).3f - .5);
  fadein("#w1k", %(knop).3f, .3); tl.fromTo("#w1k", {y: 20}, X({y: 0, duration: .4, ease: RISE}), %(knop).3f);
  tl.to("#w1a", {backgroundColor: "#7A1424", color: "#fff", scale: .94, duration: .15}, %(a).3f);
  tl.to("#w1a", {scale: 1, duration: .2}, %(a).3f + .15);
  fadein("#w1ra", %(a).3f + .2, .25);
  fadein("#w1sa", %(tudy).3f - .1, .3);
  tl.to("#w1", {%(down)s, rotationX: 2, rotationY: 5, rotationZ: 0, duration: 1.0, ease: "power3.inOut"}, %(tudy).3f);
  tl.to("#w1b", {backgroundColor: "#7A1424", color: "#fff", scale: .94, duration: .15}, %(b).3f);
  tl.to("#w1b", {scale: 1, duration: .2}, %(b).3f + .15);
  fadein("#w1rb", %(b).3f + .2, .25);
  fadein("#w1sb", %(suda).3f - .1, .3);
  tl.to("#w1", {%(wide)s, rotationX: 9, rotationY: 12, rotationZ: -2, duration: 1.2, ease: "power3.inOut"}, %(sam).3f - .3);
  full(%(f0).3f, %(f1).3f);
""" % {"o1": H1 // 2, "open": W1_OPEN, "wide": W1_WIDE, "btn": W1_BTN, "down": W1_DOWN,
       "f0": f0, "f1": f1, "pov": t_pov, "knop": t_knop, "a": t_a, "tudy": t_tudy,
       "b": t_b, "suda": t_suda, "sam": t_sam})
g.sfx("whoosh-short", f0); g.sfx("pop", t_pov); g.sfx("pop", t_knop)
g.sfx("click", t_a); g.sfx("click", t_b); g.sfx("whoosh-short", t_sam - 0.3); g.sfx("whoosh-short", f1)

# 4 · SHUFFLE — what a webinar registration collects -----------------------------
t_im, t_tel, t_inf = S(u"ім'я,", 34.23), S(u"номер", 34.93), S(u"інформацію", 36.29)
e_web = E(u"вебінар.", 36.99)
SH = [(u"Ім'я", t_im - 0.1), (u"Номер телефону", t_tel - 0.1), (u"Інфо про вебінар", t_inf - 0.1)]
for i, (txt, _) in enumerate(SH):
    F.append(u'        <div id="sa%d" class="shuf hid"><span class="chip"><i></i>%s</span></div>' % (i, txt))
js(u'  shuffle([%s], [%s], %.3f);' % (", ".join('"#sa%d"' % i for i in range(len(SH))),
                                     ", ".join("%.3f" % t for _, t in SH), e_web + 0.5))
for _, t in SH:
    g.sfx("pop", t)

# 5 · FULL 2 — the same window, now the bag shop's AI agent -----------------------
q0 = S(u"бізнес", 53.32) - 0.45
t_dir, t_opyt = S(u"пише", 55.22), S(u"опитає,", 57.14)
t_yaka, t_men = S(u"яка", 58.20), S(u"менеджеру.", 60.66)
t_tobto, t_knp = S(u"Тобто", 61.27), S(u"кнопках.", 65.40)
q1 = E(u"кнопках.", 65.40) + 0.25
W2_OPEN, W2_MID = at(1.08, 330, 700, H2), at(1.1, 520, 860, H2)
W2_LOW, W2_WIDE = at(1.06, 640, 900, H2), at(1.0, H2 / 2, 830, H2)
js(u"""
  tl.set("#w1", {autoAlpha: 0}, %(q0).3f); tl.set("#w2", {autoAlpha: 1}, %(q0).3f);
  gsap.set("#w2", {transformOrigin: "480px %(o2)dpx"});
  gsap.set("#w2", {%(open)s, rotationX: 22, rotationY: 20, rotationZ: -5});
  gsap.set("#w2", {y: "+=220", scale: .94});
  tl.to("#w2", {%(open)s, rotationX: 8, rotationY: 10, rotationZ: -2, duration: 1.3, ease: "power3.out"}, %(q0).3f + .15);
  fadein("#w2c1", %(lyud).3f, .3); tl.fromTo("#w2c1", {y: 20}, X({y: 0, duration: .4, ease: RISE}), %(lyud).3f);
  fadein("#w2d", %(dir).3f + .6, .2);
  tl.to("#w2d i", {y: -6, duration: .25, stagger: .1, yoyo: true, repeat: 3, ease: "sine.inOut"}, %(dir).3f + .7);
  tl.set("#w2d", {display: "none"}, %(opyt).3f - .05);
  tl.to("#w2", {%(mid)s, rotationX: 4, rotationY: 5, rotationZ: 0, duration: 1.1, ease: "power3.inOut"}, %(opyt).3f - .4);
  fadein("#w2a1", %(opyt).3f, .3); tl.fromTo("#w2a1", {y: 20}, X({y: 0, duration: .4, ease: RISE}), %(opyt).3f);
  fadein("#w2c2", %(yaka).3f, .3); tl.fromTo("#w2c2", {y: 20}, X({y: 0, duration: .4, ease: RISE}), %(yaka).3f);
  tl.to("#w2", {%(low)s, rotationX: 2, rotationY: -5, duration: 1.1, ease: "power3.inOut"}, %(men).3f - .9);
  tl.to("#w2th", {y: -%(scroll)d, duration: .6, ease: "power3.inOut"}, %(men).3f - .6);
  fadein("#w2a2", %(men).3f - .5, .3); tl.fromTo("#w2a2", {y: 20}, X({y: 0, duration: .4, ease: RISE}), %(men).3f - .5);
  fadein("#w2s", %(men).3f + .3, .4);
  tl.to("#w2", {%(wide)s, rotationX: 9, rotationY: -12, rotationZ: 2, duration: 1.3, ease: "power3.inOut"}, %(tobto).3f);
  full(%(q0).3f, %(q1).3f);
""" % {"o2": H2 // 2, "open": W2_OPEN, "mid": W2_MID, "low": W2_LOW, "wide": W2_WIDE, "scroll": SCROLL2,
       "q0": q0, "q1": q1, "lyud": S(u"людина", 54.9) - 0.1, "dir": t_dir, "opyt": t_opyt, "yaka": t_yaka, "men": t_men, "tobto": t_tobto})
g.sfx("whoosh-short", q0); g.sfx("notification", t_dir); g.sfx("pop", t_opyt)
g.sfx("pop", t_yaka); g.sfx("ping", t_men + 0.3); g.sfx("whoosh-short", t_tobto); g.sfx("whoosh-short", q1)

# 6 · SHUFFLE — послуги / продукти ------------------------------------------------
t_posl, t_prod = S(u"послугами,", 68.22), S(u"продуктових", 69.50)
SH2 = [(u"Послуги", t_posl - 0.1), (u"Продукти", t_prod - 0.1)]
for i, (txt, _) in enumerate(SH2):
    F.append(u'        <div id="sb%d" class="shuf hid"><span class="chip"><i></i>%s</span></div>' % (i, txt))
js(u'  shuffle(["#sb0", "#sb1"], [%.3f, %.3f], %.3f);' % (SH2[0][1], SH2[1][1], E(u"також.", 70.04) + 0.3))
g.sfx("pop", SH2[0][1]); g.sfx("pop", SH2[1][1])

# 7 · HALF — the scheme: buttons and the agent in one chain -----------------------
k0 = S(u"існувати", 72.43) - 0.15
t_razom = S(u"разом,", 74.86)
t_prosti, t_dani = S(u"прості", 78.00), S(u"базові", 79.34)
t_aga, t_det = S(u"AI-агента,", 82.22), S(u"деталі", 83.82)
k1 = E(u"запиту", 84.24) + 0.15
HALF.append((k0, k1))
js(u'''
  sketch("s1", "skP"); box("s1", 70, 400, 410, 200, {seed: 3});
  label("s1", 275, 520, "кнопки", {size: 74});
  draw("s1", %(a).3f);
  sketch("s2", "skP"); box("s2", 600, 400, 410, 200, {seed: 7, fill: true});
  label("s2", 805, 520, "AI-агент", {size: 74});
  draw("s2", %(b).3f);
  sketch("s3", "skP"); arrow("s3", 490, 500, 590, 500, {seed: 5, bend: -.18, strokeWidth: 5});
  draw("s3", %(razom).3f - .3);
  sketch("s4", "skP"); label("s4", 275, 700, "базові дані", {size: 62});
  under("s4", 110, 724, 440, {seed: 9});
  draw("s4", %(dani).3f - .1);
  sketch("s5", "skP"); label("s5", 805, 700, "деталі запиту", {size: 62, color: "#7A1424"});
  under("s5", 615, 724, 995, {seed: 11, stroke: "#7A1424"});
  draw("s5", %(det).3f - .1);
  erase("s1", %(k1).3f); erase("s2", %(k1).3f); erase("s3", %(k1).3f); erase("s4", %(k1).3f); erase("s5", %(k1).3f);
''' % {"a": k0 + 0.6, "b": k0 + 1.1, "razom": t_razom, "dani": t_dani, "det": t_det, "k1": k1})
g.sfx("whoosh-short", k0); g.sfx("click-soft", t_razom); g.sfx("click-soft", t_dani); g.sfx("click-soft", t_det)

# 8 · CTA — the pill in the subtitle band ----------------------------------------
t_plus, t_dirc = S(u"плюс", 96.89), S(u"в дірект,", 98.29)
F.append(u'''        <div id="ct1" class="pill hid" style="left:0; right:0; margin:auto; width:max-content; top:1404px;
             font-size:46px; padding:28px 56px">Пиши + у коментарях</div>''')
F.append(u'''        <div id="ct2" class="pill light hid" style="left:0; right:0; margin:auto; width:max-content; top:1404px;
             font-size:42px; padding:26px 48px">або в Direct: розкажи про свій бізнес</div>''')
js(u'  pop("#ct1", %.3f); out("#ct1", %.3f); pop("#ct2", %.3f);' % (t_plus - 0.1, t_dirc - 0.25, t_dirc - 0.05))
g.sfx("pop", t_plus); g.sfx("pop", t_dirc)
BLACKOUT.append((t_plus - 0.05, DUR))

# ---------------------------------------------------------------- half screens + their mattes
for i, (a, b) in enumerate(HALF):
    g.matte("half%d" % (i + 1), round(a - 0.1, 3), round(b - a + 1.2, 3))
    js("  half(%.3f, %.3f);" % (a, b))
    PLACE.append((a + 0.4, b + 0.2, "bottom", 938))


def main():
    chunks = g.chunks(CAPS, place=PLACE)
    doc = g.document(title=u"Reel 72 — AI-агент чи бот з кнопками", plate="assets/base.mp4",
                     behind="\n".join(B), panel="\n".join(P), front="\n".join(F), cover="\n".join(C),
                     js="\n".join(J), chunks=chunks, blackout=BLACKOUT, extra_css=EXTRA)
    g.write(HERE, doc)
    print("index.html  %d caption chunks, %d sfx cues, %d mattes" % (len(chunks), len(g.cues), len(g.mattes)))
    if "-v" in sys.argv:
        print(" ".join(u"%s/%.1f" % (c["w"], c["s"]) for c in CAPS))


main()
