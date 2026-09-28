# -*- coding: utf-8 -*-
"""Reel 12 — «Бачила питання в Threads». SMM reporting via Windsor + Claude.

Variant B, refined glass (STYLE.md §0). The middle of this reel is the
approved style test (`style-test/build.py`, PLAN beats 4-6 and 11-12), lifted
onto the kit document with her real plate and re-timed to her real words.

The one object is **the report**: bare at the top (a Threads post, somebody
doing it all «вручну»), paid off at the end (the Monday report that arrives by
itself and lands as a notification).

The chain, near -> behind -> over -> near:
    Threads post rises off her tablet -> folds into her name capsule ->
    the capsule becomes a toggle, ON on «автоматизувати» -> the toggle
    becomes the glass shelf, its knob the Windsor tile -> cable, Claude,
    flips to ChatGPT -> the shelf's frost spreads into the room -> five
    sources wired into the hub -> the wall on «мільйон» -> collapses into
    the hub -> a repeat ring, the hub flips to Claude -> iris onto burgundy:
    a month with every Monday lit -> the month shrinks to «ПН 09:00», the
    sources stream into Claude, criteria tick -> the report grows out of the
    Claude tile -> folds into a notification as the iris closes onto it ->
    later, a comment composer where «+» is typed and liked.

Her cut: two shots, 0-11.33 (reads the post off a tablet, looking down) and
11.33-44.39 (to camera). No inserts, no pull-outs.

usage: python build.py
"""
import io
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
from kit import Kit  # noqa: E402
from glass import Glass, available  # noqa: E402

DUR = 44.350           # 1331 plate frames / 30 (work/w40-queue.log)
FPS = 30
k = Kit(width=1080, height=1920, fps=FPS, duration=DUR)
g = Glass()
k.css(g.css())

BEATS = []


def beat(fn):
    BEATS.append(fn)
    return fn


# ---------------------------------------------------------------------------
# NO-PAINT ZONES — her own editing (STYLE.md §4a). Two long shots, a single
# hard cut at 11.33, no closeups and no pull-outs (tools/shots.py,
# tools/pullouts.py both clean). Nothing is hers alone.
NO_PAINT = []

# ---------------------------------------------------------------------------
# Words. Script spelling on her timing (work/r12/captions.json, settled via
# fixes.json + caption-patch.json). Ends are re-derived here from the next
# start, the same rule align.py uses, because the patch dropped a stray dash
# and merged «і ти хочеш», which left two holes in the rail.
CAPS = k.load_captions(os.path.join(ROOT, "work", "r12", "captions.json"))
for _a, _b in zip(CAPS, CAPS[1:]):
    _a["e"] = round(max(_a["s"] + 0.10, _b["s"] - 0.085), 3)


def _n(s):
    return "".join(ch for ch in s.lower() if ch.isalnum() or ch == "+")


def at(word, n=1):
    """The n-th caption carrying `word` (punctuation ignored)."""
    hit = 0
    for c in CAPS:
        if _n(word) in [_n(x) for x in c["w"].split()]:
            hit += 1
            if hit == n:
                return c
    raise KeyError(word)


def S(w, n=1):
    return at(w, n)["s"]


def E(w, n=1):
    return at(w, n)["e"]


T = {
    "pryvit": S(u"Привіт"), "ruta": S(u"Рута"), "tvoya": S(u"твоя"),
    "prod_e": E(u"продюсерка"), "rozkazhu": S(u"розкажу"),
    "avtomat": S(u"автоматизувати"),
    "naiprost": S(u"найпростіший"), "naishvyd": S(u"найшвидший"),
    "variant": S(u"варіант"),
    "windsor1": S("Windsor"), "pidkl": S(u"підключений"),
    "claude": S("Claude"), "chatgpt": S("ChatGPT"), "chatgpt_e": E("ChatGPT"),
    "ig": S(u"Інстаграм"), "fb": S(u"Фейсбук"), "target": S(u"таргет"),
    "tiktok": S(u"ТікТок"), "stat": S(u"статистику"),
    "milyon": S(u"мільйон"), "danykh_e": E(u"даних"),
    "nalasht": S(u"налаштувати"), "povtor": S(u"повторювану"),
    "shtuchn": S(u"штучному"),
    "napr": S(u"Наприклад"), "ponedilok": S(u"понеділок"),
    "ponedilok_e": E(u"понеділок"),
    "claude2": S("Claude", 2), "zbyraye": S(u"збирає"),
    "stat2": S(u"статистику", 2),
    "analizuye": S(u"аналізує"), "tvoyimy": S(u"твоїми"),
    "kryter": S(u"критеріями"),
    "vydaye": S(u"видає"), "harnenko": S(u"гарненько"),
    "sform": S(u"сформований"), "zvit": S(u"звіт"), "zvit_e": E(u"звіт"),
    "tada": S(u"Тадааам"), "avtomatyz_e": E(u"Автоматизація"),
    "vorkflou": S(u"воркфлоу"), "stav": S(u"став"), "plus": S("+"),
    "koment": S(u"коментарі"), "pospilk": S(u"поспілкуємось"),
    "dur": DUR,
}


def js(src, **extra):
    """`@name` -> a literal time. Literals, not variables, because
    tools/review.py reads the timeline off the generated numbers."""
    vals = dict(T)
    vals.update(extra)

    def rep(m):
        v = vals[m.group(1)]
        return "%.3f" % v if isinstance(v, (int, float)) else str(v)
    return re.sub(r"@(\w+)", rep, src)


# ---------------------------------------------------------------------------
# Mattes (tools/matte.py). Frame ranges as the tool cut them: (first, count).
MATTES = {"post": (0, 226), "room": (538, 207), "tada": (1045, 80)}

# the post — its lower edge tucks behind her head while she reads it
k.matte("post", MATTES["post"][0] / 30.0, MATTES["post"][1] / 30.0)
# the room — the five sources and the wall sit behind her
k.matte("room", MATTES["room"][0] / 30.0, MATTES["room"][1] / 30.0)


def matte_from(name, t):
    """A matte that only switches on part-way through its cut: the tada clip
    starts under the closing takeover, and her matte on top of a full-frame
    burgundy ground would paste her back over it. Media start is offset by
    whole frames so it still lands on its own pixels."""
    f0, n = MATTES[name]
    fs = int(math.ceil(t * FPS - 1e-6))
    off = fs - f0
    k._mattes.append(
        '      <video id="matte-%s" class="plate matte" '
        'src="assets/mattes/%s.webm"\n'
        '             data-start="%.3f" data-duration="%.3f" '
        'data-media-start="%.3f"\n'
        '             muted playsinline></video>'
        % (name, name, fs / 30.0, (n - off) / 30.0, off / 30.0))


# «Тадааам» — her arm goes up through the notification; it passes in front.
matte_from("tada", 35.50)

# ---------------------------------------------------------------------------
# Small SVG glyphs (strokes, not emoji — §5a.11)
REPEAT = ('<svg viewBox="0 0 28 28" class="rp"><path d="M5 12a9 9 0 0 1 15.5-5.2L23 9"/>'
          '<path d="M23 3.5V9h-5.5"/><path d="M23 16a9 9 0 0 1-15.5 5.2L5 19"/>'
          '<path d="M5 24.5V19h5.5"/></svg>')
UP = '<svg viewBox="0 0 22 22"><path d="M11 18V4"/><path d="M4.5 10.5 11 4l6.5 6.5"/></svg>'
BARS = ('<svg class="mk" viewBox="0 0 24 24"><rect x="3.5" y="12" width="4.4" height="8.5" rx="1.8"/>'
        '<rect x="9.8" y="7" width="4.4" height="13.5" rx="1.8"/>'
        '<rect x="16.1" y="3" width="4.4" height="17.5" rx="1.8"/></svg>')
HEART = ("M12 20.6s-7.6-4.5-9.4-9.3C1.3 7.8 3.5 4.4 7 4.4c2 0 3.7 1.1 5 3 "
         "1.3-1.9 3-3 5-3 3.5 0 5.7 3.4 4.4 6.9-1.8 4.8-9.4 9.3-9.4 9.3z")
BUBBLE = "M20.5 11.6a8.5 8.5 0 0 1-12.4 7.6L3.5 20.5l1.3-4.4A8.5 8.5 0 1 1 20.5 11.6z"
REPOST = "M4 12V9.5a3 3 0 0 1 3-3h11M15 3.5l3 3-3 3M20 12v2.5a3 3 0 0 1-3 3H6M9 20.5l-3-3 3-3"
SEND = "M21 3 10.2 13.8M21 3l-6.6 18-4.2-7.2L3 9.6z"
PERSON = ('<svg viewBox="0 0 24 24"><circle cx="12" cy="9" r="4.3"/>'
          '<path d="M4.2 21c1.1-4.4 4.3-6.6 7.8-6.6s6.7 2.2 7.8 6.6z"/></svg>')
CHECK = '<svg viewBox="0 0 24 24"><path d="M6.2 12.6l3.9 3.9 7.7-8.6"/></svg>'


def wm(size=128):
    return Glass.wordmark("w", dot=True, size=size)


k.css("""
.abs, .cx { position: absolute; }
.hide { opacity: 0; visibility: hidden; }
""")

# =================================================================== b01
# «Люди, які автоматизували … Ми втомилися все робити вручну»
POST = [u"Люди,", u"які", u"автоматизували", u"свою", u"роботу", u"для",
        u"звітності", u"в", u"СММ.", u"Підкажіть,", u"які", u"ресурси",
        u"використовуєте?", u"Ми", u"втомилися", u"все", u"робити", u"вручну"]
MARKER = (15, 16, 17)          # «все робити вручну»

k.css("""
/* ---- b01 · the Threads post she is reading ---- */
#g1post { left: 70px; top: 92px; width: 940px; height: 580px; border-radius: 64px;
  overflow: hidden; color: #17141c;
  background: linear-gradient(172deg, rgba(255,255,255,0.95) 0%, rgba(255,250,252,0.92) 55%,
              rgba(253,241,245,0.90) 100%);
  -webkit-backdrop-filter: blur(24px) saturate(1.5); backdrop-filter: blur(24px) saturate(1.5);
  box-shadow: inset 0 2px 1px #fff, inset 0 -30px 60px -30px rgba(180,18,47,0.14),
              0 60px 120px -40px rgba(20,2,8,0.6); }
#g1post .sheen { mix-blend-mode: normal; opacity: 0.5; }
#pWho { left: 52px; top: 44px; width: 380px; height: 92px; filter: blur(7px); }
#pAv { position: absolute; left: 0; top: 2px; width: 88px; height: 88px; border-radius: 50%;
  background: linear-gradient(140deg, #e8c6cf 0%, #9c7280 100%); }
#pH1 { position: absolute; left: 112px; top: 18px; width: 250px; height: 28px; border-radius: 14px;
  background: rgba(23,20,28,0.42); }
#pH2 { position: absolute; left: 112px; top: 60px; width: 150px; height: 20px; border-radius: 10px;
  background: rgba(23,20,28,0.20); }
#pTime { left: 448px; top: 66px; font-size: 28px; font-weight: 500; color: rgba(23,20,28,0.56); }
#pTh { right: 52px; top: 56px; width: 62px; height: 62px; }
#pTh svg { width: 100%; height: 100%; fill: #17141c; }
#pTxt { left: 52px; top: 168px; width: 836px; font-size: 46px; font-weight: 500;
  line-height: 62px; letter-spacing: -0.01em; }
.pw { color: rgba(23,20,28,0.32); }
.pw.hl { background-image: linear-gradient(rgba(255,110,156,0.55), rgba(255,110,156,0.55));
  background-repeat: no-repeat; background-position: 0 86%; background-size: 0% 50%; }
#pAct { left: 52px; top: 500px; display: flex; gap: 46px; align-items: center;
  font-size: 30px; font-weight: 500; color: rgba(23,20,28,0.5); }
#pAct span { display: inline-flex; align-items: center; gap: 12px; }
#pAct svg { width: 42px; height: 42px; fill: none; stroke: rgba(23,20,28,0.62); stroke-width: 2;
  stroke-linecap: round; stroke-linejoin: round; }
""")


@beat
def b01_threads_post():
    """«Люди, які автоматизували свою роботу для звітності в СММ. Підкажіть,
    які ресурси використовуєте? Ми втомилися все робити вручну»

    The post rises off the tablet she is reading and settles above her head,
    lower edge tucked behind her hair (matte `post`). Each word lights on the
    frame she reads it — Apple Music lyrics — and a pink marker sweeps «все
    робити вручну». The card says every word, so captions black out.
    She reads «втомилися все робити», not the script's «втомились робити
    все»; the card follows her, so the light runs in order."""
    words = json.load(io.open(os.path.join(ROOT, "work", "r12", "words.json"),
                              encoding="utf-8"))["words"][:len(POST)]
    spans = []
    for i, w in enumerate(POST):
        spans.append('<span class="pw%s" id="pw%d">%s</span>'
                     % (" hl" if i in MARKER else "", i, w))
    act = "".join('<span><svg viewBox="0 0 24 24"><path d="%s"/></svg>%s</span>' % (p, n)
                  for p, n in ((HEART, "48"), (BUBBLE, "23"), (REPOST, "5"), (SEND, "")))
    html = u'''
      <div class="g full" id="g1">
        <div id="g1post" class="abs edge">
          <div class="cx" id="pWho"><div id="pAv"></div><div id="pH1"></div><div id="pH2"></div></div>
          <div class="cx" id="pTime">· 2 год</div>
          <div class="cx" id="pTh">%s</div>
          <div class="cx" id="pTxt">%s</div>
          <div class="cx" id="pAct">%s</div>
          <div class="sheen"></div>
        </div>
      </div>''' % (g.mark("threads", ""), " ".join(spans), act)
    lines = []
    for i, w in enumerate(words):
        t = max(0.02, w["s"])
        lines.append('  tl.to("#pw%d", {color: "#17141c", duration: 0.16, ease: "power1.out"}, %.3f);'
                     % (i, t))
    for i in MARKER:
        w = words[i]
        d = max(0.12, min(w["e"], words[i + 1]["s"] if i + 1 < len(words) else w["e"]) - w["s"])
        lines.append('  tl.to("#pw%d", {backgroundSize: "100%% 50%%", duration: %.3f, ease: "none"}, %.3f);'
                     % (i, d, w["s"]))
    src = js('''
  tl.set("#g1", {autoAlpha: 1}, 0.000);
  gsap.set("#g1post .sheen", {xPercent: -120});
  // it rises off the tablet in her left hand (x 850, y 1320) to its seat
  tl.fromTo("#g1post", {x: 310, y: 938, scale: 0.2, rotation: -9},
            {x: 0, y: 0, scale: 1, rotation: 0, duration: 1.0, ease: SOFT}, 0.000);
  tl.fromTo("#g1post", {autoAlpha: 0.55, filter: "blur(6px)"},
            {autoAlpha: 1, filter: "blur(0px)", duration: 0.4, ease: "power2.out", immediateRender: false}, 0.000);
  tl.to("#g1post .sheen", {xPercent: 120, duration: 0.8, ease: "power2.inOut"}, 0.700);
LINES
  // «Привіт» — the post folds up into her name capsule
  tl.to("#g1post", {scaleY: 0.255, scaleX: 0.83, y: -82, duration: 0.40, ease: "power3.in"}, @pryvit);
  tl.to("#g1post", {autoAlpha: 0, filter: "blur(10px)", duration: 0.24, ease: "power2.in"}, @t_fade);
  tl.to("#g1", {autoAlpha: 0, duration: 0.02}, @t_off);''',
             t_fade=T["pryvit"] + 0.16, t_off=T["pryvit"] + 0.44)
    return html, src.replace("LINES", "\n".join(lines))


# =================================================================== b02
k.css("""
/* ---- b02 · her name capsule, which becomes a toggle ---- */
#g2cap { left: 150px; top: 226px; width: 780px; height: 148px; border-radius: 74px; }
/* the name tag is centred; the settings row that replaces it is not */
#g2av { left: 184px; top: 26px; width: 96px; height: 96px; border-radius: 50%; overflow: hidden;
  box-shadow: 0 0 0 3px rgba(255,255,255,0.55), 0 10px 24px -8px rgba(10,0,4,0.5); }
#g2av img { width: 100%; height: 100%; object-fit: cover; display: block; }
#g2name { left: 306px; top: 22px; font-size: 48px; font-weight: 700; letter-spacing: -0.015em; }
#g2role { left: 306px; top: 82px; font-size: 32px; font-weight: 500; color: rgba(255,255,255,0.76); }
#g2ic { left: 26px; top: 26px; width: 96px; height: 96px; }
#g2lab { left: 148px; top: 44px; font-size: 46px; font-weight: 700; letter-spacing: -0.015em; }
#g2sw { right: 28px; top: 29px; width: 170px; height: 90px; border-radius: 45px; overflow: hidden;
  background: rgba(255,255,255,0.16);
  box-shadow: inset 0 2px 6px rgba(0,0,0,0.35), inset 0 0 0 1.5px rgba(255,255,255,0.22); }
#g2fill { position: absolute; inset: 0; border-radius: 45px;
  background: linear-gradient(90deg, #a8102c 0%, #e0204b 55%, #ff6e9c 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.45), inset 0 -10px 18px -8px rgba(255,190,210,0.5); }
#g2knob { position: absolute; left: 6px; top: 6px; width: 78px; height: 78px; border-radius: 39px;
  background: linear-gradient(160deg, #ffffff 0%, #fff5f8 60%, #f3dde4 100%);
  box-shadow: 0 6px 14px rgba(20,2,8,0.35), inset 0 -4px 8px rgba(180,18,47,0.12); }
#g2rip { left: 150px; top: 226px; width: 780px; height: 148px; border-radius: 74px;
  border: 3px solid rgba(255,255,255,0.75); }
""")


@beat
def b02_name_toggle():
    """«Привіт, я Рута — твоя технічна продюсерка, і зараз я розкажу як це все
    можна автоматизувати!»

    The capsule says «Рута · технічна продюсерка» while she does — blackout.
    Then it becomes an iOS settings row, «Звітність СММ», whose switch flips ON
    on «автоматизувати»: liquid stretch mid-travel, the track fills burgundy
    to pink. The knob is the object that carries on into the next beat."""
    html = u'''
      <div class="g full" id="g2">
        <div class="cx hide" id="g2rip"></div>
        <div id="g2cap" class="dglass edge abs">
          <div class="cx" id="g2av"><img src="assets/avatar.jpg" alt=""></div>
          <div class="cx" id="g2name">Рута</div>
          <div class="cx" id="g2role">технічна продюсерка</div>
          <div class="cx hide" id="g2ic"><div class="jelly">%s</div></div>
          <div class="cx hide" id="g2lab">Звітність СММ</div>
          <div class="cx hide" id="g2sw"><div id="g2fill"></div><div id="g2knob"></div></div>
        </div>
      </div>''' % BARS
    src = js('''
  tl.set("#g2", {autoAlpha: 1}, @t_in);
  // the folded post lands as a capsule
  tl.fromTo("#g2cap", {autoAlpha: 0, filter: "blur(10px)"},
            {autoAlpha: 1, filter: "blur(0px)", duration: 0.30, ease: "power2.out"}, @t_in);
  tl.fromTo("#g2cap", {scaleY: 0.72, scaleX: 1.05}, {scaleY: 1, scaleX: 1, duration: 0.75, ease: POP, immediateRender: false}, @t_in);
  gsap.set(["#g2av", "#g2name", "#g2role"], {autoAlpha: 0});
  // «Рута»
  tl.fromTo("#g2av", {scale: 0.5, autoAlpha: 0}, {scale: 1, autoAlpha: 1, duration: 0.55, ease: SP}, @t_av);
  G.blurIn("#g2name", @ruta, 10, 0.32);
  tl.fromTo("#g2name", {x: -18}, {x: 0, duration: 0.6, ease: SP}, @ruta);
  // «технічна продюсерка»
  G.blurIn("#g2role", @t_role, 10, 0.32);
  tl.fromTo("#g2role", {x: -18}, {x: 0, duration: 0.6, ease: SP}, @t_role);

  // «розкажу» — the capsule turns into a settings row
  G.blurOut(["#g2av", "#g2name", "#g2role"], @t_swap, 10, 0.26);
  tl.fromTo("#g2ic", {autoAlpha: 0, scale: 0.5}, {autoAlpha: 1, scale: 1, duration: 0.6, ease: POP}, @rozkazhu);
  G.blurIn("#g2lab", @t_lab, 10, 0.32);
  tl.fromTo("#g2lab", {x: -18}, {x: 0, duration: 0.6, ease: SP}, @t_lab);
  tl.fromTo("#g2sw", {autoAlpha: 0, scale: 0.6}, {autoAlpha: 1, scale: 1, duration: 0.6, ease: POP}, @t_sw);
  gsap.set("#g2fill", {autoAlpha: 0});
  // «автоматизувати» — ON
  tl.to("#g2knob", {x: 80, duration: 0.46, ease: SP}, @avtomat);
  tl.to("#g2knob", {scaleX: 1.34, scaleY: 0.9, duration: 0.12, ease: "power2.out"}, @avtomat);
  tl.to("#g2knob", {scaleX: 1, scaleY: 1, duration: 0.45, ease: SP}, @t_knob);
  tl.to("#g2fill", {autoAlpha: 1, duration: 0.30, ease: "power1.out"}, @t_fill);
  G.bump("#g2cap", @t_fill);
  tl.fromTo("#g2rip", {scale: 1, autoAlpha: 0.7}, {scale: 1.16, autoAlpha: 0, duration: 0.8,
            ease: "power2.out", immediateRender: false}, @t_fill);

  // «найпростіший» — the row stretches into the shelf; the knob carries on
  tl.set("#g2knob", {autoAlpha: 0}, @t_hand);
  G.blurOut(["#g2ic", "#g2lab", "#g2sw"], @t_hand, 10, 0.22);
  tl.to("#g2cap", {scaleX: 1.2, scaleY: 2.0, y: 85, autoAlpha: 0, duration: 0.32, ease: "power2.in"}, @t_hand);
  tl.to("#g2", {autoAlpha: 0, duration: 0.02}, @t_off);''',
             t_in=T["pryvit"] + 0.15, t_av=T["ruta"] - 0.12,
             t_role=T["tvoya"] + 0.08, t_swap=T["rozkazhu"] - 0.16,
             t_lab=T["rozkazhu"] + 0.10, t_sw=T["rozkazhu"] + 0.22,
             t_knob=T["avtomat"] + 0.12, t_fill=T["avtomat"] + 0.04,
             t_hand=T["naiprost"] - 0.18, t_off=T["naiprost"] + 0.16)
    return html, src


# =================================================================== b04
# the room: hub, five heroes, the wall — geometry from the style test,
# checked against her real framing (head top y 580-660 in shot 2, face
# x 330-720; the heroes sit either side of her and her matte covers the rest)
HUB = (540, 300)
HERO = [("ig", "instagram", (185, 560)), ("fb", "facebook", (895, 560)),
        ("target", "meta", (150, 836)), ("tiktok", "tiktok", (930, 836)),
        ("stat", "googleanalytics", (190, 1110))]
PITCH = 124
cells = [(HUB[0] + i * PITCH, HUB[1] + j * PITCH)
         for j in range(-2, 14) for i in range(-4, 5)]


def nearest(p):
    return min(cells, key=lambda c: (c[0] - p[0]) ** 2 + (c[1] - p[1]) ** 2)


hero_cells = {key: nearest(c) for key, _, c in HERO}
FILL = [n for n in available() if n not in
        ("instagram", "facebook", "meta", "tiktok", "googleanalytics", "threads",
         "claude", "openai", "anthropic")]
wall = []
for (x, y) in cells:
    d = math.hypot(x - HUB[0], y - HUB[1])
    if d < 160 or (x, y) in hero_cells.values():
        continue
    i, j = (x - HUB[0]) // PITCH + 4, (y - HUB[1]) // PITCH + 2
    wall.append({"x": x, "y": y, "d": round(d, 1),
                 "o": round(max(0.40, 1 - d / 2300.0), 3),
                 "g": FILL[(i * 7 + j * 5 + i * j) % len(FILL)]})
MAXD = max(t["d"] for t in wall)


def wire(p):
    x0, y0 = p
    x1, y1 = HUB
    side = -1 if x0 < 540 else 1
    cx, cy = (x0 + x1) / 2 + side * 150, (y0 + y1) / 2 - 40
    return "M %d %d Q %d %d %d %d" % (x0, y0, cx, cy, x1, y1 + 60)


def repeat_ring():
    """two arcs round the hub with arrowheads, clockwise — the repeat mark"""
    cx = cy = 200
    r = 172
    out = []
    for a0, a1 in ((212, 352), (32, 172)):
        p0 = (cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0)))
        p1 = (cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1)))
        d = "M %.1f %.1f A %d %d 0 0 1 %.1f %.1f" % (p0 + (r, r) + p1)
        # arrowhead at p1, pointing along the clockwise tangent
        tx, ty = -math.sin(math.radians(a1)), math.cos(math.radians(a1))
        nx, ny = math.cos(math.radians(a1)), math.sin(math.radians(a1))
        L, Wd = 30, 22
        b = (p1[0] - tx * L, p1[1] - ty * L)
        head = "M %.1f %.1f L %.1f %.1f L %.1f %.1f" % (
            b[0] + nx * Wd, b[1] + ny * Wd, p1[0] + tx * 4, p1[1] + ty * 4,
            b[0] - nx * Wd, b[1] - ny * Wd)
        out.append((d, head))
    return out


k.css("""
/* ---- b04 · the shelf, then the room, then the hub ---- */
#softWrap, #roomTint { position: absolute; inset: 0; }
#roomTint { background: linear-gradient(180deg, rgba(62,8,24,0.14) 0%, rgba(40,5,15,0.28) 100%); }
#wires { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: visible; }
#wires .w { fill: none; stroke: rgba(255,255,255,0.55); stroke-width: 4; stroke-linecap: round; }
#wires .p { fill: none; stroke: #fff; stroke-width: 9; stroke-linecap: round; }
#wires .pk { filter: drop-shadow(0 0 8px rgba(255,150,185,0.95)); }
#wall { position: absolute; inset: 0; transform-origin: 540px 300px; }
.src { position: absolute; width: 168px; height: 168px; margin: -84px 0 0 -84px; }
.wt { position: absolute; width: 100px; height: 100px; margin: -50px 0 0 -50px; border-radius: 23px;
  background: linear-gradient(158deg, rgba(255,255,255,0.30) 0%, rgba(255,255,255,0.09) 52%,
              rgba(255,255,255,0.15) 100%);
  box-shadow: inset 0 1.5px 1px rgba(255,255,255,0.65), inset 0 -10px 18px -10px rgba(255,255,255,0.36),
              inset 0 0 0 1px rgba(255,255,255,0.10), 0 16px 30px -14px rgba(24,4,12,0.45);
  display: flex; align-items: center; justify-content: center; }
.wt svg { width: 46px; height: 46px; fill: #fff; opacity: 0.92; }

#dock { left: 70px; top: 235px; width: 940px; height: 300px; overflow: hidden; }
#cable { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: visible; }
.port { fill: #fff; }
#hubGlow { left: 240px; top: 0px; width: 600px; height: 600px;
  background: radial-gradient(circle, rgba(255,110,156,0.55) 0%, rgba(255,110,156,0) 60%); }
#aiGlow { left: 555px; top: 135px; width: 500px; height: 500px;
  background: radial-gradient(circle, rgba(255,110,156,0.6) 0%, rgba(255,110,156,0) 62%); }
.hubrip { left: 440px; top: 200px; width: 200px; height: 200px; }

#wWrap { left: 440px; top: 200px; width: 200px; height: 200px; perspective: 1100px; }
#wflip, #aflip { position: absolute; inset: 0; transform-style: preserve-3d; }
.face { position: absolute; inset: 0; backface-visibility: hidden; -webkit-backface-visibility: hidden; }
.face.back { transform: rotateY(180deg); }
#wface { border-radius: 50%; }
#wface .wmark { transform: translate(2%, -3%); }
#aiWrap, #aiGhost { left: 700px; top: 280px; width: 210px; height: 210px; }
#aiWrap { perspective: 1100px; }
#aiGhost .mk { opacity: 0.32; }
#aiGhost .clear { background: linear-gradient(158deg, rgba(255,255,255,0.22) 0%, rgba(255,255,255,0.06) 60%,
  rgba(255,255,255,0.10) 100%); }

#rep { position: absolute; left: 340px; top: 100px; width: 400px; height: 400px; overflow: visible;
  transform-origin: 200px 200px; filter: drop-shadow(0 0 14px rgba(255,110,156,0.85)); }
#rep .tube { fill: none; stroke: rgba(255,255,255,0.30); stroke-width: 28; stroke-linecap: round; }
#rep .core { fill: none; stroke: #fff; stroke-width: 12; stroke-linecap: round; stroke-linejoin: round; }
""")


@beat
def b04_windsor_room_hub():
    """«Як на мене, найпростіший і найшвидший варіант — це зробити це через
    Windsor, підключений до Claude або ChatGPT. У Windsor можна підключити
    Інстаграм, Фейсбук, таргет, ТікТок, статистику сайту і ще мільйон інших
    джерел даних, а потім налаштувати повторювану рутину в своєму штучному
    інтелекті.»

    One container because it is one object: the toggle's knob lands on the
    glass shelf as a disc with a ghost «w.», becomes the Windsor tile on
    «Windsor» and stays the hub for fifteen seconds. Style test §A and §B,
    re-timed to her words. The room goes soft behind her (a per-beat soft
    plate built with her matte, so she doesn't haloe) while the sources are
    wired in and the wall ripples out on «мільйон». Then the wall collapses
    back into the hub, a repeat ring draws round it on «повторювану» and keeps
    turning, and the hub flips to Claude on «штучному інтелекті» — the thing
    the iris opens out of."""
    f0, n = MATTES["room"]
    wall_html = "\n        ".join(
        '<div class="wt hide" id="wt%d" style="left:%dpx;top:%dpx">%s</div>'
        % (i, t["x"], t["y"], g.mark(t["g"], "")) for i, t in enumerate(wall))
    hero_html = "\n        ".join(
        '<div class="src hide" id="s-%s" style="left:%dpx;top:%dpx">'
        '<div class="clear edge">%s</div></div>' % (key, c[0], c[1], g.mark(ic))
        for key, ic, c in HERO)
    wires_html = "\n          ".join(
        '<path class="w" id="wr-%s" d="%s"/><g class="pk"><path class="p hide" id="wp-%s" d="%s"/></g>'
        % (key, wire(c), key, wire(c)) for key, _, c in HERO)
    ring = repeat_ring()
    ring_html = "".join('<path class="tube rpa" d="%s"/><path class="core rpa" id="rpa%d" d="%s"/>'
                        '<path class="core rph" id="rph%d" d="%s"/>' % (d, i, d, i, h)
                        for i, (d, h) in enumerate(ring))
    cab = "M 380 385 C 470 448 610 448 700 385"
    html = u'''
      <div class="g full" id="g4">
        <div id="softWrap" class="hide">
          <video id="soft" class="plate" src="assets/soft/room.mp4"
                 data-start="%(ss).3f" data-duration="%(sd).3f" data-media-start="0"
                 muted playsinline></video>
          <div id="roomTint"></div>
        </div>
        <svg id="wires" viewBox="0 0 1080 1920">
          %(wires)s
        </svg>
        <div id="wall">
        %(wall)s
        </div>
        %(heroes)s
        <div id="dock" class="shelf edge abs hide"><div class="sheen"></div></div>
        <svg id="cable" class="cab" viewBox="0 0 1080 1920">
          <path class="tube" id="cabT" d="%(cab)s"/>
          <path class="core" id="cabC" d="%(cab)s"/>
          <g class="pkg"><path class="pkt hide" id="cabP" d="%(cab)s"/></g>
          <circle class="port hide" cx="380" cy="385" r="11"/><circle class="port hide" cx="700" cy="385" r="11"/>
        </svg>
        <div id="hubGlow" class="abs hide"></div>
        <svg id="rep" class="hide" viewBox="0 0 400 400">%(ring)s</svg>
        <div class="sqring hubrip hide" id="hr0"></div><div class="sqring hubrip hide" id="hr1"></div>
        <div class="sqring hubrip hide" id="hr2"></div><div class="sqring hubrip hide" id="hr3"></div>
        <div class="sqring hubrip hide" id="hr4"></div>
        <div id="wWrap" class="abs hide">
          <div id="wflip">
            <div class="face front"><div id="wface" class="pearl">%(wm)s<div class="sheen"></div></div></div>
            <div class="face back"><div class="jelly">%(claude)s<div class="sheen" id="wsheen2"></div></div></div>
          </div>
        </div>
        <div id="aiGhost" class="abs hide"><div class="clear edge">%(claude)s</div></div>
        <div id="aiGlow" class="abs hide"></div>
        <div id="aiWrap" class="abs hide">
          <div id="aflip">
            <div class="face front"><div class="jelly">%(claude)s</div></div>
            <div class="face back"><div class="jelly">%(openai)s</div></div>
          </div>
        </div>
      </div>''' % {"ss": f0 / 30.0, "sd": n / 30.0, "wires": wires_html,
                   "wall": wall_html, "heroes": hero_html, "cab": cab, "ring": ring_html,
                   "wm": wm(128), "claude": g.mark("claude"), "openai": g.mark("openai")}
    cfg = {"hub": HUB, "maxd": MAXD,
           "wall": [{"x": t["x"], "y": t["y"], "d": t["d"], "o": t["o"]} for t in wall],
           "hero": [{"k": key, "x": c[0], "y": c[1], "cx": hero_cells[key][0], "cy": hero_cells[key][1],
                     "d": round(math.hypot(hero_cells[key][0] - HUB[0], hero_cells[key][1] - HUB[1]), 1),
                     "t": T[key] - 0.08} for key, _, c in HERO]}
    src = js('''
  var C4 = CFG4;
  tl.set("#g4", {autoAlpha: 1}, @t_in);
  gsap.set(["#dock .sheen", "#wface .sheen", "#wsheen2"], {xPercent: -120});
  gsap.set(C4.hero.map(function (h) { return "#wp-" + h.k; }), {autoAlpha: 0});

  // ============ A · near her: the toggle becomes the shelf ============
  // the knob, exactly where the switch left it (857, 300), becomes a disc
  gsap.set("#wWrap", {x: 317, y: 0, scale: 0.39});
  gsap.set("#wface .wmark", {autoAlpha: 0});
  tl.set("#wWrap", {autoAlpha: 1}, @t_in);
  tl.to("#wWrap", {x: -265, y: 85, scale: 0.75, duration: 0.8, ease: SP}, @t_knob);
  G.blurIn("#dock", @t_in, 14, 0.40);
  tl.fromTo("#dock", {scaleX: 0.83, scaleY: 0.49, y: -85}, {scaleX: 1, scaleY: 1, y: 0, duration: 0.9, ease: SP}, @t_in);
  // ghost slots: a faint «w.» on the disc, a faint Claude opposite
  tl.to("#wface .wmark", {autoAlpha: 0.22, duration: 0.4}, @t_ghost);
  G.blurIn("#aiGhost", @t_ghost, 12, 0.36);
  tl.fromTo("#aiGhost", {scale: 0.6, y: 26}, {scale: 1, y: 0, duration: 0.8, ease: POP}, @t_ghost);
  // «найшвидший» — one sweep across the glass
  tl.to("#dock .sheen", {xPercent: 120, duration: 0.7, ease: "power2.inOut"}, @naishvyd);
  // «варіант»
  G.bump("#wflip", @variant);
  G.bump("#aiGhost", @t_var2);

  // «Windsor» — the disc turns into the Windsor tile
  tl.to("#wface", {borderRadius: "22.4%", duration: 0.5, ease: SP}, @t_w);
  tl.to("#wWrap", {scale: 1.05, duration: 0.85, ease: POP}, @t_w);
  tl.fromTo("#wface .wmark", {scale: 0.6}, {scale: 1, autoAlpha: 1, duration: 0.6, ease: SP, immediateRender: false}, @windsor1);
  tl.to("#wface .sheen", {xPercent: 120, duration: 0.75, ease: "power2.inOut"}, @t_wsheen);

  // «підключений» — the cable
  var Lc = G.drawPrep("cabT"); G.drawPrep("cabC");
  tl.fromTo(".port", {scale: 0, transformOrigin: "50% 50%"}, {scale: 1, autoAlpha: 1, duration: 0.4, ease: POP, stagger: 0.42}, @t_port);
  tl.to(["#cabT", "#cabC"], {strokeDashoffset: 0, duration: 0.62, ease: "power2.inOut"}, @pidkl);

  // «Claude»
  G.blurOut("#aiGhost", @t_claude, 8, 0.25);
  G.blurIn("#aiWrap", @t_claude, 14, 0.36);
  tl.fromTo("#aiWrap", {x: 90, scale: 0.55}, {x: 0, scale: 1, duration: 0.85, ease: POP}, @t_claude);
  tl.fromTo("#aiWrap .front .mk", {scale: 0.55, autoAlpha: 0}, {scale: 1, autoAlpha: 1, duration: 0.55, ease: SP}, @t_claude2);
  tl.fromTo("#aiGlow", {autoAlpha: 0, scale: 0.6}, {autoAlpha: 1, scale: 1, duration: 0.32, ease: "power2.out"}, @t_cglow);
  tl.to("#aiGlow", {autoAlpha: 0, duration: 0.25, ease: "power2.in"}, @t_cglow2);
  G.packet("cabP", @t_pk1, 0.5);

  // «ChatGPT» — FLIP, started on the word that names the new face
  tl.fromTo("#aflip", {rotationY: 0}, {rotationY: 180, duration: 1.0, ease: FLIP}, @t_flip);
  tl.to("#aflip", {scale: 0.9, duration: 0.3, ease: "power2.out"}, @t_flip);
  tl.to("#aflip", {scale: 1, duration: 0.6, ease: SP}, @t_flip2);
  tl.fromTo("#aiGlow", {autoAlpha: 0}, {autoAlpha: 0.85, duration: 0.3, ease: "power2.out", immediateRender: false}, @t_gg);
  tl.to("#aiGlow", {autoAlpha: 0, duration: 0.5, ease: "power2.in"}, @t_gg2);
  G.packet("cabP", @t_pk2, 0.5);

  // ============ A -> B · the shelf's frost spreads into the room ============
  G.blurOut("#aiWrap", @t_x, 10, 0.34);
  tl.to("#aiWrap", {x: 60, scale: 0.8, duration: 0.34, ease: "power2.in"}, @t_x);
  tl.to(["#cabT", "#cabC"], {strokeDashoffset: Lc, duration: 0.4, ease: "power2.in"}, @t_x);
  tl.to(".port", {scale: 0, duration: 0.25, ease: "power2.in"}, @t_x2);
  tl.to("#dock", {scale: 1.35, duration: 0.7, ease: "power2.in"}, @t_x3);
  G.blurOut("#dock", @t_x2, 16, 0.5);
  tl.fromTo("#softWrap", {autoAlpha: 0}, {autoAlpha: 1, duration: 0.7, ease: "power1.inOut"}, @t_x4);
  tl.to("#wWrap", {x: 0, y: 0, scale: 1, duration: 0.95, ease: SP}, @t_x5);

  // ============ B · behind her: sources plug into the hub ============
  // one call per source, each on its own word (literal times: review.py
  // reads the timeline off the numbers)
  function plug(k, i, t) {
    var s = "#s-" + k;
    G.blurIn(s, t, 12, 0.36);
    tl.fromTo(s, {scale: 0.5, y: 40}, {scale: 1, y: 0, duration: 0.8, ease: POP}, t);
    tl.fromTo(s + " .mk", {scale: 0.55, autoAlpha: 0}, {scale: 1, autoAlpha: 1, duration: 0.55, ease: SP}, t + 0.1);
    G.drawPrep("wr-" + k);
    tl.to("#wr-" + k, {strokeDashoffset: 0, duration: 0.45, ease: "power2.inOut"}, t + 0.14);
    G.packet("wp-" + k, t + 0.4, 0.45);
    G.bump("#wflip", t + 0.84);
    G.ripple("#hr" + i, t + 0.86);
  }
HEROJS

  // «мільйон» — the wall ripples out of the hub, the heroes take their seats
  var tM = @t_m;
  tl.to("#wires", {autoAlpha: 0, duration: 0.3, ease: "power1.in"}, @t_m);
  C4.hero.forEach(function (h) {
    tl.to("#s-" + h.k, {x: h.cx - h.x, y: h.cy - h.y, scale: 100 / 168, duration: 0.7, ease: SP}, tM + h.d * 0.00042);
  });
  C4.wall.forEach(function (w, n) {
    var t = tM + w.d * 0.00042;
    tl.fromTo("#wt" + n, {autoAlpha: 0, scale: 0.3}, {autoAlpha: w.o, duration: 0.3, ease: "power2.out"}, t);
    tl.to("#wt" + n, {scale: 1, duration: 0.6, ease: SP}, t);
  });
  tl.fromTo("#wall", {scale: 1.1}, {scale: 1, duration: 1.5, ease: "power2.out"}, @t_m);
  tl.fromTo("#hubGlow", {autoAlpha: 0}, {autoAlpha: 1, duration: 0.6, ease: "power2.out"}, @t_m);

  // ============ B -> near · everything is pulled back into the hub ============
  var tC = @t_c;
  C4.wall.forEach(function (w, n) {
    tl.to("#wt" + n, {x: (C4.hub[0] - w.x) * 0.38, y: (C4.hub[1] - w.y) * 0.38, scale: 0, autoAlpha: 0,
                      duration: 0.42, ease: "power2.in"}, tC + (C4.maxd - w.d) * 0.00022);
  });
  C4.hero.forEach(function (h) {
    tl.to("#s-" + h.k, {x: (h.cx - h.x) + (C4.hub[0] - h.cx) * 0.38, y: (h.cy - h.y) + (C4.hub[1] - h.cy) * 0.38,
                        scale: 0, autoAlpha: 0, duration: 0.42, ease: "power2.in"}, tC + (C4.maxd - h.d) * 0.00022);
  });
  tl.to("#wflip", {scale: 1.14, duration: 0.4, ease: "power2.in"}, @t_c2);
  tl.to("#wflip", {scale: 1, duration: 0.6, ease: SP}, @t_c3);
  tl.to("#hubGlow", {autoAlpha: 0, duration: 0.5, ease: "power2.in"}, @t_c3);
  tl.to("#softWrap", {autoAlpha: 0, duration: 0.5, ease: "power1.inOut"}, @t_c4);

  // «повторювану рутину» — a repeat ring draws round the hub and keeps turning
  tl.set("#rep", {autoAlpha: 1}, @t_r);
  ["rpa0", "rpa1"].forEach(function (id) { G.draw(id, @t_r, 0.55); });
  tl.fromTo("#rep .tube", {autoAlpha: 0}, {autoAlpha: 1, duration: 0.4}, @t_r);
  tl.fromTo(["#rph0", "#rph1"], {autoAlpha: 0, scale: 0.4, transformOrigin: "50% 50%"},
            {autoAlpha: 1, scale: 1, duration: 0.45, ease: POP}, @t_r2);
  tl.fromTo("#rep", {rotation: 0}, {rotation: 400, duration: @t_rd, ease: "none"}, @t_r);
  G.ripple("#hr0", @rutynu);

  // «штучному інтелекті» — the hub turns over to Claude
  tl.fromTo("#wflip", {rotationY: 0}, {rotationY: 180, duration: 1.0, ease: FLIP}, @t_hf);
  tl.fromTo("#hubGlow", {autoAlpha: 0, scale: 0.8}, {autoAlpha: 0.9, scale: 1, duration: 0.4, ease: "power2.out", immediateRender: false}, @t_hf2);
  tl.to("#wsheen2", {xPercent: 120, duration: 0.7, ease: "power2.inOut"}, @t_hf3);

  // hands over to the takeover, which opens out of the ring
  tl.to("#g4", {autoAlpha: 0, duration: 0.02}, @t_off);'''.replace("CFG4", json.dumps(cfg)),
             t_in=T["naiprost"] - 0.18, t_knob=T["naiprost"] - 0.14,
             t_ghost=T["naiprost"] + 0.14, t_var2=T["variant"] + 0.08,
             t_w=T["windsor1"] - 0.06, t_wsheen=T["windsor1"] + 0.4,
             t_port=T["pidkl"] - 0.05,
             t_claude=T["claude"] - 0.12, t_claude2=T["claude"] - 0.02,
             t_cglow=T["claude"] + 0.05, t_cglow2=T["claude"] + 0.40,
             t_pk1=T["claude"] + 0.12,
             t_flip=T["chatgpt"] - 0.16, t_flip2=T["chatgpt"] + 0.14,
             t_gg=T["chatgpt"] + 0.1, t_gg2=T["chatgpt"] + 0.45, t_pk2=T["chatgpt"] + 0.35,
             t_x=T["chatgpt_e"] + 0.12, t_x2=T["chatgpt_e"] + 0.32,
             t_x3=T["chatgpt_e"] + 0.17, t_x4=T["chatgpt_e"] + 0.22,
             t_x5=T["chatgpt_e"] + 0.20,
             t_m=T["milyon"] - 0.04,
             t_c=T["danykh_e"] + 0.02, t_c2=T["danykh_e"] + 0.14,
             t_c3=T["danykh_e"] + 0.56, t_c4=T["danykh_e"] + 0.45,
             t_r=T["povtor"] - 0.06, t_r2=T["povtor"] + 0.40,
             t_rd=T["napr"] + 0.45 - (T["povtor"] - 0.06),
             rutynu=S(u"рутину"),
             t_hf=T["shtuchn"] - 0.16, t_hf2=T["shtuchn"] + 0.1, t_hf3=T["shtuchn"] + 0.6,
             t_off=T["napr"] + 0.38)
    herojs = "\n".join('  plug("%s", %d, %.3f);' % (key, i, T[key] - 0.08)
                       for i, (key, _, _) in enumerate(HERO))
    return html, src.replace("HEROJS", herojs)


# =================================================================== b08
# the takeover: calendar -> Claude collecting -> criteria -> the report
SEPT = []                                   # September 2026 starts on a Tuesday
for d in range(1, 31):
    SEPT.append((d, d % 7, d // 7))         # (date, col with Mon=0, row)
MONDAYS = [d for d, c, r in SEPT if c == 0]  # 7, 14, 21, 28
COLW = 760 / 7.0
SRC_POS = [("instagram", 130, 1010), ("facebook", 335, 1062), ("meta", 540, 1086),
           ("tiktok", 745, 1062), ("googleanalytics", 950, 1010)]
CRIT = [u"Охоплення", "ER", u"Ліди"]

# the report chart, seven days, smoothed with Catmull-Rom (style test)
VALS = [0.30, 0.37, 0.33, 0.50, 0.47, 0.69, 0.90]
CW, CH = 760, 230
pts = [(12 + i * (CW - 24) / 6.0, CH - 14 - v * (CH - 40)) for i, v in enumerate(VALS)]


def smooth(p):
    d = "M %.1f %.1f" % p[0]
    for i in range(len(p) - 1):
        p0 = p[i - 1] if i else p[i]
        p1, p2 = p[i], p[i + 1]
        p3 = p[i + 2] if i + 2 < len(p) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += " C %.1f %.1f %.1f %.1f %.1f %.1f" % (c1 + c2 + p2)
    return d


LINE = smooth(pts)
AREA = LINE + " L %.1f %d L %.1f %d Z" % (pts[-1][0], CH, pts[0][0], CH)
END_PT = pts[-1]

k.css("""
/* ---- b08 · over her: the burgundy takeover ---- */
#tk8 { position: absolute; inset: 0; clip-path: circle(0px at 540px 300px); }
/* the month */
#calWrap { left: 100px; top: 250px; width: 880px; height: 830px; transform-origin: 440px 50px; }
#cal { position: absolute; inset: 0; }
#calIc { left: 60px; top: 54px; width: 84px; height: 84px; }
#calT { left: 168px; top: 56px; } #calS { left: 168px; top: 110px; }
#calHair { left: 60px; right: 60px; top: 172px; }
#calGrid { left: 60px; top: 204px; width: 760px; height: 590px; }
.wd { position: absolute; top: 0; width: 108px; text-align: center; font-size: 24px; font-weight: 700;
  letter-spacing: 0.12em; color: rgba(23,20,28,0.42); }
.wd.m { color: #b4122f; }
#monBand { position: absolute; left: 4px; top: 50px; width: 100px; height: 536px; border-radius: 50px;
  background: #fbe3ea; transform-origin: 50% 0%; }
.dd { position: absolute; width: 108px; height: 92px; display: flex; align-items: center;
  justify-content: center; font-size: 38px; font-weight: 500; color: #17141c; }
.dd i { position: absolute; left: 12px; top: 4px; width: 84px; height: 84px; border-radius: 50%;
  background: linear-gradient(165deg, #e0204b 0%, #ab112e 50%, #6b081c 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.5), 0 10px 20px -8px rgba(70,4,20,0.6); }
.dd b { position: relative; font-weight: 500; }
/* Claude collecting */
#pnWrap { left: 0; top: 262px; width: 1080px; display: flex; justify-content: center; }
.pill { display: inline-flex; align-items: center; gap: 12px; height: 76px; padding: 0 30px 0 22px;
  border-radius: 38px; background: #fbe3ea; color: #b4122f; font-size: 34px; font-weight: 700;
  letter-spacing: 0.02em; box-shadow: 0 24px 50px -20px rgba(8,0,3,0.7), inset 0 2px 1px #fff; }
.rp { width: 34px; height: 34px; fill: none; stroke: #b4122f; stroke-width: 3; stroke-linecap: round;
  stroke-linejoin: round; }
#cTile { left: 420px; top: 520px; width: 240px; height: 240px; }
#cTile .sheen { mix-blend-mode: soft-light; }
#cGlow { left: 190px; top: 290px; width: 700px; height: 700px;
  background: radial-gradient(circle, rgba(255,110,156,0.55) 0%, rgba(255,110,156,0) 60%); }
.sq8 { position: absolute; width: 132px; height: 132px; margin: -66px 0 0 -66px; }
.crip { left: 420px; top: 520px; width: 240px; height: 240px; }
#critRow { left: 0; top: 862px; width: 1080px; display: flex; justify-content: center; gap: 22px; }
.crit { display: inline-flex; align-items: center; gap: 16px; height: 84px; padding: 0 34px 0 18px;
  border-radius: 42px; background: linear-gradient(170deg, #ffffff 0%, #fff4f7 100%); color: #17141c;
  font-size: 34px; font-weight: 700; box-shadow: 0 26px 50px -22px rgba(8,0,3,0.75), inset 0 2px 1px #fff; }
.ck { position: relative; width: 52px; height: 52px; border-radius: 50%;
  box-shadow: inset 0 0 0 3.5px rgba(180,18,47,0.30); }
.ck .f { position: absolute; inset: 0; border-radius: 50%;
  background: linear-gradient(165deg, #e0204b 0%, #ab112e 55%, #7a0a20 100%); }
.ck svg { position: absolute; inset: 0; width: 52px; height: 52px; fill: none; stroke: #fff;
  stroke-width: 3.4; stroke-linecap: round; stroke-linejoin: round; }
/* the report (style test §C) */
#cardWrap { left: 100px; top: 240px; width: 880px; height: 1000px; transform-origin: 440px 400px; }
#card { position: absolute; inset: 0; }
#chIcon { left: 60px; top: 54px; width: 84px; height: 84px; }
#chTitle { left: 168px; top: 56px; } #chSub { left: 168px; top: 110px; }
#chPill { right: 60px; top: 66px; height: 58px; padding: 0 24px 0 18px; border-radius: 29px;
  background: #fbe3ea; color: #b4122f; font-size: 26px; font-weight: 700; letter-spacing: 0.02em;
  display: flex; align-items: center; gap: 10px; box-shadow: inset 0 0 0 1px rgba(180,18,47,0.08); }
#chPill .rp { width: 28px; height: 28px; }
#hair1 { left: 60px; right: 60px; top: 172px; }
#kLabel { left: 60px; top: 206px; }
#kNum { left: 52px; top: 232px; }
#kDelta { right: 60px; top: 318px; height: 62px; padding: 0 24px; border-radius: 31px; background: #fde4ec;
  color: #b4122f; font-size: 30px; font-weight: 700; display: flex; align-items: center; gap: 8px; }
#kDelta svg { width: 22px; height: 22px; fill: none; stroke: #b4122f; stroke-width: 3.4; stroke-linecap: round; stroke-linejoin: round; }
#chart { left: 60px; top: 432px; width: 760px; height: 230px; overflow: visible; }
.gridl { stroke: rgba(23,20,28,0.07); stroke-width: 2; stroke-dasharray: 2 10; stroke-linecap: round; }
#days { left: 60px; top: 676px; width: 760px; display: flex; justify-content: space-between;
  font-size: 22px; font-weight: 500; color: rgba(23,20,28,0.36); letter-spacing: 0.04em; }
#days span { width: 60px; text-align: center; }
#days span:first-child { margin-left: -18px; } #days span:last-child { margin-right: -18px; }
.row { position: absolute; left: 60px; right: 60px; height: 84px; display: flex; align-items: center; }
.row .ri { width: 64px; height: 64px; border-radius: 18px; background: #fbe3ea; display: flex;
  align-items: center; justify-content: center; margin-right: 22px; box-shadow: inset 0 0 0 1px rgba(180,18,47,0.06); }
.row .ri svg { width: 34px; height: 34px; fill: #b4122f; }
.row .rl { font-size: 32px; font-weight: 500; flex: 1; letter-spacing: -0.005em; }
.row .rv { font-size: 34px; font-weight: 700; letter-spacing: -0.01em; }
.row .rd { font-size: 24px; font-weight: 700; color: #d0194a; margin-left: 14px; width: 74px; text-align: right; }
.rowline { position: absolute; left: 146px; right: 60px; height: 2px; background: rgba(23,20,28,0.06); }
""")


@beat
def b08_takeover_monday_report():
    """«Наприклад, кожен понеділок Claude збирає статистику з усіх джерел,
    аналізує її за твоїми критеріями і видає тобі гарненько сформований звіт.»

    The iris opens out of the repeat ring onto burgundy. A month grows out of
    the hub point and every Monday lights top to bottom on «понеділок». The
    month shrinks into the chip «ПН 09:00»; Claude lands under it and the five
    sources stream into it, one bump per hit. Three criteria tick on «твоїми
    критеріями». Then the report grows out of the Claude tile — which flies up
    to become the report's own icon, the chip becoming its pill — style test
    §C. Captions stay on (white on the plaque); nothing here repeats a word."""
    wd = "".join('<div class="wd%s" style="left:%dpx">%s</div>'
                 % (" m" if i == 0 else "", round(i * COLW), n)
                 for i, n in enumerate([u"ПН", u"ВТ", u"СР", u"ЧТ", u"ПТ", u"СБ", u"НД"]))
    dd = "".join('<div class="dd%s" id="dd%d" style="left:%dpx;top:%dpx">%s<b>%d</b></div>'
                 % (" mon" if c == 0 else "", d, round(c * COLW), 56 + r * 106,
                    '<i id="ddi%d"></i>' % d if c == 0 else "", d)
                 for d, c, r in SEPT)
    srcs = "".join('<div class="sq8" id="sq%d" style="left:%dpx;top:%dpx"><div class="clear edge">%s</div></div>'
                   % (i, x, y, g.mark(ic)) for i, (ic, x, y) in enumerate(SRC_POS))
    crit = "".join('<div class="crit" id="cr%d"><div class="ck"><div class="f" id="crf%d"></div>'
                   '<svg viewBox="0 0 24 24"><path id="crk%d" d="M6.2 12.6l3.9 3.9 7.7-8.6"/></svg></div>%s</div>'
                   % (i, i, i, c) for i, c in enumerate(CRIT))
    rows = []
    for i, (ic, lab, val, dl) in enumerate([("instagram", "Instagram", "12,4K", "+18%"),
                                            ("tiktok", "TikTok", "8,1K", "+9%"),
                                            ("meta", u"Реклама", u"ROAS 3,2×", "")]):
        top = 736 + i * 84
        rows.append('<div class="row" id="row%d" style="top:%dpx"><div class="ri">%s</div>'
                    '<div class="rl">%s</div><div class="rv">%s</div><div class="rd">%s</div></div>'
                    % (i, top, g.mark(ic, ""), lab, val, dl))
        if i < 2:
            rows.append('<div class="rowline" id="rl%d" style="top:%dpx"></div>' % (i, top + 83))
    html = u'''
      <div class="g full" id="g8">
        <div id="tk8">
          <div class="tkg"></div>
          <div class="aur a1"></div><div class="aur a2"></div><div class="aur a3"></div>
          <div class="grain"></div>
          <div id="calWrap" class="abs hide"><div id="cal" class="sheet">
            <div class="cx" id="calIc"><div class="jelly">%(claude)s</div></div>
            <div class="cx t-title" id="calT">Вересень</div>
            <div class="cx t-sub" id="calS">2026 · твоя рутина</div>
            <div class="cx hair" id="calHair"></div>
            <div class="cx" id="calGrid"><div id="monBand"></div>%(wd)s%(dd)s</div>
            <div class="sheen"></div>
          </div></div>
          <div id="cGlow" class="abs hide"></div>
          <div class="sqring crip hide" id="cr_r0"></div><div class="sqring crip hide" id="cr_r1"></div>
          %(srcs)s
          <div class="cx" id="critRow">%(crit)s</div>
          <div id="cardWrap" class="abs hide">
            <div id="card" class="sheet">
              <div class="cx hide" id="chIcon"><div class="jelly">%(claude)s</div></div>
              <div class="cx t-title" id="chTitle">Підсумок тижня</div>
              <div class="cx t-sub" id="chSub">21–27 вересня · 5 джерел</div>
              <div class="cx hide" id="chPill">%(repeat)s<span>ПН 09:00</span></div>
              <div class="cx hair" id="hair1"></div>
              <div class="cx t-micro" id="kLabel">ОХОПЛЕННЯ</div>
              <div class="cx t-big" id="kNum">+0%%</div>
              <div class="cx" id="kDelta">%(up)s<span>20,5K</span></div>
              <svg class="cx" id="chart" viewBox="0 0 %(cw)d %(ch)d">
                <line class="gridl" x1="0" x2="%(cw)d" y1="30" y2="30"/>
                <line class="gridl" x1="0" x2="%(cw)d" y1="100" y2="100"/>
                <line class="gridl" x1="0" x2="%(cw)d" y1="170" y2="170"/>
                <path id="cArea" d="%(area)s" fill="url(#gArea)"/>
                <path id="cLine" d="%(line)s" fill="none" stroke="url(#gLine)" stroke-width="8" stroke-linecap="round"/>
                <circle id="cRing" class="hide" cx="%(ex).1f" cy="%(ey).1f" r="12" fill="none" stroke="#ff6e9c" stroke-width="3"/>
                <circle id="cDot" cx="%(ex).1f" cy="%(ey).1f" r="12" fill="#fff" stroke="#b4122f" stroke-width="6"/>
              </svg>
              <div class="cx" id="days"><span>ПН</span><span>ВТ</span><span>СР</span><span>ЧТ</span><span>ПТ</span><span>СБ</span><span>НД</span></div>
              %(rows)s
              <div class="sheen"></div>
            </div>
          </div>
          <div class="cx" id="pnWrap"><div class="pill hide" id="pn">%(repeat)s<span>ПН 09:00</span></div></div>
          <div id="cTile" class="abs hide"><div class="jelly">%(claude)s<div class="sheen"></div></div></div>
        </div>
      </div>''' % {"claude": g.mark("claude"), "wd": wd, "dd": dd, "srcs": srcs, "crit": crit,
                   "repeat": REPEAT, "up": UP, "cw": CW, "ch": CH, "area": AREA, "line": LINE,
                   "ex": END_PT[0], "ey": END_PT[1], "rows": "\n              ".join(rows)}
    mons = "[" + ",".join(str(d) for d in MONDAYS) + "]"
    src = js('''
  tl.set("#g8", {autoAlpha: 1}, @napr);
  gsap.set(["#cal .sheen", "#card .sheen", "#cTile .sheen"], {xPercent: -120});
  gsap.set(".sq8", {autoAlpha: 0});
  gsap.set(".crit", {autoAlpha: 0});
  gsap.set(".ck .f", {autoAlpha: 0, scale: 0.4, transformOrigin: "50% 50%"});
  gsap.set(".dd.mon i", {scale: 0, transformOrigin: "50% 50%"});
  gsap.set("#monBand", {scaleY: 0});
  // «Наприклад» — the iris opens out of the repeat ring
  tl.fromTo("#tk8", {clipPath: "circle(0px at 540px 300px)"},
            {clipPath: "circle(2300px at 540px 300px)", duration: 0.85, ease: "power3.inOut", immediateRender: false}, @napr);
  G.drift("#tk8", @napr, 8.4);

  // the month grows out of the hub point
  G.blurIn("#calWrap", @t_cal, 16, 0.45);
  tl.fromTo("#calWrap", {scale: 0.22}, {scale: 1, duration: 1.05, ease: spring(0.72, 12)}, @t_cal);
  tl.fromTo(["#calIc", "#calT", "#calS"], {autoAlpha: 0, y: 16}, {autoAlpha: 1, y: 0, duration: 0.6, ease: SP, stagger: 0.06}, @t_cal2);
  tl.fromTo("#calHair", {scaleX: 0}, {scaleX: 1, duration: 0.7, ease: "power3.out"}, @t_cal3);
  tl.fromTo("#calGrid .wd, #calGrid .dd", {autoAlpha: 0, y: 10}, {autoAlpha: 1, y: 0, duration: 0.4, ease: SP, stagger: 0.012}, @t_cal3);
  // «понеділок» — every Monday, top to bottom
  tl.to("#monBand", {scaleY: 1, duration: 0.55, ease: "power3.out"}, @t_mon);
  MONS.forEach(function (d, i) {
    tl.to("#ddi" + d, {scale: 1, duration: 0.5, ease: POP}, @t_mon2 + i * 0.09);
    tl.to("#dd" + d + " b", {color: "#ffffff", fontWeight: 700, duration: 0.15}, @t_mon2 + i * 0.09);
  });
  tl.to("#calGrid .dd:not(.mon)", {autoAlpha: 0.38, duration: 0.4}, @t_mon2);
  tl.to("#cal .sheen", {xPercent: 120, duration: 0.8, ease: "power2.inOut"}, @t_mon3);

  // the month shrinks into its chip
  tl.to("#calWrap", {scale: 0.14, y: -10, duration: 0.42, ease: "power3.in"}, @t_shr);
  G.blurOut("#calWrap", @t_shr2, 12, 0.26);
  G.blurIn("#pn", @t_pn, 10, 0.3);
  tl.fromTo("#pn", {scale: 0.4}, {scale: 1, duration: 0.8, ease: POP}, @t_pn);

  // «Claude збирає статистику з усіх джерел»
  G.arrive("#cTile", @t_ct, {s: 0.45, y: 40});
  tl.fromTo("#cTile .mk", {scale: 0.55, autoAlpha: 0}, {scale: 1, autoAlpha: 1, duration: 0.55, ease: SP}, @t_ct2);
  tl.fromTo("#cGlow", {autoAlpha: 0, scale: 0.7}, {autoAlpha: 0.8, scale: 1, duration: 0.5, ease: "power2.out"}, @t_ct2);
  [0, 1, 2, 3, 4].forEach(function (i) {
    var t = @zbyraye + i * 0.06;
    G.blurIn("#sq" + i, t, 12, 0.3);
    tl.fromTo("#sq" + i, {scale: 0.5, y: 40}, {scale: 1, y: 0, duration: 0.7, ease: POP}, t);
    var p = [[130, 1010], [335, 1062], [540, 1086], [745, 1062], [950, 1010]][i];
    var ti = @stat2 + i * 0.2;
    tl.to("#sq" + i, {x: 540 - p[0], y: 640 - p[1], scale: 0.3, duration: 0.42, ease: "power2.in"}, ti);
    tl.to("#sq" + i, {autoAlpha: 0, duration: 0.12}, ti + 0.34);
    G.bump("#cTile", ti + 0.4);
    tl.fromTo("#cGlow", {autoAlpha: 1}, {autoAlpha: 0.8, duration: 0.3, immediateRender: false}, ti + 0.4);
  });

  // «аналізує її за твоїми критеріями»
  tl.to("#cTile .sheen", {xPercent: 120, duration: 0.8, ease: "power2.inOut"}, @analizuye);
  G.ripple("#cr_r0", @analizuye);
  [0, 1, 2].forEach(function (i) {
    var t = @t_cr + i * 0.15;
    G.blurIn("#cr" + i, t, 10, 0.3);
    tl.fromTo("#cr" + i, {scale: 0.6, y: 30}, {scale: 1, y: 0, duration: 0.7, ease: POP}, t);
    var tk = [@tvoyimy, @t_ck2, @kryter][i];
    tl.to("#crf" + i, {autoAlpha: 1, scale: 1, duration: 0.4, ease: POP}, tk);
    G.draw("crk" + i, tk + 0.06, 0.3);
    G.bump("#cr" + i, tk);
  });
  G.ripple("#cr_r1", @kryter);

  // «видає тобі гарненько сформований звіт» — the report grows out of Claude
  tl.to(".crit", {x: function (i) { return [180, 0, -180][i]; }, y: -230, scale: 0.2, autoAlpha: 0,
                  duration: 0.34, ease: "power2.in", stagger: 0.03}, @t_rin);
  tl.to("#cGlow", {autoAlpha: 0, duration: 0.4}, @t_rin);
  G.blurIn("#cardWrap", @t_rep, 16, 0.45);
  tl.fromTo("#cardWrap", {scale: 0.22}, {scale: 1, duration: 1.05, ease: spring(0.72, 12)}, @t_rep);
  // the Claude tile flies up to become the report's icon, the chip its pill
  tl.to("#cTile", {x: -338, y: -304, scale: 0.35, duration: 0.7, ease: SP}, @t_rep);
  tl.to("#pn", {x: 270, y: 35, scale: 0.76, duration: 0.7, ease: SP}, @t_rep);
  tl.set(["#chIcon", "#chPill"], {autoAlpha: 1}, @t_land);
  tl.set(["#cTile", "#pn"], {autoAlpha: 0}, @t_land);
  tl.fromTo(["#chTitle", "#chSub"], {autoAlpha: 0, y: 16}, {autoAlpha: 1, y: 0, duration: 0.6, ease: SP, stagger: 0.06}, @t_rep2);
  tl.fromTo("#hair1", {scaleX: 0}, {scaleX: 1, duration: 0.7, ease: "power3.out"}, @t_rep3);
  tl.fromTo("#kLabel", {autoAlpha: 0, y: 12}, {autoAlpha: 1, y: 0, duration: 0.5, ease: SP}, @t_rep4);
  tl.fromTo("#kNum", {autoAlpha: 0, y: 26}, {autoAlpha: 1, y: 0, duration: 0.6, ease: SP}, @t_num);
  G.count("#kNum", @t_num2, 38, 1.1, function (v) { return "+" + Math.round(v) + "%"; });
  tl.fromTo("#kDelta", {autoAlpha: 0, scale: 0.6}, {autoAlpha: 1, scale: 1, duration: 0.6, ease: POP}, @t_delta);
  tl.fromTo(".gridl", {autoAlpha: 0}, {autoAlpha: 1, duration: 0.5, stagger: 0.08}, @t_rep5);
  var Ll = G.drawPrep("cLine");
  tl.to("#cLine", {strokeDashoffset: 0, duration: 0.95, ease: "power2.inOut"}, @t_ch);
  tl.fromTo("#cArea", {clipPath: "inset(0px 100% 0px 0px)"}, {clipPath: "inset(0px 0% 0px 0px)", duration: 0.95, ease: "power2.inOut"}, @t_ch);
  tl.fromTo("#days span", {autoAlpha: 0, y: 8}, {autoAlpha: 1, y: 0, duration: 0.4, stagger: 0.1, ease: SP}, @t_ch);
  tl.fromTo("#cDot", {scale: 0, transformOrigin: "50% 50%"}, {scale: 1, duration: 0.5, ease: POP}, @t_dot);
  tl.fromTo("#cRing", {scale: 1, autoAlpha: 0.6, transformOrigin: "50% 50%"}, {scale: 3, autoAlpha: 0, duration: 0.9, ease: "power2.out", immediateRender: false}, @t_dot2);
  tl.fromTo([".row", ".rowline"], {autoAlpha: 0, y: 22}, {autoAlpha: 1, y: 0, duration: 0.6, ease: SP, stagger: 0.07}, @t_rows);
  tl.to("#card .sheen", {xPercent: 120, duration: 0.55, ease: "power2.inOut"}, @t_sheen);

  // ============ «Тадааам» · the report folds into a notification ============
  tl.set("#cardWrap", {transformOrigin: "440px 34px"}, @t_fold0);
  tl.to("#cardWrap", {scale: 0.2, y: -6, duration: 0.5, ease: "power3.in"}, @t_fold);
  G.blurOut("#cardWrap", @t_fold2, 12, 0.28);
  tl.to("#tk8", {clipPath: "circle(0px at 540px 274px)", duration: 0.6, ease: "power3.inOut"}, @t_iris);
  tl.to("#g8", {autoAlpha: 0, duration: 0.02}, @t_off);'''.replace("MONS", mons),
             t_cal=T["napr"] + 0.10, t_cal2=T["napr"] + 0.42, t_cal3=T["napr"] + 0.52,
             t_mon=T["ponedilok"] - 0.06, t_mon2=T["ponedilok"] + 0.04, t_mon3=T["ponedilok"] + 0.45,
             t_shr=T["ponedilok_e"] - 0.02, t_shr2=T["ponedilok_e"] + 0.14,
             t_pn=T["ponedilok_e"] + 0.06,
             t_ct=T["claude2"] - 0.10, t_ct2=T["claude2"],
             t_cr=T["analizuye"] + 0.05, t_ck2=T["tvoyimy"] + 0.19,
             t_rin=T["vydaye"] - 0.20, t_rep=T["vydaye"] - 0.12,
             t_land=T["vydaye"] + 0.56, t_rep2=T["vydaye"] + 0.20,
             t_rep3=T["vydaye"] + 0.30, t_rep4=T["vydaye"] + 0.34, t_rep5=T["vydaye"] + 0.38,
             t_num=T["harnenko"] - 0.25, t_num2=T["harnenko"] - 0.20,
             t_delta=T["harnenko"] + 0.55,
             t_ch=T["sform"] - 0.30, t_dot=T["sform"] + 0.60, t_dot2=T["sform"] + 0.70,
             t_rows=T["sform"] + 0.10, t_sheen=T["zvit"] - 0.14,
             t_fold0=T["zvit_e"] - 0.06, t_fold=T["zvit_e"] - 0.04, t_fold2=T["zvit_e"] + 0.18,
             t_iris=T["zvit_e"] + 0.02, t_off=T["zvit_e"] + 0.64)
    return html, src


# =================================================================== b12
k.css("""
/* ---- b12 · the notification (style test §D) ---- */
#banner { left: 60px; top: 186px; width: 960px; height: 176px; }
#bIcon { left: 36px; top: 36px; width: 104px; height: 104px; }
#bTitle { left: 170px; top: 42px; font-size: 36px; font-weight: 700; letter-spacing: -0.01em; }
#bBody { left: 170px; top: 94px; font-size: 30px; font-weight: 400; color: rgba(255,255,255,0.80); }
#bTime { right: 44px; top: 48px; font-size: 26px; color: rgba(255,255,255,0.50); }
""")


@beat
def b12_notification():
    """«Тадааам! Автоматизація»

    The report folds into a Claude notification as the iris closes onto it;
    haptic shake on «дам». Her arm goes up through it — matte `tada` puts the
    arm in front."""
    html = u'''
      <div class="g full" id="g12">
        <div id="banner" class="dglass edge abs">
          <div class="cx" id="bIcon"><div class="jelly">%s</div></div>
          <div class="cx" id="bTitle">Claude</div>
          <div class="cx" id="bTime">зараз</div>
          <div class="cx" id="bBody">Тижневий звіт готовий · охоплення +38%%</div>
        </div>
      </div>''' % g.mark("claude")
    src = js('''
  tl.set("#g12", {autoAlpha: 1}, @t_in);
  G.blurIn("#banner", @t_in, 12, 0.3);
  tl.fromTo("#banner", {scale: 0.62, y: -26}, {scale: 1, y: 0, duration: 0.9, ease: POP}, @t_in);
  tl.fromTo(["#bIcon", "#bTitle", "#bTime", "#bBody"], {autoAlpha: 0, y: 10},
            {autoAlpha: 1, y: 0, duration: 0.5, ease: SP, stagger: 0.05}, @t_in2);
  G.haptic("#banner", @t_hap);
  // «Автоматизація» — it sits for the word, then goes
  tl.to("#banner", {y: -48, scale: 0.97, duration: 0.42, ease: "power2.in"}, @t_out);
  G.blurOut("#banner", @t_out2, 10, 0.34);
  tl.to("#g12", {autoAlpha: 0, duration: 0.02}, @t_off);''',
             t_in=T["zvit_e"] + 0.34, t_in2=T["zvit_e"] + 0.48, t_hap=S(u"Тадааам") + 0.48,
             t_out=T["avtomatyz_e"] + 0.02, t_out2=T["avtomatyz_e"] + 0.10,
             t_off=T["avtomatyz_e"] + 0.46)
    return html, src


# =================================================================== b13
k.css("""
/* ---- b13 · the comment composer ---- */
#cmBox { left: 70px; top: 372px; width: 940px; height: 128px; border-radius: 64px; }
#cmPost { left: 70px; top: 188px; width: 940px; height: 152px; border-radius: 64px; }
.cmav { width: 80px; height: 80px; border-radius: 50%; overflow: hidden;
  background: linear-gradient(160deg, #ffffff 0%, #f6e3e9 100%);
  box-shadow: inset 0 2px 1px #fff, 0 8px 18px -6px rgba(10,0,4,0.5); }
.cmav svg { width: 100%; height: 100%; fill: rgba(180,18,47,0.42); transform: translateY(8%); }
#cmAv { left: 24px; top: 24px; } #cpAv { left: 26px; top: 36px; }
#cmPh { left: 130px; top: 42px; font-size: 36px; font-weight: 500; color: rgba(255,255,255,0.58); }
#cmTyped { left: 130px; top: 26px; font-size: 64px; font-weight: 900; line-height: 76px; }
#cmCaret { left: 132px; top: 38px; width: 4px; height: 52px; border-radius: 2px; background: #ff9cbc; }
#cmSend { right: 40px; top: 44px; font-size: 32px; font-weight: 700; color: #ff9cbc; }
#cpUser { left: 128px; top: 28px; font-size: 32px; font-weight: 700; }
#cpUser span { font-weight: 500; color: rgba(255,255,255,0.55); margin-left: 12px; }
#cpTxt { left: 128px; top: 66px; font-size: 60px; font-weight: 900; line-height: 70px; }
#cpHeart { right: 44px; top: 34px; width: 60px; height: 60px; }
#cpHeart svg { position: absolute; inset: 0; width: 60px; height: 60px; }
#cpHeart .o { fill: none; stroke: rgba(255,255,255,0.8); stroke-width: 1.8; }
#cpHeart .fl { fill: url(#gHeart); }
#cpLiked { right: 128px; top: 44px; width: 48px; height: 48px; border-radius: 50%; overflow: hidden;
  box-shadow: 0 0 0 3px rgba(255,255,255,0.7); }
#cpLiked { background: url("assets/avatar.jpg") center / cover no-repeat; }
#cpLikedH { right: 118px; top: 78px; width: 26px; height: 26px; }
#cpLikedH svg { width: 100%; height: 100%; fill: #ff4f86; stroke: #fff; stroke-width: 2.4; }
#cpRip { right: 44px; top: 34px; width: 60px; height: 60px; border-radius: 50%;
  border: 3px solid rgba(255,140,180,0.9); }
""")


@beat
def b13_comment_plus():
    """«…то став + в коментарі і ми поспілкуємось»

    An Instagram comment composer above her head. «+» is typed on «плюс» —
    blackout, the box says it — posted on «в коментарі», and liked by her on
    «поспілкуємось» (the heart fills, her avatar lands beside it: IG's
    "liked by creator")."""
    html = u'''
      <div class="g full" id="g13">
        <div id="cmPost" class="dglass edge abs hide">
          <div class="cx cmav" id="cpAv">%(person)s</div>
          <div class="cx" id="cpUser">ти<span>щойно</span></div>
          <div class="cx" id="cpTxt">+</div>
          <div class="cx hide" id="cpRip"></div>
          <div class="cx hide" id="cpLiked"></div>
          <div class="cx hide" id="cpLikedH"><svg viewBox="0 0 24 24"><path d="%(heart)s"/></svg></div>
          <div class="cx" id="cpHeart"><svg viewBox="0 0 24 24"><path class="o" d="%(heart)s"/></svg>
            <svg viewBox="0 0 24 24" id="cpFill"><path class="fl" d="%(heart)s"/></svg></div>
        </div>
        <div id="cmBox" class="dglass edge abs">
          <div class="cx cmav" id="cmAv">%(person)s</div>
          <div class="cx" id="cmPh">Додайте коментар…</div>
          <div class="cx hide" id="cmTyped">+</div>
          <div class="cx hide" id="cmCaret"></div>
          <div class="cx" id="cmSend">Опублікувати</div>
        </div>
      </div>''' % {"person": PERSON, "heart": HEART}
    src = js('''
  tl.set("#g13", {autoAlpha: 1}, @t_in);
  gsap.set("#cpFill", {scale: 0, autoAlpha: 0, transformOrigin: "50% 60%"});
  gsap.set("#cmSend", {autoAlpha: 0.4});
  G.arrive("#cmBox", @t_in, {s: 0.7, y: 40});
  tl.fromTo("#cmAv", {scale: 0.55, autoAlpha: 0}, {scale: 1, autoAlpha: 1, duration: 0.55, ease: SP}, @t_in2);
  tl.fromTo("#cmPh", {autoAlpha: 0, x: -14}, {autoAlpha: 1, x: 0, duration: 0.5, ease: SP}, @t_in3);
  // «то став» — the cursor
  tl.set("#cmCaret", {autoAlpha: 1}, @stav);
  tl.set("#cmPh", {autoAlpha: 0}, @stav);
  // «+»
  tl.fromTo("#cmTyped", {autoAlpha: 0, scale: 0.4, transformOrigin: "20% 50%"},
            {autoAlpha: 1, scale: 1, duration: 0.3, ease: POP}, @plus);
  tl.to("#cmCaret", {x: 46, duration: 0.06}, @plus);
  tl.to("#cmSend", {autoAlpha: 1, duration: 0.12}, @plus);
  // «в коментарі» — sent; it posts above
  G.bump("#cmSend", @koment);
  tl.set(["#cmTyped", "#cmCaret"], {autoAlpha: 0}, @t_post);
  tl.set("#cmPh", {autoAlpha: 1}, @t_post);
  tl.to("#cmSend", {autoAlpha: 0.4, duration: 0.2}, @t_post);
  G.blurIn("#cmPost", @t_post, 10, 0.3);
  tl.fromTo("#cmPost", {y: 150, scale: 0.9}, {y: 0, scale: 1, duration: 0.8, ease: SP}, @t_post);
  tl.fromTo("#cpTxt", {scale: 0.6, transformOrigin: "0% 50%"}, {scale: 1, duration: 0.6, ease: POP}, @t_post2);
  // «поспілкуємось» — she likes it
  tl.to("#cpFill", {scale: 1, autoAlpha: 1, duration: 0.55, ease: POP}, @pospilk);
  tl.fromTo("#cpRip", {scale: 1, autoAlpha: 0.9}, {scale: 2.1, autoAlpha: 0, duration: 0.7, ease: "power2.out", immediateRender: false}, @pospilk);
  tl.fromTo("#cpLiked", {autoAlpha: 0, scale: 0.4}, {autoAlpha: 1, scale: 1, duration: 0.55, ease: POP}, @t_lk);
  tl.fromTo("#cpLikedH", {autoAlpha: 0, scale: 0.3}, {autoAlpha: 1, scale: 1, duration: 0.5, ease: POP}, @t_lk2);''',
             t_in=T["vorkflou"] - 0.12, t_in2=T["vorkflou"] - 0.02, t_in3=T["vorkflou"] + 0.12,
             t_post=T["koment"] + 0.16, t_post2=T["koment"] + 0.26,
             t_lk=T["pospilk"] + 0.16, t_lk2=T["pospilk"] + 0.28)
    return html, src


# ---------------------------------------------------------------------------
# Captions drop only on redundancy (STYLE.md §2b.1).
BLACKOUT = [
    (0.00, 6.86, "b01 — the post says every word she reads"),
    (7.40, 8.95, "b02 — the capsule says «Рута · технічна продюсерка»"),
    (42.55, 42.76, "b13 — the composer types «+» on «плюс»"),
]
INVERT = []

EXTRA_DEFS = (
    '<linearGradient id="gLine" x1="0" y1="0" x2="1" y2="0">'
    '<stop offset="0" stop-color="#8d0d24"/><stop offset="0.55" stop-color="#c8173a"/>'
    '<stop offset="1" stop-color="#ff6e9c"/></linearGradient>'
    '<linearGradient id="gArea" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#ff6e9c" stop-opacity="0.34"/>'
    '<stop offset="1" stop-color="#ff6e9c" stop-opacity="0"/></linearGradient>'
    '<linearGradient id="gHeart" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#ff6e9c"/><stop offset="1" stop-color="#c4143a"/></linearGradient>')


def main():
    gh, gj = [], []
    for fn in BEATS:
        h, j = fn()
        gh.append(h.rstrip())
        gj.append("  /* %s */" % fn.__name__)
        gj.append(j.rstrip())

    # the slow push on the plate (§0.8): her, her mattes and the soft room
    # move as one, so the cut-outs stay on their own pixels
    head = [g.js(), "  var G = helpers(tl);",
            '  gsap.set(["#vid", ".matte", "#soft"], {transformOrigin: "540px 820px"});',
            '  tl.fromTo(["#vid", ".matte", "#soft"], {scale: 1}, {scale: 1.045, duration: %.3f, '
            'ease: "none"}, 0);' % DUR]
    doc = k.document(
        title=u"Reel 12 — Бачила питання в Threads",
        plate="assets/base.mp4",
        gfx_html=g.defs(EXTRA_DEFS) + "\n" + "\n".join(gh),
        gfx_js="\n".join(head + gj),
        caps=CAPS,
        blackout=BLACKOUT,
        invert=INVERT,
    )
    # The reel opens inside a blackout, so the kit's opening scrim fade-in
    # would bring the empty plaque up under the post for the whole read.
    first = '  tl.to("#scrim", {autoAlpha: 1, duration: 0.5}, 0.000);\n'
    assert first in doc
    doc = doc.replace(first, "", 1)
    # The «+» blackout is one 0.2 s word mid-sentence: dropping the plaque for
    # it reads as a blink. The caption goes, the plaque stays.
    for line in ('  tl.to("#scrim", {autoAlpha: 0, duration: 0.20}, 42.350);\n',
                 '  tl.to("#scrim", {autoAlpha: 1, duration: 0.25}, 42.760);\n'):
        assert line in doc
        doc = doc.replace(line, "", 1)

    out = os.path.join(HERE, "index.html")
    io.open(out, "w", encoding="utf-8").write(doc)
    print("index.html  %d captions, %d beats, %.1f KB"
          % (len(CAPS), len(BEATS), os.path.getsize(out) / 1024.0))
    for key in ("pryvit", "avtomat", "naiprost", "windsor1", "claude", "chatgpt", "ig",
                "milyon", "danykh_e", "povtor", "shtuchn", "napr", "ponedilok", "claude2",
                "analizuye", "vydaye", "zvit_e", "tada", "vorkflou", "plus", "pospilk"):
        print("  %-11s %.2f" % (key, T[key]))


main()
