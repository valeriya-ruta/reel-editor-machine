# -*- coding: utf-8 -*-
"""Reel NN template (BASE). Copy to reel-NN/ (tools/newreel.sh does), set NN,
write the beats.

The mechanics are Ruta's raw-take pipeline as built on Marina's reel 01
(2026-11-17): cut.json -> DUR, NO_PAINT from cut.py's closeups, captions from
align.py with FIX_AT for whisper's mishearings, short blocks merged, A()/X()
to put every beat on its word and off on the edit, her face measured on every
frame (face_flat.json) so every beat sits under her chin (`under()`), the
half-screen for what doesn't fit (`half()`, baked by tools/halfscreen.py),
`fit` checks against the subtitles, sfx cues, BLACKOUT only where a graphic's
own text says her words. RULES.md is the contract.

The LOOK (classes, sizes, colours, how things move) comes from tools/look.py
and LOOK.md. Nothing in this file is a design choice; the beats are invented
per script in the client's look.

usage: python build.py
   then: python ../tools/sfx.py mix NN
         python ../tools/matte.py reel-NN ...   (one per half-screen; main() prints them)
         python ../tools/halfscreen.py NN
"""
import io
import json
import os
import re
import sys

NN = "00"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
from kit import Kit, esc  # noqa: E402
from look import LOOK  # noqa: E402

WD = os.path.join(ROOT, "work", "r" + NN)
CUT = json.load(io.open(os.path.join(WD, "cut.json"), encoding="utf-8"))
FPS = 30
DUR = round(CUT["duration"], 3)   # check against the plate: (frames - 0.5) / 30
k = Kit(width=1080, height=1920, fps=FPS, duration=DUR)

# NO-PAINT: the closeups cut.py made («punch»). Captions only (RULES.md §4a).
NO_PAINT = [tuple(x) for x in CUT["no_paint"]]

# ---------------------------------------------------------------- captions
WORDS = k.load_captions(os.path.join(WD, "captions.json"))
# Whisper's mishearings, keyed by plate time (align.py kept her wording where
# it could not tell). None removes the word.   (plate time, u"right words")
FIX_AT = []
for _t, _new in FIX_AT:
    _c = min(WORDS, key=lambda c: abs(c["s"] - _t))
    assert abs(_c["s"] - _t) < 0.02, (_t, _c)
    _c["w"] = _new
WORDS = [c for c in WORDS if c["w"] is not None]
for _a, _b in zip(WORDS, WORDS[1:]):
    _a["e"] = round(max(_a["s"] + 0.10, _b["s"] - 0.085), 3)
CAPS = k.captions(WORDS)         # what is on screen, in her caption mode (LOOK.md §2b)

# A block under 0.3 s flashes; merge it into a neighbour (by plate time).
MERGE_PREV = []
MERGE_NEXT = []


def _merge(caps):
    out = [dict(c) for c in caps]
    for t in MERGE_NEXT:
        i = next(i for i, c in enumerate(out) if abs(c["s"] - t) < 0.02)
        out[i + 1]["w"] = out[i]["w"] + " " + out[i + 1]["w"]
        out[i + 1]["words"] = out[i].get("words", []) + out[i + 1].get("words", [])
        out[i + 1]["s"] = out[i]["s"]
        del out[i]
    for t in MERGE_PREV:
        i = next(i for i, c in enumerate(out) if abs(c["s"] - t) < 0.02)
        out[i - 1]["w"] += " " + out[i]["w"]
        out[i - 1]["words"] = out[i - 1].get("words", []) + out[i].get("words", [])
        out[i - 1]["e"] = out[i]["e"]
        del out[i]
    for x, y in zip(out, out[1:]):     # never two blocks at once (RULES.md §2b)
        x["e"] = round(max(x["s"] + 0.10, min(x["e"], y["s"] - 0.085)), 3)
    return out


CAPS = _merge(CAPS)


def blk(t):
    """the caption block on screen at plate time t"""
    return max((c for c in CAPS if c["s"] <= t + 0.02), key=lambda c: c["s"])


# Only where a graphic's own text says the words she is saying (RULES.md §2b.1).
BLACKOUT = []
INVERT = []   # light takeovers: captions in ink


def bo(*times):
    for t in times:
        c = blk(t)
        BLACKOUT.append((c["s"] - 0.005, c["s"] + 0.005, ""))


def split_cap(t):
    """Split the subtitle block at the word she starts at plate time t, so a
    graphic can take that word's place on its own (RULES.md §2b.1)."""
    i = next(i for i, c in enumerate(CAPS) if c["s"] < t - 0.02 and c["e"] >= t)
    c = CAPS[i]
    ws = [w for w in WORDS if c["s"] - 0.02 <= w["s"] < t - 0.02]
    n = sum(len(w["w"].split()) for w in ws)
    tok = c["w"].split()
    cw = c.get("words", [])
    CAPS[i:i + 1] = [{"w": " ".join(tok[:n]), "s": c["s"], "e": round(t - 0.085, 3), "words": cw[:n]},
                     {"w": " ".join(tok[n:]), "s": round(t, 3), "e": c["e"], "words": cw[n:]}]


SFX = []


def sfx(name, t, db=0):
    """Quiet, on the event, never on a closeup (tools/sfx.py)."""
    if any(a <= t < b for a, b in NO_PAINT):
        return
    SFX.append({"t": round(max(0.0, t), 3), "name": name, "db": db})


# ---------------------------------------------------------------- timing
LEAD = LOOK.get("lead", 0.10)      # first frame this long before the word
EDGES = [round(c["tl"], 3) for c in CUT["clips"]][1:]   # the jump cuts


def A(t):
    """arrival: LEAD before the word at plate time t"""
    return round(t - LEAD, 3)


def X(t, win=0.25):
    """exit: at the end of the phrase, on the jump cut if one is that close"""
    e = min(EDGES, key=lambda c: abs(c - t))
    return e if abs(e - t) <= win else t


def T(x):
    return "%.3f" % x


def show(g, t):
    return 'tl.set("#%s", {autoAlpha: 1}, %s);' % (g, T(t))


def hide(g, t):
    return 'tl.set("#%s", {autoAlpha: 0}, %s);' % (g, T(t))


def J(*parts):
    return "\n".join("        " + p for p in parts)


# ---------------------------------------------------------------- her face (Ruta, 2026-11-17)
# "make sure that nothing is going on her face ... They should always go under
# her chin or behind her head." face_flat.json: tools/facemap.py NN --flat,
# her face on the plate as cut, 10 samples a second.
_FF = os.path.join(WD, "face_flat.json")
FACE = json.load(io.open(_FF, encoding="utf-8")) if os.path.exists(_FF) else []
PAD = 30           # air between her chin and the first pixel of a graphic


def _near(t0, t1):
    rs = [r for r in FACE if t0 - 0.15 <= r["t"] <= t1 + 0.15]
    assert rs, "run tools/facemap.py %s --flat first" % NN
    return rs


def chin(t0, t1):
    """the lowest her chin goes while t0..t1 is on screen"""
    return max(r["chin"] for r in _near(t0, t1))


def hair(t0, t1):
    """the highest the top of her hair goes over t0..t1 (from eyes and chin)"""
    return int(min(r["eyes"] - 0.85 * (r["chin"] - r["eyes"]) for r in _near(t0, t1)))


def under(t0, t1):
    """first free y under her chin for a graphic up over t0..t1"""
    return int(round(chin(t0, t1) + PAD))


def head(t0, t1):
    rs = _near(t0, t1)
    return (min(r["box"][0] for r in rs), hair(t0, t1), max(r["box"][2] for r in rs), chin(t0, t1))


# A beat under her chin must also clear the subtitles: main() checks every
# beat's lowest pixel against the subtitle blocks on screen with it.
FIT = []


def fit(name, t0, t1, bottom):
    FIT.append((name, t0, t1, bottom))


# ---------------------------------------------------------------- half-screen (RULES.md §2c)
HALVES = []
EDGE = 1080          # the panel's bottom edge, behind her head (Ruta's mockup)
TOP = 262            # panel content starts inside the safe area (RULES.md §3a)


def half(name, t_in, t_out, content_bottom, ground):
    """register a half-screen; returns how far she moves down. `ground` is
    the panel colour from the client's look."""
    shift = max(480, int(content_bottom + 40 - hair(t_in, t_out)))
    assert shift < EDGE - 200, (name, shift)
    f0 = int((t_in - 0.05) * FPS)
    f1 = int(round((t_out + 0.05) * FPS)) + 1
    HALVES.append({"name": name, "t_in": round(t_in, 3), "t_out": round(t_out, 3),
                   "shift": shift, "edge": EDGE, "ground": ground,
                   "matte_start": round(f0 / float(FPS), 4),
                   "matte_cmd": "python tools/matte.py reel-%s %.2f %.2f %s" % (NN, t_in - 0.05, t_out + 0.05, name),
                   "_frames": (f0, f1)})
    for c in CAPS:                       # subtitles stand down for the span
        if c["s"] < t_out and c["e"] > t_in:
            if c["s"] < t_in - 0.3:
                c["e"] = round(t_in, 3)
            elif c["e"] > t_out + 0.3:
                c["s"] = round(t_out, 3)
            else:
                BLACKOUT.append((c["s"] - 0.005, c["s"] + 0.005, ""))
    return shift


# ---------------------------------------------------------------- beats
L = []        # graphic html
BEATS = []    # functions returning gsap js


def beat(fn):
    BEATS.append(fn)
    return fn


# (write the beats here, in the client's look: tools/look.py, LOOK.md)


# ---------------------------------------------------------------- checks + output
_LH = 1.1 * k.cap_size                       # one caption line
_CAP_BOTTOM = k.cap_y + k.cap_size // 2      # captions are bottom-anchored here


def check_fit():
    """every beat under her chin clears the subtitles on screen with it"""
    bad = 0
    for name, t0, t1, bottom in FIT:
        lim, why = 1470, "safe area"
        for c in CAPS:
            if any(a <= c["s"] < b for a, b, _ in BLACKOUT):
                continue
            if c["s"] < t1 - 0.034 and c["e"] > t0 + 0.034:     # a frame of slack
                lines = 2 if len(c["w"]) > LOOK.get("max_chars", 34) else 1
                top = int(_CAP_BOTTOM - lines * _LH)
                if top - 10 < lim:
                    lim, why = top - 10, u"subtitle «%s»" % c["w"]
        if bottom > lim:
            bad += 1
            print(u"  ! %s bottom %d > %d (%s)" % (name, bottom, lim, why))
    print("fit: %d beat(s) under her chin, %d too low" % (len(FIT), bad))


def main():
    gj = []
    for fn in BEATS:
        gj.append("  /* %s */" % fn.__name__)
        gj.append(fn().rstrip())
    doc = k.document(
        title=u"reel " + NN,
        plate="assets/base.mp4",
        gfx_html="\n".join(L),
        gfx_js="\n".join(gj),
        caps=CAPS,
        blackout=BLACKOUT,
        invert=INVERT,
    )
    io.open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(doc)
    SFX.sort(key=lambda c: c["t"])
    io.open(os.path.join(HERE, "sfx.json"), "w", encoding="utf-8").write(json.dumps(SFX, indent=1))
    io.open(os.path.join(HERE, "halves.json"), "w", encoding="utf-8").write(
        json.dumps([{k_: v for k_, v in h.items() if not k_.startswith("_")} for h in HALVES], indent=1))
    print("index.html  %d captions, %d beats, %d sfx cues, %d blackouts, %d half-screens"
          % (len(CAPS), len(BEATS), len(SFX), len(BLACKOUT), len(HALVES)))
    check_fit()
    for h in HALVES:
        have = os.path.exists(os.path.join(HERE, "assets", "mattes", h["name"] + ".webm"))
        print("half %-4s shift %d  matte %s  %s" % (h["name"], h["shift"], "ok     " if have else "MISSING",
                                                   h["matte_cmd"]))


main()
