# -*- coding: utf-8 -*-
"""Nika's look as a library: the approved r01 look test, made reusable.

A reel's build.py does `sys.path.insert(0, "../tools"); from look import *`,
makes a `Reel(spans)` with the same spans its plate was cut with, adds beats, and
calls `reel.write(here, body, css)`.

- Text: pink Montserrat Black on torn grid-paper scraps (`scrap`, `Reel.captions`).
- Stage: UNLOCK's white → lavender ground, with the product as angled 3D cards in
  one perspective scene (`card`, `Reel.card_in/hold/out`, `Reel.stage_in/out`).
- UI pieces drawn in HTML in UNLOCK's own system: Geist, brand gradient
  #2D43D2 → #8F31EA, ink #0A0F1D, and the site's stroke icons (`icon`).
"""
import json
import math
import os
import random

FPS = 30
PINK, RIM, DEEP = "#F9B5CA", "#B4195B", "#93104A"
HERE = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------------- type + paper


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


CAP_SIZE = 64


def cap_size(text):
    est = len(text) * 0.66 * CAP_SIZE
    return CAP_SIZE if est <= 880 else int(CAP_SIZE * 880 / est)


# --------------------------------------------------------------------------- product pieces
UI = {   # display width (px) of each site capture, and its pixel size
    "products": (840, 1720, 1040), "editor": (720, 1280, 1008), "payments": (820, 1840, 1232),
    "salespage": (820, 1440, 744), "dashboard": (960, 4608, 1764), "phone": (330, 724, 1440),
    "toast-pay": (440, 768, 240),
}


def card(cid, name, extra=""):
    w, pw, ph = UI[name]
    h = round(w * ph / pw)
    return (f'<div class="card" id="{cid}" style="width:{w}px;height:{h}px">'
            f'<img src="assets/ui/{name}.png" style="width:{w}px;height:{h}px">{extra}</div>')


def html_card(cid, w, h, inner, cls=""):
    """A UI card drawn in HTML (UNLOCK's own system), living in the 3D scene."""
    return (f'<div class="card ui {cls}" id="{cid}" style="width:{w}px;height:{h}px">{inner}</div>')


def icon(name, size=40, color="#2D43D2", width=2):
    return (f'<svg class="ic" width="{size}" height="{size}" style="color:{color};stroke-width:{width}">'
            f'<use href="#{name}"/></svg>')


CURSOR = ('<svg viewBox="0 0 24 24" width="54" height="54"><path d="M5.5 3.2 19 11.1l-6.1 1.4-3.2 5.9z" '
          'fill="#0A0F1D" stroke="#fff" stroke-width="1.5" stroke-linejoin="round"/></svg>')


def cursor(cid, fx, fy):
    """A pointer whose tip sits at (fx, fy) of its card."""
    return (f'<div class="cur" id="{cid}" style="left:{fx * 100:.1f}%;top:{fy * 100:.1f}%">{CURSOR}</div>'
            f'<div class="rip" id="{cid}r" style="left:{fx * 100:.1f}%;top:{fy * 100:.1f}%"></div>')


LOCK = ('<svg viewBox="0 0 24 24" width="104" height="104" fill="none"><path d="M8 13a4 4 0 0 1 8 0v2" '
        'stroke="#FFF" stroke-width="2.2" stroke-linecap="round"/><rect x="6" y="12" width="12" height="8" '
        'rx="2" fill="#FFF"/><circle cx="12" cy="16" r="1.4" fill="#2D43D2"/></svg>')


def sprite():
    """The site's stroke-icon sprite (Nika/r01/assets/icons.svg, captured from the site)."""
    return open(os.path.join(os.path.dirname(HERE), "r01", "assets", "icons.svg"), encoding="utf-8").read()


# --------------------------------------------------------------------------- css
CSS = """
@font-face { font-family: "MS"; src: url("assets/fonts/Montserrat.ttf"); font-weight: 100 900; font-display: block; }
@font-face { font-family: "Geist"; src: url("assets/fonts/Geist.ttf"); font-weight: 100 900; font-display: block; }
* { margin: 0; padding: 0; box-sizing: border-box; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #000;
        -webkit-font-smoothing: antialiased; font-family: "Geist", sans-serif; color: #0A0F1D; }
#cam { position: absolute; inset: 0; transform-origin: 540px 600px; }
#vid { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }
.ic { fill: none; stroke: currentColor; stroke-linecap: round; stroke-linejoin: round; flex: none; }

/* ---- the stage: UNLOCK's own white + lavender, with a faint grid like her paper ---- */
#stage { position: absolute; inset: 0; display: none; overflow: hidden;
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
.card { position: absolute; left: 0; top: 0; transform-style: preserve-3d; visibility: hidden; display: none; }
/* anything not on screen is display:none, so it neither renders nor trips the layout check */
.card > img { position: absolute; left: 0; top: 0; display: block;
  filter: drop-shadow(0 46px 50px rgba(45,50,160,0.20)) drop-shadow(0 8px 14px rgba(10,15,29,0.10)); }
.ui { background: #FFFFFF; border-radius: 36px; border: 1.5px solid rgba(10,15,29,0.08);
  box-shadow: 0 50px 80px -30px rgba(45,50,160,0.32), 0 8px 18px rgba(10,15,29,0.08); }
.cur { position: absolute; width: 54px; height: 54px; margin: -7px 0 0 -12px; visibility: hidden;
  transform-origin: 12px 7px; filter: drop-shadow(0 4px 6px rgba(10,15,29,0.30)); }
.rip { position: absolute; width: 90px; height: 90px; margin: -45px 0 0 -45px; border-radius: 50%;
  border: 5px solid rgba(45,67,210,0.55); visibility: hidden; }

/* ---- the logo ---- */
.lockup { position: absolute; display: flex; align-items: center; gap: 30px; visibility: hidden; }
.mark { width: 168px; height: 168px; border-radius: 42px; display: flex; align-items: center;
  justify-content: center; background: linear-gradient(135deg, #2D43D2 0%, #8F31EA 100%);
  box-shadow: 0 34px 60px -16px rgba(63,88,232,0.55), inset 0 2px 0 rgba(255,255,255,0.25); }
.word { font: 700 150px/1 "Geist", sans-serif; letter-spacing: -0.045em; color: #0A0F1D; padding-bottom: 14px; }

/* ---- her text: pink type on a torn scrap of grid paper ---- */
.cap, .big { position: absolute; left: 540px; top: 1262px; visibility: hidden; }
.cap { display: none; }   /* out of the render tree except in its own moment: scraps carry blur + clip-path */
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

REST = "{x:0,y:0,z:0,rotationY:-21,rotationX:13,rotationZ:2,scale:1,autoAlpha:1}"
REST_POSE = dict(rotationY=-21, rotationX=13, rotationZ=2)


# --------------------------------------------------------------------------- the reel
class Reel:
    def __init__(self, spans, speed=1.0):
        """`spans` and `speed`: exactly as her plate was cut with plate.py. At speed 1.2 her
        take plays 1.2x faster (pitch kept); the animations keep their own pace."""
        self.spans, self.offs, self.speed = [], [], speed
        acc = 0
        for a, b in spans:
            fa, n = round(a * FPS), round((b - a) * FPS)
            self.spans.append((fa / FPS, (fa + n) / FPS))
            self.offs.append(acc / FPS)
            acc += n
        self.frames = round(acc / speed)
        self.dur = round(self.frames / FPS, 3)
        self.js, self.fx_list = [], []

    def T(self, src):
        """Source time (seconds into her take) -> reel time. Inside a cut, the next span's start."""
        for (a, b), o in zip(self.spans, self.offs):
            if src < a:
                return round(o / self.speed, 3)
            if src <= b:
                return round((o + src - a) / self.speed, 3)
        return self.dur

    def cuts(self):
        """Reel times where the plate jumps."""
        return [round(o / self.speed, 3) for o in self.offs[1:]]

    # -- plumbing
    def j(self, s):
        self.js.append(s)

    def fx(self, t, name, db=0):
        self.fx_list.append({"t": round(t, 3), "name": name, "db": db})

    # -- her
    def push(self, t0, t1, s0, s1):
        self.j(f'tl.fromTo("#cam",{{scale:{s0}}},{{scale:{s1},duration:{round(t1 - t0, 3)},'
               f'ease:"sine.inOut",immediateRender:false}},{t0});')

    # -- captions
    def captions(self, caps):
        """caps: [(text, src_start, src_end)]. Each scrap lands with a little tilt, then is replaced."""
        rng = random.Random(5)
        html = []
        for i, (text, s, e) in enumerate(caps):
            html.append(scrap(f"cap{i}", text, cap_size(text), 11 + i))
            rot = round(rng.uniform(-2.4, 2.4), 2)
            t0, t1 = self.T(s), self.T(e)
            self.j(f'tl.set("#cap{i}",{{display:"block"}},{t0});')
            self.j(f'tl.fromTo("#cap{i}",{{autoAlpha:0,scale:0.8,y:18,rotation:{rot - 5}}},'
                   f'{{autoAlpha:1,scale:1,y:0,rotation:{rot},duration:0.24,ease:"back.out(2.2)",'
                   f'immediateRender:false}},{t0});')
            self.j(f'tl.set("#cap{i}",{{autoAlpha:0,display:"none"}},{round(t1 - 0.01, 3)});')
        return "\n".join(html)

    # -- presence: display on for a beat, off outside it
    def show(self, sel, t, disp="block", alpha=False):
        """Back into the render tree. `alpha` also undoes an earlier hide() (containers like the stage)."""
        sel = json.dumps(sel)
        extra = ",autoAlpha:1" if alpha else ""
        self.j(f'tl.set({sel},{{display:"{disp}"{extra}}},{t});')

    def hide(self, sel, t):
        sel = json.dumps(sel)
        self.j(f'tl.set({sel},{{autoAlpha:0,display:"none"}},{t});')

    # -- stage
    def stage_in(self, t, sound=True):
        self.show("#stage", t, alpha=True)
        self.j(f'tl.fromTo("#stage",{{clipPath:"inset(46% 30% 46% 30% round 90px)"}},'
               f'{{clipPath:"inset(0% 0% 0% 0% round 0px)",duration:0.4,ease:"power3.inOut",'
               f'immediateRender:false}},{t});')
        if sound:
            self.fx(t - 0.05, "whoosh")

    def stage_out(self, t, hide=()):
        self.j(f'tl.to("#stage",{{clipPath:"inset(46% 30% 46% 30% round 90px)",duration:0.4,'
               f'ease:"power3.in"}},{t});')
        self.hide("#stage", round(t + 0.4, 3))
        if hide:
            self.hide(list(hide), round(t + 0.41, 3))
        self.fx(t - 0.03, "swish", -2)

    # -- cards in the 3D scene
    def card_in(self, cid, t, dur=0.62):
        self.show(f"#{cid}", t)
        self.j(f'tl.fromTo("#{cid}",{{x:860,y:40,z:-260,rotationY:-48,rotationX:12,rotationZ:4,scale:1,autoAlpha:0}},'
               f'Object.assign({REST},{{duration:{dur},ease:"expo.out",immediateRender:false}}),{t});')

    def card_hold(self, cid, t, until):
        self.j(f'tl.to("#{cid}",{{z:150,rotationY:-14,rotationX:10,duration:{round(until - t, 3)},'
               f'ease:"sine.inOut"}},{t});')

    def card_out(self, cid, t, dur=0.42):
        self.j(f'tl.to("#{cid}",{{x:-900,z:-240,rotationY:22,rotationZ:-3,autoAlpha:0,duration:{dur},'
               f'ease:"power2.in"}},{t});')

    def click(self, kid, t_arrive, t_click):
        self.j(f'tl.fromTo("#{kid}",{{autoAlpha:0,x:150,y:190}},{{autoAlpha:1,x:0,y:0,'
               f'duration:{round(t_click - t_arrive, 3)},ease:"power3.out",immediateRender:false}},{t_arrive});')
        self.j(f'tl.to("#{kid}",{{scale:0.82,duration:0.07,yoyo:true,repeat:1}},{t_click});')
        self.j(f'tl.fromTo("#{kid}r",{{autoAlpha:1,scale:0.2}},{{autoAlpha:0,scale:1.5,duration:0.45,'
               f'ease:"power2.out",immediateRender:false}},{t_click});')
        self.fx(t_click, "tap")

    def pop(self, sel, t, frm="{autoAlpha:0,scale:0.5}", to="{autoAlpha:1,scale:1}", dur=0.42,
            ease="back.out(2)", sound="pop", db=-3):
        self.j(f'tl.fromTo({sel},{frm},Object.assign({to},{{duration:{dur},ease:"{ease}",'
               f'immediateRender:false}}),{t});')
        if sound:
            self.fx(t, sound, db)

    # -- output
    def write(self, here, body, css="", title="Nika", window=None):
        """window=(start, length): render only that stretch of the reel (a quick test)."""
        script = "\n  ".join(self.js)
        w0, wd = window if window else (0, self.dur)
        main = (f'var w = gsap.timeline({{paused: true}});\n  w.add(tl.tweenFromTo({w0}, {round(w0 + wd, 3)}, {{ease: "none"}}));\n'
                f'  window.__timelines["main"] = w;' if window else 'window.__timelines["main"] = tl;')
        html = f"""<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<style>{CSS}{css}</style>
</head>
<body>
{sprite()}
<div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920"
     data-duration="{wd}" data-fps="{FPS}">
  <div id="cam"><video id="vid" src="assets/base.mp4" data-start="0" data-duration="{wd}"
       data-media-start="{w0}" muted playsinline></video></div>
{body}
  <audio id="vo" src="assets/base.mp4" data-start="0" data-duration="{wd}" data-media-start="{w0}"></audio>
</div>
<script>
window.__timelines = window.__timelines || {{}};
function build() {{
  var tl = gsap.timeline({{paused: true}});
  {script}
  {main}
}}
if (document.fonts && document.fonts.ready) document.fonts.ready.then(build); else build();
</script>
</body>
</html>
"""
        open(os.path.join(here, "index.html"), "w", encoding="utf-8").write(html)
        json.dump(sorted(self.fx_list, key=lambda c: c["t"]), open(os.path.join(here, "sfx.json"), "w"), indent=1)
        name = "nika-" + os.path.basename(os.path.abspath(here))
        json.dump({"id": name, "name": name}, open(os.path.join(here, "meta.json"), "w"))
        json.dump({"$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
                   "registry": "https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry",
                   "paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"},
                   "media": {"autoProxy": True}, "authoringSkill": "general-video"},
                  open(os.path.join(here, "hyperframes.json"), "w"), indent=2)
        v = "hyperframes@0.8.33"
        json.dump({"name": name, "private": True, "type": "module",
                   "scripts": {k: f"npx --yes {v} {k if k != 'dev' else 'preview'}" for k in ("dev", "check", "render")}},
                  open(os.path.join(here, "package.json"), "w"), indent=2)
        open(os.path.join(here, ".hyperframesignore"), "w").write(
            "renders/\nassets/voice.mp4\nbuild.py\nsfx.json\nPLAN.md\nscript.txt\n")
        print("DUR", self.dur, "frames", self.frames, "sfx", len(self.fx_list), "tweens", len(self.js))
