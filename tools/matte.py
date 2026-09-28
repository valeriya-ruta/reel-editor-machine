# -*- coding: utf-8 -*-
"""Cut a span of her footage out of its background, so a graphic can sit
*behind* her instead of on top of her head.

    py -3.10 tools/matte.py reel-04 28.70 30.70 mobbin

Writes reel-04/assets/mattes/mobbin.webm — a transparent VP9 clip of just her
for those two seconds — and prints the three numbers the beat needs.

Why this exists, and why it is per-beat: background removal runs on the CPU at
about 1.75 s/frame on her laptop (re-measured 2026-09-15 over 226 frames;
the earlier 3.3 figure was pessimistic. Her Vega 10 gives ONNX no
GPU provider). A 2-second beat is ~4 minutes, which is free and invisible. A
whole reel is closer to two hours, which is not. STYLE.md §1 has the rule: matte
the beats where something big goes behind her, never the reel.

Frame alignment is the thing that can go wrong. The matte plays over the *same*
base plate at the *same* time, so a one-frame slip shows as a shimmering ghost
along her edge. That is why the cut is made with a frame-index trim rather than
a timestamp seek — `-ss` lands on whatever the decoder decides is closest, and
"closest" is not good enough here.
"""
import io
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NPX = os.path.join(os.environ.get("APPDATA", ""), "npm", "npx.cmd")


def run(cmd, **kw):
    p = subprocess.run(cmd, cwd=ROOT, **kw)
    if p.returncode:
        sys.exit("failed: %s" % " ".join(cmd[:3]))
    return p


def probe(path):
    out = subprocess.check_output([
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=r_frame_rate,nb_frames,width,height",
        "-of", "json", path], cwd=ROOT)
    s = json.loads(out.decode("utf-8", "replace"))["streams"][0]
    num, den = s["r_frame_rate"].split("/")
    return float(num) / float(den), int(s["width"]), int(s["height"])


def main():
    if len(sys.argv) < 5:
        sys.exit(__doc__)
    reel, start, end, name = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]

    base = os.path.join(reel, "assets", "base.mp4")
    if not os.path.exists(os.path.join(ROOT, base)):
        sys.exit("no such plate: " + base)
    fps, w, h = probe(base)

    # Round outward: better a frame of slack at each end than a frame missing
    # in the middle of the beat.
    f0, f1 = int(start * fps), int(round(end * fps)) + 1
    n = f1 - f0
    mins = n * 3.3 / 60.0

    out_dir = os.path.join(ROOT, reel, "assets", "mattes")
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    span = os.path.join(out_dir, "_%s_span.mp4" % name)
    webm = os.path.join(out_dir, "%s.webm" % name)

    print("%s  frames %d-%d (%d @ %.3f fps, %dx%d)" % (name, f0, f1, n, fps, w, h))
    print("  about %.1f min on the CPU" % mins)

    # Frame-exact, decoded from the top. The plate is short enough that not
    # seeking costs less than a misaligned matte does.
    run(["ffmpeg", "-v", "error", "-i", base,
         "-vf", "trim=start_frame=%d:end_frame=%d,setpts=PTS-STARTPTS" % (f0, f1),
         "-an", "-c:v", "libx264", "-crf", "16", "-preset", "veryfast",
         "-y", span])

    got = probe(span)
    cut_frames = int(subprocess.check_output([
        "ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames",
        "-show_entries", "stream=nb_read_frames", "-of",
        "default=nw=1:nk=1", span], cwd=ROOT).strip())
    if cut_frames != n:
        print("  ! asked for %d frames, cut %d — check the beat bounds" % (n, cut_frames))
        n = cut_frames

    # --quality best: the matte is laid straight over the same pixels of the
    # plate, so any colour drift in the re-encode shows up as *her* being a
    # slightly different person from the frame around her.
    # Pinned to the version ./hf uses. Unpinned, npx pulled 0.8.82 on
    # 2026-09-28, which moved onnxruntime-node to an optional install that
    # fails on this machine; 0.8.33 bundles it and is already cached.
    run([NPX, "--yes", "hyperframes@0.8.33", "remove-background", span,
         "-o", webm, "--quality", "best"])
    os.remove(span)

    rel = "assets/mattes/%s.webm" % name
    print("\n  %s" % rel)
    print("\nIn the beat, after its graphics:\n")
    print('    k.matte("%s", %.3f, %.3f)' % (name, f0 / fps, n / fps))
    print("\n(start %.3f, duration %.3f — the plate runs at composition time,"
          % (f0 / fps, n / fps))
    print(" so these are just the frame indices back in seconds.)")


if __name__ == "__main__":
    main()
