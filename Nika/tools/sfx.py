# -*- coding: utf-8 -*-
"""Nika's sound design: a small synthesised kit, mixed under her voice.

    python Nika/tools/sfx.py synth               # writes Nika/assets/sfx/*.wav
    python Nika/tools/sfx.py mix Nika/r01-test   # assets/voice.mp4 + sfx.json -> assets/base.mp4

Same brief as Ruta's reels: click on text, whoosh on a cut, pop when a card
lands, ka-ching on money. Nothing too crazy, always under her voice, and the
voice is never ducked. The kit is synthesised (not sampled) because Ruta's kit
lives on her laptop only, and Nika's folder has to stand alone.

`sfx.json` is written by the reel's build.py: [{"t": 3.42, "name": "pop"}, ...],
with an optional "db" to nudge one cue.
"""
import json
import os
import subprocess
import sys
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.join(os.path.dirname(HERE), "assets", "sfx")
SR = 48000

# peak of each effect, in dB below the peak of her voice
LEVEL = {"click": 16, "tap": 15, "pop": 13, "whoosh": 15, "swish": 17,
         "kaching": 10, "sparkle": 19, "ping": 15}


def t_(dur):
    return np.arange(int(SR * dur)) / SR


def env(n, attack, decay_tau):
    t = np.arange(n) / SR
    a = np.clip(t / max(attack, 1e-4), 0, 1)
    return a * np.exp(-np.maximum(t - attack, 0) / decay_tau)


def bandnoise(n, lo, hi, rng):
    """White noise band-limited in the frequency domain."""
    spec = np.fft.rfft(rng.standard_normal(n))
    f = np.fft.rfftfreq(n, 1 / SR)
    spec[(f < lo) | (f > hi)] = 0
    x = np.fft.irfft(spec, n)
    return x / (np.abs(x).max() + 1e-9)


def sweep_noise(dur, f0, f1, f2, q, rng):
    """Noise through a band-pass whose centre glides f0 -> f1 -> f2 (a whoosh)."""
    n = int(SR * dur)
    x = rng.standard_normal(n)
    t = np.linspace(0, 1, n)
    centre = np.where(t < 0.55, f0 + (f1 - f0) * (t / 0.55) ** 1.4,
                      f1 + (f2 - f1) * ((t - 0.55) / 0.45))
    # resonant 2-pole band-pass, coefficients updated per sample
    y = np.zeros(n)
    y1 = y2 = 0.0
    for i in range(n):
        w = 2 * np.pi * centre[i] / SR
        r = 1 - w / (2 * q) if w / (2 * q) < 0.5 else 0.5
        a1, a2 = -2 * r * np.cos(w), r * r
        yi = (1 - r) * x[i] - a1 * y1 - a2 * y2
        y[i] = yi
        y2, y1 = y1, yi
    return y / (np.abs(y).max() + 1e-9)


def stereo(x, pan_from=0.0, pan_to=0.0):
    p = np.linspace(pan_from, pan_to, len(x))
    l, r = np.cos((p + 1) * np.pi / 4), np.sin((p + 1) * np.pi / 4)
    return np.stack([x * l, x * r], axis=1)


def synth_kit():
    rng = np.random.default_rng(7)
    kit = {}

    # click: a soft UI tick, 30 ms
    n = int(SR * 0.03)
    x = bandnoise(n, 1800, 7000, rng) * env(n, 0.0005, 0.004)
    x += 0.5 * np.sin(2 * np.pi * 2900 * t_(0.03)) * env(n, 0.0005, 0.006)
    kit["click"] = stereo(x)

    # tap: a mouse click on a button, 45 ms, two quick transients
    n = int(SR * 0.045)
    x = bandnoise(n, 1200, 5000, rng) * env(n, 0.0004, 0.003)
    k = int(SR * 0.018)
    x[k:] += 0.6 * bandnoise(n - k, 900, 4000, rng) * env(n - k, 0.0004, 0.004)
    kit["tap"] = stereo(x)

    # pop: a soft bubble, 130 ms, pitch falling 950 -> 260 Hz
    tt = t_(0.13)
    f = 260 + 690 * np.exp(-tt / 0.018)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(tt), 0.002, 0.045)
    x += 0.15 * bandnoise(len(tt), 2000, 8000, rng) * env(len(tt), 0.0005, 0.004)
    kit["pop"] = stereo(x)

    # whoosh: 0.5 s, centre 350 -> 2600 -> 900 Hz, panning L -> R
    x = sweep_noise(0.5, 350, 2600, 900, 2.2, rng)
    e = np.sin(np.pi * np.linspace(0, 1, len(x)) ** 0.8) ** 2
    kit["whoosh"] = stereo(x * e, -0.5, 0.5)

    # swish: a lighter, quicker whoosh for a card sliding past, 0.28 s
    x = sweep_noise(0.28, 900, 4200, 1800, 2.8, rng)
    e = np.sin(np.pi * np.linspace(0, 1, len(x)) ** 0.7) ** 2
    kit["swish"] = stereo(x * e, 0.4, -0.3)

    # kaching: lever clack + drawer rattle + a bright bell, 0.9 s
    tt = t_(0.9)
    n = len(tt)
    x = np.zeros(n)
    k = int(SR * 0.03)
    x[:k] += 0.8 * bandnoise(k, 800, 6000, rng) * env(k, 0.0005, 0.006)
    d0, d1 = int(SR * 0.035), int(SR * 0.12)
    x[d0:d1] += 0.35 * bandnoise(d1 - d0, 2500, 9000, rng) * env(d1 - d0, 0.002, 0.03)
    b0 = int(SR * 0.09)
    tb = tt[: n - b0]
    bell = sum(a * np.sin(2 * np.pi * fr * tb) * np.exp(-tb / tau)
               for fr, a, tau in [(2093, 1.0, 0.32), (2637, 0.7, 0.26), (3136, 0.55, 0.22),
                                  (4186, 0.35, 0.16), (5274, 0.2, 0.1)])
    x[b0:] += 0.55 * bell / 2.8
    kit["kaching"] = stereo(x)

    # sparkle: five tiny high pings scattered over 0.45 s
    tt = t_(0.6)
    x = np.zeros(len(tt))
    for i, fr in enumerate([3520, 4699, 3951, 5274, 4435]):
        s = int(SR * (0.02 + i * 0.085))
        tb = tt[: len(tt) - s]
        x[s:] += (0.8 - 0.1 * i) * np.sin(2 * np.pi * fr * tb) * np.exp(-tb / 0.07)
    kit["sparkle"] = stereo(x / 2.2, -0.3, 0.3)

    # ping: a notification, two notes
    tt = t_(0.5)
    x = np.sin(2 * np.pi * 1568 * tt) * np.exp(-tt / 0.12)
    s = int(SR * 0.09)
    x[s:] += 0.8 * np.sin(2 * np.pi * 2093 * tt[: len(tt) - s]) * np.exp(-tt[: len(tt) - s] / 0.16)
    kit["ping"] = stereo(x / 1.8)

    os.makedirs(KIT, exist_ok=True)
    for name, a in kit.items():
        a = a / (np.abs(a).max() + 1e-9) * 0.9
        write_wav(os.path.join(KIT, name + ".wav"), a)
    print("kit:", ", ".join(sorted(kit)))


def write_wav(path, a):
    a = np.clip(a, -1, 1)
    with wave.open(path, "w") as f:
        f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR)
        f.writeframes((a * 32767).astype(np.int16).tobytes())


def read_wav(path):
    with wave.open(path) as f:
        a = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).reshape(-1, 2)
    return a.astype(np.float32) / 32768.0


def decode(path):
    pcm = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", path, "-vn", "-ac", "2",
                          "-ar", str(SR), "-f", "s16le", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(pcm, np.int16).reshape(-1, 2).astype(np.float32) / 32768.0


def mix(reel):
    voice_mp4 = os.path.join(reel, "assets", "voice.mp4")
    cues = json.load(open(os.path.join(reel, "sfx.json"), encoding="utf-8"))
    v = decode(voice_mp4)
    # pad the audio to the video's full length, so the plate never loses its tail
    vdur = float(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                                 "stream=duration", "-of", "csv=p=0", voice_mp4],
                                capture_output=True, text=True, check=True).stdout.strip())
    need = int(np.ceil(vdur * SR))
    if len(v) < need:
        v = np.concatenate([v, np.zeros((need - len(v), 2), np.float32)])
    peak = np.abs(v).max()
    out = v.copy()
    for c in cues:
        fx = read_wav(os.path.join(KIT, c["name"] + ".wav"))
        gain = peak * 10 ** (-(LEVEL[c["name"]] - c.get("db", 0)) / 20) / (np.abs(fx).max() + 1e-9)
        s = int(round(c["t"] * SR))
        if s >= len(out):
            continue
        e = min(len(out), s + len(fx))
        out[s:e] += fx[: e - s] * gain
    m = np.abs(out).max()
    if m > 0.98:          # only ever trims a stray overlap; her level stays where it was
        out *= 0.98 / m
    wav = os.path.join(reel, "assets", "mix.wav")
    write_wav(wav, out)
    base = os.path.join(reel, "assets", "base.mp4")
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", voice_mp4, "-i", wav,
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    base], check=True)
    os.remove(wav)
    print("mixed", len(cues), "cues ->", base)


if __name__ == "__main__":
    if sys.argv[1] == "synth":
        synth_kit()
    elif sys.argv[1] == "mix":
        mix(sys.argv[2])
