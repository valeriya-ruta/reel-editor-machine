# -*- coding: utf-8 -*-
"""Find her cuts, and show one frame per shot, so graphics stay off her jokes.

    python tools/shots.py reel-07

Her delivered plate is already edited, and the edit carries meaning: she punches
in for emphasis and pulls way out for a joke. Her note, 2026-09-14:

    "when you see some funny editing (extra closeup, extra far away) those are
     funny bits and dont paint over them"

So a shot change is not just a cut, it is an instruction. This finds them with
ffmpeg scene detection, writes one frame per shot, and tiles them into a single
contact sheet — one image to read instead of fifteen.

Output, under work/<reel>/shots/:
    shots.json   [{i, start, end, dur}]
    sheet.jpg    the contact sheet, numbered in shot order

What it deliberately does NOT do is classify the shots. Whether a pull-out is a
joke or just a breath is a judgement about her comedy, and the contact sheet is
there to make that judgement cheap rather than to replace it.
"""
import io
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THRESH = 0.22          # scene score; her cuts are hard, this is well clear of noise
MIN_SHOT = 0.40        # ignore anything shorter — a flash is not a shot


def probe_duration(path):
    out = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=nw=1:nk=1", path], cwd=ROOT)
    return float(out.strip())


def find_cuts(plate):
    """ffmpeg prints one showinfo line per frame that scores above THRESH."""
    p = subprocess.run(
        ["ffmpeg", "-nostdin", "-v", "info", "-i", plate,
         "-vf", "select='gt(scene,%s)',showinfo" % THRESH, "-an",
         "-f", "null", "-"],
        cwd=ROOT, stderr=subprocess.PIPE, stdout=subprocess.DEVNULL)
    err = p.stderr.decode("utf-8", "replace")
    times = [float(m) for m in re.findall(r"pts_time:([0-9.]+)", err)]
    return sorted(set(times))


def main():
    reel = sys.argv[1] if len(sys.argv) > 1 else "reel-07"
    work = os.path.join(ROOT, "work", "r" + reel.split("-")[-1])
    plate = os.path.join(reel, "assets", "base.mp4")
    if not os.path.exists(os.path.join(ROOT, plate)):
        sys.exit("no plate: " + plate)

    dur = probe_duration(os.path.join(ROOT, plate))
    cuts = [t for t in find_cuts(plate) if MIN_SHOT < t < dur - MIN_SHOT]

    bounds = [0.0] + cuts + [dur]
    shots = []
    for i in range(len(bounds) - 1):
        a, b = bounds[i], bounds[i + 1]
        if b - a < MIN_SHOT:
            continue
        shots.append({"i": len(shots), "start": round(a, 3),
                      "end": round(b, 3), "dur": round(b - a, 3)})

    out = os.path.join(work, "shots")
    if not os.path.isdir(out):
        os.makedirs(out)

    # one frame from the middle of each shot, where the framing has settled
    for s in shots:
        mid = s["start"] + s["dur"] / 2.0
        subprocess.run(
            ["ffmpeg", "-nostdin", "-v", "error", "-ss", "%.3f" % mid,
             "-i", plate, "-frames:v", "1", "-vf", "scale=216:-1",
             "-y", os.path.join(out, "s%02d.jpg" % s["i"])],
            cwd=ROOT, check=True)

    # tile them into one sheet: cheaper to read than N separate images
    n = len(shots)
    cols = min(6, max(1, n))
    subprocess.run(
        ["ffmpeg", "-nostdin", "-v", "error", "-i",
         os.path.join(out, "s%02d.jpg"), "-frames:v", "1",
         "-vf", "tile=%dx%d:padding=6:margin=6:color=0x141018"
         % (cols, (n + cols - 1) // cols),
         "-y", os.path.join(out, "sheet.jpg")],
        cwd=ROOT, check=True)

    io.open(os.path.join(out, "shots.json"), "w", encoding="utf-8").write(
        json.dumps(shots, indent=1))

    print("%d shots over %.2fs" % (n, dur))
    for s in shots:
        print("  %2d  %7.2f - %7.2f  (%5.2fs)" % (s["i"], s["start"],
                                                  s["end"], s["dur"]))
    print("\nsheet: %s" % os.path.join(out, "sheet.jpg"))


main()
