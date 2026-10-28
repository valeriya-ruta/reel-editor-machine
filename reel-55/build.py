# -*- coding: utf-8 -*-
"""Reel 41 — «Plan with me»: how her AI content system actually plans a week.

Variant B, refined glass (STYLE.md §0). Freestyle — no script in RUTA, so the
captions are whisper's timing with its mishearings corrected
(work/r41/captions.py). Cut by me from the «better» of two takes
(work/r41/cutplan.py, 168.3 s): carousels, the repeated «зверху буде екран»,
the early cloud line and two asides came out so it fits one reel (≤ 3 min).

Her brief: candid, *"here's how it actually happens"*, the screen on the top
half and her under it. So the middle of the reel (SPLIT) is her real 36-minute
screen recording, cut into thirteen sped-up clips (work/r41/clips.py) inside
one glass window, zooming onto the moment she names — the skill call, the tool
calls ticking, her typing, «чекай, 11 мало, треба ж 14 нам». She slides down
under it; the captions follow her.

The chain: the week strip (hook) -> Claude and its five jobs on a loop ->
«агент? скіл?» -> +300 and the DMs -> the window (her screen) -> fourteen
reels -> Google Drive -> Claude Code edits -> laptop closed, cloud -> the
evening schedule -> the checklist -> the week strip again, every day done ->
consultation | done-for-you -> «+».

usage: python build.py
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
from kit import Kit  # noqa: E402
from glass import Glass  # noqa: E402

W41 = os.path.join(ROOT, "work", "r55")
DUR = 168.750          # (5063 plate frames - 0.5) / 30
FPS = 30
k = Kit(width=1080, height=1920, fps=FPS, duration=DUR)
g = Glass(["claude", "fathom", "threads", "instagram", "tiktok", "googledrive"])
k.css(g.css())

CAPS = k.load_captions(os.path.join(W41, "captions.json"))


def _n(s):
    return "".join(ch for ch in s.lower() if ch.isalnum())


def _hit(word, near):
    hits = [c for c in CAPS if _n(word) in [_n(x) for x in c["w"].split()] or _n(word) == _n(c["w"])]
    c = min(hits, key=lambda c: abs(c["s"] - near))
    assert abs(c["s"] - near) < 0.8, (word, near, c["s"])
    return c


def S(word, near):
    return _hit(word, near)["s"]


def E(word, near):
    return _hit(word, near)["e"]


# ---------------------------------------------------------------------------
# The screen. Slots on the cut timeline; each clip in work/r41/clips.py is
# encoded to exactly its slot's length.
# Each slot starts on a word; clips.py encodes each clip to its slot's length
# from slots.json, which this file writes.
ANCH = [
    ("c1_skill",    u"Отже,", 40.55),
    ("c2_tools",    u"Він", 43.45),
    ("c3_hypo",     u"І", 53.81),
    ("c3b_leads",   u"які", 62.04),
    ("c4_calls",    u"Другий", 63.98),
    ("c4c_threads", u"А", 72.39),
    ("c5_ideas",    u"І", 76.35),
    ("c6_list",     u"Він", 84.35),
    ("c7_pick",     u"Я", 90.61),
    ("c8_14",       u"14-15,", 92.75),
    ("c9_ruta",     u"після", 93.95),
    ("c10_app",     u"я", 96.51),
    ("c11_done",    u"І", 109.41),
]
_END = S(u"Після", 114.35)
SLOTS = [(n, round(S(w, t) - (0.13 if n == "c8_14" else 0.0) + (0.18 if n == "c9_ruta" else 0.0), 3))
         for n, w, t in ANCH]
SPLIT = (round(SLOTS[0][1] - 0.16, 3), round(_END, 3))
SLOT = {}
for i, (n, t0) in enumerate(SLOTS):
    SLOT[n] = (t0, SLOTS[i + 1][1] if i + 1 < len(SLOTS) else SPLIT[1])
io.open(os.path.join(W41, "slots.json"), "w", encoding="utf-8").write(
    json.dumps({n: round(b - a, 3) for n, (a, b) in SLOT.items()}, indent=1))
_CL = json.load(io.open(os.path.join(W41, "clips.json"), encoding="utf-8"))
for n, (a, b) in SLOT.items():
    if abs(_CL[n][2] - (b - a)) > 0.02:
        print("STALE CLIP %s: %.3f vs slot %.3f — run work/r41/clips.py" % (n, _CL[n][2], b - a))

WIN = (20, 60, 1040, 770)     # the window: x, y, w, h
SHIFT = 330                    # how far she slides down under it
CAP_SHIFT = 110

L = []
J = []
BLACKOUT = []


def bo(a, b):
    BLACKOUT.append((round(a - 0.02, 3), round(b, 3), ""))


def js(s):
    J.append(s)


# ---------------------------------------------------------------------------
CSS = """
.hide { opacity: 0; visibility: hidden; }
.abs { position: absolute; }
.cell { position: absolute; width: 120px; height: 160px; border-radius: 32px; }
.cell .day { position: absolute; left: 0; right: 0; top: 16px; text-align: center; font-size: 26px;
  font-weight: 700; letter-spacing: 0.08em; color: rgba(255,255,255,0.86); }
.cell .stub { position: absolute; left: 28px; top: 58px; width: 64px; height: 84px; border-radius: 16px;
  background: linear-gradient(160deg, #ff8fb2 0%, #ff6e9c 40%, #b4122f 100%);
  box-shadow: inset 0 1.5px 1px rgba(255,255,255,0.7), 0 10px 22px -8px rgba(80,0,20,0.6); }
.cell .stub svg { position: absolute; left: 21px; top: 28px; width: 24px; height: 28px; fill: #fff; }
.cell .ok { position: absolute; left: 34px; top: 66px; width: 52px; height: 52px; border-radius: 26px;
  background: #fff; }
.cell .ok svg { position: absolute; left: 11px; top: 12px; width: 30px; height: 28px; fill: none;
  stroke: #b4122f; stroke-width: 5.5; stroke-linecap: round; stroke-linejoin: round; }
.tw { position: absolute; }
.tw .mk { position: absolute; left: 25%; top: 25%; width: 50%; height: 50%; fill: #fff; }
.tw .pearl .mk { fill: #17141c; }
.pill { position: absolute; height: 76px; line-height: 76px; padding: 0 34px; border-radius: 38px;
  font-size: 32px; font-weight: 700; letter-spacing: 0.04em; white-space: nowrap; }
.pill.light { background: linear-gradient(160deg, #ffffff 0%, #fdf0f4 100%); color: #b4122f;
  box-shadow: inset 0 1.5px 1px #fff, 0 26px 50px -20px rgba(24,4,12,0.55); }
.qm { position: absolute; width: 64px; height: 64px; border-radius: 32px; line-height: 64px;
  text-align: center; font-size: 40px; font-weight: 900; color: #fff;
  background: linear-gradient(150deg, #ff8fb2, #ff6e9c 50%, #d81b4c);
  box-shadow: 0 0 26px rgba(255,110,156,0.8); }
.ntf { position: absolute; left: 110px; width: 860px; height: 128px; border-radius: 40px; }
.ntf .ic { position: absolute; left: 24px; top: 24px; width: 80px; height: 80px; border-radius: 20px;
  background: linear-gradient(140deg, #ffd25e 0%, #ff6e9c 45%, #b4122f 80%); }
.ntf .ic .mk { position: absolute; left: 18px; top: 18px; width: 44px; height: 44px; fill: #fff; }
.ntf .t1 { position: absolute; left: 128px; top: 26px; font-size: 30px; font-weight: 700; }
.ntf .t2 { position: absolute; left: 128px; top: 70px; font-size: 26px; font-weight: 500; opacity: 0.66; }
.ntf .tm { position: absolute; right: 30px; top: 28px; font-size: 24px; font-weight: 500; opacity: 0.5; }

/* the window her screen plays in */
#bgTk { position: absolute; inset: 0; }
#herBox { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: hidden; }
#her2 { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }
#winW { position: absolute; left: %(wx)dpx; top: %(wy)dpx; width: %(ww)dpx; height: %(wh)dpx;
  filter: drop-shadow(0 40px 60px rgba(10,0,4,0.55)) drop-shadow(0 6px 14px rgba(10,0,4,0.25)); }
#win { position: absolute; inset: 0; background: #fafafa; overflow: hidden; }
#win .edge { position: absolute; inset: 0; border-radius: 56px; }
#zm { position: absolute; left: 0; top: 0; width: %(ww)dpx; height: %(wh)dpx; transform-origin: 0 0; }
.sv { position: absolute; left: 0; top: 0; width: %(ww)dpx; height: %(wh)dpx; object-fit: cover; }
#clk { position: absolute; right: 22px; top: 20px; height: 70px; padding: 0 26px 0 70px; border-radius: 35px;
  line-height: 70px; font-size: 34px; font-weight: 700; color: #fff; letter-spacing: 0.02em;
  font-variant-numeric: tabular-nums; }
#clk svg { position: absolute; left: 22px; top: 18px; width: 34px; height: 34px; fill: none;
  stroke: #fff; stroke-width: 3.4; stroke-linecap: round; }
.hl { position: absolute; border-radius: 18px; border: 6px solid #ff6e9c;
  box-shadow: 0 0 22px rgba(255,110,156,0.75), inset 0 0 18px rgba(255,110,156,0.25); }
.badge { position: absolute; width: 140px; height: 140px; }

/* full-frame beats */
.reelT { position: absolute; width: 92px; height: 150px; border-radius: 22px;
  background: linear-gradient(160deg, #ff9bbb 0%, #ff6e9c 38%, #b4122f 100%);
  box-shadow: inset 0 1.5px 1px rgba(255,255,255,0.7), 0 18px 34px -12px rgba(60,0,16,0.6); }
.reelT svg { position: absolute; left: 32px; top: 58px; width: 28px; height: 34px; fill: #fff; }
.link { position: absolute; height: 78px; line-height: 78px; padding: 0 30px 0 80px; border-radius: 39px;
  font-size: 30px; font-weight: 500; color: #17141c; white-space: nowrap;
  background: linear-gradient(160deg, #fff 0%, #fdf0f4 100%);
  box-shadow: inset 0 1.5px 1px #fff, 0 26px 50px -20px rgba(24,4,12,0.55); }
.link svg { position: absolute; left: 26px; top: 21px; width: 36px; height: 36px; fill: none;
  stroke: #b4122f; stroke-width: 3.6; stroke-linecap: round; }
.prog { position: absolute; height: 22px; border-radius: 11px; background: rgba(255,255,255,0.22); overflow: hidden; }
.prog i { position: absolute; left: 0; top: 0; bottom: 0; width: 100%%; border-radius: 11px;
  background: linear-gradient(90deg, #ffd6e3, #ff6e9c); transform-origin: 0 50%%; }
.lap { position: absolute; }
.lap svg { width: 100%%; height: 100%%; }
.xx { position: absolute; width: 150px; height: 150px; border-radius: 75px;
  background: linear-gradient(150deg, #ff8fb2, #ff6e9c 50%, #d81b4c); box-shadow: 0 0 40px rgba(255,110,156,0.8); }
.xx svg { position: absolute; left: 40px; top: 40px; width: 70px; height: 70px; fill: none;
  stroke: #fff; stroke-width: 12; stroke-linecap: round; }
.row { position: absolute; left: 60px; right: 60px; height: 96px; }
.row .d { position: absolute; left: 0; top: 0; line-height: 96px; font-size: 30px; font-weight: 700; color: rgba(23,20,28,0.42);
  letter-spacing: 0.14em; }
.row .s { position: absolute; top: 14px; width: 250px; height: 68px; border-radius: 22px; background: #fbe3ea;
  color: #b4122f; font-size: 28px; font-weight: 700; line-height: 68px; padding-left: 66px; }
.row .s svg { position: absolute; left: 22px; top: 18px; width: 30px; height: 32px; fill: #b4122f; }
.row .gap { position: absolute; top: 30px; height: 36px; line-height: 36px; font-size: 24px; font-weight: 700;
  color: rgba(23,20,28,0.5); text-align: center; }
.chk { position: absolute; left: 70px; right: 70px; height: 104px; }
.chk .bx { position: absolute; left: 0; top: 22px; width: 60px; height: 60px; border-radius: 16px;
  border: 5px solid rgba(23,20,28,0.18); }
.chk .bx svg { position: absolute; left: 4px; top: 6px; width: 42px; height: 38px; fill: none; stroke: #fff;
  stroke-width: 7; stroke-linecap: round; stroke-linejoin: round; }
.chk .fill { position: absolute; left: -5px; top: -5px; width: 60px; height: 60px; border-radius: 16px; background: #b4122f; }
.chk .tx { position: absolute; left: 92px; top: 0; line-height: 104px; font-size: 40px; font-weight: 700; color: #17141c; }
.chk .ln { position: absolute; left: 92px; right: 0; top: 52px; height: 6px; border-radius: 3px; background: #b4122f;
  transform-origin: 0 50%%; }
.opt { position: absolute; top: 150px; width: 450px; height: 330px; border-radius: 56px; }
.opt .t-micro { position: absolute; left: 44px; top: 44px; }
.opt .nm { position: absolute; left: 44px; top: 96px; font-size: 52px; font-weight: 900; letter-spacing: -0.02em;
  color: #17141c; line-height: 1.05; }
.opt .ic { position: absolute; left: 44px; bottom: 40px; width: 92px; height: 92px; border-radius: 28px;
  background: #fbe3ea; }
.opt .ic svg { position: absolute; left: 22px; top: 22px; width: 48px; height: 48px; fill: none; stroke: #b4122f;
  stroke-width: 4.5; stroke-linecap: round; stroke-linejoin: round; }
.vs { position: absolute; left: 500px; top: 270px; width: 80px; height: 80px; border-radius: 40px; line-height: 80px;
  text-align: center; font-size: 30px; font-weight: 900; color: #fff;
  background: linear-gradient(150deg, #ff8fb2, #ff6e9c 50%, #d81b4c); }
.cmt { position: absolute; left: 90px; top: 300px; width: 900px; height: 130px; border-radius: 65px; color: #17141c;
  background: linear-gradient(160deg, #ffffff 0%, #fdf0f4 100%);
  box-shadow: inset 0 1.5px 1px #fff, 0 40px 80px -30px rgba(24,4,12,0.6); }
.cmt .av { position: absolute; left: 22px; top: 22px; width: 86px; height: 86px; border-radius: 43px;
  background: linear-gradient(140deg, #ffd25e 0%, #ff6e9c 45%, #b4122f 80%); }
.cmt .cph { position: absolute; left: 136px; top: 0; line-height: 130px; font-size: 36px; font-weight: 500;
  color: rgba(23,20,28,0.45); }
.cmt .pl { position: absolute; left: 136px; top: 0; line-height: 126px; font-size: 80px; font-weight: 900; color: #b4122f; }
.cmt .snd { position: absolute; right: 22px; top: 22px; width: 86px; height: 86px; border-radius: 43px; background: #b4122f; }
.cmt .snd svg { position: absolute; left: 24px; top: 23px; width: 40px; height: 40px; fill: #fff; }
.wm { font-weight: 900; color: #17141c; letter-spacing: -0.02em; position: absolute; left: 0; right: 0;
  text-align: center; }
"""
for _k, _v in (("wx", WIN[0]), ("wy", WIN[1]), ("ww", WIN[2]), ("wh", WIN[3])):
    CSS = CSS.replace("%%(%s)d" % _k, str(_v))
CSS = CSS.replace("%%", "%")
k.css(CSS)
k.squircle("#win", WIN[2], WIN[3], 56)
k.squircle(".opt", 450, 330, 56)

PLAY = '<svg viewBox="0 0 24 28"><path d="M3 2.5v23l19-11.5z"/></svg>'
TICK = '<svg viewBox="0 0 30 28"><path d="M4 15l7 7L26 6"/></svg>'
TICK2 = '<svg viewBox="0 0 42 38"><path d="M6 20l10 10L36 8"/></svg>'
CLOCK = '<svg viewBox="0 0 34 34"><circle cx="17" cy="17" r="14"/><path d="M17 9v8l6 4"/></svg>'
LINK = ('<svg viewBox="0 0 36 36"><path d="M15 21l6-6"/><path d="M13 16l-4 4a5 5 0 0 0 7 7l4-4"/>'
        '<path d="M23 20l4-4a5 5 0 0 0-7-7l-4 4"/></svg>')
SEND = '<svg viewBox="0 0 40 40"><path d="M4 20 36 5 27 35l-7-11z"/></svg>'
XMARK = '<svg viewBox="0 0 70 70"><path d="M12 12l46 46M58 12 12 58"/></svg>'


def tile(tid, size, x, y, material, inner, cls="hide"):
    return ('<div class="tw %s" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
            '<div class="%s">%s</div></div>' % (cls, tid, x, y, size, size, material, inner))


def wm(text, size):
    return '<span class="wm" style="top:%dpx;font-size:%dpx">%s</span>' % (int(size * 0.98), size, text)


# ---------------------------------------------------------------------------
# A · 0.0–4.6  «сплануємо контент на тиждень завдяки моєму AI-продюсеру»
DAYS = [u"ПН", u"ВТ", u"СР", u"ЧТ", u"ПТ", u"СБ", u"НД"]


def week(gid, x0, y0, done=False):
    h = []
    for i, d in enumerate(DAYS):
        x = x0 + i * 134
        inner = ('<div class="ok hide" id="%s_k%d">%s</div>' % (gid, i, TICK)) if done else \
                ('<div class="stub hide" id="%s_s%d">%s</div>' % (gid, i, PLAY))
        h.append('<div class="cell shelf edge hide" id="%s_c%d" style="left:%dpx;top:%dpx">'
                 '<div class="day">%s</div>%s</div>' % (gid, i, x, y0, d, inner))
    return "".join(h)


def beat_a():
    t_on, t_cont, t_ai, t_out = 0.25, S(u"контент", 1.98), S(u"AI-продюсеру.", 3.66), E(u"AI-продюсеру.", 3.66)
    L.append('<div class="g full" id="gA">' + week("wA", 75, 330) +
             tile("tA", 170, 455, 110, "jelly", g.mark("claude")) + '</div>')
    js('tl.set("#gA", {autoAlpha: 1}, %.3f);' % t_on)
    for i in range(7):
        js('G.arrive("#wA_c%d", %.3f, {s: 0.6, y: 40});' % (i, t_on + 0.06 * i))
        js('G.arrive("#wA_s%d", %.3f, {s: 0.3, y: 10});' % (i, t_cont + 0.07 * i))
    js('G.arrive("#tA", %.3f, {s: 0.4});' % (t_ai - 0.05))
    js('G.bump("#tA", %.3f);' % (t_ai + 0.3))
    js('G.blurOut("#gA", %.3f);' % (t_out + 0.35))


# C · «AI-систему … аналізує, придумує ідеї, монтує, дизайнить, постить і так по колу»
JOBS = [(u"АНАЛІЗ", u"аналізує", 16.40, 120, 330), (u"ІДЕЇ", u"ідеї,", 17.78, 330, 150),
        (u"МОНТАЖ", u"монтує", 18.30, 650, 150), (u"ДИЗАЙН", u"дизайнить,", 19.64, 820, 330),
        (u"ПОСТИНГ", u"постить", 20.40, 420, 520)]


def beat_c():
    t_sys = S(u"AI-систему,", 11.18)
    t_kolo = S(u"колу", 21.34)
    t_out = E(u"тижня.", 22.10) + 0.2
    h = ['<div class="g full" id="gC">',
         '<svg class="abs" style="left:0;top:0" width="1080" height="700">'
         '<ellipse id="orb" cx="540" cy="365" rx="330" ry="190" fill="none" stroke="rgba(255,255,255,0.55)"'
         ' stroke-width="6" stroke-linecap="round"/>'
         '<path id="orbA" d="M 855 300 l 18 34 l -38 -2" fill="none" stroke="#fff" stroke-width="7"'
         ' stroke-linecap="round" stroke-linejoin="round" opacity="0"/></svg>',
         tile("tC", 190, 445, 270, "jelly", g.mark("claude"))]
    for i, (lab, w, near, x, y) in enumerate(JOBS):
        h.append('<div class="pill dglass edge hide" id="jC%d" style="left:%dpx;top:%dpx">%s</div>' % (i, x, y, lab))
    h.append('</div>')
    L.append("".join(h))
    js('tl.set("#gC", {autoAlpha: 1}, %.3f);' % (t_sys - 0.1))
    js('G.arrive("#tC", %.3f, {s: 0.4});' % (t_sys - 0.05))
    js('G.drawPrep("orb");')
    js('G.draw("orb", %.3f, 0.9);' % (S(u"працює", 14.66)))
    for i, (lab, w, near, x, y) in enumerate(JOBS):
        t = S(w, near)
        js('G.arrive("#jC%d", %.3f, {s: 0.5, y: 20});' % (i, t - 0.06))
    bo(S(u"аналізує", 16.40), E(u"постить", 20.40))
    # «по колу»: the loop spins once — the chips ride it
    js('tl.to("#orbA", {opacity: 1, duration: 0.2}, %.3f);' % t_kolo)
    js('tl.to("#gC .pill", {keyframes: {y: [0, -14, 0]}, duration: 0.5, stagger: 0.08, ease: "sine.inOut"}, %.3f);' % t_kolo)
    js('G.bump("#tC", %.3f);' % (t_kolo + 0.3))
    js('G.blurOut("#gC", %.3f);' % t_out)


# D · «нам кажуть, там працює агент, там працює скил»
def beat_d():
    ta, ts = S(u"агент,", 27.69), S(u"скил,", 28.53)
    out = S(u"факту", 29.01) + 0.1
    L.append('<div class="g full" id="gD">'
             '<div class="pill dglass edge hide" id="dA" style="left:150px;top:260px">%s</div>'
             '<div class="qm hide" id="dAq" style="left:368px;top:212px">?</div>'
             '<div class="pill dglass edge hide" id="dS" style="left:610px;top:340px">%s</div>'
             '<div class="qm hide" id="dSq" style="left:790px;top:292px">?</div></div>' % (u"АГЕНТ", u"СКІЛ"))
    js('tl.set("#gD", {autoAlpha: 1}, %.3f);' % (ta - 0.1))
    js('G.arrive("#dA", %.3f, {s: 0.5});' % (ta - 0.05))
    js('G.arrive("#dAq", %.3f, {s: 0.2, ease: POP});' % (ta + 0.2))
    js('G.arrive("#dS", %.3f, {s: 0.5});' % (ts - 0.05))
    js('G.arrive("#dSq", %.3f, {s: 0.2, ease: POP});' % (ts + 0.2))
    js('tl.to("#gD .qm", {rotation: 14, duration: 0.12, yoyo: true, repeat: 3, ease: "sine.inOut"}, %.3f);' % (ts + 0.45))
    js('G.blurOut("#gD", %.3f);' % out)
    bo(ta - 0.25, E(u"скил,", 28.53))


# E · «третій тиждень підряд … +300 підписників. Мені прийшла купа запитів в директ»
def beat_e():
    t0 = S(u"Уже", 33.50)
    t300 = S("300", 35.82)
    t_kupa = S(u"купа", 37.62)
    out = E(u"обробити.", 39.54) + 0.05
    L.append('<div class="g full" id="gE">'
             '<div class="sheet hide" id="eS" style="left:200px;top:140px;width:680px;height:330px">'
             '<div class="sheen"></div>'
             '<div class="t-micro abs" style="left:52px;top:48px">%s</div>'
             '<div class="t-big abs" id="eN" style="left:44px;top:104px">+0</div>'
             '<div class="abs" style="left:530px;top:130px;width:110px;height:110px">'
             '<svg viewBox="0 0 24 24" width="110" height="110" style="fill:#b4122f"><use href="#i-instagram"/></svg></div>'
             '</div></div>' % u"ЩОТИЖНЯ · 3 ТИЖНІ ПІДРЯД")
    js('tl.set("#gE", {autoAlpha: 1}, %.3f);' % (t0 - 0.1))
    js('G.arrive("#eS", %.3f, {s: 0.6});' % t0)
    js('G.sheen("#eS .sheen", %.3f);' % (t300 + 0.1))
    js('(function(){var o={v:0},el=document.getElementById("eN");'
       'tl.fromTo(o,{v:0},{v:300,duration:%.3f,ease:"power2.out",immediateRender:false,onUpdate:function(){el.textContent="+"+Math.round(o.v);}},%.3f);})();'
       % (t300 + 0.25 - (t0 + 0.5), t0 + 0.5))
    js('G.blurOut("#eS", %.3f, 10, 0.28);' % (t_kupa - 0.35))
    bo(t0 - 0.05, E(u"підписників.", 36.08))
    # the DMs stack up, one haptic each
    for i in range(3):
        y = 120 + i * 112
        L.append('<div class="g full" id="gE%d"><div class="ntf dglass edge hide" id="eD%d" style="top:%dpx">'
                 '<div class="ic"><svg class="mk"><use href="#i-instagram" width="100%%" height="100%%"/></svg></div>'
                 '<div class="t1">%s</div><div class="t2">%s</div><div class="tm">%s</div></div></div>'
                 % (i, i, y, u"Нове повідомлення", [u"Привіт! Хочу таку систему", u"Скільки коштує налаштування?",
                                                   u"А можна консультацію?"][i], u"зараз"))
        t = t_kupa - 0.1 + i * 0.42
        js('tl.set("#gE%d", {autoAlpha: 1}, %.3f);' % (i, t))
        js('G.arrive("#eD%d", %.3f, {s: 0.8, y: -60, d: 0.6});' % (i, t))
        js('G.haptic("#eD%d", %.3f);' % (i, t + 0.3))
        js('G.blurOut("#gE%d", %.3f, 10, 0.28);' % (i, out))


# ---------------------------------------------------------------------------
# SPLIT · her real screen
def _xy(px, py, s, left):
    w, h = WIN[2], WIN[3]
    x = min(0.0, max(w - w * s, w / 2.0 - px * s))
    if left is not None:            # the chat is left-aligned: never cut its first letters
        x = min(0.0, max(x, 16 - left * s))
    y = min(0.0, max(h - h * s, h / 2.0 - py * s))
    return x, y


def zoom(t, px, py, s, d=0.75, ease="power3.inOut", left=30):
    """bring window point (px, py) to the window centre at scale s, clamped so
    the recording always fills the window."""
    x, y = _xy(px, py, s, left)
    js('tl.to("#zm", {x: %.1f, y: %.1f, scale: %.4f, duration: %.2f, ease: "%s"}, %.3f);' % (x, y, s, d, ease, t))


def zset(t, px, py, s, left=30):
    x, y = _xy(px, py, s, left)
    js('tl.set("#zm", {x: %.1f, y: %.1f, scale: %.4f}, %.3f);' % (x, y, s, t))


INPUT = (520, 670)            # the reply box, window coords (CHAT crop × 0.7123)
HOME = (520, 430)             # the centred box on the empty «Afternoon, Ruta» screen
TOOLS = (360, 200)            # the tool-call lines under her message


def split():
    a, b = SPLIT
    vids = []
    for n, (t0, t1) in SLOT.items():
        vids.append('<video id="v_%s" class="sv" src="assets/scr/%s.mp4" data-start="%.3f" data-duration="%.3f" '
                    'data-media-start="0" muted playsinline></video>' % (n, n, t0, t1 - t0))
    L.append('<div class="g full" id="gS">'
             '<div id="bgTk" class="tkg"><div class="aur a1"></div><div class="aur a2"></div>'
             '<div class="aur a3"></div><div class="grain"></div></div>'
             '<div id="herBox"><video id="her2" src="assets/base.mp4" data-start="%.3f" data-duration="%.3f" '
             'data-media-start="%.3f" muted playsinline></video></div>'
             '<div id="winW"><div id="win"><div id="zm">%s'
             '<div class="hl hide" id="hl1"></div><div class="hl hide" id="hl2"></div>'
             '<div class="hl hide" id="hl3"></div></div>'
             '<div id="clk" class="dglass hide">%s<span id="clkT">0:00</span></div>'
             '<div class="edge"></div></div></div>'
             '<div class="badge hide" id="bF">%s</div>'
             '<div class="badge hide" id="bT">%s</div>'
             '<div class="badge hide" id="bR">%s</div>'
             '<div class="badge hide" id="bOk">%s</div>'
             '</div>' % (a, b - a, a, "".join(vids), CLOCK,
                         tile("bF_t", 140, 0, 0, "pearl", g.mark("fathom"), cls=""),
                         tile("bT_t", 140, 0, 0, "pearl", g.mark("threads"), cls=""),
                         tile("bR_t", 140, 0, 0, "jelly", wm("RUTA", 34), cls=""),
                         '<div class="xx" style="left:-5px;top:-5px">'
                         '<svg viewBox="0 0 70 70" style="stroke-width:11"><path d="M14 37l13 13 29-30"/></svg></div>'))
    # in: she is the plate for the first frame, then slides down as the window lands
    js('tl.set("#gS", {autoAlpha: 1}, %.3f);' % a)
    js('tl.set("#winW", {autoAlpha: 0}, 0);')
    js('tl.fromTo("#her2", {y: 0}, {y: %d, duration: 0.75, ease: SOFT, immediateRender: false}, %.3f);' % (SHIFT, a))
    js('G.arrive("#winW", %.3f, {s: 0.55, y: 120, d: 0.9});' % (a + 0.08))
    js('G.drift("#bgTk", %.3f, %.3f);' % (a, b - a))
    js('tl.to(".cap, #scrim", {y: %d, duration: 0.6, ease: SOFT}, %.3f);' % (CAP_SHIFT, a))
    # out: the window falls back into depth, she rises into the frame again
    js('tl.to("#winW", {scale: 0.6, y: -80, autoAlpha: 0, filter: "blur(10px)", duration: 0.45, ease: "power2.in"}, %.3f);' % (b - 0.25))
    js('tl.to("#her2", {y: 0, duration: 0.7, ease: SOFT}, %.3f);' % (b - 0.1))
    js('tl.to(".cap, #scrim", {y: 0, duration: 0.6, ease: SOFT}, %.3f);' % (b - 0.1))
    js('tl.set("#gS", {autoAlpha: 0}, %.3f);' % (b + 0.7))
    for n, (t0, t1) in SLOT.items():
        js('tl.set("#v_%s", {autoAlpha: 1}, %.3f); tl.set("#v_%s", {autoAlpha: 0}, %.3f);' % (n, t0, n, t1 + 0.04))
        if n != SLOTS[0][0]:
            js('tl.set("#v_%s", {autoAlpha: 0}, 0);' % n)

    s = SLOT
    # c1 · «перший крок»: the empty chat, /content-plan typed, sent
    zset(s["c1_skill"][0], HOME[0], HOME[1], 1.6, left=None)
    zoom(s["c1_skill"][0] + 1.55, 520, 385, 1.0, 0.7)
    # c2 · tool calls ticking; the clock runs on her recording's own time
    zoom(s["c2_tools"][0], TOOLS[0], TOOLS[1], 1.6)
    clock(s["c2_tools"][0], s["c2_tools"][1], 11 - 6, 55 - 6)
    zoom(S(u"останній", 48.78) - 0.2, 360, 186, 1.85, 0.6)          # «минулий тиждень (19–25 жовтня)»
    zoom(S(u"тестувати", 50.04), TOOLS[0], TOOLS[1] + 30, 1.6, 0.7)
    # c3 · the hypotheses: which hooks, topics, formats worked
    zset(s["c3_hypo"][0], 520, 385, 1.0)
    clock(s["c3_hypo"][0], s["c3_hypo"][1], 128 - 6, 178 - 6)
    zoom(S(u"гачки", 60.08) - 0.15, 470, 330, 1.3, 0.7)
    # c3b · her, candid: «так але + це мій основний дохід, мені треба ліди»
    zset(s["c3b_leads"][0], 520, 170, 1.15)
    # c4 · ideas from her calls: Fathom in the tool calls
    zset(s["c4_calls"][0], TOOLS[0], TOOLS[1] + 30, 1.6)
    badge("bF", S(u"дзвінків,", 69.63) - 0.1, 880, 750, s["c4_calls"][1] - 0.2)
    # c4c · and Threads: the idea list carries its source
    zset(s["c4c_threads"][0], 520, 385, 1.3)
    badge("bT", S(u"Threads,", 72.47) - 0.05, 880, 750, s["c4c_threads"][1] - 0.2)
    # c5 · meanwhile she types her own ideas
    zset(s["c5_ideas"][0], INPUT[0], INPUT[1], 1.7)
    zoom(s["c5_ideas"][0] + 3.6, INPUT[0] + 400, INPUT[1], 1.7, 2.0, "sine.inOut", left=None)
    # c6 · the big numbered list
    zset(s["c6_list"][0], 520, 385, 1.0)
    zoom(s["c6_list"][0] + 0.2, 470, 400, 1.22, 1.2, "power2.out")
    # c7 · she picks numbers; c8 · «чекай, 11 мало, треба ж 14 нам»
    zset(s["c7_pick"][0], 520, 630, 1.3)
    zset(s["c8_14"][0], 837, 548, 1.0, left=None)
    zoom(s["c8_14"][0] + 0.05, 837, 548, 2.0, 0.45, "power3.out", left=None)
    # c9 · into RUTA
    zset(s["c9_ruta"][0], 360, 330, 1.5)
    badge("bR", S(u"Рута,", 95.46) - 0.1, 880, 750, s["c9_ruta"][1] - 0.15)
    # c10 · the RUTA app: a voice note per idea, then «Зробити рілс»
    zset(s["c10_app"][0], 520, 380, 1.3, left=None)
    zoom(S(u"записую", 101.35) - 0.15, 878, 738, 1.9, 0.7, left=None)
    zoom(S(u"що", 102.63) + 0.6, 520, 380, 1.3, 0.8, left=None)
    # c11 · «вуаля»: the script is there
    zset(s["c11_done"][0], 520, 360, 1.3, left=None)
    badge("bOk", S(u"вуаля,", 111.13) - 0.05, 880, 750, b - 0.35)


def clock(t0, t1, s0, s1):
    """her recording's elapsed time, mm:ss, counting through the slot"""
    js('tl.set("#clk", {autoAlpha: 1}, %.3f); tl.set("#clk", {autoAlpha: 0}, %.3f);' % (t0, t1))
    js('(function(){var o={v:%d},el=document.getElementById("clkT");'
       'tl.fromTo(o,{v:%d},{v:%d,duration:%.3f,ease:"none",immediateRender:false,onUpdate:function(){'
       'var v=Math.round(o.v);el.textContent=Math.floor(v/60)+":"+("0"+v%%60).slice(-2);}},%.3f);})();'
       % (s0, s0, s1, t1 - t0, t0))


def badge(bid, t, x, y, t_out):
    """a mark tile that lands on the window's lower edge"""
    js('gsap.set("#%s", {left: %d, top: %d});' % (bid, x, y))
    js('G.arrive("#%s", %.3f, {s: 0.3, y: 30});' % (bid, t))
    js('G.bump("#%s", %.3f);' % (bid, t + 0.35))
    js('G.blurOut("#%s", %.3f, 10, 0.25);' % (bid, t_out))


# ---------------------------------------------------------------------------
# F · «знімаю всі ці 14 рілсів одразу» → G · Google Диск → посилання → Claude Code
def beat_fg():
    t14 = S("14", 118.24)
    t_drive = S(u"Google", 122.50)
    t_link = S(u"посилання", 123.58)
    t_cc = S(u"Claude", 125.62)
    h = ['<div class="g full" id="gF">']
    for i in range(14):
        r, c = divmod(i, 7)
        h.append('<div class="reelT hide" id="fR%d" style="left:%dpx;top:%dpx">%s</div>' % (i, 78 + c * 134, 150 + r * 186, PLAY))
    h.append(tile("fD", 190, 445, 230, "pearl", g.mark("googledrive")))
    h.append('<div class="link hide" id="fL" style="left:250px;top:470px">%s%s</div>' % (LINK, u"drive.google.com/…"))
    h.append(tile("fC", 190, 445, 230, "jelly", g.mark("claude")))
    h.append('</div>')
    L.append("".join(h))
    js('tl.set("#gF", {autoAlpha: 1}, %.3f);' % (t14 - 0.3))
    for i in range(14):
        js('G.arrive("#fR%d", %.3f, {s: 0.4, y: 30, d: 0.6});' % (i, t14 - 0.2 + 0.045 * i))
    # the fourteen fly into Drive
    for i in range(14):
        r, c = divmod(i, 7)
        dx, dy = 540 - (78 + c * 134 + 46), 325 - (150 + r * 186 + 75)
        js('tl.to("#fR%d", {x: %d, y: %d, scale: 0.2, autoAlpha: 0, duration: 0.5, ease: "power3.in"}, %.3f);'
           % (i, dx, dy, t_drive - 0.45 + 0.02 * i))
    js('G.arrive("#fD", %.3f, {s: 0.4});' % (t_drive - 0.05))
    js('G.bump("#fD", %.3f);' % (t_drive + 0.3))
    js('G.arrive("#fL", %.3f, {s: 0.5, y: -60});' % (t_link - 0.05))
    # the link goes into Claude Code
    js('G.blurOut("#fD", %.3f, 10, 0.3);' % (t_cc - 0.3))
    js('G.arrive("#fC", %.3f, {s: 0.4});' % (t_cc - 0.15))
    js('tl.to("#fL", {x: 40, y: -230, scale: 0.3, autoAlpha: 0, duration: 0.45, ease: "power3.in"}, %.3f);' % (t_cc - 0.2))
    js('G.bump("#fC", %.3f);' % (t_cc + 0.3))


# H · «мій Клод одразу починає їх монтувати в моєму стилі»
def beat_h():
    t0 = S(u"монтувати", 128.16)
    t_st = S(u"стилі.", 129.64)
    out = E(u"стилі.", 129.64) + 0.2
    L.append('<div class="g full" id="gH">'
             '<div class="prog hide" id="hP" style="left:250px;top:470px;width:580px"><i id="hPi"></i></div>'
             '</div>')
    js('tl.set("#gH", {autoAlpha: 1}, %.3f);' % (t0 - 0.2))
    js('G.blurIn("#hP", %.3f);' % (t0 - 0.2))
    js('tl.fromTo("#hPi", {scaleX: 0}, {scaleX: 1, duration: %.3f, ease: "power1.inOut", immediateRender: false}, %.3f);'
       % (t_st - t0 + 0.3, t0 - 0.1))
    js('gsap.set("#hPi", {scaleX: 0});')
    js('G.bump("#fC", %.3f);' % (t_st + 0.15))
    js('G.blurOut("#gH", %.3f, 10, 0.3);' % out)
    js('G.blurOut("#gF", %.3f, 10, 0.3);' % out)


# I · «треба, щоб комп'ютер був відкритий. Не треба … на хмарі. А я знаю.»
LAPTOP = ('<svg viewBox="0 0 300 200"><rect x="40" y="12" width="220" height="148" rx="18" fill="rgba(255,255,255,0.16)" '
          'stroke="#fff" stroke-width="12"/><path d="M8 178h284" stroke="#fff" stroke-width="16" stroke-linecap="round"/>'
          '<rect id="iScr" x="58" y="30" width="184" height="112" rx="8" fill="#ffd6e3"/></svg>')
CLOUD = ('<svg viewBox="0 0 300 200"><path d="M80 170h150a52 52 0 0 0 4-104 72 72 0 0 0-138-12A58 58 0 0 0 80 170z" '
         'fill="rgba(255,255,255,0.92)" stroke="#fff" stroke-width="6"/>'
         '<path d="M118 120l26 26 46-52" fill="none" stroke="#b4122f" stroke-width="16" stroke-linecap="round" '
         'stroke-linejoin="round"/></svg>')


def beat_i():
    t_komp = S(u"комп'ютер", 132.94)
    t_ne = S(u"Не", 134.06)
    t_hm = S(u"хмарі.", 136.46)
    t_zn = S(u"знаю.", 137.54)
    out = E(u"знаю.", 137.54) + 0.15
    L.append('<div class="g full" id="gI">'
             '<div class="lap hide" id="iL" style="left:240px;top:170px;width:330px;height:220px">%s</div>'
             '<div class="xx hide" id="iX" style="left:330px;top:205px">%s</div>'
             '<div class="lap hide" id="iC" style="left:560px;top:150px;width:330px;height:220px">%s</div>'
             '</div>' % (LAPTOP, XMARK, CLOUD))
    js('tl.set("#gI", {autoAlpha: 1}, %.3f);' % (t_komp - 0.2))
    js('G.arrive("#iL", %.3f, {s: 0.5});' % (t_komp - 0.1))
    js('G.arrive("#iX", %.3f, {s: 2.0, ease: POP, d: 0.5});' % (t_ne - 0.05))
    js('G.haptic("#iL", %.3f);' % (t_ne + 0.15))
    js('tl.to("#iL, #iX", {opacity: 0.35, scale: 0.86, duration: 0.4, ease: "power2.out"}, %.3f);' % (t_hm - 0.3))
    js('G.arrive("#iC", %.3f, {s: 0.4, y: -40});' % (t_hm - 0.15))
    js('G.bump("#iC", %.3f);' % (t_zn - 0.05))
    js('G.blurOut("#gI", %.3f, 10, 0.3);' % out)


# J · «планує по два на день, на вечір, з годиною між кожним, в мій Instagram і TikTok»
def beat_j():
    t0 = S(u"планує", 140.98)
    t_dva = S(u"два", 141.60)
    t_hod = S(u"годиною", 143.06)
    t_ig, t_tt = S(u"Instagram", 144.70), S(u"TikTok.", 145.46)
    out = E(u"TikTok.", 145.46) + 0.25
    rows = []
    for i, d in enumerate([u"ПН", u"ВТ", u"СР"]):
        y = 112 + i * 108
        rows.append('<div class="row" style="top:%dpx"><div class="d">%s</div>'
                    '<div class="s hide" id="jA%d" style="left:120px">%s%s</div>'
                    '<div class="gap hide" id="jG%d" style="left:380px;width:150px">%s</div>'
                    '<div class="s hide" id="jB%d" style="left:540px">%s%s</div></div>'
                    % (y, d, i, PLAY, u"рілс", i, u"+1 год", i, PLAY, u"рілс"))
    L.append('<div class="g full" id="gJ"><div class="sheet hide" id="jS" style="left:90px;top:100px;width:900px;height:460px">'
             '<div class="sheen"></div><div class="t-micro abs" style="left:60px;top:42px">%s</div>%s'
             '</div>%s%s</div>' % (u"ВЕЧІР", "".join(rows),
                                   tile("jI", 120, 830, 60, "jelly", g.mark("instagram")),
                                   tile("jT", 120, 830, 470, "jelly", g.mark("tiktok"))))
    js('tl.set("#gJ", {autoAlpha: 1}, %.3f);' % (t0 - 0.2))
    js('G.arrive("#jS", %.3f, {s: 0.6});' % (t0 - 0.15))
    for i in range(3):
        js('G.arrive("#jA%d", %.3f, {s: 0.5, y: 10, d: 0.6});' % (i, t_dva - 0.1 + 0.08 * i))
        js('G.arrive("#jB%d", %.3f, {s: 0.5, y: 10, d: 0.6});' % (i, t_dva + 0.15 + 0.08 * i))
        js('G.blurIn("#jG%d", %.3f);' % (i, t_hod - 0.05 + 0.07 * i))
    js('G.arrive("#jI", %.3f, {s: 0.4});' % (t_ig - 0.05))
    js('G.arrive("#jT", %.3f, {s: 0.4});' % (t_tt - 0.05))
    js('G.blurOut("#gJ", %.3f, 10, 0.3);' % out)
    bo(t_hod - 0.3, E(u"кожним,", 143.78))


# K · «там будуть субтитри, анімації, все як треба»
def beat_k():
    t0 = S(u"Тобто", 145.92)
    items = [(u"СУБТИТРИ", S(u"субтитри,", 149.46)), (u"АНІМАЦІЇ", S(u"анімації,", 149.94)),
             (u"ВСЕ ЯК ТРЕБА", S(u"все", 150.44))]
    out = E(u"треба.", 150.80) + 0.2
    rows = []
    for i, (lab, t) in enumerate(items):
        rows.append('<div class="chk" style="top:%dpx"><div class="bx"><div class="fill hide" id="kF%d"></div>%s</div>'
                    '<div class="tx">%s</div></div>' % (60 + i * 110, i, TICK2, lab))
    L.append('<div class="g full" id="gK"><div class="sheet hide" id="kS" style="left:190px;top:130px;width:700px;height:440px">'
             '<div class="sheen"></div>%s</div></div>' % "".join(rows))
    js('tl.set("#gK", {autoAlpha: 1}, %.3f);' % (t0 + 1.0))
    js('G.arrive("#kS", %.3f, {s: 0.6});' % (t0 + 1.0))
    for i, (lab, t) in enumerate(items):
        js('G.arrive("#kF%d", %.3f, {s: 0.3, d: 0.5});' % (i, t - 0.05))
    js('gsap.set("#gK .bx svg", {opacity: 0});')
    for i, (lab, t) in enumerate(items):
        js('tl.to("#gK .chk:nth-child(%d) .bx svg", {opacity: 1, duration: 0.15}, %.3f);' % (i + 2, t + 0.05))
    js('G.blurOut("#gK", %.3f, 10, 0.3);' % out)
    bo(items[0][1] - 0.05, out - 0.2)


# L · «От і вся система … спланували мені контент на цілий тиждень» — the strip, done
def beat_l():
    t0 = S(u"система.", 151.68)
    t_t = S(u"тиждень.", 155.08)
    out = E(u"тиждень.", 155.08) + 0.15
    L.append('<div class="g full" id="gL">' + week("wL", 75, 300, done=True) + '</div>')
    js('tl.set("#gL", {autoAlpha: 1}, %.3f);' % (t0 - 0.3))
    for i in range(7):
        js('G.arrive("#wL_c%d", %.3f, {s: 0.6, y: 40});' % (i, t0 - 0.3 + 0.05 * i))
        js('G.arrive("#wL_k%d", %.3f, {s: 0.3, y: 0, ease: POP});' % (i, S(u"спланували", 153.04) + 0.13 * i))
    js('tl.to("#gL .cell", {keyframes: {y: [0, -16, 0]}, duration: 0.42, stagger: 0.05, ease: "sine.inOut"}, %.3f);' % t_t)
    js('G.blurOut("#gL", %.3f, 10, 0.3);' % out)


# M · CTA: консультація | під ключ → «пиши плюс в коментарі»
PEOPLE = ('<svg viewBox="0 0 48 48"><circle cx="17" cy="16" r="7"/><circle cx="33" cy="18" r="6"/>'
          '<path d="M4 40c1-8 7-12 13-12s12 4 13 12"/><path d="M30 28c6 0 12 3 14 11"/></svg>')
KEY = ('<svg viewBox="0 0 48 48"><circle cx="15" cy="24" r="9"/><path d="M24 24h20M38 24v8M32 24v6"/></svg>')


def beat_m():
    t_kons = S(u"консультація,", 157.88)
    t_kl = S(u"ключ,", 161.90)
    t_out1 = E(u"готово.", 163.26) + 0.1
    t_pl = S(u"плюс", 166.44)
    t_pyshy = S(u"пиши", 166.10)
    L.append('<div class="g full" id="gM">'
             '<div class="opt sheet hide" id="mA" style="left:60px"><div class="t-micro">%s</div>'
             '<div class="nm">%s</div><div class="ic">%s</div></div>'
             '<div class="vs hide" id="mV">%s</div>'
             '<div class="opt sheet hide" id="mB" style="left:570px"><div class="t-micro">%s</div>'
             '<div class="nm">%s</div><div class="ic">%s</div></div></div>'
             % (u"РАЗОМ", u"Консуль&shy;тація", PEOPLE, u"або", u"ЗА ТЕБЕ", u"Під ключ", KEY))
    L.append('<div class="g full" id="gM2"><div class="cmt hide" id="mC"><div class="av"></div>'
             '<div class="cph" id="mPh">%s</div><div class="pl hide" id="mPl">+</div>'
             '<div class="snd">%s</div></div></div>' % (u"Додай коментар…", SEND))
    js('tl.set("#gM", {autoAlpha: 1}, %.3f);' % (t_kons - 0.3))
    js('G.arrive("#mA", %.3f, {s: 0.6});' % (t_kons - 0.2))
    js('G.arrive("#mV", %.3f, {s: 0.3});' % (S(u"або", 160.82) - 0.05))
    js('G.arrive("#mB", %.3f, {s: 0.6});' % (t_kl - 0.45))
    js('G.sheen("#mB .sheen", %.3f);' % t_kl)
    js('G.blurOut("#gM", %.3f, 10, 0.3);' % t_out1)
    bo(t_kons - 0.05, E(u"консультація,", 157.88))
    bo(S(u"під", 161.72) - 0.05, E(u"ключ,", 161.90))
    js('tl.set("#gM2", {autoAlpha: 1}, %.3f);' % (t_pyshy - 0.6))
    js('G.arrive("#mC", %.3f, {s: 0.7});' % (t_pyshy - 0.6))
    js('tl.set("#mPh", {autoAlpha: 0}, %.3f);' % (t_pl - 0.02))
    js('G.arrive("#mPl", %.3f, {s: 2.2, ease: POP, d: 0.5});' % (t_pl - 0.02))
    js('G.bump("#mC .snd", %.3f);' % (t_pl + 0.6))
    js('G.haptic("#mC", %.3f);' % (t_pl + 0.7))
    js('G.blurOut("#gM2", %.3f, 10, 0.3);' % (DUR - 0.45))
    bo(t_pl - 0.03, E(u"плюс", 166.44))


def main():
    for fn in (beat_a, beat_c, beat_d, beat_e, split, beat_fg, beat_h, beat_i, beat_j, beat_k, beat_l, beat_m):
        J.append("  /* %s */" % fn.__name__)
        fn()
    head = [g.js(), "var G = helpers(tl);",
            'gsap.set("#vid", {transformOrigin: "540px 900px"});',
            'tl.fromTo("#vid", {scale: 1}, {scale: 1.045, duration: %.3f, ease: "none"}, 0);' % DUR]
    doc = k.document(
        title=u"Reel 55 — plan with me",
        plate="assets/base.mp4",
        gfx_html=g.defs() + "\n" + "\n".join(L),
        gfx_js="\n".join(head + J),
        caps=CAPS,
        blackout=sorted(BLACKOUT),
    )
    io.open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(doc)
    print("index.html  %d captions, %d blackouts, %d js lines" % (len(CAPS), len(BLACKOUT), len(J)))


main()
