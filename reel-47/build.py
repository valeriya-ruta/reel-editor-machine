# -*- coding: utf-8 -*-
"""Reel 47 — «Навіщо Notion». Posts 2026-10-23.

Google style + Excalidraw (STYLE.md §00), the reel-41 skeleton.

The one object is **the point of reference**: a place that is not Claude's
memory, where you and Claude both look. The reel builds up to it — Claude's
memory drawn as a database that keeps stale things, the content that changes
under it, the statuses that are a mess — lands it full screen, then shows the
two real ones: a doc for slow things (strategy), Notion for fast things, which
is there for Claude, not for you.

  above   «Claude»: four skills tick on; «− мінус» lands on the card
  half    памʼять Клода = база даних → Клод; контент crossed out, стратегія /
          теми rewritten
  behind  «100%» on «він 100% згадає»
  above   «Памʼять Клода» recalls стратегія (неактуальна), тема (закрита)
  above   the statuses, in a heap, ringed in red — the quip
  above   «Система клієнта»: Claude + an extra Notion; клієнтка doesn't use it ✗,
          no link ✗
  full    «point of reference»: memory crossed out, the independent place,
          ти and Клод both look into it — актуальна інформація
  above   the strategy doc: Claude reads it, it gets updated
  above   Notion for the fast things: контент-план / ідеї / задачі; free,
          simple; you don't even have to look (an eye, struck)
  half    not for you ✗, for Claude ✓ → a board by stage, старе apart from нове
  above   CTA — зекономити, AI-система самостійно, лайфхак + Notion, «Підпишись»

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

NN = "47"
CUT = json.load(io.open(os.path.join(ROOT, "work", "r" + NN, "cut.json"), encoding="utf-8"))
DUR = 87.483           # (2625 plate frames - 0.5) / 30
g = G(dur=DUR, reel=NN)

# whisper's spelling of what she plainly said -> her word (re-heard on the take)
FIX = {
    u"мінос,": u"мінус,", (u"ай", 8.1): None, u"ай систему.": u"AI-систему.",
    u"Не": u"не", u"нас": u"нас.", (u"у", 12.5): u"У",
    u"інформацію,": u"інформацію.", (u"і", 15.1): u"І",
    (u"Клода,", 22.2): u"Клода, то", (u"що", 24.3): u"щось", u"й старе:": u"старе:",
    u"і на": u"неактуальна,", u"актуальне,": None,
    u"контенту": u"контенту —", u"безпросвєтна": u"безпросвітна",
    u"посилання": u"посилання.", u"Це Місце,": u"Це місце,", u"незалежним": u"незалежним.",
    (u"і", 49.2): u"І", u"КлодДок,": u"Клод-док,", u"оновлюється:": u"оновлюється.",
    u"стратегією": u"стратегією:", u"треба.": u"треба", (u"Я", 73.0): u"я",
    u"Якщо": u"якщо", u"AI": u"AI-систему", (u"систему", 83.2): None,
    u"самостійно": u"самостійно,", u"обов'язково": u"обовʼязково",
}
CAPS = load_caps(NN, FIX)
# «Клода, то» came out as one token; «то» starts its own caption phrase (words.json: «то» 22.6)
for _i, _c in enumerate(CAPS):
    if _c["w"] == u"Клода, то":
        CAPS[_i:_i + 1] = [dict(_c, w=u"Клода,", e=0.57 + _c["s"] - 0.02), dict(_c, w=u"то", s=round(_c["s"] + 0.45, 3))]
        break
W = Words(CAPS)
S, E = W.s, W.e

# ---------------------------------------------------------------- the beats
B, P, F, C, J = [], [], [], [], []     # behind / panel / front / cover html, js
BLACKOUT = []
PLACE = []                             # caption placement over the half screens
HALF = []


def js(s):
    J.append(s)


# sketch helpers on top of gstyle's: a database cylinder, a tick, an X, an eye
js(u'''
  function cyl(name, cx, top, w, h, o) {
    var s = SK[name], rx = w / 2;
    ell(name, cx, top, w, 56, o);
    ln(name, cx - rx, top, cx - rx, top + h, o); ln(name, cx + rx, top, cx + rx, top + h, o);
    _add(s, s.rc.path("M" + (cx - rx) + " " + (top + h) + " A " + rx + " 28 0 0 0 " + (cx + rx) + " " + (top + h),
                      opt(o, ((o && o.seed) || 61) + 3)));
  }
  function tick(name, x, y, o) { var s = SK[name];
    var k = (o && o.k) || 1;
    _add(s, s.rc.linearPath([[x - 34 * k, y], [x - 8 * k, y + 28 * k], [x + 40 * k, y - 34 * k]], opt(o, (o && o.seed) || 71))); }
  function cross(name, x1, y1, x2, y2, o) {
    var o2 = {}; for (var k in (o || {})) o2[k] = o[k]; o2.seed = ((o && o.seed) || 81) + 2;
    ln(name, x1, y1, x2, y2, o); ln(name, x2, y1, x1, y2, o2); }
  function eye(name, x, y, o) { var s = SK[name];
    _add(s, s.rc.curve([[x - 100, y], [x, y - 62], [x + 100, y]], opt(o, 91)));
    _add(s, s.rc.curve([[x - 100, y], [x, y + 62], [x + 100, y]], opt(o, 93)));
    ell(name, x, y, 58, 58, {seed: 95, fill: "#7A1424", fillStyle: "solid"}); }
''')

XMARK = (u'<svg id="b6x%d" class="hid" width="44" height="44" viewBox="0 0 44 44" style="position:absolute; left:-3px; top:-3px">'
         u'<path d="M9 8 C17 17 26 26 36 36 M35 8 C27 17 17 27 8 36" fill="none" stroke="#7A1424" stroke-width="7" '
         u'stroke-linecap="round"/></svg>')

# 1 · ABOVE — Claude can do everything … but one big minus --------------------
t_kl, t_diz, t_mon = S(u"Клод", 0.39), S(u"дизайнити,", 1.65), S(u"монтувати,", 2.37)
t_pys, t_an = S(u"писати,", 2.95), S(u"аналізувати.", 3.49)
t_ale, t_min = S(u"Але в", 4.53), S(u"мінус,", 5.87)
h0 = S(u"Його", 9.21) - 0.15
SKILLS = [(u"дизайнити", t_diz), (u"монтувати", t_mon), (u"писати", t_pys), (u"аналізувати", t_an)]
F.append(u'''
        <div id="b1" class="card hid" style="left:120px; top:318px; width:840px; padding:34px 40px 40px;">
          <div class="row" style="gap:20px; margin-bottom:26px; color:#7A1424">%s
            <span class="ttl">Claude</span></div>
          <div class="chips" id="b1cs">%s</div>
        </div>
        <div id="b1m" class="pill hid" style="left:600px; top:282px; font-size:52px; padding:22px 46px;
             transform: rotate(-4deg)"><b style="font-weight:700; font-size:64px; line-height:.6">−</b>мінус</div>'''
         % (mark("claude", 60), u"".join(u'<span class="chip on hid" id="b1c%d"><i></i>%s</span>' % (i, esc(w))
                                         for i, (w, _) in enumerate(SKILLS))))
js(u'''
  rise("#b1", %.3f);
  %s
  tl.to("#b1cs", {opacity: .38, duration: .4}, %.3f);
  pop("#b1m", %.3f, .6);
  sink("#b1, #b1m", %.3f);
''' % (t_kl - 0.25, " ".join('pop("#b1c%d", %.3f, .45);' % (i, t) for i, (_, t) in enumerate(SKILLS)),
       t_ale, t_min - 0.1, h0 - 0.3))
g.sfx("pop", t_kl - 0.2); g.sfx("click-soft", t_diz); g.sfx("click-soft", t_an)
g.sfx("pop", t_min - 0.1)
BLACKOUT.append((t_diz - 0.05, E(u"аналізувати.", 3.49) + 0.05))      # the chips say it

# 2 · HALF — memory is a database; content changes under it -------------------
h1 = S(u"І", 19.77) + 0.15
HALF.append((h0, h1))
P.append(u'<svg class="sk" id="skP" width="1080" height="1240" viewBox="0 0 1080 1240"></svg>')
t_pam, t_nel = S(u"памʼять", 9.45), S(u"нелогічна.", 10.46)
t_baza, t_bere = S(u"база", 12.99), S(u"бере", 13.91)
t_kont, t_zav = S(u"контент", 15.28), S(u"завтра", 17.23)
t_str, t_zm = S(u"стратегія", 17.91), S(u"змінюється,", 18.32)
t_temy = S(u"теми", 19.04)
js(u'''
  sketch("p1", "skP"); label("p1", 280, 352, "памʼять Клода", {size: 54});
  under("p1", 110, 372, 450, {seed: 3});
  draw("p1", %.3f, .5);
  sketch("p2", "skP"); label("p2", 500, 368, "?!", {size: 84, color: "#7A1424"});
  draw("p2", %.3f);
  sketch("p3", "skP"); cyl("p3", 280, 440, 300, 150, {seed: 5});
  label("p3", 280, 548, "база даних", {size: 48});
  draw("p3", %.3f, .55);
  sketch("p4", "skP"); arrow("p4", 280, 640, 280, 715, {seed: 9, bend: 0});
  label("p4", 280, 775, "Клод", {size: 52});
  draw("p4", %.3f, .45);
  sketch("p5", "skP"); box("p5", 610, 318, 350, 170, {seed: 11, fill: true});
  label("p5", 785, 420, "контент", {size: 54});
  draw("p5", %.3f, .6);
  sketch("p6", "skP"); cross("p6", 615, 312, 955, 494, {stroke: "#7A1424", strokeWidth: 6, seed: 13});
  draw("p6", %.3f, .35);
  sketch("p7", "skP"); label("p7", 700, 600, "стратегія", {size: 48});
  draw("p7", %.3f);
  sketch("p8", "skP"); ln("p8", 600, 588, 805, 584, {stroke: "#7A1424", strokeWidth: 5, seed: 15});
  arrow("p8", 818, 590, 870, 590, {seed: 17, bend: 0}); label("p8", 930, 603, "нова", {size: 48, color: "#7A1424"});
  draw("p8", %.3f, .35);
  sketch("p9", "skP"); label("p9", 700, 712, "теми", {size: 48});
  ln("p9", 640, 698, 765, 696, {stroke: "#7A1424", strokeWidth: 5, seed: 19});
  arrow("p9", 818, 702, 870, 702, {seed: 21, bend: 0}); label("p9", 930, 715, "нові", {size: 48, color: "#7A1424"});
  draw("p9", %.3f, .3);
  ["p1","p2","p3","p4","p5","p6","p7","p8","p9"].forEach(function (n) { erase(n, %.3f); });
''' % (t_pam - 0.1, t_nel, t_baza - 0.45, t_bere - 0.2, t_kont - 0.45, t_zav, t_str - 0.05, t_zm,
       t_temy - 0.05, h1))
g.sfx("whoosh-short", h0); g.sfx("whoosh-short", h1)
for t in (t_pam, t_baza, t_kont, t_zav):
    g.sfx("click-soft", t)

# 3 · BEHIND — «100%» -----------------------------------------------------------
t_100, t_star = S(u"100%", 22.88), E(u"старе:", 24.36)
m0, m1 = t_100 - 0.3, t_star + 0.3
B.append(u'<div id="bw1" class="big hid" style="top:500px; font-size:300px">100%</div>')
g.matte("pct", round(m0, 3), round(m1 - m0 + 0.45, 3))
js(u'''
  rise("#bw1", %.3f, 80);
  sink("#bw1", %.3f);
''' % (t_100 - 0.25, m1 - 0.35))
g.sfx("whoosh-short", t_100 - 0.2)

# 4 · ABOVE — Claude's memory recalls the stale things -------------------------
t_strg, t_neak = S(u"стратегію,", 25.34), S(u"неактуальна,", 26.1)
t_temu, t_zakr = S(u"тему,", 27.09), S(u"закрили.", 27.64)
F.append(u'''
        <div id="b4" class="card hid" style="left:120px; top:318px; width:840px; padding:34px 40px 40px;">
          <div class="row" style="gap:18px; margin-bottom:26px; color:#7A1424">%s
            <span class="ttl" style="font-size:48px">Памʼять Клода</span></div>
          <div class="row" style="margin-bottom:18px">
            <span class="chip hid" id="b4a"><i></i>стратегія</span>
            <span class="pill hid" id="b4at" style="position:relative; font-size:36px; padding:14px 30px">неактуальна</span>
          </div>
          <div class="row">
            <span class="chip hid" id="b4b"><i></i>тема</span>
            <span class="pill hid" id="b4bt" style="position:relative; font-size:36px; padding:14px 30px">закрита</span>
          </div>
        </div>''' % mark("claude", 48))
js(u'''
  rise("#b4", %.3f);
  pop("#b4a", %.3f); tl.to("#b4a", {opacity: .45, duration: .3}, %.3f); pop("#b4at", %.3f);
  pop("#b4b", %.3f); tl.to("#b4b", {opacity: .45, duration: .3}, %.3f); pop("#b4bt", %.3f);
  sink("#b4", %.3f);
''' % (t_strg - 0.45, t_strg, t_neak, t_neak, t_temu, t_zakr, t_zakr, E(u"закрили.", 27.64) + 0.12))
g.sfx("pop", t_strg - 0.4); g.sfx("click-soft", t_zakr)
BLACKOUT.append((t_strg - 0.3, E(u"закрили.", 27.64) + 0.05))

# 5 · ABOVE — the statuses: a heap, ringed in red -----------------------------
t_stat, t_bez = S(u"статуси", 28.62), S(u"безпросвітна", 30.4)
t_tomu = S(u"Тому", 31.91)
HEAP = [(u"ідея", 170, 330, -11), (u"в роботі", 420, 300, 7), (u"на апруві", 640, 352, -5),
        (u"знято", 250, 470, 9), (u"готово", 520, 450, -14), (u"опубліковано", 600, 540, 4),
        (u"сценарій", 140, 575, -4)]
F.append(u"".join(u'<span class="chip hid" id="b5c%d" style="position:absolute; left:%dpx; top:%dpx; '
                  u'transform: rotate(%ddeg); font-size:40px"><i></i>%s</span>' % (i, x, y, r, esc(w))
                  for i, (w, x, y, r) in enumerate(HEAP)))
js(u'''
  %s
  sketch("r5", "skF"); ell("r5", 540, 482, 890, 396, {stroke: "#7A1424", strokeWidth: 5, roughness: 2.8, seed: 31});
  ell("r5", 548, 478, 850, 370, {stroke: "#7A1424", strokeWidth: 4, roughness: 3, seed: 33});
  draw("r5", %.3f, .45);
  tl.to("%s", {autoAlpha: 0, y: 60, duration: .35, ease: "power2.in", stagger: .03}, %.3f);
  erase("r5", %.3f);
''' % (" ".join('pop("#b5c%d", %.3f, .45);' % (i, t_stat - 0.1 + i * 0.13) for i in range(len(HEAP))),
       t_bez - 0.2, ", ".join("#b5c%d" % i for i in range(len(HEAP))), t_tomu - 0.4, t_tomu - 0.3))
g.sfx("pop", t_stat - 0.1); g.sfx("whoosh-short", t_bez - 0.2)

# 6 · ABOVE — the client's system: Claude + an extra Notion she never opens ----
t_nal, t_sys = S(u"налаштовую", 32.91), S(u"систему", 33.43)
t_dod, t_not = S(u"додатковий", 35.49), S(u"Notion.", 36.39)
t_kli, t_kor = S(u"клієнтка", 37.77), S(u"користується,", 39.41)
t_nav2, t_pos = S(u"навіть", 40.25), S(u"посилання.", 41.35)
F.append(u'''
        <div id="b6" class="card hid" style="left:120px; top:300px; width:840px; padding:32px 40px 36px;">
          <span class="lbl">Система клієнта</span>
          <div class="chips">
            <span class="chip hid" id="b6a" style="color:#7A1424">%s<span style="color:#241919">Claude</span></span>
            <span style="position:relative; display:inline-flex">
              <span class="chip hid" id="b6s" style="border-style:dashed; color:#574142">+ додатковий</span>
              <span class="chip on hid" id="b6n" style="position:absolute; left:0; top:0; white-space:nowrap">%s Notion</span></span>
          </div>
          <div style="height:2px; background:#EFE3E3; margin:26px 0 22px"></div>
          <div class="row hid" id="b6r1"><span class="check">%s</span>
            <span style="font-size:40px; font-weight:500">клієнтка користується</span></div>
          <div class="row hid" id="b6r2" style="margin-top:16px"><span class="check">%s</span>
            <span style="font-size:40px; font-weight:500">має посилання</span></div>
        </div>''' % (mark("claude", 36), mark("notion", 36), XMARK % 1, XMARK % 2))
js(u'''
  rise("#b6", %.3f);
  pop("#b6a", %.3f);
  pop("#b6s", %.3f);
  tl.to("#b6s", {autoAlpha: 0, duration: .2}, %.3f); pop("#b6n", %.3f);
  rise("#b6r1", %.3f, 30); rise("#b6r2", %.3f, 30);
  pop("#b6x1", %.3f, .4);
  pop("#b6x2", %.3f, .4);
  sink("#b6", %.3f);
''' % (t_nal - 0.3, t_sys, t_dod, t_not - 0.05, t_not - 0.05, t_kli - 0.1, t_nav2 - 0.1,
       t_kor, t_pos, S(u"Тому", 42.17) - 0.15))
g.sfx("pop", t_nal - 0.25); g.sfx("pop", t_not - 0.05); g.sfx("click-soft", t_pos)

# 7 · FULL — the point of reference -------------------------------------------
c0, c1 = S(u"називаю,", 43.88) - 0.15, S(u"На", 52.86) - 0.3
t_poi, t_mis = S(u"point", 44.66), S(u"Це місце,", 46.12)
t_ne, t_klo = S(u"не", 46.82), S(u"Клода,", 47.7)
t_nez, t_ty = S(u"незалежним.", 48.39), S(u"ти,", 49.56)
t_ik, t_tud = S(u"і Клод", 49.69), S(u"туди", 50.54)
t_akt = S(u"актуальну", 51.08)
C.append(u'''
        <div id="c7h" class="hid" style="position:absolute; left:0; width:1080px; top:330px; text-align:center;
             font-weight:700; font-size:150px; line-height:.95; letter-spacing:-0.04em; color:#7A1424">point of<br>reference</div>
        <svg class="sk" id="skC" width="1080" height="1920" viewBox="0 0 1080 1920"></svg>''')
js(u'''
  full(%.3f, %.3f);
  pop("#c7h", %.3f, .6);
  sketch("c1", "skC"); cyl("c1", 190, 790, 180, 140, {seed: 51});
  label("c1", 190, 1010, "памʼять", {size: 44}); label("c1", 190, 1058, "Клода", {size: 44});
  draw("c1", %.3f, .45);
  sketch("c2", "skC"); box("c2", 360, 760, 620, 300, {seed: 53, fill: true, r: 32});
  draw("c2", %.3f, .7);
  sketch("c3", "skC"); cross("c3", 98, 752, 292, 1072, {stroke: "#7A1424", strokeWidth: 7, seed: 55});
  draw("c3", %.3f, .3);
  sketch("c4", "skC"); label("c4", 670, 730, "незалежне", {size: 52, color: "#7A1424"});
  draw("c4", %.3f);
  sketch("c5", "skC"); label("c5", 470, 1290, "ти", {size: 56});
  arrow("c5", 480, 1240, 540, 1085, {seed: 57, bend: .1});
  draw("c5", %.3f, .45);
  sketch("c6", "skC"); label("c6", 880, 1290, "Клод", {size: 56});
  arrow("c6", 860, 1240, 800, 1085, {seed: 59, bend: -.1});
  draw("c6", %.3f, .45);
  sketch("c7", "skC"); label("c7", 670, 900, "актуальна", {size: 54});
  label("c7", 670, 965, "інформація", {size: 54});
  draw("c7", %.3f);
''' % (c0, c1, t_poi, t_mis - 0.95, t_mis - 0.5, t_ne, t_nez, t_ty - 0.35, t_ik - 0.2, t_akt))
g.sfx("whoosh-short", c0); g.sfx("pop", t_poi); g.sfx("click-soft", t_ne); g.sfx("click-soft", t_akt)
g.sfx("whoosh-short", c1)
BLACKOUT.append((t_poi - 0.05, E(u"reference.", 45.24) + 0.05))      # the heading says it

# 8 · ABOVE — a doc for the slow things: Claude reads it, we update it --------
t_pros, t_doc = S(u"простих", 53.02), S(u"Клод-док,", 55.15)
t_onov, t_strat = S(u"оновлюється.", 56.79), S(u"стратегією:", 58.21)
t_kd, t_onovl = S(u"Клод", 59.36), S(u"оновлюємо.", 61.5)
t_ale2 = S(u"Але", 62.34)
F.append(u'''
        <div id="b8" class="card hid" style="left:120px; top:300px; width:840px; height:380px; padding:30px 40px;">
          <span class="lbl">Проста система</span>
        </div>
        <div id="b8d" class="hid" style="position:absolute; left:190px; top:372px; width:300px; height:282px;
             background:#fff; border:3px solid #DEBFBF; border-radius:22px; padding:26px 26px;">
          <div class="row" style="gap:12px; color:#7A1424">%s
            <span id="b8t" class="hid" style="font-weight:700; font-size:38px; color:#241919">Стратегія</span></div>
          <span class="line" style="margin-top:26px; width:92%%"></span>
          <span class="line" style="margin-top:16px; width:78%%"></span>
          <span class="line" style="margin-top:16px; width:86%%"></span>
          <span class="line" style="margin-top:16px; width:60%%"></span>
        </div>
        <div id="b8c" class="chip hid" style="position:absolute; left:640px; top:430px; color:#7A1424">%s<span style="color:#241919">Claude</span></div>''' % (mark("claude", 40), mark("claude", 36)))
js(u'''
  rise("#b8", %.3f);
  pop("#b8d", %.3f);
  sketch("o8", "skF");
  _add(SK.o8, SK.o8.rc.path("M 625 605 A 55 55 0 1 0 570 660", opt({stroke: "#7A1424", strokeWidth: 5}, 63)));
  _add(SK.o8, SK.o8.rc.line(570, 660, 540, 640, opt({stroke: "#7A1424", strokeWidth: 5}, 65)), "head");
  _add(SK.o8, SK.o8.rc.line(570, 660, 540, 682, opt({stroke: "#7A1424", strokeWidth: 5}, 67)), "head");
  draw("o8", %.3f, .5);
  fadein("#b8t", %.3f, .3);
  pop("#b8c", %.3f);
  sketch("a8", "skF"); arrow("a8", 632, 470, 508, 474, {seed: 69, bend: -.18});
  draw("a8", %.3f, .4);
  sketch("e8", "skF"); ln("e8", 214, 546, 452, 542, {stroke: "#7A1424", strokeWidth: 6, seed: 73});
  under("e8", 222, 616, 420, {stroke: "#7A1424", strokeWidth: 6, seed: 75});
  draw("e8", %.3f, .3);
  sink("#b8, #b8d, #b8c", %.3f); erase("o8", %.3f); erase("a8", %.3f); erase("e8", %.3f);
''' % (t_pros - 0.2, t_doc, t_onov - 0.2, t_strat, t_kd - 0.05, t_kd + 0.2, t_onovl - 0.25,
       t_ale2 - 0.25, t_ale2 - 0.25, t_ale2 - 0.25, t_ale2 - 0.25))
g.sfx("pop", t_doc); g.sfx("click-soft", t_onov - 0.2); g.sfx("pop", t_kd - 0.05); g.sfx("click-soft", t_onovl - 0.2)

# 9 · ABOVE — Notion for the fast things; free, simple, not for your eyes -----
t_kp, t_id, t_zad = S(u"контент-плану,", 63.32), S(u"ідей,", 64.18), S(u"задач,", 64.66)
t_not2, t_bezk, t_prost = S(u"Notion.", 65.88), S(u"безкоштовний,", 66.78), S(u"простий,", 67.80)
t_tobi, t_ne2 = S(u"тобі", 69.30), S(u"не", 70.14)
h2 = S(u"Я", 71.40) - 0.15
ROWS = [(u"Контент-план", t_kp), (u"Ідеї", t_id), (u"Задачі", t_zad)]
F.append(u'''
        <div id="b9" class="card hid" style="left:120px; top:300px; width:840px; height:380px; padding:32px 40px;">
          <div class="row" style="gap:16px; height:56px">
            <span class="lbl" id="b9l" style="margin:0">Все швидке</span>
            <span id="b9n" class="row hid" style="gap:14px; color:#241919">%s<b style="font-size:46px; font-weight:700">Notion</b></span>
          </div>
          <div style="height:2px; background:#EFE3E3; margin:18px 0 6px; width:420px"></div>
          %s
        </div>
        <div id="b9p1" class="pill hid" style="left:600px; top:400px; font-size:40px; padding:22px 38px; transform:rotate(-3deg)">безкоштовний</div>
        <div id="b9p2" class="pill light hid" style="left:640px; top:510px; font-size:40px; padding:22px 38px; transform:rotate(2deg)">простий</div>''' % (
    mark("notion", 50),
    u"".join(u'<div class="row hid" id="b9r%d" style="gap:16px; padding:14px 0; border-bottom:2px solid #F4EAEA; width:420px">'
             u'<span style="width:34px; height:40px; border:3px solid #DEBFBF; border-radius:6px; flex:none"></span>'
             u'<span style="font-size:40px; font-weight:500">%s</span></div>' % (i, esc(w)) for i, (w, _) in enumerate(ROWS))))
js(u'''
  rise("#b9", %.3f);
  %s
  tl.to("#b9l", {autoAlpha: 0, duration: .2}, %.3f); pop("#b9n", %.3f);
  pop("#b9p1", %.3f); pop("#b9p2", %.3f);
  out("#b9p1, #b9p2", %.3f);
  sketch("e9", "skF"); eye("e9", 780, 470, {seed: 77});
  label("e9", 780, 600, "тобі не треба", {size: 46});
  draw("e9", %.3f, .45);
  sketch("s9", "skF"); ln("s9", 670, 560, 890, 380, {stroke: "#7A1424", strokeWidth: 7, seed: 79});
  draw("s9", %.3f, .3);
  sink("#b9", %.3f); erase("e9", %.3f); erase("s9", %.3f);
''' % (t_ale2 - 0.1, " ".join('rise("#b9r%d", %.3f, 30);' % (i, t - 0.1) for i, (_, t) in enumerate(ROWS)),
       t_not2 - 0.1, t_not2 - 0.05, t_bezk, t_prost, t_tobi - 0.35, t_tobi - 0.2, t_ne2, h2 - 0.3, h2 - 0.3, h2 - 0.3))
g.sfx("pop", t_ale2 - 0.1); g.sfx("click-soft", t_kp)
g.sfx("pop", t_not2 - 0.05); g.sfx("pop", t_bezk); g.sfx("click-soft", t_ne2)
BLACKOUT.append((t_kp - 0.3, E(u"задач,", 64.66) + 0.05))
BLACKOUT.append((S(u"Він", 66.66) - 0.05, E(u"простий,", 67.80) + 0.05))

# 10 · HALF — not for you, for Claude: a board by stage, old apart from new ----
h3 = S(u"Тому", 79.27) - 0.12
HALF.append((h2, h3))
t_pid, t_teb = S(u"підключаю", 71.70), S(u"тебе,", 72.58)
t_kla, t_znav = S(u"Клода,", 74.02), S(u"знав,", 75.27)
t_etap, t_kozh = S(u"етапі", 76.05), S(u"кожен", 76.71)
t_stare, t_nov = S(u"старе", 78.13), S(u"новим.", 78.73)
P.append(u'<div id="p10n" class="row hid" style="position:absolute; left:410px; top:344px; gap:14px; color:#241919">'
         u'%s<b style="font-size:48px; font-weight:700">Notion</b></div>' % mark("notion", 56))
js(u'''
  pop("#p10n", %.3f);
  sketch("q1", "skP"); ell("q1", 220, 380, 200, 124, {seed: 101}); label("q1", 220, 398, "ти", {size: 56});
  arrow("q1", 395, 380, 330, 380, {seed: 103, bend: .15});
  draw("q1", %.3f, .4);
  sketch("q2", "skP"); cross("q2", 140, 322, 300, 438, {stroke: "#7A1424", strokeWidth: 6, seed: 105});
  draw("q2", %.3f, .3);
  sketch("q3", "skP"); arrow("q3", 655, 380, 728, 380, {seed: 107, bend: -.15});
  ell("q3", 840, 380, 210, 124, {seed: 109, stroke: "#7A1424"}); label("q3", 840, 398, "Клод", {size: 56});
  draw("q3", %.3f, .4);
  sketch("q4", "skP"); tick("q4", 958, 318, {stroke: "#7A1424", strokeWidth: 6, seed: 111, k: .75});
  draw("q4", %.3f, .3);
  sketch("q5", "skP"); box("q5", 110, 500, 860, 290, {seed: 113, r: 28});
  ln("q5", 397, 515, 397, 775, {seed: 115}); ln("q5", 683, 515, 683, 775, {seed: 117});
  label("q5", 253, 562, "ідея", {size: 46}); label("q5", 540, 562, "в роботі", {size: 46});
  label("q5", 826, 562, "вийшло", {size: 46});
  draw("q5", %.3f, .45);
  sketch("q6", "skP"); box("q6", 168, 600, 170, 84, {seed: 121, r: 18, fill: true});
  box("q6", 455, 600, 170, 84, {seed: 123, r: 18, fill: true}); box("q6", 741, 600, 170, 84, {seed: 125, r: 18, fill: true});
  draw("q6", %.3f, .35);
  sketch("q7", "skP"); label("q7", 826, 746, "старе", {size: 48, color: "#7A1424"});
  draw("q7", %.3f);
  sketch("q8", "skP"); label("q8", 253, 746, "нове", {size: 48, color: "#7A1424"});
  draw("q8", %.3f);
  out("#p10n", %.3f);
  ["q1","q2","q3","q4","q5","q6","q7","q8"].forEach(function (n) { erase(n, %.3f); });
''' % (t_pid, t_teb - 0.55, t_teb + 0.05, t_kla - 0.55, t_kla + 0.05, t_etap - 0.55, t_kozh - 0.1,
       t_stare, t_nov, h3, h3))
g.sfx("whoosh-short", h2); g.sfx("whoosh-short", h3)
for t in (t_teb + 0.05, t_kla + 0.05, t_etap - 0.5, t_stare):
    g.sfx("click-soft", t)

# 11 · ABOVE — CTA: save money, build it yourself, the lifehack, subscribe -----
# the last clip (85.97-) is a hard punch-in: her hair top rises to y ≈ 505, so
# the lifehack and the red pill sit in y 300-530 and the pointer comes from the left
t_zek, t_hro = S(u"зекономити", 80.47), S(u"грошей", 81.71)
t_ai, t_sam = S(u"AI-систему", 82.93), S(u"самостійно,", 83.55)
t_lh, t_obov = S(u"лайфхаком", 85.38), S(u"обовʼязково", 86.31)
F.append(u'''
        <div id="b11" class="hid" style="position:absolute; left:120px; top:318px; width:840px;
             display:flex; gap:14px; justify-content:center; flex-wrap:wrap">
          <span class="chip hid" id="b11a"><i></i>зекономити</span>
          <span class="chip hid" id="b11b"><i></i>AI-система самостійно</span>
        </div>
        <div id="b11l" class="hid" style="position:absolute; left:0; top:296px; width:1080px; display:flex; justify-content:center">
          <span class="pill light" style="position:relative; font-size:42px; padding:20px 42px">лайфхак:
          <span style="color:#7A1424; display:inline-flex; align-items:center; gap:10px">+ %s<b style="font-weight:700">Notion</b></span></span></div>
        <div id="b11cta" class="hid" style="position:absolute; left:0; top:408px; width:1080px; display:flex; justify-content:center">
          <span class="pill" style="position:relative; font-size:50px; padding:28px 54px">Підпишись</span></div>''' % mark("notion", 40))
js(u'''
  fadein("#b11", %.3f, .01); pop("#b11a", %.3f);
  sketch("u11", "skF"); under("u11", 172, 412, 420, {stroke: "#7A1424", strokeWidth: 5, seed: 131});
  draw("u11", %.3f, .4);
  pop("#b11b", %.3f);
  sink("#b11", %.3f); erase("u11", %.3f);
  pop("#b11l", %.3f);
  pop("#b11cta", %.3f, .6);
  sketch("a11", "skF"); arrow("a11", 185, 668, 338, 506, {stroke: "#7A1424", strokeWidth: 5, seed: 133, bend: -.12});
  draw("a11", %.3f, .45);
''' % (t_zek - 0.05, t_zek, t_hro - 0.1, t_sam - 0.1, t_lh - 0.3, t_lh - 0.3, t_lh, t_obov - 0.1, t_obov + 0.3))
g.sfx("pop", t_zek); g.sfx("kaching", t_hro); g.sfx("pop", t_lh); g.sfx("pop", t_obov - 0.1)
BLACKOUT.append((S(u"і", 85.97) - 0.05, DUR))     # the pill says it

# ---------------------------------------------------------------- mattes for the half screens
for i, (a, b) in enumerate(HALF):
    g.matte("half%d" % (i + 1), round(a - 0.1, 3), round(b - a + 1.2, 3))
    js("  half(%.3f, %.3f);" % (a, b))
    PLACE.append((a + 0.4, b + 0.2, "bottom", 980))

F.append(u'<svg class="sk" id="skF" width="1080" height="1920" viewBox="0 0 1080 1920"></svg>')


# caption phrases: where her phrasing breaks, not where 40 characters run out
SPLITS = [38.66, 40.25, 50.78, 55.15, 69.30, 81.15, 82.09, 84.76, 85.97]
JOINS = [21.73, 39.22, 41.11, 51.08, 54.48, 56.79, 70.34, 81.37, 82.93, 83.55, 86.31]
KEYS = {u"срака": True, u"мінус": True, u"думає": True, u"даних": True, u"памʼяттю": True, u"знав": True,
        u"етапі": True, u"тебе": True, u"лайфхаком": True, u"грошей": True}


def rechunk(chunks):
    near = lambda t, ts: any(abs(t - x) < 0.06 for x in ts)
    for t in SPLITS + JOINS:
        assert any(abs(w["s"] - t) < 0.06 for c in chunks for w in c["words"]), t
    groups = []
    for c in chunks:
        for i, w in enumerate(c["words"]):
            start = (i == 0 and not near(w["s"], JOINS)) or (i > 0 and near(w["s"], SPLITS))
            if start or not groups:
                groups.append([])
            groups[-1].append(w)
    out = []
    for n, ch in enumerate(groups):
        s = ch[0]["s"]
        nxt = groups[n + 1][0]["s"] if n + 1 < len(groups) else DUR
        pos = ("bottom", 1920 - 1520)
        for a, b, how, y in PLACE:
            if a <= s < b:
                pos = (how, y if how == "top" else 1920 - y)
        out.append({"s": round(s, 3), "e": round(min(nxt, ch[-1]["e"] + 0.6), 3), "words": ch,
                    "key": g._key(ch, KEYS), "pos": pos})
    return out


def main():
    if "--words" in sys.argv:
        print(" ".join("%s/%.1f" % (c["w"], c["s"]) for c in CAPS))
    chunks = rechunk(g.chunks(CAPS, keys=KEYS, place=PLACE))
    if "--chunks" in sys.argv:
        for c in chunks:
            print("%6.2f-%6.2f %s%s" % (c["s"], c["e"], " ".join(w["w"] for w in c["words"]),
                                        "  [%s]" % c["words"][c["key"]]["w"] if c["key"] is not None else ""))
    doc = g.document(title=u"Reel 47 — Навіщо Notion", plate="assets/base.mp4",
                     behind="\n".join(B), panel="\n".join(P), front="\n".join(F), cover="\n".join(C),
                     js="\n".join(J), chunks=chunks, blackout=BLACKOUT)
    g.write(HERE, doc)
    print("index.html  %d caption chunks, %d sfx cues, %d mattes" % (len(chunks), len(g.cues), len(g.mattes)))


main()
