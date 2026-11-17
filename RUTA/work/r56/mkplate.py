# -*- coding: utf-8 -*-
"""Reel 56 plate: four phone clips (portrait, HEVC, VFR ~30) cut to the story
and joined. Every piece is encoded on its own to whole frames at 30 fps, then
concatenated; audio gets a 12 ms fade in / 20 ms fade out so cuts don't click.

    python3 work/r56/mkplate.py      -> reel-56/assets/base.mp4 + work/r56/pieces.out.json

Pieces marked "vo" are the silent stretches her voiceover lines go over
(the three lines in PLAN.md); their own room sound stays, quieter.
"""
import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SRC = os.path.join(ROOT, "work", "incoming", "r56")
OUT = os.path.join(ROOT, "reel-56", "assets", "base.mp4")
SEG = os.path.join(HERE, "seg")
CUT = os.path.join(SEG, "cut.mp4")          # the cut before her voiceover goes on
FPS = 30

C1, C2, C3, C4 = ("20261117_%s.mp4" % n for n in ("132849", "132924", "134447", "135042"))
P = [
    # A · intro, to camera
    {"id": "A", "src": C1, "a": 1.60, "b": 12.65},
    # B · open Claude, New
    {"id": "B1", "src": C2, "a": 0.70, "b": 2.05},
    {"id": "B2", "src": C2, "a": 3.15, "b": 4.60},
    # C · the base prompt pasted and sent (no voice: VO 1 + 2)
    {"id": "C", "src": C2, "a": 10.60, "b": 18.38, "vo": True},
    # D · her dictating the voice note
    {"id": "D1", "src": C2, "a": 18.80, "b": 21.10},
    {"id": "D2", "src": C2, "a": 23.00, "b": 24.75},
    {"id": "D3", "src": C2, "a": 42.45, "b": 46.10},
    # E · the base is ready, the voice notes go in
    {"id": "E1", "src": C3, "a": 0.80, "b": 3.55},
    {"id": "E2", "src": C3, "a": 6.78, "b": 7.98},
    {"id": "E3", "src": C3, "a": 8.80, "b": 10.95},
    {"id": "E4", "src": C3, "a": 12.20, "b": 13.50},
    # F · five minutes later: the finished deck, edited in place (no voice: VO 3)
    {"id": "F1", "src": C4, "a": 6.20, "b": 10.40, "vo": True},
    {"id": "F2", "src": C4, "a": 12.60, "b": 16.90, "vo": True},
    # G · outro, to camera
    {"id": "G", "src": C1, "a": 13.45, "b": 16.00},
]


def load_vo():
    f = os.path.join(HERE, "vo.json")
    if not os.path.exists(f):
        return None
    vo = json.load(open(f))
    for p in P:
        if p["id"] == "C":
            p["a"] = round(p["a"] - vo["grow_c"], 3)     # her clip has the prompt on screen from 4.6 s
        if p["id"] == "F1":
            p["a"] = round(max(0.0, p["a"] - vo["grow_f"]), 3)
    return vo


def rms_db(path, spans):
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    import numpy as np
    x = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
    v = np.concatenate([x[int(a * 16000):int(b * 16000)] for a, b in spans])
    return 20 * np.log10(np.sqrt((v ** 2).mean()) + 1e-9)


def mix_vo(vo, cut):
    """her lines over the plate at their slots, levelled to her on-camera voice"""
    ref = rms_db(cut, [(2.0, 9.0)])                       # A: her intro, to camera
    gain = ref - rms_db(vo["src"], [(t["a"], t["b"]) for t in vo["takes"]])
    ins, flt = ["-i", cut], []
    for k, t in enumerate(vo["takes"]):
        ins += ["-ss", "%.3f" % t["a"], "-t", "%.3f" % (t["b"] - t["a"]), "-i", vo["src"]]
        ms = int(round(t["at"] * 1000))
        flt.append("[%d:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=%.2fdB,"
                   "afade=t=in:d=0.02,adelay=%d|%d[v%d]" % (k + 1, gain, ms, ms, k))
    flt.append("[0:a]" + "".join("[v%d]" % k for k in range(len(vo["takes"]))) +
               "amix=inputs=%d:normalize=0:duration=first[a]" % (len(vo["takes"]) + 1))
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y"] + ins +
                   ["-filter_complex", ";".join(flt), "-map", "0:v", "-map", "[a]", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", OUT], check=True)
    print("voiceover mixed, gain %+.1f dB" % gain)


def main():
    vo = load_vo()
    os.makedirs(SEG, exist_ok=True)
    lst, t, out = [], 0, []
    for i, p in enumerate(P):
        n = int(round((p["b"] - p["a"]) * FPS))
        d = n / float(FPS)
        vol = ",volume=0.5" if p.get("vo") else ""
        f = os.path.join(SEG, "p%02d.mov" % i)
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", "%.3f" % p["a"],
                        "-i", os.path.join(SRC, p["src"]), "-t", "%.4f" % d,
                        "-vf", "scale=1080:1920:flags=lanczos,fps=%d,setsar=1" % FPS, "-frames:v", str(n),
                        "-af", "apad,atrim=0:%.4f,afade=t=in:d=0.012,afade=t=out:st=%.4f:d=0.02%s"
                        % (d, d - 0.02, vol),
                        "-c:v", "libx264", "-crf", "17", "-preset", "fast", "-pix_fmt", "yuv420p",
                        "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", f], check=True)
        lst.append("file '%s'" % f)
        out.append(dict(p, f0=t, frames=n, t0=round(t / float(FPS), 4), t1=round((t + n) / float(FPS), 4)))
        t += n
    open(os.path.join(SEG, "list.txt"), "w").write("\n".join(lst) + "\n")
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0",
                    "-i", os.path.join(SEG, "list.txt"), "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart", CUT if vo else OUT], check=True)
    if vo:
        mix_vo(vo, CUT)
    json.dump(out, open(os.path.join(HERE, "pieces.out.json"), "w"), indent=1)
    print("PLATE %d frames, %.3f s" % (t, t / float(FPS)))


main()
