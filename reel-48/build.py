# -*- coding: utf-8 -*-
"""Reel 48 — «Уроки і YouTube». Posts 2026-10-23.

Google style + Excalidraw (STYLE.md §00, with her review of reel 41 on top:
old word captions, calm sketches the kit inks over the footage — no explicit
colours there — white behind-words),
the reel-41 skeleton.

The one object is **the video itself** — a short reel frame next to a long
16:9 frame with its timeline. Claude edits both the same way; the long one
goes in instead of the short one, comes out edited and cut into reels; then
the same long video is taken apart for edits: what a render is (Claude →
code → video), re-rendering the whole timeline, or cutting out just the piece
with the edit, rendering it and splicing it back.

  above   reels / уроки для курсу / довгі відео (YouTube) — one Claude badge on each
  above   the lead magnet card (+ other long videos) = a reel
  above   the reel goes into Claude crossed out; one big video goes in instead;
          it comes out edited ✓ and cut into four reels
  above   the three formats come back and shuffle — «граєшся як завгодно»
  above   «2»: an edit on the long video
  above   render bars: reel fast, long video slow
  full    what a render is: Клод → код {JSON} → готове відео; the second arrow is «рендер»
  above   the render bars again — long is just longer
  above   «1» «2» options; 1: no rush → the whole timeline re-renders (underlined)
  above   bars: рілс < 2-й раз < 1-й раз
  half    «2»: промт; Claude cuts out the piece with the edit, renders only it,
          splices it back; a clock; not the whole render (struck)
  above   the lead magnet card again: 20 хв, новий стиль, усі правки
  behind  «2–3 години»
  above   my active work struck; render runs, I tick off other things
  above   CTA — час на монтаж, система, «Пиши + в коментарі», a pointer DOWN to the comments

usage: python build.py      (then mattes; render is the orchestrator's)
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
from gstyle import G, Words, load_caps, mark, esc  # noqa: E402

NN = "48"
CUT = json.load(io.open(os.path.join(ROOT, "work", "r" + NN, "cut.json"), encoding="utf-8"))
DUR = 80.583           # (2418 plate frames - 0.5) / 30
g = G(dur=DUR, reel=NN)

# whisper's spelling of what she plainly said -> her word (re-heard on the plate)
FIX = {
    u"що довгі": u"чи довгі", u"найтип": u"на ютуб", (u"саме,", 22.7): u"сама,", u"нових": u"довгих", u"Клодом": u"Клодом.", u"що я": u"що й",
    u"велике.": u"велике,", (u"Можна", 16.5): u"можна",
    (u"На", 40.0): u"на", (u"Тому", 42.3): u"Тому,", u"Коли": u"коли", u"Перший": u"Перший:",
    (u"довше", 49.7): u"довше,", u"заріз,": u"за рілс,", u"довчно": u"точно", u"швидше": u"швидше.",
    u"варіант": u"варіант:", u"Теж": u"теж", u"поповній.": u"по повній.",
    u"2": u"2–3", u"3": None, u"робота": u"робота —", u"Якщо": u"якщо",
}
CAPS = load_caps(NN, FIX)
W = Words(CAPS)
S, E = W.s, W.e

# ---------------------------------------------------------------- the beats
B, P, F, C, J = [], [], [], [], []     # behind / panel / front / cover html, js
BLACKOUT = []
HALF = []


def js(s):
    J.append(s)


EXTRA_CSS = u"""
    .vf { position: relative; display: block; border-radius: 18px; background: #FFF0F0;
          overflow: hidden; flex: none; }
    .vf .pl { position: absolute; left: 50%; top: 44%; width: 0; height: 0; transform: translate(-38%, -50%);
              border-style: solid; border-color: transparent transparent transparent #7A1424; }
    .vf .yt { position: absolute; left: 50%; top: 44%; transform: translate(-50%, -50%); color: #7A1424; }
    .vf .tb { position: absolute; left: 9%; right: 9%; bottom: 12%; height: 8px; border-radius: 4px;
              background: #E9D2D2; }
    .vf .tb b { position: absolute; left: 0; top: 0; bottom: 0; width: 34%; border-radius: 4px;
                background: #7A1424; }
    .vf .dur { position: absolute; right: 12px; top: 12px; background: #241919; color: #fff;
               border-radius: 10px; padding: 4px 12px; font-weight: 500; font-size: 30px; }
    .vc { display: flex; flex-direction: column; align-items: center; gap: 12px; padding: 22px 26px; }
    .vc .t { font-weight: 500; font-size: 34px; color: #241919; white-space: nowrap; line-height: 1.1; }
    .badge { position: absolute; width: 66px; height: 66px; border-radius: 50%; background: #7A1424;
             color: #fff; display: flex; align-items: center; justify-content: center;
             box-shadow: 0 2px 8px rgba(122,20,36,.30); }
    .nb { width: 110px; height: 110px; border-radius: 50%; background: #FFF0F0; color: #7A1424;
          font-weight: 700; font-size: 66px; display: flex; align-items: center; justify-content: center;
          letter-spacing: -0.04em; flex: none; }
    .nb.on { background: #7A1424; color: #fff; }
    .bar { position: relative; height: 30px; border-radius: 15px; background: #F3E4E4; overflow: hidden; }
    .bar b { position: absolute; left: 0; top: 0; bottom: 0; width: 0; border-radius: 15px; background: #7A1424; }
    .bar.g b { background: #C9AFAF; }
    .seg { width: 80px; height: 84px; border-radius: 14px; background: #FFF0F0; border: 3px solid #DEBFBF;
           flex: none; position: relative; }
    .ink { position: absolute; overflow: visible; }
    .ink path { fill: none; stroke: #7A1424; stroke-width: 7; stroke-linecap: round; stroke-linejoin: round;
                stroke-dasharray: 1; stroke-dashoffset: 1; }
    .hd { font-family: "Pangolin", cursive; color: #7A1424; position: absolute; white-space: nowrap; }
"""


def vf(w, h, yt=False, extra=u"", vid=u"", style=u""):
    """a video frame: 16:9 or 9:16, play triangle (or the YouTube mark), timeline"""
    t = int(h * 0.17)
    if yt:
        centre = u'<span class="yt">%s</span>' % mark("youtube", int(h * 0.46))
    else:
        centre = u'<span class="pl" style="border-width:%dpx 0 %dpx %dpx"></span>' % (t, t, int(t * 1.6))
    return u'<span class="vf"%s style="width:%dpx;height:%dpx;%s">%s<span class="tb"><b></b></span>%s</span>' % (
        (u' id="%s"' % vid) if vid else u"", w, h, style, centre, extra)


def ink(iid, x, y, w, h, paths):
    """a hand stroke ON a card (red is fine there): drawn on with inkdraw()"""
    return (u'<svg class="ink hid" id="%s" width="%d" height="%d" viewBox="0 0 %d %d" style="left:%dpx; top:%dpx">%s</svg>'
            % (iid, w, h, w, h, x, y, u"".join(u'<path pathLength="1" d="%s"/>' % d for d in paths)))


# helpers on top of gstyle's
js(u'''
  function inkdraw(sel, t, d) {
    tl.set(sel, {autoAlpha: 1}, t);
    tl.fromTo(sel + " path", {strokeDashoffset: 1}, X({strokeDashoffset: 0, duration: d || .4, ease: "power1.inOut", stagger: .14}), t);
  }
  function fill(sel, t, d, w) { tl.fromTo(sel, {width: "0%"}, X({width: w || "100%", duration: d, ease: "none"}), t); }
  function tick(name, x, y, o) { _ink = SK[name].ink; var s = SK[name], k = (o && o.k) || 1;
    _add(s, s.rc.linearPath([[x - 34 * k, y], [x - 8 * k, y + 28 * k], [x + 40 * k, y - 34 * k]], opt(o, (o && o.seed) || 71))); }
  function play(name, cx, cy, h, o) { _ink = SK[name].ink; var s = SK[name];
    _add(s, s.rc.polygon([[cx - h * .4, cy - h * .5], [cx - h * .4, cy + h * .5], [cx + h * .55, cy]], opt(o, (o && o.seed) || 51))); }
  function clock(name, cx, cy, r, o) {
    ell(name, cx, cy, 2 * r, 2 * r, o);
    ln(name, cx, cy, cx, cy - r * .62, o); ln(name, cx, cy, cx + r * .48, cy + r * .2, o);
  }
''')

# 1 · ABOVE — reels, course lessons, long YouTube videos: the same Claude -----
t_ril, t_ur = S(u"рілси,", 1.43), S(u"уроки", 2.35)
t_dov, t_yt, t_kl = S(u"відео", 3.85) - 0.3, S(u"на ютуб", 4.13), S(u"Клодом.", 5.47)
t_ya = S(u"Я", 6.39)
BADGE = u'<span class="badge hid" id="%s" style="right:-20px; top:-20px">' + mark("claude", 38) + u'</span>'
F.append(u'''
        <div id="b1" style="position:absolute; left:0; top:306px; width:1080px; display:flex;
             justify-content:center; align-items:flex-end; gap:26px">
          <div class="card vc hid" id="b1a" style="position:relative">%s<span class="t">рілси</span>%s</div>
          <div class="card vc hid" id="b1b" style="position:relative">%s<span class="t">уроки для курсу</span>%s</div>
          <div class="card vc hid" id="b1c" style="position:relative">%s<span class="t">довгі відео</span>%s</div>
        </div>''' % (vf(96, 170), BADGE % "b1ka",
                     vf(270, 152, extra=u'<span class="dur" style="background:#7A1424">Урок 1</span>'), BADGE % "b1kb",
                     vf(270, 152, yt=True), BADGE % "b1kc"))
js(u'''
  pop("#b1a", %.3f); pop("#b1b", %.3f); pop("#b1c", %.3f);
  pop("#b1ka", %.3f, .45); pop("#b1kb", %.3f, .45); pop("#b1kc", %.3f, .45);
  sink("#b1a, #b1b, #b1c", %.3f);
''' % (t_ril - 0.1, t_ur - 0.05, t_dov, t_kl - 0.15, t_kl, t_kl + 0.15, t_ya - 0.3))
g.sfx("pop", t_ril - 0.1); g.sfx("pop", t_ur - 0.05); g.sfx("pop", t_dov); g.sfx("click-soft", t_kl)
BLACKOUT.append((t_ur - 0.05, E(u"на ютуб", 4.13)))          # the cards say it

# 2 · ABOVE — the lead magnet, other long videos = the principle of reels ------
t_zm, t_lm = S(u"так змонтувала", 6.55), S(u"лідмагніт,", 7.26)
t_in, t_dv = S(u"інші", 8.49), S(u"довгі", 8.87)
t_toy, t_zr, t_ril2 = S(u"той", 11.48), S(u"з", 12.34), S(u"рілсами.", 12.44)
t_pros = S(u"Просто", 13.2)
GHOST = u'''
        <div id="%s" class="card hid" style="left:%dpx; top:%dpx; width:470px; padding:30px 35px; transform:rotate(%ddeg)">
          <span class="lbl">&nbsp;</span>%s
        </div>'''
F.append(GHOST % ("b2g1", 92, 296, -6, vf(400, 225)) + GHOST % ("b2g2", 128, 292, 5, vf(400, 225)) + u'''
        <div id="b2" class="card hid" style="left:110px; top:300px; width:470px; padding:30px 35px;">
          <span class="lbl" id="b2l" style="font-size:34px; color:#241919; font-weight:700">Лідмагніт</span>%s
          <span class="check on hid" id="b2k" style="position:absolute; right:22px; top:22px"></span>
        </div>
        <div id="b2eq" class="nb hid" style="position:absolute; left:600px; top:416px; background:#fff; font-size:80px;
             box-shadow:0 1px 3px rgba(36,25,25,.10), 0 10px 30px rgba(36,25,25,.10)">=</div>
        <div id="b2r" class="card vc hid" style="left:730px; top:318px">%s<span class="t">рілс</span>
          %s
        </div>''' % (vf(400, 225, vid="b2v", extra=u'<span class="dur hid" id="b2d">20 хв</span>'), vf(120, 213),
                     ink("b2x", 4, 10, 176, 230, [u"M14 18 C60 80 110 150 162 214", u"M160 16 C112 84 64 152 16 212"])))
js(u'''
  rise("#b2", %.3f); fadein("#b2l", %.3f, .3); pop("#b2k", %.3f, .45);
  pop("#b2g1", %.3f, .5); pop("#b2g2", %.3f, .5);
  pop("#b2eq", %.3f); pop("#b2r", %.3f);
  sink("#b2, #b2g1, #b2g2", %.3f); out("#b2eq", %.3f);
''' % (t_zm - 0.2, t_lm, E(u"лідмагніт,", 7.26), t_in, t_dv, t_toy - 0.1, t_zr - 0.1, t_pros - 0.15, t_pros - 0.15))
js(u'  tl.set("#b2l", {autoAlpha: 0}, 0);')
g.sfx("pop", t_zm - 0.2); g.sfx("pop", t_in); g.sfx("pop", t_zr - 0.1)

# 3 · ABOVE — not the short one: one big video goes into Claude ---------------
t_zam, t_kor = S(u"замість", 13.55), S(u"короткого", 13.94)
t_odn, t_vel = S(u"одне", 15.54), S(u"велике,", 15.89)
F.append(u'''
        <div id="b3k" class="card hid" style="left:770px; top:378px; width:210px; padding:28px 20px;
             display:flex; flex-direction:column; align-items:center; gap:10px; color:#7A1424">%s
          <span style="font-weight:700; font-size:40px; color:#241919">Claude</span></div>
        <div id="b3L" class="card vc hid" style="left:90px; top:330px">%s<span class="t">одне велике</span>
          <span class="check on hid" id="b3ok" style="position:absolute; right:20px; top:20px"></span>
        </div>''' % (mark("claude", 76), vf(380, 214, vid="b3v")))
js(u'''
  tl.to("#b2r", {x: -640, duration: .7, ease: SLIDE}, %.3f);
  rise("#b3k", %.3f);
  inkdraw("#b2x", %.3f, .3);
  sink("#b2r", %.3f);
  rise("#b3L", %.3f);
  sketch("a3", "skF"); arrow("a3", 538, 452, 752, 452, {seed: 31, bend: .1});
  draw("a3", %.3f, .45);
''' % (t_pros - 0.1, t_pros + 0.15, t_kor, t_odn - 0.3, t_odn - 0.1, t_vel - 0.25))
g.sfx("whoosh-short", t_pros - 0.1); g.sfx("pop", t_odn - 0.1)

# 4 · ABOVE — it edits the big one ✓, then cuts it into small reels ----------
t_zmn, t_por = S(u"змонтує", 17.91), S(u"поріже", 19.87)
t_mal, t_tob = S(u"маленькі", 20.57), S(u"Тобто", 21.56)
REEL4 = u''.join(u'<div class="card hid" id="b4r%d" style="position:absolute; left:%dpx; top:330px; padding:14px; border-radius:30px">%s</div>'
                 % (i, 196 + i * 182, vf(120, 213)) for i in range(4))
F.append(REEL4)
js(u'''
  pop("#b3ok", %.3f, .45);
  sketch("c4", "skF");     // over the footage layer: the kit inks it dark with a white halo
  ln("c4", 214, 350, 214, 572, {strokeWidth: 6, seed: 41});
  ln("c4", 306, 350, 306, 572, {strokeWidth: 6, seed: 43});
  ln("c4", 398, 350, 398, 572, {strokeWidth: 6, seed: 45});
  draw("c4", %.3f, .3);
  out("#b3L, #b3k", %.3f); erase("c4", %.3f); erase("a3", %.3f);
  pop("#b4r0", %.3f, .5); pop("#b4r1", %.3f, .5); pop("#b4r2", %.3f, .5); pop("#b4r3", %.3f, .5);
  sink("#b4r0, #b4r1, #b4r2, #b4r3", %.3f);
''' % (t_zmn + 0.2, t_por - 0.35, t_mal - 0.35, t_mal - 0.35, t_mal - 0.35,
       t_mal - 0.05, t_mal + 0.07, t_mal + 0.19, t_mal + 0.31, t_tob + 0.15))
g.sfx("click-soft", t_por - 0.3); g.sfx("pop", t_mal - 0.05)

# 5 · ABOVE — the same scheme for all three: play with it as you like ---------
t_sh, t_gr, t_zav = S(u"схема", 21.78), S(u"граєшся", 23.2), S(u"завгодно.", 24.12)
t_dr = S(u"Друге,", 24.77)
js(u'''
  tl.set("#b1a, #b1b, #b1c", {y: 0}, %.3f);
  rise("#b1a", %.3f); rise("#b1b", %.3f); rise("#b1c", %.3f);
  tl.to("#b1a", {x: 696, duration: .6, ease: SLIDE}, %.3f);
  tl.to("#b1b", {x: 174, duration: .6, ease: SLIDE}, %.3f);
  tl.to("#b1c", {x: -522, duration: .6, ease: SLIDE}, %.3f);
  tl.to("#b1a", {y: -40, duration: .3, ease: "power1.out", yoyo: true, repeat: 1}, %.3f);
  tl.to("#b1c", {y: 40, duration: .3, ease: "power1.out", yoyo: true, repeat: 1}, %.3f);
  tl.to("#b1b", {rotation: -6, duration: .2, yoyo: true, repeat: 3, ease: "sine.inOut"}, %.3f);
  sink("#b1a, #b1b, #b1c", %.3f);
''' % (t_sh - 0.2, t_sh, t_sh + 0.08, t_sh + 0.16, t_gr, t_gr, t_gr, t_gr, t_gr, t_zav - 0.3, t_dr - 0.3))
g.sfx("pop", t_sh); g.sfx("whoosh-short", t_gr)

# 6 · ABOVE — second: how to edit such a long video --------------------------
t_pr = S(u"правки", 27.17)
t_tak = S(u"Так", 28.93)
F.append(u'''
        <div id="b6" class="card hid" style="left:120px; top:300px; width:840px; height:320px; padding:0">
          <div class="nb on" style="position:absolute; left:44px; top:105px">2</div>
          <div style="position:absolute; left:200px; top:42px">%s</div>
          %s
          <span class="hd hid" id="b6l" style="left:660px; top:44px; font-size:50px">правка</span>
        </div>''' % (vf(420, 236), ink("b6c", 380, 70, 190, 130, [u"M150 22 C186 46 182 106 112 118 C46 128 8 96 14 62 C20 26 70 6 120 10 C140 12 152 16 160 26"])))
js(u'''
  rise("#b6", %.3f);
  inkdraw("#b6c", %.3f, .45); fadein("#b6l", %.3f, .3);
  sink("#b6", %.3f);
''' % (t_dr - 0.1, t_pr - 0.25, t_pr + 0.05, t_tak - 0.3))
g.sfx("pop", t_dr - 0.1)


# 7 · ABOVE — render bars: a reel renders fast, a long video longer -----------
def bars_card(cid, rows, top=300, lbl=u""):
    out = [u'<div id="%s" class="card hid" style="left:120px; top:%dpx; width:840px; padding:32px 40px">' % (cid, top)]
    if lbl:
        out.append(u'<span class="lbl" id="%sl">%s</span>' % (cid, lbl))
    for i, (rid, icon, name, w, cls) in enumerate(rows):
        out.append(u'<div class="row" id="%s" style="margin-top:%dpx; gap:22px; height:84px">'
                   u'<div style="width:100px; display:flex; justify-content:center">%s</div>'
                   u'<span style="width:200px; font-size:36px; font-weight:500">%s</span>'
                   u'<div class="bar %s" style="width:%dpx"><b></b></div>'
                   u'<span class="check on hid" id="%sk"></span></div>'
                   % (rid, 0 if i == 0 else 14, icon, esc(name), cls, w, rid))
    out.append(u'</div>')
    return u"".join(out)


t_vril, t_tilk, t_rend = S(u"у рілсах,", 29.68), S(u"тільки", 30.32), S(u"рендериться.", 30.84)
F.append(bars_card("b7", [("b7a", vf(46, 82), u"рілс", 120, ""), ("b7b", vf(100, 56), u"довге відео", 350, "")],
                   lbl=u"Рендер"))
js(u'''
  rise("#b7", %.3f); tl.set("#b7l", {autoAlpha: 0}, 0); fadein("#b7l", %.3f, .3);
  rise("#b7a", %.3f, 30); fill("#b7a .bar b", %.3f, .45); pop("#b7ak", %.3f, .4);
  rise("#b7b", %.3f, 30); fill("#b7b .bar b", %.3f, 1.6, "62%%");
''' % (t_tak - 0.1, t_rend, t_tak - 0.1, t_vril, t_vril + 0.5, t_tilk - 0.1, t_tilk + 0.2))
js(u'  tl.set("#b7a, #b7b", {autoAlpha: 0}, 0);')
g.sfx("pop", t_tak - 0.1)

# 8 · FULL — what a render is: Claude -> code (JSON) -> the finished video -----
t_poy, t_rq = S(u"Пояснюю,", 31.66), S(u"рендер:", 32.45)
c0 = round(t_rq - 0.85, 3)           # the cover arrives ON «рендер:» with its headline
t_kld, t_bud = S(u"Клод", 33.31), S(u"будує", 33.49)
t_zv, t_kod, t_json = S(u"звичайний", 34.61), S(u"код,", 35.09), S(u"JSON,", 35.25)
t_per, t_got = S(u"перетворюється", 36.62), S(u"у готове", 37.24)
t_naz, t_r2 = S(u"називається", 38.68), S(u"рендер.", 39.22)
t_i = S(u"І", 39.83)
c1 = round(t_i - 0.08, 3)
C.append(u'''
        <svg class="sk" id="skC" width="1080" height="1920" viewBox="0 0 1080 1920"></svg>
        <div id="c8k" class="hid" style="position:absolute; left:396px; top:478px; color:#7A1424">%s</div>''' % mark("claude", 72))
js(u'''
  full(%.3f, %.3f); tl.set("#b7", {autoAlpha: 0}, %.3f);
  // the headline rides up on the cover (her review: never open onto empty white)
  sketch("h8", "skC"); label("h8", 540, 384, "що таке рендер?", {size: 76});
  draw("h8", %.3f);
  sketch("k8", "skC"); box("k8", 350, 448, 380, 140, {seed: 3}); label("k8", 610, 538, "Клод", {size: 60});
  draw("k8", %.3f, .55); fadein("#c8k", %.3f, .3);
  sketch("a8", "skC"); arrow("a8", 540, 604, 548, 778, {seed: 5, bend: .1});
  draw("a8", %.3f, .45);
  sketch("j8", "skC"); box("j8", 290, 792, 500, 200, {seed: 7});
  label("j8", 190, 905, "код", {size: 54, color: "#574142"});
  draw("j8", %.3f, .55);
  sketch("j8b", "skC"); label("j8b", 540, 880, "{ JSON }", {size: 62});
  ln("j8b", 380, 930, 640, 930, {seed: 9, strokeWidth: 4}); ln("j8b", 410, 962, 580, 962, {seed: 11, strokeWidth: 4});
  draw("j8b", %.3f, .3);
  sketch("a8b", "skC"); arrow("a8b", 540, 1008, 532, 1170, {seed: 13, bend: -.1});
  draw("a8b", %.3f, .45);
  sketch("v8", "skC"); box("v8", 370, 1184, 340, 192, {seed: 15, r: 24}); play("v8", 540, 1280, 76, {seed: 17, stroke: "#7A1424", strokeWidth: 5});
  label("v8", 345, 1270, "готове", {size: 50, anchor: "end"}); label("v8", 345, 1328, "відео", {size: 50, anchor: "end"});
  draw("v8", %.3f, .5);
  sketch("r8", "skC"); ell("r8", 536, 1090, 190, 230, {stroke: "#7A1424", strokeWidth: 5, seed: 19});
  label("r8", 655, 1105, "рендер", {size: 64, color: "#7A1424", anchor: "start"});
  draw("r8", %.3f, .6);
''' % (c0, c1, c0 + 0.9, c0 + 0.3, t_kld - 0.4, t_kld - 0.1, t_bud, t_zv - 0.3, t_json - 0.1, t_per - 0.35,
       t_got - 0.35, t_r2 - 0.75))
g.sfx("whoosh-short", c0); g.sfx("click-soft", t_kld - 0.4); g.sfx("click-soft", t_json - 0.1)
g.sfx("pop", t_r2 - 0.15)

# 8b · ABOVE — the bars again: on a long video it is just longer ---------------
t_dovg, t_dsh = S(u"довгому", 40.10), S(u"довше.", 41.65)
t_tomu = S(u"Тому,", 42.28)
js(u'''
  tl.set("#b7l", {autoAlpha: 1}, %.3f); tl.set("#b7a, #b7b", {autoAlpha: 1, y: 0}, %.3f);
  tl.set("#b7a .bar b", {width: "100%%"}, %.3f); tl.set("#b7ak", {autoAlpha: 1, scale: 1}, %.3f);
  tl.set("#b7b .bar b", {width: "0%%"}, %.3f);
  tl.set("#b7", {y: 0}, %.3f);
  rise("#b7", %.3f);
  fill("#b7b .bar b", %.3f, %.3f); pop("#b7bk", %.3f, .4);
  sink("#b7", %.3f);
''' % (c1, c1, c1, c1, c1, c1, c1 + 0.25, t_dovg, t_dsh - 0.1 - t_dovg, t_dsh - 0.1, t_tomu - 0.05))

# 9-10 · ABOVE — two options; the first: no rush, the whole timeline re-renders
t_vn, t_prk = S(u"вношу", 42.90), S(u"правку,", 43.26)
t_dva, t_var = S(u"два", 43.94), S(u"варіанти.", 44.10)
t_p1, t_nema = S(u"Перший:", 44.60), S(u"нема", 45.48)
t_pv, t_prr, t_zan = S(u"просто вношу", 46.60), S(u"перерендерить", 47.66), S(u"заново.", 48.82)
t_ce = S(u"Це", 49.53)
SEGS = u"".join(u'<span class="seg" id="b10s%d"></span>' % i for i in range(8))
F.append(u'''
        <div id="b10" class="card hid" style="left:120px; top:300px; width:840px; height:350px; padding:0">
          <div style="position:absolute; left:36px; top:34px">%s</div>
          %s
          <div class="nb hid" id="b10n1" style="position:absolute; left:340px; top:52px">1</div>
          <div class="nb hid" id="b10n2" style="position:absolute; left:476px; top:52px">2</div>
          <span class="chip hid" id="b10c" style="position:absolute; left:476px; top:72px; font-size:32px; padding:12px 20px"><i></i>нема куди спішити</span>
          <div id="b10t" class="hid" style="position:absolute; left:36px; top:226px; display:flex; gap:8px">%s</div>
          %s
          %s
        </div>''' % (vf(260, 146), ink("b10e", 150, 52, 130, 100, [u"M100 16 C126 36 120 82 72 88 C28 92 6 70 10 46 C14 20 52 6 84 10 C96 12 104 16 110 24"]),
                     SEGS, ink("b10p", 386, 236, 64, 64, [u"M8 40 C18 20 26 52 36 30 C44 14 50 40 58 24"]),
                     # «усе відео»: a hand underline under the whole timeline (no ↻ — no arrowhead on a loop)
                     ink("b10u", 28, 312, 716, 32, [u"M8 18 C160 26 380 8 706 16"])))
js(u'''
  rise("#b10", %.3f); inkdraw("#b10e", %.3f, .4);
  pop("#b10n1", %.3f, .5); pop("#b10n2", %.3f, .5);
  tl.set("#b10n1", {className: "nb on"}, %.3f); pop("#b10n1", %.3f, .45);
  out("#b10n2", %.3f); pop("#b10c", %.3f);
  rise("#b10t", %.3f, 30); tl.to("#b10s4", {borderColor: "#7A1424", duration: .2}, %.3f); inkdraw("#b10p", %.3f, .35);
  tl.to("#b10t .seg", {backgroundColor: "#7A1424", borderColor: "#7A1424", duration: .14, stagger: .15}, %.3f);
  inkdraw("#b10u", %.3f, .45);
  sink("#b10", %.3f);
''' % (t_vn - 0.3, t_prk, t_dva, t_var, t_p1, t_p1, t_nema - 0.4, t_nema, t_pv - 0.1, t_pv + 0.3, t_pv + 0.3,
       t_prr, S(u"усе", 48.3) - 0.1, t_ce - 0.3))
g.sfx("pop", t_vn - 0.3); g.sfx("pop", t_dva); g.sfx("pop", t_nema); g.sfx("typing", t_prr)

# 10b · ABOVE — longer than a reel, but the second time still faster ----------
t_dsh2, t_zril = S(u"довше,", 49.73), S(u"за рілс,", 50.33)
t_dru, t_shv = S(u"другий", 51.21), S(u"швидше.", 52.27)
t_dv2 = S(u"Другий", 52.90)
F.append(bars_card("b11", [("b11a", vf(46, 82), u"рілс", 100, "g"), ("b11b", vf(100, 56), u"2-й раз", 230, ""),
                           ("b11c", vf(100, 56), u"1-й раз", 350, "g")], top=294))
js(u'''
  tl.set("#b11a, #b11b, #b11c", {autoAlpha: 0}, 0);
  rise("#b11", %.3f);
  rise("#b11b", %.3f, 30); fill("#b11b .bar b", %.3f, .7);
  rise("#b11a", %.3f, 30); fill("#b11a .bar b", %.3f, .3);
  rise("#b11c", %.3f, 30); fill("#b11c .bar b", %.3f, .7);
  pop("#b11bk", %.3f, .45);
  sink("#b11", %.3f);
''' % (t_ce - 0.1, t_ce - 0.1, t_dsh2 - 0.1, t_zril - 0.2, t_zril, t_dru - 0.15, t_dru, t_shv, t_dv2 - 0.2))
g.sfx("pop", t_ce - 0.1); g.sfx("click-soft", t_shv)

# 11 · HALF — the special prompt: cut out the piece, render only it, splice ---
h0 = round(t_dv2 - 0.15, 3)
h1 = round(S(u"Для", 64.86) - 0.9, 3)
HALF.append((h0, h1))
t_v2, t_sp, t_pt = S(u"варіант:", 53.61), S(u"спеціальний", 54.33), S(u"промт,", 54.81)
t_vyr, t_dpr = S(u"вирізає", 55.69), S(u"де правка,", 57.21)
t_rnd, t_vkl, t_naz2 = S(u"рендерить", 57.80), S(u"вклеює", 59.02), S(u"назад", 59.54)
t_vid = S(u"відео.", 60.12)
t_zaim, t_alne, t_rn3 = S(u"займає", 61.15), S(u"але не", 62.39), S(u"рендер", 62.91)
P.append(u'''
        <svg class="sk" id="skP" width="1080" height="1240" viewBox="0 0 1080 1240"></svg>
        <div class="nb on hid" id="p2n" style="position:absolute; left:96px; top:316px">2</div>
        <div id="p2b" class="hid" style="position:absolute; left:792px; top:398px; width:188px">
          <span class="hd" style="position:relative; display:block; font-size:42px; color:#1E1E1E; margin-bottom:8px">рендер</span>
          <div class="bar" style="width:188px"><b></b></div></div>
        <div id="p2f" class="hid" style="position:absolute; left:100px; top:718px; width:880px">
          <div class="bar g" style="width:880px; height:34px"><b style="width:100%"></b></div>
          <span class="hd" style="position:relative; display:block; font-size:44px; color:#574142; margin-top:4px; text-align:center">весь рендер</span></div>''')
SEGX = [100 + i * 110 for i in range(8)]
js(u'''
  pop("#p2n", %.3f);
  sketch("st", "skP");
  %s
  draw("st", %.3f, .25);
  sketch("pc", "skP"); box("pc", 650, 562, 100, 104, {seed: 61, r: 14, fill: true}); draw("pc", %.3f, .3);
  sketch("pd", "skP"); box("pd", 230, 300, 140, 176, {seed: 63, r: 14});
  ln("pd", 258, 350, 342, 350, {seed: 65, strokeWidth: 4}); ln("pd", 258, 386, 342, 386, {seed: 67, strokeWidth: 4});
  ln("pd", 258, 422, 318, 422, {seed: 69, strokeWidth: 4});
  label("pd", 395, 410, "промт", {size: 54, anchor: "start"});
  draw("pd", %.3f, .4);
  sketch("cu", "skP"); ln("cu", 643, 528, 643, 702, {stroke: "#7A1424", strokeWidth: 6, seed: 71});
  ln("cu", 757, 528, 757, 702, {stroke: "#7A1424", strokeWidth: 6, seed: 73});
  draw("cu", %.3f, .3);
  sketch("pm", "skP"); _ink = "#7A1424";
  _add(SK.pm, SK.pm.rc.curve([[668, 640], [684, 588], [700, 630], [716, 586], [734, 626]], opt({stroke: "#7A1424", strokeWidth: 5}, 75)));
  label("pm", 700, 518, "правка", {size: 46, color: "#7A1424"});
  draw("pm", %.3f, .4);
  erase("cu", %.3f);
  tl.to("#sk-pc, #sk-pm", {y: -190, duration: .5, ease: SLIDE}, %.3f);
  fadein("#p2b", %.3f, .3); fill("#p2b .bar b", %.3f, .7);
  out("#p2b", %.3f);
  tl.to("#sk-pc, #sk-pm", {y: 0, duration: .5, ease: SLIDE}, %.3f);
  sketch("ok", "skP"); tick("ok", 812, 500, {stroke: "#7A1424", strokeWidth: 6, seed: 77, k: .8});
  draw("ok", %.3f, .35);
  sketch("cl", "skP"); clock("cl", 885, 420, 62, {seed: 79});
  draw("cl", %.3f, .45);
  fadein("#p2f", %.3f, .3);
  sketch("x2", "skP"); ln("x2", 90, 740, 990, 726, {stroke: "#7A1424", strokeWidth: 7, seed: 81});
  draw("x2", %.3f, .35);
''' % (t_v2 - 0.1,
       u" ".join(u'box("st", %d, 562, 100, 104, {seed: %d, r: 14});' % (x, 21 + i) for i, x in enumerate(SEGX) if i != 5),
       h0 + 0.85, h0 + 1.9, t_sp - 0.2, t_vyr - 0.1, t_dpr - 0.25, t_rnd - 0.3, t_rnd - 0.3,
       t_rnd, t_rnd + 0.15, t_vkl - 0.1, t_vkl, t_vid - 0.3, t_zaim - 0.1, t_alne - 0.15, t_rn3 - 0.2))
js(u'''
  ["st", "pc", "pd", "pm", "ok", "cl", "x2"].forEach(function (n) { erase(n, %.3f); });
  out("#p2n, #p2f", %.3f);
''' % (h1 + 0.9, h1 + 0.9))
g.sfx("whoosh-short", h0); g.sfx("click-soft", t_sp - 0.2); g.sfx("click-soft", t_vyr - 0.1)
g.sfx("whoosh-short", t_rnd - 0.3); g.sfx("pop", t_vkl + 0.3)
g.sfx("click-soft", t_rn3 - 0.2)

# 12 · ABOVE — the example: that 20-minute lead magnet, new style, all edits ---
t_dla, t_lm2 = S(u"Для", 64.86), S(u"той лідмагніт", 65.62)
t_20, t_nov, t_prv = S(u"на 20", 66.09), S(u"новому", 66.98), S(u"правками", 68.74)
t_zay, t_23 = S(u"зайняв", 69.18), S(u"2–3", 70.04)
F.append(u'''
        <div id="b12" class="hid" style="position:absolute; left:610px; top:372px; display:flex; flex-direction:column;
             align-items:flex-start; gap:18px">
          <span class="chip hid" id="b12a"><i></i>новий стиль</span>
          <span class="chip hid" id="b12b"><i></i>усі правки</span>
        </div>''')
js(u'''
  tl.set("#b2", {x: 0, y: 0}, %.3f); tl.set("#b2l", {autoAlpha: 1}, %.3f);
  rise("#b2", %.3f);
  pop("#b2d", %.3f, .5);
  fadein("#b12", %.3f, .01); pop("#b12a", %.3f); pop("#b12b", %.3f);
  sink("#b2, #b12", %.3f);
''' % (t_dla - 0.3, t_dla - 0.3, t_dla, t_20 + 0.15, t_nov - 0.1, t_nov + 0.2, t_prv - 0.1, t_23 - 0.45))
g.sfx("pop", t_dla); g.sfx("click-soft", t_20 + 0.15); g.sfx("pop", t_prv - 0.1)

# 13 · BEHIND — «2–3 години» ---------------------------------------------------
t_ice = S(u"І це", 71.52)
m0, m1 = t_23 - 0.2, t_ice - 0.05
B.append(u'''
        <div id="bw1" class="big hid" style="top:320px; font-size:240px">2–3</div>
        <div id="bw2" class="big hid" style="top:536px; font-size:240px">години</div>''')
g.matte("hours", round(m0 - 0.1, 3), round(m1 - m0 + 0.6, 3))
js(u'''
  rise("#bw1", %.3f); rise("#bw2", %.3f);
  sink("#bw1, #bw2", %.3f);
''' % (m0, m0 + 0.2, m1 - 0.35))
g.sfx("whoosh-short", m0)
BLACKOUT.append((t_23 - 0.05, E(u"години", 70.52) + 0.05))

# 14 · ABOVE — not my active work: the render runs, I do other things --------
t_rob, t_zm2 = S(u"робота —", 72.40), S(u"займаюсь", 73.44)
t_insh, t_spr = S(u"іншими", 73.92), S(u"справами.", 74.34)
t_tomu2 = S(u"Тому", 75.07)
F.append(u'''
        <div id="b14" class="card hid" style="left:120px; top:296px; width:840px; height:390px; padding:30px 40px">
          <div style="display:flex; justify-content:center">
            <span class="chip" id="b14a" style="position:relative">моя активна робота
              %s</span></div>
          <div style="display:flex; gap:40px; margin-top:30px">
            <div style="width:360px">
              <div class="row" style="gap:14px; color:#7A1424">%s<span style="font-weight:700; font-size:38px; color:#241919">рендер</span></div>
              <div class="bar" id="b14bar" style="width:340px; margin-top:34px"><b></b></div>
            </div>
            <div style="width:2px; background:#EFE3E3"></div>
            <div style="flex:1">
              <span style="display:block; font-weight:700; font-size:38px">я</span>
              %s
            </div>
          </div>
        </div>''' % (ink("b14x", -16, -8, 400, 86, [u"M10 50 C120 40 260 34 388 26"]), mark("claude", 46),
                     u"".join(u'<div class="row" style="margin-top:14px"><span class="check" id="b14k%d"></span>'
                              u'<span class="line" style="width:%dpx"></span></div>' % (i, w)
                              for i, w in enumerate((240, 200, 260)))))
js(u'''
  rise("#b14", %.3f); inkdraw("#b14x", %.3f, .35);
  fill("#b14bar b", %.3f, %.3f, "90%%");
  tl.set("#b14k0", {className: "check on"}, %.3f); pop("#b14k0", %.3f, .4);
  tl.set("#b14k1", {className: "check on"}, %.3f); pop("#b14k1", %.3f, .4);
  tl.set("#b14k2", {className: "check on"}, %.3f); pop("#b14k2", %.3f, .4);
  sink("#b14", %.3f);
''' % (t_ice - 0.05, t_rob, t_ice + 0.4, t_spr + 0.3 - t_ice - 0.4, t_zm2, t_zm2, t_insh, t_insh, t_spr, t_spr,
       t_tomu2 - 0.3))
g.sfx("pop", t_ice - 0.05); g.sfx("click-soft", t_rob)
for t in (t_zm2, t_spr):
    g.sfx("click-soft", t)
BLACKOUT.append((S(u"не", 71.72) - 0.05, E(u"робота —", 72.40) + 0.05))

# 15 · ABOVE — CTA: the time you lose on editing, this system, «Пиши + в коментарі»
t_zl, t_chas, t_sys = S(u"зливаєш", 76.07), S(u"час", 76.53), S(u"систему", 78.75)
t_pysh = S(u"то пиши", 79.43)
CLOCK = (u'<svg width="40" height="40" viewBox="0 0 40 40" style="flex:none"><circle cx="20" cy="20" r="16" fill="none" '
         u'stroke="#7A1424" stroke-width="4"/><path d="M20 10 V20 L27 24" fill="none" stroke="#7A1424" stroke-width="4" '
         u'stroke-linecap="round"/></svg>')
F.append(u'''
        <div id="b15" class="hid" style="position:absolute; left:120px; top:316px; width:840px;
             display:flex; gap:16px; justify-content:center; flex-wrap:wrap">
          <span class="chip hid" id="b15a">%sчас на монтаж</span>
          <span class="chip hid" id="b15b" style="color:#7A1424">%s<span style="color:#241919">така система</span></span>
        </div>
        <div id="b15cta" class="hid" style="position:absolute; left:0; top:448px; width:1080px; display:flex; justify-content:center">
          <span class="pill" style="position:relative">Пиши + в коментарі</span></div>''' % (CLOCK, mark("claude", 36)))
js(u'''
  fadein("#b15", %.3f, .01); pop("#b15a", %.3f); pop("#b15b", %.3f);
  pop("#b15cta", %.3f, .6);
  // the comments are down at the right of the IG rail: the pointer goes DOWN to
  // them, never up at the pill (her review of 41); tip left of x 900, ~300 px long
  sketch("a15", "skF"); arrow("a15", 760, 600, 878, 884, {strokeWidth: 5, seed: 97, bend: -.08});
  draw("a15", %.3f, .5);
''' % (t_zl - 0.05, t_chas, t_sys - 0.1, t_pysh - 0.1, t_pysh + 0.15))
g.sfx("pop", t_chas); g.sfx("pop", t_sys - 0.1); g.sfx("pop", t_pysh - 0.1)
BLACKOUT.append((t_pysh - 0.05, DUR))     # the pill says it

# ---------------------------------------------------------------- mattes for the half screens
for i, (a, b) in enumerate(HALF):
    g.matte("half%d" % (i + 1), round(a - 0.1, 3), round(b - a + 1.2, 3))
    js("  half(%.3f, %.3f);" % (a, b))

F.append(u'<svg class="sk" id="skF" width="1080" height="1920" viewBox="0 0 1080 1920"></svg>')


def main():
    if "--words" in sys.argv:
        print(" ".join("%s/%.1f" % (c["w"], c["s"]) for c in CAPS))
    chunks = g.chunks(CAPS)
    doc = g.document(title=u"Reel 48 — Уроки і YouTube", plate="assets/base.mp4",
                     behind="\n".join(B), panel="\n".join(P), front="\n".join(F), cover="\n".join(C),
                     js="\n".join(J), chunks=chunks, blackout=BLACKOUT, extra_css=EXTRA_CSS)
    g.write(HERE, doc)
    print("index.html  %d caption chunks, %d sfx cues, %d mattes" % (len(chunks), len(g.cues), len(g.mattes)))
    print("half", HALF, "full", (c0, c1))


main()
