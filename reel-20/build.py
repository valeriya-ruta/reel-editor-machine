# -*- coding: utf-8 -*-
"""Reel 20 — «Пам'ятаєш… штучних двійників». Posts 2026-10-04.

Variant B, refined glass (STYLE.md §0). AI twins were over-hyped: don't take
yourself out of the filming, automate everything else.

The one object is **her** — two versions of her. The twin is built from her
own footage (her old Kling reel is gone): her matte (`her0`, shot 0) repeated,
greyed, a few frames out of sync with her. Early the clones crowd the room;
late the pipeline is a chain of tiles where every step is automated except the
last, and the last tile *is* her — the live plate.

The chain, behind -> near -> over -> near -> over -> near -> over -> near:
    she splits into grey clones behind her; «AI» tags; they step forward; the
    room behind all of them turns into a beach, mountains, a city -> (cut) a
    Kling tile on the shelf, a twin reel jumps out of it, two more fan out ->
    the reels collapse into the peak of a views chart that spikes and goes
    flat; a flame on «нахайпили», a tick on «ти права», avatars jump onto the
    spike -> the iris opens out of the peak: ДВІЙНИК vs ТИ -> (her closeup) ->
    the same sheet: the twin's bars long, hers short; window, teleprompter,
    REC land on her -> the iris closes onto her portrait, which becomes a reel
    card above her head: she is erased out of it, a grey twin drops in, the
    world behind it swaps; €€€ and a checklist -> the iris opens out of the
    card: the twin's face at full size, a magnifier on the mouth, a slice of
    it one frame out -> the iris closes onto a twin tile on a shelf: money
    pours into a meter that overflows off the frame; ROI ↓ -> four stage
    tiles; three get their time cut and go automatic, filming is left ->
    (her closeup) -> the iris opens on the pipeline: AI analysis -> RUTA
    (topics, a script) -> Claude (the edit) -> the last tile is her, live, and
    it grows until it is the frame -> a teleprompter reads along with her ->
    one grey clone flickers in beside her and breaks up -> an IG poll.

Her cut: eight shots (tools/shots.py). Two short inserts are hers — the
24.13-26.43 closeup on «дорожче, складніше і довше» and the 63.20-65.33
closeup on «але себе зі зйомок не прибирай». No pull-outs.

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
from glass import Glass  # noqa: E402

DUR = 93.950           # 2819 plate frames / 30 (work/w40-queue2.log)
FPS = 30
k = Kit(width=1080, height=1920, fps=FPS, duration=DUR)
g = Glass()
k.css(g.css())

BEATS = []


def beat(layer):
    def wrap(fn):
        BEATS.append((layer, fn))
        return fn
    return wrap


# ---------------------------------------------------------------------------
# NO-PAINT ZONES — her own editing (STYLE.md §4a). tools/shots.py: eight shots;
# the two short ones are closeups and they are the jokes. tools/pullouts.py:
# none.
#   24.13 – 26.43   face closeup on «дорожче, складніше і довше»
#   63.20 – 65.33   face closeup on «але себе зі зйомок не прибирай»
NO_PAINT = [(24.13, 26.43), (63.20, 65.33)]

# ---------------------------------------------------------------------------
# Words. Script spelling on her timing (work/r20/captions.json, settled with
# work/r20/caption-patch.json: «стрибнула» — whisper hears /stryb/ as /strym/
# twice in this reel — and «мені залишається»). The REVIEW line at 73.88 is
# hers: she says «лише встати», not the script's «тільки встати».
CAPS = k.load_captions(os.path.join(ROOT, "work", "r20", "captions.json"))
CAPS[-1]["e"] = min(CAPS[-1]["e"], DUR - 0.15)   # «є.» ran past the plate

W = {  # name -> caption index
    "pamiat": 0, "kilka": 1, "vsi": 4, "khaipyly": 5, "shtuchnykh": 8, "dviinykiv": 9,
    "zaminiat": 12, "bloheriv": 13, "mozhna": 15, "znimaty": 16, "de": 17, "zavhodno": 18,
    "ya": 19, "tsiutemu": 22, "strybnula": 23, "znimala": 24, "rilsy": 25,
    "a": 26, "potim": 27, "vse": 29, "yakos": 30, "zatykhlo": 31,
    "i1": 32, "zdaietsia": 35, "trokhy": 38, "nakhaipyly": 39, "temoiu": 42,
    "ty": 44, "prava": 45, "prosto": 46, "klasna": 50, "kruto": 53, "virusylas": 54,
    "my": 56, "vsi2": 57, "nanei": 58, "strybnuly": 59,
    "ale": 60, "po": 61, "obiektyvno": 63, "shtuchnyi": 64, "dviinyk": 65, "tse2": 66,
    "nabahato": 67, "nizh": 72, "prosto2": 73, "staty": 74, "vikno": 76, "sufler": 78,
    "zapysaty": 80, "toi": 81, "rils": 82,
    "tobto": 83, "vsi3": 84, "spodivalys": 85, "pry": 89, "liudynu": 90, "bloh": 92,
    "vzahali": 93, "znimaty2": 95, "de2": 96, "zavhodno2": 97,
    "i5": 98, "tak": 101, "ie": 103, "ale2": 104, "popershe": 106, "koshtuie": 107,
    "hroshei": 108, "podruhe": 109, "potriben": 112, "yakyis": 113, "riven": 114,
    "pidhotovky": 115,
    "i6": 116, "amator": 118, "vono": 120, "vyhliadaie": 123, "troshky": 124,
    "dyvno": 125, "rot": 126, "yakos2": 127, "tak1": 129, "shchos": 130, "inshe": 131,
    "ne2": 132, "tak2": 133,
    "shchob": 135, "pratsiuvalo": 137, "klasno": 139, "treba": 140, "postaratys": 143,
    "vbukhaty": 144, "hroshi": 146, "tse4": 150, "ne3": 152, "rentab": 153,
    "tomu": 154, "yakshcho2": 155, "vazhko": 157, "rilsy2": 159, "skorochui": 161,
    "chas": 162, "vsi4": 164, "inshi": 165, "etapy": 166, "maks": 167, "sproshchui": 168,
    "zhyttia": 170,
    "umene": 177, "shtuchnyi2": 178, "analizuie": 180, "kontent": 181, "ruta": 182,
    "dopomahaie": 183, "znaity": 184, "temy": 185, "peretvoryty": 187, "dumky": 188,
    "stsenarii": 190, "klod": 191, "montuie": 192, "video": 193, "mene": 195,
    "i10": 196, "meni": 197, "lyshe": 199, "vstaty": 200, "vikno2": 202,
    "uvimknuty": 203, "frontalnu": 204, "kameru": 205, "i11": 206, "chytaty": 207,
    "zsuflera": 209, "i12": 210, "vvazhaiu": 212, "nabahato2": 215, "krashche": 216,
    "nizh2": 217, "koly": 218, "namahaieshsia": 220, "zaminyty": 221, "dviinykom": 223,
    "ale4": 224, "meni2": 225, "tsikavo": 226, "khto": 227, "probuvav": 228,
    "dviinykiv2": 230, "realno": 232, "vpysav": 233, "systemu": 236, "zruchno": 239,
    "skazaly": 245, "chy": 246, "naspravdi": 247, "ie2": 252,
}
EXTRA = {"dur": DUR}


def S(name):
    return CAPS[W[name]]["s"]


def E(name):
    return CAPS[W[name]]["e"]


def js(src):
    """`@name`, `@name_e` (its end), `@name+0.12`, `@name-0.1` -> one literal
    time. Literals, not variables, because tools/review.py reads the timeline
    off the numbers."""
    def rep(m):
        name, end, off = m.group(1), m.group(2), m.group(3)
        if name in EXTRA:
            v = EXTRA[name]
        else:
            v = E(name) if end else S(name)
        v += float(off) if off else 0.0
        return "%.3f" % v
    return re.sub(r"@([a-z0-9]+)(_e)?([+-]\d+(?:\.\d+)?)?", rep, src)


# ---------------------------------------------------------------------------
# Mattes (tools/matte.py via work/r20/mattes.sh). (first frame, count).
#   her0  shot 0: her on top of the clones and the swapped rooms (b01). The
#         same clip, greyed, IS the twin everywhere else — she has no old twin
#         reel to show, so the twin is her own footage a few frames out.
#   tw2   her on top of the one clone that flickers in beside her (b19).
MATTES = {"her0": (0, 226), "tw2": (2430, 85)}
for _n, (_f0, _c) in MATTES.items():
    k.matte(_n, _f0 / 30.0, _c / 30.0)
HER0 = "assets/mattes/her0.webm"
HER0_LEN = MATTES["her0"][1] / 30.0

# The slow push on the plate (§0.8): her and her mattes move as one.
PUSH_O = (540, 820)


def push_at(t):
    return 1.0 + 0.045 * t / DUR


# ---------------------------------------------------------------------------
# Where she is. Measured off the plate: shots 1-7 put her face at x ~460-485,
# eyes y ~795, mouth ~(462, 918), hair top ~590 (shot 2 is closer: ~520).
FACE = (465, 850)
MOUTH = (462, 918)
EYES = (465, 800)


def vid(vid_id, src, start, dur, media, cls="vv"):
    """A framework-owned <video>. `media` is where in the source it starts."""
    assert media >= 0 and (src != HER0 or media + dur <= HER0_LEN + 0.001), (vid_id, media, dur)
    return ('<video id="%s" class="%s" src="%s" data-start="%.3f" data-duration="%.3f" '
            'data-media-start="%.3f" muted playsinline></video>' % (vid_id, cls, src, start, dur, media))


def frame_xf(sx, sy, sw, cw):
    """transform that maps the source rect starting (sx, sy), sw wide, onto a
    box cw wide at its origin (origin 0 0)."""
    s = cw / float(sw)
    return "transform: translate(%.2fpx,%.2fpx) scale(%.5f)" % (-sx * s, -sy * s, s)


def face_xf(cx, cy, fx, fy, s):
    """transform that puts source point (fx, fy) at box point (cx, cy) at scale s."""
    return "transform: translate(%.2fpx,%.2fpx) scale(%.5f)" % (cx - fx * s, cy - fy * s, s)


# ---------------------------------------------------------------------------
# Glyphs — monochrome, drawn, never emoji (§5a.11).
STROKES = {
    "heart": '<path d="M12 20.2s-7.9-4.7-7.9-10.4A4.3 4.3 0 0 1 12 7.4a4.3 4.3 0 0 1 7.9 2.4c0 5.7-7.9 10.4-7.9 10.4z"/>',
    "comment": '<path d="M20.5 11.6a8.5 8.5 0 0 1-12.4 7.6L3.5 20.5l1.3-4.4A8.5 8.5 0 1 1 20.5 11.6z"/>',
    "send": '<path d="M21.2 3.3L10.5 13.5"/><path d="M21.2 3.3l-6.6 17.6-4.1-7.4-7.7-3.9z"/>',
    "check": '<path d="M5.4 12.6l4.3 4.3 8.9-9.5"/>',
    "window": '<rect x="3.6" y="3.6" width="16.8" height="16.8" rx="2.6"/><path d="M12 3.6v16.8M3.6 12h16.8"/>',
    "prompter": '<path d="M5 6.5h14M5 10.5h14M5 14.5h9M5 18.5h11.5"/>',
    "euro": '<path d="M17.6 6.3a6.9 6.9 0 1 0 0 11.4"/><path d="M4.4 10.2h9.4M4.4 13.8h9.4"/>',
    "stairs": '<path d="M3.5 19.8h5.2v-5.1h5.2V9.6h5.2V4.4h1.4"/>',
    "clock": '<circle cx="12" cy="12" r="8.6"/><path d="M12 7.2V12l3.4 2.3"/>',
    "page": '<path d="M6.4 3.4h7.8l4 4v13.2H6.4z"/><path d="M13.8 3.4v4.4h4.4"/><path d="M9.2 12.2h6.2M9.2 15.6h6.2M9.2 19h3.8"/>',
    "film": '<rect x="3.4" y="5" width="17.2" height="14" rx="2.6"/><path d="M8 5v14M16 5v14M3.4 9.6H8M3.4 14.4H8M16 9.6h4.6M16 14.4h4.6"/>',
    "camera": '<rect x="2.6" y="6.4" width="13.2" height="11.2" rx="2.7"/><path d="M15.8 10.4l5.6-3.1v9.4l-5.6-3.1z"/>',
    "bulb": '<path d="M9.2 17.6h5.6M10.2 20.6h3.6"/><path d="M12 3.4a5.9 5.9 0 0 0-3.5 10.6c.6.5.9 1.2.9 2v1.6h5.2V16c0-.8.3-1.5.9-2A5.9 5.9 0 0 0 12 3.4z"/>',
    "down": '<path d="M12 4.6v14.6M5.6 12.8l6.4 6.4 6.4-6.4"/>',
    "up": '<path d="M12 19.4V4.8M5.6 11.2L12 4.8l6.4 6.4"/>',
    "person": '<circle cx="12" cy="8.4" r="3.9"/><path d="M4.4 20.2c.9-3.9 3.8-6 7.6-6s6.7 2.1 7.6 6"/>',
}
FILLS = {
    "play": '<path d="M8 5.2v13.6l10.6-6.8z"/>',
    "person": '<circle cx="12" cy="8.6" r="4.3"/><path d="M4.2 21c1.1-4.4 4.3-6.6 7.8-6.6s6.7 2.2 7.8 6.6z"/>',
    "flame": '<path d="M12.3 22c-4.3 0-7.3-3-7.3-7 0-3.5 2.3-5.8 3.9-7.7.3 1.9 1.1 3.1 2.4 3.8-.2-4 1.6-7.1 4.5-9.3-.3 2.9.8 4.9 2.5 6.9 1.4 1.7 2.4 3.6 2.4 6.3 0 4.1-3.1 7-8.4 7z"/>',
    "spark": '<path d="M12 2.4l2.2 6.8 6.8 2.2-6.8 2.2L12 20.4l-2.2-6.8-6.8-2.2 6.8-2.2z"/>',
    "bars": ('<rect x="3.5" y="12" width="4.4" height="8.5" rx="1.8"/>'
             '<rect x="9.8" y="7" width="4.4" height="13.5" rx="1.8"/>'
             '<rect x="16.1" y="3" width="4.4" height="17.5" rx="1.8"/>'),
}


def stroke(name, cls="sk"):
    return '<svg class="%s" viewBox="0 0 24 24">%s</svg>' % (cls, STROKES[name])


def fill(name, cls="fk"):
    return '<svg class="%s" viewBox="0 0 24 24">%s</svg>' % (cls, FILLS[name])


def kling(cls="mk kl"):
    return g.mark("kling", cls)


k.css("""
.abs, .cx { position: absolute; }
.hide { opacity: 0; visibility: hidden; }
.tw { position: absolute; }
.sk { fill: none; stroke: url(#gw); stroke-width: 2.2; stroke-linecap: round; stroke-linejoin: round;
  width: 50%; height: 50%; position: relative; z-index: 1; overflow: visible; }
.fk { fill: url(#gw); width: 50%; height: 50%; position: relative; z-index: 1; }
.pearl .sk { stroke: #17141c; } .pearl .fk { fill: #17141c; }
.mk.kl { fill-rule: evenodd; }
.circ .jelly, .circ .pearl, .circ .clear, .circ .sheen { border-radius: 50%; }
.sqring.circ { border-radius: 50%; }
/* a video laid out at plate size and mapped into its box by a transform */
.vw { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; transform-origin: 0 0; }
.vw video, video.vv { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }
.gray { filter: grayscale(1) contrast(1.05) brightness(1.07); }
/* the "AI studio" a twin stands in: flat, soft, nothing behind it */
.studio { position: absolute; inset: 0;
  background: linear-gradient(172deg, #f6eef1 0%, #e6d8dd 58%, #d2c1c8 100%); }
/* the AI tag, in jelly */
.aic { position: absolute; display: flex; align-items: center; justify-content: center;
  border-radius: 999px; color: #fff; font-weight: 900; letter-spacing: 0.04em;
  background: linear-gradient(165deg, #e0204b 0%, #ab112e 55%, #7a0a20 100%);
  box-shadow: inset 0 1.5px 1px rgba(255,255,255,0.5), 0 10px 22px -8px rgba(40,2,10,0.65); }
.pill { position: absolute; display: flex; align-items: center; gap: 10px; border-radius: 999px;
  font-weight: 700; white-space: nowrap; }
.pill.w { background: linear-gradient(170deg, #ffffff 0%, #fff4f7 100%); color: #17141c;
  box-shadow: inset 0 2px 1px #fff, 0 20px 40px -18px rgba(20,2,8,0.6); }
.pill.d { background: linear-gradient(160deg, rgba(58,22,32,0.62) 0%, rgba(24,10,15,0.55) 100%); color: #fff;
  box-shadow: inset 0 1.5px 1px rgba(255,255,255,0.28), 0 18px 36px -16px rgba(10,0,4,0.6); }
.pill svg { flex: none; }
/* the takeover wrapper: the iris lives on it */
.tkc { position: absolute; inset: 0; clip-path: circle(0px at 540px 300px); }
""")

EXTRA_DEFS = []

# ---------------------------------------------------------------------------
# The three places a twin can "film anywhere". Duotone in the house palette so
# the rooms read as places without leaving burgundy/pink/white (§5).


def _city():
    """Skyline tops at y 380-600: with a crowd of her in front, only the band
    above their heads says "city"."""
    out = []
    xs = [(0, 150, 520), (140, 120, 420), (250, 170, 560), (410, 130, 380), (530, 150, 500),
          (670, 120, 440), (780, 170, 600), (940, 140, 470)]
    for i, (x, w, top) in enumerate(xs):
        out.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>'
                   % (x, top, w, 1920 - top, "#23040f" if i % 2 else "#2e0714"))
        for r in range(16):
            for c in range(max(1, w // 42)):
                if (r * 7 + c * 3 + i) % 5 in (0, 2):
                    out.append('<rect x="%d" y="%d" width="16" height="22" rx="3" fill="#ff9cbc" opacity="0.%d"/>'
                               % (x + 16 + c * 42, top + 30 + r * 58, 45 + (r + c + i) % 4 * 12))
    return "".join(out)


# Each place keeps its identity in the top 600 px — the sun and a palm, the
# peaks, the skyline and the moon — because from y 600 down the frame is full
# of her and her clones.
SCENES = u'''
<linearGradient id="bSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe9f0"/><stop offset="0.27" stop-color="#ffc4d5"/><stop offset="0.3" stop-color="#ffa7c0"/></linearGradient>
<linearGradient id="bSea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e0204b"/><stop offset="1" stop-color="#7a0a20"/></linearGradient>
<linearGradient id="mSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff7fa"/><stop offset="0.35" stop-color="#ffd3df"/></linearGradient>
<linearGradient id="cSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#22030d"/><stop offset="0.4" stop-color="#6b0c28"/></linearGradient>
<symbol id="scBeach" viewBox="0 0 1080 1920" preserveAspectRatio="xMidYMid slice">
  <rect width="1080" height="1920" fill="url(#bSky)"/>
  <circle cx="790" cy="330" r="230" fill="#ffffff" opacity="0.25"/><circle cx="790" cy="330" r="125" fill="#fff6f9"/>
  <rect y="560" width="1080" height="1360" fill="url(#bSea)"/>
  <rect y="556" width="1080" height="6" fill="#ffd0dd" opacity="0.6"/>
  <rect x="650" y="596" width="280" height="12" rx="6" fill="#ffd3e0" opacity="0.85"/>
  <rect x="680" y="640" width="220" height="10" rx="5" fill="#ffd3e0" opacity="0.7"/>
  <rect x="710" y="682" width="160" height="9" rx="4.5" fill="#ffd3e0" opacity="0.55"/>
  <rect x="740" y="722" width="100" height="8" rx="4" fill="#ffd3e0" opacity="0.4"/>
  <path d="M150 1400 C 190 1000 220 640 262 330" fill="none" stroke="#4a0a1c" stroke-width="34" stroke-linecap="round"/>
  <g fill="#4a0a1c">
    <path d="M262 330 C 190 250 110 250 30 320 C 120 290 190 300 262 344 Z"/>
    <path d="M262 330 C 220 220 150 180 80 190 C 160 220 210 260 256 340 Z"/>
    <path d="M262 330 C 290 220 360 180 440 200 C 360 220 310 260 270 340 Z"/>
    <path d="M262 330 C 350 270 430 290 490 360 C 410 320 340 320 266 344 Z"/>
    <path d="M262 330 C 250 240 270 170 320 120 C 290 190 280 260 272 336 Z"/>
  </g>
</symbol>
<symbol id="scMount" viewBox="0 0 1080 1920" preserveAspectRatio="xMidYMid slice">
  <rect width="1080" height="1920" fill="url(#mSky)"/>
  <circle cx="230" cy="200" r="80" fill="#ffffff"/>
  <path d="M0 520 L160 300 L330 470 L520 210 L720 440 L880 280 L1080 400 V1920 H0 Z" fill="#f5a9be"/>
  <path d="M470 280 L520 210 L572 284 L545 270 L520 292 L495 270 Z" fill="#ffffff"/>
  <path d="M125 348 L160 300 L198 352 L160 334 Z" fill="#ffffff"/>
  <path d="M840 334 L880 280 L924 338 L882 320 Z" fill="#ffffff"/>
  <path d="M0 700 L220 420 L430 640 L680 360 L960 660 L1080 560 V1920 H0 Z" fill="#b4122f"/>
  <path d="M630 430 L680 360 L732 432 L700 414 L680 440 L660 414 Z" fill="#ffffff"/>
  <path d="M185 466 L220 420 L258 470 L222 452 Z" fill="#ffffff"/>
  <path d="M0 1000 Q 540 900 1080 1000 V1920 H0 Z" fill="#6b081c"/>
</symbol>
<symbol id="scCity" viewBox="0 0 1080 1920" preserveAspectRatio="xMidYMid slice">
  <rect width="1080" height="1920" fill="url(#cSky)"/>
  <circle cx="830" cy="230" r="170" fill="#ffd3e0" opacity="0.12"/><circle cx="830" cy="230" r="80" fill="#ffe4ec"/>
  <circle cx="160" cy="150" r="4" fill="#fff" opacity="0.7"/><circle cx="380" cy="90" r="3" fill="#fff" opacity="0.6"/>
  <circle cx="560" cy="240" r="3.5" fill="#fff" opacity="0.5"/><circle cx="1000" cy="380" r="3" fill="#fff" opacity="0.6"/>
  <circle cx="70" cy="330" r="3" fill="#fff" opacity="0.5"/><circle cx="640" cy="120" r="3" fill="#fff" opacity="0.55"/>
  CITY
</symbol>'''.replace("CITY", _city())
EXTRA_DEFS.append(SCENES)
EXTRA_DEFS.append(
    '<linearGradient id="gLine" x1="0" y1="0" x2="1" y2="0">'
    '<stop offset="0" stop-color="#ffd6e3"/><stop offset="0.45" stop-color="#ffffff"/>'
    '<stop offset="1" stop-color="#ffc2d4"/></linearGradient>'
    '<linearGradient id="gArea" x1="0" y1="0" x2="0" y2="1">'
    '<stop offset="0" stop-color="#ff6e9c" stop-opacity="0.45"/>'
    '<stop offset="1" stop-color="#ff6e9c" stop-opacity="0"/></linearGradient>'
    '<linearGradient id="gFlame" x1="0" y1="1" x2="0" y2="0">'
    '<stop offset="0" stop-color="#b4122f"/><stop offset="0.55" stop-color="#ff4f86"/>'
    '<stop offset="1" stop-color="#ffd0de"/></linearGradient>')


def scene(sid, name, cls="scene"):
    return ('<svg class="%s" id="%s" viewBox="0 0 1080 1920" preserveAspectRatio="xMidYMid slice">'
            '<use href="#%s"/></svg>' % (cls, sid, name))


k.css("""
svg.scene { position: absolute; left: 0; top: 0; width: 100%; height: 100%; }
""")

# the shared burgundy ground for every takeover (§0.6). One set of light pools,
# not one per takeover: the heavy-element budget counts radial gradients.
TK_GROUND = u'''
      <div id="tkG" class="tkc hide">
        <div class="tkg"></div>
        <div class="aur a1"></div><div class="aur a2"></div><div class="aur a3"></div>
        <div class="grain"></div>
      </div>'''

HEAD_JS = r"""
  var G = helpers(tl);
  function bin(sel, t, b, d) { d = d || 0.38; G.blurIn(sel, t, b || 12, d); tl.set(sel, {filter: "none"}, t + d + 0.01); }
  function bout(sel, t, b, d) { d = d || 0.32; G.blurOut(sel, t, b || 10, d); tl.set(sel, {filter: "none"}, t + d + 0.01); }
  function arr(sel, t, o) {
    o = o || {};
    bin(sel, t, o.blur || 12, 0.36);
    tl.fromTo(sel, {scale: o.s == null ? 0.5 : o.s, x: o.x || 0, y: o.y == null ? 34 : o.y, rotation: o.r || 0},
              {scale: 1, x: 0, y: 0, rotation: 0, duration: o.d || 0.85, ease: o.ease || POP}, t);
  }
  function pop(sel, t, d) {
    tl.fromTo(sel, {autoAlpha: 0, scale: 0.4}, {autoAlpha: 1, scale: 1, duration: d || 0.5, ease: POP, immediateRender: false}, t);
  }
  function shn(sel, t) {
    tl.fromTo(sel, {xPercent: -120}, {xPercent: 120, duration: 0.8, ease: "power2.inOut", immediateRender: false}, t);
  }
  // the iris on the shared ground and one takeover's content, together
  function irisOpen(c, t, x, y, d) {
    tl.set(["#tkG", c], {autoAlpha: 1}, t);
    tl.fromTo(["#tkG", c], {clipPath: "circle(0px at " + x + "px " + y + "px)"},
              {clipPath: "circle(2300px at " + x + "px " + y + "px)", duration: d || 0.8, ease: "power3.inOut", immediateRender: false}, t);
  }
  function irisClose(c, t, x, y, d) {
    tl.to(["#tkG", c], {clipPath: "circle(0px at " + x + "px " + y + "px)", duration: d || 0.4, ease: "power3.inOut"}, t);
    tl.set(["#tkG", c], {autoAlpha: 0}, t + (d || 0.4) + 0.01);
  }
  gsap.set(".sheen", {xPercent: -120});
"""

# ===================================================================== b01 ==
# The clones: her matte, four times, greyed, each a few frames behind her,
# standing further back in the room (scaled about her eye line). The same
# container later gets the three rooms, full frame, behind all of them.
EYE0 = (460, 790)
CLONES = [  # id, in (word or time), lag, pose (dx, s), step-forward (dx, s)
    ("c0", 0.30, 0.25, (-300, 0.74), (-340, 0.88)),
    ("c1", "kilka", 0.50, (300, 0.74), (335, 0.88)),
    ("c2", "vsi", 0.75, (505, 0.57), (560, 0.70)),
    ("c3", "khaipyly", 0.40, (-470, 0.57), (-540, 0.70)),
]
G1_OFF = 7.490          # the cut to shot 1 is at 7.50: the rooms go with it


def _t(v):
    return v if isinstance(v, float) else S(v)


k.css("""
/* ---- b01 · the clones ---- */
.cl { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px;
  transform-origin: %dpx %dpx; opacity: 0; visibility: hidden; }
/* the matte ends at the plate's bottom edge, which on a scaled-down clone is
   mid-air: the copies dissolve downward instead of stopping on a line */
.cl .gray { position: absolute; inset: 0; opacity: 0.93;
  -webkit-mask-image: linear-gradient(180deg, #000 0%%, #000 60%%, transparent 82%%);
  mask-image: linear-gradient(180deg, #000 0%%, #000 60%%, transparent 82%%); }
.cl .aic { left: 380px; top: 500px; width: 160px; height: 76px; font-size: 44px; }
.room { position: absolute; inset: 0; clip-path: circle(0px at 460px 850px); }
""" % EYE0)


@beat("behind")
def b01_clones():
    """«Пам'ятаєш, кілька місяців тому всі хайпили на тему штучних двійників —
    що вони замінять блогерів, і що можна знімати де завгодно.»

    BEHIND. She splits: four grey copies of her step out from behind her, one
    per phrase-beat, each a few frames late (the uncanny part). «AI» tags on
    «штучних». On «замінять» they step forward. On «знімати де завгодно» the
    room behind all of them turns into a beach, mountains, a city — three
    blooms out from behind her across «можна знімати де завгодно». Her matte
    (her0) sits on top of all of it; the cut to shot 1 takes it away."""
    rooms = "".join('<div class="room" id="rm%d">%s</div>' % (i, scene("rs%d" % i, n))
                    for i, n in enumerate(["scBeach", "scMount", "scCity"]))
    clones = []
    for cid, tin, lag, _, _ in CLONES:
        t0 = _t(tin)
        clones.append('<div class="cl" id="%s"><div class="gray">%s</div>'
                      '<div class="aic hide" id="%sai">AI</div></div>'
                      % (cid, vid("v" + cid, HER0, t0, G1_OFF - t0, t0 - lag), cid))
    html = u'''
      <div class="g full" id="g1">
        %s
        %s
      </div>''' % (rooms, "\n        ".join(clones))
    lines = ['  tl.set("#g1", {autoAlpha: 1}, 0.300);']
    for i, (cid, tin, lag, (dx, s), (dx2, s2)) in enumerate(CLONES):
        t0 = _t(tin)
        lines.append('  tl.set("#%s", {x: 0, scale: 1}, 0);' % cid)
        lines.append('  tl.fromTo("#%s", {autoAlpha: 0}, {autoAlpha: 1, duration: 0.3, ease: "power1.out", immediateRender: false}, %.3f);' % (cid, t0))
        lines.append('  tl.fromTo("#%s", {x: 0, scale: 1}, {x: %d, scale: %.3f, duration: 1.1, ease: SOFT, immediateRender: false}, %.3f);'
                     % (cid, dx, s, t0))
        lines.append('  pop("#%sai", %.3f);' % (cid, S("shtuchnykh") + i * 0.07))
        lines.append('  tl.to("#%s", {x: %d, scale: %.3f, duration: 0.7, ease: SP}, %.3f);'
                     % (cid, dx2, s2, S("zaminiat") + i * 0.05))
    src = "\n".join(lines) + js('''
  // «блогерів» — the tags pulse: these are the bloggers now
  G.bump(["#c0ai", "#c1ai", "#c2ai", "#c3ai"], @bloheriv+0.05);
  // «знімати» / «де» / «завгодно» — the room behind everyone blooms into a place
  [@mozhna-0.04, @znimaty+0.16, @zavhodno-0.04].forEach(function (t, i) {
    tl.set("#rm" + i, {autoAlpha: 1}, t);
    tl.fromTo("#rm" + i, {clipPath: "circle(0px at 460px 850px)"},
              {clipPath: "circle(1500px at 460px 850px)", duration: 0.34, ease: "power3.out", immediateRender: false}, t);
  });
  tl.set("#g1", {autoAlpha: 0}, %.3f);''' % G1_OFF)
    return html, src


# ===================================================================== b04 ==
# The shelf above her head: Kling -> a twin reel -> three reels -> the chart.
# Shot 1/2 put her hair top at ~600/~520, so everything ends by y 500.
CHART = [(130, 452), (250, 447), (360, 424), (452, 300), (520, 174), (584, 300),
         (652, 398), (760, 432), (880, 440), (975, 442)]
PEAK = CHART[4]


def smooth(p):
    d = "M %.1f %.1f" % p[0]
    for i in range(len(p) - 1):
        p0 = p[i - 1] if i else p[i]
        p1, p2 = p[i], p[i + 1]
        p3 = p[i + 2] if i + 2 < len(p) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6.0, p1[1] + (p2[1] - p0[1]) / 6.0)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6.0, p2[1] - (p3[1] - p1[1]) / 6.0)
        d += " C %.1f %.1f %.1f %.1f %.1f %.1f" % (c1 + c2 + p2)
    return d


LINE4 = smooth(CHART)
AREA4 = LINE4 + " L %.1f 470 L %.1f 470 Z" % (CHART[-1][0], CHART[0][0])


def on_line(x):
    for (x0, y0), (x1, y1) in zip(CHART, CHART[1:]):
        if x0 <= x <= x1:
            return y0 + (y1 - y0) * (x - x0) / float(x1 - x0)
    return CHART[-1][1]


# the avatars that jump onto the trend: from under the shelf onto the slope
AVATARS = [380, 420, 455, 485, 556]
REEL4 = (200, 356)


def reel_card(rid, media, start, dur, extra=""):
    """A reel: the twin in the AI studio, IG's right rail, a play glyph. No
    view count: any figure here reads as her real numbers."""
    w, h = REEL4
    return (u'<div class="reel" id="%(id)s"><div class="studio"></div>'
            u'<div class="vw gray" style="%(xf)s">%(v)s</div>'
            u'<div class="rui">%(h)s%(c)s%(s)s</div>'
            u'<div class="rvw">%(p)s</div>'
            u'<div class="aic" style="left:12px;top:12px;width:62px;height:36px;font-size:20px">AI</div>%(extra)s'
            u'</div>' % {"id": rid, "xf": frame_xf(150, 470, 620, w),
                         "v": vid("v" + rid, HER0, start, dur, media),
                         "h": stroke("heart", "sk w"), "c": stroke("comment", "sk w"),
                         "s": stroke("send", "sk w"), "p": fill("play", "fk w"),
                         "extra": extra})


k.css("""
/* ---- b04 · Kling, the twin reels, the chart ---- */
#s4 { left: 70px; top: 80px; width: 940px; height: 420px; }
#k4 { left: 100px; top: 196px; width: 180px; height: 180px; }
#k4n { left: 100px; top: 392px; width: 180px; text-align: center; font-size: 30px; font-weight: 700;
  color: #fff; letter-spacing: -0.01em; }
.reelw { position: absolute; left: 470px; top: 112px; width: 200px; height: 356px; }
.reel { position: absolute; inset: 0; border-radius: 30px; overflow: hidden;
  box-shadow: inset 0 0 0 1.5px rgba(255,255,255,0.55), 0 30px 60px -24px rgba(20,2,8,0.65); }
.rui { position: absolute; right: 10px; bottom: 58px; width: 34px; display: flex; flex-direction: column; gap: 12px; }
.rui svg { width: 34px; height: 34px; }
.sk.w { stroke: #fff; width: 100%; height: 100%; }
.fk.w { fill: #fff; width: 22px; height: 22px; }
.rvw { position: absolute; left: 12px; bottom: 14px; display: flex; align-items: center; gap: 6px;
  color: #fff; font-size: 24px; font-weight: 700; text-shadow: 0 1px 6px rgba(0,0,0,0.45); }
#cab4 { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: visible; }
#ch4 { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: visible; }
#ch4 .ln { fill: none; stroke: url(#gLine); stroke-width: 10; stroke-linecap: round; stroke-linejoin: round; }
#pk4 { left: 506px; top: 160px; width: 28px; height: 28px; border-radius: 50%; background: #fff;
  box-shadow: 0 0 0 6px #b4122f, 0 0 26px 6px rgba(255,110,156,0.8); }
#pr4 { left: 490px; top: 144px; width: 60px; height: 60px; }
#fl4 { left: 466px; top: 34px; width: 108px; height: 132px; }
#fl4 svg { width: 100%; height: 100%; fill: url(#gFlame); overflow: visible; }
#ok4 { left: 812px; top: 170px; width: 120px; height: 120px; }
#ok4 .sk { stroke: #fff; stroke-width: 3; }
.av4 { position: absolute; width: 62px; height: 62px; margin: -31px 0 0 -31px; border-radius: 50%;
  overflow: hidden; background: linear-gradient(160deg, #ffffff 0%, #f6dfe6 100%);
  box-shadow: inset 0 2px 1px #fff, 0 10px 20px -6px rgba(20,2,8,0.55), 0 0 0 3px rgba(255,255,255,0.8); }
.av4 svg { position: absolute; left: 12%; top: 16%; width: 76%; height: 84%; fill: rgba(180,18,47,0.55); }
.av4:nth-child(2n) { background: linear-gradient(160deg, #ff8ab0 0%, #d61a47 100%); }
.av4:nth-child(2n) svg { fill: rgba(255,255,255,0.85); }
""")


@beat("near")
def b04_kling_reels_chart():
    """«Я теж на цю тему стрибнула, знімала рілси, а потім це все якось
    затихло. І якщо тобі здається, що ми всі трохи нахайпили з цією темою, то
    ти права. Просто це була дуже класна тема, яка круто вірусилась, і ми всі
    на неї стрибнули.»

    NEAR, one shelf, one object handed along. A Kling tile lands on «цю
    тему»; a twin reel (her greyed, in an AI studio, «AI» tag) jumps out of it
    on «стрибнула»; two more fan out on «знімала рілси», each with its views.
    «а потім»: the reels collapse into the peak of a views chart and the line
    runs out flat on «затихло» — shape only, no numbers: any figure here would
    read as her real view counts. A flame on the
    spike on «нахайпили»; a tick on «ти права»; the spike ripples on
    «вірусилась»; five avatars jump onto the slope on «ми всі на неї
    стрибнули». The iris of the next beat opens out of the peak."""
    av = "".join('<div class="av4 hide" id="av4%d" style="left:%dpx;top:%dpx">%s</div>'
                 % (i, x0, y0, FILLS["person"].join(['<svg viewBox="0 0 24 24">', '</svg>']))
                 for i, (x0, y0) in enumerate([(210, 470), (280, 478), (160, 470), (330, 484), (240, 490)]))
    cab = "M 284 286 C 360 286 400 290 468 290"
    html = u'''
      <div class="g full" id="g4">
        <div id="s4" class="shelf edge abs hide"><div class="sheen"></div></div>
        <svg id="ch4" viewBox="0 0 1080 1920">
          <path id="ar4" d="%(area)s" fill="url(#gArea)"/>
          <path id="ln4" class="ln" d="%(line)s"/>
        </svg>
        <div class="tw hide" id="k4"><div class="pearl">%(kl)s<div class="sheen"></div></div></div>
        <div class="cx hide" id="k4n">Kling AI</div>
        <svg id="cab4" class="cab" viewBox="0 0 1080 1920">
          <path class="tube" id="cab4T" d="%(cab)s"/><path class="core" id="cab4C" d="%(cab)s"/>
          <g class="pkg"><path class="pkt hide" id="cab4P" d="%(cab)s"/></g>
        </svg>
        <div class="reelw hide" id="r4b">%(rb)s</div>
        <div class="reelw hide" id="r4c">%(rc)s</div>
        <div class="reelw hide" id="r4a">%(ra)s</div>
        <div class="sqring circ hide" id="pr4"></div>
        <div class="cx hide" id="fl4"><svg viewBox="0 0 24 24">%(flame)s</svg></div>
        <div class="cx hide" id="pk4"></div>
        <div class="tw circ hide" id="ok4"><div class="jelly">%(check)s<div class="sheen"></div></div></div>
        %(av)s
      </div>''' % {
        "area": AREA4, "line": LINE4, "kl": kling(), "cab": cab,
        "ra": reel_card("r4ai", 3.0, S("strybnula") - 0.1, 2.3),
        "rb": reel_card("r4bi", 0.6, S("znimala") - 0.1, 1.3),
        # durations differ by a frame: hyperframes keys media on src/start/
        # duration, and two identical keys can be discovered as one
        "rc": reel_card("r4ci", 5.2, S("znimala") - 0.1, 1.3 + 1 / 30.0),
        "flame": FILLS["flame"], "play": fill("play"), "play2": fill("play"),
        "check": stroke("check"), "av": av}
    av_js = []
    for i, x1 in enumerate(AVATARS):
        yl = on_line(x1) - 30
        t = [S("my"), S("vsi2"), S("nanei"), S("strybnuly"), S("strybnuly") + 0.22][i]
        x0, y0 = [(210, 470), (280, 478), (160, 470), (330, 484), (240, 490)][i]
        av_js.append('  tl.fromTo("#av4%d", {autoAlpha: 0, scale: 0.5}, {autoAlpha: 1, scale: 1, duration: 0.2, immediateRender: false}, %.3f);' % (i, t - 0.06))
        av_js.append('  tl.to("#av4%d", {x: %d, duration: 0.5, ease: "none"}, %.3f);' % (i, x1 - x0, t))
        av_js.append('  tl.to("#av4%d", {y: %d, duration: 0.25, ease: "power2.out"}, %.3f);' % (i, min(yl, y0) - y0 - 110, t))
        av_js.append('  tl.to("#av4%d", {y: %d, duration: 0.25, ease: "power2.in"}, %.3f);' % (i, yl - y0, t + 0.25))
        av_js.append('  G.bump("#pk4", %.3f);' % (t + 0.5))
    src = js(u'''
  tl.set("#g4", {autoAlpha: 1}, @ya-0.06);
  // the shelf, as she starts «Я теж»
  arr("#s4", @ya-0.06, {s: 0.9, y: 30, d: 0.9, ease: SP});
  // «цю тему» — Kling
  arr("#k4", @tsiutemu-0.06, {s: 0.5, y: 30});
  G.inner("#k4 .mk", @tsiutemu-0.06);
  bin("#k4n", @tsiutemu+0.14, 8, 0.3);
  shn("#k4 .sheen", @tsiutemu+0.4);
  // «стрибнула» — a twin reel jumps out of Kling
  G.draw("cab4T", @strybnula-0.12, 0.3); G.draw("cab4C", @strybnula-0.12, 0.3);
  tl.set("#r4a", {autoAlpha: 1}, @strybnula-0.02);
  tl.fromTo("#r4a", {x: -380, y: 60, scale: 0.3, rotation: -12}, {x: 0, scale: 1, rotation: 0, duration: 0.6, ease: SP}, @strybnula-0.02);
  tl.fromTo("#r4a", {y: 60}, {y: -46, duration: 0.3, ease: "power2.out", immediateRender: false}, @strybnula-0.02);
  tl.to("#r4a", {y: 0, duration: 0.4, ease: SP}, @strybnula+0.28);
  G.packet("cab4P", @strybnula+0.05, 0.4);
  // «знімала рілси» — two more fan out behind it
  tl.set(["#r4b", "#r4c"], {autoAlpha: 1}, @znimala-0.04);
  tl.fromTo("#r4b", {x: 0, rotation: 0, scale: 0.9}, {x: -150, rotation: -8, scale: 0.92, duration: 0.7, ease: POP}, @znimala-0.04);
  tl.fromTo("#r4c", {x: 0, rotation: 0, scale: 0.9}, {x: 150, rotation: 8, scale: 0.92, duration: 0.7, ease: POP}, @znimala+0.08);
  G.bump("#r4a", @rilsy);

  // «а потім» — Kling and the cable go; the reels fold into the peak
  bout(["#k4", "#k4n"], @a-0.04, 10, 0.3);
  tl.to(["#cab4T", "#cab4C"], {autoAlpha: 0, duration: 0.25}, @a-0.04);
  tl.to(["#r4b", "#r4c"], {x: 0, rotation: 0, scale: 0.85, duration: 0.3, ease: "power2.in"}, @a-0.04);
  tl.set(["#r4b", "#r4c"], {autoAlpha: 0}, @a+0.27);
  tl.to("#r4a", {x: %(px)d, y: %(py)d, scale: 0.08, duration: 0.42, ease: "power3.in"}, @a+0.04);
  tl.set("#r4a", {autoAlpha: 0}, @a+0.46);
  tl.fromTo("#pk4", {autoAlpha: 0, scale: 0}, {autoAlpha: 1, scale: 1, duration: 0.45, ease: POP, immediateRender: false}, @a+0.40);
  // the line: up to the spike, then out flat on «затихло»
  tl.fromTo("#ln4", {strokeDashoffset: G.drawPrep("ln4")}, {strokeDashoffset: 0, duration: 1.25, ease: "power1.inOut", immediateRender: false}, @potim);
  tl.fromTo("#ar4", {clipPath: "inset(0px 100%% 0px 0px)"}, {clipPath: "inset(0px 0%% 0px 0px)", duration: 1.25, ease: "power1.inOut"}, @potim);

  // «нахайпили» — the spike catches fire
  tl.fromTo("#fl4", {autoAlpha: 0, scale: 0.2, y: 40, transformOrigin: "50%% 100%%"},
            {autoAlpha: 1, scale: 1, y: 0, duration: 0.6, ease: POP}, @nakhaipyly);
  // «то ти права» — a tick
  arr("#ok4", @ty-0.04, {s: 0.4, y: 20});
  G.inner("#ok4 .sk", @ty-0.04);
  shn("#ok4 .sheen", @prava);
  // «класна тема» — light across the glass
  shn("#s4 .sheen", @klasna);
  G.bump("#fl4", @klasna+0.1);
  // «вірусилась» — the spike rings
  G.ripple("#pr4", @virusylas);
  G.bump(["#pk4", "#fl4"], @virusylas+0.04);
  tl.to("#fl4", {scale: 1.25, duration: 0.5, ease: SP}, @virusylas+0.3);
  bout("#ok4", @virusylas+0.2, 8, 0.3);
AVJS
  // the iris of b08 opens out of the peak; the shelf goes under it
  tl.set("#g4", {autoAlpha: 0}, @ale+0.36);''' % {"px": PEAK[0] - 570, "py": PEAK[1] - 290})
    return html, src.replace("AVJS", "\n".join(av_js))


# ===================================================================== b08 ==
# ДВІЙНИК vs ТИ, a butterfly chart on one sheet, in two halves around her
# closeup: the headers before it, the bars after it.
SH8 = (100, 230)                # the sheet's top-left in the frame
P8L, P8R = (125, 46), (565, 46)  # portraits, sheet coords, 190 square
ROWS8 = [("euro", u"ЦІНА", 360, 64), ("stairs", u"СКЛАДНІСТЬ", 330, 52), ("clock", u"ЧАС", 350, 76)]
ROW8_Y = [352, 508, 664]
P8L_C = (SH8[0] + P8L[0] + 95, SH8[1] + P8L[1] + 95)   # (320, 371) in the frame
P8R_C = (SH8[0] + P8R[0] + 95, SH8[1] + P8R[1] + 95)   # (760, 371)

k.css("""
/* ---- b08 · ДВІЙНИК vs ТИ ---- */
#sh8w { left: 100px; top: 230px; width: 880px; height: 850px; transform-origin: 440px 0px; }
#sh8 { position: absolute; inset: 0; }
.por { position: absolute; width: 190px; height: 190px; border-radius: 44px; overflow: hidden;
  box-shadow: inset 0 0 0 1.5px rgba(255,255,255,0.7), 0 24px 44px -20px rgba(60,4,18,0.55); }
#p8Lg { border-radius: 44px; box-shadow: inset 0 0 0 4px rgba(23,20,28,0.10);
  background: repeating-linear-gradient(135deg, rgba(23,20,28,0.035) 0 12px, transparent 12px 24px); }
#p8Lg svg { position: absolute; left: 25%; top: 22%; width: 50%; height: 56%; fill: rgba(23,20,28,0.16); }
.l8 { position: absolute; top: 258px; width: 300px; text-align: center; font-size: 44px; font-weight: 900;
  letter-spacing: -0.01em; }
#l8L { left: 70px; color: rgba(23,20,28,0.62); } #l8R { left: 510px; color: #b4122f; }
#vs8 { left: 398px; top: 99px; width: 84px; height: 84px; border-radius: 50%; display: flex;
  align-items: center; justify-content: center; font-size: 30px; font-weight: 700; color: rgba(23,20,28,0.5);
  background: #fbe3ea; box-shadow: inset 0 2px 1px #fff; }
#dv8 { left: 439px; top: 328px; width: 2px; height: 470px; background: rgba(23,20,28,0.10); transform-origin: 50% 0; }
.rl8 { position: absolute; left: 240px; width: 400px; display: flex; align-items: center; justify-content: center;
  gap: 12px; }
.rl8 svg { width: 34px; height: 34px; fill: none; stroke: #b4122f; stroke-width: 2.2; stroke-linecap: round;
  stroke-linejoin: round; }
.tr8 { position: absolute; height: 46px; border-radius: 23px; background: rgba(23,20,28,0.05); }
.bl8 { position: absolute; height: 46px; border-radius: 23px; transform-origin: 100% 50%;
  background: linear-gradient(270deg, #7e0b20 0%, #b4122f 45%, #ff6e9c 100%); }
.br8 { position: absolute; height: 46px; border-radius: 23px; transform-origin: 0% 50%;
  background: linear-gradient(90deg, #ff8ab0 0%, #ff5c8f 100%); }
.bdg8 { position: absolute; width: 70px; height: 70px; }
.bdg8 .sk { stroke: #17141c; width: 52%; height: 52%; }
#rec8 { left: 536px; top: 22px; height: 44px; padding: 0 16px 0 12px; font-size: 22px; letter-spacing: 0.06em;
  font-weight: 900; }
#rec8 i { width: 16px; height: 16px; border-radius: 50%; background: #ff3b5c; display: block;
  box-shadow: 0 0 0 4px rgba(255,59,92,0.25); }
#kb8 { left: 272px; top: 22px; width: 76px; height: 76px; }
""")


@beat("tk")
def b08a_versus():
    """«Але по факту, обʼєктивно, штучний двійник — це набагато…»

    OVER. The iris opens out of the chart's peak onto burgundy; one sheet
    grows out of the same point. «обʼєктивно»: a divider, «vs», and ТИ — her,
    live, in a portrait — with an empty hatched slot opposite. «штучний
    двійник»: the grey twin drops into the slot, Kling on its corner, and
    ДВІЙНИК under it (captions drop for «двійник»). «це набагато»: three row
    labels and their empty tracks. Then the iris closes onto the twin before
    her closeup, which is hers."""
    def rows():
        out = []
        for i, (ic, lab, lw, rw) in enumerate(ROWS8):
            y = ROW8_Y[i]
            out.append(u'<div class="rl8 hide" id="rl8%d" style="top:%dpx">%s<span class="t-micro">%s</span></div>'
                       % (i, y, '<svg viewBox="0 0 24 24">%s</svg>' % STROKES[ic], lab))
            out.append('<div class="tr8 hide" id="tl8%d" style="left:40px;top:%dpx;width:380px"></div>' % (i, y + 50))
            out.append('<div class="tr8 hide" id="tr8%d" style="left:460px;top:%dpx;width:380px"></div>' % (i, y + 50))
            out.append('<div class="bl8" id="bl8%d" style="left:%dpx;top:%dpx;width:%dpx"></div>' % (i, 420 - lw, y + 50, lw))
            out.append('<div class="br8" id="br8%d" style="left:460px;top:%dpx;width:%dpx"></div>' % (i, y + 50, rw))
        return "\n            ".join(out)
    sL = 190 / 330.0
    html = u'''
      <div class="g full" id="g8">
        <div class="tkc" id="tk8c">
          <div id="sh8w" class="abs hide"><div id="sh8" class="sheet">
            <div class="cx" id="p8Lg" style="left:%(lx)dpx;top:%(ly)dpx;width:190px;height:190px">%(ghost)s</div>
            <div class="por hide" id="p8L" style="left:%(lx)dpx;top:%(ly)dpx"><div class="studio"></div>
              <div class="vw gray" id="p8LA" style="%(xfL)s">%(vLA)s</div>
              <div class="vw gray hide" id="p8LB" style="%(xfL)s">%(vLB)s</div></div>
            <div class="tw hide" id="kb8"><div class="pearl">%(kl)s</div></div>
            <div class="por hide" id="p8R" style="left:%(rx)dpx;top:%(ry)dpx">
              <div class="vw" id="p8RA" style="%(xfRA)s">%(vRA)s</div>
              <div class="vw hide" id="p8RB" style="%(xfRB)s">%(vRB)s</div>
              <div class="sheen"></div></div>
            <div class="pill d hide" id="rec8"><i></i>REC</div>
            <div class="tw circ bdg8 hide" id="wd8" style="left:540px;top:196px"><div class="pearl">%(win)s</div></div>
            <div class="tw circ bdg8 hide" id="pm8" style="left:720px;top:196px"><div class="pearl">%(pro)s</div></div>
            <div class="l8 hide" id="l8L">ДВІЙНИК</div>
            <div class="l8 hide" id="l8R">ТИ</div>
            <div class="cx hide" id="vs8">vs</div>
            <div class="cx" id="dv8"></div>
            %(rows)s
            <div class="sheen"></div>
          </div></div>
        </div>
      </div>''' % {
        "lx": P8L[0], "ly": P8L[1], "rx": P8R[0], "ry": P8R[1],
        "ghost": FILLS["person"].join(['<svg viewBox="0 0 24 24">', '</svg>']),
        "xfL": face_xf(95, 100, FACE[0], FACE[1] - 20, sL),
        "vLA": vid("v8LA", HER0, S("ale"), 3.62, 0.20),
        "vLB": vid("v8LB", HER0, 26.440, 4.50, 2.50),
        "kl": kling(),
        "xfRA": face_xf(95, 104, 440, 790, 0.5),
        "vRA": vid("v8RA", "assets/base.mp4", S("ale"), 3.62, S("ale")),
        "xfRB": face_xf(95, 100, FACE[0], FACE[1] - 20, sL),
        "vRB": vid("v8RB", "assets/base.mp4", 26.440, 4.50, 26.440),
        "win": stroke("window"), "pro": stroke("prompter"), "rows": rows()}
    src = js(u'''
  tl.set("#g8", {autoAlpha: 1}, @ale);
  gsap.set(".bl8, .br8", {scaleX: 0});
  gsap.set("#dv8", {scaleY: 0});
  irisOpen("#tk8c", @ale, %(px)d, %(py)d, 0.8);
  G.drift("#tkG", @ale, 3.8);
  // «по факту» — the sheet grows out of the peak
  bin("#sh8w", @po, 16, 0.45);
  tl.fromTo("#sh8w", {scale: 0.22, x: %(sx)d, y: %(sy)d}, {scale: 1, x: 0, y: 0, duration: 1.0, ease: spring(0.72, 12)}, @po);
  // «обʼєктивно» — the divider, vs, and her
  tl.to("#dv8", {scaleY: 1, duration: 0.6, ease: "power3.out"}, @obiektyvno);
  pop("#vs8", @obiektyvno+0.05);
  arr("#p8R", @obiektyvno+0.08, {s: 0.5, y: 20});
  bin("#l8R", @obiektyvno+0.24, 8, 0.3);
  // «штучний двійник» — the twin drops into the empty slot
  bout("#p8Lg", @shtuchnyi, 8, 0.2);
  arr("#p8L", @shtuchnyi, {s: 0.5, y: 20});
  pop("#kb8", @shtuchnyi+0.2);
  bin("#l8L", @dviinyk, 8, 0.3);
  tl.fromTo("#l8L", {y: 14}, {y: 0, duration: 0.5, ease: SP}, @dviinyk);
  // «це набагато» — what gets compared
  [0, 1, 2].forEach(function (i) {
    bin("#rl8" + i, @tse2 + i * 0.08, 8, 0.3);
    tl.fromTo(["#tl8" + i, "#tr8" + i], {autoAlpha: 0, scaleX: 0.6}, {autoAlpha: 1, scaleX: 1, duration: 0.4, ease: SP}, @tse2+0.06 + i * 0.08);
  });
  G.bump("#p8L", @nabahato);
  // closes onto the twin before her closeup (24.13)
  irisClose("#tk8c", 23.720, %(lcx)d, %(lcy)d, 0.36);
  tl.set("#g8", {autoAlpha: 0}, 24.100);
  tl.set(["#p8LA", "#p8RA"], {autoAlpha: 0}, 24.100);''' % {
        "px": PEAK[0], "py": PEAK[1], "sx": PEAK[0] - 540, "sy": PEAK[1] - 230,
        "lcx": P8L_C[0], "lcy": P8L_C[1]})
    return html, src


@beat("tk")
def b08b_versus_bars():
    """«…ніж просто стати перед вікном з суфлером і записати той рілс.»

    OVER, the same sheet back after her closeup. «ніж»: the twin's three bars
    run long — the «дорожче, складніше і довше» she just said; «просто
    стати»: hers stay short. Then her kit lands on her portrait, one per
    phrase: a window on «вікном», a teleprompter on «суфлером», REC on
    «записати». The iris closes onto her portrait, which becomes the next
    beat's reel card."""
    src = js(u'''
  tl.set("#g8", {autoAlpha: 1}, 26.460);
  tl.set(["#p8LB", "#p8RB"], {autoAlpha: 1}, 26.460);
  irisOpen("#tk8c", 26.460, 465, 800, 0.7);
  G.drift("#tkG", 26.460, 4.5);
  // «ніж» — the twin: long
  [0, 1, 2].forEach(function (i) {
    tl.to("#bl8" + i, {scaleX: 1, duration: 0.7, ease: SP}, @nizh + i * 0.12);
  });
  // «просто стати» — you: short
  [0, 1, 2].forEach(function (i) {
    tl.to("#br8" + i, {scaleX: 1, duration: 0.6, ease: POP}, @prosto2 + i * 0.1);
  });
  // «перед вікном» / «з суфлером» / «записати той рілс»
  pop("#wd8", @vikno);
  pop("#pm8", @sufler);
  tl.fromTo("#rec8", {autoAlpha: 0, x: -20}, {autoAlpha: 1, x: 0, duration: 0.45, ease: POP, immediateRender: false}, @zapysaty);
  G.bump("#p8R", @zapysaty+0.05);
  tl.to("#rec8 i", {keyframes: {opacity: [1, 0.25, 1]}, duration: 0.7, ease: "none"}, @toi);
  shn("#p8R .sheen", @toi);
  shn("#sh8 > .sheen", @nizh+0.2);
  // closes onto her portrait, which the next beat carries on
  irisClose("#tk8c", @rils+0.10, %(rcx)d, %(rcy)d, 0.34);
  tl.set("#g8", {autoAlpha: 0}, @rils+0.46);''' % {"rcx": P8R_C[0], "rcy": P8R_C[1]})
    return "", src


# ===================================================================== b09 ==
# A reel card above her head: her, erased; the twin, anywhere; then what it
# costs. Shot 4 puts her hair top at ~590.
C9 = (400, 52, 280, 498)        # the card: left, top, w, h
C9_C = (C9[0] + C9[2] // 2, C9[1] + C9[3] // 2)   # (540, 288)
C9_SLIDE = -265

k.css("""
/* ---- b09 · the reel card, then the list ---- */
#c9w { left: 400px; top: 52px; width: 280px; height: 498px; }
#c9 { position: absolute; inset: 0; border-radius: 40px; overflow: hidden;
  box-shadow: inset 0 0 0 1.5px rgba(255,255,255,0.6), 0 34px 70px -26px rgba(20,2,8,0.7); }
#c9 svg.scene { clip-path: circle(0px at 140px 170px); }
#c9lc { position: absolute; inset: 0; clip-path: inset(0px 0px 0px 0%); }
#c9er { left: -3px; top: 0; width: 6px; height: 498px; border-radius: 3px; background: #fff;
  box-shadow: 0 0 18px 4px rgba(255,150,185,0.95); }
#c9pb { left: 14px; bottom: 12px; width: 252px; height: 6px; border-radius: 3px; background: rgba(255,255,255,0.35); }
#c9pf { position: absolute; left: 0; top: 0; width: 100%; height: 6px; border-radius: 3px; background: #fff;
  transform-origin: 0 50%; }
#c9 .rui { bottom: 40px; }
#c9ok { left: 226px; top: -30px; width: 92px; height: 92px; }
#c9ok .sk { stroke: #fff; stroke-width: 3; }
#l9 { left: 440px; top: 84px; width: 580px; height: 410px; }
.nb9 { position: absolute; width: 76px; height: 76px; }
.nb9 .wmark { font-size: 44px; color: #fff; }
#tg9 { left: 140px; top: 30px; width: 400px; height: 92px; padding: 0 30px 0 60px; font-size: 60px;
  font-weight: 900; letter-spacing: 0.02em; justify-content: space-between; }
#tg9::before { content: ""; position: absolute; left: 24px; top: 36px; width: 20px; height: 20px; border-radius: 50%;
  background: #f1d9e0; box-shadow: inset 0 2px 3px rgba(120,10,30,0.25); }
#tg9 span { color: rgba(180,18,47,0.18); }
.ck9 { position: absolute; left: 140px; height: 52px; width: 400px; }
.ck9 .bx { position: absolute; left: 0; top: 0; width: 52px; height: 52px; border-radius: 16px;
  box-shadow: inset 0 0 0 3px rgba(255,255,255,0.55); }
.ck9 .bf { position: absolute; left: 0; top: 0; width: 52px; height: 52px; border-radius: 16px;
  background: linear-gradient(165deg, #ff6e9c 0%, #d61a47 100%); }
.ck9 svg { position: absolute; left: 0; top: 0; width: 52px; height: 52px; fill: none; stroke: #fff;
  stroke-width: 3.2; stroke-linecap: round; stroke-linejoin: round; }
.ck9 i { position: absolute; left: 76px; top: 19px; height: 14px; border-radius: 7px; background: rgba(255,255,255,0.42); }
""")


@beat("near")
def b09_card_erased():
    """«Тобто всі сподівались, що так можна прибрати людину з блогінгу
    взагалі, і знімати де завгодно. І по факту так і є, але це, по-перше,
    коштує грошей, по-друге, все одно потрібен якийсь рівень підготовки…»

    NEAR. Her portrait from the sheet becomes a reel card above her head,
    playing her live. «прибрати людину»: an eraser sweeps her out of it,
    leaving an empty studio. «з блогінгу»: the grey twin glitches in, «AI».
    «знімати де завгодно»: the world behind the twin swaps three times — the
    same beach, mountains and city as the opening. «так і є»: a tick. «але
    це»: the card steps aside for the catch — «по-першe» €€€ lighting one by
    one on «грошей»; «по-друге» a checklist ticking on «якийсь рівень
    підготовки». The next beat's iris opens out of the card."""
    xf = frame_xf(140, 480, 640, C9[2])
    ticks = "".join(u'<div class="ck9 hide" id="ck9%d" style="top:%dpx"><div class="bx"></div>'
                    u'<div class="bf" id="bf9%d"></div><svg viewBox="0 0 52 52"><path id="tk9%d" d="M14 27l8 8 16-17"/></svg>'
                    u'<i style="width:%dpx"></i></div>' % (i, 150 + i * 72, i, i, w)
                    for i, w in enumerate([300, 236, 318]))
    html = u'''
      <div class="g full" id="g9">
        <div class="tw hide" id="c9w">
          <div id="c9">
            <div class="studio"></div>
            %(scenes)s
            <div class="vw gray hide" id="c9tA" style="%(xf)s">%(vtA)s</div>
            <div class="vw gray hide" id="c9tB" style="%(xf)s">%(vtB)s</div>
            <div id="c9lc"><div class="vw" style="%(xf)s">%(vl)s</div></div>
            <div class="cx hide" id="c9er"></div>
            <div class="rui">%(h)s%(c)s%(s)s</div>
            <div class="aic hide" id="c9ai" style="left:14px;top:14px;width:70px;height:40px;font-size:22px">AI</div>
            <div class="cx" id="c9pb"><div id="c9pf"></div></div>
          </div>
          <div class="tw circ hide" id="c9ok"><div class="jelly">%(check)s<div class="sheen"></div></div></div>
        </div>
        <div id="l9" class="dglass edge abs hide">
          <div class="tw circ nb9 hide" id="nb9a" style="left:36px;top:38px"><div class="jelly">%(n1)s</div></div>
          <div class="pill w hide" id="tg9"><span id="e90">€</span><span id="e91">€</span><span id="e92">€</span></div>
          <div class="tw circ nb9 hide" id="nb9b" style="left:36px;top:188px"><div class="jelly">%(n2)s</div></div>
          %(ticks)s
        </div>
      </div>''' % {
        "scenes": "".join(scene("c9s%d" % i, n, "scene hide") for i, n in enumerate(["scBeach", "scMount", "scCity"])),
        "xf": xf,
        "vtA": vid("v9tA", HER0, 33.600, 7.40, 0.10),
        "vtB": vid("v9tB", HER0, 41.000, 2.20, 0.60),
        "vl": vid("v9l", "assets/base.mp4", 30.950, 2.40, 30.950),
        "h": stroke("heart", "sk w"), "c": stroke("comment", "sk w"), "s": stroke("send", "sk w"),
        "check": stroke("check"), "n1": Glass.wordmark("1", size=44), "n2": Glass.wordmark("2", size=44),
        "ticks": ticks}
    src = js(u'''
  tl.set("#g9", {autoAlpha: 1}, @vsi3-0.06);
  // her portrait from the sheet becomes a reel above her head
  arr("#c9w", @vsi3-0.06, {s: 0.43, x: %(fx)d, y: %(fy)d, d: 0.9, ease: SP});
  tl.fromTo("#c9pf", {scaleX: 0}, {scaleX: 1, duration: 11.2, ease: "none"}, @vsi3);
  // «прибрати людину» — an eraser sweeps her out
  tl.set("#c9er", {autoAlpha: 1}, @pry);
  tl.fromTo("#c9lc", {clipPath: "inset(0px 0px 0px 0%%)"}, {clipPath: "inset(0px 0px 0px 100%%)", duration: 0.55, ease: "power1.inOut"}, @pry);
  tl.fromTo("#c9er", {x: 0}, {x: 280, duration: 0.55, ease: "power1.inOut"}, @pry);
  tl.set("#c9er", {autoAlpha: 0}, @pry+0.56);
  // «з блогінгу» — the twin glitches in
  tl.fromTo("#c9tA", {autoAlpha: 0, x: 0}, {keyframes: {autoAlpha: [0, 0.7, 0.15, 0.95, 0.4, 1], x: [0, 8, -6, 4, 0, 0]},
            duration: 0.36, ease: "none", immediateRender: false}, @bloh);
  pop("#c9ai", @bloh+0.22);
  // «знімати де завгодно» — the world behind it swaps
  [@znimaty2-0.04, @de2-0.04, @zavhodno2-0.02].forEach(function (t, i) {
    tl.set("#c9s" + i, {autoAlpha: 1}, t);
    tl.fromTo("#c9s" + i, {clipPath: "circle(0px at 140px 170px)"},
              {clipPath: "circle(620px at 140px 170px)", duration: 0.3, ease: "power3.out", immediateRender: false}, t);
  });
  // «так і є» — true
  arr("#c9ok", @tak-0.04, {s: 0.4, y: 12});
  G.inner("#c9ok .sk", @tak-0.04);
  G.bump("#c9", @tak+0.1);
  // «але це» — the card steps aside for the catch
  bout("#c9ok", @ale2-0.1, 8, 0.25);
  tl.to("#c9w", {x: %(slide)d, duration: 0.6, ease: SP}, @ale2);
  arr("#l9", @ale2+0.04, {s: 0.9, x: 80, y: 0, d: 0.8, ease: SP});
  // «по-перше, коштує грошей»
  pop("#nb9a", @popershe);
  arr("#tg9", @koshtuie-0.04, {s: 0.6, x: -30, y: 0});
  [0, 1, 2].forEach(function (i) {
    tl.to("#e9" + i, {color: "#b4122f", duration: 0.12}, @hroshei + i * 0.14);
    G.bump("#e9" + i, @hroshei + i * 0.14);
  });
  // the twin clip runs out of footage here; the second take picks it up
  tl.set("#c9tA", {autoAlpha: 0}, 41.000);
  tl.set("#c9tB", {autoAlpha: 1}, 41.000);
  // row 2 waits as a ghost from the start (§4a.5: no blank plaque)
  tl.fromTo(["#nb9b", ".ck9"], {autoAlpha: 0}, {autoAlpha: 0.28, duration: 0.4, immediateRender: false}, @ale2+0.3);
  // «по-друге … якийсь рівень підготовки»
  tl.to("#nb9b", {autoAlpha: 1, duration: 0.2}, @podruhe);
  G.bump("#nb9b", @podruhe);
  [0, 1, 2].forEach(function (i) {
    tl.to("#ck9" + i, {autoAlpha: 1, duration: 0.25}, @potriben + i * 0.08);
    tl.fromTo("#ck9" + i, {x: -20}, {x: 0, duration: 0.5, ease: SP}, @potriben + i * 0.08);
  });
  gsap.set(".ck9 .bf", {autoAlpha: 0, scale: 0.4, transformOrigin: "50%% 50%%"});
  [@yakyis, @riven, @pidhotovky].forEach(function (t, i) {
    tl.to("#bf9" + i, {autoAlpha: 1, scale: 1, duration: 0.4, ease: POP}, t);
    G.draw("tk9" + i, t + 0.06, 0.28);
  });
  // the next beat's iris opens out of the card
  tl.set("#g9", {autoAlpha: 0}, @i6+0.36);''' % {
        "fx": P8R_C[0] - C9_C[0], "fy": P8R_C[1] - C9_C[1], "slide": C9_SLIDE})
    return html, src


# ===================================================================== b13 ==
# The twin's face, big: a magnifier on the mouth, a slice of it one frame out.
BC = (160, 130, 760, 1000)      # the card: left, top, w, h
CS = 1.35                       # plate -> card scale
CO = (178, 470)                 # plate point at the card's top-left


def to_card(p):
    return ((p[0] - CO[0]) * CS, (p[1] - CO[1]) * CS)


# her0 runs from media 1.00 here. Measured off the plate over the windows the
# magnifier sits in: the mouth over media 4.7-6.0 wanders (467-553, 896-953),
# the eyes over 6.0-7.1 (433-440, 737-800). The lens sits on the average and
# is wide enough to keep the feature inside it; the slices cover the spread.
M13 = 1.00
MOUTH_W = (496, 922)
EYES_W = (435, 770)
MOUTH_C = to_card(MOUTH_W)
EYES_C = to_card(EYES_W)
MBOX = (420, 878, 600, 976)     # the mouth band, plate coords
EBOX = (330, 715, 560, 830)     # the eye band
ZOOM = 1.45
LENS = 320


def inset_card(box):
    x0, y0 = to_card(box[:2])
    x1, y1 = to_card(box[2:])
    return "inset(%.1fpx %.1fpx %.1fpx %.1fpx)" % (y0, BC[2] - x1, BC[3] - y1, x0)


C13_FROM = (C9_C[0] + C9_SLIDE, C9_C[1])        # the reel card, slid aside: (275, 288)
T14 = (195, 285)                                 # the twin tile on the money shelf

k.css("""
/* ---- b13 · the twin up close ---- */
#bc13w { left: 160px; top: 130px; width: 760px; height: 1000px; transform-origin: 380px 500px; }
#bc13 { position: absolute; inset: 0; border-radius: 64px; overflow: hidden;
  box-shadow: inset 0 0 0 2px rgba(255,255,255,0.6), 0 70px 130px -40px rgba(8,0,3,0.75); }
#bc13 .sheen { mix-blend-mode: soft-light; }
.slc { position: absolute; left: 0; top: 0; width: 760px; height: 1000px; }
#kb13 { left: 36px; top: 36px; width: 112px; height: 112px; }
#mg13 { left: %(ml).1fpx; top: %(mt).1fpx; width: %(L)dpx; height: %(L)dpx; }
#mgc13 { position: absolute; inset: 0; border-radius: 50%%; overflow: hidden; background: #e6d8dd; }
#mgr13 { position: absolute; left: 0; top: 0; width: 760px; height: 1000px; transform-origin: 0 0; }
#mgring { position: absolute; left: -40px; top: -40px; width: 400px; height: 400px; overflow: visible; }
#mgring circle { fill: none; stroke: #fff; stroke-width: 12; }
#mgring .h { fill: none; stroke: #fff; stroke-width: 30; stroke-linecap: round; }
#mgring .glow { fill: none; stroke: rgba(255,110,156,0.55); stroke-width: 26; }
""" % {"ml": MOUTH_C[0] - LENS / 2, "mt": MOUTH_C[1] - LENS / 2, "L": LENS})
assert LENS == 320   # the ring's svg below is drawn for a 320 lens


@beat("tk")
def b13_mouth_glitch():
    """«…і на аматорському рівні воно все одно виглядає трошки дивно — рот
    якось не так, щось інше не так.»

    OVER. The iris opens out of the reel card and the twin comes up to full
    size: her own footage, greyed, in an AI studio, Kling and «AI» on the
    corner. «трошки дивно»: a band across the mouth jumps for two frames.
    «рот»: a magnifier lands on the mouth — inside it, a slice of the mouth
    running a frame behind the rest of the face and knocked sideways. «якось
    не так»: it jumps. «щось інше не так»: the magnifier moves up to the eyes
    and a band there slips too. The iris closes onto the twin tile of the
    next beat."""
    xf = frame_xf(CO[0], CO[1], BC[2] / CS, BC[2])
    ms = inset_card(MBOX)
    es = inset_card(EBOX)
    face = u'''<div class="studio"></div>
              <div class="vw gray" style="%(xf)s">%(v0)s</div>
              <div class="slc hide ms13" id="%(mid)s" style="clip-path:%(ms)s"><div class="vw gray" style="%(xf)s">%(v1)s</div></div>
              <div class="slc hide es13" id="%(eid)s" style="clip-path:%(es)s"><div class="vw gray" style="%(xf)s">%(v2)s</div></div>'''
    t0, d0, m0 = S("i6"), 6.52, M13
    lag1, lag2 = 2 / 30.0, 3 / 30.0
    f = 1 / 30.0
    # every copy gets its own start/duration key (hyperframes keys media on
    # src/start/duration; identical keys can be discovered as one, which
    # would quietly take the frame offset out of the slices)
    main = face % {"xf": xf, "ms": ms, "es": es, "mid": "ms13", "eid": "es13",
                   "v0": vid("v13a", HER0, t0, d0, m0), "v1": vid("v13b", HER0, t0, d0 - f, m0 - lag1),
                   "v2": vid("v13c", HER0, t0, d0 - 2 * f, m0 - lag2)}
    t1 = S("rot") - 0.20           # the lens only exists from «рот»
    lens = face % {"xf": xf, "ms": ms, "es": es, "mid": "ms13z", "eid": "es13z",
                   "v0": vid("v13d", HER0, t1, t0 + d0 - t1, m0 + (t1 - t0)),
                   "v1": vid("v13e", HER0, t1, t0 + d0 - t1 - f, m0 + (t1 - t0) - lag1),
                   "v2": vid("v13f", HER0, t1, t0 + d0 - t1 - 2 * f, m0 + (t1 - t0) - lag2)}
    html = u'''
      <div class="g full" id="g13">
        <div class="tkc" id="tk13c">
          <div id="bc13w" class="abs hide">
            <div id="bc13">
              %(main)s
              <div class="tw hide" id="kb13"><div class="pearl">%(kl)s</div></div>
              <div class="aic hide" id="ai13" style="left:166px;top:64px;width:96px;height:56px;font-size:30px">AI</div>
              <div class="sheen"></div>
            </div>
            <div class="tw hide" id="mg13">
              <div id="mgc13"><div id="mgr13">%(lens)s</div></div>
              <svg id="mgring" viewBox="-40 -40 400 400">
                <circle class="glow" cx="160" cy="160" r="166"/>
                <path class="h" d="M 282 282 L 346 346"/>
                <circle cx="160" cy="160" r="166"/>
              </svg>
            </div>
          </div>
        </div>
      </div>''' % {"main": main, "lens": lens, "kl": kling()}
    mx, my = MOUTH_C
    ex, ey = EYES_C
    src = js(u'''
  tl.set("#g13", {autoAlpha: 1}, @i6);
  gsap.set("#mgr13", {x: %(zx).2f, y: %(zy).2f, scale: %(Z).3f, transformOrigin: "0px 0px"});
  irisOpen("#tk13c", @i6, %(fx)d, %(fy)d, 0.8);
  G.drift("#tkG", @i6, 6.6);
  // the card grows into the twin's face
  bin("#bc13w", @i6+0.04, 16, 0.45);
  tl.fromTo("#bc13w", {x: %(cx)d, y: %(cy)d, scale: 0.33}, {x: 0, y: 0, scale: 1, duration: 1.0, ease: spring(0.72, 12)}, @i6+0.04);
  // «воно все одно виглядає» — made where, and by what
  arr("#kb13", @vono, {s: 0.5, y: 16});
  pop("#ai13", @vono+0.18);
  shn("#bc13 > .sheen", @vyhliadaie);
  // «трошки дивно» — the mouth band jumps for two frames
  tl.set(".ms13", {autoAlpha: 1, x: 16}, @troshky+0.1);
  tl.set(".ms13", {x: -10}, @troshky+0.167);
  tl.set(".ms13", {autoAlpha: 0, x: 0}, @troshky+0.234);
  tl.to("#bc13", {keyframes: {x: [0, -9, 7, -3, 0]}, duration: 0.2, ease: "none"}, @dyvno);
  tl.set(".es13", {autoAlpha: 1, x: -12}, @dyvno);
  tl.set(".es13", {autoAlpha: 0, x: 0}, @dyvno+0.1);
  // «рот» — the magnifier, and the slice stays out
  arr("#mg13", @rot-0.04, {s: 0.4, y: 40, d: 0.7});
  tl.set(".ms13", {autoAlpha: 1, x: 9}, @rot);
  // «якось не так» — it jumps
  tl.to(".ms13", {keyframes: {x: [9, -12, 14, -6, 10]}, duration: 0.42, ease: "none"}, @yakos2);
  G.bump("#mg13", @tak1);
  // «щось інше не так» — up to the eyes, and they slip too
  tl.to("#mg13", {x: %(dx).1f, y: %(dy).1f, duration: 0.5, ease: SP}, @shchos-0.04);
  tl.to("#mgr13", {x: %(zx2).2f, y: %(zy2).2f, duration: 0.5, ease: SP}, @shchos-0.04);
  tl.set(".es13", {autoAlpha: 1, x: -11}, @shchos+0.2);
  tl.to(".es13", {keyframes: {x: [-11, 12, -8, 9]}, duration: 0.36, ease: "none"}, @inshe);
  tl.to(".ms13", {keyframes: {x: [10, -14, 8]}, duration: 0.24, ease: "none"}, @ne2);
  G.bump("#bc13w", @tak2);
  // closes onto the twin tile of the money shelf
  irisClose("#tk13c", @tak2+0.12, %(tx)d, %(ty)d, 0.38);
  tl.set("#g13", {autoAlpha: 0}, @tak2+0.52);''' % {
        "Z": ZOOM, "zx": LENS / 2 - ZOOM * mx, "zy": LENS / 2 - ZOOM * my,
        "zx2": LENS / 2 - ZOOM * ex, "zy2": LENS / 2 - ZOOM * ey,
        "dx": ex - mx, "dy": ey - my,
        "fx": C13_FROM[0], "fy": C13_FROM[1],
        "cx": C13_FROM[0] - (BC[0] + BC[2] // 2), "cy": C13_FROM[1] - (BC[1] + BC[3] // 2),
        "tx": T14[0], "ty": T14[1]})
    return html, src


# ===================================================================== b14 ==
k.css("""
/* ---- b14 · money in, nothing back ---- */
#s14 { left: 70px; top: 120px; width: 940px; height: 330px; }
#tt14 { left: 110px; top: 200px; width: 170px; height: 170px; }
#tt14c { position: absolute; inset: 0; border-radius: 40px; overflow: hidden;
  box-shadow: inset 0 0 0 2px rgba(255,255,255,0.7), 0 26px 50px -20px rgba(24,4,12,0.6); }
#tt14 .aic { left: 8px; top: 8px; width: 58px; height: 32px; font-size: 18px; z-index: 2; }
#sp14 { left: 236px; top: 168px; width: 64px; height: 64px; }
#sp14 svg { width: 100%; height: 100%; fill: #ffd6e3; }
#co14 { left: 320px; top: 237px; width: 96px; height: 96px; }
#co14 .sk { stroke: #fff; stroke-width: 2.6; width: 56%; height: 56%; }
#tr14 { left: 440px; top: 262px; width: 540px; height: 46px; border-radius: 23px;
  background: rgba(255,255,255,0.14); box-shadow: inset 0 2px 6px rgba(0,0,0,0.25), inset 0 0 0 1.5px rgba(255,255,255,0.2); }
#fi14 { left: 440px; top: 262px; width: 540px; height: 46px; border-radius: 23px; transform-origin: 0 50%;
  background: linear-gradient(90deg, #8d0d24 0%, #d61a47 50%, #ff6e9c 100%);
  box-shadow: inset 0 2px 1px rgba(255,255,255,0.45), 0 0 26px rgba(255,110,156,0.6); }
.cn14 { position: absolute; top: 258px; width: 54px; height: 54px; margin-left: -27px; }
.cn14 .sk { stroke: #fff; stroke-width: 2.8; width: 60%; height: 60%; }
#roi14 { left: 604px; top: 342px; height: 70px; padding: 0 28px 0 30px; font-size: 38px; font-weight: 900; }
#roi14 svg { width: 38px; height: 38px; fill: none; stroke: #d61a47; stroke-width: 3.2; stroke-linecap: round;
  stroke-linejoin: round; }
""")


@beat("near")
def b14_money():
    """«І щоб це працювало справді класно, треба дуже сильно постаратись і
    вбухати туди гроші, і по факту це просто не рентабельно.»

    NEAR. The takeover closes onto a twin tile on a shelf. «класно»: a
    sparkle on it. «постаратись»: a money meter fills halfway. «вбухати туди
    гроші»: € coins drop in and the meter runs past the end of the shelf and
    off the frame. «не рентабельно»: ROI ↓."""
    coins = "".join('<div class="tw circ cn14 hide" id="cn14%d" style="left:%dpx"><div class="jelly">%s</div></div>'
                    % (i, x, stroke("euro")) for i, x in enumerate([600, 740, 880]))
    html = u'''
      <div class="g full" id="g14">
        <div id="s14" class="shelf edge abs hide"><div class="sheen"></div></div>
        <div class="tw hide" id="tt14"><div id="tt14c"><div class="studio"></div>
          <div class="vw gray" style="%(xf)s">%(v)s</div></div>
          <div class="aic">AI</div></div>
        <div class="cx hide" id="sp14">%(spark)s</div>
        <div class="tw circ hide" id="co14"><div class="jelly">%(euro)s<div class="sheen"></div></div></div>
        <div class="cx hide" id="tr14"></div>
        <div class="cx" id="fi14"></div>
        %(coins)s
        <div class="pill w hide" id="roi14">ROI %(down)s</div>
      </div>''' % {
        "xf": face_xf(85, 96, FACE[0], FACE[1] - 20, 0.5),
        "v": vid("v14", HER0, S("shchob") - 0.06, 6.9, 0.30),
        "spark": FILLS["spark"].join(['<svg viewBox="0 0 24 24">', '</svg>']),
        "euro": stroke("euro"), "coins": coins,
        "down": '<svg viewBox="0 0 24 24">%s</svg>' % STROKES["down"]}
    src = js(u'''
  tl.set("#g14", {autoAlpha: 1}, @shchob-0.06);
  gsap.set("#fi14", {scaleX: 0});
  arr("#s14", @shchob-0.06, {s: 0.9, y: 24, d: 0.9, ease: SP});
  arr("#tt14", @shchob-0.06, {s: 0.55, y: 0});
  // «працювало» — the money side of the shelf
  pop("#co14", @pratsiuvalo);
  bin("#tr14", @pratsiuvalo+0.1, 8, 0.3);
  tl.fromTo("#tr14", {scaleX: 0.7, transformOrigin: "0% 50%"}, {scaleX: 1, duration: 0.6, ease: SP}, @pratsiuvalo+0.1);
  // «класно» — to look good
  tl.fromTo("#sp14", {autoAlpha: 0, scale: 0.2, rotation: -90}, {autoAlpha: 1, scale: 1, rotation: 0, duration: 0.6, ease: POP, immediateRender: false}, @klasno);
  G.bump("#tt14", @klasno+0.05);
  // «треба дуже сильно постаратись»
  tl.to("#fi14", {scaleX: 0.28, duration: 0.5, ease: SP}, @treba);
  tl.to("#fi14", {scaleX: 0.56, duration: 0.7, ease: SP}, @postaratys);
  G.bump("#co14", @postaratys);
  // «вбухати туди гроші» — coins pour in, the meter runs off the frame
  [0, 1, 2].forEach(function (i) {
    var t = @vbukhaty + i * 0.16;
    tl.fromTo("#cn14" + i, {autoAlpha: 0, y: -170, scale: 0.6}, {autoAlpha: 1, y: 0, scale: 1, duration: 0.32, ease: "power2.in", immediateRender: false}, t);
    tl.to("#cn14" + i, {scale: 0, autoAlpha: 0, duration: 0.18, ease: "power2.in"}, t + 0.32);
  });
  tl.to("#fi14", {scaleX: 1.0, duration: 0.3, ease: "power2.out"}, @vbukhaty+0.3);
  tl.to("#fi14", {scaleX: 1.28, duration: 0.22, ease: "power2.out"}, @vbukhaty+0.62);
  tl.to("#fi14", {scaleX: 1.45, duration: 0.5, ease: SP}, @hroshi);
  G.haptic("#s14", @hroshi);
  // «не рентабельно» — nothing comes back
  arr("#roi14", @ne3-0.04, {s: 0.5, y: 20});
  tl.to("#tt14", {autoAlpha: 0.55, duration: 0.4}, @rentab);
  tl.set("#g14", {autoAlpha: 0}, 55.840);''')
    return html, src


# ===================================================================== b15 ==
STAGES = [("bars", u"АНАЛІЗ", 120), ("page", u"СЦЕНАРІЙ", 180), ("film", u"МОНТАЖ", 240), ("camera", u"ЗЙОМКА", 60)]
ST_L = [110, 330, 550, 770]

k.css("""
/* ---- b15 · the stages of a reel ---- */
#s15 { left: 60px; top: 100px; width: 960px; height: 370px; }
.sg15 { position: absolute; top: 132px; width: 160px; height: 300px; }
.st15 { position: absolute; left: 0; top: 0; width: 160px; height: 160px; }
.st15 .jelly { opacity: 0; }
.sl15 { position: absolute; left: -30px; top: 176px; width: 220px; text-align: center; font-size: 24px;
  font-weight: 700; letter-spacing: 0.14em; color: rgba(255,255,255,0.86); }
.sc15 { position: absolute; left: 10px; top: 222px; width: 140px; height: 52px; justify-content: center;
  font-size: 26px; }
.sk15 { position: absolute; left: 118px; top: -16px; width: 58px; height: 58px; }
.sk15 .sk { stroke: #fff; stroke-width: 3; }
""")


@beat("near")
def b15_stages():
    """«Тому якщо тобі важко знімати рілси, то просто скорочуй час на всі інші
    етапи, максимально спрощуй собі життя…»

    NEAR. A reel's four stages on a shelf — АНАЛІЗ, СЦЕНАРІЙ, МОНТАЖ, ЗЙОМКА —
    and what each costs in hours, on «важко». «скорочуй час»: the first three
    count down to minutes. «на всі інші етапи»: each of them turns jelly with
    a tick, one per word. «спрощуй собі життя»: the three fold away to the
    side and filming is what's left, in the middle. Gone before her closeup."""
    groups = []
    for i, (gl, lab, mins) in enumerate(STAGES):
        glyph = fill("bars") if gl == "bars" else stroke(gl)
        groups.append(u'<div class="sg15" id="sg15%d" style="left:%dpx">'
                      u'<div class="tw st15 hide" id="st15%d"><div class="clear">%s</div>'
                      u'<div class="jelly">%s<div class="sheen"></div></div></div>'
                      u'<div class="sl15 hide" id="sl15%d">%s</div>'
                      u'<div class="pill d sc15 hide" id="sc15%d"><span id="sn15%d">%d год</span></div>'
                      u'<div class="tw circ sk15 hide" id="sk15%d"><div class="jelly">%s</div></div></div>'
                      % (i, ST_L[i], i, glyph, glyph, i, lab, i, i, mins // 60, i, stroke("check")))
    html = u'''
      <div class="g full" id="g15">
        <div id="s15" class="shelf edge abs hide"><div class="sheen"></div></div>
        %s
      </div>''' % "\n        ".join(groups)
    src = js(u'''
  tl.set("#g15", {autoAlpha: 1}, @yakshcho2-0.06);
  arr("#s15", @yakshcho2-0.06, {s: 0.9, y: 24, d: 0.9, ease: SP});
  [0, 1, 2, 3].forEach(function (i) {
    arr("#st15" + i, @yakshcho2+0.04 + i * 0.08, {s: 0.5, y: 26});
    bin("#sl15" + i, @yakshcho2+0.3 + i * 0.08, 8, 0.3);
  });
  // «важко знімати рілси» — what each stage costs
  [0, 1, 2, 3].forEach(function (i) { pop("#sc15" + i, @vazhko + i * 0.09); });
  // «скорочуй час» — three of them drop to minutes
  [[0, 120], [1, 180], [2, 240]].forEach(function (p) {
    var o = {v: p[1]}, el = document.getElementById("sn15" + p[0]);
    tl.fromTo(o, {v: p[1]}, {v: 10, duration: 0.9, ease: "power2.inOut", immediateRender: false,
      onUpdate: function () { el.textContent = o.v >= 60 ? Math.round(o.v / 60) + " год" : Math.round(o.v) + " хв"; }},
      @skorochui + p[0] * 0.1);
  });
  G.bump(["#sc150", "#sc151", "#sc152"], @chas);
  // «на всі інші етапи» — they go automatic, one per word
  [@vsi4, @inshi, @etapy].forEach(function (t, i) {
    tl.to("#st15" + i + " .jelly", {opacity: 1, duration: 0.3, ease: "power1.out"}, t);
    G.bump("#st15" + i, t);
    pop("#sk15" + i, t + 0.08);
  });
  // «максимально спрощуй собі життя» — they fold away; filming is left
  // (labels and hours go first, so the folded three are just three ticked tiles)
  [[0, -40], [1, -170], [2, -300]].forEach(function (p) {
    tl.to(["#sl15" + p[0], "#sc15" + p[0]], {autoAlpha: 0, duration: 0.2}, @maks - 0.04);
    tl.to("#sg15" + p[0], {x: p[1], scale: 0.55, duration: 0.7, ease: SP}, @maks + p[0] * 0.05);
    tl.to("#sg15" + p[0], {autoAlpha: 0.7, duration: 0.5}, @maks + 0.2);
  });
  tl.to("#sg153", {x: -310, scale: 1.18, duration: 0.8, ease: SP}, @sproshchui-0.1);
  shn("#st153 .sheen", @sproshchui+0.3);
  G.bump("#st153", @zhyttia);
  tl.set("#g15", {autoAlpha: 0}, 63.100);''')
    return html, src


# ===================================================================== b17 ==
# The pipeline: AI analysis -> RUTA -> Claude -> her. Tiles in a row at the
# top, one product card under them that changes as it is handed along.
PT_L = [110, 340, 570, 800]
PT_Y, PT = 210, 170
PT_C = [(l + PT // 2, PT_Y + PT // 2) for l in PT_L]      # centres, y 295
FACE7 = (485, 840)             # her face in shot 7
S4 = 0.58                      # plate -> tile 4 scale
T4_GROW = 0.90
PC = (160, 520, 760, 600)      # the product card

k.css("""
/* ---- b17 · the pipeline ---- */
.pt17 { position: absolute; top: 210px; width: 170px; height: 170px; }
.pt17 .clear .sk, .pt17 .clear .fk, .pt17 .clear .mk, .pt17 .clear .wmark { opacity: 0.38; }
.pt17 .clear .wmark { color: #fff; }
.pt17 .lt { position: absolute; inset: 0; opacity: 0; }
#cab17 { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: visible; }
#t4win { position: absolute; inset: 0; clip-path: inset(210px 110px 1540px 800px round 40px); }
#t4v { transform-origin: 0 0; }
#t4rim { left: 800px; top: 210px; width: 170px; height: 170px; border-radius: 40px;
  box-shadow: inset 0 0 0 4px rgba(255,255,255,0.85), 0 36px 64px -22px rgba(30,4,12,0.55); }
#pc17w { left: 160px; top: 520px; width: 760px; height: 600px; transform-origin: 380px 0px; }
#pc17 { position: absolute; inset: 0; }
.ps17 { position: absolute; inset: 0; }
.th17 { position: absolute; top: 96px; width: 112px; height: 200px; border-radius: 20px; overflow: hidden;
  background: linear-gradient(170deg, #f6e8ed 0%, #e9ccd6 100%); box-shadow: inset 0 0 0 1.5px rgba(23,20,28,0.06); }
.th17 svg { position: absolute; left: 34px; top: 78px; width: 44px; height: 44px; fill: rgba(180,18,47,0.45); }
.vb17 { position: absolute; bottom: 60px; width: 112px; border-radius: 16px; transform-origin: 50% 100%;
  background: rgba(23,20,28,0.13); }
.vb17.top { background: linear-gradient(0deg, #8d0d24 0%, #d61a47 60%, #ff6e9c 100%); }
#top17 { left: 300px; top: 70px; height: 50px; padding: 0 18px 0 14px; font-size: 24px; background: #fbe3ea;
  color: #b4122f; }
#top17 svg { width: 24px; height: 24px; fill: none; stroke: #b4122f; stroke-width: 3; stroke-linecap: round; stroke-linejoin: round; }
.tp17 { left: 120px; width: 520px; height: 96px; padding: 0 34px 0 22px; font-size: 38px; background: #fbe3ea;
  color: #17141c; box-shadow: inset 0 2px 1px #fff; }
.tp17 svg { width: 44px; height: 44px; fill: none; stroke: #b4122f; stroke-width: 2.2; stroke-linecap: round; stroke-linejoin: round; }
#hk17 { left: 56px; top: 104px; width: 648px; font-size: 38px; font-weight: 700; line-height: 52px;
  letter-spacing: -0.01em; }
.sb17 { position: absolute; left: 56px; height: 22px; border-radius: 11px; background: rgba(23,20,28,0.12); }
#pv17 { left: 56px; top: 64px; width: 180px; height: 320px; border-radius: 26px; overflow: hidden;
  box-shadow: 0 20px 40px -18px rgba(20,2,8,0.5); }
.ck17 { position: absolute; top: 0; height: 56px; border-radius: 12px; }
.ck17.a { background: linear-gradient(90deg, #b4122f, #e0204b); }
.ck17.b { background: linear-gradient(90deg, #ff8ab0, #ff5c8f); }
.cc17 { position: absolute; top: 76px; height: 26px; border-radius: 8px; background: rgba(23,20,28,0.18); }
.wf17 { position: absolute; bottom: 0; width: 8px; border-radius: 4px; background: rgba(180,18,47,0.35); }
#tl17 { left: 276px; top: 140px; width: 430px; height: 170px; }
#ph17 { left: 276px; top: 120px; width: 6px; height: 210px; border-radius: 3px; background: #ff4f86;
  box-shadow: 0 0 12px rgba(255,79,134,0.8); }
#dn17 { left: 276px; top: 380px; height: 64px; padding: 0 26px 0 18px; font-size: 30px;
  background: linear-gradient(165deg, #e0204b 0%, #ab112e 55%, #7a0a20 100%); color: #fff; }
#dn17 svg { width: 34px; height: 34px; fill: none; stroke: #fff; stroke-width: 3; stroke-linecap: round; stroke-linejoin: round; }
""")


@beat("tk")
def b17_pipeline():
    """«У мене штучний інтелект аналізує контент, Рута допомагає знайти теми і
    перетворити думки на сценарій, Клод монтує відео за мене — і мені
    залишається лише встати перед вікном…»

    OVER, after her closeup. The iris opens on four ghost tiles in a row —
    the same four stages. «штучний інтелект»: tile 1 lights (analysis), and
    the card under it reads her last reels and picks the winner on
    «контент». «Рута»: the packet moves on, RUTA lights (captions drop for
    «Рута»); «знайти теми»: three topics; «думки на сценарій»: they fold into
    a script page that opens with this reel's own first line (captions drop
    for «сценарій»). «Клод»: Claude lights; «монтує відео»: an edit timeline,
    the playhead runs, done on «за мене». «і мені»: the last tile lights and
    it is her, live. «лише встати»: it grows until it is the frame."""
    t4a = S("i10") - 0.10
    t4b = S("lyshe") + T4_GROW + 0.02
    p_end = push_at(S("lyshe") + T4_GROW)
    tiles = []
    faces = [fill("bars"), Glass.wordmark("RUTA", size=46), g.mark("claude"), stroke("person")]
    mats = ["jelly", "pearl", "jelly", None]
    for i in range(4):
        lit = ('<div class="lt"><div class="%s">%s<div class="sheen"></div></div></div>'
               % (mats[i], faces[i])) if mats[i] else ""
        tiles.append('<div class="tw pt17 hide" id="pt17%d" style="left:%dpx"><div class="clear edge">%s</div>%s</div>'
                     % (i, PT_L[i], faces[i], lit))
        tiles.append('<div class="sqring hide" id="pr17%d" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></div>'
                     % (i, PT_L[i], PT_Y, PT, PT))
    cabs = []
    for i in range(3):
        x0, x1 = PT_L[i] + PT + 6, PT_L[i + 1] - 6
        d = "M %d %d L %d %d" % (x0, PT_C[0][1], x1, PT_C[0][1])
        cabs.append('<path class="tube" id="c17T%d" d="%s"/><path class="core" id="c17C%d" d="%s"/>'
                    '<g class="pkg"><path class="pkt hide" id="c17P%d" d="%s"/></g>' % (i, d, i, d, i, d))
    heights = [70, 104, 196, 82, 120]
    thumbs = "".join('<div class="th17" style="left:%dpx">%s</div>'
                     '<div class="vb17%s" id="vb17%d" style="left:%dpx;height:%dpx"></div>'
                     % (56 + i * 132, fill("play").replace('class="fk"', ''), " top" if i == 2 else "",
                        i, 56 + i * 132, h) for i, h in enumerate(heights))
    topics = "".join('<div class="pill tp17 hide" id="tp17%d" style="top:%dpx">%s<span>%s</span></div>'
                     % (i, 120 + i * 130, '<svg viewBox="0 0 24 24">%s</svg>' % STROKES["bulb"], t)
                     for i, t in enumerate([u"ШІ-двійники", u"Мій блог-сетап", u"Каруселі за 5 хв"]))
    bars = "".join('<div class="sb17" id="sb17%d" style="top:%dpx;width:%dpx"></div>'
                   % (i, 300 + i * 50, w) for i, w in enumerate([648, 610, 460, 280]))
    clips = []
    x = 0
    for i, w in enumerate([92, 58, 110, 70, 100]):
        clips.append('<div class="ck17 %s" style="left:%dpx;width:%dpx"></div>' % ("a" if i % 2 == 0 else "b", x, w - 6))
        x += w
    capblk = "".join('<div class="cc17" style="left:%dpx;width:%dpx"></div>' % (x0, w)
                     for x0, w in [(10, 60), (84, 44), (140, 76), (232, 52), (300, 90), (404, 20)])
    wave = "".join('<div class="wf17" style="left:%dpx;height:%dpx"></div>' % (i * 14, 10 + (i * 37 % 29))
                   for i in range(31))
    html = u'''
      <div class="g full" id="g17">
        <div class="tkc" id="tk17c">
          <svg id="cab17" class="cab" viewBox="0 0 1080 1920">%(cabs)s</svg>
          %(tiles)s
          <div id="pc17w" class="abs hide"><div id="pc17" class="sheet">
            <div class="ps17 hide" id="ps17a">
              <div class="cx t-micro" style="left:56px;top:38px">ОСТАННІ РІЛСИ</div>
              <div class="pill hide" id="top17">%(up)s<span>ТОП</span></div>
              %(thumbs)s
            </div>
            <div class="ps17 hide" id="ps17b">%(topics)s</div>
            <div class="ps17 hide" id="ps17c">
              <div class="cx t-micro" style="left:56px;top:42px">СЦЕНАРІЙ</div>
              <div class="cx" id="hk17">Пам'ятаєш, кілька місяців тому всі хайпили на темі штучних двійників…</div>
              %(bars)s
            </div>
            <div class="ps17 hide" id="ps17d">
              <div class="cx" id="pv17"><div class="studio"></div><div class="vw" style="%(pvxf)s">%(pv)s</div></div>
              <div class="cx" id="tl17">
                <div class="cx" style="left:0;top:0;width:430px;height:56px">%(clips)s</div>
                %(capblk)s
                <div class="cx" style="left:0;top:118px;width:430px;height:52px">%(wave)s</div>
              </div>
              <div class="cx" id="ph17"></div>
              <div class="pill hide" id="dn17">%(check)s<span>Готово</span></div>
            </div>
            <div class="sheen"></div>
          </div></div>
          <div id="t4win" class="hide"><div class="vw" id="t4v">%(v4)s</div></div>
          <div class="cx hide" id="t4rim"></div>
        </div>
      </div>''' % {
        "cabs": "".join(cabs), "tiles": "\n          ".join(tiles),
        "up": '<svg viewBox="0 0 24 24">%s</svg>' % STROKES["up"], "thumbs": thumbs, "topics": topics,
        "bars": bars, "clips": "".join(clips), "capblk": capblk, "wave": wave,
        "pvxf": frame_xf(140, 480, 640, 180), "pv": vid("v17p", "assets/base.mp4", S("montuie") - 0.1, 1.9, S("montuie") - 0.1),
        "check": '<svg viewBox="0 0 24 24">%s</svg>' % STROKES["check"],
        "v4": vid("v17t4", "assets/base.mp4", t4a, t4b - t4a, t4a)}
    src = js(u'''
  tl.set("#g17", {autoAlpha: 1}, @umene);
  gsap.set(".pt17 .lt", {opacity: 0});
  gsap.set("#t4v", {x: %(x0).2f, y: %(y0).2f, scale: %(s0).4f, transformOrigin: "0px 0px"});
  irisOpen("#tk17c", @umene, 540, 300, 0.8);
  G.drift("#tkG", @umene, 9.6);
  // four ghost tiles — the same four stages
  [0, 1, 2, 3].forEach(function (i) { arr("#pt17" + i, @umene+0.12 + i * 0.07, {s: 0.6, y: 20}); });
  [0, 1, 2].forEach(function (i) {
    G.drawPrep("c17T" + i); G.drawPrep("c17C" + i);
    tl.to(["#c17T" + i, "#c17C" + i], {strokeDashoffset: 0, duration: 0.4, ease: "power2.inOut"}, @umene+0.4 + i * 0.07);
  });
  function light(i, t) {
    tl.to("#pt17" + i + " .lt", {opacity: 1, duration: 0.3, ease: "power1.out"}, t);
    G.bump("#pt17" + i, t);
    G.ripple("#pr17" + i, t + 0.05);
    shn("#pt17" + i + " .lt .sheen", t + 0.2);
  }
  // «штучний інтелект аналізує контент»
  light(0, @shtuchnyi2);
  bin("#pc17w", @analizuie-0.06, 16, 0.45);
  tl.fromTo("#pc17w", {scale: 0.2, x: %(c1x)d, y: %(c1y)d}, {scale: 1, x: 0, y: 0, duration: 0.9, ease: spring(0.72, 12)}, @analizuie-0.06);
  tl.set("#ps17a", {autoAlpha: 1}, @analizuie-0.06);
  tl.fromTo("#ps17a .th17", {autoAlpha: 0, y: 20}, {autoAlpha: 1, y: 0, duration: 0.5, ease: SP, stagger: 0.06}, @analizuie+0.2);
  tl.fromTo(".vb17", {scaleY: 0}, {scaleY: 1, duration: 0.6, ease: SP, stagger: 0.07}, @kontent);
  pop("#top17", @kontent+0.4);
  // «Рута» — the packet moves on
  G.packet("c17P0", @ruta-0.3, 0.3);
  light(1, @ruta);
  // «допомагає знайти теми»
  tl.to("#ps17a", {autoAlpha: 0, duration: 0.25}, @dopomahaie);
  tl.set("#ps17b", {autoAlpha: 1}, @dopomahaie+0.1);
  [@znaity-0.1, @znaity+0.12, @temy].forEach(function (t, i) {
    arr("#tp17" + i, t, {s: 0.6, y: 20, d: 0.7});
  });
  // «перетворити думки на сценарій» — the topics fold into a script
  tl.to(".tp17", {scale: 0.3, y: -60, autoAlpha: 0, duration: 0.34, ease: "power2.in", stagger: 0.05}, @peretvoryty);
  tl.set("#ps17c", {autoAlpha: 1}, @peretvoryty+0.2);
  tl.fromTo("#hk17", {clipPath: "inset(0px 100%% 0px 0px)"}, {clipPath: "inset(0px 0%% 0px 0px)", duration: 0.7, ease: "power1.inOut"}, @dumky);
  tl.fromTo(".sb17", {scaleX: 0, transformOrigin: "0%% 50%%"}, {scaleX: 1, duration: 0.5, ease: SP, stagger: 0.07}, @stsenarii);
  G.bump("#pc17w", @stsenarii);
  // «Клод монтує відео за мене»
  G.packet("c17P1", @klod-0.3, 0.3);
  light(2, @klod);
  tl.to("#ps17c", {autoAlpha: 0, duration: 0.2}, @montuie);
  tl.set("#ps17d", {autoAlpha: 1}, @montuie+0.08);
  tl.fromTo("#tl17 .ck17, #tl17 .cc17", {scaleX: 0, transformOrigin: "0%% 50%%"}, {scaleX: 1, duration: 0.3, ease: "power2.out", stagger: 0.03}, @video-0.1);
  tl.fromTo("#tl17 .wf17", {scaleY: 0, transformOrigin: "50%% 100%%"}, {scaleY: 1, duration: 0.3, ease: "power2.out", stagger: 0.01}, @video);
  tl.fromTo("#ph17", {x: 0}, {x: 428, duration: 0.8, ease: "power1.inOut"}, @video);
  pop("#dn17", @mene);
  // «і мені залишається» — the packet reaches the last tile, and it is her
  G.packet("c17P2", @i10-0.1, 0.3);
  tl.to("#pc17w", {scale: 0.2, x: %(c4x)d, y: %(c4y)d, autoAlpha: 0, duration: 0.4, ease: "power3.in"}, @i10);
  tl.set(["#t4win", "#t4rim"], {autoAlpha: 1}, @meni-0.06);
  tl.fromTo("#t4win", {opacity: 0}, {opacity: 1, duration: 0.3, ease: "power1.out", immediateRender: false}, @meni-0.06);
  tl.set("#pt173", {autoAlpha: 0}, @meni+0.25);
  G.ripple("#pr173", @meni);
  // «лише встати перед вікном» — the tile grows until it is the frame
  tl.to("#t4win", {clipPath: "inset(0px 0px 0px 0px round 0px)", duration: %(g).2f, ease: "power3.inOut"}, @lyshe);
  tl.to("#t4v", {x: %(x1).2f, y: %(y1).2f, scale: %(s1).5f, duration: %(g).2f, ease: "power3.inOut"}, @lyshe);
  tl.to("#t4rim", {autoAlpha: 0, duration: 0.2}, @lyshe);
  tl.to(["#pt170", "#pt171", "#pt172", "#cab17"], {autoAlpha: 0, duration: 0.3}, @lyshe+0.1);
  tl.set(["#tkG", "#tk17c"], {autoAlpha: 0}, %(off).3f);
  tl.set("#g17", {autoAlpha: 0}, %(off).3f);''' % {
        "x0": PT_C[3][0] - FACE7[0] * S4, "y0": PT_C[3][1] - FACE7[1] * S4, "s0": S4,
        "x1": PUSH_O[0] * (1 - p_end), "y1": PUSH_O[1] * (1 - p_end), "s1": p_end, "g": T4_GROW,
        "c1x": PT_C[0][0] - (PC[0] + PC[2] // 2), "c1y": PT_C[0][1] - PC[1],
        "c4x": PT_C[3][0] - (PC[0] + PC[2] // 2), "c4y": PT_C[3][1] - PC[1],
        "off": S("lyshe") + T4_GROW + 0.01})
    return html, src


# ===================================================================== b18 ==
PROMPT = [[203, 204, 205], [206, 207, 208, 209], [210, 211, 212, 213, 214, 215], [216, 217, 218, 219]]
LH18 = 80

k.css("""
/* ---- b18 · the teleprompter ---- */
#pp18 { left: 70px; top: 96px; width: 940px; height: 400px; overflow: hidden; }
#cm18 { left: 455px; top: 20px; width: 30px; height: 30px; border-radius: 50%;
  background: radial-gradient(circle at 35% 35%, #4a4a5a 0%, #0b0b10 55%); box-shadow: 0 0 0 3px rgba(255,255,255,0.12); }
#cmr18 { left: 449px; top: 14px; width: 42px; height: 42px; border-radius: 50%; border: 3px solid rgba(255,140,180,0.95); }
#rc18 { left: 36px; top: 16px; height: 44px; padding: 0 16px 0 12px; font-size: 22px; letter-spacing: 0.06em; font-weight: 900; }
#rc18 i { width: 14px; height: 14px; border-radius: 50%; background: #ff3b5c; display: block; }
#lb18 { left: 0; top: 84px; width: 940px; height: 250px; overflow: hidden; }
#ln18 { left: 64px; top: 10px; width: 840px; }
.pl18 { height: 80px; line-height: 80px; font-size: 50px; font-weight: 700; letter-spacing: -0.01em; white-space: nowrap; }
.pw18 { color: rgba(255,255,255,0.30); }
#lm18 { left: 30px; top: 108px; width: 8px; height: 52px; border-radius: 4px; background: #ff6e9c;
  box-shadow: 0 0 14px rgba(255,110,156,0.8); }
""")


@beat("near")
def b18_prompter():
    """«…увімкнути фронтальну камеру і читати текст з суфлера. І я вважаю, що
    це набагато краще,»

    NEAR. What's left is hers: a teleprompter above her head, a front camera
    at its top that lights on «фронтальну камеру», REC. It reads along with
    her — each word lights as she says it, lines roll up — so the captions
    stand down for the whole stretch."""
    lines = []
    for li, idxs in enumerate(PROMPT):
        words = []
        for i in idxs:
            w = CAPS[i]["w"]
            if li == 3 and i == idxs[-1]:
                w = w + u"…"
            words.append('<span class="pw18" id="pw18_%d">%s</span>' % (i, w))
        lines.append('<div class="pl18">%s</div>' % " ".join(words))
    html = u'''
      <div class="g full" id="g18">
        <div id="pp18" class="dglass edge abs hide">
          <div class="pill d hide" id="rc18"><i></i>REC</div>
          <div class="cx hide" id="cmr18"></div>
          <div class="cx" id="cm18"></div>
          <div class="cx" id="lb18"><div class="cx" id="ln18">%s</div></div>
          <div class="cx" id="lm18"></div>
          <div class="sheen"></div>
        </div>
      </div>''' % "\n            ".join(lines)
    wl = []
    flat = [i for idxs in PROMPT for i in idxs]
    for n, i in enumerate(flat):
        if i > 216:
            break
        s = CAPS[i]["s"]
        wl.append('  tl.to("#pw18_%d", {color: "#ffffff", duration: 0.08}, %.3f);' % (i, s))
        nxt = CAPS[flat[n + 1]]["s"] if n + 1 < len(flat) else s + 0.4
        wl.append('  tl.to("#pw18_%d", {color: "rgba(255,255,255,0.62)", duration: 0.12}, %.3f);' % (i, nxt))
    src = js(u'''
  tl.set("#g18", {autoAlpha: 1}, @uvimknuty-0.08);
  arr("#pp18", @uvimknuty-0.08, {s: 0.9, y: -24, d: 0.8, ease: SP});
  // «фронтальну камеру» — the camera at the top comes on
  G.ripple("#cmr18", @frontalnu);
  tl.to("#cm18", {boxShadow: "0 0 0 3px rgba(255,140,180,0.9)", duration: 0.2}, @frontalnu);
  tl.fromTo("#rc18", {autoAlpha: 0, x: -16}, {autoAlpha: 1, x: 0, duration: 0.4, ease: POP, immediateRender: false}, @kameru);
  tl.to("#rc18 i", {keyframes: {opacity: [1, 0.25, 1, 0.25, 1]}, duration: 1.6, ease: "none"}, @chytaty);
WORDS
  // the lines roll up as she reads
  tl.to("#ln18", {y: -%(lh)d, duration: 0.36, ease: SP}, @i11-0.02);
  tl.to("#ln18", {y: -%(lh2)d, duration: 0.36, ease: SP}, @i12-0.02);
  tl.to("#ln18", {y: -%(lh3)d, duration: 0.36, ease: SP}, @krashche-0.02);
  shn("#pp18 .sheen", @vvazhaiu);
  // folds away as the sentence turns to the twin
  tl.to("#pp18", {y: -40, scale: 0.96, duration: 0.34, ease: "power2.in"}, @krashche_e);
  bout("#pp18", @krashche_e+0.04, 10, 0.3);
  tl.set("#g18", {autoAlpha: 0}, @krashche_e+0.38);''' % {"lh": LH18, "lh2": 2 * LH18, "lh3": 3 * LH18})
    return html, src.replace("WORDS", "\n".join(wl))


# ===================================================================== b19 ==
EYE7 = (480, 790)


@beat("behind")
def b19_clone_breaks():
    """«…ніж коли ти намагаєшся замінити себе двійником.»

    BEHIND. One grey copy of her flickers in beside her on «коли ти
    намагаєшся», steadies with its «AI» tag on «замінити себе», and breaks up
    on «двійником». Her matte (tw2) keeps her in front of it."""
    html = u'''
      <div class="g full" id="g19">
        <div class="cl" id="c19" style="transform-origin:%dpx %dpx"><div class="gray">%s</div>
          <div class="aic hide" id="c19ai" style="left:%dpx">AI</div></div>
      </div>''' % (EYE7[0], EYE7[1], vid("v19", HER0, 81.300, 2.40, 2.00), EYE7[0] - 80)
    src = js(u'''
  tl.set("#g19", {autoAlpha: 1}, 81.300);
  gsap.set("#c19", {x: 330, scale: 0.8});
  // «коли ти намагаєшся» — it flickers in
  tl.fromTo("#c19", {autoAlpha: 0}, {keyframes: {autoAlpha: [0, 0.55, 0.1, 0.75, 0.25, 0.92]}, duration: 0.5, ease: "none", immediateRender: false}, @koly);
  tl.to("#c19", {keyframes: {x: [330, 342, 322, 330]}, duration: 0.3, ease: "none"}, @koly);
  // «замінити себе» — it steadies, tagged
  tl.to("#c19", {x: 300, scale: 0.88, duration: 0.6, ease: SP}, @zaminyty);
  pop("#c19ai", @zaminyty+0.1);
  // «двійником» — and breaks up
  tl.to("#c19", {keyframes: {x: [300, 334, 276, 312, 300]}, duration: 0.16, ease: "none"}, @dviinykom);
  tl.to("#c19", {scaleY: 0.02, autoAlpha: 0, duration: 0.22, ease: "power2.in"}, @dviinykom+0.16);
  tl.set("#g19", {autoAlpha: 0}, @dviinykom+0.40);''')
    return html, src


# ===================================================================== b20 ==
k.css("""
/* ---- b20 · the IG poll sticker ---- */
#poll20 { left: 110px; top: 104px; width: 860px; height: 400px; border-radius: 52px; overflow: hidden;
  background: linear-gradient(172deg, #ffffff 0%, #fff9fb 60%, #fdf1f5 100%);
  box-shadow: inset 0 2px 1px #fff, inset 0 -24px 44px -26px rgba(180,18,47,0.16),
              0 50px 100px -36px rgba(20,2,8,0.7), 0 0 0 1px rgba(255,255,255,0.4); }
#pq20 { position: absolute; left: 0; right: 0; top: 52px; text-align: center; font-size: 56px; font-weight: 900;
  letter-spacing: -0.02em; color: #17141c; }
.po20 { position: absolute; top: 204px; width: 380px; height: 140px; border-radius: 70px;
  background: #f4edf0; box-shadow: inset 0 2px 5px rgba(120,10,30,0.07); }
.po20 b { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center;
  font-size: 46px; font-weight: 900; letter-spacing: -0.01em; color: #17141c; }
.po20 i { position: absolute; inset: 0; border-radius: 70px; box-shadow: inset 0 0 0 5px #ff4f86, 0 0 24px rgba(255,79,134,0.35);
  opacity: 0; }
""")


@beat("near")
def b20_poll():
    """«Але мені цікаво, хто пробував таких двійників і реально вписав їх в
    свою систему — це реально зручно, класно, швидко, дешево, і все, що ми
    сказали, чи насправді воно так і не є.»

    NEAR. An Instagram poll sticker lands above her head on «мені цікаво»:
    «Як тобі ШІ-двійники?» — Було зручно / Не пробувала (captions drop for
    «двійників»). «зручно» lights the first answer; «чи насправді» hands the
    light to the second. It stays to the last frame."""
    html = u'''
      <div class="g full" id="g20">
        <div id="poll20" class="abs hide">
          <div id="pq20">Як тобі ШІ-двійники?</div>
          <div class="po20 hide" id="po20a" style="left:40px"><i id="pi20a"></i><b>Було зручно</b></div>
          <div class="po20 hide" id="po20b" style="left:440px"><i id="pi20b"></i><b>Не пробувала</b></div>
          <div class="sheen"></div>
        </div>
      </div>'''
    src = js(u'''
  tl.set("#g20", {autoAlpha: 1}, @meni2-0.04);
  arr("#poll20", @meni2-0.04, {s: 0.55, y: -20});
  G.inner("#pq20", @tsikavo);
  // «хто пробував» — the two answers
  arr("#po20a", @probuvav, {s: 0.5, y: 14, d: 0.7});
  arr("#po20b", @probuvav+0.14, {s: 0.5, y: 14, d: 0.7});
  // «вписав їх в свою систему»
  G.bump("#poll20", @vpysav);
  shn("#poll20 .sheen", @vpysav+0.05);
  // «зручно»
  tl.to("#pi20a", {opacity: 1, duration: 0.2}, @zruchno);
  G.bump("#po20a", @zruchno);
  // «чи насправді … не є»
  tl.to("#pi20a", {opacity: 0, duration: 0.25}, @chy);
  tl.to("#pi20b", {opacity: 1, duration: 0.2}, @chy);
  G.bump("#po20b", @chy);
  G.haptic("#poll20", @ie2-0.1);''')
    return html, src


# ---------------------------------------------------------------------------
# Captions drop only on redundancy (STYLE.md §2b.1).
BLACKOUT = [
    (22.52, 23.26, u"b08a — the sheet reads ДВІЙНИК on «двійник»"),
    (67.92, 68.17, u"b17 — the tile reads RUTA on «Рута»"),
    (70.42, 71.23, u"b17 — the page reads СЦЕНАРІЙ on «сценарій»"),
    (75.38, 81.15, u"b18 — the teleprompter lights every word she reads"),
    (85.50, 86.03, u"b20 — the poll asks about ШІ-двійники on «двійників»"),
]
INVERT = []
KEEP_PLAQUE = [b for b in BLACKOUT if b[1] - b[0] < 2.0]   # short drops: the words go, the plaque stays


def push_js():
    return "\n".join([
        '  gsap.set(["#vid", ".matte"], {transformOrigin: "%dpx %dpx"});' % PUSH_O,
        '  tl.fromTo(["#vid", ".matte"], {scale: 1}, {scale: 1.045, duration: %.3f, ease: "none"}, 0);' % DUR,
    ])


def main():
    layers = {"behind": [], "near": [], "tk": [TK_GROUND]}
    gj = []
    for layer, fn in BEATS:
        h, j = fn()
        if h.strip():
            layers[layer].append(h.rstrip())
        gj.append("  /* %s */" % fn.__name__)
        gj.append(j.rstrip())
    gfx = "\n".join(layers["behind"] + layers["near"] + layers["tk"])
    doc = k.document(
        title=u"Reel 20 — штучні двійники",
        plate="assets/base.mp4",
        gfx_html=g.defs("".join(EXTRA_DEFS)) + "\n" + gfx,
        gfx_js="\n".join([g.js(), HEAD_JS, push_js()] + gj),
        caps=CAPS,
        blackout=BLACKOUT,
        invert=INVERT,
    )
    for a, b, _ in KEEP_PLAQUE:
        for line in ('  tl.to("#scrim", {autoAlpha: 0, duration: 0.20}, %.3f);\n' % (a - 0.20),
                     '  tl.to("#scrim", {autoAlpha: 1, duration: 0.25}, %.3f);\n' % b):
            assert line in doc, line
            doc = doc.replace(line, "", 1)
    out = os.path.join(HERE, "index.html")
    io.open(out, "w", encoding="utf-8").write(doc)
    print("index.html  %d captions, %d beats, %.1f KB"
          % (len(CAPS), len(BEATS), os.path.getsize(out) / 1024.0))


main()
