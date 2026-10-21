# -*- coding: utf-8 -*-
"""Reel 50 — «Поки я сплю». Posts 2026-10-24.

Her Google style + Excalidraw look (STYLE.md §00, with her review of reel 41:
word-by-word captions; sketches over the footage pass contrast by themselves —
the kit makes closed shapes white stickers with a dark outline and gives
strokes a white halo, so nothing here passes a colour over the footage; white
behind-me; a pointer goes DOWN, never up at the pill).

The one object is **the clock that runs while she doesn't**: an empty Claude
chat that is still «працює»; the routines behind her; a clock that ticks every
few hours and turns her chats into a checklist; a weekly report with ideas;
the same clock as an alarm in the morning with everything already ticked; then
the cloud — the laptop closes and sleeps, the clock spins (any time), the cloud
makes the reel. CTA: «такі системи» as chips, «Підпишись», a pointer down
to the follow button.

  above   Claude card «працює» over an empty composer, circled on «нічого»
  behind  «рутини»
  half    clock (hour hand jumps) -> Instagram / Telegram chats, ticked ->
          checklist of tasks: мені / команді
  above   two cards: weekly content report (bars), ideas for next week
  above   alarm clock rings; «Вже готове» checklist ticks
  above   a cloud: Claude + чати / задачі / звіти
  half    cloud; the laptop closes (z z z); the clock spins; cloud -> a reel
  above   CTA — chips, «Підпишись», pointer down to the follow button

usage: python build.py
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
from gstyle import G, Words, load_caps, mark, esc  # noqa: E402

NN = "50"
DUR = 37.750           # (1133 plate frames - 0.5) / 30
g = G(dur=DUR, reel=NN)

# whisper's spelling of what she plainly said -> her word (re-heard on the plate)
FIX = {
    u"Claude": u"Мій Клод",          # «Міклот» on the plate: «Мій Клод»
    u"коли я йому": u"коли йому",    # no «я» on the plate (3 of 4 hearings)
    u"пишу.": u"пишу,",
    u"У нього": u"у нього",
    u"сорюю": u"створює",            # fast «створює»
    u"виконуються": u"виконується",  # she says the singular (every unprompted hearing)
    u"Це": u"це",
    u"відкритим": u"відкритим.",
    (u"він", 29.9): u"Він",
    u"сам,": u"сам.",
    u"наприклад": u"Наприклад,",
    u"монтаж": u"монтаж рілсів.",    # the cut clips «рілсів» short; prompted pass hears it
}


def split_multi(caps):
    """captions are word by word (her review of 41): a token the aligner kept
    as a phrase («і в телеграмі,») is split, its time shared by letters"""
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
P.append(u'<svg class="sk" id="skP" width="1080" height="1240" viewBox="0 0 1080 1240"></svg>')

# helpers on top of the kit: a hand tick, a cloud at any size, a polyline
js(u'''
  function tick(name, x, y, o) { _ink = SK[name].ink; var s = SK[name];
    _add(s, s.rc.linearPath([[x, y], [x + 16, y + 22], [x + 50, y - 24]], opt(o, (o && o.seed) || 23))); }
  function poly(name, pts, o) { _ink = SK[name].ink; var s = SK[name];
    _add(s, s.rc.linearPath(pts, opt(o, (o && o.seed) || 29))); }
  // closed outlines go through the kit's blob(): over the footage it makes them
  // a white sticker with the dark outline (her review of 41), on the panel ink
  function cloud(name, cx, cy, k, o) {
    var d = "M300 600 C240 600 230 520 300 505 C300 430 400 410 440 460 C470 380 610 380 630 455 " +
            "C700 420 790 470 760 540 C830 560 810 640 740 630 Z";
    var i = 0;
    d = d.replace(/[\\d.]+/g, function (v) { var n = parseFloat(v), r = (i++ % 2 === 0)
      ? cx + (n - 525) * k : cy + (n - 510) * k; return r.toFixed(1); });
    blob(name, d, [cx - 295 * k, cy - 130 * k, 600 * k, 260 * k], {seed: (o && o.seed) || 31}); }
  // an alarm-clock bell: a dome whose base sits on the face at angle a (deg)
  function bell(name, cx, cy, r, a, o) {
    var rad = a * Math.PI / 180, ux = Math.cos(rad), uy = Math.sin(rad), dx = -uy, dy = ux;
    var bx = cx + ux * (r - 8), by = cy + uy * (r - 8), hw = 42;
    var x1 = bx - dx * hw, y1 = by - dy * hw, x2 = bx + dx * hw, y2 = by + dy * hw;
    var rot = Math.atan2(dy, dx) * 180 / Math.PI;
    var d = "M" + x1.toFixed(1) + " " + y1.toFixed(1) + " A" + hw + " 36 " + rot.toFixed(1) + " 0 1 " +
            x2.toFixed(1) + " " + y2.toFixed(1) + " Z";
    blob(name, d, [bx - 50, by - 50, 100, 100], {seed: (o && o.seed) || 37}); }
''')

# 1 · ABOVE — an empty Claude chat that still «працює» --------------------------
t_klod, t_prac = S(u"Клод", 1.0), S(u"працює", 1.33)
t_koly, t_nich, e_pyshu = S(u"коли", 2.99), S(u"нічого", 3.39), E(u"пишу,", 4.13)
F.append(u'''
        <div id="b1" class="card hid" style="left:120px; top:340px; width:840px; padding:32px 36px;">
          <div class="row" style="gap:18px">
            <span style="color:#7A1424; display:flex">%s</span>
            <span class="ttl" style="font-size:52px">Claude</span>
            <span class="chip on hid" id="b1s" style="margin-left:auto; font-size:32px; padding:10px 22px"><i></i>працює</span>
          </div>
          <div id="b1in" class="hid" style="position:relative; margin-top:28px; display:flex; align-items:center; gap:16px;
               border:2px solid #DEBFBF; border-radius:999px; padding:14px 14px 14px 32px; background:#FFF8F7">
            <span style="flex:1; font-size:34px; color:#A08C8C">Напиши повідомлення…</span>
            <span style="width:58px; height:58px; border-radius:50%%; background:#EFE3E3; display:flex;
                  align-items:center; justify-content:center">
              <svg width="28" height="28" viewBox="0 0 28 28"><path d="M14 23 V6 M6 13 L14 5 L22 13" fill="none"
                   stroke="#fff" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
            <svg class="sk" id="skB1" width="840" height="200" viewBox="0 0 840 200" style="left:-36px; top:-40px"></svg>
          </div>
        </div>''' % mark("claude", 56))
js(u'''
  rise("#b1", %.3f); pop("#b1s", %.3f);
  rise("#b1in", %.3f, 24);
  // round the empty composer: an outline, not a sticker (a white fill would hide it)
  sketch("c1", "skB1"); box("c1", 22, 26, 796, 114, {r: 56, fill: false, strokeWidth: 5, seed: 3});
  draw("c1", %.3f, .6);
  sink("#b1", %.3f); erase("c1", %.3f);
''' % (t_klod - 0.45, t_prac, t_koly - 0.2, t_nich - 0.1, e_pyshu - 0.2, e_pyshu - 0.2))
g.sfx("pop", t_klod - 0.4); g.sfx("click-soft", t_nich)
BLACKOUT.append((S(u"Мій", 0.8) - 0.03, S(u"на", 1.8) - 0.03))      # the card says «Claude · працює»

# 2 · BEHIND — «рутини» -------------------------------------------------------
t_rut, e_rut = S(u"рутини.", 5.92), E(u"рутини.", 5.92)
# 240 px, x-height ≈ y 592–707: her hair (top ≈ 680–700 on the word) covers ~25 % of it
B.append(u'        <div id="bw" class="big hid" style="top:530px; font-size:240px">рутини</div>')
g.matte("rut", round(t_rut - 0.75, 3), round(e_rut - t_rut + 1.1, 3))
js(u'''
  rise("#bw", %.3f); sink("#bw", %.3f);
''' % (t_rut - 0.6, e_rut - 0.3))
g.sfx("whoosh-short", t_rut - 0.55)
BLACKOUT.append((t_rut - 0.03, e_rut))                              # the big word says it

# 3 · HALF — every few hours: chats -> checked -> tasks for me and the team -----
h0, h1 = round(e_rut - 0.15, 3), E(u"команді.", 14.41)
HALF.append((h0, h1))
P.append(u'        <span id="pig" class="hid" style="position:absolute; left:642px; top:322px; color:#7A1424">%s</span>'
         % mark("instagram", 60))
P.append(u'        <span id="ptg" class="hid" style="position:absolute; left:642px; top:457px; color:#7A1424">%s</span>'
         % mark("telegram", 60))
t_kozh, t_kil, t_god = S(u"кожні", 7.94), S(u"кілька", 8.1), S(u"годин", 8.42)
t_perev, t_chat = S(u"перевіряє", 8.92), S(u"чати", 9.66)
t_ig, t_tg = S(u"інстаграмі", 10.0), S(u"телеграмі,", 10.5)
t_nich2, t_prop = S(u"нічого", 11.29), S(u"пропустила,", 11.73)
t_sam, t_stv, t_zad = S(u"сам", 12.61), S(u"створює", 12.85), S(u"задачі", 13.51)
t_meni, t_kom = S(u"мені", 13.99), S(u"команді.", 14.41)
js(u'''
  sketch("ck", "skP"); ell("ck", 220, 410, 200, 200, {seed: 3});
  draw("ck", %.3f, .6);
  sketch("ckt", "skP"); ln("ckt", 220, 320, 220, 336, {seed: 4}); ln("ckt", 310, 410, 294, 410, {seed: 5});
  ln("ckt", 220, 500, 220, 484, {seed: 6}); ln("ckt", 130, 410, 146, 410, {seed: 7});
  draw("ckt", %.3f, .2);
  sketch("mh", "skP"); ln("mh", 220, 410, 220, 340, {seed: 8, strokeWidth: 5});
  sketch("hh", "skP"); ln("hh", 220, 410, 220, 366, {seed: 9, strokeWidth: 7});
  gsap.set("#sk-hh", {rotation: 120, svgOrigin: "220 410"});
  draw("mh", %.3f, .3); draw("hh", %.3f, .25);
  tl.to("#sk-hh", {rotation: 210, svgOrigin: "220 410", duration: .22, ease: POP}, %.3f);
  tl.to("#sk-hh", {rotation: 300, svgOrigin: "220 410", duration: .22, ease: POP}, %.3f);
  tl.to("#sk-hh", {rotation: 390, svgOrigin: "220 410", duration: .22, ease: POP}, %.3f);
  sketch("ckl", "skP"); label("ckl", 220, 572, "кожні кілька", {size: 42}); label("ckl", 220, 618, "годин", {size: 42});
  draw("ckl", %.3f);

  sketch("a1", "skP"); arrow("a1", 340, 405, 598, 392, {seed: 11, bend: .1});
  draw("a1", %.3f, .5);
  sketch("ch1", "skP"); box("ch1", 620, 300, 260, 105, {seed: 13, r: 30});
  ln("ch1", 722, 337, 852, 337, {seed: 14, strokeWidth: 4}); ln("ch1", 722, 372, 812, 372, {seed: 15, strokeWidth: 4});
  draw("ch1", %.3f, .45);
  sketch("ch2", "skP"); box("ch2", 620, 435, 260, 105, {seed: 16, r: 30});
  ln("ch2", 722, 472, 852, 472, {seed: 17, strokeWidth: 4}); ln("ch2", 722, 507, 800, 507, {seed: 18, strokeWidth: 4});
  draw("ch2", %.3f, .45);
  pop("#pig", %.3f); pop("#ptg", %.3f);

  sketch("ok1", "skP"); tick("ok1", 902, 352, {stroke: "#7A1424", strokeWidth: 6, seed: 19});
  sketch("ok2", "skP"); tick("ok2", 902, 487, {stroke: "#7A1424", strokeWidth: 6, seed: 21});
  draw("ok1", %.3f, .35); draw("ok2", %.3f, .35);

  sketch("a2", "skP"); arrow("a2", 775, 560, 684, 722, {seed: 25, bend: -.18});
  draw("a2", %.3f, .5);
  sketch("tk", "skP"); box("tk", 290, 645, 372, 182, {seed: 27, r: 28});
  draw("tk", %.3f, .55);
  sketch("tkl", "skP"); label("tkl", 190, 756, "задачі", {size: 52});
  draw("tkl", %.3f);
  sketch("tr", "skP");
  [690, 740, 790].forEach(function (y, i) {
    box("tr", 312, y - 15, 30, 30, {r: 8, seed: 41 + i, strokeWidth: 4});
    ln("tr", 358, y, 488, y, {seed: 51 + i, strokeWidth: 4});
  });
  draw("tr", %.3f, .25);
  sketch("as1", "skP"); label("as1", 504, 704, "мені", {size: 40, anchor: "start", color: "#7A1424"});
  label("as1", 504, 804, "мені", {size: 40, anchor: "start", color: "#7A1424"});
  sketch("as2", "skP"); label("as2", 504, 754, "команді", {size: 40, anchor: "start", color: "#7A1424"});
  draw("as1", %.3f); draw("as2", %.3f);
  ["ck", "ckt", "mh", "hh", "ckl", "a1", "ch1", "ch2", "ok1", "ok2", "a2", "tk", "tkl", "tr", "as1", "as2"]
    .forEach(function (n) { erase(n, %.3f); });
  out("#pig, #ptg", %.3f);
''' % (t_kozh - 0.5, t_kozh - 0.05, t_kozh + 0.05, t_kozh + 0.1, t_kil, t_god, t_god + 0.3, t_god - 0.1,
       t_perev - 0.15, t_chat - 0.45, t_ig + 0.05, t_ig, t_tg, t_nich2 - 0.05, t_prop,
       t_sam - 0.35, t_stv - 0.05, t_zad - 0.1, t_zad - 0.25, t_meni - 0.05, t_kom - 0.05, h1, h1))
g.sfx("whoosh-short", h0); g.sfx("click-soft", t_kil); g.sfx("pop", t_ig); g.sfx("click-soft", t_nich2)
g.sfx("pop", t_stv); g.sfx("whoosh-short", h1)
BLACKOUT.append((t_zad - 0.03, h1))                                 # the labels write «задачі · мені · команді»

# 4 · ABOVE — a weekly report on the content, and next week's ideas -----------
t_rut2, t_raz = S(u"рутина,", 15.4), S(u"раз", 15.9)
t_zvit, t_odr, t_idei = S(u"звіт", 16.82), S(u"одразу", 17.95), S(u"ідеї", 18.26)
t_nast, e_tyzh = S(u"наступний", 18.9), E(u"тиждень.", 19.22)
bars = [40, 62, 50, 84, 70, 92, 100]
bulb = (u'<svg width="30" height="40" viewBox="0 0 30 40" style="flex:none"><path d="M15 3 a11.5 11.5 0 0 1 7 20.6 '
        u'V28 H8 V23.6 A11.5 11.5 0 0 1 15 3 Z" fill="#7A1424"/><rect x="9" y="31" width="12" height="5" rx="2.5" '
        u'fill="#7A1424"/></svg>')
F.append(u'''
        <div id="b4a" class="card hid" style="left:96px; top:300px; width:430px; padding:30px 32px;">
          <span class="lbl" style="margin-bottom:12px">Рутина</span>
          <div style="display:flex; margin-bottom:16px">
            <span class="chip hid" id="b4w" style="font-size:28px; padding:8px 16px; gap:10px; white-space:nowrap"><i></i>раз на тиждень</span>
          </div>
          <span class="ttl hid" id="b4t" style="font-size:40px">Звіт по контенту</span>
          <div style="display:flex; align-items:flex-end; gap:14px; height:120px; margin-top:22px">%s</div>
        </div>
        <div id="b4b" class="card hid" style="left:554px; top:300px; width:430px; padding:30px 32px;">
          <span class="lbl" style="margin-bottom:12px">Одразу</span>
          <div style="display:flex; margin-bottom:16px">
            <span class="chip hid" id="b4n" style="font-size:28px; padding:8px 16px; gap:10px; white-space:nowrap"><i></i>наступний тиждень</span>
          </div>
          <span class="ttl" style="font-size:40px">Ідеї</span>
          %s
        </div>''' % (
    u"".join(u'<span class="bar" style="flex:1; height:%d%%; border-radius:10px; background:%s; display:block"></span>'
             % (h, "#7A1424" if i == len(bars) - 1 else "#F2C7CA") for i, h in enumerate(bars)),
    u"".join(u'<div class="row hid" id="b4i%d" style="margin-top:%dpx">%s<span class="line" style="flex:none; width:%dpx"></span></div>'
             % (i, 18 if i == 0 else 12, bulb, w) for i, w in enumerate((290, 230, 260)))))
js(u'''
  rise("#b4a", %.3f); pop("#b4w", %.3f, .5);
  rise("#b4t", %.3f, 24);
  tl.fromTo("#b4a .bar", {scaleY: 0, transformOrigin: "50%% 100%%"}, X({scaleY: 1, duration: .5, ease: RISE, stagger: .07}), %.3f);
  rise("#b4b", %.3f);
  pop("#b4i0", %.3f, .45); pop("#b4i1", %.3f, .45); pop("#b4i2", %.3f, .45);
  pop("#b4n", %.3f, .5);
  sink("#b4a, #b4b", %.3f);
''' % (t_rut2 - 0.25, t_raz, t_zvit - 0.2, t_zvit, t_odr - 0.3, t_idei, t_idei + 0.15, t_idei + 0.3,
       t_nast - 0.05, e_tyzh - 0.15))
g.sfx("pop", t_rut2 - 0.2); g.sfx("pop", t_odr - 0.25)
BLACKOUT.append((t_zvit - 0.03, S(u"і", 17.8) - 0.03))              # the card title says it

# 5 · ABOVE — the alarm rings; everything is already ticked --------------------
t_tob, t_prok = S(u"Тобто", 19.9), S(u"прокидаюсь,", 20.24)
t_a, t_vzhe, t_vse, t_lezh = S(u"а", 20.82), S(u"вже", 21.12), S(u"все", 21.38), S(u"лежить", 21.6)
e_got = E(u"готове.", 21.9)
rows5 = [u"задачі мені і команді", u"звіт по контенту", u"ідеї на тиждень"]
F.append(u'''
        <div id="b5" class="card hid" style="left:420px; top:322px; width:564px; padding:30px 36px;">
          <span class="lbl">Вже готове</span>
          %s
        </div>''' % u"".join(u'<div class="row" style="margin-top:%dpx"><span class="check" id="b5k%d"></span>'
                              u'<span style="font-size:34px; font-weight:500">%s</span></div>'
                              % (0 if i == 0 else 16, i, esc(t)) for i, t in enumerate(rows5)))
js(u'''
  sketch("al", "skF"); bell("al", 255, 440, 95, -132, {seed: 62}); bell("al", 255, 440, 95, -48, {seed: 63});
  ell("al", 255, 440, 190, 190, {seed: 61});
  ln("al", 190, 524, 168, 556, {seed: 64}); ln("al", 320, 524, 342, 556, {seed: 65});
  ln("al", 255, 440, 255, 374, {seed: 66, strokeWidth: 5}); ln("al", 255, 440, 222, 478, {seed: 67, strokeWidth: 6});
  draw("al", %.3f, .3);
  tl.to("#sk-al", {rotation: 7, svgOrigin: "255 440", duration: .06, yoyo: true, repeat: 7, ease: "none"}, %.3f);
  sketch("rg", "skF"); ln("rg", 132, 340, 110, 322, {seed: 68}); ln("rg", 124, 374, 100, 374, {seed: 69});
  ln("rg", 378, 340, 400, 322, {seed: 70}); ln("rg", 386, 374, 410, 374, {seed: 71});
  draw("rg", %.3f, .15);
  rise("#b5", %.3f);
  tl.set("#b5k0", {className: "check on"}, %.3f); pop("#b5k0", %.3f, .45);
  tl.set("#b5k1", {className: "check on"}, %.3f); pop("#b5k1", %.3f, .45);
  tl.set("#b5k2", {className: "check on"}, %.3f); pop("#b5k2", %.3f, .45);
  sink("#b5", %.3f); erase("al", %.3f); erase("rg", %.3f);
''' % (t_tob - 0.05, t_prok, t_prok, t_a - 0.45, t_vzhe, t_vzhe, t_vse, t_vse, t_lezh, t_lezh,
       e_got - 0.15, e_got - 0.15, e_got - 0.15))
g.sfx("notification", t_prok); g.sfx("click-soft", t_vse)

# 6 · ABOVE — the cloud: Claude and its actions --------------------------------
t_klod2, t_bag, t_diy = S(u"Клод", 24.05), S(u"багато", 24.77), S(u"дій", 25.19)
t_vyk, t_hm, e_hm = S(u"виконується", 25.37), S(u"хмарі.", 26.09), E(u"хмарі.", 26.09)
F.append(u'''
        <div id="b6p" class="pill light hid" style="left:412px; top:392px; font-size:40px; padding:18px 36px; gap:14px">
          <span style="color:#7A1424; display:flex">%s</span>Claude</div>
        <div style="position:absolute; left:0; top:500px; width:1080px; display:flex; justify-content:center; gap:12px">
          <span class="chip hid" id="b6a" style="font-size:30px; padding:8px 18px; gap:10px"><i></i>чати</span>
          <span class="chip hid" id="b6b" style="font-size:30px; padding:8px 18px; gap:10px"><i></i>задачі</span>
          <span class="chip hid" id="b6c" style="font-size:30px; padding:8px 18px; gap:10px"><i></i>звіти</span>
        </div>''' % mark("claude", 44))
js(u'''
  pop("#b6p", %.3f);
  pop("#b6a", %.3f, .45); pop("#b6b", %.3f, .45); pop("#b6c", %.3f, .45);
  sketch("cl", "skF"); cloud("cl", 540, 460, 1.2, {seed: 73});
  draw("cl", %.3f, .9);
  sink("#b6p, #b6a, #b6b, #b6c", %.3f); erase("cl", %.3f);
''' % (t_klod2 - 0.1, t_bag, t_diy - 0.15, t_diy + 0.05, t_vyk - 0.15, e_hm - 0.3, e_hm - 0.3))
g.sfx("pop", t_klod2 - 0.1)

# 7 · HALF — the laptop closes and sleeps; the cloud works any time ------------
h2, h3 = round(e_hm - 0.05, 3), round(S(u"тому", 34.14) - 0.2, 3)
HALF.append((h2, h3))
P.append(u'        <span id="pcl" class="hid" style="position:absolute; left:760px; top:368px; color:#7A1424">%s</span>'
         % mark("claude", 60))
t_ozn, t_trym, t_vidk = S(u"означає,", 27.15), S(u"тримати", 28.53), S(u"відкритим.", 29.39)
t_vin, t_bud, t_sam2 = S(u"Він", 29.88), S(u"будь-який", 31.66), S(u"сам.", 32.42)
t_napr, t_mont = S(u"Наприклад,", 32.9), S(u"монтаж", 33.57)
js(u'''
  sketch("cl2", "skP"); cloud("cl2", 790, 398, .65, {seed: 75});
  draw("cl2", %.3f, .8); pop("#pcl", %.3f);
  sketch("lp", "skP"); box("lp", 125, 560, 300, 190, {seed: 77, r: 18});
  box("lp", 150, 584, 250, 142, {seed: 78, r: 10, strokeWidth: 3});
  draw("lp", %.3f, .45);
  sketch("lb", "skP"); box("lb", 95, 752, 360, 30, {seed: 79, r: 12});
  draw("lb", %.3f, .45);
  tl.to("#sk-lp", {scaleY: .05, svgOrigin: "275 752", duration: .4, ease: "power2.in"}, %.3f);
  sketch("zz", "skP"); label("zz", 300, 700, "z z z", {size: 56});
  draw("zz", %.3f);
  sketch("ck2", "skP"); ell("ck2", 250, 395, 170, 170, {seed: 81});
  ln("ck2", 250, 318, 250, 332, {seed: 82}); ln("ck2", 327, 395, 313, 395, {seed: 83});
  ln("ck2", 250, 472, 250, 458, {seed: 84}); ln("ck2", 173, 395, 187, 395, {seed: 85});
  draw("ck2", %.3f, .3);
  sketch("mh2", "skP"); ln("mh2", 250, 395, 250, 335, {seed: 86, strokeWidth: 5});
  sketch("hh2", "skP"); ln("hh2", 250, 395, 285, 395, {seed: 87, strokeWidth: 7});
  draw("mh2", %.3f, .25); draw("hh2", %.3f, .25);
  tl.to("#sk-mh2", {rotation: 720, svgOrigin: "250 395", duration: .85, ease: "power2.inOut"}, %.3f);
  tl.to("#sk-hh2", {rotation: 60, svgOrigin: "250 395", duration: .85, ease: "power2.inOut"}, %.3f);
  sketch("a3", "skP"); arrow("a3", 640, 470, 800, 690, {seed: 89, bend: -.2});
  draw("a3", %.3f, .5);
  sketch("ph", "skP"); box("ph", 822, 590, 130, 215, {seed: 91, r: 24});
  poly("ph", [[868, 660], [868, 738], [920, 699], [868, 660]], {seed: 92});
  ln("ph", 866, 784, 908, 784, {seed: 93});
  draw("ph", %.3f, .4);
  sketch("phl", "skP"); label("phl", 800, 815, "монтаж рілсів", {size: 40, anchor: "end"});
  draw("phl", %.3f);
  ["cl2", "lp", "lb", "zz", "ck2", "mh2", "hh2", "a3", "ph", "phl"].forEach(function (n) { erase(n, %.3f); });
  out("#pcl", %.3f);
''' % (t_ozn - 0.4, t_ozn + 0.3, t_trym - 0.25, t_trym + 0.1, t_vidk + 0.05, t_vin - 0.1,
       t_bud - 0.75, t_bud - 0.35, t_bud - 0.3, t_bud, t_bud, t_napr - 0.05, t_mont - 0.4, t_mont, h3, h3))
g.sfx("whoosh-short", h2); g.sfx("pop", t_mont - 0.1); g.sfx("whoosh-short", h3)
BLACKOUT.append((t_mont - 0.03, E(u"рілсів.", 33.8)))               # the label says «монтаж рілсів»

# 8 · ABOVE — CTA ---------------------------------------------------------------
t_taki, t_to, t_pid = S(u"такі", 35.54), S(u"то", 36.42), S(u"підпишись.", 37.0)
F.append(u'''
        <div style="position:absolute; left:0; top:300px; width:1080px; display:flex; justify-content:center; gap:14px">
          <span class="chip hid" id="b8a" style="font-size:32px; padding:10px 20px"><i></i>рутини</span>
          <span class="chip hid" id="b8b" style="font-size:32px; padding:10px 20px"><i></i>задачі з чатів</span>
          <span class="chip hid" id="b8c" style="font-size:32px; padding:10px 20px"><i></i>звіти</span>
          <span class="chip hid" id="b8d" style="font-size:32px; padding:10px 20px"><i></i>хмара</span>
        </div>
        <div style="position:absolute; left:0; top:404px; width:1080px; display:flex; justify-content:center">
          <div id="b8p" class="pill hid" style="position:relative">Підпишись</div>
        </div>''')
js(u'''
  pop("#b8a", %.3f, .45); pop("#b8b", %.3f, .45); pop("#b8c", %.3f, .45); pop("#b8d", %.3f, .45);
  pop("#b8p", %.3f, .6);
  // the pointer goes DOWN, never up at the pill (her review of 41): her CTA is
  // «підпишись», so it heads for the follow button by her username, lower left
  sketch("pt", "skF"); arrow("pt", 330, 560, 190, 840, {seed: 97, bend: -.18, strokeWidth: 5});
  draw("pt", %.3f, .5);
''' % (t_taki - 0.3, t_taki - 0.15, t_taki, t_taki + 0.15, t_to, t_to + 0.4))
g.sfx("pop", t_taki - 0.3); g.sfx("pop", t_to)
BLACKOUT.append((t_pid - 0.05, DUR))     # the pill says it

# ---------------------------------------------------------------- mattes for the half screens
for i, (a, b) in enumerate(HALF):
    g.matte("half%d" % (i + 1), round(a - 0.1, 3), round(b - a + 1.2, 3))
    js("  half(%.3f, %.3f);" % (a, b))
    PLACE.append((a + 0.4, b + 0.2, "bottom", 980))


def main():
    print(" ".join(u"%s/%.1f" % (c["w"], c["s"]) for c in CAPS))
    chunks = g.chunks(CAPS, place=PLACE)
    doc = g.document(title=u"Reel 50 — Поки я сплю", plate="assets/base.mp4",
                     behind="\n".join(B), panel="\n".join(P), front="\n".join(F), cover="\n".join(C),
                     js="\n".join(J), chunks=chunks, blackout=BLACKOUT)
    g.write(HERE, doc)
    print("index.html  %d caption chunks, %d sfx cues, %d mattes" % (len(chunks), len(g.cues), len(g.mattes)))


main()
