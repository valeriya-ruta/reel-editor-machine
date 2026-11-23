# -*- coding: utf-8 -*-
"""Reel 56 — «Презентація з Клодом за 5 хвилин». Cut + captions only (her
call for this one: "simple editing today, minimal animations, just
cutting+subtitles"), in the RUTA look's caption rail (STYLE.md §00, her
review of reel 41: word by word, upper case, Product Sans Black, white on
the underlay plaque).

The plate is cut by work/r56/mkplate.py from four phone clips; captions are
work/r56/captions.json (work/r56/captions.py). No graphics, no sound cues,
no push on the plate.

usage: python3 build.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))
from gstyle import G, load_caps  # noqa: E402

NN = "56"
# plate length from the cut (work/r56/mkplate.py): 1431 frames = 47.7 s before any voiceover growth
DUR = round(json.load(open(os.path.join(ROOT, "work", "r56", "pieces.out.json")))[-1]["t1"], 4)
g = G(dur=DUR, reel=NN)
CAPS = load_caps(NN)


def main():
    chunks = g.chunks(CAPS)
    doc = g.document(title=u"Reel 56 — Презентація з Клодом", plate="assets/base.mp4",
                     chunks=chunks, push=False)
    g.write(HERE, doc)
    print("index.html  %d words, %d sfx cues" % (sum(len(c["words"]) for c in chunks), len(g.cues)))


main()
