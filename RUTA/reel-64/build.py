# -*- coding: utf-8 -*-
"""Reel 64 — «Які автоматизації зробити коучці?». Batch 2026-11-20 (raw 20261120_135006).
STYLE.md §00 + her review of reel 61 (2026-11-23): natural editing, one meaningful
moment per sentence group; the five points run through ONE shuffle slot.

Chain: behind «Claude» (hook) -> shuffle 1 «Анкета перед сесією» -> FULL: the
pipeline as a platform ad (form -> sheet row lands -> Claude scheduled task,
Google Drive switched on -> a résumé, three rows tick on her words) -> shuffle 2
-> glass plan card 30/60/90 (fills, a line edited on «поправити», sent on
«відправити») -> shuffle 3 -> glass Telegram bot check-in -> shuffle 4 -> behind
«зникла» -> glass list of who went quiet, «Нагадати» pressed on «пушити» ->
shuffle 5 -> HALF: the after-session scheme Fathom -> Claude -> SendPulse ->
клієнтка -> CTA pill in the subtitle band.

usage: python3 build.py   (then: sh work/b1021/mattes.sh 64; python3 tools/sfx.py mix 64)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
from gstyle import G, Words, load_caps, mark  # noqa: E402

NN = "64"
DUR = 76.0            # (plate frames - 0.5) / 30
g = G(dur=DUR, reel=NN)
g.PANEL_TOP = 820

FIX = {
}
CAPS = load_caps(NN, FIX)
W = Words(CAPS)
S, E = W.s, W.e
# every beat on its word (STYLE §4a.1)
T = dict(
    claude0=S(u"з клод", 5.0),
    b1a=S(u"автоматизації", 4.3) - 0.9, b1b=E(u"зробила", 5.7) + 0.25,
    pt=[(S(u"Перше", 6.7) - 0.1, S(u"Звичайна", 9.1) - 0.2),
        (S(u"Друге", 24.4) - 0.1, S(u"Скіл", 27.6) - 0.1),
        (S(u"Третє", 37.4) - 0.1, S(u"Запланована", 39.5) + 0.3),
        (S(u"Четверте", 47.2) - 0.1, S(u"клієнтка", 49.2) - 0.1),
        (S(u"пʼяте", 60.6) - 0.1, S(u"Fathom", 63.0) - 0.6)],
    f0=S(u"Звичайна", 9.1) - 0.1, form=S(u"Google", 9.7),
    vidp=S(u"відповіді", 10.5), tabl=S(u"таблецію,", 11.6),
    drive=S(u"Drive", 13.1), shchor=S(u"щоранку", 16.3), rez=S(u"резюме", 17.7),
    chogo=S(u"чого", 19.5), zavazh=S(u"заважає,", 21.0), pochat=S(u"почати.", 21.8),
    f1=E(u"почати.", 21.8) + 0.2,
    pl0=S(u"Скіл", 27.6), plfill=S(u"збирає", 31.1) - 0.2, popr=S(u"поправити.", 34.1),
    vidpr=S(u"відправити.", 34.9), pl1=E(u"відправити.", 34.9) + 0.3,
    tg0=S(u"пише", 42.4), tg1=E(u"плану.", 45.4) + 0.3,
    b2a=S(u"клієнтка", 49.2) - 0.1, b2b=E(u"зникла.", 49.9) + 0.4,
    ls0=S(u"дивиться,", 51.7) - 0.2, row0=S(u"відповідає", 53.2), row1=S(u"застряг", 54.1),
    push=S(u"Пушить", 57.9), ls1=E(u"крок.", 59.9) + 0.2,
    k0=S(u"Fathom", 63.0) - 0.5, fath=S(u"Fathom", 63.0), cla5=S(u"Claude", 64.5), sam=S(u"самарі,", 65.3),
    sp5=S(u"син", 67.9), klnt=S(u"клієнтці.", 69.3), k1=E(u"клієнтці.", 69.3) + 0.2,
    cta=S(u"Збережеся", 72.5),
)

B, P, F, C, J = [], [], [], [], []
BLACKOUT, PLACE, HALF = [], [], []


def js(s):
    J.append(s)


P.append(u'<svg class="sk" id="skP" data-layout-allow-occlusion width="1080" height="1240" viewBox="0 0 1080 1240"></svg>')

EXTRA = u'''
    .glass { position: absolute; border-radius: 36px; background: rgba(255,255,255,.62);
             -webkit-backdrop-filter: blur(22px) saturate(1.5); backdrop-filter: blur(22px) saturate(1.5);
             box-shadow: inset 0 1px 0 rgba(255,255,255,.85), inset 0 0 0 1px rgba(255,255,255,.45),
                         0 12px 36px rgba(36,25,25,.16); }
    .shuf { position: absolute; left: 0; right: 0; margin: auto; width: max-content; top: 330px;
            transform-origin: 50% 100%; }
    .shuf .chip { font-size: 42px; padding: 18px 32px; background: #fff; border-color: #fff;
                  box-shadow: 0 1px 3px rgba(36,25,25,.10), 0 10px 30px rgba(36,25,25,.14); }
    .shuf .chip .n { font-weight: 700; color: #7A1424; margin-right: 4px; }
    .gc { left: 150px; top: 300px; width: 780px; padding: 24px 28px; font-family: "Google Sans", sans-serif; }
    .gc .hd { display: flex; align-items: center; gap: 14px; font-size: 26px; font-weight: 500;
              color: #574142; margin-bottom: 16px; }
    .gc .hd .mark { color: #7A1424; }
    .gc .hd .tm { margin-left: auto; font-size: 22px; color: #8a7475; }
    .bub { display: inline-block; border-radius: 26px; padding: 16px 24px; font-size: 32px;
           font-weight: 500; line-height: 1.25; background: rgba(255,255,255,.95); color: #241919;
           border-bottom-left-radius: 8px; }
    /* plan card */
    .cols { display: flex; gap: 16px; }
    .col { flex: 1; background: rgba(255,255,255,.92); border-radius: 22px; padding: 16px 18px; }
    .col b { display: block; font-size: 30px; font-weight: 700; color: #7A1424; margin-bottom: 12px; }
    .col .row { gap: 10px; margin-top: 10px; }
    .col .check { width: 30px; height: 30px; border-radius: 9px; border-width: 3px; }
    .col .check.on::after { left: 8px; top: 2px; width: 8px; height: 15px; border-width: 0 4px 4px 0; }
    .col .line { flex: 1; height: 14px; }
    .col .line.ed { background: #F2C7CA; }
    .gbtn { display: inline-flex; align-items: center; gap: 10px; border-radius: 999px; padding: 10px 24px;
            font-size: 26px; font-weight: 500; background: #7A1424; color: #fff; }
    .gbtn.done { background: #fff; color: #7A1424; box-shadow: inset 0 0 0 2px #7A1424; }
    /* who went quiet */
    .pp { display: flex; align-items: center; gap: 16px; background: rgba(255,255,255,.92);
          border-radius: 22px; padding: 14px 18px; margin-top: 12px; font-size: 30px; color: #241919; }
    .pp .av { width: 52px; height: 52px; border-radius: 50%; background: #F2C7CA; color: #7A1424;
              font-weight: 700; font-size: 26px; display: flex; align-items: center; justify-content: center; flex: none; }
    .pp .why { color: #574142; font-size: 26px; }
    .pp .gbtn { margin-left: auto; font-size: 24px; padding: 8px 20px; }
'''

# 1 · BEHIND — «Claude»: the hook word and the cover frame ------------------------
t_cl = T["claude0"]
B.append(u'        <div id="bw1" class="big hid" data-layout-allow-occlusion style="top:430px; font-size:230px">Claude</div>')
g.matte("b1", round(T["b1a"] - 0.3, 3), round(T["b1b"] - T["b1a"] + 0.7, 3))
js(u'  rise("#bw1", %.3f); sink("#bw1", %.3f);' % (T["b1a"], T["b1b"]))
g.sfx("whoosh-short", T["b1a"])

# 2 · SHUFFLE — the five points, one slot ------------------------------------------
PTS = [(u"1", u"Анкета перед першою сесією"), (u"2", u"План на 30 · 60 · 90 днів"),
       (u"3", u"Щоденні чек-іни"), (u"4", u"Сигнал: клієнтка зникла"), (u"5", u"Після сесії")]
for i, (n, txt) in enumerate(PTS):
    F.append(u'        <div id="pt%d" class="shuf hid"><span class="chip"><span class="n">%s</span>%s</span></div>' % (i, n, txt))
    a, b = T["pt"][i]
    js(u'  tl.fromTo("#pt%d", {autoAlpha: 0, y: 90, scale: .92, rotationX: -35}, X({autoAlpha: 1, y: 0, scale: 1, rotationX: 0, duration: .55, ease: "back.out(1.4)"}), %.3f);' % (i, a))
    js(u'  tl.to("#pt%d", {autoAlpha: 0, y: -80, scale: .92, rotationX: 35, duration: .4, ease: "power2.in"}, %.3f);' % (i, b))
    g.sfx("pop", a)

# 3 · FULL — point 1 as a platform ad: form -> sheet -> Claude task -> résumé -------
f0, f1 = T["f0"], T["f1"]
C.append(u"""
        <div id="stage">
          <div id="win">
            <div id="gf" class="pn" style="left:0;top:0;width:430px;height:520px">
              <div class="gf-band"></div>
              <div class="gf-t">Анкета перед першою сесією</div>
              <div class="gf-q">Чого ти хочеш насправді?</div><div class="gf-f"></div>
              <div class="gf-q">Що тобі заважає?</div><div class="gf-f"></div>
              <div class="gf-q">З чого хочеш почати?</div><div class="gf-f"></div>
              <div id="gfb" class="gf-b">Надіслати</div>
            </div>
            <div id="sh" class="pn" style="left:470px;top:0;width:430px;height:520px">
              <div class="sh-top"><i></i>Відповіді анкети</div>
              <div class="sh-g">
                <div class="sh-r sh-h"><span>Ім'я</span><span>Чого хоче</span><span>Що заважає</span></div>
                <div class="sh-r"><span><u></u></span><span><u></u></span><span><u></u></span></div>
                <div class="sh-r"><span><u></u></span><span><u></u></span><span><u></u></span></div>
                <div id="shn" class="sh-r sh-n"><span><u></u></span><span><u></u></span><span><u></u></span></div>
                <div class="sh-r"></div><div class="sh-r"></div>
              </div>
            </div>
            <div id="ct" class="pn" style="left:0;top:560px;width:900px;height:300px">
              <div class="ct-hd">%(claude)s<b>Запланована задача</b><span id="ctw" class="ct-ch">Щоранку</span></div>
              <div class="ct-p">Прочитай нові відповіді анкети й зроби коротке резюме по кожній новій клієнтці.</div>
              <div class="ct-c"><span class="ct-k">%(gdrive)s Google Drive<em id="ctg"><u></u></em></span></div>
            </div>
            <div id="rs" class="pn" style="left:0;top:900px;width:900px;height:340px">
              <div class="rs-t">Резюме · нова клієнтка</div>
              <div class="rs-r"><span id="rc0" class="check"></span><b>Чого хоче насправді</b><i class="line"></i></div>
              <div class="rs-r"><span id="rc1" class="check"></span><b>Що їй заважає</b><i class="line"></i></div>
              <div class="rs-r"><span id="rc2" class="check"></span><b>З чого почати</b><i class="line"></i></div>
            </div>
          </div>
        </div>""" % {"claude": mark("claude", 40), "gdrive": mark("googledrive", 30)})
EXTRA += u"""
    #cover { background: radial-gradient(120% 80% at 50% 35%, #FFFFFF 0%, #F6EFEF 70%, #F1E7E7 100%); }
    #stage { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; perspective: 2400px; }
    #win { position: absolute; left: 0; top: 0; width: 900px; height: 1240px; transform-origin: 0 0;
           font-family: "Google Sans", sans-serif; color: #1f1f1f; will-change: transform; }
    .pn { position: absolute; background: #fff; border-radius: 22px; overflow: hidden;
          box-shadow: 0 2px 6px rgba(36,25,25,.10), 0 24px 60px rgba(36,25,25,.18); }
    .gf-band { height: 14px; background: #673AB7; }
    .gf-t { font-size: 30px; font-weight: 700; line-height: 1.15; padding: 22px 26px 8px; }
    .gf-q { font-size: 20px; font-weight: 500; color: #3c4043; padding: 16px 26px 6px; }
    .gf-f { margin: 0 26px; height: 2px; background: #DADCE0; margin-top: 26px; }
    .gf-b { position: absolute; left: 26px; bottom: 26px; padding: 12px 26px; border-radius: 8px;
            background: #673AB7; color: #fff; font-size: 20px; font-weight: 500; }
    .sh-top { display: flex; align-items: center; gap: 12px; padding: 20px 22px; font-size: 22px; font-weight: 500;
              border-bottom: 1px solid #E3E3E3; }
    .sh-top i { width: 28px; height: 34px; border-radius: 4px; background: #1E8E3E; display: block; }
    .sh-r { display: grid; grid-template-columns: 1fr 1.3fr 1.3fr; height: 56px; border-bottom: 1px solid #E3E3E3; }
    .sh-r span { border-right: 1px solid #E3E3E3; padding: 0 12px; display: flex; align-items: center;
                 font-size: 17px; font-weight: 700; color: #3c4043; }
    .sh-r u { display: block; height: 10px; width: 80%; border-radius: 5px; background: #E8EAED; }
    .sh-h { background: #F8F9FA; }
    .sh-n u { background: #CEEAD6; }
    .ct-hd { display: flex; align-items: center; gap: 14px; padding: 26px 30px 12px; font-size: 30px; }
    .ct-hd .mark { color: #D97757; }
    .ct-ch { margin-left: auto; font-size: 24px; padding: 8px 20px; border-radius: 999px; background: #F3EEEE; color: #574142; }
    .ct-p { margin: 8px 30px; padding: 18px 22px; border: 2px solid #E6DEDE; border-radius: 16px;
            font-size: 24px; line-height: 1.4; color: #3c4043; }
    .ct-c { padding: 14px 30px; }
    .ct-k { display: inline-flex; align-items: center; gap: 12px; font-size: 24px; font-weight: 500;
            background: #F6F7F9; border-radius: 14px; padding: 12px 18px; }
    .ct-k .mark { color: #3c4043; }
    .ct-k em { position: relative; width: 52px; height: 28px; border-radius: 14px; background: #C4C7C5; margin-left: 16px; }
    .ct-k em u { position: absolute; left: 3px; top: 3px; width: 22px; height: 22px; border-radius: 50%; background: #fff;
                 box-shadow: 0 1px 2px rgba(0,0,0,.25); }
    .rs-t { font-size: 32px; font-weight: 700; padding: 28px 32px 10px; }
    .rs-r { display: flex; align-items: center; gap: 18px; padding: 16px 32px; }
    .rs-r b { font-size: 26px; font-weight: 500; white-space: nowrap; }
    .rs-r .line { flex: 1; height: 14px; }
"""
# camera: the canvas turns and scales about its centre O = (450, 620); a point p of
# it lands at O + s*(p - O) + (x, y). cam() centres point p on screen (cx, cy).
def cam(px, py, sc, cx=540, cy=840):
    return (round(cx - 450 - sc * (px - 450), 1), round(cy - 620 - sc * (py - 620), 1))
V = {
    "wide": (0.80,) + cam(450, 620, 0.80),
    "gf": (1.55,) + cam(215, 260, 1.55),
    "sh": (1.55,) + cam(685, 230, 1.55),
    "ct": (1.15,) + cam(450, 710, 1.15),
    "rs": (1.15,) + cam(450, 1070, 1.15),
}
def go(view, t, d=1.1, rx=0, ry=0, rz=0, ease="power3.inOut"):
    s, x, y = V[view]
    js(u'  tl.to("#win", {x: %s, y: %s, scale: %s, rotationX: %s, rotationY: %s, rotationZ: %s, duration: %s, ease: "%s"}, %.3f);'
       % (x, y, s, rx, ry, rz, d, ease, t))
s, x, y = V["wide"]
js(u"""
  gsap.set("#win", {transformOrigin: "450px 620px"});
  gsap.set("#win", {x: %s, y: %s + 240, scale: %s * .86, rotationX: 26, rotationY: -18, rotationZ: 5});
  tl.to("#win", {x: %s, y: %s, scale: %s, rotationX: 10, rotationY: -10, rotationZ: 2, duration: 1.2, ease: "power3.out"}, %.3f);
  full(%.3f, %.3f);
""" % (x, y, s, x, y, s, f0 + 0.1, f0, f1))
go("gf", T["form"] - 0.45, 1.0, 4, 8, 0)
js(u'  tl.fromTo("#gfb", {scale: 1}, X({scale: .92, duration: .15, yoyo: true, repeat: 1}), %.3f);' % (T["vidp"]))
go("sh", T["vidp"] + 0.2, 1.0, 3, -8, 0)
js(u'  tl.fromTo("#shn", {autoAlpha: 0, y: -30}, X({autoAlpha: 1, y: 0, duration: .45, ease: "back.out(1.6)"}), %.3f);' % T["tabl"])
js(u'  tl.fromTo("#shn", {backgroundColor: "rgba(30,142,62,.18)"}, X({backgroundColor: "rgba(30,142,62,0)", duration: 1.2}), %.3f);' % (T["tabl"] + 0.3))
go("ct", T["drive"] - 0.6, 1.1, 3, 2, 0)
js(u'  tl.to("#ctg", {backgroundColor: "#7A1424", duration: .2}, %.3f);' % T["drive"])
js(u'  tl.to("#ctg u", {x: 24, duration: .3, ease: "back.out(2)"}, %.3f);' % T["drive"])
js(u'  tl.to("#ctw", {backgroundColor: "#7A1424", color: "#fff", duration: .25}, %.3f);' % T["shchor"])
go("rs", T["rez"] - 0.5, 1.1, -2, -3, 0)
for i, k in enumerate(["chogo", "zavazh", "pochat"]):
    js(u'  tl.set("#rc%d", {className: "check on"}, %.3f);' % (i, T[k]))
    js(u'  tl.fromTo("#rc%d", {scale: .6}, X({scale: 1, duration: .4, ease: POP}), %.3f);' % (i, T[k]))
    g.sfx("click-soft", T[k])
go("wide", f1 - 0.9, 0.9, 8, 10, -1)
g.sfx("whoosh-short", f0); g.sfx("whoosh-short", T["form"] - 0.45); g.sfx("pop", T["tabl"])
g.sfx("whoosh-short", T["drive"] - 0.6); g.sfx("click", T["drive"]); g.sfx("whoosh-short", T["rez"] - 0.5)
g.sfx("whoosh-short", f1)

# 4 · ABOVE — the plan card: 30 / 60 / 90, edited, sent ----------------------------
cols = u""
for n in (u"30", u"60", u"90"):
    cols += (u'<div class="col"><b>%s днів</b>' % n +
             u''.join(u'<div class="row"><span class="check"></span><i class="line"></i></div>' for _ in range(2)) +
             u'</div>')
F.append(u'''
        <div id="pl" class="glass gc hid">
          <div class="hd">%s Скіл · план клієнтки<span class="tm"><span id="plb" class="gbtn">Надіслати</span></span></div>
          <div class="cols">%s</div>
        </div>''' % (mark("claude", 30), cols))
js(u'''
  rise("#pl", %(a).3f);
  tl.fromTo("#pl .col", {autoAlpha: 0, y: 24}, X({autoAlpha: 1, y: 0, duration: .45, stagger: .25, ease: RISE}), %(fill).3f);
  tl.to("#pl .col:nth-child(2) .row:nth-child(3) .line", {backgroundColor: "#F2C7CA", width: "60%%", duration: .4}, %(edit).3f);
  tl.set("#plb", {className: "gbtn done", textContent: "✓ Надіслано"}, %(send).3f);
  tl.fromTo("#plb", {scale: .8}, X({scale: 1, duration: .4, ease: POP}), %(send).3f);
  sink("#pl", %(b).3f);
''' % {"a": T["pl0"], "fill": T["plfill"], "edit": T["popr"], "send": T["vidpr"], "b": T["pl1"]})
g.sfx("pop", T["pl0"]); g.sfx("click-soft", T["popr"]); g.sfx("click", T["vidpr"])

# 5 · ABOVE — the Telegram bot check-in --------------------------------------------
F.append(u'''
        <div id="tg" class="glass gc hid">
          <div class="hd">%s Telegram-бот · через SendPulse<span class="tm">щовечора</span></div>
          <div><span class="bub">Як сьогодні з диханням? Вдалось зробити вправу з твого плану?</span></div>
        </div>''' % mark("telegram", 30))
js(u'  rise("#tg", %.3f); sink("#tg", %.3f);' % (T["tg0"], T["tg1"]))
g.sfx("notification", T["tg0"])

# 6 · BEHIND — «зникла» ----------------------------------------------------------------
B.append(u'        <div id="bw2" class="big hid" data-layout-allow-occlusion style="top:440px; font-size:230px">зникла</div>')
g.matte("b2", round(T["b2a"] - 0.3, 3), round(T["b2b"] - T["b2a"] + 0.7, 3))
js(u'  rise("#bw2", %.3f); sink("#bw2", %.3f);' % (T["b2a"], T["b2b"]))
g.sfx("whoosh-short", T["b2a"])

# 7 · ABOVE — who went quiet, and «Нагадати» pressed ----------------------------------
F.append(u'''
        <div id="ls" class="glass gc hid">
          <div class="hd">%s Тобі · клієнтки, які зникли</div>
          <div id="ls0" class="pp hid"><span class="av">О</span><span>Олена<br><span class="why">не відповідає кілька днів</span></span><span id="lb0" class="gbtn">Нагадати</span></div>
          <div id="ls1" class="pp hid"><span class="av">І</span><span>Ірина<br><span class="why">застрягла на одному кроці</span></span><span id="lb1" class="gbtn">Нагадати</span></div>
        </div>''' % mark("claude", 30))
js(u'''
  rise("#ls", %(a).3f);
  rise("#ls0", %(r0).3f, 30); rise("#ls1", %(r1).3f, 30);
  tl.set(["#lb0", "#lb1"], {className: "gbtn done", textContent: "✓ Надіслано"}, %(push).3f);
  tl.fromTo(["#lb0", "#lb1"], {scale: .8}, X({scale: 1, duration: .4, stagger: .12, ease: POP}), %(push).3f);
  sink("#ls", %(b).3f);
''' % {"a": T["ls0"], "r0": T["row0"], "r1": T["row1"], "push": T["push"], "b": T["ls1"]})
g.sfx("pop", T["ls0"]); g.sfx("notification", T["row1"] + 0.6); g.sfx("click", T["push"])

# 8 · HALF — after the session: Fathom -> Claude -> SendPulse -> клієнтка -------------
k0, k1 = T["k0"], T["k1"]
HALF.append((k0, k1))
js(u'''
  sketch("s1", "skP"); box("s1", 90, 310, 360, 120, {seed: 3}); label("s1", 270, 388, "Fathom: дзвінок", {size: 48});
  draw("s1", %(a).3f);
  sketch("s2", "skP"); arrow("s2", 455, 370, 590, 370, {seed: 5, bend: -.08});
  box("s2", 600, 290, 390, 260, {seed: 7, fill: true}); label("s2", 795, 360, "Claude", {size: 58});
  draw("s2", %(b).3f);
  sketch("s3", "skP"); label("s3", 795, 425, "самарі", {size: 42}); label("s3", 795, 475, "домовленості", {size: 42});
  label("s3", 795, 525, "задачі", {size: 42});
  draw("s3", %(c).3f);
  sketch("s4", "skP"); arrow("s4", 600, 500, 330, 600, {seed: 9, bend: .1});
  box("s4", 90, 610, 350, 120, {seed: 11}); label("s4", 265, 688, "SendPulse", {size: 52});
  draw("s4", %(d).3f);
  sketch("s5", "skP"); arrow("s5", 450, 670, 610, 670, {seed: 15, bend: -.06});
  ell("s5", 800, 670, 340, 130, {seed: 17}); label("s5", 800, 686, "клієнтка", {size: 50});
  draw("s5", %(e).3f);
  erase("s1", %(z).3f); erase("s2", %(z).3f); erase("s3", %(z).3f); erase("s4", %(z).3f); erase("s5", %(z).3f);
''' % {"a": T["fath"] - 0.3, "b": T["cla5"] - 0.5, "c": T["sam"] - 0.1, "d": T["sp5"] - 0.6,
       "e": T["klnt"] - 0.4, "z": k1})
g.sfx("whoosh-short", k0); g.sfx("click-soft", T["cla5"]); g.sfx("click-soft", T["sp5"]); g.sfx("pop", T["klnt"])

# 9 · CTA — the pill in the subtitle band ----------------------------------------------
F.append(u'''        <div id="ctp" class="pill hid" style="left:0; right:0; margin:auto; width:max-content; top:1404px;
             font-size:44px; padding:28px 50px">Збережи і перешли знайомій коучці</div>''')
js(u'  pop("#ctp", %.3f);' % T["cta"])
g.sfx("pop", T["cta"])
BLACKOUT.append((T["cta"] - 0.05, DUR))

for i, (a, b) in enumerate(HALF):
    g.matte("half%d" % (i + 1), round(a - 0.1, 3), round(b - a + 1.2, 3))
    js("  half(%.3f, %.3f);" % (a, b))
    PLACE.append((a + 0.4, b + 0.2, "bottom", 938))


def main():
    chunks = g.chunks(CAPS, place=PLACE)
    doc = g.document(title=u"Reel 64 — автоматизації для коучки", plate="assets/base.mp4",
                     behind="\n".join(B), panel="\n".join(P), front="\n".join(F), cover="\n".join(C),
                     js="\n".join(J), chunks=chunks, blackout=BLACKOUT, extra_css=EXTRA)
    g.write(HERE, doc)
    print("index.html  %d caption chunks, %d sfx cues, %d mattes" % (len(chunks), len(g.cues), len(g.mattes)))


main()
