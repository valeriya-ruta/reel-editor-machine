# -*- coding: utf-8 -*-
"""Reel 59 — «Які автоматизації зробити репетиторці?». Batch 2026-11-20
(raw 20261120_133928). STYLE.md §00 + her review of reel 61 (natural editing).

A list reel: four automations she'd set up as a maths / history tutor. The list
runs through ONE shuffle slot above her head (a numbered card on «Перше»,
«Друге», «Третє», «Четверте»); each item then gets one meaningful moment:

  hook   glass Threads card: the question («питання з тредс»)
  behind «Claude» (... налаштувала з Claude)
  1      FULL: Claude chat rebuilt as a platform ad — Notion / Google Drive
         connectors light up, «Оля заплатила за 4 уроки» is typed and sent, a
         Notion row lands with a tick, «Скільки я заробила?» -> a redacted sum
         (no money amounts in the UI)
  2      HALF 1 scheme: Google Calendar + SendPulse -> Claude (щоранку) ->
         учню / батькам; then a glass Telegram bot card: «Оплачені уроки
         закінчились» + the WayForPay button on «посилання»
  3      HALF 2 scheme: Zoom / Meet -> Fathom -> Claude + скіл -> конспект +
         домашка -> SendPulse -> учню / батькам
  4      FULL: an НМТ test screen — the skill chip on «тест за темою», the
         Google Drive chip, an answer picked on «порішав»; behind «Kahoot»;
         the same answers come back as four quiz tiles on «вікторину»
  CTA    the whole list, four ticks; pill «Збережи і перешли колезі»

usage: python3 build.py   (then mattes, sfx mix — see work/b1120/AGENT-BRIEF.md)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
from gstyle import G, Words, load_caps, mark  # noqa: E402

NN = "59"
DUR = 83.483           # (2505 plate frames - 0.5) / 30
g = G(dur=DUR, reel=NN)
g.cta_start = None     # set below, once S() exists: «Тому збережи…»
g.PANEL_TOP = 780      # panel captions: bottom 898; her pushed hair at ≈ 925-940

FIX = {
    u'репетиторці?"': u"репетиторці?»",
    (u"По", 11.3): u"По-перше,", u"Перше": None,
    (u"через", 8.2): u"чи", u"асторію,": u"історії,", (u"щоб", 9.6): u"що",
    u"складом.": u"з Claude.",
    u"надеюсь": u"не десь", u"приблизно": u"приблизно.", u"Друге": u"Друге,",
    (u"в", 31.3): u"В", u"конектору": u"конекторі", u"гугл": u"Google", u"календар": u"Calendar",
    (u"син", 32.8): u"SendPulse,", u"пульс": None, u"вклод": u"в Claude", u"шранку.": u"щоранку,",
    u"якийсь": u"в кого", u"батькану": u"батькам", (u"а", 40.9): u"А",
    u"вейфорпей": u"WayForPay", u"себе": u"сам",
    u"aftercare.": u"афтеркер.", u"Урок": u"урок", u"зумі": u"Zoom", u"мід": u"Meet",
    u"Фатум.": u"Fathom.", u"Третє": u"Третє,",
    (u"син", 58.5): u"SendPulse", u"пусть": None, (u"батькам", 61.1): u"батькам.",
    u"Четверте": u"Четверте,", (u"Скіл", 65.9): u"скіл", u"темою»": u"темою»,",
    u"формацію": u"інформацію", u"NMT.": u"НМТ,",
    u"То": u"то", u"іде?": u"є", u"Кахут": u"Kahoot,", u"бікторину": u"вікторину",
    u"кахуті.": u"Kahoot.", u"Збережи,": u"збережи,",
}
CAPS = load_caps(NN, FIX)
W = Words(CAPS)
S, E = W.s, W.e
g.cta_start = S(u"Тому", 79.80)

B, P, F, C, J = [], [], [], [], []
BLACKOUT, PLACE, HALF = [], [], []


def js(s):
    J.append(s)


P.append(u'<svg class="sk" id="skP" data-layout-allow-occlusion width="1080" height="1240" viewBox="0 0 1080 1240"></svg>')

EXTRA = u'''
    .gl { left: 150px; top: 300px; width: 780px; padding: 26px 30px; }
    .gl .hd { display: flex; align-items: center; gap: 14px; font-size: 26px; font-weight: 500;
              color: #574142; margin-bottom: 16px; }
    .gl .hd .mark { color: #241919; }
    .gl .q { font-size: 42px; font-weight: 700; line-height: 1.18; letter-spacing: -0.015em; color: #241919; }
    .bub { display: inline-block; border-radius: 26px; padding: 16px 24px; font-size: 32px;
           font-weight: 500; line-height: 1.25; background: rgba(255,255,255,.92); color: #241919;
           border-bottom-left-radius: 8px; }
    .tgbtn { margin-top: 14px; display: flex; align-items: center; justify-content: center; gap: 14px;
             height: 66px; border-radius: 18px; background: #7A1424; color: #fff; font-size: 30px; font-weight: 500; }
    .tgbtn small { font-size: 24px; opacity: .8; font-weight: 400; }

    /* the list slot: a numbered white card (shuffle), no glass */
    .shuf .chip b { display: inline-flex; width: 52px; height: 52px; border-radius: 50%; background: #7A1424;
                    color: #fff; font-size: 30px; font-weight: 700; align-items: center; justify-content: center; }

    /* the quiz tiles (Kahoot) — the test's answers, again */
    .quiz { left: 0; right: 0; margin: auto; width: 700px; top: 300px; padding: 22px;
            display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
    .tile { height: 96px; border-radius: 18px; display: flex; align-items: center; gap: 22px; padding: 0 26px;
            color: #fff; font-size: 44px; font-weight: 700; }
    .tile svg { flex: none; }

    /* CTA: the whole list, ticked */
    .lst { left: 0; right: 0; margin: auto; width: 700px; top: 296px; padding: 24px 32px; }
    .lst .row { height: 50px; gap: 16px; font-size: 32px; font-weight: 500; color: #241919; }
    .lst .row + .row { margin-top: 8px; }
    .lst .check { width: 38px; height: 38px; border-radius: 10px; }
    .lst .check.on::after { left: 10px; top: 3px; width: 10px; height: 20px; }

    #cover { background: radial-gradient(120% 80% at 50% 35%, #FFFFFF 0%, #F6EFEF 70%, #F1E7E7 100%); }
    .stage { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; perspective: 2200px; }
    .win { position: absolute; left: 0; top: 0; width: 800px; height: 560px; background: #fff;
           border-radius: 16px; font-family: "Google Sans", sans-serif; color: #1f1f1f; overflow: hidden;
           box-shadow: 0 2px 6px rgba(36,25,25,.10), 0 30px 80px rgba(36,25,25,.22);
           transform-origin: 400px 280px; will-change: transform; }
    .win > div { position: absolute; }
'''

# ---------------------------------------------------------------- hook · glass Threads card
t_pyt, t_yaki, t_kor = S(u"питання", 1.49), S(u"«Які", 2.87), S(u"Коротше,", 5.90)
F.append(u'''
        <div id="th" class="glass gl hid">
          <div class="hd">%s Питання з Threads</div>
          <div class="q">Які автоматизації можна використати репетиторці?</div>
        </div>''' % mark("threads", 34))
js(u'  rise("#th", %.3f); sink("#th", %.3f);' % (t_pyt, t_kor - 0.15))
g.sfx("pop", t_pyt)
BLACKOUT.append((t_yaki - 0.03, t_kor - 0.05))

# ---------------------------------------------------------------- meme 34: «якби я була репетиторкою з математики чи історії»
g.meme(F, J, "34", E(u"історії,", 8.56) + 0.1, dur=0.85, slot="top")

# ---------------------------------------------------------------- behind «Claude»
t_cl = S(u"з Claude.", 10.70)
B.append(u'        <div id="bw1" class="big hid" data-layout-allow-occlusion style="top:440px; font-size:220px">Claude</div>')
g.matte("b1", round(t_cl - 0.7, 3), 2.4)
js(u'  rise("#bw1", %.3f); sink("#bw1", %.3f);' % (t_cl - 0.45, t_cl + 1.3))
g.sfx("whoosh-short", t_cl - 0.45)
BLACKOUT.append((t_cl - 0.03, E(u"з Claude.", 10.70)))

# ---------------------------------------------------------------- the list slot
ITEMS = [u"CRM учнів і фінанси", u"Нагадування про урок і оплату", u"Афтеркер", u"Тести у форматі НМТ"]
for i, txt in enumerate(ITEMS):
    F.append(u'        <div id="li%d" class="shuf hid"><span class="chip"><b>%d</b>%s</span></div>' % (i, i + 1, txt))


def item(i, t0, t1):
    js(u'  shuffle(["#li%d"], [%.3f], %.3f);' % (i, t0, t1))
    g.sfx("pop", t0)


# ---------------------------------------------------------------- 1 · FULL: Claude chat
t_pershe = S(u"По-перше,", 11.27)
item(0, t_pershe, S(u"Підключаєш", 14.08) - 0.1)
f0 = S(u"Підключаєш", 14.08) - 0.05
f1 = S(u"а", 26.74) + 0.25        # out on «а не десь…»: her face carries the punchline
C.append(u"""
        <div id="st1" class="stage">
          <div id="win1" class="win" style="background:#FBFAF7">
            <div style="left:0;top:0;width:800px;height:46px;border-bottom:1px solid #ECE7E2;background:#fff"></div>
            <div style="left:20px;top:12px;display:flex;align-items:center;gap:9px;font-size:16px;font-weight:700;color:#7A1424">%(claude)s<span style="color:#1f1f1f">Claude</span></div>
            <div style="left:610px;top:15px;font-size:12px;color:#8a8580">Учні та оплати</div>

            <div id="u1" class="ub" style="left:470px;top:66px">Оля заплатила за 4 уроки</div>
            <div id="r1" style="left:40px;top:112px;width:720px">
              <div class="tool">%(notion)s Notion · Учні та оплати · додано рядок</div>
              <div class="tbl">
                <div class="tr th"><span>Учень</span><span>Уроки</span><span>Оплата</span></div>
                <div class="tr" id="row"><span>Оля</span><span>4</span><span><i id="tk" class="ok"></i>оплачено</span></div>
              </div>
            </div>
            <div id="u2" class="ub" style="left:446px;top:262px">Скільки я заробила за листопад?</div>
            <div id="r2" style="left:40px;top:308px;font-size:15px;color:#1f1f1f;display:flex;align-items:center;gap:10px">
              За листопад, за даними таблиці: <span class="red"></span></div>

            <div id="inp" style="left:40px;top:440px;width:720px;height:96px;background:#fff;border:1px solid #E3DED8;border-radius:16px;box-shadow:0 2px 8px rgba(0,0,0,.04)">
              <div id="ph" style="position:absolute;left:18px;top:14px;font-size:15px;color:#9b958f">Напиши Claude…</div>
              <div id="ty" style="position:absolute;left:18px;top:14px;font-size:15px;color:#1f1f1f;white-space:nowrap;clip-path:inset(0%% 100%% 0%% 0%%)">Оля заплатила за 4 уроки</div>
              <div id="cn" class="cn" style="position:absolute;left:14px;top:56px">%(notion)s Notion</div>
              <div id="cg" class="cn" style="position:absolute;left:112px;top:56px">%(drive)s Google Drive</div>
              <div id="snd" style="position:absolute;right:12px;top:54px;width:30px;height:30px;border-radius:9px;background:#D8B9BD;color:#fff;font-size:17px;text-align:center;line-height:30px">↑</div>
            </div>
          </div>
        </div>""" % {"claude": mark("claude", 20), "notion": mark("notion", 13), "drive": mark("googledrive", 13)})
EXTRA += u"""
    .ub { background: #EFE9E3; border-radius: 14px; padding: 9px 14px; font-size: 15px; color: #1f1f1f; white-space: nowrap; }
    .tool { display: inline-flex; align-items: center; gap: 7px; font-size: 12px; color: #6b6560;
            border: 1px solid #E6E0DA; border-radius: 9px; padding: 5px 10px; background: #fff; margin-bottom: 10px; }
    .tbl { width: 460px; border: 1px solid #E6E0DA; border-radius: 10px; background: #fff; overflow: hidden; }
    .tr { display: grid; grid-template-columns: 1.4fr 1fr 1.3fr; padding: 9px 14px; font-size: 14px; align-items: center; }
    .tr.th { background: #F6F3F0; color: #6b6560; font-size: 12px; font-weight: 700; }
    .tr span { display: flex; align-items: center; gap: 7px; }
    .ok { display: inline-block; width: 15px; height: 15px; border-radius: 4px; background: #7A1424; position: relative; }
    .ok::after { content: ""; position: absolute; left: 5px; top: 1px; width: 4px; height: 9px;
                 border: solid #fff; border-width: 0 2px 2px 0; transform: rotate(45deg); }
    .red { display: inline-block; width: 110px; height: 20px; border-radius: 6px; background: #E8DCDC; }
    .cn { display: inline-flex; align-items: center; gap: 6px; font-size: 12px; color: #6b6560;
          border: 1px solid #E3DED8; border-radius: 999px; padding: 5px 11px; background: #fff; }
    .cn .mark, .tool .mark { color: #3c3c3c; }
"""


def cam(px, py, sc, cx=540, cy=760):
    # the window scales about its own centre (400, 280): a point p lands at
    # O + s*(p - O) + (x, y)
    return "{x: %.1f, y: %.1f, scale: %.3f" % (cx - 400 - sc * (px - 400), cy - 280 - sc * (py - 280), sc)


t_notion, t_gd = S(u"Notion", 15.48), S(u"Google", 16.10)
t_olia, t_uroky, t_vnos, t_opl = S(u"«Оля", 18.30), S(u"уроки».", 20.51), S(u"вносить", 21.81), S(u"оплату,", 22.29)
t_skil, t_tsyf, t_ne = S(u"«скільки", 24.76), S(u"цифрою,", 26.22), S(u"не десь", 27.26)
WIDE1 = cam(400, 280, 1.2)
js(u"""
  gsap.set("#win1", %(wide)s, rotationX: 24, rotationY: -20, rotationZ: 5});
  gsap.set("#win1", {y: "+=220", scale: 1.2 * .86});
  gsap.set(["#u1", "#r1", "#u2", "#r2"], {autoAlpha: 0});
  tl.to("#win1", %(wide)s, rotationX: 9, rotationY: -12, rotationZ: 2, duration: 1.3, ease: "power3.out"}, %(f0).3f + .12);
  tl.to("#win1", %(inp)s, rotationX: 3, rotationY: 6, rotationZ: 0, duration: 1.1, ease: "power3.inOut"}, %(notion).3f - .7);
  tl.to("#cn", {borderColor: "#7A1424", backgroundColor: "#FBEFF0", color: "#7A1424", duration: .25}, %(notion).3f);
  tl.to("#cg", {borderColor: "#7A1424", backgroundColor: "#FBEFF0", color: "#7A1424", duration: .25}, %(gd).3f);
  tl.set("#ph", {autoAlpha: 0}, %(olia).3f - .1);
  tl.fromTo("#ty", {clipPath: "inset(0%% 100%% 0%% 0%%)"}, X({clipPath: "inset(0%% 0%% 0%% 0%%)", duration: %(tyd).3f, ease: "steps(24)"}), %(olia).3f - .1);
  tl.to("#snd", {backgroundColor: "#7A1424", duration: .15}, %(uroky).3f);
  tl.set("#ty", {autoAlpha: 0}, %(uroky).3f + .25); tl.set("#ph", {autoAlpha: 1}, %(uroky).3f + .25);
  tl.to("#win1", %(chat)s, rotationX: -2, rotationY: -7, duration: 1.0, ease: "power3.inOut"}, %(uroky).3f + .05);
  tl.fromTo("#u1", {autoAlpha: 0, y: 30}, X({autoAlpha: 1, y: 0, duration: .4, ease: RISE}), %(uroky).3f + .25);
  tl.fromTo("#r1", {autoAlpha: 0, y: 20}, X({autoAlpha: 1, y: 0, duration: .45, ease: RISE}), %(vnos).3f - .1);
  tl.fromTo("#row", {backgroundColor: "#FBEFF0"}, X({backgroundColor: "#FFFFFF", duration: 1.2}), %(vnos).3f + .3);
  tl.fromTo("#tk", {scale: 0}, X({scale: 1, duration: .4, ease: POP}), %(opl).3f);
  tl.to("#win1", %(q)s, rotationX: 2, rotationY: 7, duration: 1.1, ease: "power3.inOut"}, %(skil).3f - .6);
  tl.fromTo("#u2", {autoAlpha: 0, y: 30}, X({autoAlpha: 1, y: 0, duration: .4, ease: RISE}), %(skil).3f);
  tl.fromTo("#r2", {autoAlpha: 0, y: 20}, X({autoAlpha: 1, y: 0, duration: .45, ease: RISE}), %(tsyf).3f - .1);
  gsap.set("#st1", {autoAlpha: 1}); tl.set("#st1", {autoAlpha: 0}, %(f1).3f + .9);
  full(%(f0).3f, %(f1).3f);
""" % {"wide": WIDE1, "wy": "%.1f" % 0, "inp": cam(250, 500, 2.2), "chat": cam(400, 190, 1.4),
       "q": cam(400, 290, 1.45), "f0": f0, "f1": f1, "notion": t_notion, "gd": t_gd, "olia": t_olia,
       "uroky": t_uroky, "tyd": t_uroky - t_olia - 0.1, "vnos": t_vnos, "opl": t_opl, "skil": t_skil,
       "tsyf": t_tsyf, "ne": t_ne})
g.sfx("whoosh-short", f0); g.sfx("click-soft", t_notion); g.sfx("click-soft", t_gd)
g.sfx("typing", t_olia - 0.1); g.sfx("click", t_uroky); g.sfx("pop", t_opl)
g.sfx("notification", t_tsyf - 0.1); g.sfx("whoosh-short", f1)

# ---------------------------------------------------------------- meme 05: «а не десь щось там приблизно»
g.meme(F, J, "05", E(u"приблизно.", 28.06) + 0.1, dur=0.8, slot="top")

# ---------------------------------------------------------------- 2 · reminders
t_druhe = S(u"нагадування", 29.20)   # the card lands on its own word, after the meme
h1a = S(u"В", 31.35) - 0.15
item(1, t_druhe, h1a)
h1b = S(u"А", 40.93) - 0.2
HALF.append((h1a, h1b))
t_cal, t_sp, t_vcl, t_shch, t_uch = S(u"Calendar", 32.17), S(u"SendPulse,", 32.81), S(u"в Claude", 33.49), \
    S(u"щоранку,", 35.21), S(u"учню", 37.70)
js(u'''
  sketch("a1", "skP"); box("a1", 50, 300, 420, 110, {seed: 3});
  label("a1", 260, 372, "Google Calendar", {size: 48});
  draw("a1", %.3f);
  sketch("a2", "skP"); label("a2", 540, 378, "+", {size: 70});
  box("a2", 610, 300, 420, 110, {seed: 5}); label("a2", 820, 372, "SendPulse", {size: 48});
  draw("a2", %.3f);
  sketch("a3", "skP"); arrow("a3", 260, 420, 420, 505, {seed: 7, bend: .1}); arrow("a3", 820, 420, 660, 505, {seed: 9, bend: -.1});
  box("a3", 380, 500, 320, 110, {seed: 11, fill: true}); label("a3", 540, 572, "Claude", {size: 54});
  draw("a3", %.3f, .5);
  sketch("a4", "skP"); ell("a4", 820, 555, 96, 96, {seed: 13, fill: false});
  ln("a4", 820, 555, 820, 522, {seed: 15}); ln("a4", 820, 555, 843, 566, {seed: 17});
  label("a4", 885, 570, "щоранку", {size: 44, anchor: "start"});
  draw("a4", %.3f, .4);
  sketch("a5", "skP"); arrow("a5", 540, 620, 540, 650, {seed: 19, bend: 0});
  box("a5", 330, 655, 420, 100, {seed: 21}); label("a5", 540, 722, "учню / батькам", {size: 48});
  draw("a5", %.3f, .45);
  erase("a1", %.3f); erase("a2", %.3f); erase("a3", %.3f); erase("a4", %.3f); erase("a5", %.3f);
''' % (t_cal - 0.5, t_sp - 0.35, t_vcl - 0.5, t_shch - 0.25, t_uch - 0.35, h1b, h1b, h1b, h1b, h1b))
g.sfx("whoosh-short", h1a); g.sfx("click-soft", t_vcl); g.sfx("click-soft", t_shch); g.sfx("click-soft", t_uch)

# the bot message: lessons ran out -> a pay link
t_zak, t_posyl, t_vidpr = S(u"закінчились", 41.75), S(u"посилання", 46.10), S(u"відправляти", 47.46)
t_tretie = S(u"Третє,", 49.17)
F.append(u'''
        <div id="tg" class="glass gl hid">
          <div class="hd">%s Бот репетиторки</div>
          <div><span class="bub hid" id="tg1">Оплачені уроки закінчились. Оплатимо наступні?</span></div>
          <div class="tgbtn hid" id="tg2">Оплатити <small>· WayForPay</small></div>
        </div>''' % mark("telegram", 32))
EXTRA += u"    #tg .bub { font-size: 30px; }\n"
js(u'''
  rise("#tg", %.3f);
  pop("#tg1", %.3f);
  pop("#tg2", %.3f);
  tl.to("#tg2", {keyframes: {scale: [1, .94, 1]}, duration: .3}, %.3f);
  sink("#tg", %.3f);
''' % (h1b + 0.55, t_zak, t_posyl, t_vidpr, t_tretie - 0.35))
g.sfx("notification", t_zak); g.sfx("pop", t_posyl); g.sfx("click", t_vidpr)

# ---------------------------------------------------------------- 3 · aftercare (HALF 2)
h2a = S(u"Тобто", 51.07) - 0.1
item(2, t_tretie, h2a)
h2b = S(u"Четверте,", 61.57) - 0.45
HALF.append((h2a, h2b))
t_zoom, t_fat, t_cl2, t_kons = S(u"Zoom", 51.86), S(u"Fathom.", 53.02), S(u"у Claude,", 55.87), S(u"конспект", 57.18)
t_sp2, t_uch2 = S(u"SendPulse", 58.54), S(u"учню", 60.38)
js(u'''
  sketch("c1", "skP"); box("c1", 60, 295, 330, 105, {seed: 3}); label("c1", 225, 364, "Zoom / Meet", {size: 46});
  draw("c1", %.3f);
  sketch("c2", "skP"); arrow("c2", 400, 348, 670, 348, {seed: 5, bend: .08});
  box("c2", 690, 295, 330, 105, {seed: 7}); label("c2", 855, 364, "Fathom", {size: 48});
  draw("c2", %.3f, .5);
  sketch("c3", "skP"); arrow("c3", 855, 405, 855, 470, {seed: 9, bend: 0});
  box("c3", 690, 475, 330, 105, {seed: 11, fill: true}); label("c3", 855, 544, "Claude + скіл", {size: 44});
  draw("c3", %.3f, .45);
  sketch("c4", "skP"); arrow("c4", 680, 528, 410, 528, {seed: 13, bend: -.08});
  box("c4", 40, 465, 360, 125, {seed: 15}); label("c4", 220, 520, "конспект", {size: 44}); label("c4", 220, 568, "+ домашка", {size: 44});
  draw("c4", %.3f, .5);
  sketch("c5", "skP"); arrow("c5", 220, 595, 220, 650, {seed: 17, bend: 0});
  box("c5", 60, 655, 330, 100, {seed: 19}); label("c5", 225, 721, "SendPulse", {size: 46});
  draw("c5", %.3f, .45);
  sketch("c6", "skP"); arrow("c6", 400, 705, 670, 705, {seed: 21, bend: .08});
  box("c6", 690, 655, 330, 100, {seed: 23}); label("c6", 855, 721, "учню / батькам", {size: 42});
  draw("c6", %.3f, .5);
  ["c1","c2","c3","c4","c5","c6"].forEach(function (n) { erase(n, %.3f); });
''' % (t_zoom - 0.4, t_fat - 0.5, t_cl2 - 0.45, t_kons - 0.5, t_sp2 - 0.4, t_uch2 - 0.5, h2b))
g.sfx("whoosh-short", h2a); g.sfx("click-soft", t_fat); g.sfx("click-soft", t_cl2)
g.sfx("click-soft", t_kons); g.sfx("click-soft", t_sp2); g.sfx("click-soft", t_uch2)

# ---------------------------------------------------------------- 4 · FULL: the НМТ test
t_chetv = S(u"Четверте,", 61.57)
g0 = S(u"Тобто", 64.53) - 0.15
item(3, t_chetv + 0.3, g0 - 0.05)
g1 = S(u"то", 74.53) - 0.15
OPTS = [(u"А", u"2"), (u"Б", u"4"), (u"В", u"6"), (u"Г", u"10")]
opts = u"".join(u'<div class="op" id="op%d" style="left:%dpx;top:%dpx"><b>%s</b>%s</div>'
                % (i, 40 + (i % 2) * 370, 300 + (i // 2) * 74, a, v) for i, (a, v) in enumerate(OPTS))
C.append(u"""
        <div id="st2" class="stage">
          <div id="win2" class="win">
            <div style="left:0;top:0;width:800px;height:54px;border-bottom:1px solid #EEE"></div>
            <div style="left:24px;top:15px;font-size:17px;font-weight:700">Тест НМТ · Математика</div>
            <div id="ks" class="cn" style="left:418px;top:14px">✦ скіл «тест за темою»</div>
            <div id="kg" class="cn" style="left:606px;top:14px">%(drive)s Google Drive</div>
            <div style="left:40px;top:84px;font-size:13px;color:#6b6560">Завдання 7 з 20</div>
            <div style="left:40px;top:106px;width:720px;height:6px;border-radius:3px;background:#F1E7E7"></div>
            <div style="left:40px;top:106px;width:252px;height:6px;border-radius:3px;background:#7A1424"></div>
            <div id="qq" style="left:40px;top:150px;font-size:26px;font-weight:700;line-height:1.3">Розвʼяжіть рівняння:<br><span style="font-weight:400">2x + 6 = 14</span></div>
            %(opts)s
            <div style="left:620px;top:470px;width:140px;height:44px;border-radius:12px;background:#7A1424;color:#fff;font-size:15px;font-weight:500;text-align:center;line-height:44px">Далі</div>
          </div>
        </div>""" % {"drive": mark("googledrive", 13), "opts": opts})
EXTRA += u"""
    .op { width: 350px; height: 60px; border: 1.5px solid #E3DED8; border-radius: 12px; display: flex;
          align-items: center; gap: 14px; padding: 0 16px; font-size: 18px; background: #fff; }
    .op b { width: 30px; height: 30px; border-radius: 50%; border: 1.5px solid #CFC6C6; display: inline-flex;
            align-items: center; justify-content: center; font-size: 14px; color: #574142; }
"""
t_test, t_nmt, t_gd2, t_porish, t_azart = S(u"«тест", 66.42), S(u"інформацію", 68.86), S(u"Google", 70.74), \
    S(u"й порішав", 73.35), S(u"азартом,", 73.99)
WIDE2 = cam(400, 280, 1.2)
js(u"""
  gsap.set("#win2", %(wide)s, rotationX: 24, rotationY: 20, rotationZ: -5});
  gsap.set("#win2", {y: "+=220", scale: 1.2 * .86});
  tl.to("#win2", %(wide)s, rotationX: 9, rotationY: 12, rotationZ: -2, duration: 1.3, ease: "power3.out"}, %(g0).3f + .12);
  tl.to("#win2", %(sk)s, rotationX: 3, rotationY: -6, rotationZ: 0, duration: 1.1, ease: "power3.inOut"}, %(test).3f - .7);
  tl.to("#ks", {borderColor: "#7A1424", backgroundColor: "#FBEFF0", color: "#7A1424", duration: .25}, %(test).3f);
  tl.to("#win2", %(qq)s, rotationX: -2, rotationY: 6, duration: 1.1, ease: "power3.inOut"}, %(nmt).3f - .6);
  tl.to("#win2", %(sk2)s, rotationX: 2, rotationY: -5, duration: 1.0, ease: "power3.inOut"}, %(gd2).3f - .6);
  tl.to("#kg", {borderColor: "#7A1424", backgroundColor: "#FBEFF0", color: "#7A1424", duration: .25}, %(gd2).3f);
  tl.to("#win2", %(ops)s, rotationX: 4, rotationY: 8, rotationZ: -1, duration: 1.2, ease: "power3.inOut"}, %(gd2).3f + .9);
  tl.to("#op1", {borderColor: "#7A1424", backgroundColor: "#FBEFF0", duration: .2}, %(porish).3f);
  tl.to("#op1 b", {backgroundColor: "#7A1424", borderColor: "#7A1424", color: "#fff", duration: .2}, %(porish).3f);
  tl.to("#op1", {keyframes: {scale: [1, .96, 1]}, duration: .3}, %(porish).3f);
  gsap.set("#st2", {autoAlpha: 0}); tl.set("#st2", {autoAlpha: 1}, %(g0).3f - .05);
  full(%(g0).3f, %(g1).3f);
""" % {"wide": WIDE2, "g0": g0, "g1": g1, "sk": cam(560, 40, 2.4), "qq": cam(240, 200, 2.0),
       "sk2": cam(640, 40, 2.4), "ops": cam(400, 330, 1.3), "test": t_test, "nmt": t_nmt,
       "gd2": t_gd2, "porish": t_porish})
g.sfx("whoosh-short", g0); g.sfx("click-soft", t_test); g.sfx("click-soft", t_gd2)
g.sfx("click", t_porish); g.sfx("whoosh-short", g1)

# ---------------------------------------------------------------- behind «Kahoot»
t_kh, e_kh = S(u"Kahoot,", 75.90), E(u"Kahoot,", 75.90)
t_kon = S(u"конектор", 75.14)
B.append(u'        <div id="bw2" class="big hid" data-layout-allow-occlusion style="top:440px; font-size:220px">Kahoot</div>')
g.matte("b2", round(t_kon - 0.4, 3), round(e_kh + 1.1 - (t_kon - 0.4), 3))
js(u'  rise("#bw2", %.3f); sink("#bw2", %.3f);' % (t_kon - 0.15, e_kh + 0.75))
g.sfx("whoosh-short", t_kon - 0.15)
BLACKOUT.append((t_kh - 0.03, e_kh))

# the same answers, as quiz tiles
t_vik, t_tomu = S(u"вікторину", 78.14), S(u"Тому", 79.80)
SH = [u'<svg width="40" height="40" viewBox="0 0 40 40"><path d="M20 4 L37 35 H3 Z" fill="#fff"/></svg>',
      u'<svg width="40" height="40" viewBox="0 0 40 40"><path d="M20 2 L38 20 L20 38 L2 20 Z" fill="#fff"/></svg>',
      u'<svg width="40" height="40" viewBox="0 0 40 40"><circle cx="20" cy="20" r="17" fill="#fff"/></svg>',
      u'<svg width="40" height="40" viewBox="0 0 40 40"><rect x="4" y="4" width="32" height="32" rx="3" fill="#fff"/></svg>']
TC = [u"#7A1424", u"#A3364A", u"#5B0F1B", u"#C2566A"]
F.append(u'        <div id="qz" class="card quiz hid">%s</div>' % u"".join(
    u'<div class="tile" id="qt%d" style="background:%s">%s%s</div>' % (i, TC[i], SH[i], OPTS[i][1]) for i in range(4)))
js(u'  rise("#qz", %.3f);' % (S(u"зробить", 77.42) - 0.1))
for i in range(4):
    js(u'  pop("#qt%d", %.3f, .45);' % (i, t_vik - 0.15 + i * 0.12))
js(u'  sink("#qz", %.3f);' % (t_tomu - 0.3))
g.sfx("pop", S(u"зробить", 77.42) - 0.1); g.sfx("sparkle", t_vik)

# ---------------------------------------------------------------- CTA
t_zber = S(u"збережи,", 80.05)
rows = u"".join(u'<div class="row"><span class="check"><span class="check on" id="ck%d" style="position:absolute;left:-3px;top:-3px"></span></span>%s</div>' % (i, t) for i, t in enumerate(ITEMS))
F.append(u'        <div id="ls" class="card lst hid">%s</div>' % rows)
F.append(u'''        <div id="ctp" class="pill hid" style="left:0; right:0; margin:auto; width:max-content; top:1404px;
             font-size:46px; padding:28px 56px">Збережи і перешли колезі</div>''')
js(u'  rise("#ls", %.3f);' % (t_tomu - 0.1))
for i in range(4):
    js(u'  pop("#ck%d", %.3f, .35);' % (i, t_tomu + 0.35 + i * 0.22))
js(u'  pop("#ctp", %.3f);' % (t_zber - 0.05))
g.sfx("pop", t_tomu - 0.1); g.sfx("click-soft", t_tomu + 0.35); g.sfx("pop", t_zber)
BLACKOUT.append((t_zber - 0.1, DUR))

# ---------------------------------------------------------------- half screens + their mattes
for i, (a, b) in enumerate(HALF):
    g.matte("h%d" % (i + 1), round(a - 0.1, 3), round(b - a + 1.2, 3))
    js("  half(%.3f, %.3f);" % (a, b))
    PLACE.append((a + 0.4, b + 0.2, "bottom", 898))


def main():
    chunks = g.chunks(CAPS, place=PLACE)
    doc = g.document(title=u"Reel 59 — автоматизації репетиторки", plate="assets/base.mp4",
                     behind="\n".join(B), panel="\n".join(P), front="\n".join(F), cover="\n".join(C),
                     js="\n".join(J), chunks=chunks, blackout=BLACKOUT, extra_css=EXTRA)
    g.write(HERE, doc)
    print("index.html  %d caption chunks, %d sfx cues, %d mattes" % (len(chunks), len(g.cues), len(g.mattes)))


if __name__ == "__main__":
    if "--caps" in sys.argv:
        print(" ".join(u"%s/%.1f" % (c["w"], c["s"]) for c in CAPS))
    main()
