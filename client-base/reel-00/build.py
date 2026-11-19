# -*- coding: utf-8 -*-
"""Reel NN template. Copy this folder to reel-NN/, set NN, write the beats.

Skeleton taken from Ruta's reel-21/build.py (the worked example of her raw-take
pipeline): cut.json -> DUR, NO_PAINT from the closeups cut.py made, captions
from align.py with a FIX dict for whisper's mishearings, S()/E() to anchor
every beat on its word, @name times in js(), sfx() cues, BLACKOUT only where a
graphic's own text repeats her words. The look is the client's
(tools/look.py, LOOK.md); the rules are RULES.md; the beats are invented per
script.

usage: python build.py   (then: python ../tools/sfx.py mix NN)
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

WD = os.path.join(ROOT, "work", "r" + NN)
CUT = json.load(io.open(os.path.join(WD, "cut.json"), encoding="utf-8"))
FPS = 30
DUR = round(CUT["duration"], 3)   # check against the plate: (frames - 0.5) / 30
k = Kit(width=1080, height=1920, fps=FPS, duration=DUR)

# NO-PAINT: the closeups cut.py made («punch»). Captions only (RULES.md §4a).
NO_PAINT = [tuple(x) for x in CUT["no_paint"]]

# Word timings, spelling from her transcript (align.py). Fix whisper here.
WORDS = k.load_captions(os.path.join(WD, "captions.json"))
FIX = {}
for c in WORDS:
    c["w"] = FIX.get(c["w"], c["w"])
for _a, _b in zip(WORDS, WORDS[1:]):
    _a["e"] = round(max(_a["s"] + 0.10, _b["s"] - 0.085), 3)
CAPS = k.captions(WORDS)         # what is on screen, in her caption mode (LOOK.md §2b)


def _n(s):
    return "".join(ch for ch in s.lower() if ch.isalnum())


def S(word, near):
    hits = [c for c in WORDS if _n(word) == _n(c["w"])]
    c = min(hits, key=lambda c: abs(c["s"] - near))
    assert abs(c["s"] - near) < 0.6, (word, near, c["s"])
    return c["s"]


def E(word, near):
    hits = [c for c in WORDS if _n(word) == _n(c["w"])]
    return min(hits, key=lambda c: abs(c["s"] - near))["e"]


T = {"dur": DUR}                 # "name": S(u"слово", approx_time), ...


def js(src, **extra):
    """`@name`, `@name+0.12`, `@name-0.1` -> one literal time."""
    vals = dict(T)
    vals.update(extra)

    def rep(m):
        v = vals[m.group(1)] + (float(m.group(2)) if m.group(2) else 0.0)
        return "%.3f" % v
    return re.sub(r"@(\w+)([+-]\d+(?:\.\d+)?)?", rep, src)


SFX = []


def sfx(name, t, db=0):
    """Quiet, on the event, never on a closeup (tools/sfx.py)."""
    if any(a <= t < b for a, b in NO_PAINT):
        return
    SFX.append({"t": round(max(0.0, t), 3), "name": name, "db": db})


L = []        # graphic html
BEATS = []    # functions returning gsap js


def span_words(a, b):
    return (a, b, "")


# Only where a graphic's own text says the word she is saying (§2b.1).
BLACKOUT = []
INVERT = []   # light takeovers: captions in ink


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
    print("index.html  %d captions, %d beats, %d sfx cues" % (len(CAPS), len(BEATS), len(SFX)))


main()
