# -*- coding: utf-8 -*-
"""Reel 46 — «Два акаунти, одна система». Posts 2026-10-21.

Google style + Excalidraw look (STYLE.md §00). The one object is **the two
accounts as two columns**: one «AI-система» pill under two account cards is
split by the panel into two columns with a wall between, which fill with their
own skills; the routine fills the same columns with different people; several
accounts double the setup; the exception folds the two back into one blog.

  above   two IG account cards: особистий / професійний, свій / школа
  above   cards shrink, «AI-система» pill under both; circled, split «?»
  half    two columns, a red wall, скіл сценариста / tone of voice /
          дизайн-система each side, ⇄ across the wall
  above   two posts dealt left / right to the two accounts
  behind  «дві / окремі»
  half    «рутина»: one analysis struck out; competitors as people, ≠, the wall
  above   the cards again; the setup checklist doubles; + робота / час / гроші
  above   one blog: особисте + професійне = особистий бренд; «дві окремі
          системи» struck out
  above   CTA — блогерка / СММниця / підприємиця, a team, a full battery,
          «Став + в коментарі»

usage: python build.py      (mattes: sh work/b1021/mattes.sh 46)
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
from gstyle import G, Words, load_caps, mark, esc  # noqa: E402

NN = "46"
CUT = json.load(io.open(os.path.join(ROOT, "work", "r" + NN, "cut.json"), encoding="utf-8"))
DUR = 66.050           # (1982 plate frames - 0.5) / 30
g = G(dur=DUR, reel=NN)

# whisper's spelling of what she plainly said -> her word (checked on the plate)
FIX = {
    u"Вони": u"І вони,", u"можуть перекликатися,": u"можуть перекликатися.", u"і в": u"І в",
    u"постати.": u"постити.", u"особистеблух": u"особистий блог —",
    (u"трошки", 48.0): u"трошечки", (u"більше", 48.7): u"більше.", u"мікс": u"мікс,",
    u"есемемниця,": u"СММниця,", (u"плюс", 64.9): u"+", u"коментарі": u"коментарі.",
    u"команду": u"команду,", u"підприємниця,": u"підприємиця,", u"втомлюється": u"втомлюється,",
    u"tone": u"tone of voice,", u"of": None, u"voice,": None,
}
CAPS = load_caps(NN, FIX)
W = Words(CAPS)
S, E = W.s, W.e

# ---------------------------------------------------------------- the beats
B, P, F, C, J = [], [], [], [], []     # behind / panel / front / cover html, js
BLACKOUT = []
PLACE = []                             # caption placement over the half screens
HALF = []

EXTRA_CSS = u"""
    .ava { width: 78px; height: 78px; border-radius: 50%; flex: none; display: flex;
           align-items: center; justify-content: center; color: var(--primary);
           background: var(--container-low); border: 3px solid var(--primary); }
    .plus { width: 40px; height: 40px; border-radius: 50%; flex: none; display: inline-flex;
            align-items: center; justify-content: center; background: var(--primary);
            color: #fff; font-weight: 700; font-size: 34px; line-height: 1; }
    .ctr { position: absolute; left: 0; width: 1080px; display: flex; justify-content: center;
           gap: 14px; }
    .ctr .pill { position: relative; }
    .post { position: absolute; width: 190px; height: 220px; padding: 18px; border-radius: 28px; }
    .post .img { display: block; height: 110px; margin-top: 12px; border-radius: 16px;
                 background: var(--container-low); }
    .tick { font-size: 38px; font-weight: 500; }
"""


def js(s):
    J.append(s)


def acct(i, x, top, title, chip, shown=False):
    """An Instagram account card: avatar, handle/bio lines, the account's name, a chip."""
    h = u"" if shown else u" hid"
    return u'''
        <div id="%s" class="card hid" style="left:%dpx; top:%dpx; width:410px; padding:28px 30px;">
          <div class="row" style="gap:18px">
            <span class="ava">%s</span>
            <div style="flex:1"><span class="line" style="width:86%%"></span>
              <span class="line" style="width:58%%; margin-top:12px"></span></div>
          </div>
          <span class="ttl%s" id="%st" style="font-size:52px; margin-top:22px">%s</span>
          <div class="chips" style="margin-top:16px"><span class="chip%s" id="%sc"><i></i>%s</span></div>
        </div>''' % (i, x, top, mark("instagram", 40), h, i, esc(title), h, i, esc(chip))


def people(name, xs, cy, head="", body=""):
    """Stick-figure people for a sketch: a head and a shoulder arc each."""
    return u" ".join(
        u'ell("%s", %d, %d, 58, 58, {seed: %d%s}); '
        u'_add(SK["%s"], SK["%s"].rc.curve([[%d, %d], [%d, %d], [%d, %d]], opt({%s}, %d)));'
        % (name, x, cy, 100 + i * 7, head, name, name, x - 46, cy + 112, x, cy + 44, x + 46, cy + 112,
           body, 103 + i * 7)
        for i, x in enumerate(xs))


F.append(u'<svg class="sk" id="skF" width="1080" height="1920" viewBox="0 0 1080 1920"></svg>')
P.append(u'<svg class="sk" id="skP" width="1080" height="1240" viewBox="0 0 1080 1240"></svg>')

# 1 · ABOVE — two accounts: особистий / професійний, свій / школа ---------------
t_dva, t_os, t_pro = S(u"два", 1.16), S(u"особистий", 2.11), S(u"професійний,", 2.65)
t_sv, t_shk = S(u"свій", 3.77), S(u"школи.", 4.55)
F.append(acct("a1", 110, 310, u"особистий", u"свій") + acct("a2", 560, 310, u"професійний", u"школа"))
js(u'''
  rise("#a1", %.3f); rise("#a2", %.3f);
  fadein("#a1t", %.3f, .3); pop("#a1t", %.3f, .5);
  fadein("#a2t", %.3f, .3); pop("#a2t", %.3f, .5);
  pop("#a1c", %.3f); pop("#a2c", %.3f);
''' % (t_dva - 0.3, t_dva - 0.1, t_os, t_os, t_pro, t_pro, t_sv, t_shk))
g.sfx("pop", t_dva - 0.25); g.sfx("click-soft", t_os)
BLACKOUT.append((t_os - 0.05, t_pro + 0.05))           # the titles say it

# 2 · ABOVE — one «AI-система» under both; 3 · circled, then split «?» ---------
t_nal, t_ai = S(u"налаштувати", 5.76), S(u"AI-систему", 6.69)
t_odna, t_chy, t_dvi = S(u"одна", 8.69), S(u"чи", 9.99), S(u"дві", 10.21)
h0, h1 = S(u"Так", 11.19) - 0.2, S(u"І в", 20.69) - 0.25
t_dv2 = S(u"дві", 12.07)
F.append(u'''
        <div class="ctr" style="top:572px"><div id="sys" class="pill hid"
             style="padding:22px 46px; font-size:44px">AI-система</div></div>''')
js(u'''
  gsap.set("#a1, #a2", {transformOrigin: "50%% 0%%"});
  tl.to("#a1, #a2", {scale: .72, y: -14, duration: .6, ease: RISE}, %.3f);
  sketch("in2", "skF"); arrow("in2", 330, 532, 440, 596, {seed: 5, bend: -.1}); arrow("in2", 750, 532, 640, 596, {seed: 9, bend: .1});
  draw("in2", %.3f, .45);
  pop("#sys", %.3f);
  sketch("c3", "skF"); ell("c3", 540, 622, 440, 160, {stroke: "#7A1424", strokeWidth: 5, seed: 15});
  draw("c3", %.3f, .6);
  sketch("q3", "skF"); ln("q3", 545, 548, 535, 700, {stroke: "#7A1424", strokeWidth: 7, seed: 21});
  label("q3", 790, 600, "?", {size: 72, color: "#7A1424"});
  draw("q3", %.3f, .4);
  sink("#a1, #a2", %.3f);
  out("#sys", %.3f); erase("in2", %.3f); erase("c3", %.3f); erase("q3", %.3f);
''' % (t_nal - 0.1, t_ai - 0.55, t_ai, t_odna - 0.15, t_chy, h0 - 0.1, t_dv2 - 0.3, h0 - 0.1,
       t_dv2 - 0.3, t_dv2 - 0.3))
g.sfx("pop", t_ai); g.sfx("click-soft", t_dvi)

# 4 · HALF — two columns: headers, the wall, the three parts each, ⇄ ----------
HALF.append((h0, h1))
t_ok2, t_sys2 = S(u"окремі", 12.45), S(u"системи.", 12.87)
t_kozh = S(u"кожен", 13.82)
t_skil, t_tov, t_diz = S(u"скіл", 15.5), S(u"tone of voice,", 16.91), S(u"дизайн-систему.", 17.93)
t_voni = S(u"І вони,", 19.19)
ROWS = [("r1", 490, u"скіл сценариста", t_skil - 0.45), ("r2", 600, u"tone of voice", t_tov - 0.3),
        ("r3", 710, u"дизайн-система", t_diz - 0.3)]
rows_js = u"".join(u'''
  sketch("%sL", "skP"); box("%sL", 110, %d, 360, 90, {seed: %d}); label("%sL", 290, %d, "%s", {size: 42}); draw("%sL", %.3f, .5);
  sketch("%sR", "skP"); box("%sR", 610, %d, 360, 90, {seed: %d}); label("%sR", 790, %d, "%s", {size: 42}); draw("%sR", %.3f, .5);'''
                   % (n, n, y, 30 + i * 4, n, y + 58, t, n, a, n, n, y, 32 + i * 4, n, y + 58, t, n, a + 0.3)
                   for i, (n, y, t, a) in enumerate(ROWS))
names1 = ["hL", "hR", "wall", "dn"] + [n + s for n, _, _, _ in ROWS for s in "LR"] + ["ech"]
js(u'''
  sketch("hL", "skP"); box("hL", 110, 300, 360, 100, {seed: 23, fill: true}); label("hL", 290, 366, "особистий", {size: 50});
  draw("hL", %.3f, .55);
  sketch("hR", "skP"); box("hR", 610, 300, 360, 100, {seed: 25, fill: true}); label("hR", 790, 366, "школа", {size: 50});
  draw("hR", %.3f, .55);
  sketch("wall", "skP"); ln("wall", 540, 292, 538, 812, {stroke: "#7A1424", strokeWidth: 6, seed: 27});
  draw("wall", %.3f, .55);
  sketch("dn", "skP"); arrow("dn", 290, 410, 290, 478, {seed: 28, bend: 0}); arrow("dn", 790, 410, 790, 478, {seed: 29, bend: 0});
  draw("dn", %.3f, .35);
%s
  sketch("ech", "skP"); arrow("ech", 430, 652, 650, 652, {stroke: "#7A1424", strokeWidth: 5, seed: 41, bend: .28});
  arrow("ech", 650, 690, 430, 690, {stroke: "#7A1424", strokeWidth: 5, seed: 43, bend: .28});
  draw("ech", %.3f, .45);
  %s
''' % (t_dv2 - 0.1, t_ok2 - 0.1, t_sys2 - 0.25, t_kozh - 0.15, rows_js, t_voni - 0.05,
       " ".join('erase("%s", %.3f);' % (n, h1) for n in names1)))
g.sfx("whoosh-short", h0); g.sfx("click-soft", t_dv2); g.sfx("click-soft", t_skil - 0.45)
g.sfx("click-soft", t_diz - 0.3); g.sfx("click-soft", t_voni)
g.sfx("whoosh-short", h1)

# 5 · ABOVE — what goes where: two posts dealt to the two accounts --------------
t_kin, t_vyr = S(u"кінці", 20.87), S(u"вирішуємо,", 22.09)
t_kudy, t_post = S(u"куди", 23.04), S(u"постити.", 23.48)
t_ale = S(u"Але", 24.32)


def post(i, x, rot):
    return (u'<div id="%s" class="card post hid" style="left:%dpx; top:322px; transform: rotate(%ddeg)">'
            u'<div class="row" style="gap:10px; color:#7A1424">%s<span class="line" style="flex:1"></span></div>'
            u'<span class="img"></span><span class="line" style="margin-top:14px; width:70%%"></span></div>'
            % (i, x, rot, mark("instagram", 30)))


F.append(u'''
        <div id="pcL" class="hid" style="position:absolute; left:120px; top:568px"><span class="chip" id="pcLc"><i></i>особистий</span></div>
        <div id="pcR" class="hid" style="position:absolute; left:790px; top:568px"><span class="chip" id="pcRc"><i></i>школа</span></div>
        %s
        %s''' % (post("ps1", 425, -6), post("ps2", 465, 5)))
js(u'''
  pop("#pcL", %.3f); pop("#pcR", %.3f);
  pop("#ps1", %.3f); pop("#ps2", %.3f);
  tl.to("#ps1", {x: -300, rotation: -3, duration: .55, ease: RISE}, %.3f);
  tl.to("#ps2", {x: 325, rotation: 3, duration: .55, ease: RISE}, %.3f);
  tl.set("#pcLc, #pcRc", {className: "chip on"}, %.3f);
  pop("#pcL, #pcR", %.3f, .45);
  sink("#pcL, #pcR, #ps1, #ps2", %.3f);
''' % (t_kin + 0.45, t_kin + 0.6, t_vyr - 0.15, t_vyr + 0.05, t_kudy - 0.1, t_kudy + 0.05,
       t_post, t_post, t_ale - 0.15))
g.sfx("pop", t_vyr - 0.15); g.sfx("whoosh-short", t_kudy - 0.1)

# 6 · BEHIND — «дві / окремі» -----------------------------------------------------
t_ce, t_dv3, t_ok3, t_sy3 = S(u"це", 25.83), S(u"дві", 26.2), S(u"окремі", 26.76), S(u"системи.", 27.26)
t_te = S(u"Те", 28.05)
m0, m1 = t_dv3 - 0.45, t_te + 0.05
B.append(u'''
        <div id="bw1" class="big hid" style="top:300px; font-size:240px">дві</div>
        <div id="bw2" class="big hid" style="top:516px; font-size:240px">окремі</div>''')
g.matte("big", round(m0, 3), round(m1 - m0, 3))
js(u'''
  rise("#bw1", %.3f); rise("#bw2", %.3f);
  sink("#bw1, #bw2", %.3f);
''' % (t_dv3 - 0.25, t_ok3 - 0.3, t_te - 0.4))
g.sfx("whoosh-short", t_dv3 - 0.25)
BLACKOUT.append((t_ce - 0.05, t_ce + 0.05))            # the big words say it

# 7 · HALF — the routine: one analysis struck out; different people; the wall ---
h2, h3 = S(u"Те", 28.05) - 0.1, S(u"Тому", 38.57) - 0.25
HALF.append((h2, h3))
t_rut, t_zap, t_odyn = S(u"рутиною.", 28.57), S(u"запхати", 29.95), S(u"один", 30.93)
t_ale2, t_kon1, t_kon2 = S(u"але", 31.53), S(u"конкуренти", 31.73), S(u"конкуренти", 33.13)
t_rizni, t_ne = S(u"різні", 35.11), S(u"не", 37.46)
names2 = ["lp", "an1", "an2", "anx", "cR", "cL", "ne", "wall2"]
js(u'''
  sketch("lp", "skP"); ell("lp", 540, 378, 420, 150, {seed: 51});
  arrow("lp", 668, 310, 722, 340, {seed: 53, bend: 0});
  label("lp", 540, 396, "рутина", {size: 52});
  draw("lp", %.3f, .7);
  sketch("an1", "skP"); label("an1", 225, 540, "особистий", {size: 44}); label("an1", 855, 540, "школа", {size: 44});
  arrow("an1", 230, 562, 335, 632, {seed: 55, bend: -.12}); arrow("an1", 850, 562, 745, 632, {seed: 57, bend: .12});
  draw("an1", %.3f, .45);
  sketch("an2", "skP"); box("an2", 340, 600, 400, 104, {seed: 59, fill: true}); label("an2", 540, 668, "один аналіз", {size: 48});
  draw("an2", %.3f, .5);
  sketch("anx", "skP"); ln("anx", 320, 720, 760, 585, {stroke: "#7A1424", strokeWidth: 7, seed: 61});
  draw("anx", %.3f, .35);
  erase("an1", %.3f); erase("an2", %.3f); erase("anx", %.3f);
  sketch("cR", "skP"); box("cR", 600, 470, 370, 330, {seed: 63}); label("cR", 785, 532, "школа", {size: 48});
  %s
  draw("cR", %.3f, .4);
  sketch("cL", "skP"); box("cL", 110, 470, 370, 330, {seed: 65}); label("cL", 295, 532, "особистий блог", {size: 44});
  %s
  draw("cL", %.3f, .4);
  sketch("ne", "skP"); ln("ne", 512, 622, 570, 620, {stroke: "#7A1424", strokeWidth: 7, seed: 71});
  ln("ne", 512, 656, 570, 654, {stroke: "#7A1424", strokeWidth: 7, seed: 73});
  ln("ne", 562, 592, 522, 688, {stroke: "#7A1424", strokeWidth: 7, seed: 75});
  draw("ne", %.3f, .3);
  erase("ne", %.3f);
  sketch("wall2", "skP"); ln("wall2", 540, 452, 538, 815, {stroke: "#7A1424", strokeWidth: 7, seed: 77});
  draw("wall2", %.3f, .5);
  %s
''' % (t_rut - 0.3, t_zap - 0.2, t_odyn - 0.3, t_ale2 - 0.05, t_kon1 + 0.3, t_kon1 + 0.3, t_kon1 + 0.3,
       people("cR", (690, 785, 880), 610), t_kon1 + 0.45,
       people("cL", (200, 295, 390), 610, u', stroke: "#7A1424", fill: "#F2C7CA", fillStyle: "hachure", '
              u'hachureGap: 12, hachureAngle: -41, fillWeight: 2.5', u'stroke: "#7A1424"'), t_kon2 - 0.05,
       t_rizni - 0.2, t_ne - 0.45, t_ne - 0.3, " ".join('erase("%s", %.3f);' % (n, h3) for n in names2)))
g.sfx("whoosh-short", h2); g.sfx("click-soft", t_odyn - 0.3)
g.sfx("click-soft", t_ale2); g.sfx("pop", t_kon1 + 0.45); 
g.sfx("click-soft", t_ne - 0.3); g.sfx("whoosh-short", h3)

# 8 · ABOVE — several accounts: the cards again, then the setup doubles --------
t_dek, t_riz = S(u"декілька", 39.53), S(u"різних", 40.91)
t_u, t_rob = S(u"у", 41.77), S(u"роботі", 41.91)
t_plus, t_chas, t_kosh = S(u"плюс", 43.9), S(u"часу", 46.26), S(u"коштує", 47.56)
t_ale3 = S(u"Але", 49.37)
F.append(acct("a3", 110, 310, u"особистий", u"свій", shown=True) +
         acct("a4", 560, 310, u"професійний", u"школа", shown=True))


def checklist(i, x, top, who):
    rows = [u"скіл сценариста", u"tone of voice", u"дизайн-система"]
    return (u'<div id="%s" class="card hid" style="left:%dpx; top:%dpx; width:500px; padding:30px 36px;">'
            u'<div class="row" style="gap:12px; color:#7A1424; margin-bottom:18px">%s'
            u'<span class="lbl" style="margin:0">налаштування · %s</span></div>%s</div>'
            % (i, x, top, mark("instagram", 30), esc(who),
               u"".join(u'<div class="row" style="margin-top:%dpx"><span class="check"></span>'
                        u'<span class="tick">%s</span></div>' % (0 if n == 0 else 16, esc(r))
                        for n, r in enumerate(rows))))


F.append(checklist("ck2", 140, 342, u"школа") + checklist("ck1", 100, 300, u"особистий"))
F.append(u''.join(u'<div id="pl%d" class="hid" style="position:absolute; left:668px; top:%dpx">'
                  u'<span class="chip" style="font-size:40px; padding:14px 26px 14px 16px"><b class="plus">+</b>%s</span></div>'
                  % (n, y, w) for n, (y, w) in enumerate(((322, u"робота"), (430, u"час"), (538, u"гроші")))))
js(u'''
  rise("#a3", %.3f); rise("#a4", %.3f);
  tl.to("#a3", {rotation: -4, x: -14, duration: .5, ease: POP}, %.3f);
  tl.to("#a4", {rotation: 4, x: 14, duration: .5, ease: POP}, %.3f);
  sink("#a3, #a4", %.3f);
  rise("#ck1", %.3f);
  tl.fromTo("#ck2", {autoAlpha: 0, x: -40, y: -42}, X({autoAlpha: 1, x: 0, y: 0, duration: .55, ease: POP}), %.3f);
  pop("#pl0", %.3f); pop("#pl1", %.3f); pop("#pl2", %.3f);
  sink("#ck1, #ck2, #pl0, #pl1, #pl2", %.3f);
''' % (t_dek - 0.1, t_dek + 0.1, t_riz, t_riz, t_u - 0.25, t_rob - 0.05, t_plus, t_plus + 0.1, t_chas, t_kosh,
       t_ale3 - 0.2))
g.sfx("pop", t_dek - 0.1); g.sfx("pop", t_rob - 0.05); g.sfx("pop", t_plus)
g.sfx("click-soft", t_chas); g.sfx("kaching", t_kosh)
BLACKOUT.append((t_plus - 0.05, t_plus + 0.05))         # «+ робота» says it

# 9 · ABOVE — the exception: one blog, особисте + професійне = особистий бренд --
t_blog, t_osb, t_prf = S(u"Блогери,", 50.97), S(u"особисте", 52.54), S(u"професійне", 53.24)
t_odn, t_brand, t_miks = S(u"одному", 53.86), S(u"особистий", 54.92), S(u"мікс,", 56.38)
t_dovas, t_ne2, t_tomu = S(u"до вас", 57.18), S(u"не", 57.56), S(u"Тому", 58.64)
F.append(u'''
        <div id="bl" class="card hid" style="left:120px; top:300px; width:840px; padding:34px 40px;">
          <div class="row" style="gap:20px">
            <span class="ava">%s</span>
            <div style="flex:1"><span class="line" style="width:52%%"></span>
              <span class="line" style="width:34%%; margin-top:12px"></span></div>
          </div>
          <div class="chips" style="margin-top:24px; justify-content:center; align-items:center">
            <span class="chip hid" id="bl1"><i></i>особисте</span>
            <b class="plus hid" id="blp">+</b>
            <span class="chip hid" id="bl2"><i></i>професійне</span>
          </div>
          <span class="ttl hid" id="blt" style="font-size:56px; margin-top:22px; text-align:center">особистий бренд</span>
        </div>
        <div class="ctr" style="top:430px"><div id="no2" class="pill light hid"
             style="font-size:46px; padding:26px 50px">дві окремі системи</div></div>''' % mark("instagram", 40))
js(u'''
  rise("#bl", %.3f);
  pop("#bl1", %.3f); pop("#bl2", %.3f); pop("#blp", %.3f, .45);
  rise("#blt", %.3f, 30);
  sketch("mx", "skF"); ell("mx", 540, 470, 700, 124, {stroke: "#7A1424", strokeWidth: 5, seed: 81});
  draw("mx", %.3f, .6);
  sink("#bl", %.3f); erase("mx", %.3f);
  pop("#no2", %.3f);
  sketch("nx", "skF"); ln("nx", 236, 500, 846, 470, {stroke: "#7A1424", strokeWidth: 8, seed: 83});
  draw("nx", %.3f, .35);
  out("#no2", %.3f); erase("nx", %.3f);
''' % (t_blog - 0.1, t_osb, t_prf, t_odn, t_brand - 0.05, t_miks - 0.25, t_dovas - 0.2, t_dovas - 0.2,
       t_dovas, t_ne2 - 0.1, t_tomu - 0.15, t_tomu - 0.15))
g.sfx("pop", t_blog - 0.1); g.sfx("click-soft", t_odn)
g.sfx("pop", t_dovas); g.sfx("click-soft", t_ne2 - 0.1)

# 10 · ABOVE — CTA: who it is for, a team that never tires, the pill ----------
t_bl, t_smm, t_pid = S(u"блогерка,", 59.22), S(u"СММниця,", 60.14), S(u"підприємиця,", 61.02)
t_kom, t_nik, t_stav = S(u"команду,", 62.7), S(u"ніколи", 63.22), S(u"то став", 64.72)
F.append(u'''
        <div class="ctr" style="top:312px">
          <span class="chip hid" id="ct1"><i></i>блогерка</span>
          <span class="chip hid" id="ct2"><i></i>СММниця</span>
          <span class="chip hid" id="ct3"><i></i>підприємиця</span>
        </div>
        <div class="ctr" style="top:450px"><div id="ctaP" class="pill hid">Став + в коментарі</div></div>''')
js(u'''
  pop("#ct1", %.3f); pop("#ct2", %.3f); pop("#ct3", %.3f);
  sketch("tm", "skF"); %s
  draw("tm", %.3f, .4);
  sketch("bt", "skF"); box("bt", 650, 470, 200, 104, {seed: 91, r: 20, fill: "#F2C7CA"});
  box("bt", 850, 500, 22, 44, {seed: 93, r: 8});
  draw("bt", %.3f, .45);
  erase("tm", %.3f); erase("bt", %.3f);
  pop("#ctaP", %.3f, .6);
  sketch("pt", "skF"); arrow("pt", 930, 700, 852, 582, {stroke: "#7A1424", strokeWidth: 5, seed: 97, bend: .15});
  draw("pt", %.3f, .45);
''' % (t_bl, t_smm, t_pid, people("tm", (330, 440, 550), 452), t_kom - 0.4, t_nik - 0.1,
       t_stav - 0.2, t_stav - 0.2, t_stav, t_stav + 0.4))
g.sfx("pop", t_bl)
g.sfx("click-soft", t_kom - 0.4); g.sfx("pop", t_stav)
BLACKOUT.append((t_stav - 0.05, DUR))                   # the pill says it

# ---------------------------------------------------------------- mattes for the half screens
for i, (a, b) in enumerate(HALF):
    g.matte("half%d" % (i + 1), round(a - 0.1, 3), round(b - a + 1.2, 3))
    js("  half(%.3f, %.3f);" % (a, b))
    PLACE.append((a + 0.4, b + 0.2, "bottom", 1010))

# ---------------------------------------------------------------- captions
# phrase breaks by meaning (word start times): add a break / drop the kit's one
ADD = [6.31, 15.06, 16.63, 25.83, 30.71, 31.53, 33.03, 39.53, 41.77, 43.05, 43.90, 46.66,
       53.70, 54.50, 55.64]
DROP = [7.23, 15.50, 26.76, 30.93, 32.75, 40.91, 42.47, 44.54, 46.80, 50.50, 54.12, 55.92]
KEYS = {1.16: True, 8.69: True, 10.21: True, 12.45: True, 19.87: True, 33.75: True, 40.91: True,
        u"школи": True, u"налаштувати": True, u"AI-систему": True, u"кожен": True, u"сценариста": True,
        u"tone of voice": True, u"дизайн-систему": True, u"вирішуємо": True, u"куди": True,
        u"основі": True, u"рутиною": True, u"запхати": True, u"один": True, u"різні": True,
        u"нормально": True, u"перетинаються": True, u"AI-системою": True, u"часу": True,
        u"коштує": True, u"всіх": True, u"Блогери": True, u"одному": True, u"бренд": True,
        u"мікс": True, u"команду": True, "off": [38.57, 43.05]}


def rechunk(chunks):
    words = [w for c in chunks for w in c["words"]]
    starts = [c["s"] for c in chunks if not any(abs(c["s"] - t) < 0.03 for t in DROP)] + ADD
    groups = []
    for w in words:
        if not groups or any(abs(w["s"] - t) < 0.03 for t in starts):
            groups.append([w])
        else:
            groups[-1].append(w)
    res = []
    for n, ch in enumerate(groups):
        s = ch[0]["s"]
        nxt = groups[n + 1][0]["s"] if n + 1 < len(groups) else DUR
        pos = ("bottom", 1920 - 1520)
        for a, b, how, y in PLACE:
            if a <= s < b:
                pos = (how, y if how == "top" else 1920 - y)
        res.append({"s": round(s, 3), "e": round(min(nxt, ch[-1]["e"] + 0.6), 3), "words": ch,
                    "key": g._key(ch, KEYS), "pos": pos})
    return res


def main():
    chunks = rechunk(g.chunks(CAPS, place=PLACE))
    if "-v" in sys.argv:
        print(" ".join("%s/%.1f" % (c["w"], c["s"]) for c in CAPS))
        for c in chunks:
            k = c["key"]
            print("%6.2f-%6.2f %-6s %s   [%s]" % (c["s"], c["e"], c["pos"][1], " ".join(w["w"] for w in c["words"]),
                                                 c["words"][k]["w"] if k is not None else "-"))
    doc = g.document(title=u"Reel 46 — Два акаунти, одна система", plate="assets/base.mp4",
                     behind="\n".join(B), panel="\n".join(P), front="\n".join(F), cover="\n".join(C),
                     js="\n".join(J), chunks=chunks, blackout=BLACKOUT, extra_css=EXTRA_CSS)
    g.write(HERE, doc)
    print("index.html  %d caption chunks, %d sfx cues, %d mattes" % (len(chunks), len(g.cues), len(g.mattes)))


main()
