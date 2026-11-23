# -*- coding: utf-8 -*-
"""Find the spans where she pushes the frame back, so graphics stay off them.

    python tools/pullouts.py reel-07

`tools/shots.py` finds her *cuts*. This finds her *zooms*, which is a different
and sneakier thing: on reel 7 she pulls the camera way out across 11.0–14.7s
while she lists everything you stop knowing, and because it is a smooth scale
inside one continuous shot, scene detection never sees it. A graphic went
straight over the joke.

Her rule, 2026-09-14:

    "when you see some funny editing (extra closeup, extra far away) those are
     funny bits and dont paint over them"

What every pull-out has in common is letterboxing: the plate shrinks and black
appears around its edge. So sample the border luminance across the reel and
call anything much darker than the reel's own median a pull-out. That is robust
to her grade, to the room, and to the time of day, because the reel is measured
against itself rather than against an absolute threshold.

Prints the spans and writes work/rNN/pullout-spans.json. Feed them into the
build's NO_PAINT list alongside the short inserts from shots.py.
"""
import io
import json
import os
import subprocess
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FPS = 4                # a gag she holds long enough to read is >= 0.5 s
BORDER = 4             # px of the sampled picture-frame, on the 120px proxy
RATIO = 0.55           # darker than 55% of the reel's median = pushed back
MIN_SPAN = 0.40
GAP = 0.50             # spans closer than this are one span


def main():
    reel = sys.argv[1] if len(sys.argv) > 1 else "reel-07"
    work = os.path.join(ROOT, "work", "r" + reel.split("-")[-1])
    plate = os.path.join(ROOT, reel, "assets", "base.mp4")
    if not os.path.exists(plate):
        sys.exit("no plate: " + plate)

    tmp = os.path.join(work, "_pullout")
    if not os.path.isdir(tmp):
        os.makedirs(tmp)
    for f in os.listdir(tmp):
        os.remove(os.path.join(tmp, f))

    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", plate,
                    "-vf", "fps=%d,scale=120:-1" % FPS, "-y",
                    os.path.join(tmp, "f%05d.jpg")], check=True)

    rows = []
    for i, f in enumerate(sorted(os.listdir(tmp))):
        im = Image.open(os.path.join(tmp, f)).convert("L")
        w, h = im.size
        px = im.load()
        vals = []
        for x in range(w):
            for y in list(range(BORDER)) + list(range(h - BORDER, h)):
                vals.append(px[x, y])
        for y in range(h):
            for x in list(range(BORDER)) + list(range(w - BORDER, w)):
                vals.append(px[x, y])
        rows.append((i / float(FPS), sum(vals) / float(len(vals))))

    med = sorted(r[1] for r in rows)[len(rows) // 2]
    spans, cur = [], None
    for t, v in rows:
        if v < med * RATIO:
            if cur and t - cur[1] <= GAP:
                cur[1] = t
            else:
                if cur:
                    spans.append(cur)
                cur = [t, t]
    if cur:
        spans.append(cur)
    spans = [[a, b + 1.0 / FPS] for a, b in spans if b + 1.0 / FPS - a >= MIN_SPAN]

    for f in os.listdir(tmp):
        os.remove(os.path.join(tmp, f))
    os.rmdir(tmp)

    print("median border luminance %.1f over %d samples" % (med, len(rows)))
    if not spans:
        print("no pull-outs found")
    for a, b in spans:
        print("  %7.2f - %7.2f  (%.2fs)" % (a, b, b - a))
    io.open(os.path.join(work, "pullout-spans.json"), "w").write(
        json.dumps([[round(a, 2), round(b, 2)] for a, b in spans], indent=1))


main()
