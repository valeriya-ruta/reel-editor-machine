# -*- coding: utf-8 -*-
"""Sound design: mix short effects under her voice.

    python tools/sfx.py synth          # one-time: assets/sfx/kaching.wav
    python tools/sfx.py mix 21         # reel-21/assets/voice.mp4 + reel-21/sfx.json
                                       #   -> reel-21/assets/base.mp4

`sfx.json` is written by the reel's build.py: [{"t": 3.42, "name": "pop"}, ...],
optional "db" to nudge one cue. Her brief, 2026-10-05: *"some clicking on text,
whooshing, kachinging etc? nothing too crazy, just to give some style"*. So
every effect is normalised against her own voice and sits well under it; the
voice is never ducked.

The kit (assets/sfx/): click-soft (text / caption pops), pop (a tile or card
lands), whoosh-short (a transition, an iris, a takeover), kaching (money),
notification / ping (a notification lands), typing / key-press (a prompt being
typed), sparkle (a reveal, sparingly).
"""
import json
import os
import subprocess
import sys
import wave

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KIT = os.path.join(ROOT, "assets", "sfx")
CACHE = "E:/reels-work/sfxcache"
SR = 48000

# peak of the effect, in dB below the peak of her voice
LEVEL = {
    "click-soft": 14, "click": 14, "key-press": 15, "typing": 17,
    "pop": 13, "whoosh-short": 15, "whoosh": 15, "whoosh-cinematic": 18,
    "kaching": 10, "notification": 13, "ping": 15, "chime": 17, "sparkle": 18,
    "impact-bass-1": 16, "riser": 20, "glitch-1": 20,
}


def write_wav(path, a):
    a = np.clip(a, -1, 1)
    if a.ndim == 1:
        a = np.stack([a, a], axis=1)
    with wave.open(path, "w") as f:
        f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR)
        f.writeframes((a * 32767).astype(np.int16).tobytes())


def read_any(path):
    os.makedirs(CACHE, exist_ok=True)
    w = os.path.join(CACHE, os.path.basename(path) + ".wav")
    if not os.path.exists(w) or os.path.getmtime(w) < os.path.getmtime(path):
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", path, "-ac", "2",
                        "-ar", str(SR), "-c:a", "pcm_s16le", w], check=True)
    with wave.open(w) as f:
        a = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).reshape(-1, 2)
    return a.astype(np.float32) / 32768.0


def bandnoise(n, lo, hi, rng):
    x = rng.standard_normal(n)
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(n, 1 / SR)
    X[(f < lo) | (f > hi)] = 0
    y = np.fft.irfft(X, n)
    return y / (np.abs(y).max() + 1e-9)


def synth_kaching():
    rng = np.random.default_rng(7)
    n = int(SR * 1.25)
    t = np.arange(n) / SR
    out = np.zeros(n)
    # "ka": the drawer — two short mechanical clicks and a low knock
    for t0, g in ((0.0, 0.9), (0.045, 0.55)):
        i0, m = int(t0 * SR), int(0.018 * SR)
        burst = bandnoise(m, 1800, 7000, rng) * np.exp(-np.arange(m) / (0.004 * SR))
        out[i0:i0 + m] += g * burst
    k = int(0.06 * SR)
    out[:k] += 0.5 * np.sin(2 * np.pi * 140 * t[:k]) * np.exp(-t[:k] / 0.012)
    # "ching": a small bright bell, inharmonic partials, slight shimmer
    t0 = 0.075
    tb = np.clip(t - t0, 0, None)
    on = (t >= t0).astype(float)
    f0 = 2489.0
    for r, amp, dec in ((1.0, 1.0, 0.55), (1.505, 0.45, 0.38), (2.0, 0.32, 0.30),
                        (2.76, 0.22, 0.20), (3.42, 0.12, 0.14), (5.1, 0.06, 0.08)):
        for det in (-1.6, 1.6):
            out += on * 0.5 * amp * np.sin(2 * np.pi * (f0 * r + det) * tb) * np.exp(-tb / dec)
    # a couple of coin glints
    for tc, fc in ((0.16, 6100.0), (0.23, 5400.0), (0.31, 6900.0)):
        tg = np.clip(t - tc, 0, None)
        out += (t >= tc) * 0.10 * np.sin(2 * np.pi * fc * tg) * np.exp(-tg / 0.05)
    attack = np.clip((t - t0) / 0.002, 0, 1) * on + (t < t0)
    out *= attack
    out *= np.minimum(1, (1.25 - t) / 0.15)       # tail fade
    out /= np.abs(out).max()
    write_wav(os.path.join(KIT, "kaching.wav"), out * 0.89)


def mix(nn):
    reel = os.path.join(ROOT, "reel-" + nn)
    voice = os.path.join(reel, "assets", "voice.mp4")
    cues = json.load(open(os.path.join(reel, "sfx.json"), encoding="utf-8"))
    tmp = os.path.join("E:/reels-work", "r" + nn)
    os.makedirs(tmp, exist_ok=True)
    vw = os.path.join(tmp, "voice-mix-in.wav")
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", voice, "-vn", "-ac", "2",
                    "-ar", str(SR), "-c:a", "pcm_s16le", vw], check=True)
    with wave.open(vw) as f:
        v = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).reshape(-1, 2)
    v = v.astype(np.float32) / 32768.0
    # her peak, robustly: 99.9th percentile of |x|
    vpk = float(np.percentile(np.abs(v), 99.9))
    out = v.copy()
    lib = {}
    for c in cues:
        name = c["name"]
        if name not in lib:
            p = os.path.join(KIT, name + (".wav" if name == "kaching" else ".mp3"))
            lib[name] = read_any(p)
        s = lib[name]
        spk = float(np.abs(s).max()) + 1e-9
        db = -LEVEL.get(name, 15) + c.get("db", 0)
        g = vpk / spk * 10 ** (db / 20)
        i0 = int(round(c["t"] * SR))
        if i0 >= len(out):
            continue
        seg = s[: len(out) - i0] * g
        out[i0:i0 + len(seg)] += seg
    pk = np.abs(out).max()
    if pk > 0.97:                       # never clip; a soft trim, not a limiter
        out *= 0.97 / pk
    mw = os.path.join(tmp, "mix.wav")
    with wave.open(mw, "w") as f:
        f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR)
        f.writeframes((out * 32767).astype(np.int16).tobytes())
    base = os.path.join(reel, "assets", "base.mp4")
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", voice, "-i", mw,
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart", base], check=True)
    print("mixed %d cues -> %s" % (len(cues), base))


if __name__ == "__main__":
    if sys.argv[1] == "synth":
        synth_kaching()
    elif sys.argv[1] == "mix":
        mix(sys.argv[2])
