# -*- coding: utf-8 -*-
"""Mux a reel: video.mp4 + her voice + light SFX, CTA tail in silence.

    python3 leadmagnet/reels/rmix.py [k ...]  -> reels/out/REEL-LM-0k.mp4
"""
import json, os, subprocess, sys, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from assemble import synth  # noqa: E402
SR = 48000
NAMES = {1: "openrouter", 2: "skopiyuvaty-montazh", 3: "ai-slop", 4: "moi-rilsy-montuye-ai", 5: "bezpechni-zony",
         6: "mudbord", 7: "shcho-take-md", 8: "chat-vs-code"}


def mix(k):
    d = os.path.join(HERE, "r%02d" % k)
    meta = json.load(open(os.path.join(d, "reel.json")))
    w = wave.open(os.path.join(d, "voice.wav"))
    ch = w.getnchannels()
    v = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, ch).astype(np.float32) / 32768
    n = int(round(meta["duration"] * SR))
    out = np.zeros((n, ch), np.float32)
    out[:min(n, len(v))] = v[:n]
    K = synth()
    for t, name in meta["sfx"]:
        s = K[name] * {"pop": 0.6, "whoosh": 0.35, "click": 0.9}.get(name, 0.5)
        i = int(max(0, t) * SR)
        e = min(n, i + len(s))
        out[i:e] += s[:e - i, None] * 0.6
    out = np.clip(out, -1, 1)
    o = wave.open(os.path.join(d, "mix.wav"), "w")
    o.setnchannels(ch); o.setsampwidth(2); o.setframerate(SR)
    o.writeframes((out * 32767).astype(np.int16).tobytes()); o.close()
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    dst = os.path.join(HERE, "out", "REEL-LM-%02d-%s.mp4" % (k, NAMES[k]))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(d, "video.mp4"), "-i", os.path.join(d, "mix.wav"),
                    "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "slow", "-crf", "21", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", "-shortest", dst], check=True)
    print(dst, os.path.getsize(dst) // 1048576, "MB")


if __name__ == "__main__":
    for k in [int(a) for a in sys.argv[1:]] or sorted(NAMES):
        mix(k)
