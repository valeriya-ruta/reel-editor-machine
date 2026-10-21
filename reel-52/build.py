# -*- coding: utf-8 -*-
"""Reel 52 — «Якщо в тебе фомо на…». No post date yet.

Her look from reel 41 on (STYLE.md §00) with her review of 41 applied by the
kit: word-by-word captions, calm white sketches over her footage, white
behind-me words.

RUTA held only the first line; she improvised the rest. The one object is
**her free YouTube playlist** — a mini-course on Claude in three videos. The
reel opens on the FOMO rush (buy a course / ask Threads), stops it with a
stopwatch, then the playlist card fills in and each of its three rows is
opened in turn: connectors (half screen: «твій ШІ» gets «потужні руки»),
skills (same panel: what a skill is → a new one made inside the video), the
copywriter (a card writing in your style → her own texts). The CTA brings the
playlist back as a compact card with the link, «Пиши YouTube в коментарі»,
then the follow button.

  behind  «фомо / на ШІ»
  above   a course card «Купити» clicked · a Threads post typing «Який курс взяти?»
  above   a stopwatch — «почекай хвилинку»
  above   the playlist card: title, «українською» «безкоштовно», YouTube, three
          rows, «база», Claude, row 1 «Конектори»
  half    1 Конектори: твій ШІ → Gmail / Календар / Notion, «потужні руки»;
          2 Скіли: «скіл?» → a video → «новий скіл»
  above   the playlist again, row 3 «Копірайтер» → the copywriter card: lines
          writing, «твій стиль»; then «Пишу ним»: сценарії · лід-магніти ·
          повідомлення · …
  above   CTA: compact playlist + «посилання», red pill «Пиши YouTube в
          коментарі», pointer; link lights on «вишлю тобі посилання»
  above   «Підписатися» pressed on «підпишись»

usage: python build.py      (render / sfx mix: the orchestrator)
"""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
from gstyle import G, Words, load_caps, mark, esc  # noqa: E402

NN = "52"
CUT = json.load(io.open(os.path.join(ROOT, "work", "r" + NN, "cut.json"), encoding="utf-8"))
DUR = 54.416           # (1633 plate frames - 0.5) / 30
g = G(dur=DUR, reel=NN)

# whisper's spelling of what she plainly said -> her word (re-heard on the plate)
FIX = {
    u"ТРЕЦ": u"Threads,", u"питати,": u"спитати,", u"Поджекай": u"почекай",
    (u"міні", 9.9): u"міні-курс", (u"курс", 10.2): None,
    u"кладу": u"Клоду", u"кладом.": u"Клодом.",
    u"конектори.": u"конектори,", u"інтелекту.": u"інтелекту",
    (u"що", 25.9): u"Що", u"це,": u"це", u"таке": u"таке?", (u"як", 26.6): u"Як",
    u"копіррайтера.": u"копірайтера", u"колоді,": u"Клоді,",
    (u"будь", 35.8): u"будь-який", (u"який", 36.2): None,
    (u"будь", 39.2): u"будь-яких", u"яких": None,
    u"сценарій,": u"сценаріїв,", u"лід": u"лід-магнітів,", u"магнітів,": None,
    u"далі,": u"далі.", (u"тому", 43.9): u"Тому",
    u"посилання...": u"посилання,", u"youtube": u"YouTube", u"коментарі": u"коментарі,",
    u"посилання.": u"посилання", u"плейліс": u"плейлист", u"вітобі": u"в YouTube.",
}
CAPS = load_caps(NN, FIX)
W = Words(CAPS)
S, E = W.s, W.e
if "-w" in sys.argv:
    print(" ".join("%s/%.1f" % (c["w"], c["s"]) for c in CAPS))

# ---------------------------------------------------------------- the beats
B, P, F, C, J = [], [], [], [], []     # behind / panel / front / cover html, js
BLACKOUT = []
PLACE = []                             # caption placement over the half screens
HALF = []


def js(s):
    J.append(s)


EXTRA_CSS = u"""
    .btn { display: inline-flex; align-items: center; justify-content: center;
           background: var(--primary); color: #fff; border-radius: 999px;
           font-weight: 500; font-size: 32px; padding: 14px 40px; }
    .ch { opacity: 0; visibility: hidden; }
    .caret { display: inline-block; width: 4px; height: 40px; background: var(--primary);
             vertical-align: -6px; margin-left: 3px; }
    .plh { display: flex; align-items: center; gap: 16px; }
    .plh .t { font-weight: 700; font-size: 42px; letter-spacing: -0.02em; color: var(--on-surface); }
    .sm { font-size: 28px; padding: 8px 18px; gap: 10px; }
    .plr { display: flex; align-items: center; gap: 20px; height: 60px; margin-top: 8px;
           border-radius: 14px; padding: 0 8px; }
    .th { position: relative; flex: none; width: 96px; height: 54px; border-radius: 12px;
          background: #EFE3E3; }
    .th b { position: absolute; left: 40px; top: 16px; width: 0; height: 0;
            border-left: 20px solid #fff; border-top: 11px solid transparent;
            border-bottom: 11px solid transparent; }
    .rw { position: relative; flex: 1; height: 54px; }
    .rw .gl { position: absolute; left: 0; top: 18px; width: 300px; height: 18px;
              border-radius: 9px; background: #EFE3E3; }
    .rw .rt { position: absolute; left: 0; top: 0; line-height: 54px; font-weight: 500;
              font-size: 36px; color: var(--on-surface); opacity: 0; }
    .hd { position: absolute; left: 110px; top: 300px; display: flex; align-items: center; gap: 24px; }
    .hd .th { width: 120px; height: 68px; border-radius: 14px; background: var(--primary); }
    .hd .th b { left: 50px; top: 20px; border-left-width: 24px; border-top-width: 14px;
                border-bottom-width: 14px; }
    .hd .rw { width: 420px; height: 68px; }
    .hd .rw .gl { top: 25px; }
    .hd .rw .rt { line-height: 68px; font-size: 54px; font-weight: 700; letter-spacing: -0.02em; }
    .wl { display: block; height: 18px; border-radius: 9px; background: #EFE3E3; width: 0; margin-top: 18px; }
    .ctr { position: absolute; left: 0; width: 1080px; display: flex; justify-content: center; }
    .ctr .pill { position: relative; }
"""

# 1 · BEHIND — «фомо / на ШІ» ---------------------------------------------------
t_fomo, t_sht = S(u"фомо", 0.75), S(u"цей штучний", 1.45)
b_out = S(u"що", 3.09) - 0.2
B.append(u'''
        <div id="bw1" class="big hid" style="top:320px; font-size:240px">фомо</div>
        <div id="bw2" class="big hid" style="top:536px; font-size:240px">на ШІ</div>''')
g.matte("fomo", 0.5, round(b_out + 0.45 - 0.5, 3))
js(u'''
  rise("#bw1", %.3f); rise("#bw2", %.3f);
  sink("#bw1, #bw2", %.3f);
''' % (t_fomo - 0.15, t_sht - 0.1, b_out))
g.sfx("whoosh-short", t_fomo - 0.15)

# 2 · ABOVE — buy a course · ask Threads ---------------------------------------
t_kup, t_kurs = S(u"купувати", 4.19), S(u"курс", 4.77)
t_thr, t_yak, t_vz = S(u"Threads,", 5.73), S(u"який", 6.47), E(u"взяти,", 6.93)
t_poch = S(u"почекай", 7.43)
Q = u"Який курс взяти?"
F.append(u'''
        <div id="b2a" class="card hid" style="left:110px; top:318px; width:410px; padding:26px 28px;">
          <div style="height:110px; border-radius:22px; background:#FFF0F0; display:flex; align-items:center;
               justify-content:center; font-weight:700; font-size:64px; letter-spacing:-0.03em; color:#7A1424">ШІ</div>
          <span class="ttl" style="font-size:40px; margin-top:16px">Курс по ШІ</span>
          <span class="btn" id="b2btn" style="margin-top:18px">Купити</span>
        </div>
        <svg id="b2cur" class="hid" style="position:absolute; left:236px; top:574px" width="54" height="66" viewBox="0 0 27 33">
          <path d="M2 2 L2 26 L8 20 L12 30 L16 28 L12 18 L20 18 Z" fill="#fff" stroke="#241919"
                stroke-width="2" stroke-linejoin="round"/></svg>
        <div id="b2b" class="card hid" style="left:560px; top:318px; width:410px; height:314px; padding:26px 28px;">
          <div class="row" style="gap:14px; color:#241919">%s<span style="font-weight:700; font-size:34px">Threads</span></div>
          <div style="margin-top:26px; font-weight:500; font-size:40px; line-height:1.25; color:#241919">%s<span class="caret hid" id="b2car"></span></div>
          <span class="btn" style="position:absolute; right:28px; bottom:26px; font-size:26px; padding:10px 26px;
                background:#fff; color:#574142; border:2px solid #DEBFBF">Опублікувати</span>
        </div>''' % (mark("threads", 44), u"".join(u'<span class="ch">%s</span>' % esc(ch) for ch in Q)))
step = (t_vz - t_yak) / len(Q)
js(u'''
  rise("#b2a", %.3f);
  tl.fromTo("#b2cur", {autoAlpha: 0, x: 70, y: 70}, X({autoAlpha: 1, x: 0, y: 0, duration: .45, ease: RISE}), %.3f);
  tl.to("#b2btn", {scale: .9, duration: .1, yoyo: true, repeat: 1, ease: "power1.inOut"}, %.3f);
  rise("#b2b", %.3f); fadein("#b2car", %.3f, .1);
  %s
  sink("#b2a, #b2b, #b2cur", %.3f);
''' % (t_kup - 0.35, t_kurs - 0.45, t_kurs, t_thr - 0.25, t_thr + 0.2,
       " ".join(u'tl.set("#b2b .ch:nth-child(%d)", {autoAlpha: 1}, %.3f);' % (i + 1, t_yak + i * step)
                for i in range(len(Q))),
       t_poch - 0.12))
g.sfx("pop", t_kup - 0.35); g.sfx("click-soft", t_kurs); g.sfx("pop", t_thr - 0.25); g.sfx("typing", t_yak)
BLACKOUT.append((t_yak - 0.03, t_poch - 0.03))          # the post types it

# 3 · ABOVE — «почекай хвилинку»: a stopwatch ----------------------------------
t_tomu = S(u"Тому", 8.99)
F.append(u'<svg class="sk" id="skF" width="1080" height="1920" viewBox="0 0 1080 1920"></svg>')
js(u'''
  sketch("sw", "skF");
  ell("sw", 540, 490, 250, 250, {seed: 3});
  ln("sw", 540, 365, 540, 338, {seed: 5}); box("sw", 512, 306, 56, 30, {seed: 7, r: 10});
  ln("sw", 540, 395, 540, 412, {seed: 9}); ln("sw", 635, 490, 618, 490, {seed: 11});
  ln("sw", 540, 585, 540, 568, {seed: 13}); ln("sw", 445, 490, 462, 490, {seed: 15});
  ln("sw", 540, 490, 588, 418, {seed: 17, strokeWidth: 6});
  draw("sw", %.3f, .4);
  erase("sw", %.3f);
''' % (t_poch, t_tomu - 0.2))
g.sfx("click-soft", t_poch)

# 4 · ABOVE — the playlist card ------------------------------------------------
t_zn, t_mk, t_po = S(u"зняла", 9.51), S(u"міні-курс", 9.91), S(u"Клоду", 10.73)
t_ukr, t_bez, t_yt = S(u"українською", 11.27), S(u"безкоштовно", 11.97), S(u"Ютубі.", 12.81)
t_try, t_baz, t_kl = S(u"Три", 13.49), S(u"базу,", 15.36), S(u"Клодом.", 17.52)
t_od, t_kon = S(u"Одне", 18.23), S(u"конектори,", 19.15)
h0 = S(u"про", 19.84) - 0.15


def row(i, title):
    return (u'<div class="plr" id="pr%d"><span class="th"><b></b></span>'
            u'<span class="rw"><span class="gl"></span><span class="rt">%s</span></span></div>' % (i, esc(title)))


F.append(u'''
        <div id="pl" class="card hid" style="left:120px; top:300px; width:840px; padding:26px 32px;">
          <div class="plh"><span id="plyt" style="color:#DEBFBF; display:flex">%s</span>
            <span class="t">Міні-курс <span id="plt2" class="hid">по %s Claude</span></span></div>
          <div class="chips" style="margin-top:12px; gap:12px; height:48px">
            <span class="chip sm hid" id="plc1"><i></i>українською</span>
            <span class="chip sm hid" id="plc2"><i></i>безкоштовно</span>
            <span class="chip sm on hid" id="plc3"><i></i>база</span>
          </div>
          <div style="margin-top:8px">%s</div>
        </div>''' % (mark("youtube", 52), u'<span id="plcl" style="display:inline-block; vertical-align:-4px; color:#7A1424">%s</span>'
                     % mark("claude", 36), u"".join(row(i + 1, t) for i, t in
                                                   enumerate((u"Конектори", u"Скіли", u"Копірайтер")))))
js(u'''
  gsap.set("#plcl", {autoAlpha: 0});
  rise("#pl", %.3f);
  fadein("#plt2", %.3f, .3);
  pop("#plc1", %.3f); pop("#plc2", %.3f);
  tl.to("#plyt", {color: "#7A1424", duration: .2}, %.3f); tl.fromTo("#plyt", {scale: 1}, X({scale: 1.25, duration: .18, yoyo: true, repeat: 1}), %.3f);
  tl.fromTo("#pl .plr", {autoAlpha: 0, y: -16}, X({autoAlpha: 1, y: 0, duration: .45, ease: RISE, stagger: .16}), %.3f);
  pop("#plc3", %.3f);
  pop("#plcl", %.3f, .5);
  tl.to("#pr1", {backgroundColor: "#FFF0F0", duration: .25}, %.3f);
  tl.to("#pr1 .th", {backgroundColor: "#7A1424", duration: .25}, %.3f);
  tl.to("#pr1 .gl", {autoAlpha: 0, duration: .15}, %.3f); tl.to("#pr1 .rt", {opacity: 1, duration: .25}, %.3f);
  sink("#pl", %.3f);
''' % (t_zn - 0.25, t_po, t_ukr, t_bez, t_yt, t_yt, t_try - 0.05, t_baz, t_kl, t_od, t_od,
       t_kon - 0.05, t_kon - 0.05, h0 - 0.1))
g.sfx("pop", t_zn - 0.25); g.sfx("click-soft", t_ukr); g.sfx("pop", t_yt)
g.sfx("pop", t_try - 0.05); g.sfx("click-soft", t_kon)
BLACKOUT.append((t_ukr - 0.03, S(u"на", 12.63) - 0.03))   # the chips say it

# 5 · HALF — 1 Конектори: твій ШІ gets hands · 2 Скіли: a new one, in the video --
h1 = S(u"І", 30.43) - 0.15
HALF.append((h0, h1))
t_te, t_pid, t_daty = S(u"те,", 20.12), S(u"підключити,", 20.58), S(u"дати", 21.33)
t_pot = S(u"потужні", 23.19)
t_dr, t_sk = S(u"Друге", 24.45), S(u"скіли.", 25.19)
t_sho, t_tak, t_stv = S(u"Що", 25.88), S(u"таке?", 26.22), S(u"створити?", 26.90)
t_uv, t_stvm, t_nov = S(u"у", 28.18), S(u"створюємо", 28.86), S(u"новий", 29.70)
P.append(u'''
        <div class="hd hid" id="hd1"><span class="th"><b></b></span>
          <span class="rw"><span class="rt" style="opacity:1">Конектори</span></span></div>
        <div class="hd hid" id="hd2"><span class="th"><b></b></span>
          <span class="rw"><span class="gl"></span><span class="rt">Скіли</span></span></div>
        <svg class="sk" id="skP" width="1080" height="1240" viewBox="0 0 1080 1240"></svg>''')
js(u'''
  rise("#hd1", %.3f);
  sketch("k1", "skP"); box("k1", 100, 470, 300, 170, {seed: 21}); label("k1", 250, 572, "твій ШІ", {size: 54});
  draw("k1", %.3f, .55);
  sketch("k2", "skP");
  box("k2", 690, 395, 290, 100, {seed: 23, r: 24}); label("k2", 835, 460, "Gmail", {size: 46});
  box("k2", 690, 530, 290, 100, {seed: 25, r: 24}); label("k2", 835, 595, "Календар", {size: 46});
  box("k2", 690, 665, 290, 100, {seed: 27, r: 24}); label("k2", 835, 730, "Notion", {size: 46});
  draw("k2", %.3f, .4);
  sketch("k3", "skP");
  arrow("k3", 412, 515, 676, 447, {seed: 31, bend: .1}); arrow("k3", 412, 555, 676, 580, {seed: 33, bend: .06});
  arrow("k3", 412, 595, 676, 712, {seed: 35, bend: -.06});
  draw("k3", %.3f, .45);
  sketch("k4", "skP"); label("k4", 500, 800, "потужні руки", {size: 58, color: "#7A1424"});
  under("k4", 330, 818, 670, {stroke: "#7A1424", seed: 37});
  draw("k4", %.3f, .45);
  erase("k1", %.3f); erase("k2", %.3f); erase("k3", %.3f); erase("k4", %.3f); sink("#hd1", %.3f);
  rise("#hd2", %.3f);
  tl.to("#hd2 .gl", {autoAlpha: 0, duration: .15}, %.3f); tl.to("#hd2 .rt", {opacity: 1, duration: .25}, %.3f);
  sketch("s1", "skP"); box("s1", 110, 430, 280, 330, {seed: 41});
  label("s1", 250, 510, "скіл", {size: 58});
  ln("s1", 150, 590, 350, 590, {seed: 43}); ln("s1", 150, 650, 350, 650, {seed: 45}); ln("s1", 150, 710, 300, 710, {seed: 47});
  draw("s1", %.3f, .45);
  sketch("s2", "skP"); label("s2", 470, 540, "?", {size: 120, color: "#7A1424"}); draw("s2", %.3f);
  sketch("s3", "skP"); arrow("s3", 408, 640, 600, 610, {seed: 51, bend: .1}); draw("s3", %.3f, .45);
  sketch("s4", "skP"); box("s4", 620, 420, 370, 300, {seed: 53});
  ln("s4", 700, 680, 960, 680, {seed: 55}); ell("s4", 760, 680, 20, 20, {seed: 57});
  _ink = SK.s4.ink; _add(SK.s4, SK.s4.rc.path("M652 664 L652 696 L678 680 Z", opt({seed: 59}, 59)));
  draw("s4", %.3f, .45);
  sketch("s5", "skP"); box("s5", 705, 450, 200, 190, {seed: 61, r: 20, fill: true}); draw("s5", %.3f, .5);
  sketch("s6", "skP"); label("s6", 805, 800, "новий скіл", {size: 56, color: "#7A1424"}); draw("s6", %.3f);
  erase("s1", %.3f); erase("s2", %.3f); erase("s3", %.3f); erase("s4", %.3f); erase("s5", %.3f); erase("s6", %.3f);
  sink("#hd2", %.3f);
''' % (h0 + 0.45, t_te - 0.05, t_pid - 0.15, t_daty - 0.1, t_pot - 0.2,
       t_dr - 0.2, t_dr - 0.2, t_dr - 0.2, t_dr - 0.2, t_dr - 0.2,
       t_dr, t_sk - 0.05, t_sk - 0.05,
       t_sho - 0.1, t_tak - 0.1, t_stv - 0.25, t_uv - 0.1, t_stvm - 0.05, t_nov - 0.05,
       h1, h1, h1, h1, h1, h1, h1))
g.sfx("whoosh-short", h0); g.sfx("click-soft", t_pot); g.sfx("pop", t_stvm)
g.sfx("whoosh-short", h1)

# 6 · ABOVE — back to the playlist: row 3 «Копірайтер» ------------------------
t_tr, t_kop, t_kld = S(u"третє", 30.81), S(u"копірайтера", 31.51), S(u"Клоді,", 33.01)
js(u'''
  tl.set("#pr1", {backgroundColor: "rgba(255,240,240,0)"}, %.3f);
  tl.set("#pr2 .th", {backgroundColor: "#7A1424"}, %.3f); tl.set("#pr2 .gl", {autoAlpha: 0}, %.3f);
  tl.set("#pr2 .rt", {opacity: 1}, %.3f);
  rise("#pl", %.3f);
  tl.to("#pr3", {backgroundColor: "#FFF0F0", duration: .25}, %.3f);
  tl.to("#pr3 .th", {backgroundColor: "#7A1424", duration: .25}, %.3f);
  tl.to("#pr3 .gl", {autoAlpha: 0, duration: .15}, %.3f); tl.to("#pr3 .rt", {opacity: 1, duration: .25}, %.3f);
  sink("#pl", %.3f);
''' % (h0 + 0.5, h0 + 0.5, h0 + 0.5, h0 + 0.5, t_tr - 0.15, t_tr, t_kop - 0.05, t_kop - 0.05, t_kop - 0.05,
       t_kld - 0.45))
g.sfx("pop", t_tr - 0.15)

# 7 · ABOVE — the copywriter writes in your style; then her own texts ---------
t_pys, t_tv, t_tekst = S(u"писати", 33.93), S(u"твоєму", 34.83), S(u"текст,", 36.40)
t_kor, t_sc, t_lid, t_pov, t_tak = (S(u"користуюсь", 38.00), S(u"сценаріїв,", 39.88), S(u"лід-магнітів,", 40.72),
                                    S(u"повідомлень", 41.77), S(u"так", 42.47))
t_end7 = E(u"далі.", 42.61) + 0.3
WL = (92, 84, 96, 62)
F.append(u'''
        <div id="cw" class="card hid" style="left:120px; top:300px; width:840px; height:370px; padding:30px 36px;">
          <div class="row" style="gap:16px; color:#7A1424">%s
            <span class="ttl" style="font-size:46px">Копірайтер</span>
            <span class="chip on hid" id="cwst" style="margin-left:auto; font-size:30px; padding:10px 22px"><i></i>твій стиль</span></div>
          <div id="cwa" style="margin-top:10px">%s</div>
          <div id="cwb" class="hid" style="position:absolute; left:36px; right:36px; top:126px">
            <span class="lbl">Пишу ним</span>
            <div class="chips" style="gap:12px">
              <span class="chip hid" id="cwc1"><i></i>сценарії</span>
              <span class="chip hid" id="cwc2"><i></i>лід-магніти</span>
              <span class="chip hid" id="cwc3"><i></i>повідомлення</span>
              <span class="chip hid" id="cwc4" style="font-weight:700; letter-spacing:.1em">…</span>
            </div>
          </div>
        </div>''' % (mark("claude", 48), u"".join(u'<span class="wl" id="cwl%d"></span>' % i for i in range(len(WL)))))
lstep = (t_tekst + 0.35 - t_pys) / len(WL)
js(u'''
  rise("#cw", %.3f);
  %s
  pop("#cwst", %.3f);
  tl.to("#cwa", {autoAlpha: 0, duration: .3}, %.3f); fadein("#cwb", %.3f, .35);
  pop("#cwc1", %.3f); pop("#cwc2", %.3f); pop("#cwc3", %.3f); pop("#cwc4", %.3f);
  sink("#cw", %.3f);
''' % (t_kld - 0.2,
       " ".join(u'tl.to("#cwl%d", {width: "%d%%", duration: %.3f, ease: "none"}, %.3f);' % (i, w, lstep * 0.92, t_pys + i * lstep)
                for i, w in enumerate(WL)),
       t_tv, t_kor - 0.3, t_kor - 0.1, t_sc, t_lid, t_pov, t_tak, t_end7))
g.sfx("pop", t_kld - 0.2); g.sfx("typing", t_pys); g.sfx("pop", t_tv)
for t in (t_sc, t_lid, t_pov):
    g.sfx("click-soft", t)
BLACKOUT.append((t_tv - 0.03, S(u"будь-який", 35.84) - 0.03))      # the chip says it
BLACKOUT.append((t_sc - 0.03, S(u"і", 42.31) - 0.03))              # the chips say it

# 8 · ABOVE — CTA ----------------------------------------------------------------
t_otr, t_pos1 = S(u"отримати", 44.70), S(u"посилання,", 45.00)
t_pys2, t_kom = S(u"пиши", 46.39), S(u"коментарі,", 47.13)
t_pos2, t_ya = S(u"посилання", 48.35), S(u"А якщо", 51.83)
LINK = (u'<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" '
        u'stroke-linecap="round" stroke-linejoin="round"><path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/>'
        u'<path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/></svg>')
F.append(u'''
        <div id="plc" class="card hid" style="left:120px; top:300px; width:840px; padding:24px 30px;
             display:flex; align-items:center; gap:16px">
          <span style="color:#7A1424; display:flex">%s</span>
          <span style="font-weight:700; font-size:38px; letter-spacing:-0.02em">Міні-курс по Claude</span>
          <span class="chip hid" id="plk" style="margin-left:auto; font-size:30px; padding:10px 20px; gap:10px;
                color:#7A1424">%s<span style="color:#241919" id="plkt">посилання</span></span>
        </div>
        <div class="ctr" style="top:452px"><div id="cta" class="pill hid">Пиши YouTube в коментарі</div></div>''' % (
    mark("youtube", 56), LINK))
js(u'''
  rise("#plc", %.3f); pop("#plk", %.3f);
  pop("#cta", %.3f, .6);
  sketch("pt", "skF"); arrow("pt", 958, 770, 884, 592, {seed: 71, bend: .12}); draw("pt", %.3f, .45);
  tl.to("#plk", {backgroundColor: "#7A1424", borderColor: "#7A1424", color: "#FFFFFF", duration: .25}, %.3f);
  tl.to("#plkt", {color: "#FFFFFF", duration: .25}, %.3f);
  tl.fromTo("#plk", {scale: 1}, X({scale: 1.12, duration: .18, yoyo: true, repeat: 1}), %.3f);
  sink("#plc, #cta", %.3f); erase("pt", %.3f);
''' % (t_otr - 0.3, t_pos1, t_pys2, t_kom - 0.3, t_pos2, t_pos2, t_pos2, t_ya - 0.3, t_ya - 0.3))
g.sfx("pop", t_otr - 0.3); g.sfx("pop", t_pys2); g.sfx("notification", t_pos2)
BLACKOUT.append((t_pys2 - 0.03, S(u"і", 47.61) - 0.03))            # the pill says it

# 9 · ABOVE — «підпишись»: the follow button is pressed ------------------------
t_pidp = S(u"підпишись!", 53.71)
F.append(u'''
        <div class="ctr" style="top:372px"><div id="fb" class="pill light hid" style="font-weight:700; font-size:52px;
             padding:28px 64px; color:#7A1424; border:3px solid #7A1424">Підписатися</div></div>''')
js(u'''
  pop("#fb", %.3f);
  tl.to("#fb", {scale: .9, duration: .1, yoyo: true, repeat: 1, ease: "power1.inOut"}, %.3f);
  tl.to("#fb", {backgroundColor: "#7A1424", color: "#FFFFFF", duration: .2}, %.3f);
''' % (t_ya, t_pidp, t_pidp + 0.05))
g.sfx("pop", t_ya); g.sfx("click-soft", t_pidp)
BLACKOUT.append((t_pidp - 0.03, DUR))                              # the button says it

# ---------------------------------------------------------------- mattes for the half screens
for i, (a, b) in enumerate(HALF):
    g.matte("half%d" % (i + 1), round(a - 0.1, 3), round(b - a + 1.2, 3))
    js("  half(%.3f, %.3f);" % (a, b))
    PLACE.append((a + 0.4, b + 0.2, "bottom", 980))


def main():
    chunks = g.chunks(CAPS, place=PLACE)
    doc = g.document(title=u"Reel 52 — Якщо в тебе фомо на…", plate="assets/base.mp4",
                     behind="\n".join(B), panel="\n".join(P), front="\n".join(F), cover="\n".join(C),
                     js="\n".join(J), chunks=chunks, blackout=BLACKOUT, extra_css=EXTRA_CSS)
    g.write(HERE, doc)
    print("index.html  %d caption chunks, %d sfx cues, %d mattes" % (len(chunks), len(g.cues), len(g.mattes)))


main()
