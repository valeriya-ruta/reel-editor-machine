# -*- coding: utf-8 -*-
"""Reel 49 — «Все з телефону». Posts 2026-10-24.

Short (26.6 s), her Google style + Excalidraw look (STYLE.md §00, with her
review of reel 41 on top: word-by-word captions, calm white sketches over
the footage, long arrows).

The one object is **the cloud**. It is drawn round her AI system, shrinks
aside so a task can be thrown into it from a phone, grows back with Claude's
own laptop working inside it; the half screen runs the same phone → cloud →
result diagram twice (photo → carousel, video → edit, not your computer);
the CTA closes on the cloud again, holding «24/7».

  above   «АІ-система» card, «+» badge on «плюс», a cloud drawn round it on «хмарі»
  above   the cloud shrinks right; a phone; a task (check + line) thrown into the cloud
  above   the cloud grows back: Claude's laptop inside, the task ticks, an edit renders
  half    phone → Claude cloud → carousel «твій дизайн»; then video → «монтаж»
          in the cloud (red) and «твій компʼютер» crossed out
  above   CTA — блогерка / СММниця / підприємиця, a cloud holding «24/7»,
          «Став + в коментарі» + pointer

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

NN = "49"
CUT = json.load(io.open(os.path.join(ROOT, "work", "r" + NN, "cut.json"), encoding="utf-8"))
DUR = 26.65            # (800 plate frames - 0.5) / 30
g = G(dur=DUR, reel=NN)

# whisper's spelling of what she said -> her word (re-heard on the plate)
FIX = {
    u"Та": u"Те",                                  # «Те саме з монтажем»
    u"самемноця": u"СММниця",
    (u"телефону", 12.5): u"телефона",              # she says «з телефона» both times
    (u"компʼютері,", 19.4): u"компʼютері.",        # the clause after it was cut
    (u"тому", 20.1): u"Тому",
    u"24": u"24/7,", (u"на", 24.8): None, u"7,": None,
    (u"плюс", 25.6): u"+",
    u"коментарі": u"коментарі.",
}
CAPS = load_caps(NN, FIX)
# «єйсистеми» is two words, «АІ системи»: split it so the rail shows each
for i, c in enumerate(CAPS):
    if c["w"] == u"єйсистеми":
        mid = round(c["s"] + 0.27, 3)
        CAPS[i:i + 1] = [dict(c, w=u"АІ", e=round(mid - 0.02, 3)), dict(c, w=u"системи", s=mid)]
        break
W = Words(CAPS)
S, E = W.s, W.e

# ---------------------------------------------------------------- the beats
B, P, F, C, J = [], [], [], [], []     # behind / panel / front / cover html, js
BLACKOUT = []
PLACE = []                             # caption placement over the half screen
HALF = []


def js(s):
    J.append(s)


# a cloud, in unit coordinates: flat bottom, four bumps, a roomy middle
CLOUD = [(0.15, 0.95), (0.00, 0.95), (-0.02, 0.62), (0.14, 0.58), (0.10, 0.30), (0.34, 0.20), (0.42, 0.34),
         (0.48, 0.02), (0.78, 0.04), (0.80, 0.32), (0.98, 0.26), (1.04, 0.56), (0.92, 0.66),
         (1.04, 0.78), (0.98, 0.98), (0.85, 0.95)]


def cloud(name, x, y, w, h, o=u""):
    """the kit's blob() for a cloud: over the footage it becomes a white sticker
    with a dark outline (her review of 41), on the panel it stays a plain stroke"""
    p = ["%.0f %.0f" % (x + u * w, y + v * h) for u, v in CLOUD]
    d = "M" + p[0] + "".join(" C" + ", ".join(p[i:i + 3]) for i in range(1, len(p), 3)) + " Z"
    return u'blob("%s", "%s", [%d, %d, %d, %d]%s);' % (name, d, x, y, w, h, (u", " + o) if o else u"")


# an open hand-drawn polyline (a photo's mountain, a play triangle) — panel only
js(u'''
  function poly(name, pts, o) { _ink = SK[name].ink;
    _add(SK[name], SK[name].rc.linearPath(pts, opt(o, (o && o.seed) || 45))); }
''')

# 1 · ABOVE — the system, its plus, the cloud round it ---------------------------
t_gol, t_plus = S(u"Головний", 0.43), S(u"плюс", 0.91)
t_hm1, e_hm1 = S(u"хмарі.", 4.63), E(u"хмарі.", 4.63)
# the cloud and everything that lives in it share one wrapper, so the cloud can
# step aside for the phone (beat 2) and come back (beat 3) with its contents
F.append(u'''
        <div id="w1" class="L">
          <svg class="sk" id="skW" width="1080" height="1920" viewBox="0 0 1080 1920"></svg>
          <div id="b1" class="card hid" style="left:330px; top:455px; width:420px; padding:26px 30px;">
            <div class="row" style="gap:20px">
              <span style="color:#7A1424">%s</span>
              <div><span class="lbl" style="margin-bottom:6px">Моє налаштування</span>
                   <span class="ttl" style="font-size:48px">АІ-система</span></div>
            </div>
          </div>
          <div id="b1x" class="hid" style="position:absolute; left:702px; top:418px; width:78px; height:78px;
               border-radius:50%%; background:#7A1424; color:#fff; font-weight:700; font-size:62px;
               line-height:76px; text-align:center;
               box-shadow:0 1px 3px rgba(36,25,25,.12), 0 10px 30px rgba(122,20,36,.22)">+</div>
          <div id="lap" class="card hid" style="left:360px; top:428px; width:360px; height:190px; padding:0;
               border-radius:22px;">
            <div id="laph" class="row hid" style="position:absolute; left:24px; top:16px; gap:10px">
              <span style="color:#7A1424">%s</span><span style="font-size:30px; font-weight:500">Claude</span>
            </div>
            <div id="lapp" class="hid" style="position:absolute; left:24px; right:24px; bottom:18px;
                 display:flex; align-items:center; gap:12px">
              <svg width="24" height="28" viewBox="0 0 24 28"><path d="M3 2 L22 14 L3 26 Z" fill="#7A1424"/></svg>
              <span class="line" style="flex:1; position:relative; overflow:hidden">
                <span id="lapf" style="position:absolute; left:0; top:0; bottom:0; width:100%%;
                      background:#7A1424; border-radius:9px"></span></span>
            </div>
          </div>
          <div id="lapb" class="hid" style="position:absolute; left:320px; top:626px; width:440px; height:22px;
               background:#fff; border-radius:6px 6px 16px 16px;
               box-shadow:0 1px 3px rgba(36,25,25,.10), 0 10px 30px rgba(36,25,25,.10)"></div>
        </div>
        <svg class="sk" id="skF" width="1080" height="1920" viewBox="0 0 1080 1920"></svg>
        <div id="t2" class="chip hid" style="position:absolute; left:152px; top:448px; padding:10px 16px; gap:12px">
          <span class="check" id="t2c"></span><span class="line" style="width:44px"></span>
        </div>''' % (mark("claude", 58), mark("claude", 38)))
js(u'''
  gsap.set("#w1", {transformOrigin: "540px 480px"});
  gsap.set("#lapf", {scaleX: 0, transformOrigin: "0%% 50%%"});
  rise("#b1", %.3f);
  pop("#b1x", %.3f);
  sketch("cl", "skW"); %s
  draw("cl", %.3f, .7);
  sink("#b1, #b1x", %.3f);
''' % (t_gol - 0.13, t_plus, cloud("cl", 140, 262, 800, 420, u"{seed: 41}"), t_hm1 - 0.65, e_hm1))
g.sfx("pop", t_gol - 0.13); g.sfx("whoosh-short", t_hm1 - 0.65)

# 2 · ABOVE — the cloud steps aside; a task thrown from the phone into it -------
t_mv = e_hm1 + 0.02
t_zad, t_kyn, t_tel = S(u"задачу", 5.44), S(u"кинути", 6.0), S(u"телефона,", 6.7)
t_back = S(u"а", 7.42) - 0.12
js(u'''
  tl.to("#w1", {x: 165, y: 0, scale: .6, duration: .7, ease: SLIDE}, %.3f);
  sketch("ph", "skF"); box("ph", 140, 330, 160, 300, {seed: 43, r: 30});
  ln("ph", 200, 352, 240, 352, {seed: 45}); ln("ph", 195, 606, 245, 606, {seed: 47});
  draw("ph", %.3f, .5);
  pop("#t2", %.3f, .5);
  sketch("ar", "skF"); arrow("ar", 310, 470, 488, 486, {seed: 49, bend: .15});
  draw("ar", %.3f, .35);
  tl.to("#t2", {keyframes: [{x: 245, y: -110, duration: .32, ease: "power1.out"},
                            {x: 487, y: 20, duration: .33, ease: "power1.in"}]}, %.3f);
  sketch("phl", "skF"); label("phl", 220, 676, "телефон", {size: 42});
  draw("phl", %.3f);
  erase("ph", %.3f); erase("ar", %.3f); erase("phl", %.3f);
''' % (t_mv, t_mv - 0.05, t_zad, t_kyn - 0.15, t_kyn, S(u"прямо", 6.3) + 0.1, t_back, t_back, t_back))
g.sfx("pop", t_zad); g.sfx("whoosh-short", t_kyn)

# 3 · ABOVE — the cloud grows back: Claude's laptop, the task ticks, an edit renders
t_kl, t_pra, t_mon = S(u"Клод", 7.74), S(u"працює", 7.94), S(u"і монтує", 8.48)
t_hmn, e_komp = S(u"хмарному", 9.7), E(u"компʼютері.", 10.4)
t_clr = min(e_komp - 0.03, S(u"Наприклад,", 11.27) - 0.3)   # gone before «Наприклад»
js(u'''
  tl.to("#w1", {x: 0, y: 0, scale: 1, duration: .7, ease: SLIDE}, %.3f);
  tl.to("#t2", {x: 232, y: 40, duration: .7, ease: SLIDE}, %.3f);
  pop("#lap", %.3f, .6); pop("#lapb", %.3f, .55);
  pop("#laph", %.3f, .5);
  tl.set("#t2c", {className: "check on"}, %.3f); pop("#t2c", %.3f, .45);
  fadein("#lapp", %.3f, .3);
  tl.to("#lapf", {scaleX: 1, duration: %.3f, ease: "power1.inOut"}, %.3f);
  // a second outline on «хмарному»: it lies on the white cloud sticker drawn
  // above, so it stays an outline (fill: false) instead of a second sticker
  // that would paint over the first outline
  sketch("cl2", "skW"); %s
  draw("cl2", %.3f, .6);
  tl.to("#w1, #t2", {autoAlpha: 0, duration: .3, ease: "power2.in"}, %.3f);
''' % (t_back, t_back, t_back, t_back + 0.08, t_kl, t_pra + 0.08, t_pra + 0.08, t_mon - 0.12,
       t_clr - 0.2 - t_mon, t_mon, cloud("cl2", 140, 262, 800, 420, u"{seed: 53, strokeWidth: 6, fill: false}"),
       t_hmn - 0.4, t_clr))
g.sfx("pop", t_back); g.sfx("click-soft", t_pra + 0.08)

# 4 · HALF — phone → Claude → carousel; video → «монтаж» in the cloud, not your computer
h0 = S(u"кидаєш", 11.85) - 0.23
h1 = h0 + 8.0
HALF.append((h0, h1))
t_foto, t_cla = S(u"фото", 12.23), S(u"Claude,", 13.19)
t_kar, t_dyz = S(u"карусель", 14.25), S(u"дизайні.", 14.97)
t_te, t_mtzh = S(u"Те", 15.62), S(u"з монтажем:", 16.0)
t_kyd2, t_vid = S(u"кидаєш", 16.6), S(u"відео,", 16.94)
t_hm2, t_ane = S(u"в хмарі,", 18.18), S(u"а не", 18.82)
t_komp2 = S(u"компʼютері.", 19.38)
P.append(u'<svg class="sk" id="skP" width="1080" height="1240" viewBox="0 0 1080 1240"></svg>')
P.append(u'<div id="pm" class="hid" style="position:absolute; left:510px; top:470px; color:#7A1424">%s</div>'
         % mark("claude", 64))
CL_P = (392, 380, 300, 280)          # the panel cloud, drawn twice
js(u'''
  sketch("a_ph", "skP"); box("a_ph", 95, 400, 130, 250, {seed: 61, r: 26});
  ln("a_ph", 145, 422, 175, 422, {seed: 62}); ln("a_ph", 140, 628, 180, 628, {seed: 63});
  draw("a_ph", %.3f, .5);
  sketch("a_ft", "skP"); box("a_ft", 112, 470, 96, 96, {seed: 64, r: 12});
  poly("a_ft", [[118, 556], [145, 520], [163, 540], [180, 522], [202, 556]], {seed: 65});
  ell("a_ft", 185, 494, 20, 20, {seed: 66});
  draw("a_ft", %.3f, .4);
  sketch("a_ftl", "skP"); label("a_ftl", 160, 722, "фото", {size: 46}); draw("a_ftl", %.3f);
  sketch("a_a1", "skP"); arrow("a_a1", 238, 528, 396, 518, {seed: 67});
  draw("a_a1", %.3f, .35);
  sketch("a_cl", "skP"); %s
  draw("a_cl", %.3f, .55);
  pop("#pm", %.3f, .5);
  sketch("a_cll", "skP"); label("a_cll", 545, 622, "Claude", {size: 46}); draw("a_cll", %.3f);
  sketch("a_a2", "skP"); arrow("a_a2", 698, 520, 852, 510, {seed: 69});
  draw("a_a2", %.3f, .35);
  sketch("a_car", "skP"); box("a_car", 858, 400, 132, 200, {seed: 70, r: 20, fill: true});
  ell("a_car", 900, 634, 16, 16, {seed: 71, stroke: "#7A1424"}); ell("a_car", 924, 634, 14, 14, {seed: 72});
  ell("a_car", 948, 634, 14, 14, {seed: 73});
  draw("a_car", %.3f, .45);
  sketch("a_carl", "skP"); label("a_carl", 990, 722, "карусель", {size: 44, anchor: "end"}); draw("a_carl", %.3f);
  sketch("a_dz", "skP"); under("a_dz", 790, 808, 990, {stroke: "#7A1424", seed: 74});
  label("a_dz", 990, 790, "твій дизайн", {size: 44, anchor: "end", color: "#7A1424"});
  draw("a_dz", %.3f, .45);
''' % (h0 + 0.1, h0 + 0.45, t_foto + 0.2, t_cla - 0.55, cloud("a_cl", *CL_P, o=u"{seed: 68}"), t_cla - 0.45, t_cla, t_cla + 0.1,
       t_kar - 0.6, t_kar - 0.35, t_kar + 0.1, t_dyz - 0.35))
js(u'''
  erase("a_ft", %.3f); erase("a_ftl", %.3f); erase("a_a1", %.3f); erase("a_a2", %.3f);
  erase("a_car", %.3f); erase("a_carl", %.3f); erase("a_dz", %.3f);
  erase("a_cll", %.3f);
  sketch("b_ml", "skP"); label("b_ml", 545, 622, "монтаж", {size: 46}); draw("b_ml", %.3f);
  sketch("b_vd", "skP"); box("b_vd", 112, 470, 96, 96, {seed: 81, r: 12});
  poly("b_vd", [[146, 494], [146, 542], [184, 518], [146, 494]], {seed: 82, stroke: "#7A1424"});
  draw("b_vd", %.3f, .4);
  sketch("b_vdl", "skP"); label("b_vdl", 160, 722, "відео", {size: 46}); draw("b_vdl", %.3f);
  sketch("b_a1", "skP"); arrow("b_a1", 238, 528, 396, 518, {seed: 83});
  draw("b_a1", %.3f, .35);
  sketch("b_clr", "skP"); %s
  draw("b_clr", %.3f, .5);
  sketch("b_lp", "skP"); box("b_lp", 860, 420, 110, 84, {seed: 85, r: 12}); box("b_lp", 842, 512, 146, 16, {seed: 86, r: 8});
  draw("b_lp", %.3f, .4);
  sketch("b_lpl", "skP"); label("b_lpl", 990, 600, "твій", {size: 42, anchor: "end"});
  label("b_lpl", 990, 650, "компʼютер", {size: 42, anchor: "end"}); draw("b_lpl", %.3f);
  sketch("b_x", "skP"); ln("b_x", 835, 400, 995, 545, {seed: 87, stroke: "#7A1424", strokeWidth: 7});
  ln("b_x", 995, 400, 835, 545, {seed: 88, stroke: "#7A1424", strokeWidth: 7});
  draw("b_x", %.3f, .25);
''' % ((t_te - 0.05,) * 7 + (t_mtzh - 0.1, t_mtzh, t_kyd2 - 0.25, t_vid, t_vid + 0.05,
                              cloud("b_clr", *CL_P, o=u'{seed: 84, stroke: "#7A1424", strokeWidth: 5.5}'), t_hm2 - 0.3,
                              t_ane - 0.1, t_ane + 0.25, t_komp2 - 0.3)))
g.sfx("whoosh-short", h0); g.sfx("pop", t_kar - 0.35); g.sfx("click-soft", t_komp2); g.sfx("whoosh-short", h1)

# 5 · ABOVE — CTA: who it is for, a cloud team 24/7, «став +» ---------------------
t_blog, t_smm, t_pid = S(u"блогерка,", 20.82), S(u"СММниця", 21.32), S(u"підприємиця", 22.0)
t_hmn2, t_24, t_stav = S(u"хмарну", 23.38), S(u"24/7,", 24.34), S(u"став", 25.4)
t_to = S(u"то", 25.3)
# chips 290-361 · the cloud sticker 376-558 holding «24/7» · the pill 572-678 ·
# her hair from y ~705, so everything stays above her
F.append(u'''
        <div id="c1" style="position:absolute; left:90px; width:900px; top:290px; display:flex; gap:14px;
             justify-content:center">
          <span class="chip hid" id="c1a"><i></i>блогерка</span>
          <span class="chip hid" id="c1b"><i></i>СММниця</span>
          <span class="chip hid" id="c1c"><i></i>підприємиця</span>
        </div>
        <div style="position:absolute; left:0; width:1080px; top:436px; display:flex; justify-content:center">
          <span id="c24" class="num hid" style="position:relative; font-size:92px">24/7</span></div>
        <div style="position:absolute; left:0; width:1080px; top:572px; display:flex; justify-content:center">
          <span id="cta" class="pill hid" style="position:relative; padding:22px 50px">Став + в коментарі</span></div>''')
js(u'''
  pop("#c1a", %.3f); pop("#c1b", %.3f); pop("#c1c", %.3f);
  sketch("cc", "skF"); %s
  draw("cc", %.3f, .7);
  pop("#c24", %.3f);
  pop("#cta", %.3f, .6);
  // the comments button is down the IG rail on the right: the pointer goes DOWN
  // toward the lower right, tip left of x 900 — never up at the pill (her review of 41)
  sketch("pt", "skF"); label("pt", 838, 748, "сюди!", {size: 50});
  arrow("pt", 842, 778, 882, 986, {strokeWidth: 5, seed: 97, bend: -.22});
  draw("pt", %.3f, .5);
''' % (t_blog, t_smm, t_pid, cloud("cc", 340, 372, 400, 190, u"{seed: 91}"), t_hmn2 - 0.45, t_24, t_stav,
       t_stav + 0.1))
g.sfx("pop", t_blog); g.sfx("pop", t_24); g.sfx("pop", t_stav)
BLACKOUT.append((t_to - 0.05, DUR))     # «то став + в коментарі»: the pill says it

# ---------------------------------------------------------------- matte for the half screen
for i, (a, b) in enumerate(HALF):
    g.matte("half%d" % (i + 1), round(a - 0.1, 3), round(b - a + 1.2, 3))
    js("  half(%.3f, %.3f);" % (a, b))
    PLACE.append((a + 0.4, b + 0.2, "bottom", 980))


def main():
    print(" ".join(u"%s/%.1f" % (c["w"], c["s"]) for c in CAPS))
    chunks = g.chunks(CAPS, place=PLACE)
    doc = g.document(title=u"Reel 49 — Все з телефону", plate="assets/base.mp4",
                     behind="\n".join(B), panel="\n".join(P), front="\n".join(F), cover="\n".join(C),
                     js="\n".join(J), chunks=chunks, blackout=BLACKOUT)
    g.write(HERE, doc)
    print("index.html  %d caption chunks, %d sfx cues, %d mattes" % (len(chunks), len(g.cues), len(g.mattes)))
    print("half", HALF)


main()
