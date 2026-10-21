# -*- coding: utf-8 -*-
"""Reel 43 — «€400 чи €1300». Posts 2026-10-20.

Google style + Excalidraw (STYLE.md §00), cut from a tired take by tools/cut.py
(work/r43/cut-fix.json has every hand call).

The one object is **the bill**: what she pays an SMM every month, set against
what a system costs once — and then the payback, stacked month by month until
it reaches the one-off price.

  above   the SMM bill: €400 / місяць, 1 акаунт, reels in the feed — she gets
          sick, the reels drop out
  above   a consultation → her bill, twice → €800 / місяць, «дорого»
  behind  «система / €1300?»
  above   €400 every month vs €1300 once — «одноразова інвестиція»
  above   six calendar pages of 1300, struck out but the first; the rest tick
  half    the payback: a «1300» tower; «400 − Claude» blocks stack to it in
          ~3,5 months; two accounts / an editor stack «800» blocks, < 2 months
  above   СММниця, монтажер — both struck: «ні від кого не залежиш»
  above   your process, unchanged: reports, analytics, approve texts, scripts
  above   all the work: the unreliable SMM struck, Claude does it
  above   CTA — €1300 once, «Пиши + в коментарі»

usage: python build.py      (sfx.json is mixed by tools/sfx.py at render)
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
from gstyle import G, Words, load_caps, mark, esc  # noqa: E402

NN = "43"
CUT = json.load(io.open(os.path.join(ROOT, "work", "r" + NN, "cut.json"), encoding="utf-8"))
DUR = 62.683           # (1881 plate frames - 0.5) / 30
g = G(dur=DUR, reel=NN)

# whisper's spelling of what she plainly said -> her word (re-heard on the plate)
FIX = {
    u"мене": u"СММниці",
    u"якою": u"в якої",
    u"взагалі": u"взагалі-то", (u"то", 18.2): None,
    (u"Ти", 23.4): u"ти", u"щомісяця,": u"щомісяця",
    u"переховати": u"порахувати",
    u"клоун,": u"Claude,", (u"бла", 32.6): u"бла-бла-бла,", (u"бла", 32.8): None, u"бла,": None,
    u"опровнати": u"опрувнути",
    u"СММ,": u"СММник,",
    u"виконай": u"виконає", u"СММники.": u"СММники,",
    u"тому": u"Тому", u"систему": u"систему,",
    u"акаунт": u"акаунт,", u"налаштовуєш": u"налаштовуєш,",
}
# words whisper lost on the plate (solo pass, cut-fix.json): «залежиш», «Claude»
ADD = [
    {"w": u"залежиш.", "s": 43.44, "e": 43.95},
    {"w": u"Claude.", "s": 58.55, "e": 58.85},
]


def caps_with_adds():
    caps = load_caps(NN, FIX) + [dict(a) for a in ADD]
    caps.sort(key=lambda c: c["s"])
    for a, b in zip(caps, caps[1:]):
        a["e"] = round(max(a["s"] + 0.10, min(a["e"], b["s"] - 0.02)), 3)
    return caps


CAPS = caps_with_adds()
W = Words(CAPS)
S, E = W.s, W.e

# ---------------------------------------------------------------- the beats
B, P, F, C, J = [], [], [], [], []     # behind / panel / front / cover html, js
BLACKOUT = []
PLACE = []                             # caption placement over the half screens
HALF = []


def js(s):
    J.append(s)


F.append(u'<svg class="sk" id="skF" width="1080" height="1920" viewBox="0 0 1080 1920"></svg>')

REEL = u'''<span class="th" id="%s"><svg width="34" height="34" viewBox="0 0 34 34"><path d="M10 6 L28 17 L10 28 Z" fill="#7A1424"/></svg></span>'''
EXTRA_CSS = u'''
    .slot { width: 160px; height: 96px; border-radius: 18px; border: 3px dashed #DEBFBF;
            display: flex; align-items: center; justify-content: center; }
    .th { width: 160px; height: 96px; border-radius: 18px; background: #F2C7CA;
          display: flex; align-items: center; justify-content: center; margin: -3px; }
    .page { width: 112px; height: 150px; border-radius: 16px; background: #fff; position: relative;
            border: 3px solid #DEBFBF; overflow: hidden; flex: none; }
    .page b { position: absolute; left: 0; top: 0; width: 100%; height: 34px; background: #7A1424; }
    .page b::before, .page b::after { content: ""; position: absolute; top: 11px; width: 12px; height: 12px;
            border-radius: 50%; background: #fff; }
    .page b::before { left: 26px; } .page b::after { right: 26px; }
    .page span { position: absolute; left: 0; width: 100%; top: 62px; text-align: center;
                 font-weight: 700; font-size: 34px; letter-spacing: -0.02em; color: #241919; }
    .page .ok { left: 34px; top: 66px; }
    .col { flex: 1; }
    .ctr { position: absolute; left: 0; width: 1080px; display: flex; justify-content: center; }
    .sm { font-size: 34px; font-weight: 500; color: #574142; }
'''

# 1 · ABOVE — the SMM bill; she gets sick, the reels drop out ------------------
t_smm, t_400, t_akk = S(u"СММниці", 0.75), S(u"400", 1.39), S(u"один", 2.85)
t_zah, t_kon, t_nem = S(u"захворіла,", 4.07), S(u"контенту", 4.75), S(u"немає.", 5.93)
F.append(u'''
        <div id="b1" class="card hid" style="left:150px; top:300px; width:780px; padding:30px 40px;">
          <div class="row" style="justify-content:space-between">
            <span class="lbl" style="margin:0">СММниця</span>
            <span class="chip on hid" id="b1s" style="font-size:30px; padding:8px 20px">захворіла</span>
          </div>
          <div class="row" style="margin-top:8px; align-items:baseline; gap:14px">
            <span class="num hid" id="b1n" style="font-size:104px">€400</span>
            <span class="sm hid" id="b1m">/ місяць</span>
            <span class="chip hid" id="b1a" style="margin-left:auto; font-size:32px; padding:10px 20px"><i></i>1 акаунт</span>
          </div>
          <div class="row" style="margin-top:22px; gap:20px">
            %s
          </div>
        </div>''' % u"".join(u'<span class="slot">%s</span>' % (REEL % ("b1t%d" % i)) for i in range(4)))
js(u'''
  rise("#b1", %.3f);
  pop("#b1n", %.3f); fadein("#b1m", %.3f); pop("#b1a", %.3f);
  pop("#b1s", %.3f);
  tl.to("#b1t0, #b1t1, #b1t2, #b1t3", {autoAlpha: 0, scale: .3, duration: .35, ease: "power2.in", stagger: .18}, %.3f);
  sketch("x1", "skF"); ln("x1", 180, 540, 900, 600, {stroke: "#7A1424", strokeWidth: 6, seed: 3});
  draw("x1", %.3f, .45);
  sink("#b1", %.3f); erase("x1", %.3f);
''' % (0.05, t_400, S(u"місяць", 2.39), t_akk, t_zah, t_kon, t_nem - 0.1, 6.45, 6.45))
g.sfx("pop", 0.05); g.sfx("kaching", t_400); g.sfx("pop", t_zah)
BLACKOUT.append((t_400 - 0.05, E(u"акаунт", 3.09) + 0.05))

# 2 · ABOVE — a consultation; her bill, twice; €800, «дорого» -----------------
t_kons, t_same = S(u"консультацію", 8.0), S(u"саме", 9.46)
t_dva, t_800, t_dor = S(u"два акаунти,", 10.79), S(u"800", 12.01), S(u"дорого.", 13.87)
CAM = (u'<svg width="58" height="40" viewBox="0 0 58 40"><rect x="2" y="4" width="36" height="32" rx="8" fill="#7A1424"/>'
       u'<path d="M41 14 L56 6 V34 L41 26 Z" fill="#7A1424"/></svg>')
F.append(u'''
        <div class="ctr" style="top:340px"><div id="b2k" class="pill light hid" style="position:relative; padding:22px 44px; font-size:44px;">%s консультація</div></div>
        <div id="b2a" class="card hid" style="left:120px; top:310px; width:390px; padding:28px 34px;">
          <span class="lbl" style="margin-bottom:8px">акаунт 1</span>
          <div class="row" style="align-items:baseline; gap:10px"><span class="num" style="font-size:80px">€400</span><span class="sm">/ міс</span></div>
        </div>
        <div id="b2p" class="hid" style="position:absolute; left:510px; top:360px; width:60px; text-align:center;
             font-weight:700; font-size:72px; color:#7A1424">+</div>
        <div id="b2b" class="card hid" style="left:570px; top:310px; width:390px; padding:28px 34px;">
          <span class="lbl" style="margin-bottom:8px">акаунт 2</span>
          <div class="row" style="align-items:baseline; gap:10px"><span class="num" style="font-size:80px">€400</span><span class="sm">/ міс</span></div>
        </div>
        <div id="b2s" class="pill hid" style="left:190px; top:530px; padding:20px 46px; font-size:52px; font-weight:700">€800 / місяць</div>''' % CAM)
js(u'''
  pop("#b2k", %.3f);
  sink("#b2k", %.3f);
  rise("#b2a", %.3f);
  pop("#b2p", %.3f, .45); rise("#b2b", %.3f);
  pop("#b2s", %.3f, .6);
  sketch("d2", "skF"); label("d2", 690, 600, "дорого!", {size: 56, color: "#7A1424", anchor: "start"});
  under("d2", 684, 618, 870, {stroke: "#7A1424", seed: 9});
  draw("d2", %.3f, .45);
  sink("#b2a, #b2p, #b2b, #b2s", %.3f); erase("d2", %.3f);
''' % (t_kons, t_same - 0.4, t_same - 0.05, t_dva - 0.1, t_dva, t_800, t_dor - 0.1,
       S(u"І", 14.55) - 0.25, S(u"І", 14.55) - 0.25))
g.sfx("pop", t_kons); g.sfx("pop", t_dva); g.sfx("kaching", t_800)
BLACKOUT.append((t_800 - 0.05, t_800 + 0.05))      # the pill says «€800 / місяць»

# 3 · BEHIND — «система / €1300?» ---------------------------------------------
t_sys, t_1300, t_bil = S(u"система", 16.01), S(u"1300,", 16.77), S(u"більше?", 18.41)
m0, m1 = t_sys - 0.15, 19.30
B.append(u'''
        <div id="bw1" class="big hid" style="top:350px; font-size:240px">система</div>
        <div id="bw2" class="big hid" style="top:566px; font-size:240px">€1300<span id="bwq" style="visibility:hidden">?</span></div>''')
g.matte("sys", round(m0, 3), round(m1 - m0, 3))
js(u'''
  rise("#bw1", %.3f); rise("#bw2", %.3f);
  tl.fromTo("#bwq", {autoAlpha: 0, y: -40}, X({autoAlpha: 1, y: 0, duration: .5, ease: POP}), %.3f);
  sink("#bw1, #bw2", %.3f);
''' % (t_sys - 0.1, t_1300 - 0.1, t_bil, 18.88))
g.sfx("whoosh-short", t_sys - 0.1); g.sfx("kaching", t_1300)
BLACKOUT.append((t_sys - 0.05, t_sys + 0.05))      # «система за 1300,» stands behind her

# 4 · ABOVE — €400 every month vs €1300 once ----------------------------------
t_cyf, t_bil2, t_odn = S(u"цифри", 20.33), S(u"більше,", 20.65), S(u"одноразова", 21.55)
F.append(u'''
        <div id="b4" class="card hid" style="left:120px; top:310px; width:840px; padding:32px 40px;">
          <div class="row" style="align-items:flex-start; gap:30px">
            <div class="col"><span class="lbl">СММниця</span>
              <div class="row" style="align-items:baseline; gap:10px"><span class="num" style="font-size:84px; color:#241919">€400</span><span class="sm">/ міс</span></div></div>
            <div class="col"><span class="lbl">Система</span>
              <span class="num hid" id="b4n" style="display:block; font-size:84px">€1300</span>
              <span class="chip on hid" id="b4c" style="margin-top:18px; font-size:30px; padding:10px 20px"><i></i>одноразова інвестиція</span></div>
          </div>
        </div>''')
js(u'''
  rise("#b4", %.3f); pop("#b4n", %.3f); pop("#b4c", %.3f);
  sink("#b4", %.3f);
''' % (t_cyf - 0.2, t_bil2, t_odn, S(u"Тобто", 23.15) - 0.3))
g.sfx("pop", t_cyf - 0.2); g.sfx("click-soft", t_odn)

# 5 · ABOVE — six months of 1300, struck out but the first; the rest just work -
t_tob, t_shch, t_13b = S(u"Тобто", 23.15), S(u"щомісяця", 24.03), S(u"1300,", 24.65)
t_raz, t_dal, t_prac = S(u"раз", 25.99), S(u"далі", 26.93), S(u"працює", 27.67)
pages = u"".join(u'<div class="page hid" id="b5p%d"><b></b><span id="b5n%d">1300</span>'
                 u'<i class="check on hid ok" id="b5k%d" style="position:absolute"></i></div>' % (i, i, i)
                 for i in range(6))
F.append(u'''
        <div id="b5" class="card hid" style="left:120px; top:300px; width:840px; padding:30px 34px;">
          <div class="row" style="gap:20px">%s</div>
        </div>''' % pages)
js(u'''
  rise("#b5", %.3f);
  %s
  sketch("s5", "skF"); ln("s5", 290, 405, 935, 410, {stroke: "#7A1424", strokeWidth: 7, seed: 31});
  draw("s5", %.3f, .45);
  sketch("o5", "skF"); ell("o5", 220, 405, 170, 210, {stroke: "#7A1424", strokeWidth: 5, seed: 33});
  draw("o5", %.3f, .5);
  erase("s5", %.3f);
  tl.to("#b5n1, #b5n2, #b5n3, #b5n4, #b5n5", {autoAlpha: 0, duration: .25}, %.3f);
  %s
  sketch("w5", "skF"); label("w5", 540, 560, "далі просто працює", {size: 50, color: "#7A1424"});
  draw("w5", %.3f);
  sink("#b5", %.3f); erase("o5", %.3f); erase("w5", %.3f);
''' % (t_tob - 0.15,
       " ".join('pop("#b5p%d", %.3f, .45);' % (i, t_tob + 0.05 + i * 0.16) for i in range(6)),
       t_13b, t_raz - 0.35, t_dal - 0.05, t_dal - 0.05,
       " ".join('pop("#b5k%d", %.3f, .4);' % (i, t_dal + 0.1 + (i - 1) * 0.14) for i in range(1, 6)),
       t_prac, 28.85, 28.85, 28.85))
g.sfx("pop", t_tob - 0.15); g.sfx("click-soft", t_13b); g.sfx("click-soft", t_dal + 0.1)

# 6 · HALF — the payback ------------------------------------------------------
h0, h1 = S(u"Якщо", 29.28) - 0.1, 41.18
HALF.append((h0, h1))
P.append(u'<svg class="sk" id="skP" width="1080" height="1240" viewBox="0 0 1080 1240"></svg>')
t_por, t_akk1, t_4b = S(u"порахувати", 29.46), S(u"акаунт:", 30.24), S(u"400", 30.74)
t_min, t_cl = S(u"мінус", 31.61), S(u"Claude,", 32.37)
t_sys2, t_oku, t_des = S(u"система", 33.39), S(u"окупається", 33.71), S(u"десь", 34.29)
t_try, t_mis = S(u"три", 34.95), S(u"місяці.", 36.01)
t_dva2, t_mon = S(u"акаунтів", 37.26), S(u"монтажеру,", 39.18)
t_men, t_dva3 = S(u"менше", 40.24), S(u"два", 40.86)
# geometry: base y 740, the 1300 level y 400 (340 high); one account stacks a
# block of 340/3.5 a month, two accounts twice that, 1.75 blocks to the level
BASE, TOP = 740, 400
b1 = 340 / 3.5
js(u'''
  sketch("h1", "skP"); box("h1", 110, %(top)d, 200, %(hh)d, {seed: 41, fill: true});
  label("h1", 210, 585, "1300", {size: 64}); label("h1", 210, 800, "система", {size: 46});
  draw("h1", %(t1).3f, .7);
  sketch("h2", "skP"); label("h2", 510, 372, "1 акаунт", {size: 46}); draw("h2", %(t2).3f);
  sketch("h3", "skP"); box("h3", 400, %(y1).1f, 220, %(b).1f, {seed: 43, r: 18});
  label("h3", 510, %(ly1).1f, "400", {size: 48}); draw("h3", %(t3).3f, .55);
  sketch("h4", "skP"); label("h4", 634, %(ly1).1f, "– Claude", {size: 42, color: "#7A1424", anchor: "start"});
  ln("h4", 404, %(cy).1f, 616, %(cy).1f, {stroke: "#7A1424", strokeWidth: 5, seed: 45});
  draw("h4", %(t4).3f, .4);
  sketch("h5", "skP"); ln("h5", 312, %(top)d, 990, %(top)d, {stroke: "#7A1424", strokeWidth: 4, seed: 47});
  draw("h5", %(t5).3f, .6);
  sketch("h6", "skP"); box("h6", 400, %(y2).1f, 220, %(b).1f, {seed: 49, r: 18}); draw("h6", %(t6).3f, .45);
  sketch("h7", "skP"); box("h7", 400, %(y3).1f, 220, %(b).1f, {seed: 51, r: 18}); draw("h7", %(t7).3f, .45);
  sketch("h8", "skP"); box("h8", 400, %(top)d, 220, %(bh).1f, {seed: 53, r: 14, fill: true}); draw("h8", %(t8).3f, .45);
  sketch("h9", "skP"); label("h9", 510, 800, "~3,5 міс", {size: 52, color: "#7A1424"});
  under("h9", 420, 818, 600, {stroke: "#7A1424", seed: 55}); draw("h9", %(t9).3f, .45);
  erase("h4", %(t10).3f);
  sketch("r1", "skP"); label("r1", 830, 322, "2 акаунти", {size: 44}); box("r1", 720, %(ry1).1f, 220, %(b2).1f, {seed: 57, r: 18});
  label("r1", 830, %(rly1).1f, "800", {size: 52}); draw("r1", %(t11).3f, .55);
  sketch("r2", "skP"); label("r2", 830, 372, "або монтажер", {size: 40, color: "#574142"}); draw("r2", %(t12).3f);
  sketch("r3", "skP"); box("r3", 720, %(top)d, 220, %(rbh).1f, {seed: 59, r: 18, fill: true}); draw("r3", %(t13).3f, .45);
  sketch("r4", "skP"); label("r4", 830, 800, "< 2 міс", {size: 52, color: "#7A1424"});
  under("r4", 745, 818, 915, {stroke: "#7A1424", seed: 61}); draw("r4", %(t14).3f, .45);
  erase("h1", %(t15).3f); erase("h2", %(t15).3f); erase("h3", %(t15).3f); erase("h5", %(t15).3f);
  erase("h6", %(t15).3f); erase("h7", %(t15).3f); erase("h8", %(t15).3f); erase("h9", %(t15).3f);
  erase("r1", %(t15).3f); erase("r2", %(t15).3f); erase("r3", %(t15).3f); erase("r4", %(t15).3f);
''' % {"top": TOP, "hh": BASE - TOP, "b": b1, "b2": 2 * b1, "bh": BASE - TOP - 3 * b1,
       "y1": BASE - b1, "y2": BASE - 2 * b1, "y3": BASE - 3 * b1, "ly1": BASE - b1 / 2 + 17,
       "cy": BASE - b1 + 12, "ry1": BASE - 2 * b1, "rly1": BASE - b1 + 18, "rbh": BASE - TOP - 2 * b1,
       "t1": t_por - 0.1, "t2": t_akk1 - 0.15, "t3": t_4b - 0.1, "t4": t_min, "t5": t_oku - 0.1,
       "t6": t_des - 0.45, "t7": t_des - 0.1, "t8": t_try - 0.15, "t9": S(u"половиною", 35.53),
       "t10": t_mis + 0.5, "t11": t_dva2 - 0.1, "t12": t_mon - 0.3, "t13": t_men - 0.1, "t14": t_dva3 - 0.1,
       "t15": h1 + 0.9})
g.sfx("whoosh-short", h0); g.sfx("whoosh-short", h1)
g.sfx("kaching", t_4b); g.sfx("click-soft", t_oku)
g.sfx("pop", t_dva2); g.sfx("click-soft", t_dva3)

# 7 · ABOVE — nobody to depend on --------------------------------------------
t_ty, t_ni, t_zal = S(u"ти", 41.83), S(u"ні", 42.43), S(u"залежиш.", 43.44)
F.append(u'''
        <div id="b7" class="hid" style="position:absolute; left:120px; top:380px; width:840px;
             display:flex; gap:30px; justify-content:center">
          <span class="pill light hid" id="b7a" style="position:relative; padding:24px 48px">СММниця</span>
          <span class="pill light hid" id="b7b" style="position:relative; padding:24px 48px">монтажер</span>
        </div>''')
js(u'''
  fadein("#b7", %.3f, .01); pop("#b7a", %.3f); pop("#b7b", %.3f);
  sketch("x7", "skF"); ln("x7", 225, 432, 515, 445, {stroke: "#7A1424", strokeWidth: 7, seed: 71});
  ln("x7", 565, 445, 860, 432, {stroke: "#7A1424", strokeWidth: 7, seed: 73});
  draw("x7", %.3f, .35);
  sink("#b7", %.3f); erase("x7", %.3f);
''' % (t_ty - 0.1, t_ty - 0.1, S(u"більше", 41.95) + 0.1, t_ni, 43.9, 43.9))
g.sfx("pop", t_ty - 0.1); g.sfx("click-soft", t_ni)

# 8 · ABOVE — your process does not change -----------------------------------
t_pro, t_niak = S(u"процес", 45.7), S(u"ніяк", 46.02)
t_zv, t_an = S(u"звітність,", 47.88), S(u"аналітику.", 48.89)
t_op, t_sc = S(u"опрувнути", 50.49), S(u"сценарії.", 52.28)
rows = [(u"звітність", "a", t_zv), (u"аналітика", "b", t_an), (u"опрувнути тексти", "c", t_op),
        (u"продивитися сценарії", "d", t_sc)]
F.append(u'''
        <div id="b8" class="card hid" style="left:150px; top:300px; width:780px; padding:30px 40px;">
          <div class="row" style="justify-content:space-between; margin-bottom:16px">
            <span class="lbl" style="margin:0">Твій процес</span>
            <span class="chip on hid" id="b8n" style="font-size:30px; padding:8px 20px">не змінюється</span>
          </div>
          %s
        </div>''' % u"".join(
    u'<div class="row hid" id="b8r%s" style="margin-top:%dpx"><span class="check" id="b8k%s"></span>'
    u'<span style="font-size:40px; font-weight:500">%s</span></div>' % (k, 0 if i == 0 else 14, k, esc(t))
    for i, (t, k, _) in enumerate(rows)))
js(u'''
  rise("#b8", %.3f); pop("#b8n", %.3f);
  %s
  sink("#b8", %.3f);
''' % (t_pro - 0.25, t_niak,
       " ".join(u'rise("#b8r%s", %.3f, 24); tl.set("#b8k%s", {className: "check on"}, %.3f); pop("#b8k%s", %.3f, .45);'
                % (k, t - 0.15, k, t + 0.2, k, t + 0.2) for _, k, t in rows),
       S(u"А", 52.95) - 0.15))
g.sfx("pop", t_pro - 0.25)
for t in (t_zv, t_op):
    g.sfx("click-soft", t + 0.2)

# 9 · ABOVE — all the work: the unreliable SMM out, Claude in ------------------
t_vsia, t_rob = S(u"вся", 53.17), S(u"робота,", 53.59)
t_nen, t_to, t_cld = S(u"ненадійний", 55.17), S(u"то", 57.63), S(u"Claude.", 58.55)
F.append(u'''
        <div id="b9" class="card hid" style="left:150px; top:300px; width:780px; padding:30px 40px;">
          <span class="lbl" style="margin-bottom:16px">Вся робота</span>
          %s
          <div class="row" style="margin-top:24px; gap:16px; height:68px">
            <span class="sm">робить:</span>
            <span style="position:relative; display:inline-block">
              <span class="chip hid" id="b9s" style="white-space:nowrap">ненадійний СММник</span>
              <span class="chip on hid" id="b9c" style="position:absolute; left:0; top:0; white-space:nowrap">%s Claude</span>
            </span>
          </div>
        </div>''' % (u"".join(u'<div class="row" style="margin-top:%dpx"><span class="check" id="b9k%d"></span>'
                              u'<span class="line" style="width:%dpx"></span></div>' % (0 if i == 0 else 12, i, w)
                              for i, w in enumerate((470, 380, 520))), mark("claude", 34)))
js(u'''
  rise("#b9", %.3f);
  pop("#b9s", %.3f);
  sketch("x9", "skF"); ln("x9", 320, 592, 735, 586, {stroke: "#7A1424", strokeWidth: 7, seed: 91});
  draw("x9", %.3f, .35);
  tl.to("#b9s", {autoAlpha: 0, duration: .25}, %.3f); erase("x9", %.3f);
  pop("#b9c", %.3f);
  %s
  sink("#b9", %.3f);
''' % (t_vsia - 0.2, t_nen, t_to, S(u"твій", 58.32) - 0.05, S(u"твій", 58.32) - 0.05, t_cld - 0.15,
       " ".join(u'tl.set("#b9k%d", {className: "check on"}, %.3f); pop("#b9k%d", %.3f, .4);'
                % (i, t_cld + 0.1 + i * 0.12, i, t_cld + 0.1 + i * 0.12) for i in range(3)),
       S(u"ти готовий", 59.41) - 0.1))
g.sfx("pop", t_vsia - 0.2); g.sfx("pop", t_nen); g.sfx("notification", t_cld - 0.15)

# 10 · ABOVE — CTA ------------------------------------------------------------
t_inv, t_pysh = S(u"інвестувати", 59.85), S(u"пиши", 61.49)
F.append(u'''
        <div class="ctr" style="top:330px"><div id="b10a" class="pill light hid" style="position:relative; padding:22px 46px; font-size:46px">
          <b style="color:#7A1424; font-weight:700">€1300</b>&nbsp;· один раз</div></div>
        <div class="ctr" style="top:470px"><div id="b10b" class="pill hid" style="position:relative; font-size:52px; padding:30px 58px">Пиши + в коментарі</div></div>''')
js(u'''
  pop("#b10a", %.3f);
  pop("#b10b", %.3f, .6);
  sketch("a10", "skF"); arrow("a10", 905, 620, 960, 820, {stroke: "#7A1424", strokeWidth: 5, seed: 97, bend: -.25});
  draw("a10", %.3f, .5);
''' % (t_inv, t_pysh - 0.2, t_pysh + 0.35))
g.sfx("kaching", t_inv); g.sfx("pop", t_pysh - 0.2)
BLACKOUT.append((S(u"то", 61.31) - 0.05, DUR))     # the pill says it

# ---------------------------------------------------------------- mattes for the half screens
for i, (a, b) in enumerate(HALF):
    g.matte("half%d" % (i + 1), round(a - 0.1, 3), round(b - a + 1.2, 3))
    js("  half(%.3f, %.3f);" % (a, b))
    PLACE.append((a + 0.4, b + 0.2, "bottom", 980))


# her phrases, by the start time of their first word: the automatic chunker
# splits «СММниці 400 євро на / місяць» mid-thought on this fast take
PHRASES = [0.0, 1.39, 2.65, 3.57, 4.65, 7.18, 8.62, 10.27, 11.23, 12.01, 13.23, 14.55, 15.27, 16.01,
           17.39, 18.90, 20.33, 21.15, 23.15, 25.33, 26.77, 28.05, 29.28, 30.74, 32.63, 34.29, 36.63,
           37.98, 39.86, 41.63, 44.00, 45.28, 46.98, 48.59, 49.67, 51.68, 52.95, 54.57, 56.49, 57.63,
           58.87, 60.45, 61.31]
# the key word's pill, where the longest-word rule picks the wrong one
KEYS = {u"ненадійний": 55.17, u"немає.": 5.93, u"більше?": 18.41, u"щомісяця": 24.03, u"окупається": 33.71, u"три": 34.95,
        u"два,": 37.74, u"менше": 40.24, u"процес": 45.70, u"сценарії.": 52.28, u"робота,": 53.59}


def phrases(caps, place):
    out = []
    for c in caps:
        if not out or any(abs(c["s"] - t) < 0.06 for t in PHRASES):
            out.append([])
        out[-1].append(c)
    keyt = [W.s(w, t) for w, t in KEYS.items()]
    res = []
    for n, ch in enumerate(out):
        s = ch[0]["s"]
        nxt = out[n + 1][0]["s"] if n + 1 < len(out) else DUR
        hit = [i for i, w in enumerate(ch) if any(abs(w["s"] - t) < 0.01 for t in keyt)]
        kw = hit[0] if hit else (None if abs(s - 15.27) < 0.06 else g._key(ch, {}))
        pos = ("bottom", 1920 - 1520)
        for a, b, how, y in place:
            if a <= s < b:
                pos = (how, y if how == "top" else 1920 - y)
        res.append({"s": round(s, 3), "e": round(min(nxt, ch[-1]["e"] + 0.6), 3), "words": ch, "key": kw, "pos": pos})
    assert len(res) == len(PHRASES), (len(res), len(PHRASES))
    return res


def main():
    if "--words" in sys.argv:
        print(" ".join("%s/%.1f" % (c["w"], c["s"]) for c in CAPS))
    chunks = phrases(CAPS, PLACE)
    if "--chunks" in sys.argv:
        for n, c in enumerate(chunks):
            print("%2d %6.2f-%6.2f %s%s" % (n, c["s"], c["e"], " ".join(w["w"] for w in c["words"]),
                                           "  [%s]" % c["words"][c["key"]]["w"] if c["key"] is not None else ""))
    doc = g.document(title=u"Reel 43 — €400 чи €1300", plate="assets/base.mp4",
                     behind="\n".join(B), panel="\n".join(P), front="\n".join(F), cover="\n".join(C),
                     js="\n".join(J), chunks=chunks, blackout=BLACKOUT, extra_css=EXTRA_CSS)
    g.write(HERE, doc)
    print("index.html  %d caption chunks, %d sfx cues, %d mattes" % (len(chunks), len(g.cues), len(g.mattes)))


main()
