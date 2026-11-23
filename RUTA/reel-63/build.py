# -*- coding: utf-8 -*-
"""Reel 63 — «Які автоматизації зробити викладачці мови?». Batch 2026-11-20
(raw 20261120_134834). STYLE.md §00 + her review of reel 61 (2026-11-23):
natural editing, one meaningful moment per sentence group; reel-61/build.py is
the skeleton.

Chain: behind «Claude» (hook / cover) -> a running list through ONE slot
(shuffle: 1 Картки з нових слів · 2 Щоденник помилок · 3 Перевірка домашок ·
4 Тест на рівень) -> FULL: a Claude chat as a platform-ad sequence (the
Quizlet connector switches on, the word list types, a Quizlet set comes back,
the student opens it, a card flips) -> HALF: the scheme Fathom -> Claude (скіл)
-> помилки + вправи; -> Notion -> картка учня -> a glass homework checklist
(ticks, the one not handed in lights up) -> a glass level-test card (a
question, the A1…C2 scale) -> behind «SendPulse» -> a glass CRM card: a new
lead lands with its level -> CTA: bookmark / paper plane through the slot,
pill «Збережи і перешли колезі» in the subtitle band.

usage: python3 build.py   (then: sh work/b1021/mattes.sh 63; python3 tools/sfx.py mix 63)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
from gstyle import G, Words, load_caps, mark  # noqa: E402

NN = "63"
DUR = 66.150           # (1985 plate frames - 0.5) / 30
g = G(dur=DUR, reel=NN)
g.PANEL_TOP = 740      # panel captions end ≈ y 858; her pushed hair ≈ y 890 on the punch-in

FIX = {
    u"з клод": u"з Claude",
    u"По": u"По-перше,", u"Перше": None, u"звичайна": u"звичайні", u"картинка.": u"картки", u"таки": None,
    u"квісла.": u"Quizlet.", u"сет,": u"сет", u"впізлят.": u"в Quizlet.",
    (u"а", 28.5): u"А", u"Notion": u"Notion,",
    (u"урок,", 27.2): u"урок", u"зробити": u"зробити,", (u"це", 45.2): u"Це", u"чотверте,": u"четверте,",
    u"колодом": u"Claude", (u"в", 51.4): None, u"шкалу,": u"шкалу.",
    u"в Сенпусі": u"в SendPulse", u"коду,": u"коду.",
    u"Сьоромся": u"CRM-систему.", u"з того.": None, u"Це": u"це",
    u"Збережи": u"збережи", u"щоб не загубити,": u"щоб не загубити", u"ідей.": u"ідей,",
    u"знайомій": u"своїй", u"викладачці.": u"колезі.",
}
CAPS = load_caps(NN, FIX)
W = Words(CAPS)
S, E = W.s, W.e

B, P, F, C, J = [], [], [], [], []
BLACKOUT, PLACE, HALF = [], [], []


def js(s):
    J.append(s)


g.cta_start = S(u"Тому", 61.87)    # the CTA line «Тому обов'язково збережи…»: no meme from here


P.append(u'<svg class="sk" id="skP" data-layout-allow-occlusion width="1080" height="1240" viewBox="0 0 1080 1240"></svg>')

EXTRA = u'''
    /* the running list: a number badge on a plain white card (her note: no glass around it) */
    .shuf .chip b.n { width: 50px; height: 50px; border-radius: 50%; background: #7A1424; color: #fff;
                      display: inline-flex; align-items: center; justify-content: center; font-size: 30px;
                      font-weight: 700; margin-left: -8px; }
    .shuf .chip.ic { padding: 22px; }
    .shuf .chip.ic svg { display: block; }
    .glass .hd { display: flex; align-items: center; gap: 14px; font-size: 28px; font-weight: 700;
                 color: #241919; margin-bottom: 14px; }
    .glass .hd small { font-weight: 500; color: #574142; font-size: 24px; margin-left: auto; }
'''

# 1 · BEHIND — «Claude» (the hook and the cover frame) -----------------------------
t_kl = S(u"з Claude", 4.26)
B.append(u'        <div id="bw1" class="big hid" data-layout-allow-occlusion style="top:420px; font-size:230px">Claude</div>')
g.matte("b1", 0.0, 4.4)
js(u'  rise("#bw1", 0.15); sink("#bw1", %.3f);' % (S(u"налаштувала", 5.32) - 0.85))
g.sfx("whoosh-short", 0.15)

# 2 · the running list: four items through one slot ---------------------------------
LIST = [u"Картки з нових слів", u"Щоденник помилок", u"Перевірка домашок", u"Тест на рівень"]
t_l = [S(u"По-перше,", 6.03), S(u"Друге", 18.70) + 0.25, S(u"Третє", 32.47), S(u"четверте,", 46.41) - 0.2]
t_lo = [S(u"У", 9.73) - 0.1, S(u"Fathom", 20.78) - 0.45, S(u"Саму", 35.03) + 0.4, S(u"З", 49.40)]
for i, txt in enumerate(LIST):
    F.append(u'        <div id="l%d" class="shuf hid"><span class="chip"><b class="n">%d</b>%s</span></div>' % (i, i + 1, txt))
    js(u'  shuffle(["#l%d"], [%.3f], %.3f);' % (i, t_l[i], t_lo[i]))
    g.sfx("pop", t_l[i])

# 3 · FULL — a Claude chat as a platform-ad sequence: Quizlet ---------------------------
# No screenshot of hers for this: a clean Claude-like chat rebuilt in HTML, only
# the labels she says (конектор Quizlet, список слів / транскрипт, готовий сет,
# учень відкриває). Window 800×560, camera like reel 61.
f0 = S(u"У", 9.73) - 0.05
f1 = S(u"Друге", 18.70) - 0.5
CLAUDE = mark("claude", 30, "cm")
C.append(u"""
        <div id="stage">
          <div id="win">
            <div class="c-top">%(cl)s<span>Claude</span></div>
            <div id="menu" class="c-menu">
              <div class="c-mt">Конектори</div>
              <div id="mq" class="c-row"><i class="qz">Q</i>Quizlet<em id="tq"><u></u></em></div>
              <div class="c-row"><i style="background:#ECE6E6;color:#574142">N</i>Notion<em><u></u></em></div>
            </div>
            <div id="ans" class="c-ans">
              <div class="c-ah">%(cl)s<span>Готово — сет у Quizlet</span></div>
              <div class="c-set">
                <div class="c-sh"><i class="qz">Q</i><b>Нові слова уроку</b></div>
                <div class="c-mini"><span>homework</span><span>deadline</span><span>to borrow</span><span>rehearsal</span></div>
                <div id="opn" class="c-btn">Відкрити в Quizlet</div>
              </div>
            </div>
            <div id="inp" class="c-inp">
              <div class="c-plus">+</div>
              <div class="c-txt"><span id="typ">Зроби сет карток: homework, deadline, to borrow, rehearsal</span></div>
              <div class="c-send">↑</div>
            </div>
          </div>
          <div id="card" class="qcard"><div class="qf"><small>Quizlet</small>homework</div><div class="qb"><small>Quizlet</small>домашнє завдання</div></div>
        </div>""" % {"cl": CLAUDE})
EXTRA += u"""
    #cover { background: radial-gradient(120% 80% at 50% 35%, #FFFFFF 0%, #F6EFEF 70%, #F1E7E7 100%); }
    #stage { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; perspective: 2200px; }
    #win { position: absolute; left: 0; top: 0; width: 800px; height: 560px; background: #FAF9F5;
           border-radius: 18px; font-family: "Google Sans", sans-serif; color: #1f1f1f; overflow: hidden;
           box-shadow: 0 2px 6px rgba(36,25,25,.10), 0 30px 80px rgba(36,25,25,.22); will-change: transform; }
    #win > div { position: absolute; }
    .cm { fill: #D97757; }
    .c-top { left: 22px; top: 18px; display: flex; align-items: center; gap: 10px; font-size: 20px; font-weight: 500; }
    .qz { display: inline-flex; width: 26px; height: 26px; border-radius: 7px; background: #4255FF; color: #fff;
          font-style: normal; font-size: 15px; font-weight: 700; align-items: center; justify-content: center; }
    .c-menu { left: 40px; top: 300px; width: 290px; background: #fff; border-radius: 14px; padding: 10px;
              box-shadow: 0 6px 24px rgba(0,0,0,.14); }
    .c-mt { font-size: 12px; color: #6b6b6b; padding: 4px 8px 6px; }
    .c-row { display: flex; align-items: center; gap: 10px; font-size: 16px; padding: 8px; border-radius: 8px; position: relative; }
    .c-row i { width: 26px; height: 26px; border-radius: 7px; font-style: normal; font-size: 14px; font-weight: 700;
               display: inline-flex; align-items: center; justify-content: center; }
    .c-row em { position: absolute; right: 10px; top: 13px; width: 32px; height: 18px; border-radius: 9px; background: #C4C7C5; }
    .c-row em u { position: absolute; left: 2px; top: 2px; width: 14px; height: 14px; border-radius: 50%; background: #fff; }
    .c-inp { left: 40px; top: 446px; width: 720px; height: 82px; background: #fff; border: 1px solid #E3DED6;
             border-radius: 20px; box-shadow: 0 2px 8px rgba(0,0,0,.05); }
    .c-plus { position: absolute; left: 14px; top: 24px; width: 34px; height: 34px; border-radius: 50%;
              border: 1px solid #DDD; text-align: center; line-height: 32px; font-size: 22px; color: #555; }
    .c-txt { position: absolute; left: 62px; top: 28px; width: 590px; font-size: 18px; color: #1f1f1f; white-space: nowrap; overflow: hidden; }
    #typ { display: inline-block; clip-path: inset(0 100% 0 0); }
    .c-send { position: absolute; right: 14px; top: 22px; width: 38px; height: 38px; border-radius: 10px;
              background: #D97757; color: #fff; text-align: center; line-height: 38px; font-size: 20px; font-weight: 700; }
    .c-ans { left: 40px; top: 74px; width: 720px; }
    .c-ah { display: flex; align-items: center; gap: 10px; font-size: 18px; margin-bottom: 14px; }
    .c-set { background: #fff; border: 1px solid #E3DED6; border-radius: 16px; padding: 18px 20px; width: 480px; }
    .c-sh { display: flex; align-items: center; gap: 10px; font-size: 18px; margin-bottom: 14px; }
    .c-mini { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 16px; }
    .c-mini span { border: 1px solid #E6E8F0; border-radius: 10px; padding: 14px 12px; font-size: 16px; text-align: center;
                   box-shadow: 0 1px 2px rgba(0,0,0,.05); }
    .c-btn { display: inline-block; background: #4255FF; color: #fff; border-radius: 22px; padding: 10px 22px; font-size: 15px; font-weight: 500; }
    .qcard { position: absolute; left: 190px; top: 560px; width: 700px; height: 440px; transform-style: preserve-3d; }
    .qcard > div { position: absolute; inset: 0; background: #fff; border-radius: 36px; backface-visibility: hidden;
                   display: flex; align-items: center; justify-content: center; font-family: "Google Sans", sans-serif;
                   font-size: 76px; font-weight: 500; color: #241919; text-align: center; padding: 0 40px;
                   box-shadow: 0 2px 6px rgba(36,25,25,.10), 0 30px 80px rgba(36,25,25,.22); }
    .qcard .qb { transform: rotateY(180deg); font-size: 64px; }
    .qcard small { position: absolute; left: 34px; top: 26px; font-size: 26px; color: #4255FF; font-weight: 700; }
"""
t_kon, t_quiz = S(u"конектор", 11.14), S(u"Quizlet.", 11.52)
t_kyd, t_otr, t_uch, t_vidk = S(u"кидаєш", 12.36), S(u"отримуєш", 14.76), S(u"учень", 16.73), S(u"відкриває", 17.57)


def cam(px, py, sc, cx=540, cy=760):
    # the window scales about its own centre (400, 280): a point p of it lands at O + s*(p-O) + (x, y)
    return (round(cx - 400 - sc * (px - 400), 1), round(cy - 280 - sc * (py - 280), 1))


WIDE = (1.2,) + cam(400, 280, 1.2)
MEN = (2.6,) + cam(185, 345, 2.6)
INP = (1.7,) + cam(400, 487, 1.7)
ANS = (1.75,) + cam(285, 215, 1.75, cy=720)
js(u"""
  gsap.set("#win", {transformOrigin: "400px 280px"});
  gsap.set(["#menu", "#ans", "#card"], {autoAlpha: 0});
  gsap.set("#win", {x: %(wx)s, y: %(wy)s + 220, scale: %(ws)s * .86, rotationX: 24, rotationY: -20, rotationZ: 5});
  tl.to("#win", {x: %(wx)s, y: %(wy)s, scale: %(ws)s, rotationX: 9, rotationY: -12, rotationZ: 2, duration: 1.1, ease: "power3.out"}, %(f0)s + .1);
  tl.fromTo("#menu", {autoAlpha: 0, y: 12}, X({autoAlpha: 1, y: 0, duration: .3}), %(kon)s - .9);
  tl.to("#win", {x: %(mx)s, y: %(my)s, scale: %(ms)s, rotationX: 3, rotationY: 6, rotationZ: 0, duration: 1.0, ease: "power3.inOut"}, %(kon)s - .6);
  tl.to("#tq", {backgroundColor: "#4255FF", duration: .2}, %(quiz)s);
  tl.to("#tq u", {x: 14, duration: .3, ease: "back.out(2)"}, %(quiz)s);
  tl.to("#menu", {autoAlpha: 0, duration: .25}, %(kyd)s - .35);
  tl.to("#win", {x: %(ix)s, y: %(iy)s, scale: %(is)s, rotationX: -3, rotationY: -6, duration: 1.0, ease: "power3.inOut"}, %(kyd)s - .5);
  tl.fromTo("#typ", {clipPath: "inset(0 100%% 0 0)"}, X({clipPath: "inset(0 0%% 0 0)", duration: 1.9, ease: "steps(28)"}), %(kyd)s);
  tl.to("#typ", {autoAlpha: 0, duration: .2}, %(otr)s - .2);
  tl.fromTo("#ans", {autoAlpha: 0, y: 30}, X({autoAlpha: 1, y: 0, duration: .5, ease: "power3.out"}), %(otr)s);
  tl.to("#win", {x: %(ax)s, y: %(ay)s, scale: %(as)s, rotationX: 6, rotationY: 8, rotationZ: -1, duration: 1.1, ease: "power3.inOut"}, %(otr)s - .2);
  tl.to("#opn", {scale: .92, backgroundColor: "#2E3BBF", duration: .12, yoyo: true, repeat: 1}, %(uch)s + .3);
  tl.to("#win", {y: "-=260", scale: %(as)s * .8, rotationX: 14, duration: .9, ease: "power3.inOut"}, %(uch)s + .4);
  tl.fromTo("#card", {autoAlpha: 0, y: 220, rotationX: -30}, X({autoAlpha: 1, y: 0, rotationX: 0, duration: .7, ease: "power3.out"}), %(uch)s + .5);
  tl.to("#card", {rotationY: 180, duration: .7, ease: "power2.inOut"}, %(vidk)s + .15);
  full(%(f0)s, %(f1)s);
""" % {"wx": WIDE[1], "wy": WIDE[2], "ws": WIDE[0], "mx": MEN[1], "my": MEN[2], "ms": MEN[0],
       "ix": INP[1], "iy": INP[2], "is": INP[0], "ax": ANS[1], "ay": ANS[2], "as": ANS[0],
       "f0": "%.3f" % f0, "f1": "%.3f" % f1, "kon": "%.3f" % t_kon, "quiz": "%.3f" % t_quiz,
       "kyd": "%.3f" % t_kyd, "otr": "%.3f" % t_otr, "uch": "%.3f" % t_uch, "vidk": "%.3f" % t_vidk})
g.sfx("whoosh-short", f0); g.sfx("whoosh-short", t_kon - 0.6); g.sfx("click", t_quiz)
g.sfx("typing", t_kyd); g.sfx("notification", t_otr); g.sfx("click", t_uch + 0.3)
g.sfx("whoosh-short", t_vidk + 0.15); g.sfx("whoosh-short", f1)

# 4 · HALF — the scheme (Excalidraw): Fathom -> Claude (скіл) -> помилки + вправи; Notion -> картка учня
k0 = S(u"Fathom", 20.78) - 0.35
k1 = S(u"Третє", 32.47) - 0.55
HALF.append((k0, k1))
t_fat, t_cl2, t_skil = S(u"Fathom", 20.78), S(u"Claude", 22.02), S(u"скіл", 23.65)
t_pom, t_vpr, t_not, t_lah = S(u"помилки", 24.68), S(u"вправи", 25.98), S(u"Notion,", 29.72), S(u"лягти", 30.92)
js(u'''
  sketch("s1", "skP"); box("s1", 90, 300, 210, 112, {seed: 3}); label("s1", 195, 372, "Fathom", {size: 50});
  draw("s1", %.3f);
  sketch("s2", "skP"); arrow("s2", 305, 356, 425, 356, {seed: 5, bend: -.12});
  box("s2", 435, 300, 210, 112, {seed: 7, fill: true}); label("s2", 540, 372, "Claude", {size: 50});
  draw("s2", %.3f);
  sketch("s3", "skP"); label("s3", 540, 462, "+ скіл", {size: 44}); draw("s3", %.3f);
  sketch("s4", "skP"); arrow("s4", 520, 480, 340, 560, {seed: 9, bend: .15});
  box("s4", 120, 540, 260, 130, {seed: 11}); label("s4", 250, 593, "помилки", {size: 44});
  draw("s4", %.3f);
  sketch("s5", "skP"); label("s5", 250, 648, "вправи", {size: 44}); draw("s5", %.3f);
  sketch("s6", "skP"); arrow("s6", 650, 356, 770, 356, {seed: 13, bend: .12});
  box("s6", 780, 300, 210, 112, {seed: 15}); label("s6", 885, 372, "Notion", {size: 50});
  draw("s6", %.3f, .35);
  sketch("s7", "skP"); arrow("s7", 885, 420, 835, 545, {seed: 17, bend: -.2});
  box("s7", 660, 550, 320, 112, {seed: 19, fill: true}); label("s7", 820, 622, "картка учня", {size: 46});
  draw("s7", %.3f, .35);
  erase("s1", %.3f); erase("s2", %.3f); erase("s3", %.3f); erase("s4", %.3f); erase("s5", %.3f); erase("s6", %.3f); erase("s7", %.3f);
''' % (t_fat - 0.1, t_cl2 - 0.5, t_skil - 0.1, t_pom - 0.5, t_vpr - 0.1, t_not - 0.5, t_lah - 0.8,
       k1, k1, k1, k1, k1, k1, k1))
g.sfx("whoosh-short", k0); g.sfx("click-soft", t_cl2); g.sfx("click-soft", t_pom); g.sfx("click-soft", t_not)
g.sfx("pencil", t_lah - 0.3)

# 4b · MEME — «перевірку я б… не віддавала повністю Клоду» -> 13, the paw: «stop».
# Her line is a firm no; the paw says it. Clear stretch: list card 3 left at
# «Саму»+0.4, the checklist rises on «організовувати».
g.meme(F, J, "13", E(u"Клоду,", 38.02) + 0.1, dur=1.0, slot="r")

# 5 · ABOVE — a glass homework checklist: ticks, and the one nobody should miss ---------
t_org, t_maks, t_vytr, t_mozh = S(u"організовувати", 39.55), S(u"максимально", 41.64), S(u"витрачала", 43.69), S(u"можна.", 45.70)
F.append(u'''
        <div id="hw" class="glass hid" style="left:190px; top:290px; width:700px; padding:22px 30px">
          <div class="hd">Домашки<small>цей тиждень</small></div>
          <div class="hr"><i id="c1" class="cb"></i><span>Оля</span><em id="e1">здано</em></div>
          <div class="hr"><i id="c2" class="cb"></i><span>Марко</span><em id="e2">здано</em></div>
          <div class="hr" id="r3"><i class="cb"></i><span>Іра</span><em id="e3" class="wait">ще не здала</em></div>
        </div>''')
EXTRA += u"""
    .hr { display: flex; align-items: center; gap: 18px; font-size: 32px; font-weight: 500; color: #241919;
          padding: 9px 12px; border-top: 1px solid rgba(36,25,25,.08); border-radius: 14px; }
    .hr span { flex: 1; }
    .cb { width: 34px; height: 34px; border-radius: 9px; border: 3px solid #574142; position: relative; flex: none; }
    .hr em { font-style: normal; font-size: 26px; color: #574142; opacity: 0; }
    .hr em.wait { color: #7A1424; font-weight: 700; }
    .tick { position: absolute; left: 4px; top: -2px; width: 22px; height: 12px; border-left: 5px solid #fff;
            border-bottom: 5px solid #fff; transform: rotate(-45deg); transform-origin: 50% 50%; }
"""
js(u'''
  rise("#hw", %(org)s);
  ["#c1", "#c2"].forEach(function (s, i) {
    document.querySelector(s).innerHTML = '<b class="tick"></b>';
    tl.to(s, {backgroundColor: "#7A1424", borderColor: "#7A1424", duration: .2}, %(maks)s + i * .35);
    tl.fromTo(s + " .tick", {scale: 0}, X({scale: 1, duration: .3, ease: "back.out(2)"}), %(maks)s + i * .35);
    tl.to("#e" + (i + 1), {opacity: 1, duration: .25}, %(maks)s + i * .35);
  });
  tl.to("#r3", {backgroundColor: "rgba(122,20,36,.10)", duration: .3}, %(vytr)s);
  tl.to("#e3", {opacity: 1, duration: .25}, %(vytr)s);
  tl.to("#r3", {keyframes: {x: [0, -8, 7, -4, 2, 0]}, duration: .35, ease: "none"}, %(vytr)s + .1);
  sink("#hw", %(out)s);
''' % {"org": "%.3f" % t_org, "maks": "%.3f" % t_maks, "vytr": "%.3f" % t_vytr, "out": "%.3f" % (t_mozh + 0.3)})
g.sfx("pop", t_org); g.sfx("click-soft", t_maks); g.sfx("click-soft", t_maks + 0.35); g.sfx("notification", t_vytr)

# 6 · ABOVE — a glass level test: a question, then the scale --------------------------
t_pyt, t_shk, t_lanc = S(u"питання", 50.67), S(u"шкалу.", 51.53), S(u"Ланцюжок", 51.99)
F.append(u'''
        <div id="lt" class="glass hid" style="left:170px; top:290px; width:740px; padding:22px 30px">
          <div class="hd">Тест на рівень</div>
          <div class="q">She ___ to school every day.</div>
          <div class="opts"><span>go</span><span id="ok">goes</span><span>going</span></div>
          <div id="sc" class="scale"><span>A1</span><span>A2</span><span id="b1">B1</span><span>B2</span><span>C1</span><span>C2</span></div>
        </div>''')
EXTRA += u"""
    .q { font-size: 32px; color: #241919; margin-bottom: 14px; }
    .opts { display: flex; gap: 12px; }
    .opts span { font-size: 28px; padding: 8px 20px; border-radius: 14px; border: 2px solid #DEBFBF; background: rgba(255,255,255,.8); }
    .scale { display: flex; gap: 8px; margin-top: 16px; }
    .scale span { flex: 1; text-align: center; font-size: 28px; font-weight: 700; padding: 8px 0; border-radius: 12px;
                  background: #FFF0F0; color: #574142; }
"""
js(u'''
  rise("#lt", %.3f);
  tl.to("#ok", {backgroundColor: "#7A1424", borderColor: "#7A1424", color: "#fff", duration: .2}, %.3f);
  tl.fromTo("#sc span", {autoAlpha: 0, y: 14}, X({autoAlpha: 1, y: 0, duration: .3, stagger: .06, ease: "power3.out"}), %.3f);
  tl.to("#b1", {backgroundColor: "#7A1424", color: "#fff", duration: .2}, %.3f);
  sink("#lt", %.3f);
''' % (t_pyt - 0.3, t_pyt + 0.5, t_shk - 0.2, t_shk + 0.4, t_lanc + 0.6))
g.sfx("pop", t_pyt - 0.3); g.sfx("click-soft", t_shk)

# 7 · BEHIND — «SendPulse» -----------------------------------------------------------
t_sp, t_kodu = S(u"в SendPulse", 53.45), E(u"коду.", 54.27)
B.append(u'        <div id="bw2" class="big hid" data-layout-allow-occlusion style="top:430px; font-size:200px">SendPulse</div>')
g.matte("b2", round(t_sp - 0.7, 3), round(t_kodu - t_sp + 1.3, 3))
js(u'  rise("#bw2", %.3f); sink("#bw2", %.3f);' % (t_sp - 0.45, t_kodu + 0.2))
g.sfx("whoosh-short", t_sp - 0.45)
BLACKOUT.append((t_sp - 0.03, E(u"в SendPulse", 53.45)))

# 8 · ABOVE — a glass CRM card: the result lands as a lead --------------------------
t_pad, t_crm, t_lid, t_kval, t_tomu = S(u"падають", 56.25), S(u"CRM-систему.", 57.34), S(u"лідмагніт,", 58.85), S(u"і кваліфікація", 59.41), S(u"Тому", 61.87)
F.append(u'''
        <div id="crm" class="glass hid" style="left:170px; top:290px; width:740px; padding:22px 30px">
          <div class="hd">CRM<small>нові ліди</small></div>
          <div id="ld" class="lead"><b></b><span>Нова учениця<br><small>тест на рівень</small></span><em id="lv">B1</em></div>
          <div class="tags"><span id="tg1">лідмагніт</span><span id="tg2">кваліфікація</span></div>
        </div>''')
EXTRA += u"""
    .lead { display: flex; align-items: center; gap: 18px; background: rgba(255,255,255,.85); border-radius: 20px; padding: 14px 18px; }
    .lead b { width: 56px; height: 56px; border-radius: 50%; background: #7A1424; flex: none; }
    .lead span { flex: 1; font-size: 32px; font-weight: 500; color: #241919; line-height: 1.15; }
    .lead small { font-size: 24px; color: #574142; font-weight: 400; }
    .lead em { font-style: normal; font-size: 30px; font-weight: 700; color: #fff; background: #7A1424; border-radius: 14px; padding: 8px 16px; }
    .tags { display: flex; gap: 12px; margin-top: 14px; }
    .tags span { font-size: 26px; padding: 8px 18px; border-radius: 14px; border: 2px solid #DEBFBF; background: #FFF8F7; color: #574142; }
"""
js(u'''
  rise("#crm", %.3f);
  tl.fromTo("#ld", {autoAlpha: 0, y: -40}, X({autoAlpha: 1, y: 0, duration: .5, ease: "back.out(1.6)"}), %.3f);
  tl.set(["#tg1", "#tg2"], {autoAlpha: 0}, 0);
  pop("#tg1", %.3f); pop("#tg2", %.3f);
  sink("#crm", %.3f);
''' % (t_pad - 0.3, t_crm - 0.1, t_lid, t_kval + 0.1, t_tomu - 0.1))
g.sfx("pop", t_pad - 0.3); g.sfx("notification", t_crm - 0.1); g.sfx("click-soft", t_lid); g.sfx("click-soft", t_kval + 0.1)

# 9 · CTA — bookmark, then paper plane through the slot; the pill in the subtitle band ----
t_zb, t_per = S(u"збережи", 62.56), S(u"перешли", 64.75)
BM = u'<svg width="72" height="72" viewBox="0 0 24 24"><path d="M6 3h12v18l-6-4.5L6 21z" fill="#7A1424"/></svg>'
PL = u'<svg width="72" height="72" viewBox="0 0 24 24"><path d="M2 11.5 22 3l-8.5 19-2.6-8.1z" fill="#7A1424"/></svg>'
F.append(u'        <div id="ct1" class="shuf hid"><span class="chip ic">%s</span></div>' % BM)
F.append(u'        <div id="ct2" class="shuf hid"><span class="chip ic">%s</span></div>' % PL)
F.append(u'''        <div id="ctp" class="pill hid" style="left:0; right:0; margin:auto; width:max-content; top:1404px;
             font-size:46px; padding:28px 56px">Збережи і перешли колезі</div>''')
js(u'  shuffle(["#ct1", "#ct2"], [%.3f, %.3f], %.3f);' % (t_zb - 0.1, t_per - 0.1, DUR + 1))
js(u'  pop("#ctp", %.3f);' % (t_zb - 0.1))
g.sfx("pop", t_zb - 0.1); g.sfx("pop", t_per - 0.1)
BLACKOUT.append((t_zb - 0.15, DUR))

# ---------------------------------------------------------------- half screen + its matte
for i, (a, b) in enumerate(HALF):
    g.matte("half1", round(a - 0.1, 3), round(b - a + 1.0, 3))
    js("  half(%.3f, %.3f);" % (a, b))
    PLACE.append((a + 0.4, b + 0.2, "bottom", 858))


def main():
    chunks = g.chunks(CAPS, place=PLACE)
    doc = g.document(title=u"Reel 63 — автоматизації для викладачки мови", plate="assets/base.mp4",
                     behind="\n".join(B), panel="\n".join(P), front="\n".join(F), cover="\n".join(C),
                     js="\n".join(J), chunks=chunks, blackout=BLACKOUT, extra_css=EXTRA)
    g.write(HERE, doc)
    print("index.html  %d caption chunks, %d sfx cues, %d mattes" % (len(chunks), len(g.cues), len(g.mattes)))


if __name__ == "__main__":
    main()
