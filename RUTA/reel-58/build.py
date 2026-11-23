# -*- coding: utf-8 -*-
"""Reel 58 — «Автоматизація без бану». Batch 2026-11-20 (raw 20261120_133702).
STYLE.md §00 + her review of reel 61 (2026-11-23): natural editing, one
meaningful moment per sentence group, reel-61's skeleton and idioms.

Beats: behind «Без бану» (cover) -> shuffle «писати лідам / нагадувати /
розсилати повідомлення» -> behind «Claude» -> FULL A: Claude's app with its
browser, the camera into the tab strip on «хром» -> her face -> FULL B: the same
window: instagram.com, log in, the prompt typed into Claude and sent, then the
browser walks Direct: search, a lead, a message, sent -> glass «Дію
заблоковано» shakes on «по шапці» -> HALF: the pause scheme (дія · 30-40 с ·
дія · 30-40 с · дія; довше vs заблокували, loop round довше) -> FULL C: the
same window: a DM with only the name -> her profile, the bio -> the bio written
into the message, «скрипт» lights in Claude -> CTA pill «Підпишись».

usage: python3 build.py   (then: sh work/b1021/mattes.sh 58; python3 tools/sfx.py mix 58)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
from gstyle import G, Words, load_caps, mark  # noqa: E402

NN = "58"
DUR = 90.017           # (2701 plate frames - 0.5) / 30
g = G(dur=DUR, reel=NN)

FIX = {
    u"можу": u"може", u"про чось,": u"про щось,", u"Перша": u"Перше", u"цепь": u"це",
    u"пауза": u"пауза,", u"Ніж": u"між", u"Входиш": u"входиш", u"Тут": u"тут", u"Не": u"не",
    u"Так": u"так", u"корисно": u"корисно,", u"\"довше\"": u"«довше»",
    u"\"заблокували": u"«заблокували", u"акаунт\"": u"акаунт»,", u"Ми": u"ми",
}
CAPS = load_caps(NN, FIX)
W = Words(CAPS)
S, E = W.s, W.e

B, P, F, C, J = [], [], [], [], []
BLACKOUT, PLACE, HALF = [], [], []


def js(s):
    J.append(s)


P.append(u'<svg class="sk" id="skP" data-layout-allow-occlusion width="1080" height="1240" viewBox="0 0 1080 1240"></svg>')
g.PANEL_TOP = 820

EXTRA = u'''
    /* her glass (reel 61): the Instagram warning over her footage */
    .alert { left: 0; right: 0; margin: auto; width: 560px; top: 320px; padding: 30px 34px 0;
             text-align: center; overflow: hidden; }
    .alert b { display: block; font-size: 38px; font-weight: 700; color: #1f1f1f; }
    .alert span { display: block; font-size: 28px; color: #574142; margin: 10px 0 24px; }
    .alert em { display: block; font-style: normal; font-size: 30px; font-weight: 700; color: #0095F6;
                border-top: 1px solid rgba(36,25,25,.14); padding: 18px 0 20px; margin: 0 -34px; }
'''

# 1 · BEHIND — «Без бану», the cover frame ------------------------------------------
t_zhod, e_zabl = S(u"жодного", 4.93), E(u"заблокував.", 7.05)
B.append(u'        <div id="bw1" class="big hid" data-layout-allow-occlusion style="top:470px; font-size:210px">Без бану</div>')
g.matte("b1", round(t_zhod - 0.45, 3), round(e_zabl - t_zhod + 0.9, 3))
js(u'  rise("#bw1", %.3f); sink("#bw1", %.3f);' % (t_zhod - 0.15, e_zabl + 0.05))
g.sfx("whoosh-short", t_zhod - 0.15)

# 2 · ABOVE — what the method is for: a shuffle ----------------------------------
CH = [(u"писати лідам", S(u"писати", 11.65) - 0.1), (u"нагадувати", S(u"нагадувати", 12.39) - 0.1),
      (u"розсилати повідомлення", S(u"розсилати", 13.44) - 0.1)]
for i, (txt, _) in enumerate(CH):
    F.append(u'        <div id="sh%d" class="shuf hid"><span class="chip"><i></i>%s</span></div>' % (i, txt))
js(u'  shuffle([%s], [%s], %.3f);' % (", ".join('"#sh%d"' % i for i in range(len(CH))),
                                    ", ".join("%.3f" % t for _, t in CH), S(u"То", 14.53) + 0.5))
for _, t in CH:
    g.sfx("pop", t)

# 3 · BEHIND — «Claude» (the name) ---------------------------------------------------
t_cl, e_cl = S(u"Клод", 15.83), E(u"Клод", 15.83)
t_men = E(u"менеджер,", 18.26)
B.append(u'        <div id="bw2" class="big hid" data-layout-allow-occlusion style="top:470px; font-size:220px">Claude</div>')
g.matte("b2", round(t_cl - 0.5, 3), round(t_men - t_cl + 0.9, 3))
js(u'  rise("#bw2", %.3f); sink("#bw2", %.3f);' % (t_cl - 0.25, t_men))
g.sfx("whoosh-short", t_cl - 0.25)
BLACKOUT.append((t_cl - 0.03, e_cl))

# ---------------------------------------------------------------- the window (FULL A, B, C)
# Claude's desktop app: chat on the left, its browser on the right. Rebuilt as
# clean HTML, labels only what she says; the leads and messages are a demo.
CLAUDE = mark("claude", 18, "mk")
IG = mark("instagram", 22, "mk")
C.append(u"""
        <div id="stage">
          <div id="win">
            <div class="tb"><i></i><i></i><i></i><span>%(claude)s Claude</span></div>
            <div class="chat">
              <div id="ubub" class="ub hid">Розішли повідомлення лідам зі списку</div>
              <div id="ans" class="ans hid">%(claude)s<span>Працюю у браузері…</span></div>
              <div id="scr" class="file hid"><b>≡</b>мій скрипт</div>
              <div class="inp"><span id="ph">Напиши Claude…</span><span id="typ" class="typ">Розішли повідомлення лідам зі списку</span><u id="sendc">↑</u></div>
            </div>
            <div class="br">
              <div class="tabs"><div class="tab"><span id="tabt0">Нова вкладка</span><span id="tabt1" class="hid">%(ig)s Instagram</span></div></div>
              <div class="tool"><span class="nav">‹ ›&nbsp;↻</span><div id="omni" class="omni"><span id="url0">Пошук або URL</span><span id="url1" class="typ">instagram.com</span></div></div>
              <div class="pgs">
                <div id="p0" class="pg"><div class="srch">Пошук або URL</div></div>
                <div id="p1" class="pg hid">
                  <div class="igw" style="top:56px">Instagram</div>
                  <div class="fld" style="top:126px">Ім'я користувача</div>
                  <div class="fld" style="top:164px">Пароль</div>
                  <div id="login" class="blue" style="top:208px">Увійти</div>
                </div>
                <div id="p1b" class="pg hid">
                  <div class="igw" style="left:20px;top:14px;font-size:22px">Instagram</div>
                  <i class="av" style="left:492px;top:14px;width:28px;height:28px"></i>
                  <div class="stories"><i></i><i></i><i></i><i></i><i></i><i></i></div>
                  <div class="post"></div>
                </div>
                <div id="p2" class="pg hid">
                  <div class="list">
                    <div id="dsr" class="dsr"><span id="dsr0">Пошук</span><span id="dsr1" class="typ">olena</span></div>
                    <div id="r0" class="lr"><i class="av"></i>olena.interiors</div>
                    <div class="lr"><i class="av"></i>maria.studio</div>
                    <div class="lr"><i class="av"></i>kate.lashes</div>
                    <div class="lr"><i class="av"></i>anna.coach</div>
                  </div>
                  <div class="th">
                    <div class="thh"><i class="av"></i>olena.interiors</div>
                    <div id="sent" class="sent hid">Привіт, Олено! Маю для тебе пропозицію.</div>
                    <div id="cmp" class="cmp">
                      <span id="c0" class="ph2">Повідомлення…</span>
                      <span id="c1" class="typ">Привіт, Олено! Маю для тебе пропозицію.</span>
                      <span id="c2" class="hid">Привіт, <span id="nm" class="hl">Олено</span>! <span id="gen" class="hl">Маю для тебе пропозицію.</span></span>
                      <span id="c3" class="hid">Привіт, Олено! <span id="pers" class="hl">Бачу, ти робиш інтер'єри в Києві</span> — маю ідею для твоїх клієнтів.</span>
                      <u id="snd">Надіслати</u>
                    </div>
                  </div>
                </div>
                <div id="p3" class="pg hid">
                  <i class="av" style="left:44px;top:30px;width:86px;height:86px"></i>
                  <div class="hd3">olena.interiors <span class="b2">Повідомлення</span></div>
                  <div class="nm3">Олена</div>
                  <div id="bio" class="bio"><span>Дизайнерка інтер'єрів · Київ</span></div>
                  <div class="grid"><i></i><i></i><i></i><i></i><i></i><i></i></div>
                </div>
                <svg id="cur" class="cur hid" width="22" height="22" viewBox="0 0 24 24"><path d="M4 2l15 11-6.5 1.2L16 21l-3 1.4-3.4-6.6L4 20z" fill="#1f1f1f" stroke="#fff" stroke-width="1.5"/></svg>
              </div>
            </div>
          </div>
        </div>""" % {"claude": CLAUDE, "ig": IG})
EXTRA += u"""
    #cover { background: radial-gradient(120% 80% at 50% 35%, #FFFFFF 0%, #F6EFEF 70%, #F1E7E7 100%); }
    #stage { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; perspective: 2200px; }
    #win { position: absolute; left: 0; top: 0; width: 800px; height: 540px; background: #fff;
           border-radius: 14px; overflow: hidden; font-family: "Google Sans", sans-serif; color: #1f1f1f;
           box-shadow: 0 2px 6px rgba(36,25,25,.10), 0 30px 80px rgba(36,25,25,.22);
           transform-origin: 0 0; will-change: transform; }
    #win div, #win span, #win u, #win i { box-sizing: border-box; }
    .mk { vertical-align: -3px; }
    .tb { position: absolute; left: 0; top: 0; width: 800px; height: 34px; background: #F3F1EE;
          border-bottom: 1px solid #E6E2DD; }
    .tb i { position: absolute; top: 12px; width: 11px; height: 11px; border-radius: 50%; background: #D6D2CC; }
    .tb i:nth-child(1) { left: 14px; } .tb i:nth-child(2) { left: 31px; } .tb i:nth-child(3) { left: 48px; }
    .tb span { position: absolute; left: 0; right: 0; top: 8px; text-align: center; font-size: 13px; font-weight: 500; color: #3c3a37; }
    .tb .mk path, .ans .mk path { fill: #D97757; }
    .chat { position: absolute; left: 0; top: 34px; width: 262px; height: 506px; background: #FAF9F7;
            border-right: 1px solid #E6E2DD; }
    .ub { position: absolute; right: 12px; top: 18px; max-width: 200px; background: #EFECE6; border-radius: 12px;
          padding: 8px 11px; font-size: 11.5px; line-height: 1.35; }
    .ans { position: absolute; left: 12px; top: 74px; font-size: 11.5px; color: #3c3a37; display: flex; gap: 7px; align-items: center; }
    .file { position: absolute; left: 12px; top: 104px; border: 1px solid #E0DCD5; background: #fff; border-radius: 9px;
            padding: 7px 11px; font-size: 11.5px; display: flex; gap: 7px; align-items: center; }
    .file b { color: #D97757; }
    .inp { position: absolute; left: 10px; top: 436px; width: 242px; height: 58px; background: #fff;
           border: 1px solid #DEDAD3; border-radius: 14px; padding: 9px 36px 9px 11px; font-size: 11.5px; line-height: 1.35; }
    .inp #ph { position: absolute; left: 11px; top: 9px; color: #8a867f; }
    .inp u { position: absolute; right: 8px; bottom: 8px; width: 22px; height: 22px; border-radius: 7px;
             background: #E3B9A8; color: #fff; text-decoration: none; text-align: center; line-height: 22px; font-size: 13px; }
    .typ { clip-path: inset(0 100% 0 0); }
    .br { position: absolute; left: 262px; top: 34px; width: 538px; height: 506px; }
    .tabs { height: 30px; background: #E8E6E3; position: relative; }
    .tab { position: absolute; left: 8px; top: 5px; width: 168px; height: 25px; background: #fff; border-radius: 8px 8px 0 0;
           font-size: 11px; padding: 6px 12px; color: #3c4043; }
    .tab span { position: absolute; left: 12px; top: 5px; white-space: nowrap; }
    .tab .mk { width: 13px; height: 13px; vertical-align: -2px; }
    .tool { height: 34px; position: relative; border-bottom: 1px solid #E3E3E3; }
    .nav { position: absolute; left: 12px; top: 8px; font-size: 14px; color: #80868b; letter-spacing: 2px; }
    .omni { position: absolute; left: 70px; top: 5px; width: 452px; height: 24px; border-radius: 12px; background: #F1F3F4;
            font-size: 11.5px; padding: 5px 14px; color: #5f6368; }
    .omni span { position: absolute; left: 14px; top: 5px; }
    #url1 { color: #1f1f1f; }
    .pgs { position: absolute; left: 0; top: 64px; width: 538px; height: 442px; overflow: hidden; }
    .pg { position: absolute; inset: 0; background: #fff; }
    .pg > div, .pg > i { position: absolute; }
    .srch { left: 119px; top: 170px; width: 300px; height: 34px; border-radius: 17px; border: 1px solid #DADCE0;
            font-size: 12px; color: #80868b; padding: 9px 16px; }
    .igw { left: 0; right: 0; text-align: center; font-size: 30px; font-weight: 700; letter-spacing: -.02em; }
    .fld { left: 169px; width: 200px; height: 30px; border: 1px solid #DBDBDB; background: #FAFAFA; border-radius: 4px;
           font-size: 10.5px; color: #8e8e8e; padding: 8px 9px; }
    .blue { left: 169px; width: 200px; height: 30px; border-radius: 8px; background: #0095F6; color: #fff;
            font-size: 12px; font-weight: 700; text-align: center; line-height: 30px; }
    .av { display: inline-block; border-radius: 50%; background: linear-gradient(135deg, #E9DCD8, #CDB8B4); }
    .pg > .av { position: absolute; }
    .stories { left: 20px; top: 60px; display: flex; gap: 14px; }
    .stories i { width: 46px; height: 46px; border-radius: 50%; border: 2px solid #C9C9C9; background: #EEE; }
    .post { left: 119px; top: 128px; width: 300px; height: 300px; border-radius: 6px; background: #F0EEEE; }
    .list { left: 0; top: 0; width: 196px; height: 442px; border-right: 1px solid #EFEFEF; }
    .dsr { position: absolute; left: 12px; top: 12px; width: 172px; height: 26px; border-radius: 8px; background: #EFEFEF;
           font-size: 11px; color: #8e8e8e; }
    .dsr span { position: absolute; left: 11px; top: 6px; } #dsr1 { color: #1f1f1f; }
    .lr { position: absolute; left: 6px; width: 184px; height: 44px; border-radius: 8px; font-size: 11px; font-weight: 500;
          display: flex; align-items: center; gap: 9px; padding-left: 8px; }
    .lr .av { width: 30px; height: 30px; flex: none; }
    .lr:nth-child(2) { top: 50px; } .lr:nth-child(3) { top: 96px; } .lr:nth-child(4) { top: 142px; } .lr:nth-child(5) { top: 188px; }
    .th { position: absolute; left: 196px; top: 0; width: 342px; height: 442px; }
    .thh { position: absolute; left: 0; top: 0; width: 342px; height: 48px; border-bottom: 1px solid #EFEFEF;
           display: flex; align-items: center; gap: 9px; padding-left: 14px; font-size: 12px; font-weight: 700; }
    .thh .av { width: 28px; height: 28px; }
    .sent { position: absolute; right: 12px; top: 250px; max-width: 230px; background: #3797F0; color: #fff;
            border-radius: 16px; padding: 8px 12px; font-size: 11.5px; line-height: 1.35; }
    .cmp { position: absolute; left: 12px; top: 352px; width: 318px; height: 76px; border: 1px solid #DBDBDB; border-radius: 18px;
           font-size: 11.5px; line-height: 1.4; padding: 9px 74px 9px 13px; color: #1f1f1f; }
    .cmp > span { position: absolute; left: 13px; top: 9px; width: 226px; }
    .ph2 { color: #8e8e8e; }
    .cmp u { position: absolute; right: 12px; bottom: 9px; font-size: 11.5px; font-weight: 700; color: #0095F6; text-decoration: none; }
    .hl { border-radius: 4px; padding: 0 2px; margin: 0 -2px; box-decoration-break: clone; -webkit-box-decoration-break: clone; }
    .hd3 { left: 166px; top: 38px; font-size: 16px; font-weight: 500; display: flex; gap: 12px; align-items: center; }
    .b2 { font-size: 11px; font-weight: 700; background: #EFEFEF; border-radius: 8px; padding: 6px 12px; }
    .nm3 { left: 166px; top: 74px; font-size: 12px; font-weight: 700; }
    .bio { left: 160px; top: 92px; font-size: 12px; padding: 3px 6px; border-radius: 5px; }
    .grid { left: 20px; top: 150px; width: 498px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 4px; }
    .grid i { height: 140px; background: #F0EEEE; }
    .cur { position: absolute; left: 300px; top: 300px; }
"""

# camera: the window turns and scales about its centre (400, 270); a point p of it
# lands at O + s*(p - O) + (x, y). Wide puts the window's centre at (540, 760).
OX, OY = 400, 270


def cam(px, py, sc, cx=540, cy=760):
    return {"x": round(cx - OX - sc * (px - OX), 1), "y": round(cy - OY - sc * (py - OY), 1), "scale": sc}


def to(t, c, rx, ry, rz=0, d=1.2, ease="power3.inOut"):
    js(u'  tl.to("#win", {x: %s, y: %s, scale: %s, rotationX: %s, rotationY: %s, rotationZ: %s, duration: %s, ease: "%s"}, %.3f);'
       % (c["x"], c["y"], c["scale"], rx, ry, rz, d, ease, t))


def enter(t, c):
    js(u'  tl.fromTo("#win", {x: %s, y: %s, scale: %s, rotationX: 24, rotationY: -20, rotationZ: 5},'
       u' X({x: %s, y: %s, scale: %s, rotationX: 9, rotationY: -12, rotationZ: 2, duration: 1.3, ease: "power3.out"}), %.3f);'
       % (c["x"], c["y"] + 220, round(c["scale"] * .86, 3), c["x"], c["y"], c["scale"], t))


def typ(sel, t, d, n):
    js(u'  tl.fromTo("%s", {clipPath: "inset(0%% 100%% 0%% 0%%)"}, X({clipPath: "inset(0%% 0%% 0%% 0%%)", duration: %s, ease: "steps(%d)"}), %.3f);' % (sel, d, n, t))


def show(sel, t):
    js(u'  tl.set("%s", {autoAlpha: 1}, %.3f);' % (sel, t))


def hide(sel, t):
    js(u'  tl.set("%s", {autoAlpha: 0}, %.3f);' % (sel, t))


def hl(sel, t):
    js(u'  tl.fromTo("%s", {backgroundColor: "rgba(122,20,36,0)"}, X({backgroundColor: "rgba(122,20,36,.18)", duration: .3}), %.3f);' % (sel, t))


def curto(t, x, y, d=.5):   # cursor, in page coordinates
    js(u'  tl.to("#cur", {left: %d, top: %d, duration: %s, ease: "power2.inOut"}, %.3f);' % (x, y, d, t))


WIDE = cam(400, 270, 1.24)
js(u'  gsap.set("#win", {transformOrigin: "%dpx %dpx"});' % (OX, OY))
js(u'  gsap.set("#win", {x: %s, y: %s, scale: %s});' % (WIDE["x"], WIDE["y"], WIDE["scale"]))

# 4 · FULL A — Claude's own browser: «той же хром» ------------------------------------
a0 = S(u"внутрішньому", 23.03) - 0.15
a1 = S(u"просто", 29.93) - 0.1
enter(a0 + 0.15, WIDE)
to(S(u"браузеру", 24.18) - 0.3, cam(531, 230, 1.75), 6, 8, 1)                 # onto the browser pane
to(S(u"той", 27.56) - 0.5, cam(450, 80, 2.7), 3, -6, 0)                      # tab strip + omnibox
js(u'  tl.fromTo("#omni", {boxShadow: "0 0 0 0 rgba(122,20,36,0)"}, X({boxShadow: "0 0 0 2px rgba(122,20,36,.55)", duration: .3}), %.3f);' % S(u"хром,", 28.12))
to(S(u"звичайний", 28.90) - 0.2, WIDE, 10, 14, -2, 1.1)
js(u'  tl.to("#omni", {boxShadow: "0 0 0 0 rgba(122,20,36,0)", duration: .3}, %.3f);' % (a1 + 0.9))
js(u'  full(%.3f, %.3f);' % (a0, a1))
g.sfx("whoosh-short", a0); g.sfx("whoosh-short", S(u"той", 27.56) - 0.5); g.sfx("click-soft", S(u"хром,", 28.12))
g.sfx("whoosh-short", a1)

# 5 · FULL B — open it, log in, ask, and it walks Direct -----------------------------
b0 = S(u"Відкриваєш", 34.23) - 0.15
b1 = S(u"Але", 44.27) - 0.12
t_vkh, t_akk = S(u"входиш", 35.57), S(u"акаунт", 36.21)
t_pros, t_povid = S(u"просиш", 37.37), S(u"повідомлення.", 38.61)
t_ot = S(u"От і", 39.40)
t_hod, t_shuk, t_pys, t_vidp = S(u"ходити", 41.09), S(u"шукати", 42.23), S(u"писати", 43.11), S(u"відправляти.", 43.69)
enter(b0 + 0.15, WIDE)
to(t_vkh - 0.6, cam(531, 200, 1.6), 5, 7, 1, 1.0)
typ("#url1", t_vkh - 0.5, .45, 13); hide("#url0", t_vkh - 0.5)
hide("#p0", t_vkh); show("#p1", t_vkh); hide("#tabt0", t_vkh); show("#tabt1", t_vkh)
js(u'  tl.to("#login", {scale: .94, duration: .1, yoyo: true, repeat: 1}, %.3f);' % t_akk)
hide("#p1", t_akk + 0.3); show("#p1b", t_akk + 0.3)
to(t_pros - 0.55, cam(131, 470, 2.6), 4, 10, 0, 1.0)                          # the Claude prompt
hide("#ph", t_pros - 0.05); typ("#typ", t_pros - 0.05, 1.0, 18)
js(u'  tl.to("#sendc", {backgroundColor: "#D97757", duration: .15}, %.3f);' % (t_povid - 0.15))
hide("#typ", t_povid + 0.1); show("#ph", t_povid + 0.1); pop_ub = t_povid + 0.1
js(u'  pop("#ubub", %.3f, .45); fadein("#ans", %.3f);' % (pop_ub, pop_ub + 0.6))
to(t_ot - 0.2, WIDE, 9, -12, 2, 1.1)
hide("#p1b", t_hod); show("#p2", t_hod); show("#cur", t_hod)
to(t_hod - 0.45, cam(500, 330, 1.75), 4, 8, 0, 1.0)                           # into Direct
curto(t_hod, 120, 26, .6); hide("#dsr0", t_shuk); typ("#dsr1", t_shuk, .35, 5)
curto(t_shuk + 0.3, 90, 72, .3)
js(u'  tl.to("#r0", {backgroundColor: "#EFEFEF", duration: .15}, %.3f);' % (t_shuk + 0.55))
hide("#c0", t_pys); typ("#c1", t_pys, .55, 12); curto(t_pys - 0.1, 470, 410, .4)
js(u'  tl.to("#snd", {scale: 1.15, duration: .1, yoyo: true, repeat: 1}, %.3f);' % t_vidp)
hide("#c1", t_vidp + 0.12); show("#c0", t_vidp + 0.12); pop_s = t_vidp + 0.12
js(u'  pop("#sent", %.3f, .4);' % pop_s)
js(u'  full(%.3f, %.3f);' % (b0, b1))
g.sfx("whoosh-short", b0); g.sfx("typing", t_vkh - 0.5); g.sfx("click", t_akk)
g.sfx("whoosh-short", t_pros - 0.55); g.sfx("typing", t_pros); g.sfx("click", t_povid - 0.15)
g.sfx("whoosh-short", t_hod - 0.45); g.sfx("click-soft", t_shuk + 0.55); g.sfx("typing", t_pys)
g.sfx("notification", t_vidp); g.sfx("whoosh-short", b1)

# 6 · ABOVE — glass: what Instagram does to a bot ----------------------------------
t_mozh, t_shap, t_tomu = S(u"можуть", 51.04), S(u"по", 51.62), S(u"Тому", 52.23)
F.append(u'''
        <div id="al" class="glass alert hid"><b>Дію заблоковано</b><span>Спробуйте пізніше.</span><em>OK</em></div>''')
js(u'''
  rise("#al", %.3f);
  tl.to("#al", {keyframes: {x: [0, -14, 12, -8, 5, 0]}, duration: .4, ease: "none"}, %.3f);
  sink("#al", %.3f);
''' % (t_mozh - 0.3, t_shap, t_tomu + 0.35))
g.sfx("notification", t_mozh - 0.3); g.sfx("click", t_shap)

# 7 · HALF — rule 1, the pause (Excalidraw scheme) ------------------------------------
k0 = S(u"Перше", 55.40) - 0.15
k1 = E(u"довше.", 67.36) + 0.05
HALF.append((k0, k1))
t_pauza, t_30, t_mizh, t_diy = S(u"пауза,", 56.27), S(u"30-40", 57.46), S(u"між", 58.47), S(u"дією,", 59.90)
t_dov, t_zab, t_obyr = S(u"«довше»", 64.79), S(u"«заблокували", 65.37), S(u"обираємо", 66.94)
js(u'''
  sketch("h1", "skP"); box("h1", 80, 380, 190, 110, {seed: 3, fill: true}); label("h1", 175, 450, "дія", {size: 54});
  draw("h1", %.3f);
  sketch("h2", "skP"); arrow("h2", 285, 420, 435, 420, {seed: 5, bend: -.25}); label("h2", 360, 345, "30-40 с", {size: 44});
  box("h2", 450, 380, 190, 110, {seed: 7, fill: true}); label("h2", 545, 450, "дія", {size: 54});
  draw("h2", %.3f);
  sketch("h3", "skP"); arrow("h3", 655, 420, 805, 420, {seed: 9, bend: -.25}); label("h3", 730, 345, "30-40 с", {size: 44});
  box("h3", 820, 380, 190, 110, {seed: 11, fill: true}); label("h3", 915, 450, "дія", {size: 54});
  draw("h3", %.3f);
  sketch("h4", "skP"); box("h4", 120, 600, 300, 120, {seed: 13, fill: true}); label("h4", 270, 676, "довше", {size: 52});
  draw("h4", %.3f);
  sketch("h5", "skP"); box("h5", 600, 600, 380, 120, {seed: 15}); label("h5", 790, 676, "заблокували", {size: 48});
  draw("h5", %.3f);
  sketch("h6", "skP"); ln("h6", 615, 615, 965, 705, {stroke: "#7A1424", strokeWidth: 7, seed: 17});
  ell("h6", 270, 660, 400, 200, {seed: 19, stroke: "#7A1424", strokeWidth: 6, fill: false});
  draw("h6", %.3f, .5);
  erase("h1", %.3f); erase("h2", %.3f); erase("h3", %.3f); erase("h4", %.3f); erase("h5", %.3f); erase("h6", %.3f);
''' % (t_pauza - 0.2, t_30 - 0.4, t_diy - 0.5, t_dov - 0.1, t_zab - 0.1, t_obyr - 0.1,
       k1 - 0.3, k1 - 0.3, k1 - 0.3, k1 - 0.3, k1 - 0.3, k1 - 0.3))
g.sfx("whoosh-short", k0); g.sfx("click-soft", t_30 - 0.4); g.sfx("click-soft", t_diy - 0.5)
g.sfx("click", t_obyr)

# 8 · FULL C — rule 2, personalisation: name only -> her profile -> the message ------
c0 = k1 + 0.15
c1 = S(u"Тому", 81.10) - 0.15
t_pers, t_imya, t_same = S(u"персоналізація,", 68.68), S(u"ім'я,", 72.15), S(u"саме", 72.75)
t_tut, t_profil, t_podyv = S(u"тут", 74.28), S(u"профіль", 76.50), S(u"чим", 77.73)
t_vpys, t_skr = S(u"і вписати", 78.77), S(u"моїм", 80.31)
# the window as B left it: Direct open, the lead picked, the first message sent
for sel in ("#p0", "#p1", "#p1b", "#url0", "#tabt0", "#cur", "#ans", "#sent"):
    hide(sel, c0 + 0.05)
for sel in ("#p2", "#url1", "#tabt1", "#ubub"):
    show(sel, c0 + 0.05)
js(u'  tl.set("#r0", {backgroundColor: "#EFEFEF"}, %.3f);' % (c0 + 0.05))
enter(c0 + 0.15, WIDE)
hide("#c0", t_pers); typ("#c1", t_pers, .7, 14)
to(S(u"глибша,", 70.10) - 0.3, cam(430, 454, 2.5), 3, -8, 0, 1.1)               # onto the message
hide("#c1", t_imya - 0.1); show("#c2", t_imya - 0.1); hl("#nm", t_imya)
hl("#gen", t_same)
to(t_tut - 0.2, WIDE, 9, 12, -2, 1.1)
hide("#p2", t_profil - 0.1); show("#p3", t_profil - 0.1)
to(t_podyv - 0.55, cam(390, 165, 2.6), 3, 7, 0, 1.0)                           # the bio
hl("#bio", t_podyv)
hide("#p3", t_vpys - 0.05); show("#p2", t_vpys - 0.05); hide("#c2", t_vpys - 0.05); show("#c3", t_vpys - 0.05)
js(u'  tl.set("#pers", {backgroundColor: "rgba(122,20,36,.18)"}, %.3f);' % (t_vpys - 0.05))
to(t_vpys - 0.5, cam(430, 454, 2.5), 3, -8, 0, 0.9)
show("#scr", t_skr - 0.6)
to(t_skr - 0.45, cam(140, 150, 2.3), 4, 10, 0, 0.8)                             # «мій скрипт»
js(u'  tl.fromTo("#scr", {boxShadow: "0 0 0 0 rgba(122,20,36,0)"}, X({boxShadow: "0 0 0 3px rgba(122,20,36,.5)", duration: .3}), %.3f);' % t_skr)
js(u'  full(%.3f, %.3f);' % (c0, c1))
g.sfx("whoosh-short", c0); g.sfx("typing", t_pers); g.sfx("whoosh-short", S(u"глибша,", 70.10) - 0.3)
g.sfx("click-soft", t_imya); g.sfx("click-soft", t_same); g.sfx("whoosh-short", t_podyv - 0.55)
g.sfx("click-soft", t_podyv); g.sfx("whoosh-short", t_vpys - 0.5); g.sfx("click-soft", t_skr)
g.sfx("whoosh-short", c1)

# 9 · CTA — the pill in the subtitle band ---------------------------------------------
t_to = S(u"то", 88.70)
F.append(u'''        <div id="ctp" class="pill hid" style="left:0; right:0; margin:auto; width:max-content; top:1404px;
             font-size:50px; padding:28px 64px">Підпишись</div>''')
js(u'  pop("#ctp", %.3f);' % (t_to - 0.1))
g.sfx("pop", t_to - 0.1)
BLACKOUT.append((t_to - 0.15, DUR))

# ---------------------------------------------------------------- half screen + its matte
for i, (a, b) in enumerate(HALF):
    g.matte("half%d" % (i + 1), round(a - 0.1, 3), round(b - a + 1.2, 3))
    js("  half(%.3f, %.3f);" % (a, b))
    PLACE.append((a + 0.4, b + 0.2, "bottom", 938))


def main():
    chunks = g.chunks(CAPS, place=PLACE)
    doc = g.document(title=u"Reel 58 — автоматизація без бану", plate="assets/base.mp4",
                     behind="\n".join(B), panel="\n".join(P), front="\n".join(F), cover="\n".join(C),
                     js="\n".join(J), chunks=chunks, blackout=BLACKOUT, extra_css=EXTRA)
    g.write(HERE, doc)
    print("index.html  %d caption chunks, %d sfx cues, %d mattes" % (len(chunks), len(g.cues), len(g.mattes)))
    if "-v" in sys.argv:
        print(" ".join(u"%s/%.1f" % (c["w"], c["s"]) for c in CAPS))


main()
