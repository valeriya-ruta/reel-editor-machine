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

Colour is the other thing (her catch, 2026-10-21: "my colors change to slightly
more orange" on every behind-me word and half screen of reels 41–52). The
remove-background output was ~9 levels short of blue against the plate, for
three stacked reasons: it encodes RGB->YUV with the BT.601 matrix but tags the
file BT.709; HyperFrames extracts alpha video as PNGs that carry that BT.709
curve as a cICP chunk, which Chrome then colour-manages; and the plate takes a
different road (JPEG frames) whose own 601/709 mix-up cancels against the
render's final encode, where the cut-out's does not. So we keep only the
*shape* from remove-background and repaint it with the plate's own YUV,
untouched, tagged the way the plate's road ends up decoded (BT.601 matrix, no
transfer or primaries, so no PNG colour chunk). Measured on reel 48 at 1:12,
same frame rendered with and without the matte: old -4/-6/-9 RGB levels,
repainted -1/-1/-1 (compression noise). `--repaint` redoes an existing matte
without running background removal again:

    python3 tools/matte.py reel-48 69.733 72.0 hours --repaint
"""
import io
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NPX = os.path.join(os.environ.get("APPDATA", ""), "npm", "npx.cmd")
if not os.path.exists(NPX):        # the cloud container (Linux): npx on PATH
    NPX = "npx"


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


def count_frames(path):
    return int(subprocess.check_output([
        "ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames",
        "-show_entries", "stream=nb_read_frames", "-of",
        "default=nw=1:nk=1", path], cwd=ROOT).strip())


def rembg_shape(span, shape, w, h):
    """The cloud container's path (MATTE_REMBG=1): hyperframes' remove-background
    needs onnxruntime-node, whose installer cannot download there. Same model
    family (u2net_human_seg) through python rembg; only the alpha is used, the
    colour is repainted from the plate by repaint() anyway."""
    import numpy as np
    from rembg import new_session, remove
    from PIL import Image
    sess = new_session("u2net_human_seg")
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-i", span, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                           stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", "%dx%d" % (w, h),
                            "-r", "30", "-i", "-", "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-crf", "20",
                            "-b:v", "0", "-auto-alt-ref", "0", "-row-mt", "1", "-y", shape], stdin=subprocess.PIPE)
    fb = w * h * 3
    while True:
        buf = dec.stdout.read(fb)
        if len(buf) < fb:
            break
        img = Image.frombytes("RGB", (w, h), buf)
        # matte at half size (4x faster), alpha scaled back up — the edge is
        # repainted from the plate, so only the shape's accuracy matters
        small = img.resize((w // 2, h // 2))
        m = remove(small, session=sess, only_mask=True).resize((w, h), Image.BILINEAR)
        rgba = np.dstack([np.asarray(img), np.asarray(m)])
        enc.stdin.write(rgba.astype(np.uint8).tobytes())
    enc.stdin.close(); enc.wait(); dec.wait()


def repaint(base, f0, f1, shape, webm):
    """Her own plate pixels, the matte's alpha: the cut-out is the same picture
    as the frame around it. YUV goes straight through (alphamerge, no RGB
    round trip); see the docstring for why the tags say BT.601 and nothing else."""
    run(["ffmpeg", "-v", "error", "-i", base, "-c:v", "libvpx-vp9", "-i", shape,
         "-filter_complex",
         "[0:v]trim=start_frame=%d:end_frame=%d,setpts=PTS-STARTPTS[p];"
         "[1:v]alphaextract[a];[p][a]alphamerge,format=yuva420p" % (f0, f1),
         "-an", "-c:v", "libvpx-vp9", "-pix_fmt", "yuva420p", "-crf", "16", "-b:v", "0",
         "-auto-alt-ref", "0", "-row-mt", "1",
         "-colorspace", "smpte170m", "-color_primaries", "unknown", "-color_trc", "unknown",
         "-color_range", "tv", "-y", webm])


def main():
    if len(sys.argv) < 5:
        sys.exit(__doc__)
    reel, start, end, name = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
    only_repaint = "--repaint" in sys.argv[5:]

    base = os.path.join(reel, "assets", "base.mp4")
    if not os.path.exists(os.path.join(ROOT, base)):     # before the sfx mix: same frames
        base = os.path.join(reel, "assets", "voice.mp4")
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
    shape = os.path.join(out_dir, "_%s_shape.webm" % name)
    webm = os.path.join(out_dir, "%s.webm" % name)

    if only_repaint:
        # The start is a composition time already on the frame grid (k.matte
        # snaps it), so round it — int() would land 69.733 s on frame 2091.
        # The length is whatever the existing matte has.
        f0 = int(round(start * fps))
        n = count_frames(webm)
        os.replace(webm, shape)
        repaint(base, f0, f0 + n, shape, webm)
        os.remove(shape)
        print("%s  repainted from the plate, frames %d-%d" % (name, f0, f0 + n))
        return

    print("%s  frames %d-%d (%d @ %.3f fps, %dx%d)" % (name, f0, f1, n, fps, w, h))
    print("  about %.1f min on the CPU" % mins)

    # Frame-exact, decoded from the top. The plate is short enough that not
    # seeking costs less than a misaligned matte does.
    run(["ffmpeg", "-v", "error", "-i", base,
         "-vf", "trim=start_frame=%d:end_frame=%d,setpts=PTS-STARTPTS" % (f0, f1),
         "-an", "-c:v", "libx264", "-crf", "16", "-preset", "veryfast",
         "-y", span])

    cut_frames = count_frames(span)
    if cut_frames != n:
        print("  ! asked for %d frames, cut %d — check the beat bounds" % (n, cut_frames))
        n = cut_frames

    # --quality best: the matte is laid straight over the same pixels of the
    # plate, so any colour drift in the re-encode shows up as *her* being a
    # slightly different person from the frame around her.
    # Pinned to the version ./hf uses. Unpinned, npx pulled 0.8.82 on
    # 2026-09-28, which moved onnxruntime-node to an optional install that
    # fails on this machine; 0.8.33 bundles it and is already cached.
    if os.environ.get("MATTE_REMBG"):
        rembg_shape(span, shape, w, h)
    else:
        run([NPX, "--yes", "hyperframes@0.8.33", "remove-background", span,
             "-o", shape, "--quality", "best"])
    os.remove(span)
    repaint(base, f0, f0 + n, shape, webm)
    os.remove(shape)

    rel = "assets/mattes/%s.webm" % name
    print("\n  %s" % rel)
    print("\nIn the beat, after its graphics:\n")
    print('    k.matte("%s", %.3f, %.3f)' % (name, f0 / fps, n / fps))
    print("\n(start %.3f, duration %.3f — the plate runs at composition time,"
          % (f0 / fps, n / fps))
    print(" so these are just the frame indices back in seconds.)")


if __name__ == "__main__":
    main()
