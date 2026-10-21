# -*- coding: utf-8 -*-
"""Reel 42 — «Що від мене треба?». Posts 2026-10-19.

Google style + Excalidraw (STYLE.md §00), built on reel 41's skeleton.

The one object is **the client's checklist**: what she needs before she starts.
It is an empty list of five ghost rows that fills in, row by row, as she names
each item; the last item (rules for scripts) opens into its own card — a voice
note that goes into the skills. Then the split: on the panel the one thing the
client writes («про тебе», ти) gets structure and a place in the system, and
everything else in that system is hers (я). The client's part ends as two
buttons: окей / не окей. CTA above her.

  behind  «під / ключ»
  above   checklist «Від тебе»: доступи · блогерки · шрифти і кольори ·
          дизайн і монтаж · правила для сценаріїв
  above   voice note -> «скіли»
  half    ти: ядро «про тебе» -> структура -> місце в системі;
          я: аналіз контенту, стиль, скіли, підключення, тести
  above   результат -> окей / не окей
  above   CTA — «АІ-система під ключ», «Став + в коментарі», a red pointer

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

NN = "42"
CUT = json.load(io.open(os.path.join(ROOT, "work", "r" + NN, "cut.json"), encoding="utf-8"))
DUR = 45.483           # (1365 plate frames - 0.5) / 30
g = G(dur=DUR, reel=NN)

# whisper's spelling of what she plainly said -> her word (checked on the plate)
FIX = {
    u"працювати": u"працювати.", u"Доступы": u"доступи", u"зберемо.": u"зберемо",
    u"Єдине,": u"єдине,", u"то встав": u"то став", (u"є", 11.7): u"є,", u"інше": u"інше —",
    u"тести": u"тести —",
}
CAPS = load_caps(NN, FIX)
W = Words(CAPS)
S, E = W.s, W.e

# ---------------------------------------------------------------- the beats
B, P, F, C, J = [], [], [], [], []     # behind / panel / front / cover html, js
BLACKOUT = []
PLACE = []                             # caption placement over the half screens
HALF = []


def js(s):
    J.append(s)


EXTRA_CSS = u"""
    .ck { height: 48px; margin-top: 10px; }
    .ck .check { width: 44px; height: 44px; }
    .slot { position: relative; flex: 1; height: 48px; display: flex; align-items: center; }
    .gl { position: absolute; left: 0; top: 15px; }
    .tx { font-size: 36px; font-weight: 500; white-space: nowrap; color: var(--on-surface); }
    .vis { display: flex; align-items: center; gap: 10px; margin-left: auto; }
    .vis .mark { color: var(--primary); }
    .sw { position: relative; width: 36px; height: 36px; flex: none; }
    .sw b { position: absolute; inset: 0; border-radius: 50%; border: 3px dashed var(--outline-var); }
    .sw i { position: absolute; inset: 0; border-radius: 50%; }
    .tile { position: relative; width: 40px; height: 50px; border-radius: 10px; flex: none;
            background: #fff; border: 3px solid var(--outline-var); overflow: hidden; }
    .tile u { position: absolute; left: 5px; right: 5px; top: 6px; height: 8px; border-radius: 4px;
              background: var(--primary); }
    .tile s { position: absolute; left: 5px; right: 9px; height: 5px; border-radius: 3px;
              background: #EFE3E3; }
    .wave { display: flex; align-items: center; gap: 5px; }
    .wave span { display: block; width: 7px; border-radius: 4px; background: var(--primary); }
    .btn { position: relative; display: inline-flex; align-items: center; gap: 14px; border-radius: 999px;
           padding: 18px 44px; font-weight: 500; font-size: 42px; }
    .btn.ok { background: var(--primary); color: #fff;
              box-shadow: 0 1px 3px rgba(36,25,25,.12), 0 10px 30px rgba(122,20,36,.22); }
    .btn.no { background: #fff; color: var(--on-surface); border: 3px solid var(--outline-var); }
"""

KEY = (u'<svg width="44" height="44" viewBox="0 0 44 44"><circle cx="14" cy="22" r="9" fill="none" '
       u'stroke="#7A1424" stroke-width="5"/><path d="M23 22 H40 M33 22 V30 M39 22 V28" fill="none" '
       u'stroke="#7A1424" stroke-width="5" stroke-linecap="round"/></svg>')
AVA = (u'<svg width="44" height="44" viewBox="0 0 44 44" style="margin-left:-12px"><circle cx="22" cy="22" r="20" '
       u'fill="#FFF0F0" stroke="#DEBFBF" stroke-width="3"/><circle cx="22" cy="17" r="7.5" fill="#7A1424"/>'
       u'<path d="M9 36 C11 26 33 26 35 36 Z" fill="#7A1424"/></svg>')
HEART = (u'<svg width="40" height="40" viewBox="0 0 40 40"><path d="M20 35 C6 25 2 18 4 12 C6 5 15 4 20 11 '
         u'C25 4 34 5 36 12 C38 18 34 25 20 35 Z" fill="#7A1424"/></svg>')
PLAY = (u'<svg width="%d" height="%d" viewBox="0 0 72 72"><circle cx="36" cy="36" r="36" fill="#7A1424"/>'
        u'<path d="M29 22 L52 36 L29 50 Z" fill="#fff"/></svg>')
WAVE_H = [18, 30, 46, 26, 54, 38, 22, 48, 60, 34, 20, 42, 56, 30, 16, 38, 50, 26, 44, 20, 32, 14]


def tile(i, play=False):
    if play:
        return (u'<span class="tile" id="%s" style="border-color:#7A1424"><svg width="34" height="44" '
                u'viewBox="0 0 34 44" style="position:absolute;left:0;top:0"><path d="M12 14 L25 22 L12 30 Z" '
                u'fill="#7A1424"/></svg></span>' % i)
    return (u'<span class="tile" id="%s"><u></u><s style="top:21px"></s><s style="top:30px;right:14px"></s>'
            u'<s style="top:39px"></s></span>' % i)


# 1 · BEHIND — «під ключ» ------------------------------------------------------
t_pid, t_kl = S(u"під", 1.46), S(u"ключ,", 1.62)
t_pr = S(u"Перше", 4.56)
b_out = t_pr - 0.45
B.append(u'''
        <div id="bw1" class="big hid" style="top:320px; font-size:240px">під</div>
        <div id="bw2" class="big hid" style="top:536px; font-size:240px">ключ</div>''')
m0, m1 = t_pid - 0.35, b_out + 0.45
g.matte("key", round(m0, 3), round(m1 - m0, 3))
js(u'''
  rise("#bw1", %.3f); rise("#bw2", %.3f);
  sink("#bw1, #bw2", %.3f);
''' % (t_pid - 0.15, t_kl, b_out))
g.sfx("whoosh-short", t_pid - 0.2)

# 2 · ABOVE — the checklist fills in -------------------------------------------
t_dos, t_ak = S(u"доступи", 5.33), S(u"до акаунтів.", 5.88)
t_bl, t_dyv, t_pod = S(u"блогерів,", 7.03), S(u"дивишся", 8.01), S(u"подобаються.", 8.95)
t_shr, t_kol = S(u"шрифти", 10.10), S(u"і кольори,", 10.52)
t_nem, t_zb, t_raz = S(u"немає,", 12.12), S(u"зберемо", 13.22), S(u"разом.", 13.62)
t_pry, t_diz, t_mon, t_pod2 = S(u"Приклади", 14.26), S(u"дизайну", 14.70), S(u"і монтажу,", 15.10), S(u"подобаються.", 16.02)
t_prav, t_sc = S(u"правила,", 18.15), S(u"сценарій,", 19.15)
t_toty = S(u"то ти", 19.65)
ROWS = [
    (u"доступи до акаунтів", 290,
     u'%s<span class="hid" id="v1a">%s</span><span class="hid" id="v1b">%s</span><span class="hid" id="v1c">%s</span>'
     % (u'<span class="hid" id="v1k">%s</span>' % KEY, mark("instagram", 36), mark("threads", 36), mark("telegram", 36))),
    (u"блогери, які подобаються", 380,
     u'<span class="row" style="gap:0">%s</span><span class="hid" id="v2h">%s</span>'
     % (u"".join(u'<span class="hid" id="v2a%d">%s</span>' % (i, AVA) for i in range(3)), HEART)),
    (u"шрифти і кольори", 260,
     u'<span class="hid" id="v3a" style="font-weight:700;font-size:38px;color:#7A1424;margin-right:6px">Aa</span>%s'
     % u"".join(u'<span class="sw hid" id="v3s%d"><b></b><i style="background:%s"></i></span>' % (i, c)
                for i, c in enumerate(("#7A1424", "#DEBFBF", "#F2C7CA")))),
    (u"приклади дизайну і монтажу", 420,
     u'<span class="hid" id="v4a">%s</span><span class="hid" id="v4b">%s</span><span class="hid" id="v4c">%s</span>'
     % (tile("v4t0"), tile("v4t1"), tile("v4t2", play=True))),
    (u"правила для сценаріїв", 330,
     u'<span class="hid" id="v5a" style="display:flex;align-items:center;gap:10px;background:#FFF0F0;border-radius:24px;'
     u'padding:4px 16px 4px 4px">%s<span class="wave">%s</span></span>'
     % (PLAY % (40, 40), u"".join(u'<span style="height:%dpx;width:5px"></span>' % h for h in (12, 22, 30, 18, 26, 14)))),
]
rows = u"".join(u'''
          <div class="row ck"><span class="check" id="r%dk"></span>
            <span class="slot"><span class="line gl" id="r%dg" style="width:%dpx"></span><span class="tx hid" id="r%dt">%s</span></span>
            <span class="vis">%s</span></div>''' % (i, i, w, i, esc(t), v) for i, (t, w, v) in enumerate(ROWS))
F.append(u'''
        <div id="ckl" class="card hid" style="left:120px; top:298px; width:840px; padding:24px 36px 26px;">
          <span class="lbl" style="margin-bottom:6px">Від тебе</span>%s
        </div>''' % rows)


def item(i, t):      # a ghost row turns into its words
    return u'out("#r%dg", %.3f); rise("#r%dt", %.3f, 20);' % (i, t - 0.1, i, t - 0.05)


def tick(i, t):
    return u'tl.set("#r%dk", {className: "check on"}, %.3f); pop("#r%dk", %.3f, .45);' % (i, t, i, t)


ck_out = t_toty - 0.2
js(u'''
  rise("#ckl", %.3f);
  %s pop("#v1k", %.3f); pop("#v1a", %.3f); pop("#v1b", %.3f); pop("#v1c", %.3f); %s
  %s pop("#v2a0", %.3f); pop("#v2a1", %.3f); pop("#v2a2", %.3f); pop("#v2h", %.3f); %s
  %s pop("#v3a", %.3f); pop("#v3s0", %.3f); pop("#v3s1", %.3f); pop("#v3s2", %.3f);
  tl.to("#v3s0 i, #v3s1 i, #v3s2 i", {scale: 0, duration: .3, ease: "power2.in", stagger: .08}, %.3f);
  tl.to("#v3s0 i, #v3s1 i, #v3s2 i", {scale: 1, duration: .5, ease: POP, stagger: .15}, %.3f); %s
  %s pop("#v4a", %.3f); pop("#v4b", %.3f); pop("#v4c", %.3f); %s
  %s pop("#v5a", %.3f); %s
  sink("#ckl", %.3f);
''' % (t_pr - 0.2,
       item(0, t_dos), t_dos + 0.1, t_ak, t_ak + 0.15, t_ak + 0.3, tick(0, t_ak + 0.55),
       item(1, t_bl), t_dyv - 0.1, t_dyv + 0.05, t_dyv + 0.2, t_pod, tick(1, t_pod + 0.4),
       item(2, t_shr), t_shr + 0.2, t_kol + 0.05, t_kol + 0.2, t_kol + 0.35, t_nem, t_zb, tick(2, t_raz),
       item(3, t_pry), t_diz, t_diz + 0.2, t_mon + 0.05, tick(3, t_pod2),
       item(4, t_prav), t_sc - 0.1, tick(4, t_sc + 0.2),
       ck_out))
g.sfx("pop", t_pr - 0.2)
for t in (t_bl, t_shr, t_pry, t_prav):
    g.sfx("click-soft", t)
g.sfx("pop", t_zb)

# 3 · ABOVE — the voice note goes into the skills ------------------------------
t_gol, t_poya = S(u"голосове", 20.65), S(u"пояснюєш,", 21.25)
t_dod, t_potr, t_skil = S(u"додаю", 22.95), S(u"потрібні", 24.03), S(u"скіли.", 24.39)
wave = u"".join(u'<span style="height:%dpx"></span>' % h for h in WAVE_H)
F.append(u'''
        <div id="vc" class="card hid" style="left:120px; top:320px; width:840px; height:330px;">
          <span class="lbl">Правила для сценаріїв</span>
          <div id="vb" class="hid" style="position:absolute; left:36px; top:126px; width:430px; height:124px;
               border-radius:62px; background:#FFF0F0; display:flex; align-items:center; gap:18px; padding:0 26px 0 26px;">
            %s<span class="wave" id="vw">%s</span>
          </div>
          <div id="vs" class="hid" style="position:absolute; left:576px; top:96px; width:228px; height:190px;
               border-radius:28px; border:3px solid #DEBFBF; background:#FFF8F7; padding:22px 24px;">
            <span style="display:block; font-weight:700; font-size:44px; letter-spacing:-0.02em; color:#7A1424">скіли</span>
            <span class="line" style="margin-top:16px; width:90%%"></span>
            <span class="line" style="margin-top:12px; width:70%%"></span>
            <span id="vsw" class="wave hid" style="margin-top:12px; gap:4px">%s</span>
          </div>
        </div>''' % (PLAY % (76, 76), wave,
                     u"".join(u'<span style="height:%dpx;width:6px"></span>' % h for h in (10, 20, 28, 16, 24, 12, 20, 14))))
F.append(u'<svg class="sk" id="skF" width="1080" height="1920" viewBox="0 0 1080 1920"></svg>')
v_out = E(u"скіли.", 24.39) + 0.12
js(u'''
  rise("#vc", %.3f);
  pop("#vb", %.3f);
  tl.fromTo("#vw span", {scaleY: .15}, X({scaleY: 1, duration: .35, ease: RISE, stagger: .045}), %.3f);
  sketch("va", "skF"); arrow("va", 596, 508, 688, 508, {stroke: "#7A1424", strokeWidth: 5, seed: 5, bend: .18});
  draw("va", %.3f, .45);
  pop("#vs", %.3f);
  pop("#vsw", %.3f, .45);
  sink("#vc", %.3f); erase("va", %.3f);
''' % (ck_out + 0.2, t_gol - 0.1, t_poya - 0.1, t_dod - 0.5, t_dod, t_skil, v_out, v_out))
g.sfx("pop", t_gol - 0.1); g.sfx("pop", t_dod); g.sfx("click-soft", t_skil)

# 4 · HALF — ти: the core; я: everything else in the system ---------------------
h0 = S(u"сама", 26.56) - 0.4
h1 = h0 + 11.95
HALF.append((h0, h1))
P.append(u'<svg class="sk" id="skP" width="1080" height="1240" viewBox="0 0 1080 1240"></svg>')
t_ty = S(u"ти,", 26.80)
t_yad, t_pro = S(u"ядро", 27.63), S(u"«про", 28.03)
t_kra = S(u"краще", 29.23)
t_str = S(u"структуру", 31.94)
t_mis, t_sys = S(u"місце", 32.68), S(u"системі.", 33.16)
t_vse = S(u"Все", 33.80)
t_an, t_st, t_sk, t_pk, t_ts = (S(u"аналіз", 34.42), S(u"стиль,", 35.41), S(u"скіли,", 35.77),
                                S(u"підключення,", 36.19), S(u"тести", 36.88))
t_moya = S(u"моя", 37.52)
js(u'''
  sketch("d1", "skP"); box("d1", 96, 390, 340, 290, {seed: 3});
  draw("d1", %.3f, .6);
  sketch("d1s", "skP");
  _add(SK.d1s, SK.d1s.rc.curve([[136, 560], [180, 545], [220, 570], [270, 548], [320, 568], [390, 552]], opt({seed: 5}, 5)));
  _add(SK.d1s, SK.d1s.rc.curve([[136, 610], [170, 596], [230, 620], [280, 598], [350, 615]], opt({seed: 7}, 7)));
  draw("d1s", %.3f, .45);
  sketch("d1t", "skP"); label("d1t", 266, 350, "ти", {size: 64, color: "#7A1424"}); draw("d1t", %.3f);
  sketch("d2", "skP"); label("d2", 266, 470, "про тебе", {size: 54}); label("d2", 266, 515, "ядро", {size: 36, color: "#574142"});
  draw("d2", %.3f);
  sketch("d3", "skP"); under("d3", 160, 486, 372, {stroke: "#7A1424", strokeWidth: 5, seed: 9}); draw("d3", %.3f, .5);
  erase("d1s", %.3f);
  sketch("d4", "skP");
  ln("d4", 136, 566, 396, 566, {seed: 11, roughness: 1.6}); ln("d4", 136, 612, 396, 612, {seed: 13, roughness: 1.6});
  ln("d4", 136, 658, 330, 658, {seed: 15, roughness: 1.6});
  draw("d4", %.3f, .35);
  sketch("d5", "skP"); arrow("d5", 446, 520, 528, 520, {seed: 17, bend: .2}); draw("d5", %.3f, .45);
  sketch("d6", "skP"); box("d6", 540, 390, 450, 420, {seed: 19});
  label("d6", 765, 440, "система", {size: 42, color: "#574142"});
  box("d6", 576, 462, 380, 64, {seed: 21, r: 20, fill: true}); label("d6", 766, 506, "про тебе", {size: 36});
  draw("d6", %.3f, .55);
  sketch("d7", "skP"); label("d7", 765, 350, "я", {size: 64, color: "#7A1424"}); draw("d7", %.3f);
  %s
  sketch("d9", "skP"); ell("d9", 765, 330, 120, 96, {stroke: "#7A1424", strokeWidth: 5, seed: 41}); draw("d9", %.3f, .5);
  erase("d1", %.3f); erase("d1t", %.3f); erase("d2", %.3f); erase("d3", %.3f); erase("d4", %.3f);
  erase("d5", %.3f); erase("d6", %.3f); erase("d7", %.3f); erase("d9", %.3f);
''' % (h0 + 0.35, h0 + 0.8, t_ty, t_pro - 0.05, t_kra, t_str - 0.35, t_str - 0.25, t_mis - 0.45, t_sys - 0.6,
       t_vse,
       u"\n  ".join(u'sketch("d8%d", "skP"); label("d8%d", 586, %d, "%s", {size: 40, anchor: "start"}); '
                    u'draw("d8%d", %.3f);' % (i, i, 578 + 50 * i, txt, i, t)
                    for i, (txt, t) in enumerate(((u"аналіз контенту", t_an), (u"стиль", t_st), (u"скіли", t_sk),
                                                  (u"підключення", t_pk), (u"тести", t_ts)))),
       t_moya - 0.3,
       h1, h1, h1, h1, h1, h1, h1, h1, h1))
js(u"  " + u" ".join(u'erase("d8%d", %.3f);' % (i, h1) for i in range(5)))
g.sfx("whoosh-short", h0); g.sfx("whoosh-short", h1)
for t in (t_ty, t_pro, t_str, t_an, t_ts):
    g.sfx("click-soft", t)
g.sfx("pop", t_sys - 0.1)
BLACKOUT.append((t_st - 0.05, t_ts - 0.05))         # the system's own labels say it

# 5 · ABOVE — the result, and the client's two buttons -------------------------
t_pod3, t_rez = S(u"подивитись", 39.27), S(u"результат", 39.83)
t_ok, t_ne = S(u"окей", 40.87), S(u"не", 41.42)
t_tomu = S(u"Тому", 41.93)
F.append(u'''
        <div id="rc" class="card hid" style="left:120px; top:318px; width:840px; padding:28px 36px 30px;">
          <span class="lbl" style="margin-bottom:16px">Результат</span>
          <div class="row" style="gap:16px">%s</div>
          <div class="row" style="gap:20px; margin-top:22px; justify-content:center">
            <span class="btn ok hid" id="rok"><svg width="34" height="34" viewBox="0 0 34 34"><path d="M6 18 L14 26 L29 8"
              fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>окей</span>
            <span class="btn no hid" id="rno">не окей</span>
          </div>
        </div>''' % u"".join(
    u'''<span class="hid" id="rt%d" style="position:relative; display:block; width:180px; height:150px; border-radius:22px;
         background:#fff; border:3px solid #DEBFBF; overflow:hidden">
         <span style="position:absolute; left:16px; top:16px; width:60%%; height:16px; border-radius:6px; background:#7A1424"></span>
         <span class="line" style="position:absolute; left:16px; top:46px; width:80%%; height:12px"></span>
         <span class="line" style="position:absolute; left:16px; top:68px; width:56%%; height:12px"></span>
         <span style="position:absolute; left:16px; right:16px; bottom:14px; height:44px; border-radius:12px; background:#FFF0F0"></span>%s
       </span>''' % (i, u'<svg width="40" height="40" viewBox="0 0 72 72" style="position:absolute;right:20px;bottom:16px">'
                        u'<path d="M24 16 L56 36 L24 56 Z" fill="#7A1424"/></svg>' if i == 3 else u"")
    for i in range(4)))
r_out = t_tomu - 0.1
js(u'''
  rise("#rc", %.3f);
  pop("#rt0", %.3f); pop("#rt1", %.3f); pop("#rt2", %.3f); pop("#rt3", %.3f);
  pop("#rok", %.3f); pop("#rno", %.3f);
  sink("#rc", %.3f);
''' % (t_pod3 - 0.25, t_rez - 0.1, t_rez + 0.05, t_rez + 0.2, t_rez + 0.35, t_ok - 0.05, t_ne - 0.05, r_out))
g.sfx("pop", t_pod3 - 0.25); g.sfx("click-soft", t_ok)
BLACKOUT.append((t_ok - 0.05, t_tomu - 0.05))      # the buttons say it

# 6 · ABOVE — CTA ---------------------------------------------------------------
t_tsya, t_stav = S(u"ця", 42.88), S(u"то став", 44.16)
F.append(u'''
        <div id="ct1" class="hid" style="position:absolute; left:90px; width:900px; top:340px; display:flex; justify-content:center">
          <span class="pill light" style="position:relative; font-weight:700; color:#7A1424">АІ-система під ключ</span></div>
        <div id="ct2" class="hid" style="position:absolute; left:90px; width:900px; top:476px; display:flex; justify-content:center">
          <span class="pill" style="position:relative">Став + в коментарі</span></div>''')
js(u'''
  pop("#ct1", %.3f);
  pop("#ct2", %.3f, .6);
  sketch("ca", "skF"); arrow("ca", 930, 760, 836, 618, {stroke: "#7A1424", strokeWidth: 5, seed: 97});
  draw("ca", %.3f, .5);
''' % (t_tsya - 0.05, t_stav + 0.05, t_stav + 0.5))
g.sfx("pop", t_tsya - 0.05); g.sfx("pop", t_stav + 0.05)
BLACKOUT.append((t_stav - 0.05, DUR))               # the pill says it

# ---------------------------------------------------------------- mattes for the half screens
for i, (a, b) in enumerate(HALF):
    g.matte("half%d" % (i + 1), round(a - 0.1, 3), round(b - a + 1.2, 3))
    js("  half(%.3f, %.3f);" % (a, b))
    PLACE.append((a + 0.4, b + 0.2, "bottom", 980))


def main():
    if "--words" in sys.argv:
        print(" ".join(u"%s/%.1f" % (c["w"], c["s"]) for c in CAPS))
    # key-word pills: the noun she leans on, not whisper's merged pairs
    keys = {S(u"треба", 2.61): True, S(u"доступи", 5.33): True, S(u"шрифти", 10.10): True, S(u"немає,", 12.12): True,
            S(u"дизайну", 14.70): True, S(u"голосове", 20.65): True, S(u"скіли.", 24.39): True,
            S(u"ядро", 27.63): True, S(u"аналіз", 34.42): True, S(u"знає.", 30.65): True}
    chunks = g.chunks(CAPS, keys=keys, place=PLACE)
    if "--chunks" in sys.argv:
        for n, c in enumerate(chunks):
            print(n, "%.2f-%.2f" % (c["s"], c["e"]), " ".join(w["w"] for w in c["words"]),
                  "| key:", c["words"][c["key"]]["w"] if c["key"] is not None else "-", c["pos"])
    doc = g.document(title=u"Reel 42 — Що від мене треба?", plate="assets/base.mp4",
                     behind="\n".join(B), panel="\n".join(P), front="\n".join(F), cover="\n".join(C),
                     js="\n".join(J), chunks=chunks, blackout=BLACKOUT, extra_css=EXTRA_CSS)
    g.write(HERE, doc)
    print("index.html  %d caption chunks, %d sfx cues, %d mattes" % (len(chunks), len(g.cues), len(g.mattes)))


main()
