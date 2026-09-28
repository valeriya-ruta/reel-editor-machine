# -*- coding: utf-8 -*-
"""Reel 17 — «Ти думаєш, що всі ці рілси хтось монтував руками». Posts 2026-10-01.

Variant B, refined glass (STYLE.md §0). A reel about AI-edited reels, edited
by AI, so it gets to be meta. Six shots (tools/shots.py) plus one it missed:
three short inserts are hers — 20.10-21.73 (the pointing «І ось
найцікавіше»), the 31.10-31.87 closeup on «типово» and the face she pulls in
closeup from 63.43 to the end — and stay NO_PAINT. No pull-outs.

The one object is **her Reels grid** — the nine real cells she sent
(work/media/r17, cropped to reel-17/assets/grid). It opens as a wall behind
her, drains when she «випала з блогу», comes back one day at a time on a
calendar, flies out of Drafts back onto the wall, and at «ось результат» this
very reel shrinks into one cell of it.

The chain, behind -> near -> behind -> near -> over -> near:
    her reels on a wall behind her; a Claude tile lands above her head and a
    light passes over the wall -> the wall falls away and a month calendar
    lands on the dark glass shelf, every day empty, a "today" ring racing
    through it; the last nine days fill with the series -> the best one of
    them (day 27) lifts out into its real insights: 2 799 views, flat; then
    43 likes, 37 saves, 7 shares, +6 follows count up -> a DM thread starts
    -> the shelf's frost spreads into the room: a Drafts folder behind her,
    six reels fly out of it onto the wall, and the one left inside dies there
    -> (her insert) -> a Claude tile, and out of it the typical AI output in
    three formats — a video, a design, a carousel — all in the same slop ->
    (her closeup) -> the iris opens out of the carousel into the slop at full
    frame: sparkles on «підсвічене», the colours spin on «кольорів», stickers
    on «елементами» -> «навчити»: the stickers are knocked off, the slide
    shrinks onto a burgundy ground and drains into a clean white sheet; one
    «AI» sticker survives on its corner and is flicked off on «AI-слоп» ->
    the same sheet turns into the bad news: 90 % НАВЧАННЯ / 10 % ПЕРЕВІРКА,
    and the 10 % gets its tick -> the iris closes onto her -> «ось результат»:
    the whole frame, her included, shrinks into the middle cell of her grid,
    her other reels around it, and scales back -> an IG poll sticker,
    «Здогадалась би?», Так / Ні, and a tap lands on «Ні».

She cut three lines from the script while recording (the «на вході, а не на
виході» sentence and the whole «не так важливо, скільки переглядів» passage),
so PLAN.md beats 12, 14 and 15 are gone; her wording is in the captions
(work/r17/caption-patch.json).

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
sys.path.insert(0, os.path.join(ROOT, "reel-13"))
from kit import Kit  # noqa: E402
from glass import Glass  # noqa: E402
from slop import Slop  # noqa: E402  (the reusable slop frame — imported, not forked)

DUR = 64.317           # 1930 plate frames / 30 (work/w40-queue2.log)
FPS = 30
k = Kit(width=1080, height=1920, fps=FPS, duration=DUR)
g = Glass()
k.css(g.css())
slop = Slop()
k.css(slop.css())

BEATS = []


def beat(fn):
    BEATS.append(fn)
    return fn


# ---------------------------------------------------------------------------
# NO-PAINT ZONES — her own editing (STYLE.md §4a). tools/shots.py: six shots,
# two of them short inserts; tools/pullouts.py: none.
#   20.10 – 21.73   she cuts in pointing on «І ось найцікавіше:»
#   31.10 – 31.87   face closeup on «типово.»
#   63.43 – 64.32   she cuts in close and pulls a face to end the reel — too
#                   near the end for shots.py to call it a shot; found by frame
#                   difference (frame 1903, mean |Δ| 23 against ~0.5)
NO_PAINT = [(20.10, 21.73), (31.10, 31.87), (63.43, 64.32)]

# ---------------------------------------------------------------------------
# Words. Script spelling on her timing (work/r17/captions.json, settled with
# work/r17/caption-patch.json). Ends re-derived from the next start, the rule
# align.py uses, because the patch merged and dropped tokens.
CAPS = k.load_captions(os.path.join(ROOT, "work", "r17", "captions.json"))
for _a, _b in zip(CAPS, CAPS[1:]):
    _a["e"] = round(max(_a["s"] + 0.10, _b["s"] - 0.085), 3)

T = {
    "ty": 0.00, "vsi": 0.96, "rilsy": 1.56, "khtos": 1.96, "rukamy": 2.78,
    "a1": 3.32, "montuvav": 3.64, "shtuchnyi": 4.12, "intelekt": 4.76,
    "ya": 5.44, "vypala": 5.56, "na": 6.44, "tsilyi": 6.64, "misiats": 7.24,
    "a2": 7.64, "zapostyla": 8.04, "seriiu": 8.66, "rilsiv": 9.12,
    "ikhoch": 9.74, "perehliady": 10.80, "ne": 11.42, "super": 11.62,
    "ale": 11.94, "aktyvnist": 12.12, "pidnialas": 12.98,
    "rozmovy": 13.68, "vdirekti": 14.04, "pishly": 14.54,
    "i1": 15.28, "holovne": 15.42, "kontent": 15.98, "realno": 16.34, "vyishov": 16.84,
    "ane": 17.28, "zavys": 17.50, "chernetkakh": 18.26, "i2": 18.74, "vmer": 18.96,
    "yak": 19.50, "zavzhdy": 19.72,
    "robyt": 26.92, "shtuchnyi2": 27.24, "imontazh": 28.44, "dyzain": 29.16,
    "karuseli": 29.70, "vono": 30.46, "vyhliadaie": 30.72,
    "os": 32.50, "pidsvichene": 34.52, "kupa": 35.28, "koloriv": 35.66,
    "napichkane": 36.62, "elementamy": 37.08,
    "tak": 38.08, "pravylno": 39.26, "navchyty": 39.68, "mozhe": 40.36,
    "normalno": 41.04, "bez": 41.54, "slop": 42.48,
    "pohana": 43.40, "novyna": 43.80, "pravylno2": 44.74, "p90": 46.08,
    "roboty": 47.52, "ostanni": 48.22, "p10": 48.54, "pereviryty": 49.86,
    "zrobyv": 50.72, "yaktreba": 51.26,
    "ale2": 51.46, "tochno": 52.96, "pratsiuiut": 53.30, "bo": 54.16,
    "os2": 54.26, "rezultat": 54.74, "a3": 55.40, "napyshy": 55.74,
    "chy": 56.92, "zdogadalas": 57.18, "shcho": 58.22, "rils": 58.64,
    "zmont": 59.10, "ne2": 61.32, "skazala": 61.58,
    "meni": 62.28, "tsikavo": 62.64, "pobachyty": 63.00,
    "dur": DUR,
}
_starts = [c["s"] for c in CAPS]
for _k, _v in T.items():
    if _k != "dur":
        assert min(abs(_v - s) for s in _starts) < 0.021, (_k, _v)


def js(src):
    """`@name`, `@name+0.12`, `@name-0.1` -> one literal time. Literals, not
    variables, because tools/review.py reads the timeline off the numbers."""
    def rep(m):
        v = T[m.group(1)] + (float(m.group(2)) if m.group(2) else 0.0)
        return "%.3f" % v
    return re.sub(r"@(\w+)([+-]\d+(?:\.\d+)?)?", rep, src)


# ---------------------------------------------------------------------------
# Mattes (tools/matte.py via work/r17/mattes.sh). (first frame, count). The
# soft rooms (work/r17/softroom.sh) are cut from the same frames.
MATTES = {"wall": (0, 169), "drafts": (456, 147)}
for _n, (_f0, _c) in MATTES.items():
    k.matte(_n, _f0 / 30.0, _c / 30.0)

# The slow push on the plate (§0.8), about the frame's centre: scaling about
# (540, 960) keeps the plate's centre put, which is what lets it shrink
# straight into the middle cell of the grid (b13) without a correction.
PUSH_O = (540, 960)


def push_at(t):
    return 1.0 + 0.045 * t / DUR


# ---------------------------------------------------------------------------
# Glyphs — monochrome, drawn, never emoji (§5a.11). Strokes use .sk.
STROKES = {
    "eye": '<path d="M1.8 12s3.8-6.8 10.2-6.8S22.2 12 22.2 12s-3.8 6.8-10.2 6.8S1.8 12 1.8 12z"/><circle cx="12" cy="12" r="3.1"/>',
    "heart": '<path d="M12 20.2s-7.9-4.7-7.9-10.4A4.3 4.3 0 0 1 12 7.4a4.3 4.3 0 0 1 7.9 2.4c0 5.7-7.9 10.4-7.9 10.4z"/>',
    "save": '<path d="M6.6 3.8h10.8v16.6L12 16.3l-5.4 4.1z"/>',
    "send": '<path d="M21.2 3.3L10.5 13.5"/><path d="M21.2 3.3l-6.6 17.6-4.1-7.4-7.7-3.9z"/>',
    "follow": '<circle cx="9.4" cy="8.1" r="3.7"/><path d="M2.9 20.1c.8-3.7 3.3-5.7 6.5-5.7s5.7 2 6.5 5.7"/><path d="M18.7 8.2v6.2M15.6 11.3h6.2"/>',
    "up": '<path d="M12 19.2V5.2M5.8 11.4L12 5.2l6.2 6.2"/>',
    "flat": '<path d="M3.5 12h15.2M14.2 7.6l4.5 4.4-4.5 4.4"/>',
    "check": '<path d="M5.4 12.6l4.3 4.3 8.9-9.5"/>',
    "spark": '<path d="M12 3.2l1.9 5.6 5.7 1.9-5.7 1.9L12 18.2l-1.9-5.6-5.7-1.9 5.7-1.9z"/>',
}


def stroke(name, cls="sk"):
    return '<svg class="%s" viewBox="0 0 24 24">%s</svg>' % (cls, STROKES[name])


def tile(tid, size, x, y, material, inner, extra_cls="", ring=True):
    """A tile in the glass family: the wrapper takes the motion, the tile the
    material. x, y are its top-left. A ripple ring of the same shape rides
    with it when asked."""
    r = ('<div class="sqring%s" id="%sR" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></div>'
         % (" circ" if "circ" in extra_cls else "", tid, x, y, size, size)) if ring else ""
    return ('%s<div class="tw %s" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
            '<div class="%s">%s<div class="sheen"></div></div></div>'
            % (r, extra_cls, tid, x, y, size, size, material, inner))


def hidden(html):
    return html.replace('class="tw ', 'class="tw hide ', 1)


k.css("""
.abs, .cx { position: absolute; }
.hide { opacity: 0; visibility: hidden; }
.tw { position: absolute; }
.sk { fill: none; stroke: url(#gw); stroke-width: 2.2; stroke-linecap: round; stroke-linejoin: round;
  width: 50%; height: 50%; position: relative; z-index: 1; overflow: visible; }
.sk.w { stroke: #fff; width: 100%; height: 100%; }
.pearl .sk { stroke: #17141c; }
.circ .jelly, .circ .pearl, .circ .clear, .circ .sheen { border-radius: 50%; }
.sqring.circ { border-radius: 50%; }
.roomTint { position: absolute; inset: 0;
  background: linear-gradient(180deg, rgba(62,8,24,0.16) 0%, rgba(40,5,15,0.34) 100%); }
""")

# the cells she sent, oldest -> newest is c8 -> c0 (her grid reads newest first)
CELL = "assets/grid/c%d.jpg"
GREY = "assets/grid/c%d_g.jpg"

# ============================================================ layers ==
# Bottom to top: BEHIND (in her room, under her mattes) -> NEAR (the shelf
# and tiles above her head, the grid, the poll) -> TK (the takeover). All of
# it is gfx, so all of it sits under her mattes, which only exist while
# something big is behind her.
L = {"behind": [], "near": [], "tk": []}

# ====================================================== A · the wall ==
# 4 x 3 wall of 9:16 cells. Row 0 is clear above her head; rows 1-2 show at
# the sides; the middle four sit behind her and carry repeats.
WALL_X = [50, 300, 550, 800]
WALL_Y = [70, 499, 928]
WALL_W, WALL_H = 230, 409
WALL_SRC = [0, 3, 2, 1,
            5, 1, 6, 4,
            7, 2, 0, 8]
HUB = (540, 250)


def wall_cells():
    out = []
    for i, src in enumerate(WALL_SRC):
        x, y = WALL_X[i % 4], WALL_Y[i // 4]
        cx, cy = x + WALL_W / 2.0, y + WALL_H / 2.0
        out.append({"x": x, "y": y, "src": src,
                    "d": round(math.hypot(cx - HUB[0], cy - HUB[1]), 1),
                    "col": i % 4})
    return out


WALL = wall_cells()

k.css("""
/* ---- b01-b02 · her reels on a wall behind her, the room soft ---- */
.wt { position: absolute; width: 230px; height: 409px; object-fit: cover; border-radius: 22px;
  box-shadow: 0 0 0 2px rgba(255,255,255,0.30), 0 34px 56px -22px rgba(12,0,5,0.7); }
#sweepW { position: absolute; left: 0; top: 0; width: 560px; height: 1500px; pointer-events: none;
  background: linear-gradient(100deg, rgba(255,226,236,0) 18%, rgba(255,226,236,0.42) 50%, rgba(255,226,236,0) 82%);
  mix-blend-mode: screen; }
""")


@beat
def b01_wall():
    """«Ти думаєш, що всі ці рілси хтось монтував руками.»

    BEHIND, cold open. The room goes soft (a soft plate built from her matte,
    so she does not halo) and her real reels ripple out onto a wall behind
    her head — the nine cells she sent, view counts and all. It settles on
    «рілси»."""
    f0, n = MATTES["wall"]
    tiles = "\n          ".join(
        '<img class="wt hide" id="wa%d" src="%s" style="left:%dpx;top:%dpx" alt="">'
        % (i, CELL % c["src"], c["x"], c["y"]) for i, c in enumerate(WALL))
    L["behind"].append(u'''
      <div class="g full" id="gW">
        <div id="roomW" class="hide">
          <video id="softW" class="plate" src="assets/soft/wall.mp4"
                 data-start="%.3f" data-duration="%.3f" data-media-start="0" muted playsinline></video>
          <div class="roomTint"></div>
        </div>
        <div id="wallW">
          %s
        </div>
        <div id="sweepW" class="hide"></div>
        %s
      </div>''' % (f0 / 30.0, n / 30.0, tiles,
                   hidden(tile("clW", 200, 440, 150, "jelly", g.mark("claude")))))
    cfg = json.dumps([{"d": c["d"], "col": c["col"]} for c in WALL])
    return js('''
  tl.set("#gW", {autoAlpha: 1}, @ty);
  tl.fromTo("#roomW", {autoAlpha: 0}, {autoAlpha: 1, duration: 0.55, ease: "power1.inOut"}, @ty);
  var WA = %s;
  WA.forEach(function (w, n) {
    var t = 0.06 + w.d * 0.00046;
    tl.fromTo("#wa" + n, {autoAlpha: 0}, {autoAlpha: 1, duration: 0.3, ease: "power2.out"}, t);
    tl.fromTo("#wa" + n, {scale: 0.55, y: 40}, {scale: 1, y: 0, duration: 0.75, ease: SP, immediateRender: false}, t);
  });
  gsap.set("#wallW", {transformOrigin: "540px 250px"});
  tl.fromTo("#wallW", {scale: 1.06}, {scale: 1, duration: 1.4, ease: "power2.out"}, @ty+0.05);
  // «рілси» — they settle
  G.bump("#wallW", @rilsy);''' % cfg)


@beat
def b02_ai_edited():
    """«А їх монтував штучний інтелект.»

    NEAR over the wall. The Claude tile drops in above her head on «А їх
    монтував»; on «штучний» it sends a ripple and one light passes across the
    whole wall, every cell bumping as it reaches it. Then the wall falls away
    — «я випала з блогу» — and is gone before her matte ends (5.63)."""
    return js('''
  tl.set("#gW", {autoAlpha: 1}, @a1);
  arr("#clW", @a1-0.04, {s: 0.5, y: 30});
  G.inner("#clW .mk", @a1-0.04);
  // «штучний інтелект» — the light passes over everything it made
  G.ripple("#clWR", @shtuchnyi);
  G.sheen("#clW .sheen", @shtuchnyi+0.05);
  tl.set("#sweepW", {autoAlpha: 1}, @shtuchnyi);
  tl.fromTo("#sweepW", {x: -620}, {x: 1180, duration: 0.95, ease: "power1.inOut", immediateRender: false}, @shtuchnyi);
  tl.set("#sweepW", {autoAlpha: 0}, @shtuchnyi+0.96);
  WA.forEach(function (w, n) {
    var t = @shtuchnyi + 0.05 + w.d * 0.00042;
    tl.to("#wa" + n, {scale: 1.045, duration: 0.12, ease: "power2.out"}, t);
    tl.to("#wa" + n, {scale: 1, duration: 0.42, ease: SP}, t + 0.12);
  });
  // «я випала з блогу» — the wall falls out of the frame
  bout("#clW", @ya-0.14, 10, 0.24);
  WA.forEach(function (w, n) {
    tl.to("#wa" + n, {y: 260, rotation: (w.col < 2 ? -7 : 7), autoAlpha: 0, duration: 0.22, ease: "power2.in"},
          @ya-0.1 + w.col * 0.012);
  });
  tl.to("#roomW", {autoAlpha: 0, duration: 0.28, ease: "power1.inOut"}, @ya-0.14);
  tl.set("#gW", {autoAlpha: 0}, @ya+0.18);''')


# ============================================ B · the month, and after ==
# One dark-glass shelf above her head carries the calendar, then the real
# insights of her best reel, then a DM thread. Days start on a Monday.
CAL_X0, CAL_Y0, CAL_DX, CAL_DY, CAL_W, CAL_H = 112, 146, 124, 76, 112, 66
SERIES = {22: 8, 23: 7, 24: 6, 25: 5, 26: 4, 27: 3, 28: 2, 29: 1, 30: 0}   # day -> cell


def day_xy(d):
    r, c = (d - 1) // 7, (d - 1) % 7
    return CAL_X0 + c * CAL_DX, CAL_Y0 + r * CAL_DY


k.css("""
/* ---- b03-b06 · the dark shelf: calendar -> insights -> DMs ---- */
#pan { left: 70px; top: 70px; width: 940px; height: 476px; }
.wd { position: absolute; top: 102px; width: 112px; text-align: center; font-size: 22px; font-weight: 700;
  letter-spacing: 0.12em; color: rgba(255,255,255,0.46); }
.dc { position: absolute; width: 112px; height: 66px; border-radius: 16px;
  background: rgba(255,255,255,0.07); box-shadow: inset 0 0 0 2px rgba(255,255,255,0.13); }
.dc b { position: absolute; left: 12px; top: 7px; font-size: 22px; font-weight: 700; color: rgba(255,255,255,0.5); }
.dimg { position: absolute; width: 112px; height: 66px; border-radius: 16px; object-fit: cover;
  object-position: 50% 30%; box-shadow: 0 0 0 2px rgba(255,255,255,0.55), 0 12px 22px -10px rgba(10,0,4,0.7); }
#today { position: absolute; width: 112px; height: 66px; border-radius: 16px; border: 4px solid #ff6e9c;
  box-shadow: 0 0 18px rgba(255,110,156,0.65), inset 0 0 12px rgba(255,110,156,0.35); }

#insT { position: absolute; left: 106px; top: 106px; width: 227px; height: 404px; border-radius: 24px;
  object-fit: cover; box-shadow: 0 0 0 2px rgba(255,255,255,0.5), 0 26px 44px -18px rgba(10,0,4,0.75); }
#insE { position: absolute; left: 382px; top: 148px; width: 70px; height: 70px; }
#insN { position: absolute; left: 468px; top: 110px; font-size: 136px; font-weight: 900; line-height: 1.1;
  letter-spacing: -0.045em; color: rgba(255,255,255,0.9); white-space: nowrap; }
#insF { position: absolute; left: 872px; top: 150px; width: 104px; height: 62px; border-radius: 31px;
  background: rgba(255,255,255,0.13); box-shadow: inset 0 1.5px 1px rgba(255,255,255,0.3);
  display: flex; align-items: center; justify-content: center; }
#insF .sk { width: 40px; height: 40px; stroke: rgba(255,255,255,0.8); }
.ich { position: absolute; width: 290px; height: 78px; border-radius: 39px;
  background: rgba(255,255,255,0.10); box-shadow: inset 0 1.5px 1px rgba(255,255,255,0.28), inset 0 0 0 1px rgba(255,255,255,0.08); }
.ich .sk { position: absolute; left: 24px; top: 19px; width: 40px; height: 40px; stroke: #fff; }
.ich b { position: absolute; left: 82px; top: 10px; font-size: 46px; font-weight: 900; color: #fff;
  letter-spacing: -0.03em; line-height: 58px; }

.bub { position: absolute; height: 104px; }
.bub i { position: absolute; left: 34px; height: 20px; border-radius: 10px; display: block; }
.bub.in { background: linear-gradient(160deg, #ffffff 0%, #fbf3f6 100%); border-radius: 52px 52px 52px 16px;
  box-shadow: inset 0 -10px 20px -12px rgba(180,18,47,0.18), 0 22px 40px -18px rgba(10,0,4,0.6); }
.bub.in i { background: rgba(23,20,28,0.16); }
.bub.out { background: linear-gradient(165deg, #e0204b 0%, #ab112e 60%, #7a0a21 100%); border-radius: 52px 52px 16px 52px;
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.4), 0 22px 40px -18px rgba(10,0,4,0.6); }
.bub.out i { background: rgba(255,255,255,0.55); }
""")


def shelf_html():
    wd = "".join('<div class="wd" style="left:%dpx">%s</div>' % (CAL_X0 + i * CAL_DX, n)
                 for i, n in enumerate([u"ПН", u"ВТ", u"СР", u"ЧТ", u"ПТ", u"СБ", u"НД"]))
    cells = []
    for d in range(1, 31):
        x, y = day_xy(d)
        cells.append('<div class="dc" id="dc%d" style="left:%dpx;top:%dpx"><b>%d</b></div>' % (d, x, y, d))
    fills = "".join('<img class="dimg hide" id="df%d" src="%s" style="left:%dpx;top:%dpx" alt="">'
                    % ((d, CELL % c) + day_xy(d)) for d, c in sorted(SERIES.items()))
    x1, y1 = day_xy(1)
    chips = [("heart", 380, 330, "0"), ("save", 690, 330, "0"),
             ("send", 380, 424, "0"), ("follow", 690, 424, "+0")]
    chip_html = "".join(
        '<div class="ich hide" id="ich%d" style="left:%dpx;top:%dpx">%s<b id="ichV%d">%s</b></div>'
        % (i, x, y, stroke(ic, "sk"), i, v) for i, (ic, x, y, v) in enumerate(chips))

    def bub(bid, cls, x, y, w, bars):
        return ('<div class="bub %s hide" id="%s" style="left:%dpx;top:%dpx;width:%dpx">%s</div>'
                % (cls, bid, x, y, w, "".join('<i style="top:%dpx;width:%d%%"></i>' % (t, p)
                                             for t, p in bars)))
    return u'''
      <div class="g full" id="gS">
        <div id="pan" class="dglass edge hide"></div>
        <div id="cal" class="abs" style="left:0;top:0;width:1080px;height:600px">
          %(wd)s
          %(cells)s
          %(fills)s
          <div id="today" class="hide" style="left:%(x1)dpx;top:%(y1)dpx"></div>
        </div>
        <img id="insT" class="hide" src="%(best)s" alt="">
        <div id="insE" class="hide">%(eye)s</div>
        <div id="insN" class="hide">0</div>
        <div id="insF" class="hide">%(flat)s</div>
        %(chips)s
        %(up)s
        %(dm)s
        %(b1)s%(b2)s%(b3)s
      </div>''' % {
        "wd": wd, "cells": "\n          ".join(cells), "fills": fills, "x1": x1, "y1": y1,
        "best": CELL % 3, "eye": stroke("eye", "sk w"), "flat": stroke("flat", "sk"),
        "chips": chip_html,
        "up": hidden(tile("insU", 74, 936, 290, "jelly", stroke("up"), "circ", ring=False)),
        "dm": hidden(tile("dmT", 170, 118, 150, "jelly", stroke("send"))),
        "b1": bub("bu1", "in", 336, 104, 450, [(26, 78), (58, 46)]),
        "b2": bub("bu2", "out", 604, 226, 370, [(26, 72), (58, 40)]),
        "b3": bub("bu3", "in", 336, 348, 500, [(26, 84), (58, 58)]),
    }


L["near"].append(shelf_html())


@beat
def b03_month_empty():
    """«я випала з блогу на цілий місяць,»

    NEAR. The dark glass shelf lands above her head as the wall falls, and it
    is a month: weekdays, thirty numbered days, every one of them empty. On
    «на цілий місяць» a "today" ring races through them — day after day,
    nothing in any of them."""
    steps = []
    for i, d in enumerate(range(2, 22)):
        x, y = day_xy(d)
        x1, y1 = day_xy(1)
        steps.append('tl.set("#today", {x: %d, y: %d}, %.3f);' % (x - x1, y - y1, T["na"] + 0.08 + i * 0.052))
    return js('''
  tl.set("#gS", {autoAlpha: 1}, @ya);
  bin("#pan", @ya, 14, 0.42);
  tl.fromTo("#pan", {scale: 0.9, y: 30}, {scale: 1, y: 0, duration: 0.9, ease: SP}, @ya);
  tl.fromTo("#cal .wd", {autoAlpha: 0, y: 10}, {autoAlpha: 1, y: 0, duration: 0.4, ease: SP, stagger: 0.03}, @vypala);
  tl.fromTo("#cal .dc", {autoAlpha: 0, scale: 0.6}, {autoAlpha: 1, scale: 1, duration: 0.45, ease: SP, stagger: 0.012}, @vypala+0.06);
  // «на цілий місяць» — a whole month goes by, empty
  tl.fromTo("#today", {autoAlpha: 0, scale: 1.3}, {autoAlpha: 1, scale: 1, duration: 0.25, ease: "power2.out"}, @na);
  ''' + "\n  ".join(steps))


@beat
def b04_series():
    """«а потім запостила серію рілсів.»

    The last nine days fill with the series, one reel a day, in a quick run
    — the real cells, oldest first — and the ring walks on with them."""
    fills = []
    for i, d in enumerate(range(22, 31)):
        x, y = day_xy(d)
        x1, y1 = day_xy(1)
        t = T["zapostyla"] + i * 0.115
        fills.append('tl.set("#today", {x: %d, y: %d}, %.3f);' % (x - x1, y - y1, t))
        fills.append('tl.fromTo("#df%d", {autoAlpha: 0, scale: 1.6}, {autoAlpha: 1, scale: 1, duration: 0.42, '
                     'ease: POP}, %.3f);' % (d, t))
    return js('''
  tl.set("#gS", {autoAlpha: 1}, @a2);
  ''' + "\n  ".join(fills) + '''
  // «рілсів» — the run lands
  G.bump("#cal", @rilsiv);
  tl.to("#today", {autoAlpha: 0, duration: 0.3}, @rilsiv+0.2);''')


@beat
def b05_views():
    """«І хоч з самого початку перегляди були не супер,»

    The calendar clears, and day 27 — her best reel of the series — lifts out
    into its real insights (her screenshot): an eye and 2 799, counting up
    and stalling, with a flat-trend chip on «не супер». Honest: this is her
    best one."""
    x27, y27 = day_xy(27)
    # #insT is 227x404 at (106,106); start it over day 27's cell
    sx = (x27 + CAL_W / 2.0) - (106 + 227 / 2.0)
    sy = (y27 + CAL_H / 2.0) - (106 + 404 / 2.0)
    return js('''
  tl.set("#gS", {autoAlpha: 1}, @ikhoch);
  bout(["#cal .wd", "#cal .dc"], @ikhoch-0.04, 10, 0.3);
  tl.to("#cal .dimg:not(#df27)", {autoAlpha: 0, scale: 0.7, duration: 0.28, ease: "power2.in"}, @ikhoch-0.04);
  tl.set("#df27", {autoAlpha: 0}, @ikhoch+0.1);
  tl.set("#insT", {autoAlpha: 1}, @ikhoch+0.1);
  tl.fromTo("#insT", {x: %.1f, y: %.1f, scale: 0.3}, {x: 0, y: 0, scale: 1, duration: 0.85, ease: SOFT,
            immediateRender: false}, @ikhoch+0.1);
  // «перегляди»
  arr("#insE", @perehliady-0.08, {s: 0.5, y: 0});
  bin("#insN", @perehliady, 10, 0.3);
  G.count("#insN", @perehliady, 2799, 1.3, function (v) {
    v = Math.round(v); return v >= 1000 ? Math.floor(v / 1000) + "\\u00a0" + ("00" + (v %% 1000)).slice(-3) : "" + v; });
  // «не супер» — flat
  arr("#insF", @ne-0.04, {s: 0.5, x: -20, y: 0});''' % (sx, sy))


@beat
def b06_activity():
    """«але активність в акаунті піднялась,»

    The views step back; the same reel's activity counts up from her
    insights — 43 likes, 37 saves, 7 shares, +6 follows — and an up badge
    lands on «піднялась»."""
    return js('''
  tl.set("#gS", {autoAlpha: 1}, @ale);
  tl.to(["#insE", "#insN", "#insF"], {autoAlpha: 0.38, duration: 0.35, ease: "power1.out"}, @ale);
  [0, 1, 2, 3].forEach(function (i) {
    arr("#ich" + i, @aktyvnist-0.06 + i * 0.07, {s: 0.6, y: 18});
  });
  G.count("#ichV0", @aktyvnist+0.05, 43, 0.9);
  G.count("#ichV1", @aktyvnist+0.12, 37, 0.9);
  G.count("#ichV2", @aktyvnist+0.19, 7, 0.8);
  G.count("#ichV3", @aktyvnist+0.26, 6, 0.8, function (v) { return "+" + Math.round(v); });
  // «піднялась»
  arr("#insU", @pidnialas-0.04, {s: 0.3, y: 20});
  G.inner("#insU .sk", @pidnialas-0.04);
  tl.to(".ich b", {color: "#ffc2d4", duration: 0.3, stagger: 0.05}, @pidnialas);
  G.bump([".ich"], @pidnialas+0.1);''')


@beat
def b06b_dms():
    """«розмови в директі пішли,»

    The numbers clear and the shelf turns into Direct: the paper-plane tile
    lands where the reel was, and a conversation starts — in, out, in — the
    last bubble landing on «пішли». Then the shelf's frost spreads into the
    room for b07."""
    return js('''
  tl.set("#gS", {autoAlpha: 1}, @rozmovy);
  bout(["#insE", "#insN", "#insF", ".ich", "#insU"], @rozmovy-0.06, 10, 0.28);
  tl.to("#insT", {x: -40, scale: 0.8, autoAlpha: 0, duration: 0.3, ease: "power2.in"}, @rozmovy-0.06);
  arr("#dmT", @rozmovy+0.1, {s: 0.5, y: 20});
  G.inner("#dmT .sk", @rozmovy+0.1);
  // «в директі пішли» — in, out, in
  arr("#bu1", @vdirekti, {s: 0.6, x: -40, y: 20, d: 0.7});
  arr("#bu2", @vdirekti+0.3, {s: 0.6, x: 40, y: 20, d: 0.7});
  arr("#bu3", @pishly, {s: 0.6, x: -40, y: 20, d: 0.7});
  G.ripple("#dmTR", @pishly+0.05);
  G.haptic("#bu3", @pishly+0.45);
  // «і головне» — out, and the frost spreads into the room
  bout(["#dmT", "#bu1", "#bu2", "#bu3"], @i1-0.04, 10, 0.24);
  tl.to("#pan", {scale: 1.3, duration: 0.34, ease: "power2.in"}, @i1-0.02);
  bout("#pan", @i1, 16, 0.3);
  tl.set("#gS", {autoAlpha: 0}, @i1+0.32);''')


# ====================================== C · out of Drafts, onto the wall ==
FOLD = dict(x=300, y=150, w=480, h=380)          # the back plate
FLY_SLOTS = [(50, 70), (800, 70), (50, 499), (800, 499), (50, 928), (800, 928)]
FLY_SRC = [0, 1, 2, 3, 4, 5]
FLY_FROM = (540, 330)                            # centre, inside the pocket

k.css("""
/* ---- b07 · the Drafts folder behind her ---- */
.fb { position: absolute;
  background: linear-gradient(165deg, rgba(255,255,255,0.66) 0%, rgba(255,241,246,0.46) 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.8), 0 40px 80px -30px rgba(20,2,8,0.55); }
#fTab { left: 300px; top: 112px; width: 196px; height: 64px; border-radius: 26px 26px 0 0; }
#fBk { left: 300px; top: 150px; width: 480px; height: 380px; border-radius: 0 38px 38px 38px; }
#fFr { position: absolute; left: 286px; top: 292px; width: 508px; height: 256px; border-radius: 36px;
  background: linear-gradient(168deg, rgba(255,255,255,0.93) 0%, rgba(253,238,243,0.84) 100%);
  box-shadow: inset 0 2.5px 1px #fff, inset 0 -24px 40px -22px rgba(180,18,47,0.16),
              0 -10px 30px -12px rgba(20,2,8,0.25), 0 44px 80px -30px rgba(20,2,8,0.55);
  display: flex; align-items: center; justify-content: center; }
#fFr span { font-size: 46px; font-weight: 900; letter-spacing: 0.08em; color: #8d0d24; }
.pk { position: absolute; width: 130px; height: 231px; border-radius: 16px; object-fit: cover;
  box-shadow: 0 0 0 2px rgba(255,255,255,0.6), 0 16px 30px -12px rgba(20,2,8,0.5); }
.fly { position: absolute; width: 230px; height: 409px; }
.fly img { position: absolute; inset: 0; width: 230px; height: 409px; border-radius: 22px; object-fit: cover;
  box-shadow: 0 0 0 2px rgba(255,255,255,0.3), 0 34px 56px -22px rgba(12,0,5,0.7); }
""")


@beat
def b07_out_of_drafts():
    """«і головне — контент реально вийшов, а не завис у мене в чернетках, і
    вмер там, як завжди.»

    BEHIND, matted, the room soft. A Drafts folder stands behind her head
    with greyed reels peeking out of it. On «контент реально вийшов» six
    reels climb out of it one by one, colour coming back as they fly, and
    land on the wall around her — the wall from the opening. The folder
    bumps on «в чернетках» (the caption drops for the one word: the folder
    says it); on «вмер там» the last grey draft keels over and sinks into
    the pocket. Clear before her 20.10 cut."""
    f0, n = MATTES["drafts"]
    flyers = []
    cfg = []
    for i, ((sx, sy), src) in enumerate(zip(FLY_SLOTS, FLY_SRC)):
        flyers.append('<div class="fly hide" id="fl%d" style="left:%dpx;top:%dpx">'
                      '<img src="%s" alt=""><img class="flc" src="%s" alt=""></div>'
                      % (i, sx, sy, GREY % src, CELL % src))
        cfg.append({"x": round(FLY_FROM[0] - (sx + 115), 1), "y": round(FLY_FROM[1] - (sy + 204.5), 1)})
    L["behind"].append(u'''
      <div class="g full" id="gD">
        <div id="roomD" class="hide">
          <video id="softD" class="plate" src="assets/soft/drafts.mp4"
                 data-start="%.3f" data-duration="%.3f" data-media-start="0" muted playsinline></video>
          <div class="roomTint"></div>
        </div>
        <div id="fold" class="abs hide" style="left:0;top:0;width:1080px;height:600px">
          <div class="fb" id="fTab"></div><div class="fb" id="fBk"></div>
          <img class="pk" id="pk0" src="%s" style="left:352px;top:214px;transform:rotate(-8deg)" alt="">
          <img class="pk" id="pk1" src="%s" style="left:598px;top:208px;transform:rotate(7deg)" alt="">
          %s
          <div id="fFr"><span>ЧЕРНЕТКИ</span></div>
        </div>
      </div>''' % (f0 / 30.0, n / 30.0, GREY % 7, GREY % 6, "\n          ".join(flyers)))
    return js('''
  tl.set("#gD", {autoAlpha: 1}, @i1);
  tl.fromTo("#roomD", {autoAlpha: 0}, {autoAlpha: 1, duration: 0.6, ease: "power1.inOut"}, @i1+0.04);
  gsap.set("#fold", {transformOrigin: "540px 340px"});
  bin("#fold", @holovne-0.04, 14, 0.4);
  tl.fromTo("#fold", {scale: 0.7, y: 40}, {scale: 1, y: 0, duration: 0.85, ease: SP}, @holovne-0.04);
  // «контент реально вийшов» — out of Drafts, colour back, onto the wall
  var FL = %s;
  FL.forEach(function (f, i) {
    var t = @kontent + i * 0.2, s = "#fl" + i;
    gsap.set(s + " .flc", {autoAlpha: 0});
    tl.set(s, {autoAlpha: 1}, t);
    tl.fromTo(s, {x: f.x, y: f.y + 60, scale: 0.46}, {x: f.x, y: f.y - 150, scale: 0.5, duration: 0.24,
              ease: "power2.out", immediateRender: false}, t);
    tl.to(s, {x: 0, y: 0, scale: 1, rotation: 0, duration: 0.62, ease: SP}, t + 0.24);
    tl.to(s + " .flc", {autoAlpha: 1, duration: 0.4, ease: "power1.inOut"}, t + 0.2);
  });
  G.bump("#fFr", @kontent+0.02);
  // «а не завис у мене в чернетках»
  G.bump(["#fTab", "#fBk", "#fFr", ".pk"], @chernetkakh-0.02);
  // «і вмер там» — the one left inside keels over and sinks
  tl.to("#pk0", {rotation: -34, x: 26, y: 96, autoAlpha: 0, duration: 0.62, ease: "power2.in"}, @vmer);
  // «як завжди» — clear before her cut at 20.10
  tl.to(".fly", {autoAlpha: 0, scale: 0.9, duration: 0.28, ease: "power2.in"}, @zavzhdy-0.08);
  bout("#fold", @zavzhdy-0.06, 12, 0.28);
  tl.to("#roomD", {autoAlpha: 0, duration: 0.36, ease: "power1.inOut"}, @zavzhdy-0.06);
  tl.set("#gD", {autoAlpha: 0}, 20.05);''' % json.dumps(cfg))


# =========================================== D · how AI output looks ==
FMT = [  # id, kind, centre x, w, h, label
    ("fmV", "slV", 380, 164, 292, u"МОНТАЖ", "imontazh"),
    ("fmD", "slD", 612, 236, 236, u"ДИЗАЙН", "dyzain"),
    ("fmC", "slC", 862, 206, 275, u"КАРУСЕЛІ", "karuseli"),
]
FMT_CY = 318
CL2 = (180, 318)          # the Claude tile's centre in b09a: the shelf's left end

k.css("""
/* ---- b09a · three formats, one look ---- */
#shA { left: 70px; top: 96px; width: 940px; height: 456px; }
.fmt { position: absolute; }
.fmt .slop { left: 0; top: 0; }
.fplay { position: absolute; left: 50%; top: 46%; width: 62px; height: 62px; margin: -31px 0 0 -31px;
  border-radius: 50%; background: rgba(255,255,255,0.92); box-shadow: 0 0 22px 4px rgba(255,43,214,0.8); }
.fplay:after { content: ""; position: absolute; left: 24px; top: 18px; border-left: 20px solid #8a2bff;
  border-top: 13px solid transparent; border-bottom: 13px solid transparent; }
.fbar { position: absolute; left: 12px; right: 12px; bottom: 14px; height: 7px; border-radius: 4px;
  background: rgba(255,255,255,0.45); }
.fbar i { position: absolute; left: 0; top: 0; bottom: 0; width: 38%; border-radius: 4px; background: #fff22b; }
.fdots { position: absolute; left: 0; right: 0; bottom: 12px; display: flex; justify-content: center; gap: 7px; }
.fdots i { width: 9px; height: 9px; border-radius: 50%; background: rgba(255,255,255,0.55); display: block; }
.fdots i:first-child { background: #fff; }
.fchip { position: absolute; width: 210px; height: 52px; border-radius: 26px; text-align: center;
  background: linear-gradient(160deg, #ffffff 0%, #fff5f8 52%, #f5dfe6 100%);
  box-shadow: inset 0 2px 1px #fff, 0 18px 34px -14px rgba(30,4,12,0.6);
  font-size: 26px; font-weight: 700; letter-spacing: 0.1em; color: #17141c; line-height: 52px; white-space: nowrap; }
""")


def formats_html():
    parts = []
    for fid, sid, cx, w, h, lab, _ in FMT:
        extra = ""
        if fid == "fmV":
            extra = '<div class="fplay"></div><div class="fbar"><i></i></div>'
        elif fid == "fmC":
            extra = '<div class="fdots"><i></i><i></i><i></i><i></i><i></i></div>'
        parts.append('<div class="fmt hide" id="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">%s%s</div>'
                     % (fid, cx - w // 2, FMT_CY - h // 2, w, h, slop.slide(sid, w, h), extra))
        parts.append('<div class="fchip hide" id="%sL" style="left:%dpx;top:%dpx">%s</div>'
                     % (fid, cx - 105, FMT_CY + h // 2 - 22, lab))
    return u'''
      <div class="g full" id="gA">
        <div id="shA" class="shelf edge hide"></div>
        %s
        %s
      </div>''' % (hidden(tile("clA", 150, CL2[0] - 75, CL2[1] - 75, "jelly", g.mark("claude"))),
                   "\n        ".join(parts))


L["near"].append(formats_html())


@beat
def b09a_three_formats():
    """«Бо ми всі звикли, що коли щось робить штучний інтелект — і монтаж, і
    дизайн, і каруселі — воно виглядає типово.»

    NEAR. The glass shelf and the Claude tile land on «робить штучний
    інтелект»; out of the tile, on each word, the typical AI output in its
    format — a video (play button, scrubber), a design, a carousel (dots) —
    all three the same garish slop. Pearl chips name them, so the captions
    drop for «і монтаж, і дизайн, і каруселі». On «виглядає» all three do the
    same wobble: typical. Gone before her closeup at 31.10."""
    lines = []
    for fid, sid, cx, w, h, lab, word in FMT:
        dx, dy = CL2[0] - cx, CL2[1] - FMT_CY
        lines.append('tl.set("#%s", {autoAlpha: 1}, @%s);' % (fid, word))
        lines.append('tl.fromTo("#%s", {x: %d, y: %d, scale: 0.2}, {x: 0, y: 0, scale: 1, duration: 0.8, '
                     'ease: POP, immediateRender: false}, @%s);' % (fid, dx, dy, word))
        lines.append('G.bump("#clA", @%s-0.04);' % word)
        lines.append('arr("#%sL", @%s+0.16, {s: 0.5, y: 10});' % (fid, word))
    return js('''
  tl.set("#gA", {autoAlpha: 1}, @robyt);
  bin("#shA", @robyt, 14, 0.42);
  tl.fromTo("#shA", {scale: 0.9, y: 30}, {scale: 1, y: 0, duration: 0.9, ease: SP}, @robyt);
  arr("#clA", @shtuchnyi2-0.08, {s: 0.5, y: 30});
  G.inner("#clA .mk", @shtuchnyi2-0.08);
  G.sheen("#clA .sheen", @shtuchnyi2+0.3);
  ''' + "\n  ".join(lines) + '''
  // «виглядає» — typical: the same wobble, all three at once
  tl.to([".fmt"], {keyframes: {rotation: [0, -5, 4, -2, 0]}, duration: 0.42, ease: "none"}, @vyhliadaie);
  tl.to([".fchip"], {keyframes: {rotation: [0, -5, 4, -2, 0]}, duration: 0.42, ease: "none"}, @vyhliadaie);
  // out before the closeup
  bout(["#shA", "#clA", ".fmt", ".fchip"], 30.88, 10, 0.18);
  tl.set("#gA", {autoAlpha: 0}, 31.08);''')


# ============================================ E · the slop, cleaned ==
SHEET = dict(x=140, y=150, w=800, h=1066)
SLOP_S = SHEET["w"] / 1440.0                     # full-bleed slide -> sheet
SLOP_T = [   # native 1080x1440 coords, shown x1.333 from x -180: native 135-945 is on screen
    ("sparkw", 330, 190, 130, 0), ("spark", 790, 900, 150, 0), ("sparkc", 250, 1010, 120, 0),
    ("rocket", 190, 540, 320, -18), ("bubble", 830, 420, 340, 10), ("crown", 560, 110, 270, -6),
    ("flame", 860, 1140, 290, 12), ("tag", 260, 1320, 270, -14), ("star", 900, 720, 240, 16),
    ("heart", 430, 1060, 210, -10), ("arrow", 700, 1370, 300, -8), ("burst", 160, 330, 250, -16),
]
ORB = 170
ORB_FULL = (760, 300)                            # frame centre while it is full-frame
ORB_SHEET = (SHEET["x"] + SHEET["w"] - 26, SHEET["y"] + 30)   # on the sheet's corner

k.css("""
/* ---- b09-b11 · the takeover: slop -> clean sheet -> 90/10 ---- */
#tk { position: absolute; inset: 0; clip-path: circle(0px at 830px 386px); }
#slT { left: -180px; top: 0; transform-origin: 0 0; }
#clean { left: 140px; top: 150px; width: 800px; height: 1066px; }
#clean .sx { position: absolute; }
#csMicro, #nbMicro { color: rgba(23,20,28,0.58); }
#csMicro { left: 64px; top: 70px; }
#csBig { left: 52px; top: 118px; font-size: 300px !important; }
#csTitle { left: 64px; top: 452px; width: 660px; font-size: 66px; font-weight: 700; line-height: 1.08;
  letter-spacing: -0.025em; color: #17141c; }
#csSub { left: 64px; top: 626px; width: 640px; font-size: 30px; font-weight: 500; line-height: 1.35;
  color: rgba(23,20,28,0.5); }
#csHair { left: 64px; right: 64px; top: 760px; }
#csDots { left: 64px; top: 946px; display: flex; gap: 12px; }
#csDots i { width: 14px; height: 14px; border-radius: 50%; background: rgba(23,20,28,0.14); display: block; }
#csDots i:first-child { background: #b4122f; width: 34px; border-radius: 7px; }
#csNext { right: 64px; top: 926px; }
#csNext svg { width: 26px; height: 26px; fill: none; stroke: #b4122f; stroke-width: 3; stroke-linecap: round;
  stroke-linejoin: round; }

#nbMicro { left: 64px; top: 70px; }
#nbBig { left: 52px; top: 112px; }
#nbBar { left: 64px; top: 360px; width: 672px; height: 104px; }
#nbA { position: absolute; left: 0; top: 0; width: 600px; height: 104px; border-radius: 34px 12px 12px 34px;
  transform-origin: 0 50%;
  background: linear-gradient(118deg, #7e0b20 0%, #b4122f 55%, #d8264f 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.45), inset 0 -18px 30px -16px rgba(255,125,165,0.5); }
#nbB { position: absolute; left: 608px; top: 0; width: 64px; height: 104px; border-radius: 12px 34px 34px 12px;
  transform-origin: 0 50%;
  background: linear-gradient(160deg, #ff8ab0 0%, #ff5c8f 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.6); }
#nbTrk { position: absolute; inset: 0; border-radius: 34px; background: #f6e6eb;
  box-shadow: inset 0 2px 6px rgba(120,10,30,0.08); }
.nrow { position: absolute; left: 64px; right: 64px; height: 110px; display: flex; align-items: center; }
.nrow .ri { width: 76px; height: 76px; border-radius: 22px; display: flex; align-items: center;
  justify-content: center; margin-right: 26px; flex: none; }
.nrow .ri.a { background: linear-gradient(118deg, #7e0b20 0%, #b4122f 55%, #d8264f 100%); }
.nrow .ri.b { background: linear-gradient(160deg, #ff8ab0 0%, #ff5c8f 100%); }
.nrow .ri svg { width: 42px; height: 42px; fill: none; stroke: #fff; stroke-width: 2.4; stroke-linecap: round;
  stroke-linejoin: round; }
.nrow .rl { flex: 1; font-size: 36px; font-weight: 700; letter-spacing: 0.1em; color: #17141c; }
.nrow .rv { font-size: 52px; font-weight: 900; letter-spacing: -0.03em; color: #17141c; }
#nrl { position: absolute; left: 166px; right: 64px; top: 718px; height: 2px; background: rgba(23,20,28,0.07); }
#nbOk .sk { width: 56%; height: 56%; }
""")

NEXT_ARROW = '<svg viewBox="0 0 26 26"><path d="M4 13h17M15 7l6 6-6 6"/></svg>'


def tk_html():
    orb = Slop.sticker("orb", 0, 0, ORB, 0)
    clean = u'''
          <div class="sheet hide" id="clean">
            <div id="csA">
              <div class="sx t-micro" id="csMicro">КАРУСЕЛЬ · 1 / 10</div>
              <div class="sx t-big" id="csBig">10</div>
              <div class="sx" id="csTitle">порад для ідеальних каруселей</div>
              <div class="sx" id="csSub">Структура, шрифт і відступи — без зайвого</div>
              <div class="sx hair" id="csHair"></div>
              <div class="sx" id="csDots"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div>
              <div class="sx chip" id="csNext"><span>Гортай</span>%(arrow)s</div>
            </div>
            <div id="csB">
              <div class="sx t-micro hide" id="nbMicro">РОБОТА З ШІ</div>
              <div class="sx t-big hide" id="nbBig">0%%</div>
              <div class="sx hide" id="nbBar"><div id="nbTrk"></div><div id="nbA"></div><div id="nbB"></div></div>
              <div class="nrow hide" id="nr1" style="top:548px"><div class="ri a">%(spark)s</div>
                <div class="rl">НАВЧАННЯ</div><div class="rv" id="nv1">90%%</div></div>
              <div id="nrl" class="hide"></div>
              <div class="nrow hide" id="nr2" style="top:724px"><div class="ri b">%(check)s</div>
                <div class="rl">ПЕРЕВІРКА</div><div class="rv" id="nv2">10%%</div></div>
              %(ok)s
            </div>
            <div class="sheen"></div>
          </div>''' % {"arrow": NEXT_ARROW,
                       "spark": '<svg viewBox="0 0 24 24">%s</svg>' % STROKES["spark"],
                       "check": '<svg viewBox="0 0 24 24">%s</svg>' % STROKES["eye"],
                       "ok": hidden(tile("nbOk", 88, 660, 316, "jelly", stroke("check"), "circ"))}
    return u'''
      <div id="tk" class="hide">
        <div class="tkg"></div><div class="aur a1"></div><div class="aur a2"></div><div class="aur a3"></div>
        <div class="grain"></div>
        <div class="g full" id="gT">
          %(clean)s
          %(slop)s
          <div class="tw hide" id="orbW" style="left:%(ox)dpx;top:%(oy)dpx;width:%(o)dpx;height:%(o)dpx">
            <div class="slop" data-layout-ignore style="width:%(o)dpx;height:%(o)dpx">%(orb)s</div></div>
        </div>
      </div>''' % {"clean": clean, "slop": slop.slide("slT", 1440, extra=SLOP_T),
                   "ox": ORB_FULL[0] - ORB // 2, "oy": ORB_FULL[1] - ORB // 2, "o": ORB, "orb": orb}


L["tk"].append(tk_html())


@beat
def b09_slop():
    """«Ось цей стиль штучного інтелекту, де все підсвічене, купа кольорів,
    все напічкане елементами.»

    OVER. Out of the closeup, the iris opens out of where the carousel sat
    into the slop at full frame — rainbow, sunburst, extruded title, garbled
    copy. Built up on the words: sparkles on «підсвічене», the whole thing
    spins through the colour wheel on «кольорів», and on «напічкане
    елементами» nine stickers slap on and spill off the edges; the last one
    is a purple «AI» orb."""
    return js('''
  tl.set("#gT", {autoAlpha: 1}, @os);
  G.irisOpen("#tk", @os, 830, 386, 0.85);
  G.drift("#tk", @os, 20);
  // «підсвічене» — it lights up
  slopPop(tl, "slT", @pidsvichene, 0.12, 0, 3);
  G.bump(["#slT .sl-pill", "#slT .sl-btn"], @pidsvichene+0.1);
  // «купа кольорів» — every colour at once
  tl.fromTo("#slT .sl-art", {filter: "hue-rotate(0deg)"}, {filter: "hue-rotate(360deg)", duration: 0.95,
            ease: "power1.inOut", immediateRender: false}, @koloriv);
  tl.set("#slT .sl-art", {filter: "none"}, @koloriv+0.97);
  // «напічкане елементами»
  slopPop(tl, "slT", @napichkane, 0.1, 3, 12);
  tl.set("#orbW", {autoAlpha: 1}, @elementamy+0.3);
  tl.fromTo("#orbW .stk", {scale: 2.1, rotation: -28}, {scale: 1, rotation: 0, duration: 0.5, ease: POP,
            immediateRender: false}, @elementamy+0.3);''')


@beat
def b10_cleaned():
    """«Так от, насправді, якщо його правильно навчити, він може робити
    нормально, без цього стилю AI-слоп.»

    The thesis. «правильно навчити»: the stickers are knocked off; the slide
    shrinks from full frame onto the burgundy ground and its colour drains
    into the clean white sheet under it — the same slide, done properly.
    Sheen on «нормально». One «AI» orb stayed stuck on its corner; on
    «AI-слоп» it is flicked off."""
    ox = ORB_SHEET[0] - ORB_FULL[0]
    oy = ORB_SHEET[1] - ORB_FULL[1]
    return js('''
  tl.set("#gT", {autoAlpha: 1}, @tak);
  // «правильно навчити» — knocked off
  slopShed(tl, "slT", @pravylno);
  tl.to("#slT", {x: %.1f, y: %.1f, scale: %.5f, duration: 0.8, ease: SOFT}, @navchyty);
  tl.to("#orbW", {x: %.1f, y: %.1f, scale: 0.72, rotation: 12, duration: 0.8, ease: SOFT}, @navchyty);
  tl.set("#clean", {autoAlpha: 1}, @navchyty+0.3);
  // «може робити нормально» — the colour drains out of it
  tl.to("#slT", {autoAlpha: 0, duration: 0.6, ease: "power1.inOut"}, @mozhe);
  tl.fromTo(["#csMicro", "#csBig", "#csTitle", "#csSub"], {autoAlpha: 0, y: 18},
            {autoAlpha: 1, y: 0, duration: 0.55, ease: SP, stagger: 0.07, immediateRender: false}, @mozhe+0.2);
  tl.fromTo("#csHair", {scaleX: 0}, {scaleX: 1, duration: 0.6, ease: "power3.out", immediateRender: false}, @mozhe+0.4);
  tl.fromTo(["#csDots", "#csNext"], {autoAlpha: 0, y: 12}, {autoAlpha: 1, y: 0, duration: 0.5, ease: SP,
            stagger: 0.06, immediateRender: false}, @mozhe+0.5);
  shn("#clean > .sheen", @normalno);
  // «AI-слоп» — the last sticker goes
  tl.to("#orbW", {x: %.1f, y: %.1f, rotation: 200, scale: 0.6, duration: 0.7, ease: "power2.in"}, @slop+0.02);
  tl.to("#orbW", {autoAlpha: 0, duration: 0.2}, @slop+0.55);
  G.bump("#clean", @slop+0.08);''' % (
        SHEET["x"] + 180, SHEET["y"], SLOP_S, ox, oy, ox + 260, oy + 820))


@beat
def b11_ninety_ten():
    """«Погана новина — це «правильно навчити» і є 90% всієї роботи. Останні
    10% — це просто перевірити, що він зробив як треба.»

    The same sheet delivers the bad news: a haptic shake on «Погана», the
    slide clears, and two rows are laid out — НАВЧАННЯ, ПЕРЕВІРКА — before
    she names them. «90%»: the bar fills to 90 and the big number counts to
    it; «10%»: the pink sliver clicks in. Captions drop on those two words:
    the sheet says them. «зробив як треба»: the 10 % gets its tick."""
    return js('''
  tl.set("#gT", {autoAlpha: 1}, @pohana);
  G.haptic("#clean", @pohana);
  bout("#csA > *", @pohana+0.08, 10, 0.3);
  bin("#nbMicro", @novyna, 8, 0.3);
  bin("#nbBar", @novyna+0.05, 8, 0.3);
  gsap.set(["#nbA", "#nbB"], {scaleX: 0});
  tl.fromTo(["#nr1", "#nrl", "#nr2"], {autoAlpha: 0, y: 22}, {autoAlpha: 1, y: 0, duration: 0.55, ease: SP,
            stagger: 0.08, immediateRender: false}, @novyna+0.18);
  gsap.set(["#nv1", "#nv2"], {autoAlpha: 0});
  // «правильно навчити» — that row
  G.bump("#nr1", @pravylno2+0.1);
  // «90%»
  bin("#nbBig", @p90-0.04, 10, 0.3);
  G.count("#nbBig", @p90-0.04, 90, 0.8, function (v) { return Math.round(v) + "%"; });
  tl.to("#nbA", {scaleX: 1, duration: 0.8, ease: "power2.out"}, @p90-0.04);
  tl.fromTo("#nv1", {autoAlpha: 0, x: 16}, {autoAlpha: 1, x: 0, duration: 0.45, ease: SP, immediateRender: false}, @p90+0.3);
  // «10%»
  tl.to("#nbB", {scaleX: 1, duration: 0.45, ease: POP}, @p10-0.04);
  tl.fromTo("#nv2", {autoAlpha: 0, x: 16}, {autoAlpha: 1, x: 0, duration: 0.45, ease: SP, immediateRender: false}, @p10+0.05);
  G.bump("#nr2", @p10+0.05);
  // «перевірити, що він зробив як треба» — ticked
  G.bump("#nbB", @pereviryty);
  arr("#nbOk", @zrobyv-0.06, {s: 0.3, y: 0});
  G.inner("#nbOk .sk", @zrobyv-0.06);
  G.ripple("#nbOkR", @zrobyv+0.3);
  G.haptic("#clean", @yaktreba);
  // «Але способи є» — the sheet folds into the iris, which closes onto her
  tl.to("#clean", {scale: 0.55, duration: 0.5, ease: "power3.in"}, @ale2);
  G.irisClose("#tk", @ale2+0.02, 540, 760, 0.6);
  tl.set("#gT", {autoAlpha: 0}, @ale2+0.66);''')


# ================================================ F · ось результат ==
# The plate shrinks into the middle cell of a 3x3 grid of 356x633 cells with
# 6 px gutters (black, like her grid in dark mode) — 0.32963 of the frame, so
# the cell is the frame at a third. Her other reels are around it.
CELL_W, CELL_H, GUT = 356.0, 632.9, 6.0
S_CELL = CELL_W / 1080.0
GRID_SRC = [0, 1, 2,
            3, None, 4,
            5, 6, 7]
T_OUT0, T_OUT1 = T["tochno"], T["tochno"] + 1.24      # pull back
T_IN0, T_IN1 = T["napyshy"], T["napyshy"] + 0.76      # and in again

k.css("""
/* ---- b13 · this reel, one cell of her grid ---- */
#gridW { position: absolute; inset: 0; transform-origin: 540px 960px; }
.gc { position: absolute; width: 356px; height: 633px; object-fit: cover; }
#gRing { position: absolute; left: 362px; top: 643.5px; width: 356px; height: 633px;
  box-shadow: 0 0 0 5px #fff, 0 0 34px 8px rgba(255,110,156,0.75); }
""")


def grid_html():
    cells = []
    for i, src in enumerate(GRID_SRC):
        if src is None:
            continue
        x = (i % 3) * (CELL_W + GUT)
        y = (1920 - 3 * CELL_H - 2 * GUT) / 2.0 + (i // 3) * (CELL_H + GUT)
        cells.append('<img class="gc" id="gc%d" src="%s" style="left:%.1fpx;top:%.1fpx" alt="">'
                     % (i, CELL % src, x, y))
    return u'''
      <div class="g full" id="gG">
        <div id="gridW" data-layout-allow-overflow>
          %s
          <div id="gRing" class="hide"></div>
        </div>
      </div>''' % "\n          ".join(cells)


L["near"].append(grid_html())


@beat
def b13_result_grid():
    """«і вони точно працюють, бо ось результат.»

    NEAR, the payoff. From «точно» the camera pulls back: the whole frame —
    her, the room — shrinks into the middle cell of her Reels grid, her real
    reels (with their real view counts) around it, landing on «бо ось». On
    «результат» a lit ring finds this reel and the others step back. On
    «напиши» it scales back up to full frame."""
    s0 = push_at(T_OUT0)
    s1 = push_at(T_IN1)
    return js('''
  tl.set("#gG", {autoAlpha: 1}, @tochno);
  // pull back: the plate and the grid move as one camera
  tl.fromTo("#gridW", {scale: %.5f}, {scale: 1, duration: %.3f, ease: "power3.inOut", immediateRender: false}, @tochno);
  // «результат» — this one
  tl.fromTo("#gRing", {autoAlpha: 0, scale: 1.08}, {autoAlpha: 1, scale: 1, duration: 0.5, ease: SP,
            immediateRender: false}, @rezultat-0.06);
  tl.to(".gc", {opacity: 0.5, duration: 0.45, ease: "power1.out"}, @rezultat);
  // «напиши» — back in
  tl.to("#gRing", {autoAlpha: 0, duration: 0.2}, @napyshy-0.04);
  tl.to(".gc", {opacity: 1, duration: 0.2}, @napyshy-0.04);
  tl.to("#gridW", {scale: %.5f, duration: %.3f, ease: "power3.inOut"}, @napyshy);
  tl.set("#gG", {autoAlpha: 0}, %.3f);''' % (
        s0 / S_CELL, T_OUT1 - T_OUT0, s1 / S_CELL, T_IN1 - T_IN0, T_IN1 + 0.02))


# ======================================================= G · the poll ==
k.css("""
/* ---- b16 · the IG poll sticker ---- */
#poll { left: 170px; top: 104px; width: 740px; height: 392px; border-radius: 48px; overflow: hidden;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 60%, #fdf1f5 100%);
  box-shadow: inset 0 2px 1px #fff, inset 0 -24px 44px -26px rgba(180,18,47,0.16),
              0 50px 100px -36px rgba(20,2,8,0.7), 0 0 0 1px rgba(255,255,255,0.4); }
#pQ { position: absolute; left: 0; right: 0; top: 50px; text-align: center; font-size: 58px; font-weight: 900;
  letter-spacing: -0.02em; color: #17141c; }
.popt { position: absolute; top: 196px; width: 318px; height: 138px; border-radius: 69px; overflow: hidden;
  background: #f4edf0; box-shadow: inset 0 2px 5px rgba(120,10,30,0.07); }
.popt b { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center;
  font-size: 56px; font-weight: 900; letter-spacing: -0.01em; color: #17141c; }
#pNf { position: absolute; inset: 0; transform-origin: 0 50%;
  background: linear-gradient(118deg, #7e0b20 0%, #b4122f 55%, #e0204b 100%); }
#pNw { color: #fff !important; }
#pTap { position: absolute; left: 0; top: 0; width: 120px; height: 120px; margin: -60px 0 0 -60px; border-radius: 50%;
  background: rgba(255,255,255,0.35); box-shadow: 0 0 0 4px rgba(255,255,255,0.9), 0 10px 30px rgba(20,2,8,0.35); }
""")


def poll_html():
    return u'''
      <div class="g full" id="gP">
        <div id="poll" class="abs hide">
          <div id="pQ">Здогадалась би?</div>
          <div class="popt hide" id="pY" style="left:36px"><b>Так</b></div>
          <div class="popt hide" id="pN" style="left:386px"><div id="pNf"></div><b id="pNb">Ні</b><b id="pNw" class="hide">Ні</b></div>
          <div class="sheen"></div>
        </div>
        <div id="pTap" class="hide" style="left:715px;top:369px"></div>
      </div>'''


L["near"].append(poll_html())


@beat
def b16_poll():
    """«А тепер напиши в коментарях, чи ти здогадалась би, що цей рілс теж
    змонтований штучним інтелектом, якщо я б про це не сказала? Мені дуже
    цікаво побачити.»

    NEAR. An Instagram poll sticker lands above her head on «чи ти
    здогадалась би» with that question on it (the captions drop for those
    words), Так / Ні pop in on «що цей рілс», and on «не сказала» a tap lands
    on «Ні» and fills it. A bump on «цікаво», and it leaves before the end."""
    return js('''
  tl.set("#gP", {autoAlpha: 1}, @chy);
  gsap.set("#pNf", {scaleX: 0});
  arr("#poll", @chy-0.02, {s: 0.55, y: -20});
  G.inner("#pQ", @chy+0.05);
  // «що цей рілс» — the two answers
  arr("#pY", @shcho, {s: 0.5, y: 14, d: 0.7});
  arr("#pN", @shcho+0.12, {s: 0.5, y: 14, d: 0.7});
  // «не сказала» — a tap on «Ні»
  tl.fromTo("#pTap", {autoAlpha: 0, scale: 1.5}, {autoAlpha: 1, scale: 1, duration: 0.2, ease: "power2.out",
            immediateRender: false}, @ne2-0.08);
  tl.to("#pTap", {scale: 0.82, duration: 0.1, ease: "power2.in"}, @ne2+0.13);
  tl.to("#pN", {scale: 0.95, duration: 0.1, ease: "power2.in"}, @ne2+0.12);
  tl.to("#pN", {scale: 1, duration: 0.45, ease: POP}, @ne2+0.22);
  tl.to("#pNf", {scaleX: 1, duration: 0.42, ease: "power3.out"}, @ne2+0.2);
  tl.set("#pNw", {autoAlpha: 1}, @ne2+0.3);
  tl.set("#pNb", {autoAlpha: 0}, @ne2+0.3);
  tl.to("#pY", {autoAlpha: 0.45, duration: 0.3}, @ne2+0.25);
  tl.to("#pTap", {scale: 2.2, autoAlpha: 0, duration: 0.5, ease: "power2.out"}, @ne2+0.24);
  G.haptic("#poll", @skazala+0.1);
  // «цікаво»
  G.bump("#poll", @tsikavo);
  shn("#poll .sheen", @tsikavo+0.05);
  // «побачити» — gone before her closing closeup at 63.43
  tl.to("#poll", {y: -30, scale: 0.96, duration: 0.3, ease: "power2.in"}, @pobachyty+0.04);
  bout("#poll", @pobachyty+0.08, 10, 0.28);
  tl.set("#gP", {autoAlpha: 0}, @pobachyty+0.38);''')


# ================================================================ assemble ==
# Captions drop only on redundancy (STYLE.md §2b.1).
BLACKOUT = [
    (18.24, 18.70, "b07 — the folder reads ЧЕРНЕТКИ on «чернетках»"),
    (28.42, 30.40, "b09a — chips read МОНТАЖ / ДИЗАЙН / КАРУСЕЛІ on those words"),
    (46.06, 46.86, "b11 — the sheet reads 90% on «90%»"),
    (48.52, 49.27, "b11 — the sheet reads 10% on «10%»"),
    (56.90, 58.16, "b16 — the poll asks «Здогадалась би?» on «чи ти здогадалась би»"),
]
INVERT = []

HEAD_JS = r"""
  var G = helpers(tl);
  function bin(sel, t, b, d) { d = d || 0.38; G.blurIn(sel, t, b || 12, d); tl.set(sel, {filter: "none"}, t + d + 0.01); }
  function bout(sel, t, b, d) { d = d || 0.32; G.blurOut(sel, t, b || 10, d); tl.set(sel, {filter: "none"}, t + d + 0.01); }
  function arr(sel, t, o) {
    o = o || {};
    bin(sel, t, o.blur || 12, 0.36);
    tl.fromTo(sel, {scale: o.s == null ? 0.5 : o.s, x: o.x || 0, y: o.y == null ? 34 : o.y},
              {scale: 1, x: 0, y: 0, duration: o.d || 0.85, ease: o.ease || POP}, t);
  }
  function shn(sel, t) {
    gsap.set(sel, {xPercent: -120});
    tl.fromTo(sel, {xPercent: -120}, {xPercent: 120, duration: 0.8, ease: "power2.inOut", immediateRender: false}, t);
  }
  gsap.set(".sheen", {xPercent: -120});
  ["slV", "slD", "slC", "slT"].forEach(slopInit);
"""


def push_js():
    """§0.8's push, and the plate's own trip into the grid. The mattes and the
    behind layers take the plain push; the plate's is split around b13 so it
    can go down to a third and back without two tweens fighting over it."""
    o = '"%dpx %dpx"' % PUSH_O
    rest = json.dumps([".matte", "#gW", "#gD"])
    a, b, c, d = T_OUT0, T_OUT1, T_IN0, T_IN1
    return "\n".join([
        '  gsap.set(%s, {transformOrigin: %s});' % (json.dumps(["#vid", ".matte", "#gW", "#gD"]), o),
        '  tl.fromTo(%s, {scale: 1}, {scale: 1.045, duration: %.3f, ease: "none"}, 0);' % (rest, DUR),
        '  tl.fromTo("#vid", {scale: 1}, {scale: %.5f, duration: %.3f, ease: "none"}, 0);' % (push_at(a), a),
        '  tl.to("#vid", {scale: %.5f, duration: %.3f, ease: "power3.inOut"}, %.3f);' % (S_CELL, b - a, a),
        '  tl.to("#vid", {scale: %.5f, duration: %.3f, ease: "power3.inOut"}, %.3f);' % (push_at(d), d - c, c),
        '  tl.to("#vid", {scale: 1.045, duration: %.3f, ease: "none"}, %.3f);' % (DUR - d, d),
    ])


def main():
    gj = []
    for fn in BEATS:
        j = fn()
        gj.append("  /* %s */" % fn.__name__)
        gj.append(j.rstrip())
    gfx = "\n".join(L["behind"] + L["near"] + L["tk"])
    head = [g.js(), slop.js(), HEAD_JS, push_js()]
    doc = k.document(
        title=u"Reel 17 — рілси монтує ШІ",
        plate="assets/base.mp4",
        gfx_html=g.defs() + "\n" + slop.defs() + "\n" + gfx,
        gfx_js="\n".join(head + gj),
        caps=CAPS,
        blackout=BLACKOUT,
        invert=INVERT,
    )
    # Every blackout is a phrase inside a running sentence: dropping the
    # plaque for it reads as a blink. The captions go, the plaque stays.
    for a, b, _ in BLACKOUT:
        for line in ('  tl.to("#scrim", {autoAlpha: 0, duration: 0.20}, %.3f);\n' % (a - 0.20),
                     '  tl.to("#scrim", {autoAlpha: 1, duration: 0.25}, %.3f);\n' % b):
            assert line in doc, line
            doc = doc.replace(line, "", 1)

    out = os.path.join(HERE, "index.html")
    io.open(out, "w", encoding="utf-8").write(doc)
    print("index.html  %d captions, %d beats, %.1f KB"
          % (len(CAPS), len(BEATS), os.path.getsize(out) / 1024.0))


main()
