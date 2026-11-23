# -*- coding: utf-8 -*-
"""Cut her take into a reel's plate: graded, pauses tightened, voice at -14 LUFS.

    python Nika/tools/plate.py <source.MOV> <reel dir> <a-b,a-b,...> [speed] [tail]   # kept source spans, seconds
                                                                              # -> <reel dir>/assets/voice.mp4

- **Speed**: optional, e.g. 1.2. Her take is sped up after the join, picture by
  re-timing and voice by `atempo` (pitch kept). `look.Reel(spans, speed)` maps
  times the same way, and the plate is cut to exactly the frame count it expects.
- **Tail**: optional seconds of held last frame + silence after her last word, for
  an end card that covers the frame and carries only sound effects.

- **Spans**: the source is cut to these spans and joined. Each span is rounded to
  whole frames, so picture and sound stay locked. `look.Reel(spans)` maps source
  time to reel time the same way. Joins get a 10 ms audio fade, so they don't
  click.
- **Grade** (GRADE): her camera filter makes everything orange and soft. This takes
  the orange out (the wall goes from orange to a warm beige, skin stays warm),
  adds a touch of contrast and a light luma sharpen. Approved on a still,
  2026-11-17.
- **Loudness**: her takes come in very quiet (IMG_7332: -33 LUFS, peaks at -16
  dBTP), so she is normalised to -14 LUFS in two passes. Then
  `sfx.py mix <reel dir>` lays the effects on top and writes assets/base.mp4.
"""
import json
import os
import re
import subprocess
import sys

FPS = 30
TARGET = "I=-14:TP=-1.5:LRA=11"
GRADE = ("colorchannelmixer=rr=0.94:gg=1.02:bb=1.15,colorbalance=rs=-0.02:gs=0.05:bs=-0.02,"
         "eq=contrast=1.06:saturation=1.04,unsharp=5:5:0.55:5:5:0")


def frame_spans(spans):
    """Snap each span's start to a frame and its length to whole frames."""
    out = []
    for a, b in spans:
        fa = round(a * FPS)
        n = round((b - a) * FPS)
        out.append((fa / FPS, (fa + n) / FPS))
    return out


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, check=True)


def main(src, reel, spec, speed="1", tail="0"):
    speed, tail = float(speed), float(tail)
    spans = frame_spans([tuple(float(x) for x in s.split("-")) for s in spec.split(",")])
    frames = round(sum(round((b - a) * FPS) for a, b in spans) / speed) + round(tail * FPS)
    assets = os.path.join(reel, "assets")
    os.makedirs(assets, exist_ok=True)
    raw, out = os.path.join(assets, "voice_raw.mkv"), os.path.join(assets, "voice.mp4")

    # 1. cut + join + grade: picture to H.264, sound kept as PCM until it is normalised
    parts, labels = [], []
    for i, (a, b) in enumerate(spans):
        d = b - a
        parts.append(f"[0:v]trim=start={a:.4f}:end={b:.4f},setpts=PTS-STARTPTS[v{i}];"
                     f"[0:a]atrim=start={a:.4f}:end={b:.4f},asetpts=PTS-STARTPTS,"
                     f"afade=t=in:d=0.01,afade=t=out:st={d - 0.01:.4f}:d=0.01[a{i}];")
        labels.append(f"[v{i}][a{i}]")
    graph = ("".join(parts) + "".join(labels) + f"concat=n={len(spans)}:v=1:a=1[vc][ac];"
             f"[vc]setpts=PTS/{speed},scale=1080:1920:flags=lanczos,fps={FPS},{GRADE},"
             f"tpad=stop_mode=clone:stop_duration={tail + 0.5},format=yuv420p[v];"
             f"[ac]atempo={speed},apad=pad_dur={tail + 0.5}[a]")
    run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", src, "-filter_complex", graph,
         "-map", "[v]", "-map", "[a]", "-frames:v", str(frames), "-t", f"{frames / FPS:.4f}",
         "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-c:a", "pcm_s16le", "-ar", "48000", raw])

    # 2. loudness, measured on the joined take, then applied linearly where possible
    probe = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-i", raw, "-vn", "-af",
                            f"loudnorm={TARGET}:print_format=json", "-f", "null", "-"],
                           capture_output=True, text=True, check=True).stderr
    m = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", probe, re.S).group(0))
    norm = (f"loudnorm={TARGET}:measured_I={m['input_i']}:measured_TP={m['input_tp']}"
            f":measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}"
            f":offset={m['target_offset']}:linear=true,aresample=48000")
    run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", raw, "-map", "0:v", "-map", "0:a",
         "-c:v", "copy", "-af", norm, "-c:a", "aac", "-b:a", "192k", out])
    os.remove(raw)
    print(f"{out}: {len(spans)} spans at {speed}x, {frames} frames ({frames / FPS:.3f} s); "
          f"voice {m['input_i']} LUFS -> -14")


if __name__ == "__main__":
    main(*sys.argv[1:6])
