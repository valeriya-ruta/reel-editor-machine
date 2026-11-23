# -*- coding: utf-8 -*-
"""Nika r01, look test: source 15.40–34.83 s of IMG_7332.

    python build.py        # writes index.html + sfx.json (+ the HyperFrames project files)

Nika's look (Nika/README.md), not Ruta's: pink Montserrat Black on torn
grid-paper scraps for the text, and the real UNLOCK UI as angled 3D mockups on a
clean white-to-lavender stage, one smooth move per shot. index.html is
generated; edit this file.
"""
import json
import math
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
T0 = 15.40                 # source time of frame 0
FRAMES = 583               # assets/voice.mp4
DUR = round(FRAMES / 30, 3)


def T(src):
    """Source time (IMG_7332 seconds) -> composition time."""
    return round(src - T0, 3)


# --------------------------------------------------------------------------- type
PINK, RIM, DEEP = "#F9B5CA", "#B4195B", "#93104A"


def pink_shadow(r):
    """Raspberry outline (a ring of shadows) plus a short 3D drop."""
    ring = [f"{r * math.cos(a):.2f}px {r * math.sin(a):.2f}px 0 {RIM}"
            for a in (i * 2 * math.pi / 20 for i in range(20))]
    k = r / 3.4
    drop = [f"0 {4.5 * k:.1f}px 0 {RIM}", f"{0.6 * k:.1f}px {6.5 * k:.1f}px 0 {DEEP}",
            f"{0.8 * k:.1f}px {8 * k:.1f}px 0 {DEEP}"]
    return ", ".join(ring + drop)


def torn(seed):
    """A ripped notebook scrap: ragged top, softer sides and bottom."""
    r = random.Random(seed)
    pts, x = [], 0.0
    while x < 100:
        tear = r.random() < 0.12
        pts.append(f"{x:.1f}% {r.uniform(4, 11) if tear else r.uniform(0, 5):.1f}px")
        x += r.uniform(1.2, 3.4)
    pts.append(f"100% {r.uniform(0, 5):.1f}px")
    for y in (12, 32, 54, 76, 94):
        pts.append(f"calc(100% - {r.uniform(0, 4):.1f}px) {y}%")
    x = 100.0
    while x > 0:
        pts.append(f"{x:.1f}% calc(100% - {r.uniform(0, 3.5):.1f}px)")
        x -= r.uniform(2.5, 6)
    pts.append(f"0% calc(100% - {r.uniform(0, 3):.1f}px)")
    for y in (90, 68, 44, 22, 8):
        pts.append(f"{r.uniform(0, 4):.1f}px {y}%")
    return "polygon(" + ", ".join(pts) + ")"


def scrap(el_id, text, size, seed, cls="cap"):
    pad_x, pad_y = round(size * 0.42), round(size * 0.24)
    return (f'<div class="{cls}" id="{el_id}"><div class="pp" style="inset:-{pad_y}px -{pad_x}px">'
            f'<div class="fb" style="clip-path:{torn(seed * 7 + 1)}"></div>'
            f'<div class="gr" style="clip-path:{torn(seed * 7 + 2)}"></div></div>'
            f'<span class="tx" style="font-size:{size}px;text-shadow:{pink_shadow(size * 0.058)}">{text}</span></div>')


# --------------------------------------------------------------------------- captions
# (text, first word's source start, next caption's start or the hold end)
CAPS = [
    ("а тепер достатньо", 15.67, 17.02),
    ("лише двох речей", 17.02, 18.00),
    # 18.00–20.45: the stage says it — «твоя експертиза + unlock»
    ("мене звати Ніка", 20.56, 21.76),
    ("і я працюю над Unlock", 21.76, 23.08),
    ("над платформою,", 23.08, 23.88),
    ("де ти можеш", 23.88, 24.40),
    ("створювати", 24.40, 24.92),
    ("мінікурси,", 24.92, 25.66),
    ("приймати оплати", 25.66, 26.60),
    ("та продавати", 26.60, 27.30),
    ("свої знання", 27.30, 27.92),
    ("і все в одному місці", 27.92, 29.80),
    ("і зараз я хочу", 29.80, 30.98),
    ("особисто", 30.98, 31.70),
    ("познайомитися", 31.70, 32.60),
    ("з нашими першими", 32.60, 33.62),
    ("користувачами", 33.62, T0 + DUR),
]
CAP_SIZE = 64


def cap_size(text):
    est = len(text) * 0.66 * CAP_SIZE
    return CAP_SIZE if est <= 880 else int(CAP_SIZE * 880 / est)


# --------------------------------------------------------------------------- the product
# display width (px) of each UI capture, and its pixel size
UI = {
    "products": (840, 1720, 1040), "editor": (720, 1280, 1008), "payments": (820, 1840, 1232),
    "salespage": (820, 1440, 744), "dashboard": (960, 4608, 1764), "phone": (330, 724, 1440),
    "toast-pay": (440, 768, 240),
}


def card(cid, name, extra=""):
    w, pw, ph = UI[name]
    h = round(w * ph / pw)
    return (f'<div class="card" id="{cid}" style="width:{w}px;height:{h}px">'
            f'<img src="assets/ui/{name}.png" style="width:{w}px;height:{h}px">{extra}</div>')


CURSOR = ('<svg viewBox="0 0 24 24" width="54" height="54"><path d="M5.5 3.2 19 11.1l-6.1 1.4-3.2 5.9z" '
          'fill="#0A0F1D" stroke="#fff" stroke-width="1.5" stroke-linejoin="round"/></svg>')


def cursor(cid, fx, fy):
    """A pointer whose tip sits at (fx, fy) of its card."""
    return (f'<div class="cur" id="{cid}" style="left:{fx * 100:.1f}%;top:{fy * 100:.1f}%">{CURSOR}</div>'
            f'<div class="rip" id="{cid}r" style="left:{fx * 100:.1f}%;top:{fy * 100:.1f}%"></div>')


LOCK = ('<svg viewBox="0 0 24 24" width="104" height="104" fill="none"><path d="M8 13a4 4 0 0 1 8 0v2" '
        'stroke="#FFF" stroke-width="2.2" stroke-linecap="round"/><rect x="6" y="12" width="12" height="8" '
        'rx="2" fill="#FFF"/><circle cx="12" cy="16" r="1.4" fill="#2D43D2"/></svg>')

# --------------------------------------------------------------------------- html
CSS = """
@font-face { font-family: "MS"; src: url("assets/fonts/Montserrat.ttf"); font-weight: 100 900; font-display: block; }
@font-face { font-family: "Geist"; src: url("assets/fonts/Geist.ttf"); font-weight: 100 900; font-display: block; }
* { margin: 0; padding: 0; box-sizing: border-box; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #000;
        -webkit-font-smoothing: antialiased; }
#cam { position: absolute; inset: 0; transform-origin: 540px 600px; }
#vid { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }

/* ---- the stage: UNLOCK's own white + lavender, with a faint grid like her paper ---- */
#stage { position: absolute; inset: 0; visibility: hidden; overflow: hidden;
  background: linear-gradient(180deg, #FFFFFF 0%, #F5F4FF 55%, #EFEBFF 100%); }
.blob { position: absolute; border-radius: 50%; }
#bl1 { left: 420px; top: -380px; width: 1100px; height: 1100px;
  background: radial-gradient(closest-side, rgba(143,49,234,0.20), rgba(143,49,234,0) 100%); }
#bl2 { left: -520px; top: 1000px; width: 1200px; height: 1200px;
  background: radial-gradient(closest-side, rgba(63,88,232,0.17), rgba(63,88,232,0) 100%); }
#gridbg { position: absolute; inset: -80px;
  background-image: linear-gradient(rgba(45,67,210,0.06) 2px, transparent 2px),
                    linear-gradient(90deg, rgba(45,67,210,0.06) 2px, transparent 2px);
  background-size: 72px 72px;
  -webkit-mask-image: radial-gradient(ellipse 70% 60% at 50% 42%, #000 30%, transparent 100%);
          mask-image: radial-gradient(ellipse 70% 60% at 50% 42%, #000 30%, transparent 100%); }
#scene { position: absolute; left: 540px; top: 770px; width: 0; height: 0; perspective: 2300px; }
#world { position: absolute; left: 0; top: 0; transform-style: preserve-3d; }
.card { position: absolute; left: 0; top: 0; transform-style: preserve-3d; visibility: hidden; }
.card img { position: absolute; left: 0; top: 0; display: block;
  filter: drop-shadow(0 46px 50px rgba(45,50,160,0.20)) drop-shadow(0 8px 14px rgba(10,15,29,0.10)); }
.cur { position: absolute; width: 54px; height: 54px; margin: -7px 0 0 -12px; visibility: hidden;
  transform-origin: 12px 7px; filter: drop-shadow(0 4px 6px rgba(10,15,29,0.30)); }
.rip { position: absolute; width: 90px; height: 90px; margin: -45px 0 0 -45px; border-radius: 50%;
  border: 5px solid rgba(45,67,210,0.55); visibility: hidden; }

/* ---- stage B: «твоя експертиза + unlock» ---- */
#plus { position: absolute; left: 540px; top: 905px; visibility: hidden;
  font: 900 120px/1 "MS", sans-serif; color: #F9B5CA; }
#lock { position: absolute; left: 540px; top: 1085px; display: flex; align-items: center; gap: 30px;
  visibility: hidden; }
#mark { width: 168px; height: 168px; border-radius: 42px; display: flex; align-items: center;
  justify-content: center; background: linear-gradient(135deg, #2D43D2 0%, #8F31EA 100%);
  box-shadow: 0 34px 60px -16px rgba(63,88,232,0.55), inset 0 2px 0 rgba(255,255,255,0.25); }
#word { font: 700 150px/1 "Geist", sans-serif; letter-spacing: -0.045em; color: #0A0F1D;
  padding-bottom: 14px; }

/* ---- her text: pink type on a torn scrap of grid paper ---- */
.cap, .big { position: absolute; left: 540px; top: 1262px; visibility: hidden; }
.big { top: 715px; }
.pp { position: absolute; filter: drop-shadow(0 8px 10px rgba(70,20,50,0.22)); }
.fb { position: absolute; inset: -5px; background: #FFFFFF; filter: blur(1.4px); }
.gr { position: absolute; inset: 0; background-color: #FDFDFD;
  background-image: linear-gradient(rgba(140,160,190,0.50) 1.5px, transparent 1.5px),
                    linear-gradient(90deg, rgba(140,160,190,0.50) 1.5px, transparent 1.5px);
  background-size: 23px 23px; background-position: 7px 5px; }
.tx { position: relative; display: block; white-space: nowrap; font-family: "MS", sans-serif;
  font-weight: 900; line-height: 1.05; letter-spacing: 0.005em; color: """ + PINK + """; }
"""


def html_body():
    caps = "\n".join(scrap(f"cap{i}", t, cap_size(t), 11 + i) for i, (t, *_rest) in enumerate(CAPS))
    stage = f"""
  <div id="stage">
    <div class="blob" id="bl1"></div><div class="blob" id="bl2"></div><div id="gridbg"></div>
    {scrap("bExp", "твоя експертиза", 86, 3, cls="big")}
    <div id="plus" style="text-shadow:{pink_shadow(6)}">+</div>
    <div id="lock"><div id="mark">{LOCK}</div><div id="word">unlock</div></div>
    <div id="scene"><div id="world">
      {card("cP", "products", cursor("k1", 0.874, 0.232))}
      {card("cE", "editor")}
      {card("cPay", "payments")}
      {card("tPay", "toast-pay")}
      {card("cS", "salespage", cursor("k2", 0.83, 0.83))}
      {card("cD", "dashboard")}
      {card("cPh", "phone")}
    </div></div>
  </div>"""
    return f"""<div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920"
     data-duration="{DUR}" data-fps="30">
  <div id="cam"><video id="vid" src="assets/base.mp4" data-start="0" data-duration="{DUR}"
       data-media-start="0" muted playsinline></video></div>
{stage}
  <div id="caps">
{caps}
  </div>
  <audio id="vo" src="assets/base.mp4" data-start="0" data-duration="{DUR}" data-media-start="0"></audio>
</div>"""


# --------------------------------------------------------------------------- motion
JS, SFX = [], []


def js(s):
    JS.append(s)


def sfx(t, name, db=0):
    SFX.append({"t": round(t, 3), "name": name, "db": db})


REST = "{x:0,y:0,z:0,rotationY:-21,rotationX:13,rotationZ:2,scale:1,autoAlpha:1}"


def card_in(cid, t, dur=0.62):
    js(f'tl.fromTo("#{cid}",{{x:860,y:40,z:-260,rotationY:-48,rotationX:12,rotationZ:4,scale:1,autoAlpha:0}},'
       f'Object.assign({REST},{{duration:{dur},ease:"expo.out"}}),{t});')


def card_hold(cid, t, until):
    """The slow push while a card is the shot."""
    js(f'tl.to("#{cid}",{{z:150,rotationY:-14,rotationX:10,duration:{round(until - t, 3)},ease:"sine.inOut"}},{t});')


def card_out(cid, t, dur=0.42):
    js(f'tl.to("#{cid}",{{x:-900,z:-240,rotationY:22,rotationZ:-3,autoAlpha:0,duration:{dur},'
       f'ease:"power2.in"}},{t});')


def stage_in(t):
    js(f'tl.set("#stage",{{visibility:"visible"}},{t});')
    js(f'tl.fromTo("#stage",{{clipPath:"inset(46% 30% 46% 30% round 90px)"}},'
       f'{{clipPath:"inset(0% 0% 0% 0% round 0px)",duration:0.4,ease:"power3.inOut"}},{t});')
    sfx(t - 0.05, "whoosh")


def stage_out(t):
    js(f'tl.to("#stage",{{clipPath:"inset(46% 30% 46% 30% round 90px)",duration:0.4,ease:"power3.in"}},{t});')
    js(f'tl.set("#stage",{{visibility:"hidden"}},{round(t + 0.4, 3)});')
    sfx(t - 0.03, "swish", -2)


def click(kid, t_arrive, t_click):
    js(f'tl.fromTo("#{kid}",{{autoAlpha:0,x:150,y:190}},{{autoAlpha:1,x:0,y:0,'
       f'duration:{round(t_click - t_arrive, 3)},ease:"power3.out"}},{t_arrive});')
    js(f'tl.to("#{kid}",{{scale:0.82,duration:0.07,yoyo:true,repeat:1}},{t_click});')
    js(f'tl.fromTo("#{kid}r",{{autoAlpha:1,scale:0.2}},{{autoAlpha:0,scale:1.5,duration:0.45,'
       f'ease:"power2.out"}},{t_click});')
    sfx(t_click, "tap")


def build_motion():
    js('gsap.set([".cap",".big","#plus","#lock"],{xPercent:-50,yPercent:-50});')
    js('gsap.set(".card",{xPercent:-50,yPercent:-50});')
    js('gsap.set(["#bl1","#bl2"],{x:0,y:0});')
    js(f'tl.to("#bl1",{{x:-160,y:120,duration:{DUR},ease:"none"}},0);')
    js(f'tl.to("#bl2",{{x:140,y:-140,duration:{DUR},ease:"none"}},0);')

    # her: a slow push-in on each of her shots, a new framing after every product shot
    a, b, c = T(18.00), T(20.45), T(29.80)
    js(f'tl.fromTo("#cam",{{scale:1.0}},{{scale:1.035,duration:{a},ease:"sine.inOut"}},0);')
    js(f'tl.fromTo("#cam",{{scale:1.06}},{{scale:1.10,duration:{round(T(23.0) - b, 3)},ease:"sine.inOut"}},{b});')
    js(f'tl.fromTo("#cam",{{scale:1.0}},{{scale:1.045,duration:{round(DUR - T(29.80), 3)},'
       f'ease:"sine.inOut"}},{T(29.80)});')

    # captions: each scrap lands with a little tilt, and is replaced, not faded
    rng = random.Random(5)
    for i, (text, s, e) in enumerate(CAPS):
        rot = round(rng.uniform(-2.4, 2.4), 2)
        js(f'tl.fromTo("#cap{i}",{{autoAlpha:0,scale:0.8,y:18,rotation:{rot - 5}}},'
           f'{{autoAlpha:1,scale:1,y:0,rotation:{rot},duration:0.24,ease:"back.out(2.2)"}},{T(s)});')
        js(f'tl.set("#cap{i}",{{autoAlpha:0}},{T(e) - 0.01});')
    sfx(T(15.67), "click")
    sfx(T(20.56), "click")

    # ---- stage B, 18.00–20.45: «твоєї експертизи та Unlock»
    stage_in(a)
    js(f'tl.fromTo("#bExp",{{autoAlpha:0,scale:0.6,rotation:-12}},{{autoAlpha:1,scale:1,rotation:-3,'
       f'duration:0.5,ease:"back.out(1.9)"}},{T(18.30)});')
    sfx(T(18.30), "pop")
    js(f'tl.fromTo("#plus",{{autoAlpha:0,scale:0.3,rotation:-90}},{{autoAlpha:1,scale:1,rotation:0,'
       f'duration:0.4,ease:"back.out(2.5)"}},{T(19.24)});')
    sfx(T(19.24), "pop", -5)
    js(f'tl.set("#lock",{{autoAlpha:1}},{T(19.40)});')
    js(f'tl.fromTo("#mark",{{scale:0,rotation:-25}},{{scale:1,rotation:0,duration:0.55,'
       f'ease:"back.out(2)"}},{T(19.40)});')
    js(f'tl.fromTo("#word",{{autoAlpha:0,x:-50,clipPath:"inset(0 100% 0 0)"}},{{autoAlpha:1,x:0,'
       f'clipPath:"inset(0 0% 0 0)",duration:0.5,ease:"power3.out"}},{T(19.55)});')
    sfx(T(19.40), "pop", -2)
    sfx(T(19.50), "sparkle")
    js(f'tl.to(["#bExp","#plus","#lock"],{{y:"-=26",duration:{round(b - T(18.06), 3)},ease:"sine.inOut"}},{T(18.06)});')
    stage_out(b)
    js(f'tl.set(["#bExp","#plus","#lock"],{{autoAlpha:0}},{round(b + 0.41, 3)});')

    # ---- stage D, 23.00–29.80: the platform, one screen per thing she names
    d = T(23.00)
    stage_in(d)
    # «над платформою, де ти можеш створювати» — home, and a click on «+ Створити»
    card_in("cP", T(23.06))
    card_hold("cP", T(23.68), T(24.80))
    click("k1", T(23.90), T(24.36))
    card_out("cP", T(24.80))
    sfx(T(24.80), "swish")
    # «мінікурси» — the course editor
    card_in("cE", T(24.86))
    card_hold("cE", T(25.48), T(25.58))
    card_out("cE", T(25.58))
    sfx(T(25.58), "swish")
    # «приймати оплати» — payments, and the money lands
    card_in("cPay", T(25.64))
    card_hold("cPay", T(26.26), T(26.52))
    js(f'tl.fromTo("#tPay",{{autoAlpha:0,x:240,y:-330,z:160,scale:0.7,rotationY:-21,rotationX:13,rotationZ:2}},'
       f'{{autoAlpha:1,x:220,y:-300,z:200,scale:1,duration:0.45,ease:"back.out(2)"}},{T(26.06)});')
    sfx(T(26.06), "kaching")
    card_out("cPay", T(26.52))
    js(f'tl.to("#tPay",{{x:-700,y:-380,z:0,autoAlpha:0,duration:0.42,ease:"power2.in"}},{T(26.52)});')
    sfx(T(26.52), "swish")
    # «та продавати свої знання» — the sales page, and someone buys
    card_in("cS", T(26.58))
    card_hold("cS", T(27.20), T(27.90))
    click("k2", T(27.10), T(27.52))
    # «і все в одному місці» — everything at once, and the camera pulls back
    e = T(27.90)
    sfx(e - 0.04, "whoosh", -3)
    js(f'tl.to("#k2",{{autoAlpha:0,duration:0.15}},{e});')
    js(f'tl.to("#cS",{{x:-275,y:215,z:140,rotationY:-18,rotationX:12,rotationZ:2,scale:0.6,duration:0.75,'
       f'ease:"power3.inOut"}},{e});')
    js(f'tl.fromTo("#cD",{{autoAlpha:0,x:0,y:-90,z:-700,rotationY:-21,rotationX:13,rotationZ:2}},'
       f'{{autoAlpha:1,z:-60,duration:0.8,ease:"expo.out"}},{round(e + 0.05, 3)});')
    js(f'tl.fromTo("#cP",{{autoAlpha:0,x:-560,y:-460,z:-200,rotationY:-34,rotationX:13,rotationZ:2,scale:0.55}},'
       f'{{autoAlpha:1,x:-240,y:-440,z:60,rotationY:-21,duration:0.75,ease:"expo.out"}},{round(e + 0.15, 3)});')
    js(f'tl.fromTo("#cPh",{{autoAlpha:0,x:620,y:120,z:-100,rotationY:-34,rotationX:13,rotationZ:2,scale:1}},'
       f'{{autoAlpha:1,x:330,y:40,z:200,rotationY:-18,duration:0.75,ease:"expo.out"}},{round(e + 0.22, 3)});')
    js(f'tl.fromTo("#tPay",{{autoAlpha:0,x:560,y:-470,z:120,rotationY:-21,rotationX:13,rotationZ:2,scale:0.8}},'
       f'{{autoAlpha:1,x:270,y:-430,z:240,scale:0.9,duration:0.6,ease:"back.out(1.8)"}},{round(e + 0.35, 3)});')
    sfx(e + 0.35, "pop", -6)
    js(f'tl.fromTo("#world",{{scale:1.1,y:0}},{{scale:0.94,y:-70,duration:{round(T(29.80) - e, 3)},'
       f'ease:"sine.inOut"}},{e});')
    js(f'tl.fromTo("#world",{{rotationY:0}},{{rotationY:-5,duration:{round(T(29.80) - e, 3)},'
       f'ease:"sine.inOut"}},{e});')
    stage_out(c)


# --------------------------------------------------------------------------- write
def main():
    build_motion()
    script = "\n  ".join(JS)
    html = f"""<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="utf-8">
<title>Nika r01 — look test</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<style>{CSS}</style>
</head>
<body>
{html_body()}
<script>
window.__timelines = window.__timelines || {{}};
function build() {{
  var tl = gsap.timeline({{paused: true}});
  {script}
  window.__timelines["main"] = tl;
}}
if (document.fonts && document.fonts.ready) document.fonts.ready.then(build); else build();
</script>
</body>
</html>
"""
    open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(html)
    json.dump(sorted(SFX, key=lambda c: c["t"]), open(os.path.join(HERE, "sfx.json"), "w"), indent=1)
    name = "nika-r01-test"
    json.dump({"id": name, "name": name}, open(os.path.join(HERE, "meta.json"), "w"))
    json.dump({"$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
               "registry": "https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry",
               "paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"},
               "media": {"autoProxy": True}, "authoringSkill": "general-video"},
              open(os.path.join(HERE, "hyperframes.json"), "w"), indent=2)
    v = "hyperframes@0.8.33"
    json.dump({"name": name, "private": True, "type": "module",
               "scripts": {k: f"npx --yes {v} {k if k != 'dev' else 'preview'}" for k in ("dev", "check", "render")}},
              open(os.path.join(HERE, "package.json"), "w"), indent=2)
    open(os.path.join(HERE, ".hyperframesignore"), "w").write(
        "renders/\nassets/voice.mp4\nbuild.py\nsfx.json\n")
    print("DUR", DUR, "captions", len(CAPS), "sfx", len(SFX), "tweens", len(JS))


if __name__ == "__main__":
    main()
