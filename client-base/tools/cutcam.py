# -*- coding: utf-8 -*-
"""Cut silences and give each clip its own framing.

The framing is not decoration. Removing a silence leaves a jump cut; changing
the crop across that cut is what makes it read as an edit instead of a glitch.
So the rule is simply: never use the same framing twice in a row.

Source is 2160x3840, output 1080x1920 — 2x linear headroom, so every punch-in
is a real crop of real pixels.
"""
import json
import re
import subprocess
import sys

SRC_W, SRC_H = 2160, 3840
OUT_W, OUT_H = 1080, 1920

PAD = 0.11
MERGE = 0.22
BLOCK_GAP = 1.8

# name -> (zoom, x-bias, y-bias)  bias is a fraction of the leftover margin
# Ruta's grain: 5-10% steps, not camera changes. Big jumps read as a different
# shot; small ones read as emphasis, which is the point.
FRAMES = {
    "base":   (1.00, 0.50, 0.50),
    "in1":    (1.06, 0.50, 0.46),
    "in2":    (1.11, 0.50, 0.43),
    "in1_l":  (1.06, 0.44, 0.46),
    "in1_r":  (1.06, 0.56, 0.46),
    "in2_l":  (1.11, 0.45, 0.43),
    # reserved for a real emphasis beat, still under 20%
    "punch":  (1.18, 0.50, 0.40),
}
CYCLE = ["base", "in1", "in2_l", "in1_r", "in2", "in1_l", "base", "in1_r"]


def detect(wav, noise="-28dB", d=0.30):
    out = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", wav, "-af",
         f"silencedetect=noise={noise}:d={d}", "-f", "null", "-"],
        capture_output=True, text=True).stderr
    s = [float(x) for x in re.findall(r"silence_start:\s*([0-9.]+)", out)]
    e = [float(x) for x in re.findall(r"silence_end:\s*([0-9.]+)", out)]
    return list(zip(s, e))


def duration(p):
    return float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", p], capture_output=True, text=True).stdout.strip())


def build_clips(wav, drops=()):
    dur = duration(wav)
    sil = detect(wav)
    speech, cur = [], 0.0
    for a, b in sil:
        if a > cur:
            speech.append([cur, a])
        cur = max(cur, b)
    if cur < dur:
        speech.append([cur, dur])

    padded = [[max(0, a - PAD), min(dur, b + PAD)] for a, b in speech]
    merged = []
    for seg in padded:
        if merged and seg[0] - merged[-1][1] < MERGE:
            merged[-1][1] = seg[1]
        else:
            merged.append(seg)
    merged = [m for m in merged if m[1] - m[0] > 0.35]
    merged = [m for m in merged
              if not any(not (m[1] <= a or m[0] >= b) for a, b in drops)]

    clips, t, ci = [], 0.0, 0
    for i, (a, b) in enumerate(merged):
        gap = a - merged[i - 1][1] if i else 0.0
        # never repeat a framing across a cut. A long pause is a new idea, so
        # jump further round the cycle — a bigger visual change marks the beat.
        ci += 3 if gap >= BLOCK_GAP else 1
        name = CYCLE[ci % len(CYCLE)]
        d = b - a
        clips.append({
            "i": i, "src_in": round(a, 3), "src_out": round(b, 3),
            "dur": round(d, 3), "tl": round(t, 3),
            "frame": name, "gap": round(gap, 3),
            # long holds get a slow push so they do not sit static
            "push": round(0.045, 3) if d > 5.0 else 0.0,
        })
        t += b - a
    return clips, round(t, 3)


def crop_filter(name):
    z, bx, by = FRAMES[name]
    cw, ch = int(SRC_W / z), int(SRC_H / z)
    cw -= cw % 2
    ch -= ch % 2
    x = int((SRC_W - cw) * bx)
    y = int((SRC_H - ch) * by)
    return f"crop={cw}:{ch}:{x}:{y},scale={OUT_W}:{OUT_H}:flags=lanczos"


if __name__ == "__main__":
    wav, src, out_json = sys.argv[1], sys.argv[2], sys.argv[3]
    clips, total = build_clips(wav)
    json.dump({"duration": total, "clips": clips},
              open(out_json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{len(clips)} clips, {total}s (from {duration(wav):.1f}s)")
    for c in clips[:14]:
        print(f"  {c['i']:2d}  {c['src_in']:7.2f}-{c['src_out']:7.2f}  "
              f"{c['dur']:5.2f}s  {c['frame']:6s}  gap {c['gap']:4.2f}")
