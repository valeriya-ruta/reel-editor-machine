# -*- coding: utf-8 -*-
"""Reel 41 final: plate + rendered animation windows + subtitles -> one MP4.

    python work/demo/final.py            # plate + whatever windows are rendered + subs
    python work/demo/final.py --plain    # plate + subs only (the first cut she watches)

The long video is not rendered end to end in HyperFrames. Only the windows that
carry a graphic are (demo/w/<name>/, each a composition over its own slice
of the plate), and they are laid back over the plate here, frame-exact, so a
window's first and last frames are the plate itself. Subtitles go on last, as
.ass through libass, so they sit over b-roll and graphics alike.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
REEL = os.path.join(ROOT, "demo")
FPS = 30


def main():
    plain = "--plain" in sys.argv
    plate = os.path.join(REEL, "assets", "voice.mp4")
    out = os.path.join(REEL, "renders", "DEMO%s.mp4" % ("-cut" if plain else ""))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    wins = []
    if not plain and os.path.exists(os.path.join(REEL, "windows.json")):
        for w in json.load(open(os.path.join(REEL, "windows.json"))):
            mp4 = os.path.join(REEL, "w", w["name"], "renders", "out.mp4")
            if os.path.exists(mp4):
                wins.append((w, mp4))
            else:
                print("not rendered, skipped:", w["name"])
    cmd = ["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", plate]
    for _, mp4 in wins:
        cmd += ["-i", mp4]
    g, last = [], "0:v"
    for k, (w, _) in enumerate(wins, 1):
        a, b = w["f0"], w["f0"] + w["frames"]
        # the window's final rendered frame repeats the plate frame before it
        # (data-duration is frames - 0.5), so it is trimmed and the plate
        # supplies that frame. No `enable`: with `n` it silently disables the
        # overlay; the timestamps alone put each window in place.
        g.append("[%d:v]trim=end_frame=%d,setpts=PTS-STARTPTS+%d/(%d*TB)[w%d]" % (k, b - a - 1, a, FPS, k))
        g.append("[%s][w%d]overlay=0:0:eof_action=pass:repeatlast=0[o%d]" % (last, k, k))
        last = "o%d" % k
    fonts = os.path.join(ROOT, "assets", "fonts")
    g.append("[%s]ass=%s:fontsdir=%s,format=yuv420p[v]" % (last, os.path.join(HERE, "captions.ass"), fonts))
    cmd += ["-filter_complex", ";".join(g), "-map", "[v]", "-map", "0:a",
            "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p", "-r", str(FPS),
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    fr = subprocess.run(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v",
                         "-show_entries", "stream=nb_read_packets", "-of", "csv=p=0", out],
                        capture_output=True, text=True).stdout.strip()
    print("OUT %s  frames %s  windows %d" % (out, fr, len(wins)))


if __name__ == "__main__":
    main()
