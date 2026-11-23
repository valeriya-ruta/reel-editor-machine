# -*- coding: utf-8 -*-
"""Cut her take into a reel's plate: 1080x1920 H.264 30 fps, voice at -14 LUFS.

    python Nika/tools/plate.py <source.MOV> <start> <end> <reel dir>     # -> <reel dir>/assets/voice.mp4

Her front-camera takes come in very quiet (IMG_7332: -33.3 LUFS, peaks at
-16 dBTP). Loudness is measured on the slice and normalised in two passes, so
speech keeps its dynamics wherever the target allows. Then
`sfx.py mix <reel dir>` lays the effects on top and writes assets/base.mp4.
"""
import json
import os
import re
import subprocess
import sys

TARGET = "I=-14:TP=-1.5:LRA=11"


def main(src, start, end, reel):
    out = os.path.join(reel, "assets", "voice.mp4")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    cut = ["-ss", start, "-to", end, "-i", src]
    probe = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", *cut, "-vn", "-af",
                            f"loudnorm={TARGET}:print_format=json", "-f", "null", "-"],
                           capture_output=True, text=True, check=True).stderr
    m = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", probe, re.S).group(0))
    norm = (f"loudnorm={TARGET}:measured_I={m['input_i']}:measured_TP={m['input_tp']}"
            f":measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}"
            f":offset={m['target_offset']}:linear=true")
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", *cut,
                    "-vf", "scale=1080:1920:flags=lanczos,fps=30", "-c:v", "libx264", "-preset", "slow",
                    "-crf", "17", "-pix_fmt", "yuv420p",
                    "-af", norm + ",aresample=48000", "-c:a", "aac", "-b:a", "192k", out], check=True)
    print(f"{out}: input {m['input_i']} LUFS / {m['input_tp']} dBTP -> -14 LUFS")


if __name__ == "__main__":
    main(*sys.argv[1:5])
