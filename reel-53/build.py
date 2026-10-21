# -*- coding: utf-8 -*-
"""Reel 53 — «Як я монтую рілси з Клодом». Unplanned, no post date yet.

Her Google style + Excalidraw look (STYLE.md §00, with her review of reel 41:
word-by-word captions, calm sketches, white stickers over the footage).
No RUTA script: work/r53/script.txt is her own final wording.

The one object is **the pipeline**, step by step, as she does it:
gallery (12 hearted reels) -> Google Drive folder -> «доступ для усіх» ->
посилання -> Claude -> 2–3 годинки -> files to review / правки -> phone -> Edits
-> post. Each step's visual is ONE element, ids step1…step8, so a screen
recording she sends later can replace it (see PLAN.md).

Her plate is framed close: head top y ≈ 300–425, chin ≈ 875–1025. There is no
room above her head, so the «above me» cards sit over her chest (y 1095–1390),
and there is no behind-me word (a 240 px word from y 290 would be mostly hidden).
36.33–47.40 is her own laptop footage (Drive -> share -> Claude): it is not
painted over, only labelled with chips over the keyboard.

  front   a calendar crossed out, «?!» bubbles (people can't believe it)
  front   card: ghost videos -> Claude («налаштований»), lit on «відео»
  full    step1 — her gallery: 12 reels, hearted on «сердечком»
  front   step2 — card: 12 tiles fly into the Drive folder
  half    why the cloud: desktop / files / cloud; «старенький», power gauge drops
  front   step2 again on «Гугл-диск»
  laptop  step2-tag «папочка з рілсами», step3 «доступ для усіх»,
          step4 посилання -> Claude, «працює» + spinner
  half    step5 clock spins «2–3 годинки»; step6 Claude -> files, play, правки, ♥
  front   step7 files -> phone; step8 Edits on the phone -> Instagram; ✓ «Все»
  front   recap row of the whole chain, pill «настільки просто»
  front   CTA — the row again, circled on «ця система»; «Пиши + в коментарі»

usage: python build.py
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
from gstyle import G, Words, load_caps, mark, esc  # noqa: E402

NN = "53"
DUR = 75.150           # (2255 plate frames - 0.5) / 30
g = G(dur=DUR, reel=NN)

# whisper's spelling of what she said -> her word (re-heard solo on the plate)
FIX = {
    u"налаштували,": u"налаштувала,",
}


def split_multi(caps):
    """captions are word by word (her review of 41): a token the aligner kept
    as a phrase («з Клодом») is split, its time shared by letters"""
    out = []
    for c in caps:
        parts = c["w"].split()
        if len(parts) < 2:
            out.append(c)
            continue
        n = float(sum(len(p) for p in parts))
        t, span = c["s"], c["e"] - c["s"]
        for p in parts:
            d = span * len(p) / n
            out.append(dict(c, w=p, s=round(t, 3), e=round(t + d, 3)))
            t += d
    return out


CAPS = split_multi(load_caps(NN, FIX))
# «Все.» (62.43–63.03, its own clip) is on the plate but not in words.json
CAPS.append({"w": u"Все.", "s": 62.50, "e": 62.95})
CAPS.sort(key=lambda c: c["s"])
W = Words(CAPS)
S, E = W.s, W.e

# ---------------------------------------------------------------- the beats
B, P, F, C, J = [], [], [], [], []     # behind / panel / front / cover html, js
BLACKOUT = []
HALF = []


def js(s):
    J.append(s)


def red(svg):
    return u'<span style="color:#7A1424; display:inline-flex">%s</span>' % svg


def r3(x):
    return round(x, 3)


CSS = u"""
    .vt { position: absolute; width: 76px; height: 120px; border-radius: 14px; background: #FFF0F0;
          border: 2px solid #DEBFBF; display: flex; align-items: center; justify-content: center; }
    .vt.sm { width: 54px; height: 86px; border-radius: 10px; }
    .vt svg path { fill: #7A1424; }
    .phone { position: absolute; left: 0; top: 0; width: 580px; height: 1060px; border-radius: 64px;
             background: #241919; padding: 14px;
             box-shadow: 0 1px 3px rgba(36,25,25,.12), 0 18px 50px rgba(36,25,25,.18); }
    .scr { position: relative; width: 100%; height: 100%; border-radius: 52px; background: #fff;
           overflow: hidden; padding: 64px 26px 26px; }
    .gh { display: flex; align-items: center; justify-content: space-between; height: 56px;
          margin-bottom: 22px; }
    .gh b { font-weight: 700; font-size: 48px; letter-spacing: -0.02em; color: #241919; }
    .gh .n { background: #7A1424; color: #fff; border-radius: 999px; padding: 2px 26px;
             font-weight: 700; font-size: 40px; }
    .grid { display: grid; grid-template-columns: repeat(3, 160px); gap: 10px; }
    .th { position: relative; width: 160px; height: 200px; border-radius: 14px; background: #FFF0F0;
          overflow: hidden; }
    .th .sil { position: absolute; left: 0; top: 0; }
    .th .hz { position: absolute; left: 10px; bottom: 10px; width: 44px; height: 44px; }
    .mt { position: absolute; width: 34px; height: 50px; border-radius: 8px; background: #FFF0F0;
          border: 2px solid #DEBFBF; }
    .fold { position: absolute; width: 240px; height: 136px; }
    .fold .tab { position: absolute; left: 0; top: 0; width: 96px; height: 30px;
                 border-radius: 12px 12px 0 0; background: #F2C7CA; }
    .fold .body { position: absolute; left: 0; top: 22px; width: 240px; height: 114px;
                  border-radius: 0 18px 18px 18px; background: #FFF0F0; border: 2px solid #DEBFBF;
                  display: flex; align-items: center; justify-content: center; color: #7A1424; }
    .spin { display: inline-block; width: 30px; height: 30px; border-radius: 50%;
            border: 5px solid #DEBFBF; border-top-color: #7A1424; flex: none; }
    .ph { position: absolute; border: 7px solid #241919; border-radius: 24px; background: #fff;
          display: flex; align-items: center; justify-content: center; }
    .rc { display: inline-flex; align-items: center; gap: 8px; border: 2px solid var(--outline-var);
          border-radius: 16px; padding: 8px 14px; background: var(--chip); font-weight: 700;
          font-size: 30px; color: var(--on-surface); }
    .ra { flex: none; }
"""

PLAY = u'<svg width="%d" height="%d" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>'
HEART = (u'<svg class="%s" width="%d" height="%d" viewBox="0 0 24 24"><path fill="#7A1424" stroke="#FFFFFF" '
         u'stroke-width="1.6" d="M12 21.3l-1.4-1.3C5.4 15.4 2 12.3 2 8.5 2 5.4 4.4 3 7.5 3c1.7 0 3.4.8 4.5 '
         u'2.1C13.1 3.8 14.8 3 16.5 3 19.6 3 22 5.4 22 8.5c0 3.8-3.4 6.9-8.6 11.5L12 21.3z"/></svg>')
GLOBE = (u'<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">'
         u'<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18"/></svg>')
LINK = (u'<svg width="38" height="38" viewBox="0 0 24 24"><path fill="#7A1424" d="M3.9 12c0-1.71 1.39-3.1 '
        u'3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4'
        u'c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z"/></svg>')
CLOCK = (u'<svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#7A1424" stroke-width="2.6" '
         u'stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>')
RARROW = (u'<svg class="ra" width="34" height="22" viewBox="0 0 34 22"><path d="M3 11 H27 M19 4 L28 11 L19 18" '
          u'fill="none" stroke="#7A1424" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>')
SIL = (u'<svg class="sil" width="160" height="200" viewBox="0 0 160 200"><circle cx="80" cy="80" r="31" '
       u'fill="#DEBFBF"/><path d="M22 200 C28 136 132 136 138 200 Z" fill="#DEBFBF"/></svg>')

# front-layer sketches (over her footage: the kit makes them pass contrast)
SKF = u'<svg class="sk" id="skF" width="1080" height="1920" viewBox="0 0 1080 1920"></svg>'

js(u'''
  // a speech bubble: a rounded box with a tail, as one closed outline
  function bubbleD(x, y, w, h, tx, dir) {
    var r = 30, b = y + h;
    return "M" + (x + r) + " " + y + " H" + (x + w - r) + " A" + r + " " + r + " 0 0 1 " + (x + w) + " " + (y + r) +
      " V" + (b - r) + " A" + r + " " + r + " 0 0 1 " + (x + w - r) + " " + b +
      " H" + (tx + 34) + " L" + (tx + dir * 34) + " " + (b + 44) + " L" + tx + " " + b +
      " H" + (x + r) + " A" + r + " " + r + " 0 0 1 " + x + " " + (b - r) + " V" + (y + r) +
      " A" + r + " " + r + " 0 0 1 " + (x + r) + " " + y + " Z";
  }
  function poly(name, pts, o) { _ink = SK[name].ink; var s = SK[name];
    _add(s, s.rc.linearPath(pts, opt(o, (o && o.seed) || 29))); }
  function arc(name, cx, cy, w, h, a0, a1, o) { _ink = SK[name].ink; var s = SK[name];
    _add(s, s.rc.arc(cx, cy, w, h, a0, a1, false, opt(o, (o && o.seed) || 37))); }
  function cloud(name, cx, cy, k, o) { _ink = SK[name].ink; var s = SK[name];
    var d = "M300 600 C240 600 230 520 300 505 C300 430 400 410 440 460 C470 380 610 380 630 455 " +
            "C700 420 790 470 760 540 C830 560 810 640 740 630 Z";
    var i = 0;
    d = d.replace(/[\\d.]+/g, function (v) { var n = parseFloat(v), r = (i++ %% 2 === 0)
      ? cx + (n - 525) * k : cy + (n - 510) * k; return r.toFixed(1); });
    _add(s, s.rc.path(d, opt(o, (o && o.seed) || 31))); }
  function halfP(a, b) { half(a, b); }     // captions stay under her chin (PLAN.md)
'''.replace(u"%%", u"%"))

# 1 · FRONT — not planned: a calendar crossed out; «?!» — they can't believe it --
t_zapl, t_lyud, t_mozh = S(u"запланований", 0.39), S(u"люди", 1.37), S(u"можуть", 1.71)
t_shcho = S(u"що", 2.49)
js(u'''
  sketch("cal", "skF"); box("cal", 375, 1105, 240, 220, {seed: 3, r: 26});
  draw("cal", 0.0, .35);
  sketch("calg", "skF"); ln("calg", 375, 1162, 615, 1162, {seed: 4}); ln("calg", 430, 1086, 430, 1126, {seed: 5});
  ln("calg", 560, 1086, 560, 1126, {seed: 6}); ln("calg", 375, 1218, 615, 1218, {seed: 7, strokeWidth: 3});
  ln("calg", 375, 1272, 615, 1272, {seed: 8, strokeWidth: 3}); ln("calg", 455, 1162, 455, 1325, {seed: 9, strokeWidth: 3});
  ln("calg", 535, 1162, 535, 1325, {seed: 10, strokeWidth: 3});
  draw("calg", 0.1, .15);
  sketch("calx", "skF"); ln("calx", 392, 1122, 598, 1310, {stroke: "#7A1424", strokeWidth: 7, seed: 11});
  ln("calx", 598, 1122, 392, 1310, {stroke: "#7A1424", strokeWidth: 7, seed: 12});
  draw("calx", %(x).3f, .25);
  sketch("bb1", "skF"); blob("bb1", bubbleD(110, 1110, 210, 120, 250, 1), [110, 1110, 210, 164], {seed: 13});
  label("bb1", 215, 1196, "?!", {size: 64});
  draw("bb1", %(b1).3f, .45);
  sketch("bb2", "skF"); blob("bb2", bubbleD(670, 1150, 200, 120, 690, -1), [670, 1150, 200, 164], {seed: 15});
  label("bb2", 770, 1236, "?", {size: 64});
  draw("bb2", %(b2).3f, .45);
  ["cal", "calg", "calx", "bb1", "bb2"].forEach(function (n) { erase(n, %(out).3f); });
''' % {"x": t_zapl + 0.05, "b1": t_lyud - 0.05, "b2": t_mozh, "out": t_shcho - 0.1})
g.sfx("click-soft", t_zapl + 0.1); g.sfx("pop", t_lyud)

# 2 · FRONT — the claim: (her) videos -> Claude, once Claude is set up --------
t_zmon, t_klod = S(u"змонтувати", 3.1), S(u"Клодом", 4.15)
t_nal, t_vid = S(u"налаштувала,", 5.11), S(u"відео", 6.55)
t_klodu, t_tomu = S(u"Клоду.", 7.62), S(u"Тому", 8.18)
F.append(u'''
        <div id="b2" class="card hid" style="left:100px; top:1105px; width:790px; height:270px; padding:26px 34px;">
          <span class="lbl">Монтаж рілсів</span>
          %(tiles)s
          <span class="chip hid" id="b2c" style="position:absolute; left:500px; top:96px; font-weight:700; font-size:40px">%(cl)s Claude</span>
          <span class="chip on hid" id="b2n" style="position:absolute; left:500px; top:186px; font-size:28px; padding:8px 18px"><i></i>налаштований</span>
        </div>''' % {"cl": red(mark("claude", 44)),
                     "tiles": u"".join(u'<span class="vt" id="b2t%d" style="left:%dpx; top:92px; opacity:.35; filter:grayscale(1)">%s</span>'
                                       % (i, 40 + i * 88, PLAY % (34, 34)) for i in range(3))})
js(u'''
  rise("#b2", %(rise).3f);
  pop("#b2c", %(klod).3f);
  pop("#b2n", %(nal).3f, .45);
  tl.to("#b2t0, #b2t1, #b2t2", {opacity: 1, filter: "grayscale(0)", scale: 1.08, duration: .25, stagger: .08, ease: "power2.out"}, %(vid).3f);
  tl.to("#b2t0, #b2t1, #b2t2", {scale: 1, duration: .25, stagger: .08}, %(vid2).3f);
  sketch("a2", "skF"); arrow("a2", 410, 1262, 588, 1250, {seed: 17, bend: .15});
  draw("a2", %(arr).3f, .45);
  sink("#b2", %(out).3f); erase("a2", %(out).3f);
''' % {"rise": t_zmon - 0.2, "klod": t_klod - 0.05, "nal": t_nal, "vid": t_vid - 0.05, "vid2": t_vid + 0.2,
       "arr": t_klodu - 0.6, "out": t_tomu + 0.1})
g.sfx("pop", t_zmon - 0.2); g.sfx("click-soft", t_klod); g.sfx("pop", t_vid)

# 3 · FULL — step1: her gallery, 12 new reels, hearted -----------------------
t_sohodni, t_12 = S(u"Сьогодні", 10.24), S(u"12", 10.90)
t_galer, t_serd = S(u"галереї,", 12.96), S(u"сердечком.", 14.13)
c0, c1 = r3(t_12 - 0.85), r3(S(u"І", 15.05) - 0.05)
thumbs = u"".join(u'<div class="th hid" id="s1t%d">%s%s</div>' % (i, SIL, HEART % ("hz hid", 44, 44)) for i in range(12))
C.append(u'''
        <div id="step1" style="position:absolute; left:250px; top:300px; width:580px; height:1060px;">
          <div class="phone"><div class="scr" id="step1-screen">
            <div class="gh"><b>Галерея</b><span class="n hid" id="s1n">12</span></div>
            <div class="grid">%s</div>
          </div></div>
        </div>
        <svg class="sk" id="skC" width="1080" height="1920" viewBox="0 0 1080 1920"></svg>''' % thumbs)
js(u'''
  full(%(c0).3f, %(c1).3f);
  pop("#s1n", %(n).3f);
  %(th)s
  sketch("gu", "skC"); under("gu", 288, 444, 520, {stroke: "#7A1424", strokeWidth: 6, seed: 19});
  draw("gu", %(gal).3f, .45);
  %(hz)s
''' % {"c0": c0, "c1": c1, "n": t_12,
       "th": u" ".join(u'pop("#s1t%d", %.3f, .45);' % (i, t_12 - 0.12 + i * 0.035) for i in range(12)),
       "gal": t_galer - 0.2,
       "hz": u" ".join(u'pop("#s1t%d .hz", %.3f, .4);' % (i, t_serd - 0.4 + i * 0.04) for i in range(12))})
g.sfx("whoosh-short", c0); g.sfx("pop", t_12); g.sfx("pop", t_serd - 0.2)
g.sfx("whoosh-short", c1)

# 4 · FRONT — step2: «завантажити їх на диск» — 12 tiles fly into the Drive folder
FOLD_C = (730, 1254)                   # page centre of the folder body
mts, mt_ids = [], []
for i in range(12):
    cx, cy = 40 + (i % 6) * 43, 92 + (i // 6) * 59
    mts.append(u'<span class="mt" id="s2m%d" style="left:%dpx; top:%dpx"></span>' % (i, cx, cy))
    mt_ids.append((i, 100 + cx + 17, 1105 + cy + 25))
F.append(u'''
        <div id="step2" class="card hid" style="left:100px; top:1105px; width:790px; height:270px; padding:26px 34px;">
          <span class="lbl">Завантажити на диск</span>
          %(mts)s
          <div class="fold" id="s2f" style="left:510px; top:70px;"><div class="tab"></div>
            <div class="body">%(dr)s</div></div>
          <span id="s2t" style="position:absolute; left:510px; top:214px; width:240px; text-align:center;
                font-weight:500; font-size:30px; color:#241919">Google Drive</span>
        </div>''' % {"mts": u"".join(mts), "dr": mark("googledrive", 60)})


def fly(t):
    return u" ".join(u'tl.to("#s2m%d", {x: %d, y: %d, scale: .3, autoAlpha: 0, duration: .45, ease: "power2.in"}, %.3f);'
                     % (i, FOLD_C[0] - x, FOLD_C[1] - y, t + i * 0.03) for i, x, y in mt_ids)


RESET = u'tl.set("%s", {x: 0, y: 0, scale: 1, autoAlpha: 1}, %%.3f);' % u", ".join(u"#s2m%d" % i for i in range(12))
t_zav, t_dysk = S(u"завантажити", 18.75), S(u"диск.", 19.81)
t_yakshcho = S(u"якщо", 20.64)
js(u'''
  rise("#step2", %(rise).3f);
  sketch("dr1", "skF"); arrow("dr1", 408, 1262, 598, 1255, {seed: 21, bend: .15});
  draw("dr1", %(arr).3f, .4);
  %(fly)s
  tl.fromTo("#s2f", {scale: 1}, X({scale: 1.1, duration: .18, yoyo: true, repeat: 1, ease: "power2.out"}), %(dysk).3f);
  sink("#step2", %(out).3f); erase("dr1", %(out).3f);
''' % {"rise": t_zav - 0.3, "arr": t_zav, "fly": fly(t_dysk - 0.6), "dysk": t_dysk - 0.05,
       "out": t_yakshcho - 0.3})
g.sfx("pop", t_zav - 0.3); g.sfx("click-soft", t_dysk)

# 5 · HALF 1 — why the cloud: a desktop would do, but hers is old and weak -----
h0, h1 = r3(S(u"десктопі,", 22.02) - 0.85), r3(S(u"хмарі.", 33.11) - 0.1)
HALF.append((h0, h1))
t_desk, t_zak, t_komp = S(u"десктопі,", 22.02), S(u"закинути", 24.86), S(u"комп'ютер.", 25.52)
t_hm, t_star = S(u"хмарі,", 27.45), S(u"старенький,", 28.91)
t_trosh, t_potuzh = S(u"трошечки", 29.61), S(u"потужний,", 30.65)
t_prost, t_mont = S(u"простіше", 31.91), S(u"монтувати", 32.25)
P.append(u'        <div id="why" class="L"><svg class="sk" id="skP1" width="1080" height="1240" viewBox="0 0 1080 1240"></svg></div>')
js(u'''
  sketch("pc", "skP1"); box("pc", 100, 470, 240, 160, {seed: 23, r: 16});
  ln("pc", 220, 630, 220, 668, {seed: 24}); ln("pc", 160, 672, 280, 672, {seed: 25});
  label("pc", 220, 450, "десктоп", {size: 46});
  draw("pc", %(desk).3f, .4);
  sketch("fl", "skP1"); box("fl", 440, 300, 62, 100, {seed: 27, r: 12}); box("fl", 510, 300, 62, 100, {seed: 28, r: 12});
  box("fl", 580, 300, 62, 100, {seed: 29, r: 12});
  poly("fl", [[464, 334], [464, 366], [486, 350], [464, 334]], {seed: 30, strokeWidth: 3.5});
  poly("fl", [[534, 334], [534, 366], [556, 350], [534, 334]], {seed: 31, strokeWidth: 3.5});
  poly("fl", [[604, 334], [604, 366], [626, 350], [604, 334]], {seed: 32, strokeWidth: 3.5});
  draw("fl", %(zak).3f, .22);
  sketch("a1", "skP1"); arrow("a1", 430, 372, 300, 462, {seed: 33, bend: -.2});
  draw("a1", %(komp).3f, .45);
  sketch("cl", "skP1"); cloud("cl", 855, 560, .45, {seed: 35});
  label("cl", 855, 584, "хмара", {size: 46});
  draw("cl", %(hm).3f, .7);
  sketch("st", "skP1"); label("st", 220, 730, "старенький", {size: 46, color: "#7A1424"});
  draw("st", %(star).3f);
  sketch("ga", "skP1"); arc("ga", 220, 604, 130, 130, Math.PI, Math.PI * 2, {seed: 39, strokeWidth: 4});
  draw("ga", %(trosh).3f, .4);
  sketch("nd", "skP1"); ln("nd", 220, 604, 220, 552, {stroke: "#7A1424", strokeWidth: 6, seed: 41});
  draw("nd", %(trosh2).3f, .25);
  tl.to("#sk-nd", {rotation: -72, svgOrigin: "220 604", duration: .5, ease: POP}, %(pot).3f);
  sketch("a3", "skP1"); arrow("a3", 652, 372, 790, 492, {seed: 43, bend: .2});
  draw("a3", %(prost).3f, .45);
  sketch("tk", "skP1"); poly("tk", [[922, 452], [944, 480], [986, 424]], {stroke: "#7A1424", strokeWidth: 7, seed: 45});
  draw("tk", %(mont).3f, .35);
  ["pc", "fl", "a1", "cl", "st", "ga", "nd", "a3", "tk"].forEach(function (n) { erase(n, %(h1).3f); });
''' % {"desk": t_desk - 0.1, "zak": t_zak - 0.1, "komp": t_komp - 0.45, "hm": t_hm - 0.55, "star": t_star - 0.05,
       "trosh": t_trosh - 0.1, "trosh2": t_trosh + 0.25, "pot": t_potuzh - 0.2, "prost": t_prost - 0.45,
       "mont": t_mont - 0.05, "h1": h1})
g.sfx("whoosh-short", h0); g.sfx("click-soft", t_komp); g.sfx("pop", t_hm); g.sfx("click-soft", t_star)
g.sfx("click-soft", t_potuzh); g.sfx("whoosh-short", h1)

# 6 · FRONT — step2 again: «завантажую їх на Гугл-диск» ----------------------
t_pershe, t_zav2, t_gd = S(u"перше,", 33.89), S(u"завантажую", 34.89), S(u"Гугл-диск.", 35.49)
s2b0 = max(t_pershe - 0.1, h1 + 0.85)
js(u'''
  %(reset)s
  rise("#step2", %(rise).3f);
  sketch("dr2", "skF"); arrow("dr2", 408, 1262, 598, 1255, {seed: 47, bend: .15});
  draw("dr2", %(arr).3f, .4);
  %(fly)s
  tl.fromTo("#s2f", {scale: 1}, X({scale: 1.1, duration: .18, yoyo: true, repeat: 1, ease: "power2.out"}), %(gd).3f);
  tl.fromTo("#s2t", {color: "#241919"}, X({color: "#7A1424", duration: .2}), %(gd).3f);
  out("#step2", %(out).3f); erase("dr2", %(out).3f);
''' % {"reset": RESET % (s2b0 - 0.05), "rise": s2b0, "arr": t_zav2 - 0.35, "fly": fly(t_zav2 + 0.05),
       "gd": t_gd - 0.05, "out": 36.0})
g.sfx("pop", s2b0); g.sfx("click-soft", t_gd)

# 7 · LAPTOP (her own footage 36.33–47.40) — chips over the keyboard ------------
t_pap, t_dali = S(u"папочка,", 37.3), S(u"Далі", 39.70)
t_dost, t_usih = S(u"доступ", 40.55), S(u"усіх", 41.05)
t_beru, t_pos = S(u"Беру", 42.71), S(u"посилання", 43.03)
t_klod2, t_os, t_pracyuye = S(u"Клод.", 45.09), S(u"ось", 46.02), S(u"працює.", 46.80)
F.append(u'''
        <span id="step2-tag" class="chip hid" style="position:absolute; left:100px; top:1262px;">%(dr)s папочка з рілсами</span>
        <span id="step3" class="chip on hid" style="position:absolute; left:100px; top:1262px;">%(globe)s доступ для усіх</span>
        <div id="step4" class="L">
          <span id="s4l" class="chip hid" style="position:absolute; left:100px; top:1262px;">%(link)s посилання</span>
          <span id="s4c" class="chip hid" style="position:absolute; left:610px; top:1262px; font-weight:700">%(cl)s Claude</span>
          <span id="s4w" class="chip hid" style="position:absolute; left:610px; top:1160px; font-size:32px"><span class="spin" id="s4sp"></span>працює</span>
        </div>''' % {"dr": red(mark("googledrive", 34)), "globe": GLOBE, "link": LINK, "cl": red(mark("claude", 40))})
js(u'''
  pop("#step2-tag", %(pap).3f); out("#step2-tag", %(dali).3f);
  pop("#step3", %(dost).3f); out("#step3", %(beru).3f);
  pop("#s4l", %(pos).3f);
  sketch("s4a", "skF"); arrow("s4a", 392, 1300, 596, 1296, {seed: 49, bend: .15});
  draw("s4a", %(arr).3f, .45);
  pop("#s4c", %(klod).3f);
  pop("#s4w", %(os).3f);
  tl.fromTo("#s4sp", {rotation: 0}, X({rotation: 540, duration: %(spin).3f, ease: "none"}), %(os).3f);
  out("#s4l, #s4c, #s4w", %(end).3f); erase("s4a", %(end).3f);
''' % {"pap": t_pap - 0.08, "dali": t_dali - 0.3, "dost": t_dost - 0.1, "beru": t_beru - 0.3,
       "pos": t_pos - 0.08, "arr": t_klod2 - 0.6, "klod": t_klod2 - 0.08, "os": t_os,
       "spin": 47.25 - t_os, "end": 47.25})
g.sfx("pop", t_pap); g.sfx("pop", t_dost); g.sfx("pop", t_pos)
g.sfx("typing", t_os)
BLACKOUT.append((t_dost - 0.05, E(u"усіх", 41.05) + 0.05))

# 8 · HALF 2 — step5: wait 2–3 годинки; step6: Claude -> files, play, правки, ♥ --
h2 = 47.5
t_poch, t_23, t_god = S(u"почекати", 48.47), S(u"2-3", 48.93), S(u"годинки,", 49.29)
t_vin, t_pidg = S(u"він", 50.59), S(u"підготує,", 51.56)
t_vyd, t_fay = S(u"видасть", 52.74), S(u"файли,", 53.46)
t_progl, t_daty, t_pravky = S(u"проглянути,", 54.30), S(u"дати", 55.01), S(u"правки.", 55.49)
t_podob, t_to = S(u"подобається,", 56.85), S(u"то", 57.49)
h3 = r3(t_to - 0.2)
HALF.append((h2, h3))
P.append(u'''        <div id="step5" class="L"><svg class="sk" id="skS5" width="1080" height="1240" viewBox="0 0 1080 1240"></svg></div>
        <div id="step6" class="L"><svg class="sk" id="skS6" width="1080" height="1240" viewBox="0 0 1080 1240"></svg>
          <span id="s6m" class="hid" style="position:absolute; left:440px; top:335px; color:#7A1424">%(cl)s</span>
          <div id="s6bar" class="hid" style="position:absolute; left:430px; top:452px; width:220px; height:28px;
               border:3px solid #1E1E1E; border-radius:14px; overflow:hidden; padding:3px">
            <div id="s6fill" style="width:100%%; height:100%%; border-radius:9px; background:#7A1424;
                 transform-origin:0 50%%; transform:scaleX(0)"></div></div>
        </div>''' % {"cl": mark("claude", 58)})
js(u'''
  sketch("ck", "skS5"); ell("ck", 230, 470, 230, 230, {seed: 51});
  draw("ck", %(poch).3f, .55);
  sketch("ckt", "skS5"); ln("ckt", 230, 362, 230, 380, {seed: 52}); ln("ckt", 338, 470, 320, 470, {seed: 53});
  ln("ckt", 230, 578, 230, 560, {seed: 54}); ln("ckt", 122, 470, 140, 470, {seed: 55});
  draw("ckt", %(poch2).3f, .15);
  sketch("mh", "skS5"); ln("mh", 230, 470, 230, 388, {seed: 56, strokeWidth: 5});
  sketch("hh", "skS5"); ln("hh", 230, 470, 282, 470, {seed: 57, strokeWidth: 7});
  draw("mh", %(hands).3f, .25); draw("hh", %(hands).3f, .25);
  tl.to("#sk-mh", {rotation: 720, svgOrigin: "230 470", duration: 1.0, ease: "power2.inOut"}, %(t23).3f);
  tl.to("#sk-hh", {rotation: 75, svgOrigin: "230 470", duration: 1.0, ease: "power2.inOut"}, %(t23).3f);
  sketch("ckl", "skS5"); label("ckl", 230, 656, "2–3 годинки", {size: 48, color: "#7A1424"});
  draw("ckl", %(god).3f);

  sketch("cb", "skS6"); box("cb", 420, 300, 240, 130, {seed: 59, r: 26});
  label("cb", 582, 381, "Claude", {size: 46});
  draw("cb", %(vin).3f, .5);
  pop("#s6m", %(vin2).3f, .45);
  fadein("#s6bar", %(bar).3f, .3);
  tl.fromTo("#s6fill", {scaleX: 0}, X({scaleX: 1, duration: 1.1, ease: "power1.inOut"}), %(bar2).3f);
  sketch("a6", "skS6"); arrow("a6", 668, 380, 806, 478, {seed: 61, bend: -.2});
  draw("a6", %(vyd).3f, .45);
  sketch("fs", "skS6"); box("fs", 780, 492, 62, 110, {seed: 63, r: 12}); box("fs", 850, 492, 62, 110, {seed: 64, r: 12});
  box("fs", 920, 492, 62, 110, {seed: 65, r: 12});
  draw("fs", %(fay).3f, .3);
  sketch("fp", "skS6");
  poly("fp", [[801, 532], [801, 562], [823, 547], [801, 532]], {seed: 66, strokeWidth: 3.5});
  poly("fp", [[871, 532], [871, 562], [893, 547], [871, 532]], {seed: 67, strokeWidth: 3.5});
  poly("fp", [[941, 532], [941, 562], [963, 547], [941, 532]], {seed: 68, strokeWidth: 3.5});
  draw("fp", %(progl).3f, .2);
  sketch("pr", "skS6"); poly("pr", [[786, 628], [806, 614], [826, 632], [846, 612], [866, 632], [886, 612], [906, 632], [926, 612], [946, 630], [972, 614]],
    {stroke: "#7A1424", strokeWidth: 5, seed: 69});
  draw("pr", %(daty).3f, .45);
  sketch("prl", "skS6"); label("prl", 880, 696, "правки", {size: 48, color: "#7A1424"});
  draw("prl", %(pravky).3f);
  sketch("lv", "skS6"); blob("lv", "M880 478 C842 452 832 418 856 404 C870 396 880 406 880 416 C880 406 890 396 904 404 C928 418 918 452 880 478 Z",
    [832, 396, 96, 82], {stroke: "#7A1424", strokeWidth: 5, fill: "#F2C7CA", fillStyle: "hachure", hachureGap: 9, fillWeight: 2.5, seed: 71});
  draw("lv", %(podob).3f, .45);
  ["ck", "ckt", "mh", "hh", "ckl", "cb", "a6", "fs", "fp", "pr", "prl", "lv"].forEach(function (n) { erase(n, %(h3).3f); });
  out("#s6m, #s6bar", %(h3).3f);
''' % {"poch": t_poch - 0.15, "poch2": t_poch + 0.2, "hands": t_poch + 0.35, "t23": t_23, "god": t_god - 0.05,
       "vin": t_vin - 0.1, "vin2": t_vin + 0.25, "bar": t_pidg - 0.55, "bar2": t_pidg - 0.35,
       "vyd": t_vyd - 0.1, "fay": t_fay - 0.3, "progl": t_progl - 0.1, "daty": t_daty, "pravky": t_pravky - 0.1,
       "podob": t_podob - 0.3, "h3": h3})
g.sfx("whoosh-short", h2); g.sfx("click-soft", t_poch); g.sfx("click-soft", t_pidg); g.sfx("pop", t_fay)
g.sfx("click-soft", t_pravky); g.sfx("pop", t_podob); g.sfx("whoosh-short", h3)

# 9 · FRONT — step7: files -> her phone; step8: Edits on the phone -> Instagram; ✓
t_zav3, t_tel = S(u"завантажую", 57.77), S(u"телефон,", 58.79)
t_edits, t_zapost = S(u"Edits", 60.40), S(u"запостити", 60.90)
t_edits2, t_vse, t_tomu2 = S(u"Edits.", 61.98), S(u"Все.", 62.43), S(u"Тому", 63.43)
F.append(u'''
        <div id="step7" class="card hid" style="left:100px; top:1105px; width:790px; height:270px; padding:26px 34px;">
          <span class="lbl">Собі на телефон</span>
          %(files)s
          <div id="step7-phone" class="ph hid" style="left:385px; top:50px; width:118px; height:206px;">
            <span id="step8" class="hid" style="font-weight:700; font-size:30px; letter-spacing:-0.02em; color:#241919">Edits</span>
          </div>
          <div id="step8-post" class="hid" style="position:absolute; left:675px; top:84px; width:90px; text-align:center; color:#7A1424">
            %(ig)s<span style="display:block; margin-top:6px; font-weight:500; font-size:28px; color:#241919">пост</span></div>
        </div>''' % {"ig": mark("instagram", 64),
                     "files": u"".join(u'<span class="vt sm" style="left:%dpx; top:96px">%s</span>' % (30 + i * 62, PLAY % (24, 24))
                                       for i in range(3))})
js(u'''
  rise("#step7", %(rise).3f);
  sketch("a7", "skF"); arrow("a7", 318, 1262, 478, 1252, {seed: 73, bend: .15});
  draw("a7", %(arr).3f, .45);
  pop("#step7-phone", %(tel).3f);
  pop("#step8", %(ed).3f, .45);
  sketch("a8", "skF"); arrow("a8", 620, 1262, 770, 1236, {seed: 75, bend: .15});
  draw("a8", %(arr2).3f, .4);
  pop("#step8-post", %(post).3f);
  tl.to("#step8", {color: "#7A1424", scale: 1.15, duration: .2, ease: "power2.out"}, %(ed2).3f);
  tl.to("#step8", {scale: 1, duration: .25}, %(ed3).3f);
  sketch("vs", "skF"); poly("vs", [[808, 1148], [830, 1176], [872, 1118]], {stroke: "#7A1424", strokeWidth: 8, seed: 77});
  draw("vs", %(vse).3f, .3);
  sink("#step7", %(out).3f); ["a7", "a8", "vs"].forEach(function (n) { erase(n, %(out).3f); });
''' % {"rise": t_zav3 - 0.25, "arr": t_zav3 + 0.2, "tel": t_tel - 0.1, "ed": t_edits - 0.05,
       "arr2": t_zapost - 0.45, "post": t_zapost, "ed2": t_edits2 - 0.05, "ed3": t_edits2 + 0.2,
       "vse": t_vse - 0.05, "out": t_tomu2 - 0.35})
g.sfx("pop", t_zav3 - 0.25); g.sfx("pop", t_edits); g.sfx("click-soft", t_zapost)
g.sfx("click-soft", t_vse)

# 10 · FRONT — «настільки просто»: the whole chain in one row ------------------
t_nast, t_tse2, t_nast2 = S(u"настільки", 68.76), S(u"Це", 69.74), S(u"настільки", 69.86)
t_i = S(u"І", 70.96)
row = [u'<span class="rc hid" id="rc0">%s 12</span>' % (HEART % ("", 30, 30)),
       u'<span class="rc hid" id="rc1" style="color:#7A1424">%s</span>' % mark("googledrive", 32),
       u'<span class="rc hid" id="rc2" style="color:#7A1424">%s</span>' % mark("claude", 32),
       u'<span class="rc hid" id="rc3">%s 2–3 год</span>' % CLOCK,
       u'<span class="rc hid" id="rc4">Edits</span>']
F.append(u'''
        <div id="recap" class="card hid" style="left:100px; top:1095px; width:790px; padding:16px 20px;
             display:flex; align-items:center; justify-content:center; gap:10px">%s</div>
        <div id="rpill" class="pill hid" style="left:250px; top:1228px;">настільки просто</div>'''
         % (u"".join(x + (u'<span class="hid" id="ra%d" style="display:inline-flex">%s</span>' % (i, RARROW) if i < 4 else u"")
                     for i, x in enumerate(row))))
rc0 = t_nast - 0.62
js(u'''
  fadein("#recap", %(r0).3f, .25);
  %(chips)s
  pop("#rpill", %(pill).3f);
  sink("#recap, #rpill", %(out).3f);
''' % {"r0": rc0 - 0.1,
       "chips": u" ".join(u'pop("#rc%d", %.3f, .45);' % (i, rc0 + i * 0.15) for i in range(5)) + u" " +
                u" ".join(u'pop("#ra%d", %.3f, .35);' % (i, rc0 + i * 0.15 + 0.07) for i in range(4)),
       "pill": t_nast2 - 0.12, "out": t_i - 0.2})
g.sfx("pop", rc0); g.sfx("pop", t_nast2)
BLACKOUT.append((t_nast2 - 0.05, min(E(u"просто.", 70.26) + 0.1, t_i - 0.25)))

# 11 · FRONT — CTA: the system again, circled; «Пиши + в коментарі» -----------
t_tsya, t_syst = S(u"ця", 73.16), S(u"система,", 73.34)
t_to2, t_plus = S(u"то", 73.96), S(u"плюс", 74.30)
F.append(u'''
        <div id="cta" class="pill hid" style="left:100px; top:1238px;">Пиши + в коментарі</div>''')
js(u'''
  tl.set("#rc0, #rc1, #rc2, #rc3, #rc4, #ra0, #ra1, #ra2, #ra3", {autoAlpha: 1, scale: 1}, %(t).3f);
  rise("#recap", %(t).3f, 40);
  sketch("ce", "skF"); under("ce", 150, 1202, 840, {stroke: "#7A1424", strokeWidth: 6, seed: 79});
  draw("ce", %(syst).3f, .55);
  pop("#cta", %(to).3f, .6);
  sketch("cp", "skF"); arrow("cp", 862, 1446, 690, 1312, {stroke: "#7A1424", strokeWidth: 6, seed: 81, bend: -.2});
  draw("cp", %(plus).3f, .45);
''' % {"t": t_tsya - 0.2, "syst": t_syst - 0.1, "to": t_to2 - 0.05, "plus": t_plus - 0.2})
g.sfx("pop", t_tsya - 0.2); g.sfx("pop", t_to2)
BLACKOUT.append((t_to2 - 0.05, DUR))     # the pill says it

# front sketches over everything else in #front
F.append(SKF)

# ---------------------------------------------------------------- mattes for the half screens
for i, (a, b) in enumerate(HALF):
    g.matte("half%d" % (i + 1), round(a - 0.1, 3), round(b - a + 1.2, 3))
    js("  halfP(%.3f, %.3f);" % (a, b))


def main():
    print(" ".join(u"%s/%.1f" % (c["w"], c["s"]) for c in CAPS))
    chunks = g.chunks(CAPS)
    doc = g.document(title=u"Reel 53 — Як я монтую рілси з Клодом", plate="assets/base.mp4",
                     behind="\n".join(B), panel="\n".join(P), front="\n".join(F), cover="\n".join(C),
                     js="\n".join(J), chunks=chunks, blackout=BLACKOUT, extra_css=CSS)
    g.write(HERE, doc)
    print("index.html  %d caption chunks, %d sfx cues, %d mattes" % (len(chunks), len(g.cues), len(g.mattes)))
    print("HALF", HALF, "BLACKOUT", [(round(a, 2), round(b, 2)) for a, b in BLACKOUT])


main()
