# -*- coding: utf-8 -*-
"""Style test — "refined glass". A ~16 s slice of the 2026-09-28 script
(«Бачила питання в Threads»), acted over a still of her, to show one visual
language across the three placements: near her, behind her, over her.

    python build.py            -> index.html + captions.json

No audio: word timings are synthesised from syllable counts so the captions
and every beat land where a real read would put them.
"""
import io
import json
import math
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1080, 1920, 30

# --- 1. the words ------------------------------------------------------------
SEGMENTS = [
    "Через Windsor, підключений до Claude або ChatGPT.",
    "У Windsor можна підключити Інстаграм, Фейсбук, таргет, ТікТок, "
    "статистику сайту і ще мільйон інших джерел даних,",
    # jump cut in her edit
    "і видає тобі гарненько сформований звіт.",
    "Тадааам!",
]
VOW = set(u"аеєиіїоуюяАЕЄИІЇОУЮЯ")
SPECIAL = {"Windsor": 2, "Claude": 1, "ChatGPT": 4}


def syl(w):
    core = w.strip(",.!?")
    if core in SPECIAL:
        return SPECIAL[core]
    return max(1, sum(ch in VOW for ch in core))


def timings():
    out, t = [], 0.30
    for si, seg in enumerate(SEGMENTS):
        if si == 2:
            t += 0.30                      # the cut
        for w in seg.split():
            d = 0.95 if w.startswith(u"Тада") else 0.07 + 0.152 * syl(w)
            out.append({"w": w, "s": round(t, 3), "e": round(t + d, 3)})
            t += d
            t += {",": 0.14, ".": 0.38, "!": 0.35}.get(w[-1], 0.03)
    for a, b in zip(out, out[1:]):
        a["e"] = round(min(a["e"] + 0.08, b["s"] - 0.085), 3)
    return out


WORDS = timings()
DUR = math.floor(math.floor((WORDS[-1]["e"] + 1.05) * FPS) / FPS * 1000) / 1000.0


def at(word, n=1):
    """start/end of the n-th occurrence of a word (punctuation ignored)."""
    k = 0
    for x in WORDS:
        if x["w"].strip(",.!?") == word:
            k += 1
            if k == n:
                return x
    raise KeyError(word)


T = {
    "cherez": at(u"Через")["s"], "windsor1": at("Windsor")["s"],
    "pidkl": at(u"підключений")["s"], "claude": at("Claude")["s"],
    "abo": at(u"або")["s"], "chatgpt": at("ChatGPT")["s"],
    "chatgpt_e": at("ChatGPT")["e"],
    "u": at(u"У")["s"], "windsor2": at("Windsor", 2)["s"],
    "ig": at(u"Інстаграм")["s"], "fb": at(u"Фейсбук")["s"],
    "target": at(u"таргет")["s"], "tiktok": at(u"ТікТок")["s"],
    "stat": at(u"статистику")["s"], "milyon": at(u"мільйон")["s"],
    "danykh_e": at(u"даних")["e"], "i2": at(u"і", 2)["s"],
    "vydaie": at(u"видає")["s"], "harnenko": at(u"гарненько")["s"],
    "sform": at(u"сформований")["s"], "zvit": at(u"звіт")["s"],
    "tada": at(u"Тадааам")["s"], "dur": DUR,
}

# --- 2. marks ------------------------------------------------------------------
ICON_DIR = os.path.join(HERE, "assets", "icons")


def icon_path(name):
    svg = io.open(os.path.join(ICON_DIR, name + ".svg"), encoding="utf-8").read()
    return re.search(r'<path d="([^"]+)"', svg).group(1)


ICONS = sorted(f[:-4] for f in os.listdir(ICON_DIR) if f.endswith(".svg"))
SYMBOLS = "\n".join(
    '<symbol id="i-%s" viewBox="0 0 24 24"><path d="%s"/></symbol>'
    % (n, icon_path(n)) for n in ICONS)


def glyph(name, cls="gl"):
    return ('<svg class="%s"><use href="#i-%s" width="100%%" height="100%%"/></svg>'
            % (cls, name))


# --- 3. geometry ---------------------------------------------------------------
HUB = (540, 300)
HERO = [  # key, icon, centre, anchor word
    ("ig", "instagram", (185, 560)),
    ("fb", "facebook", (895, 560)),
    ("target", "meta", (150, 836)),
    ("tiktok", "tiktok", (930, 836)),
    ("stat", "googleanalytics", (196, 1112)),
]
PITCH, CELL = 124, 100
cells = []
for j in range(-2, 14):
    for i in range(-4, 5):
        cells.append((HUB[0] + i * PITCH, HUB[1] + j * PITCH))


def nearest(p):
    return min(cells, key=lambda c: (c[0] - p[0]) ** 2 + (c[1] - p[1]) ** 2)


hero_cells = {k: nearest(c) for k, _, c in HERO}
FILL = [n for n in ICONS if n not in
        ("instagram", "facebook", "meta", "tiktok", "googleanalytics")]
wall = []
for idx, (x, y) in enumerate(cells):
    d = math.hypot(x - HUB[0], y - HUB[1])
    if d < 160 or (x, y) in hero_cells.values():
        continue
    i, j = (x - HUB[0]) // PITCH + 4, (y - HUB[1]) // PITCH + 2
    wall.append({"x": x, "y": y, "d": round(d, 1),
                 "o": round(max(0.40, 1 - d / 2300.0), 3),
                 "g": FILL[(i * 7 + j * 5 + i * j) % len(FILL)]})
MAXD = max(t["d"] for t in wall)


def wire(p):
    """a cable from a source tile up to the hub, bowed away from her head."""
    x0, y0 = p
    x1, y1 = HUB
    side = -1 if x0 < 540 else 1
    cx, cy = (x0 + x1) / 2 + side * 150, (y0 + y1) / 2 - 40
    return "M %d %d Q %d %d %d %d" % (x0, y0, cx, cy, x1, y1 + 60)


# the chart on the report card — seven days, smoothed with Catmull-Rom
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

# --- 4. document ---------------------------------------------------------------
CSS = u"""
@font-face { font-family: "PS"; src: url("assets/fonts/ProductSans-Regular.ttf"); font-weight: 400; font-display: block; }
@font-face { font-family: "PS"; src: url("assets/fonts/ProductSans-Medium.ttf"); font-weight: 500; font-display: block; }
@font-face { font-family: "PS"; src: url("assets/fonts/ProductSans-Bold.ttf"); font-weight: 700; font-display: block; }
@font-face { font-family: "PS"; src: url("assets/fonts/ProductSans-Black.woff") format("woff"); font-weight: 900; font-display: block; }
* { margin: 0; padding: 0; box-sizing: border-box; }
#root { position: relative; width: 1080px; height: 1920px; overflow: hidden;
        background: #000; font-family: "PS", system-ui, sans-serif; color: #17141c;
        -webkit-font-smoothing: antialiased; }
.abs { position: absolute; }
.hide { opacity: 0; visibility: hidden; }

/* ---- the camera: plate, the room gone soft, what sits behind her, her ---- */
#cam { position: absolute; inset: 0; transform-origin: 540px 820px; }
#plate, #roomSoft, #her { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }
#roomTint { position: absolute; inset: 0;
  background: linear-gradient(180deg, rgba(62,8,24,0.12) 0%, rgba(40,5,15,0.26) 100%); }
#behind, #wall { position: absolute; inset: 0; }
#wall { transform-origin: 540px 300px; }
#wires { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: visible; }
#wires .w { fill: none; stroke: rgba(255,255,255,0.55); stroke-width: 4; stroke-linecap: round; }
#wires .p { fill: none; stroke: #fff; stroke-width: 9; stroke-linecap: round; }
#wires .pk { filter: drop-shadow(0 0 8px rgba(255,150,185,0.95)); }

/* ---- material 1: clear glass (a tile sitting in the soft room) ---- */
.edge::before { content: ""; position: absolute; inset: 0; border-radius: inherit; padding: 1.6px;
  background: linear-gradient(140deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.34) 16%,
              rgba(255,255,255,0.05) 42%, rgba(255,255,255,0.07) 62%,
              rgba(255,255,255,0.50) 86%, rgba(255,255,255,0.90) 100%);
  -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
  -webkit-mask-composite: xor; mask-composite: exclude; pointer-events: none; }
.clear { position: absolute; inset: 0; border-radius: 22.4%;
  background: linear-gradient(158deg, rgba(255,255,255,0.36) 0%, rgba(255,255,255,0.11) 48%,
              rgba(255,255,255,0.17) 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.70),
              inset 0 -18px 30px -14px rgba(255,255,255,0.42),
              0 34px 60px -22px rgba(24,4,12,0.55), 0 3px 8px rgba(24,4,12,0.10);
  display: flex; align-items: center; justify-content: center; }
.src { position: absolute; width: 168px; height: 168px; margin: -84px 0 0 -84px; }
.src .gl { width: 84px; height: 84px; fill: url(#gw); }
.wt { position: absolute; width: 100px; height: 100px; margin: -50px 0 0 -50px; border-radius: 23px;
  background: linear-gradient(158deg, rgba(255,255,255,0.30) 0%, rgba(255,255,255,0.09) 52%,
              rgba(255,255,255,0.15) 100%);
  box-shadow: inset 0 1.5px 1px rgba(255,255,255,0.65), inset 0 -10px 18px -10px rgba(255,255,255,0.36),
              inset 0 0 0 1px rgba(255,255,255,0.10), 0 16px 30px -14px rgba(24,4,12,0.45);
  display: flex; align-items: center; justify-content: center; }
.wt svg { width: 46px; height: 46px; fill: #fff; opacity: 0.92; }

/* ---- material 2: the glass shelf over footage ---- */
#dock { left: 70px; top: 235px; width: 940px; height: 300px; border-radius: 80px;
  background: linear-gradient(158deg, rgba(255,255,255,0.24) 0%, rgba(255,255,255,0.07) 50%,
              rgba(255,255,255,0.13) 100%);
  -webkit-backdrop-filter: blur(22px) saturate(1.7) brightness(1.05);
  backdrop-filter: blur(22px) saturate(1.7) brightness(1.05);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.65), inset 0 -24px 44px -22px rgba(255,255,255,0.36),
              0 44px 90px -34px rgba(24,4,12,0.5); }

/* ---- material 3: pearl (the hub) and jelly (the AI) ---- */
.pearl { position: absolute; inset: 0; border-radius: 22.4%; overflow: hidden;
  background: linear-gradient(160deg, #ffffff 0%, #fff5f8 52%, #f5dfe6 100%);
  box-shadow: inset 0 2px 1px #fff, inset 0 -20px 32px -14px rgba(180,18,47,0.18),
              0 36px 64px -22px rgba(30,4,12,0.55), 0 3px 8px rgba(30,4,12,0.12);
  display: flex; align-items: center; justify-content: center; }
.jelly { position: absolute; inset: 0; border-radius: 22.4%; overflow: hidden;
  background: linear-gradient(165deg, #e0204b 0%, #ab112e 46%, #6b081c 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.55), inset 0 -26px 40px -14px rgba(255,125,165,0.60),
              inset 0 0 0 1px rgba(255,255,255,0.10),
              0 36px 64px -22px rgba(70,4,20,0.62), 0 3px 8px rgba(70,4,20,0.14);
  display: flex; align-items: center; justify-content: center; }
.jelly::after, .pearl::after { content: ""; position: absolute; left: 7%; right: 7%; top: 3.5%; height: 44%;
  border-radius: 40% 40% 50% 50% / 38% 38% 24% 24%;
  background: linear-gradient(180deg, rgba(255,255,255,0.26), rgba(255,255,255,0)); }
.pearl::after { background: linear-gradient(180deg, rgba(255,255,255,0.9), rgba(255,255,255,0)); opacity: 0.5; }
.jelly .gl { width: 50%; height: 50%; fill: url(#gw); position: relative; z-index: 1; }
.wmark { font-weight: 900; color: #17141c; letter-spacing: -0.045em; line-height: 1;
  position: relative; z-index: 1; transform: translate(2%, -3%); }
.wmark i { font-style: normal; color: #b4122f; }
.sheen { position: absolute; inset: -10%; z-index: 2;
  background: linear-gradient(105deg, rgba(255,255,255,0) 38%, rgba(255,255,255,0.75) 50%, rgba(255,255,255,0) 62%);
  mix-blend-mode: soft-light; }

#wWrap { left: 440px; top: 200px; width: 200px; height: 200px; }
#wtile { position: absolute; inset: 0; }
#wtile .wmark { font-size: 128px; }
.ring { position: absolute; left: 440px; top: 200px; width: 200px; height: 200px; border-radius: 22.4%;
  border: 3px solid rgba(255,255,255,0.75); }
#hubGlow { left: 240px; top: 0px; width: 600px; height: 600px;
  background: radial-gradient(circle, rgba(255,110,156,0.55) 0%, rgba(255,110,156,0) 60%); }

#cable { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: visible; }
#cable .tube { fill: none; stroke: rgba(255,255,255,0.26); stroke-width: 20; stroke-linecap: round; }
#cable .core { fill: none; stroke: rgba(255,255,255,0.92); stroke-width: 4.5; stroke-linecap: round; }
#cable .pkt { fill: none; stroke: #ffd6e3; stroke-width: 11; stroke-linecap: round; }
#cable .pk { filter: drop-shadow(0 0 10px rgba(255,120,165,1)); }
.port { fill: #fff; }
#aiWrap { left: 700px; top: 280px; width: 210px; height: 210px; perspective: 1100px; }
#flip { position: absolute; inset: 0; transform-style: preserve-3d; }
.face { position: absolute; inset: 0; backface-visibility: hidden; -webkit-backface-visibility: hidden; }
.face.back { transform: rotateY(180deg); }
#aiGlow { left: 555px; top: 135px; width: 500px; height: 500px;
  background: radial-gradient(circle, rgba(255,110,156,0.6) 0%, rgba(255,110,156,0) 62%); }

/* ---- the takeover ---- */
#tk { position: absolute; inset: 0; clip-path: circle(0px at 540px 300px); }
#tkGround { position: absolute; inset: 0;
  background: linear-gradient(172deg, #4a0a1c 0%, #660c26 36%, #3c0716 70%, #1d030a 100%); }
.blob { position: absolute; border-radius: 50%; }
#bl1 { left: 260px; top: -420px; width: 1200px; height: 1200px;
  background: radial-gradient(circle, rgba(255,110,156,0.50) 0%, rgba(255,110,156,0) 62%); }
#bl2 { left: -640px; top: 960px; width: 1400px; height: 1400px;
  background: radial-gradient(circle, rgba(222,32,74,0.55) 0%, rgba(222,32,74,0) 64%); }
#bl3 { left: 330px; top: 760px; width: 900px; height: 900px;
  background: radial-gradient(circle, rgba(255,198,214,0.20) 0%, rgba(255,198,214,0) 60%); }
#grain { position: absolute; inset: 0; background: url("assets/grain.png"); opacity: 0.075;
  mix-blend-mode: overlay; }

#cardWrap { left: 100px; top: 240px; width: 880px; height: 1000px; transform-origin: 440px 60px; }
#card { position: absolute; inset: 0; border-radius: 68px; overflow: hidden;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 55%, #fdf0f4 100%);
  box-shadow: inset 0 2px 1px #fff, inset 0 -30px 60px -30px rgba(180,18,47,0.14),
              0 70px 130px -40px rgba(8,0,3,0.75), 0 0 0 1px rgba(255,255,255,0.35); }
#card .sheen { mix-blend-mode: normal; opacity: 0.55; }
.cx { position: absolute; }
#chIcon { left: 60px; top: 54px; width: 84px; height: 84px; }
#chIcon .wmark { font-size: 54px; color: #fff; }
#chIcon .wmark i { color: #ffb3c9; }
#chTitle { left: 168px; top: 56px; font-size: 42px; font-weight: 700; letter-spacing: -0.015em; }
#chSub { left: 168px; top: 110px; font-size: 26px; font-weight: 500; color: rgba(23,20,28,0.46); }
#chPill { right: 60px; top: 66px; height: 58px; padding: 0 24px 0 18px; border-radius: 29px;
  background: #fbe3ea; color: #b4122f; font-size: 26px; font-weight: 700; letter-spacing: 0.02em;
  display: flex; align-items: center; gap: 10px; box-shadow: inset 0 0 0 1px rgba(180,18,47,0.08); }
#chPill svg { width: 28px; height: 28px; fill: none; stroke: #b4122f; stroke-width: 3; stroke-linecap: round; stroke-linejoin: round; }
#hair1 { left: 60px; right: 60px; top: 172px; height: 2px; background: rgba(23,20,28,0.07); transform-origin: 0 0; }
#kLabel { left: 60px; top: 206px; font-size: 24px; font-weight: 700; letter-spacing: 0.16em; color: rgba(23,20,28,0.42); }
#kNum { left: 52px; top: 232px; font-size: 176px; font-weight: 900; letter-spacing: -0.045em; line-height: 1;
  background: linear-gradient(118deg, #7e0b20 0%, #b4122f 42%, #ff6e9c 100%);
  -webkit-background-clip: text; background-clip: text; color: transparent; padding-right: 10px; }
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

/* ---- the notification ---- */
#banner { left: 60px; top: 186px; width: 960px; height: 176px; border-radius: 64px;
  background: linear-gradient(160deg, rgba(58,22,32,0.58) 0%, rgba(24,10,15,0.50) 100%);
  -webkit-backdrop-filter: blur(30px) saturate(1.8); backdrop-filter: blur(30px) saturate(1.8);
  box-shadow: inset 0 1.5px 1px rgba(255,255,255,0.30), inset 0 -16px 30px -16px rgba(255,255,255,0.14),
              0 40px 80px -30px rgba(10,0,4,0.6); color: #fff; }
#bIcon { left: 36px; top: 36px; width: 104px; height: 104px; }
#bTitle { left: 170px; top: 42px; font-size: 36px; font-weight: 700; letter-spacing: -0.01em; }
#bBody { left: 170px; top: 94px; font-size: 30px; font-weight: 400; color: rgba(255,255,255,0.80); }
#bTime { right: 44px; top: 48px; font-size: 26px; color: rgba(255,255,255,0.50); }

/* ---- captions: unchanged house style ---- */
#scrim { position: absolute; left: 20px; top: 1247px; width: 1040px; height: 450px;
  background-image: url("assets/underlay.png"); background-size: 100% 100%; background-repeat: no-repeat;
  opacity: 0; visibility: hidden; pointer-events: none; }
.cap { position: absolute; left: 0; width: 1080px; top: 1413px; height: 118px; line-height: 118px;
  text-align: center; color: #fff; font-size: 90px; font-weight: 900; letter-spacing: -0.015em;
  white-space: nowrap; opacity: 0; visibility: hidden; }
"""

REPEAT = ('<svg viewBox="0 0 28 28"><path d="M5 12a9 9 0 0 1 15.5-5.2L23 9"/>'
          '<path d="M23 3.5V9h-5.5"/><path d="M23 16a9 9 0 0 1-15.5 5.2L5 19"/>'
          '<path d="M5 24.5V19h5.5"/></svg>')
UP = '<svg viewBox="0 0 22 22"><path d="M11 18V4"/><path d="M4.5 10.5 11 4l6.5 6.5"/></svg>'


def wall_html():
    out = []
    for n, t in enumerate(wall):
        out.append('<div class="wt hide" id="wt%d" style="left:%dpx;top:%dpx">%s</div>'
                   % (n, t["x"], t["y"], glyph(t["g"], "")))
    return "\n        ".join(out)


def hero_html():
    return "\n        ".join(
        '<div class="src hide" id="s-%s" style="left:%dpx;top:%dpx">'
        '<div class="clear edge" id="st-%s">%s</div></div>'
        % (k, c[0], c[1], k, glyph(ic)) for k, ic, c in HERO)


def wires_html():
    return "\n          ".join(
        '<path class="w" id="wr-%s" d="%s"/><g class="pk"><path class="p" id="wp-%s" d="%s"/></g>'
        % (k, wire(c), k, wire(c)) for k, _, c in HERO)


def rows_html():
    rows = [("instagram", "Instagram", "12,4K", "+18%"),
            ("tiktok", "TikTok", "8,1K", "+9%"),
            ("meta", u"Реклама", u"ROAS 3,2×", "")]
    out = []
    for i, (ic, lab, val, dl) in enumerate(rows):
        top = 736 + i * 84
        out.append('<div class="row" id="row%d" style="top:%dpx"><div class="ri">%s</div>'
                   '<div class="rl">%s</div><div class="rv">%s</div><div class="rd">%s</div></div>'
                   % (i, top, glyph(ic, ""), lab, val, dl))
        if i < 2:
            out.append('<div class="rowline" id="rl%d" style="top:%dpx"></div>' % (i, top + 83))
    return "\n            ".join(out)


def captions_html():
    return "\n    ".join('<div class="cap" id="cap%d">%s</div>'
                         % (i, c["w"].upper().replace(",", ",").rstrip()) for i, c in enumerate(WORDS))


def captions_js():
    lines = []
    for i, c in enumerate(WORDS):
        lines.append('tl.set("#cap%d",{autoAlpha:1},%.3f);tl.set("#cap%d",{autoAlpha:0},%.3f);'
                     % (i, c["s"], i, c["e"]))
    lines.append('tl.to("#scrim",{autoAlpha:1,duration:0.5},%.3f);' % max(0, WORDS[0]["s"] - 0.3))
    lines.append('tl.to("#scrim",{autoAlpha:0,duration:0.6},%.3f);' % (WORDS[-1]["e"] + 0.1))
    return "\n  ".join(lines)


CFG = {
    "T": T, "hub": HUB, "maxd": MAXD,
    "wall": [{"x": t["x"], "y": t["y"], "d": t["d"], "o": t["o"]} for t in wall],
    "hero": [{"k": k, "x": c[0], "y": c[1], "cx": hero_cells[k][0], "cy": hero_cells[k][1],
              "d": round(math.hypot(hero_cells[k][0] - HUB[0], hero_cells[k][1] - HUB[1]), 1)}
             for k, _, c in HERO],
    "end": END_PT,
}

JS = r"""
function spring(z, w) {
  var wd = w * Math.sqrt(1 - z * z);
  function f(t) { return 1 - Math.exp(-z * w * t) * (Math.cos(wd * t) + (z * w / wd) * Math.sin(wd * t)); }
  var e = f(1);
  return function (t) { return t >= 1 ? 1 : f(t) / e; };
}
var SP = spring(0.62, 13), POP = spring(0.46, 14), SOFT = spring(0.84, 11), FLIP = spring(0.58, 9);

function build() {
  var tl = gsap.timeline({paused: true});
  var T = CFG.T;
  function blurIn(sel, t, b, d) {
    tl.fromTo(sel, {autoAlpha: 0, filter: "blur(" + (b || 12) + "px)"},
                   {autoAlpha: 1, filter: "blur(0px)", duration: d || 0.38, ease: "power2.out"}, t);
  }
  function blurOut(sel, t, b, d) {
    tl.to(sel, {autoAlpha: 0, filter: "blur(" + (b || 10) + "px)", duration: d || 0.32, ease: "power2.in"}, t);
  }
  function len(id) { return document.getElementById(id).getTotalLength(); }
  function drawPrep(id) { var L = len(id); gsap.set("#" + id, {strokeDasharray: L + " " + (L + 40), strokeDashoffset: L + 3}); return L + 3; }
  function packet(id, t, d) {
    var L = len(id);
    tl.fromTo("#" + id, {strokeDasharray: "46 " + (L + 200), strokeDashoffset: 49, autoAlpha: 1},
              {strokeDashoffset: -L, duration: d || 0.5, ease: "power1.inOut"}, t);
    tl.set("#" + id, {autoAlpha: 0}, t + (d || 0.5));
  }

  gsap.set(".sheen", {xPercent: -120});
  // --- camera: the still breathes forward the whole time
  tl.fromTo("#cam", {scale: 1.0}, {scale: 1.045, duration: T.dur, ease: "none"}, 0);

  // ================= A · near her: the glass shelf, Windsor, the AI =================
  var tA = T.cherez - 0.12;
  blurIn("#dock", tA, 14, 0.45);
  tl.fromTo("#dock", {scale: 0.9, y: 36}, {scale: 1, y: 0, duration: 0.95, ease: SP}, tA);

  // Windsor: starts at its shelf seat, later becomes the hub
  gsap.set("#wWrap", {x: -265, y: 85, scale: 1.05});
  blurIn("#wWrap", T.windsor1 - 0.1, 14, 0.36);
  tl.fromTo("#wtile", {scale: 0.5, y: 34}, {scale: 1, y: 0, duration: 0.85, ease: POP}, T.windsor1 - 0.1);
  tl.fromTo("#wtile .wmark", {scale: 0.6, autoAlpha: 0}, {scale: 1, autoAlpha: 1, duration: 0.6, ease: SP}, T.windsor1);
  tl.to("#wtile .sheen", {xPercent: 120, duration: 0.75, ease: "power2.inOut"}, T.windsor1 + 0.4);

  var Lc = drawPrep("cabT"); drawPrep("cabC");
  tl.fromTo(".port", {scale: 0, transformOrigin: "50% 50%"}, {scale: 1, duration: 0.4, ease: POP, stagger: 0.42}, T.pidkl - 0.05);
  tl.to(["#cabT", "#cabC"], {strokeDashoffset: 0, duration: 0.62, ease: "power2.inOut"}, T.pidkl);

  blurIn("#aiWrap", T.claude - 0.12, 14, 0.36);
  tl.fromTo("#aiWrap", {x: 90, scale: 0.55}, {x: 0, scale: 1, duration: 0.85, ease: POP}, T.claude - 0.12);
  tl.fromTo("#aiWrap .front .gl", {scale: 0.55, autoAlpha: 0}, {scale: 1, autoAlpha: 1, duration: 0.55, ease: SP}, T.claude - 0.02);
  tl.fromTo("#aiGlow", {autoAlpha: 0, scale: 0.6}, {autoAlpha: 1, scale: 1, duration: 0.35, ease: "power2.out"}, T.claude + 0.05);
  tl.to("#aiGlow", {autoAlpha: 0, duration: 0.6, ease: "power2.in"}, T.claude + 0.45);
  packet("cabP", T.claude + 0.12, 0.5);

  var tF = T.chatgpt - 0.16;
  tl.fromTo("#flip", {rotationY: 0}, {rotationY: 180, duration: 1.0, ease: FLIP}, tF);
  tl.to("#flip", {scale: 0.9, duration: 0.3, ease: "power2.out"}, tF);
  tl.to("#flip", {scale: 1, duration: 0.6, ease: SP}, tF + 0.3);
  tl.fromTo("#aiGlow", {autoAlpha: 0}, {autoAlpha: 0.85, duration: 0.3, ease: "power2.out", immediateRender: false}, T.chatgpt + 0.1);
  tl.to("#aiGlow", {autoAlpha: 0, duration: 0.6, ease: "power2.in"}, T.chatgpt + 0.45);
  packet("cabP", T.chatgpt + 0.35, 0.5);

  // ================= A -> B · the shelf's frost spreads into the room =================
  var tX = T.chatgpt_e + 0.12;
  blurOut("#aiWrap", tX, 10, 0.34);
  tl.to("#aiWrap", {x: 60, scale: 0.8, duration: 0.34, ease: "power2.in"}, tX);
  tl.to(["#cabT", "#cabC"], {strokeDashoffset: Lc, duration: 0.4, ease: "power2.in"}, tX);
  tl.to(".port", {scale: 0, duration: 0.25, ease: "power2.in"}, tX + 0.2);
  tl.to("#dock", {scale: 1.35, duration: 0.7, ease: "power2.in"}, tX + 0.05);
  blurOut("#dock", tX + 0.2, 16, 0.5);
  tl.fromTo(["#roomSoft", "#roomTint"], {autoAlpha: 0}, {autoAlpha: 1, duration: 0.7, ease: "power1.inOut"}, tX + 0.1);
  tl.to("#wWrap", {x: 0, y: 0, scale: 1, duration: 0.95, ease: SP}, tX + 0.08);

  // ================= B · behind her: sources plug into the hub =================
  CFG.hero.forEach(function (h, i) {
    var t = T[h.k] - 0.08, s = "#s-" + h.k;
    blurIn(s, t, 12, 0.36);
    tl.fromTo(s, {scale: 0.5, y: 40}, {scale: 1, y: 0, duration: 0.8, ease: POP}, t);
    tl.fromTo(s + " .gl", {scale: 0.55, autoAlpha: 0}, {scale: 1, autoAlpha: 1, duration: 0.55, ease: SP}, t + 0.1);
    var L = drawPrep("wr-" + h.k);
    tl.to("#wr-" + h.k, {strokeDashoffset: 0, duration: 0.45, ease: "power2.inOut"}, t + 0.14);
    gsap.set("#wp-" + h.k, {autoAlpha: 0});
    packet("wp-" + h.k, t + 0.4, 0.45);
    tl.to("#wtile", {scale: 1.07, duration: 0.1, ease: "power2.out"}, t + 0.84);
    tl.to("#wtile", {scale: 1, duration: 0.45, ease: SP}, t + 0.94);
    tl.fromTo("#ring" + i, {scale: 1, autoAlpha: 0.7}, {scale: 1.75, autoAlpha: 0, duration: 0.8, ease: "power2.out", immediateRender: false}, t + 0.86);
  });

  // "мільйон": the wall ripples out of the hub, the heroes take their seats
  var tM = T.milyon - 0.04;
  tl.to("#wires", {autoAlpha: 0, duration: 0.3, ease: "power1.in"}, tM);
  CFG.hero.forEach(function (h) {
    tl.to("#s-" + h.k, {x: h.cx - h.x, y: h.cy - h.y, scale: 100 / 168, duration: 0.7, ease: SP}, tM + h.d * 0.00042);
  });
  CFG.wall.forEach(function (w, n) {
    var t = tM + w.d * 0.00042;
    tl.fromTo("#wt" + n, {autoAlpha: 0, scale: 0.3}, {autoAlpha: w.o, duration: 0.3, ease: "power2.out"}, t);
    tl.to("#wt" + n, {scale: 1, duration: 0.6, ease: SP}, t);
  });
  tl.fromTo("#wall", {scale: 1.1}, {scale: 1, duration: 1.5, ease: "power2.out"}, tM);
  tl.fromTo("#hubGlow", {autoAlpha: 0}, {autoAlpha: 1, duration: 0.6, ease: "power2.out"}, tM);

  // ================= B -> C · everything is pulled into the hub, which opens =================
  var tC = T.danykh_e + 0.02;
  CFG.wall.forEach(function (w, n) {
    tl.to("#wt" + n, {x: (CFG.hub[0] - w.x) * 0.38, y: (CFG.hub[1] - w.y) * 0.38, scale: 0, autoAlpha: 0,
                      duration: 0.42, ease: "power2.in"}, tC + (CFG.maxd - w.d) * 0.00022);
  });
  CFG.hero.forEach(function (h) {
    tl.to("#s-" + h.k, {x: (h.cx - h.x) + (CFG.hub[0] - h.cx) * 0.38, y: (h.cy - h.y) + (CFG.hub[1] - h.cy) * 0.38,
                        scale: 0, autoAlpha: 0, duration: 0.42, ease: "power2.in"}, tC + (CFG.maxd - h.d) * 0.00022);
  });
  tl.to("#wtile", {scale: 1.14, duration: 0.4, ease: "power2.in"}, tC + 0.12);
  tl.to("#hubGlow", {scale: 1.4, duration: 0.4, ease: "power2.in"}, tC + 0.12);

  var tI = tC + 0.42;
  tl.set("#tk", {autoAlpha: 1}, tI);
  tl.fromTo("#tk", {clipPath: "circle(0px at 540px 300px)"},
            {clipPath: "circle(2300px at 540px 300px)", duration: 0.85, ease: "power3.inOut", immediateRender: false}, tI);
  tl.fromTo("#bl1", {x: 0, y: 0}, {x: -140, y: 90, duration: 4.5, ease: "sine.inOut"}, tI);
  tl.fromTo("#bl2", {x: 0, y: 0}, {x: 160, y: -120, duration: 4.5, ease: "sine.inOut"}, tI);
  tl.fromTo("#bl3", {x: 0, y: 0}, {x: -90, y: -60, duration: 4.5, ease: "sine.inOut"}, tI);
  // under the takeover, put her room back
  tl.set(["#roomSoft", "#roomTint", "#wWrap", "#hubGlow", "#wall", "#behind"], {autoAlpha: 0}, tI + 0.9);

  // ================= C · over her: the report grows out of the hub =================
  var tR = tI + 0.1;
  blurIn("#cardWrap", tR, 16, 0.45);
  tl.fromTo("#cardWrap", {scale: 0.22}, {scale: 1, duration: 1.05, ease: spring(0.72, 12)}, tR);
  tl.fromTo(["#chIcon", "#chTitle", "#chSub", "#chPill"], {autoAlpha: 0, y: 16},
            {autoAlpha: 1, y: 0, duration: 0.6, ease: SP, stagger: 0.06}, tR + 0.32);
  tl.fromTo("#hair1", {scaleX: 0}, {scaleX: 1, duration: 0.7, ease: "power3.out"}, tR + 0.42);
  tl.fromTo("#kLabel", {autoAlpha: 0, y: 12}, {autoAlpha: 1, y: 0, duration: 0.5, ease: SP}, tR + 0.46);
  var num = {v: 0}, kn = document.getElementById("kNum");
  tl.fromTo("#kNum", {autoAlpha: 0, y: 26}, {autoAlpha: 1, y: 0, duration: 0.6, ease: SP}, T.harnenko - 0.25);
  tl.fromTo(num, {v: 0}, {v: 38, duration: 1.1, ease: "power2.out",
            onUpdate: function () { kn.textContent = "+" + Math.round(num.v) + "%"; }}, T.harnenko - 0.2);
  tl.fromTo("#kDelta", {autoAlpha: 0, scale: 0.6}, {autoAlpha: 1, scale: 1, duration: 0.6, ease: POP}, T.harnenko + 0.55);
  tl.fromTo(".gridl", {autoAlpha: 0}, {autoAlpha: 1, duration: 0.5, stagger: 0.08}, tR + 0.5);
  var Ll = drawPrep("cLine");
  tl.to("#cLine", {strokeDashoffset: 0, duration: 0.95, ease: "power2.inOut"}, T.sform - 0.3);
  tl.fromTo("#cArea", {clipPath: "inset(0px 100% 0px 0px)"}, {clipPath: "inset(0px 0% 0px 0px)", duration: 0.95, ease: "power2.inOut"}, T.sform - 0.3);
  tl.fromTo("#days span", {autoAlpha: 0, y: 8}, {autoAlpha: 1, y: 0, duration: 0.4, stagger: 0.1, ease: SP}, T.sform - 0.3);
  tl.fromTo("#cDot", {scale: 0, transformOrigin: "50% 50%"}, {scale: 1, duration: 0.5, ease: POP}, T.sform + 0.6);
  tl.fromTo("#cRing", {scale: 1, autoAlpha: 0.6, transformOrigin: "50% 50%"}, {scale: 3, autoAlpha: 0, duration: 0.9, ease: "power2.out", immediateRender: false}, T.sform + 0.7);
  tl.fromTo([".row", ".rowline"], {autoAlpha: 0, y: 22}, {autoAlpha: 1, y: 0, duration: 0.6, ease: SP, stagger: 0.07}, T.sform + 0.1);
  tl.to("#card .sheen", {xPercent: 120, duration: 0.9, ease: "power2.inOut"}, T.zvit + 0.05);

  // ================= D · the report folds into a notification near her =================
  var tN = T.tada - 0.42;
  tl.to("#cardWrap", {scale: 0.2, y: -40, duration: 0.5, ease: "power3.in"}, tN);
  blurOut("#cardWrap", tN + 0.22, 12, 0.28);
  tl.to("#tk", {clipPath: "circle(0px at 540px 274px)", duration: 0.6, ease: "power3.inOut"}, tN + 0.05);
  tl.set("#tk", {autoAlpha: 0}, tN + 0.66);
  var tB = tN + 0.36;
  blurIn("#banner", tB, 12, 0.3);
  tl.fromTo("#banner", {scale: 0.62, y: -26}, {scale: 1, y: 0, duration: 0.9, ease: POP}, tB);
  tl.fromTo(["#bIcon", "#bTitle", "#bTime", "#bBody"], {autoAlpha: 0, y: 10},
            {autoAlpha: 1, y: 0, duration: 0.5, ease: SP, stagger: 0.05}, tB + 0.14);
  tl.to("#banner", {keyframes: {x: [0, -9, 8, -5, 3, 0]}, duration: 0.34, ease: "none"}, T.tada + 0.38);
  var tE = T.dur - 0.62;
  tl.to("#banner", {y: -48, scale: 0.97, duration: 0.42, ease: "power2.in"}, tE);
  blurOut("#banner", tE + 0.08, 10, 0.34);

  CAPTIONS
  window.__timelines["main"] = tl;
}
if (document.fonts && document.fonts.ready) document.fonts.ready.then(build); else build();
"""


def document():
    wm = '<span class="wmark">w<i>.</i></span>'
    html = u'''<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="utf-8">
<title>Style test — refined glass</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<style>%(css)s</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-width="1080" data-height="1920"
     data-duration="%(dur).3f" data-fps="30">
  <svg width="0" height="0" style="position:absolute">
    <defs>
      <linearGradient id="gw" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#ffdbe6"/>
      </linearGradient>
      <linearGradient id="gLine" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0" stop-color="#8d0d24"/><stop offset="0.55" stop-color="#c8173a"/><stop offset="1" stop-color="#ff6e9c"/>
      </linearGradient>
      <linearGradient id="gArea" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="#ff6e9c" stop-opacity="0.34"/><stop offset="1" stop-color="#ff6e9c" stop-opacity="0"/>
      </linearGradient>
      %(symbols)s
    </defs>
  </svg>

  <div id="cam">
    <img id="plate" src="assets/plate.jpg" alt="">
    <img id="roomSoft" class="hide" src="assets/room_soft.jpg" alt="">
    <div id="roomTint" class="hide"></div>
    <div id="behind">
      <svg id="wires" viewBox="0 0 1080 1920">
          %(wires)s
      </svg>
      <div id="wall">
        %(wall)s
      </div>
        %(heroes)s
    </div>
    <img id="her" src="assets/her.png" alt="">
  </div>

  <div id="near">
    <div id="dock" class="abs edge hide"></div>
    <svg id="cable" viewBox="0 0 1080 1920">
      <path class="tube" id="cabT" d="M 380 385 C 470 448 610 448 700 385"/>
      <path class="core" id="cabC" d="M 380 385 C 470 448 610 448 700 385"/>
      <g class="pk"><path class="pkt hide" id="cabP" d="M 380 385 C 470 448 610 448 700 385"/></g>
      <circle class="port" cx="380" cy="385" r="11"/><circle class="port" cx="700" cy="385" r="11"/>
    </svg>
    <div id="hubGlow" class="abs hide"></div>
    <div class="ring hide" id="ring0"></div><div class="ring hide" id="ring1"></div><div class="ring hide" id="ring2"></div>
    <div class="ring hide" id="ring3"></div><div class="ring hide" id="ring4"></div>
    <div id="wWrap" class="abs hide"><div id="wtile" class="pearl">%(wm)s<div class="sheen"></div></div></div>
    <div id="aiGlow" class="abs hide"></div>
    <div id="aiWrap" class="abs hide">
      <div id="flip">
        <div class="face front"><div class="jelly">%(claude)s</div></div>
        <div class="face back"><div class="jelly">%(openai)s</div></div>
      </div>
    </div>
  </div>

  <div id="tk" class="hide">
    <div id="tkGround"></div>
    <div class="blob" id="bl1"></div><div class="blob" id="bl2"></div><div class="blob" id="bl3"></div>
    <div id="grain"></div>
    <div id="cardWrap" class="abs hide">
      <div id="card">
        <div class="cx" id="chIcon"><div class="jelly">%(wm)s</div></div>
        <div class="cx" id="chTitle">Підсумок тижня</div>
        <div class="cx" id="chSub">22–28 вересня · 5 джерел</div>
        <div class="cx" id="chPill">%(repeat)s<span>ПН 09:00</span></div>
        <div class="cx" id="hair1"></div>
        <div class="cx" id="kLabel">ОХОПЛЕННЯ</div>
        <div class="cx" id="kNum">+0%%</div>
        <div class="cx" id="kDelta">%(up)s<span>12,4K</span></div>
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
  </div>

  <div id="top">
    <div id="banner" class="abs edge hide">
      <div class="cx" id="bIcon"><div class="jelly">%(claude)s</div></div>
      <div class="cx" id="bTitle">Claude</div>
      <div class="cx" id="bTime">зараз</div>
      <div class="cx" id="bBody">Тижневий звіт готовий · охоплення +38%%</div>
    </div>
  </div>

  <div id="scrim"></div>
    %(caps)s
</div>
<script>
var CFG = %(cfg)s;
%(js)s
</script>
</body>
</html>
''' % {
        "css": CSS, "dur": DUR, "symbols": SYMBOLS, "wires": wires_html(),
        "wall": wall_html(), "heroes": hero_html(), "wm": wm,
        "claude": glyph("claude"), "openai": glyph("openai"),
        "repeat": REPEAT, "up": UP, "cw": CW, "ch": CH, "area": AREA, "line": LINE,
        "ex": END_PT[0], "ey": END_PT[1], "rows": rows_html(),
        "caps": captions_html(), "cfg": json.dumps(CFG),
        "js": JS.replace("CAPTIONS", captions_js()),
    }
    return html


if __name__ == "__main__":
    io.open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(document())
    json.dump({"words": WORDS}, io.open(os.path.join(HERE, "captions.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("DUR %.3f  (%d frames)  words %d  wall %d" % (DUR, round(DUR * FPS), len(WORDS), len(wall)))
    for k in ("windsor1", "claude", "chatgpt", "ig", "stat", "milyon", "danykh_e", "vydaie", "zvit", "tada"):
        print("  %-9s %.2f" % (k, T[k]))
