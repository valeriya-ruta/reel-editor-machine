# -*- coding: utf-8 -*-
"""Lift the long video's graphics into each reel, in sync.

    python3 leadmagnet/reels/rlv.py [k ...]   -> reels/rNN/lv.mp4

Every reel segment is a stretch of the raw take; the long video's EDL says
where that stretch landed in the 20-minute cut, and the beat render there
already has the drawing / fake screen for those exact words. So each segment's
frames are copied out of that beat render, cropped to the graphic (the
Excalidraw canvas, or the browser window without her camera square), and laid
end to end on the reel's own timeline. No graphics are redrawn.
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
LM = os.path.dirname(HERE)
sys.path.insert(0, LM)
from cut import src_to_out  # noqa: E402

EDL = json.load(open(os.path.join(LM, "edl.json")))
SCREEN = {"b08", "b10", "b11", "b12", "b13", "b14", "b15", "b18", "b19"}
CROP = {"theory": (0, 0, 1330, 1080, 1080, 878), "screen": (100, 40, 1080, 828, 1080, 828)}
KIND = {1: "screen", 2: "screen", 3: "theory", 4: "theory", 5: "theory", 6: "screen", 7: "theory", 8: "screen"}

BEATS = []
for b in sorted(os.listdir(os.path.join(LM, "beats"))):
    p = os.path.join(LM, "beats", b, "beat.json")
    if os.path.exists(p):
        j = json.load(open(p))
        BEATS.append((j["t0"], j["t1"], b))


def run(k):
    d = os.path.join(HERE, "r%02d" % k)
    cut = json.load(open(os.path.join(d, "cut.json")))
    x, y, w, h, ow, oh = CROP[KIND[k]]
    tmp = os.path.join(d, "lvtmp")
    os.makedirs(tmp, exist_ok=True)
    lst = []
    for i, s in enumerate(cut["segments"]):
        t = None
        for dt in [x * 0.05 for x in range(40)]:    # a segment can open inside a pause the long cut squeezed
            t = src_to_out(EDL, s["src"] + 0.02 + dt)
            if t is not None:
                t -= dt
                break
        f = os.path.join(tmp, "l%03d.mp4" % i)
        lst.append("file '%s'" % f)
        hit = [bt for bt in BEATS if t is not None and bt[0] - 1.0 <= t < bt[1] - 0.05]
        dur = s["nf"] / 30
        if hit:
            t0, t1, b = hit[0]
            src = os.path.join(LM, "beats", b, "out.mp4")
            lead = max(0.0, t0 - t)
            vf = ("crop=%d:%d:%d:%d,scale=%d:%d,fps=30,tpad=start_mode=clone:start_duration=%.3f:stop_mode=clone:stop_duration=30,format=yuv420p"
                  % (w, h, x, y, ow, oh, lead))
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "%.3f" % max(0.0, t - t0), "-i", src, "-frames:v", str(s["nf"]),
                            "-an", "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-g", "30", f], check=True)
        else:
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "color=c=white:s=%dx%d:r=30" % (ow, oh),
                            "-frames:v", str(s["nf"]), "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p", f], check=True)
    open(os.path.join(tmp, "list.txt"), "w").write("\n".join(lst) + "\n")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", os.path.join(tmp, "list.txt"),
                    "-c", "copy", os.path.join(d, "lv.mp4")], check=True)
    subprocess.run(["rm", "-rf", tmp])
    print("r%02d lv done (%s)" % (k, KIND[k]))


def lv_time(k, reel_t):
    """Long-video time shown at reel time reel_t (for authoring windows)."""
    cut = json.load(open(os.path.join(HERE, "r%02d" % k, "cut.json")))
    for s in cut["segments"]:
        a = s["out"] / 30
        if a <= reel_t < a + s["nf"] / 30:
            return src_to_out(EDL, s["src"] + (reel_t - a))
    return None


if __name__ == "__main__":
    ks = [int(a) for a in sys.argv[1:]] or sorted(KIND)
    for k in ks:
        run(k)
