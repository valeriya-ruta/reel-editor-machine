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
DUR = 76.183           # (2286 plate frames - 0.5) / 30
g = G(dur=DUR, reel=NN)
g.PANEL_TOP = 820      # panel captions: bottom 938, her pushed hair at ≈ 960

FIX = {
    u"з клод": u"з Claude", (u"По", 6.3): None, u"Перше": u"По-перше,", u"Форума.": u"Форма.",
    u"таблецію,": u"таблицю,", u"а контактеру": u"а конектор", u"бирає": u"бере",
    u"транскритує": u"транскрипт", u"противитися,": u"подивитися,", u"поправити.": u"поправити",
    u"ганіально.": u"геніально.", u"симпульс": u"SendPulse", (u"ще", 48.8): u"що", u"Та": u"та",
    u"шли": u"шле", u"людей?": u"людей,", u"Пушить": u"пушить", u"їх.": u"їх,", u"Власне,": u"власне,",
    u".ц": u"це", u"син": u"SendPulse", u"пульс": None, u"націлається": u"надсилає",
    u"треба.": u"треба", u"зробила": u"зробила.", u"Четверте": u"четверте", u"Збережеся": u"Збережи,", (u"ми", 73.3): u"щоб не", u"Тобто": u"Тобто,",
}
CAPS = load_caps(NN, FIX)
W = Words(CAPS)
S, E = W.s, W.e
# every beat on its word (STYLE §4a.1)
T = dict(
    cl=S(u"з Claude", 5.0), cle=E(u"з Claude", 5.0), zrob=E(u"зробила", 5.74),
    pt=[S(u"По-перше,", 6.66) - 0.1, S(u"Друге", 24.43) - 0.1, S(u"чек-іни.", 38.88) - 0.4,
        S(u"четверте", 47.22) - 0.1, S(u"пʼяте", 60.6) - 0.1],
    pt_out=[S(u"Звичайна", 9.14) - 0.15, S(u"Скіл", 27.63) - 0.05, S(u"Запланована", 39.47) + 0.3,
            S(u"клієнтка", 49.17) + 0.6, S(u"Fathom", 63.02) - 0.55],
    f0=S(u"Звичайна", 9.14) - 0.1, form=S(u"Google", 9.74),
    vidp=S(u"відповіді", 10.49), tabl=S(u"таблицю,", 11.57),
    drive=S(u"Drive", 13.09), shchor=S(u"щоранку", 16.34), rez=S(u"резюме", 17.72),
    chogo=S(u"чого", 19.47), zavazh=S(u"заважає,", 21.05), pochat=S(u"почати.", 21.83),
    f1=E(u"почати.", 21.83) + 0.2,
    pl0=S(u"Скіл", 27.63), plfill=S(u"збирає", 31.08) - 0.2, popr=S(u"поправити", 34.06),
    vidpr=S(u"відправити.", 34.86), pl1=E(u"відправити.", 34.86) + 0.2,
    gen=E(u"геніально.", 36.76),
    tg0=S(u"пише", 42.36), tg1=E(u"плану.", 45.45) + 0.3,
    znykla=E(u"зникла.", 49.85),
    ls0=S(u"дивиться,", 51.66) - 0.2, row0=S(u"відповідає", 53.19), row1=S(u"застряг", 54.09),
    push=S(u"пушить", 57.93), ls1=E(u"крок.", 59.95),
    k0=S(u"Fathom", 63.02) - 0.5, fath=S(u"Fathom", 63.02), cla5=S(u"Claude", 64.47), sam=S(u"самарі,", 65.33),
    sp5=S(u"SendPulse", 67.87), klnt=S(u"клієнтці.", 69.35), k1=E(u"клієнтці.", 69.35) + 0.2,
    cta=S(u"Збережи,", 72.53),
)
g.cta_start = T["cta"]

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
B.append(u'        <div id="bw1" class="big hid" data-layout-allow-occlusion style="top:430px; font-size:230px">Claude</div>')
g.matte("b1", round(T["cl"] - 0.6, 3), round(T["zrob"] - T["cl"] + 1.2, 3))
js(u'  rise("#bw1", %.3f); sink("#bw1", %.3f);' % (T["cl"] - 0.35, T["zrob"] + 0.25))
g.sfx("whoosh-short", T["cl"] - 0.35)
BLACKOUT.append((T["cl"] - 0.03, T["cle"]))

# 2 · SHUFFLE — the five points pass through ONE slot, each on its word -----------
PTS = [(u"1", u"Анкета перед першою сесією"), (u"2", u"План на 30 · 60 · 90 днів"),
       (u"3", u"Щоденні чек-іни"), (u"4", u"Сигнал: клієнтка зникла"), (u"5", u"Після сесії")]
for i, (n, txt) in enumerate(PTS):
    F.append(u'        <div id="pt%d" class="shuf hid"><span class="chip"><span class="n">%s</span>%s</span></div>' % (i, n, txt))
    js(u'  shuffle(["#pt%d"], [%.3f], %.3f);' % (i, T["pt"][i], T["pt_out"][i]))
    g.sfx("pop", T["pt"][i])

# 3 · FULL — point 1 as a platform ad: form -> sheet -> Claude task -> résumé -------
# The window is 980 x 1110 at scale 1 on the wide view (91 % of the frame width,
# y 285-1395, clear of the caption band); body text >= 30 px, labels >= 26 px.
# Layout: task (top), résumé, then form + sheet at the bottom, so zooming into
# the form/sheet pushes the rest up (off the top), never under the captions.
f0, f1 = T["f0"], T["f1"]
C.append(u"""
        <div id="stage">
          <div id="win">
            <div id="gf" class="pn" style="left:0;top:590px;width:470px;height:520px">
              <div class="gf-band"></div>
              <div class="gf-t">Анкета перед першою сесією</div>
              <div class="gf-q">Чого ти хочеш насправді?</div><div class="gf-f"></div>
              <div class="gf-q">Що тобі заважає?</div><div class="gf-f"></div>
              <div class="gf-q">З чого почати?</div><div class="gf-f"></div>
              <div id="gfb" class="gf-b">Надіслати</div>
            </div>
            <div id="sh" class="pn" style="left:510px;top:590px;width:470px;height:520px">
              <div class="sh-top"><i></i>Відповіді анкети</div>
              <div class="sh-g">
                <div class="sh-r sh-h"><span>Ім'я</span><span>Хоче</span><span>Заважає</span></div>
                <div class="sh-r"><span><u></u></span><span><u></u></span><span><u></u></span></div>
                <div class="sh-r"><span><u></u></span><span><u></u></span><span><u></u></span></div>
                <div id="shn" class="sh-r sh-n"><span><u></u></span><span><u></u></span><span><u></u></span></div>
                <div class="sh-r"><span></span><span></span><span></span></div>
                <div class="sh-r"><span></span><span></span><span></span></div>
              </div>
            </div>
            <div id="ct" class="pn" style="left:0;top:0;width:980px;height:270px">
              <div class="ct-hd">%(claude)s<b>Запланована задача</b><span id="ctw" class="ct-ch">Щоранку</span></div>
              <div class="ct-p">Прочитай нові відповіді анкети й зроби коротке резюме по кожній новій клієнтці.</div>
              <div class="ct-c"><span class="ct-k">%(gdrive)s Google Drive<em id="ctg"><u></u></em></span></div>
            </div>
            <div id="rs" class="pn" style="left:0;top:300px;width:980px;height:260px">
              <div class="rs-t">Резюме · нова клієнтка</div>
              <div class="rs-r"><span id="rc0" class="check"></span><b>Чого хоче насправді</b><i class="line"></i></div>
              <div class="rs-r"><span id="rc1" class="check"></span><b>Що їй заважає</b><i class="line"></i></div>
              <div class="rs-r"><span id="rc2" class="check"></span><b>З чого почати</b><i class="line"></i></div>
            </div>
          </div>
        </div>""" % {"claude": mark("claude", 44), "gdrive": mark("googledrive", 34)})
EXTRA += u"""
    #cover { background: radial-gradient(120% 80% at 50% 35%, #FFFFFF 0%, #F6EFEF 70%, #F1E7E7 100%); }
    #stage { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; perspective: 2400px; }
    #win { position: absolute; left: 0; top: 0; width: 980px; height: 1110px; transform-origin: 490px 555px;
           font-family: "Google Sans", sans-serif; color: #1f1f1f; will-change: transform; }
    .pn { position: absolute; background: #fff; border-radius: 26px; overflow: hidden;
          box-shadow: 0 2px 6px rgba(36,25,25,.10), 0 24px 60px rgba(36,25,25,.18); }
    .gf-band { height: 16px; background: #7A1424; }
    .gf-t { font-size: 38px; font-weight: 700; line-height: 1.12; padding: 24px 30px 4px; }
    .gf-q { font-size: 30px; font-weight: 500; color: #3c4043; padding: 22px 30px 0; }
    .gf-f { margin: 30px 30px 0; height: 3px; background: #DADCE0; }
    .gf-b { position: absolute; left: 30px; bottom: 28px; padding: 14px 32px; border-radius: 12px;
            background: #7A1424; color: #fff; font-size: 30px; font-weight: 500; }
    .sh-top { display: flex; align-items: center; gap: 14px; padding: 24px 26px; font-size: 32px; font-weight: 500;
              border-bottom: 2px solid #E3E3E3; }
    .sh-top i { width: 32px; height: 40px; border-radius: 5px; background: #7A1424; display: block; flex: none; }
    .sh-r { display: grid; grid-template-columns: 1fr 1fr 1.25fr; height: 70px; border-bottom: 2px solid #E3E3E3; }
    .sh-r span { border-right: 2px solid #E3E3E3; padding: 0 14px; display: flex; align-items: center;
                 font-size: 26px; font-weight: 700; color: #3c4043; }
    .sh-r u { display: block; height: 14px; width: 80%; border-radius: 7px; background: #E8EAED; }
    .sh-h { background: #F8F9FA; }
    .sh-n u { background: #F2C7CA; }
    .ct-hd { display: flex; align-items: center; gap: 16px; padding: 26px 32px 10px; font-size: 38px; }
    .ct-hd .mark { color: #7A1424; }
    .ct-ch { margin-left: auto; font-size: 30px; padding: 8px 24px; border-radius: 999px; background: #F3EEEE; color: #574142; }
    .ct-p { margin: 8px 32px; padding: 14px 22px; border: 2px solid #E6DEDE; border-radius: 18px;
            font-size: 30px; line-height: 1.3; color: #3c4043; }
    .ct-c { padding: 10px 32px; }
    .ct-k { display: inline-flex; align-items: center; gap: 14px; font-size: 30px; font-weight: 500;
            background: #F6F7F9; border-radius: 16px; padding: 10px 20px; }
    .ct-k .mark { color: #3c4043; }
    .ct-k em { position: relative; width: 64px; height: 36px; border-radius: 18px; background: #C4C7C5; margin-left: 18px; }
    .ct-k em u { position: absolute; left: 4px; top: 4px; width: 28px; height: 28px; border-radius: 50%; background: #fff;
                 box-shadow: 0 1px 2px rgba(0,0,0,.25); }
    .rs-t { font-size: 36px; font-weight: 700; padding: 24px 32px 6px; }
    .rs-r { display: flex; align-items: center; gap: 20px; padding: 10px 32px; }
    .rs-r .check { width: 40px; height: 40px; flex: none; }
    .rs-r b { font-size: 32px; font-weight: 500; white-space: nowrap; }
    .rs-r .line { flex: 1; height: 16px; }
"""
# camera: the window turns and scales about its centre O = (490, 555); a point p of
# it lands at O + s*(p - O) + (x, y). cam() centres point p on screen (cx, cy).
def cam(px, py, sc, cx=540, cy=840):
    return (round(cx - 490 - sc * (px - 490), 1), round(cy - 555 - sc * (py - 555), 1))
V = {
    "wide": (1.0,) + cam(490, 555, 1.0),
    "gf": (1.6,) + cam(235, 850, 1.6, 540, 830),
    "sh": (1.6,) + cam(745, 850, 1.6, 540, 830),
    # ct / rs span the window's width: no zoom past the frame, a near-wide move
    "ct": (1.04,) + cam(490, 555, 1.04, 540, 850),
    "rs": (1.04,) + cam(490, 555, 1.04, 540, 830),
}
def go(view, t, d=1.1, rx=0, ry=0, rz=0, ease="power3.inOut"):
    s, x, y = V[view]
    js(u'  tl.to("#win", {x: %s, y: %s, scale: %s, rotationX: %s, rotationY: %s, rotationZ: %s, duration: %s, ease: "%s"}, %.3f);'
       % (x, y, s, rx, ry, rz, d, ease, t))
# it lands straight on the form (one tween: an overlapping entrance tween would
# win the last frames sequentially rendered and flash back to wide)
s, x, y = V["wide"]
gs, gx, gy = V["gf"]
js(u"""
  gsap.set("#win", {x: %s, y: %s + 240, scale: %s * .86, rotationX: 24, rotationY: -18, rotationZ: 4});
  tl.to("#win", {x: %s, y: %s, scale: %s, rotationX: 4, rotationY: 8, rotationZ: 0, duration: 1.2, ease: "power3.out"}, %.3f);
  full(%.3f, %.3f);
""" % (x, y, s, gx, gy, gs, f0 + 0.1, f0, f1))
js(u'  tl.fromTo("#gfb", {scale: 1}, X({scale: .92, duration: .15, yoyo: true, repeat: 1}), %.3f);' % (T["vidp"]))
go("sh", T["vidp"] + 0.2, 1.0, 3, -8, 0)
js(u'  tl.fromTo("#shn", {autoAlpha: 0, y: -30}, X({autoAlpha: 1, y: 0, duration: .45, ease: "back.out(1.6)"}), %.3f);' % T["tabl"])
js(u'  tl.fromTo("#shn", {backgroundColor: "rgba(122,20,36,.14)"}, X({backgroundColor: "rgba(122,20,36,0)", duration: 1.2}), %.3f);' % (T["tabl"] + 0.3))
go("ct", T["drive"] - 0.6, 1.1, 4, 3, 0)
js(u'  tl.to("#ctg", {backgroundColor: "#7A1424", duration: .2}, %.3f);' % T["drive"])
js(u'  tl.to("#ctg u", {x: 28, duration: .3, ease: "back.out(2)"}, %.3f);' % T["drive"])
js(u'  tl.to("#ctw", {backgroundColor: "#7A1424", color: "#fff", duration: .25}, %.3f);' % T["shchor"])
go("rs", T["rez"] - 0.5, 1.1, -3, -4, 0)
for i, k in enumerate(["chogo", "zavazh", "pochat"]):
    js(u'  tl.set("#rc%d", {className: "check on"}, %.3f);' % (i, T[k]))
    js(u'  tl.fromTo("#rc%d", {scale: .6}, X({scale: 1, duration: .4, ease: POP}), %.3f);' % (i, T[k]))
    g.sfx("click-soft", T[k])
go("wide", f1 - 0.9, 0.9, 7, 9, -1)
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

# MEME — «Мені здається, що це взагалі геніально» -> 35 deal-with-it hamster ---------
g.meme(F, J, "35", T["gen"] + 0.1, dur=1.0, slot="r")

# 5 · ABOVE — the Telegram bot check-in --------------------------------------------
F.append(u'''
        <div id="tg" class="glass gc hid">
          <div class="hd">%s Telegram-бот · через SendPulse<span class="tm">щовечора</span></div>
          <div><span class="bub">Як сьогодні з диханням? Вдалось зробити вправу з твого плану?</span></div>
        </div>''' % mark("telegram", 30))
js(u'  rise("#tg", %.3f); sink("#tg", %.3f);' % (T["tg0"], T["tg1"]))
g.sfx("notification", T["tg0"])

# MEME — «клієнтка зникла» -> 59 «алівідерчі» (the bird peeking out, bye) ------------
# (in place of a second behind-me word: one moment for this line, not two)
g.meme(F, J, "59", T["znykla"] + 0.1, dur=1.0, slot="top")

# 7 · ABOVE — who went quiet, and «Нагадати» pressed ----------------------------------
F.append(u'''
        <div id="ls" class="glass gc hid">
          <div class="hd">%s Тобі · клієнтки, які зникли</div>
          <div id="ls0" class="pp hid"><span class="av">К</span><span>Клієнтка<br><span class="why">не відповідає кілька днів</span></span><span id="lb0" class="gbtn">Нагадати</span></div>
          <div id="ls1" class="pp hid"><span class="av">К</span><span>Клієнтка<br><span class="why">застрягла на одному кроці</span></span><span id="lb1" class="gbtn">Нагадати</span></div>
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
