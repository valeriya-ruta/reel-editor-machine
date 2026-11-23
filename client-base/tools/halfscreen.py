# -*- coding: utf-8 -*-
"""Bake the half-screen beats into the plate (RULES.md §2c, Ruta's mockup).

    python tools/halfscreen.py 01        # reads reel-01/halves.json, rewrites reel-01/assets/base.mp4
    python tools/halfscreen.py 01 b03    # only these half-screens (to look at one before the rest are matted)

The half-screen: she slides down to make space, a flat panel fills the top,
and her head, cut out, sits in front of the panel's bottom edge. Done in the
browser with a transparent cut-out video on top, her face came out warmer
than the rest of her (the renderer converts transparent video differently:
skin +5 red, -14 blue, measured 2026-11-17). Ruta: "there is a clear
difference where it's natural and then there's more yellow".

So the half-screen is composed here, in ffmpeg, before the render: the
shifted plate, the panel ground, and her head *as her own plate pixels*,
with the cut-out (tools/matte.py) used only as a mask. Every pixel of her
comes from the same decode, so nothing can differ. The browser adds only the
panel's content (text, ticks) on top.

halves.json (written by the reel's build.py):
    [{"name": "b19", "t_in": 81.11, "t_out": 91.43, "shift": 480,
      "edge": 1080, "ground": "#RRGGBB", "matte_start": 81.0333}, ...]
t_in/t_out are plate seconds; the move in and out takes 5 frames each, inside
the span. The matte for each beat is reel-NN/assets/mattes/<name>.webm, cut by
tools/matte.py. Both read the plate as cut, voice.mp4 (sfx.py copies its video
stream into base.mp4 untouched), so a rerun always starts from her own frames
and never from an earlier bake; the sound is taken from base.mp4 as it is.
Order: build.py -> sfx.py mix -> matte.py -> halfscreen.py.
"""
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FPS = 30
MOVE = 5            # frames for her move down / back up


def run(cmd):
    p = subprocess.run(cmd)
    if p.returncode:
        sys.exit("failed: " + " ".join(cmd[:6]))


def nframes(path):
    return int(subprocess.check_output(
        ["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v:0",
         "-show_entries", "stream=nb_read_packets", "-of", "csv=p=0", path]).strip())


def half_graph(h, src_label, idx_matte, n_total):
    """filter chain for one half: returns (chain text, out label, f_in, f_out)"""
    f_in, f_out = int(round(h["t_in"] * FPS)), int(round(h["t_out"] * FPS))
    m0 = int(round(h["matte_start"] * FPS))
    n = f_out - f_in
    T = n / float(FPS)
    D = MOVE / float(FPS)
    S, E = int(h["shift"]), int(h["edge"])
    nm = h["name"]
    # ease-out on the way in, ease-in on the way out
    e1 = "(1-pow(1-min(t/%.4f\\,1)\\,2))" % D
    e2 = "pow(max(min((t-%.4f)/%.4f\\,1)\\,0)\\,2)" % (T - D, D)
    y_her = "%d*%s*(1-%s)" % (S, e1, e2)
    y_gnd = "-%d*(1-%s)-%d*%s" % (E, e1, E, e2)
    col = h["ground"].lstrip("#")
    chain = (
        "[{src}]trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS,split[{nm}s1][{nm}s2];"
        "[{im}:v]trim=start_frame={ma}:end_frame={mb},setpts=PTS-STARTPTS,format=yuva420p,"
        "alphaextract[{nm}m];"
        "[{nm}s2][{nm}m]alphamerge[{nm}head];"
        "color=c=black:s=1080x1920:r={fps}:d={T:.4f}[{nm}bg];"
        "color=c=0x{col}:s=1080x{E}:r={fps}:d={T:.4f}[{nm}gnd];"
        "[{nm}bg][{nm}s1]overlay=x=0:y='{yh}':eval=frame[{nm}c1];"
        "[{nm}c1][{nm}gnd]overlay=x=0:y='{yg}':eval=frame[{nm}c2];"
        "[{nm}c2][{nm}head]overlay=x=0:y='{yh}':eval=frame,trim=end_frame={n},format=yuv420p[{nm}out]"
    ).format(src=src_label, a=f_in, b=f_out, nm=nm, im=idx_matte, ma=f_in - m0, mb=f_out - m0,
             fps=FPS, T=T, col=col, E=E, yh=y_her, yg=y_gnd, n=n)
    return chain, nm + "out", f_in, f_out


def main():
    nn = sys.argv[1].zfill(2)
    reel = os.path.join(ROOT, "reel-" + nn)
    halves = json.load(open(os.path.join(reel, "halves.json")))
    if len(sys.argv) > 2:
        halves = [h for h in halves if h["name"] in sys.argv[2:]]
    base = os.path.join(reel, "assets", "base.mp4")
    flat = os.path.join(reel, "assets", "voice.mp4")
    n_total = nframes(flat)
    halves.sort(key=lambda h: h["t_in"])
    inputs = ["-i", flat, "-i", base]
    for h in halves:
        m = os.path.join(reel, "assets", "mattes", h["name"] + ".webm")
        if not os.path.exists(m):
            sys.exit("missing matte %s: run tools/matte.py first" % m)
        inputs += ["-c:v", "libvpx-vp9", "-i", m]
    splits = 2 * len(halves) + 1         # a gap and a half per beat, and the tail
    parts, chains = [], ["[0:v]split=%d%s" % (splits, "".join("[p%d]" % i for i in range(splits)))]
    cursor, k = 0, 0
    for i, h in enumerate(halves):
        chain, out, f_in, f_out = half_graph(h, "p%d" % k, i + 2, n_total)
        k += 1
        chains.append("[p%d]trim=start_frame=%d:end_frame=%d,setpts=PTS-STARTPTS[gap%d]" % (k, cursor, f_in, i))
        k += 1
        chains.append(chain)
        parts += ["[gap%d]" % i, "[%s]" % out]
        cursor = f_out
    chains.append("[p%d]trim=start_frame=%d,setpts=PTS-STARTPTS[tail]" % (k, cursor))
    parts.append("[tail]")
    chains.append("%sconcat=n=%d:v=1:a=0[v]" % ("".join(parts), len(parts)))
    tmp = base + ".tmp.mp4"
    run(["ffmpeg", "-nostdin", "-v", "error", "-y"] + inputs +
        ["-filter_complex", ";".join(chains), "-map", "[v]", "-map", "1:a", "-c:a", "copy",
         "-c:v", "libx264", "-crf", "15", "-preset", "medium", "-g", "30", "-keyint_min", "30",
         "-pix_fmt", "yuv420p", "-r", str(FPS), "-colorspace", "bt709", "-color_primaries", "bt709",
         "-color_trc", "bt709", "-movflags", "+faststart", tmp])
    got = nframes(tmp)
    if got != n_total:
        sys.exit("frame count changed: %d -> %d (kept the old plate)" % (n_total, got))
    os.replace(tmp, base)
    print("baked %d half-screen beat(s) into %s (%d frames)" % (len(halves), base, got))


if __name__ == "__main__":
    main()
