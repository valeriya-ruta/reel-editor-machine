# -*- coding: utf-8 -*-
"""A stand-in sound kit, synthesised, for when her own (assets/sfx, kept on her
laptop and gitignored) is not on this machine. Same names as hers, so
tools/sfx.py mixes it unchanged; her real files simply replace these.

    python tools/sfxsynth.py            -> assets/sfx/*.mp3 (+ kaching.wav via sfx.py)

Small, clean, nothing cartoonish: her brief was "some clicking on text,
whooshing, kachinging etc? nothing too crazy, just to give some style".
"""
import os
import subprocess
import sys
import wave

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KIT = os.path.join(ROOT, "assets", "sfx")
SR = 48000
rng = np.random.default_rng(7)


def t(sec):
    return np.arange(int(SR * sec)) / SR


def env(n, a, d):
    """attack a s, exponential decay with time-constant d s"""
    x = np.arange(n) / SR
    e = np.minimum(1.0, x / max(a, 1e-4)) * np.exp(-np.maximum(0, x - a) / d)
    return e


def bp(x, lo, hi):
    """band-pass by FFT mask (fine for one-shot effects)"""
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X[(f < lo) | (f > hi)] = 0
    return np.fft.irfft(X, len(x))


def click(freq=2600, dur=0.035, bright=1.0):
    n = int(SR * dur)
    tick = np.sin(2 * np.pi * freq * t(dur)) * env(n, 0.0008, 0.006)
    noise = bp(rng.standard_normal(n), 1500, 9000 * bright) * env(n, 0.0005, 0.004) * 0.6
    return tick + noise


def pop():
    d = 0.09
    x = t(d)
    f = 820 * np.exp(-x / 0.035) + 260
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * env(len(x), 0.002, 0.03)


def whoosh(d=0.42):
    n = int(SR * d)
    x = rng.standard_normal(n)
    out = np.zeros(n)
    # a band that sweeps up and back, under a rise-and-fall envelope
    seg = 8
    for i in range(seg):
        a, b = i * n // seg, (i + 1) * n // seg
        c = 500 + 2600 * np.sin(np.pi * (i + 0.5) / seg)
        out[a:b] = bp(x, c * 0.5, c * 1.6)[a:b]
    shape = np.sin(np.pi * np.linspace(0, 1, n)) ** 1.6
    return out * shape


def bell(freqs, d=0.5, decay=0.18):
    x = t(d)
    s = np.zeros_like(x)
    for f, g in freqs:
        s += g * np.sin(2 * np.pi * f * x) * np.exp(-x / decay)
    return s * env(len(x), 0.002, 10)


def notification():
    a = bell([(1318.5, 1), (2637, 0.25), (3955, 0.08)], 0.32, 0.12)
    b = bell([(1760, 1), (3520, 0.25), (5280, 0.08)], 0.5, 0.18)
    out = np.zeros(int(SR * 0.62))
    out[:len(a)] += a
    out[int(SR * 0.11):int(SR * 0.11) + len(b)] += b
    return out


def typing(d=1.1, rate=11):
    out = np.zeros(int(SR * d))
    k = 0.0
    while k < d - 0.05:
        c = click(freq=rng.uniform(1700, 2600), dur=0.03, bright=0.8) * rng.uniform(0.55, 1.0)
        i = int(k * SR)
        out[i:i + len(c)] += c[:len(out) - i]
        k += rng.uniform(0.6, 1.4) / rate
    return out


def sparkle(d=0.6):
    out = np.zeros(int(SR * d))
    for _ in range(9):
        f = rng.uniform(2800, 6000)
        b = bell([(f, 1), (f * 2.01, 0.2)], 0.25, 0.05) * rng.uniform(0.4, 1.0)
        i = int(rng.uniform(0, d - 0.25) * SR)
        out[i:i + len(b)] += b
    return out * np.linspace(1, 0.6, len(out))


KITSET = {
    "click-soft": lambda: click(2400, 0.035, 0.7) * 0.8,
    "click": lambda: click(3000, 0.04, 1.0),
    "key-press": lambda: click(2000, 0.03, 0.8),
    "pop": pop,
    "whoosh-short": lambda: whoosh(0.42),
    "whoosh": lambda: whoosh(0.7),
    "notification": notification,
    "ping": lambda: bell([(1975.5, 1), (3951, 0.2)], 0.45, 0.15),
    "chime": lambda: bell([(1046.5, 1), (1568, 0.6), (2093, 0.3)], 0.8, 0.3),
    "typing": typing,
    "sparkle": sparkle,
}


def write_mp3(name, x):
    x = x / (np.abs(x).max() + 1e-9) * 0.89
    st = np.stack([x, x], 1)
    wav = os.path.join(KIT, name + ".tmp.wav")
    with wave.open(wav, "w") as f:
        f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR)
        f.writeframes((st * 32767).astype(np.int16).tobytes())
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", wav, "-c:a", "libmp3lame", "-q:a", "2",
                    os.path.join(KIT, name + ".mp3")], check=True)
    os.remove(wav)


def main():
    os.makedirs(KIT, exist_ok=True)
    for name, fn in KITSET.items():
        p = os.path.join(KIT, name + ".mp3")
        if os.path.exists(p) and "--force" not in sys.argv:
            continue                      # her real file wins
        write_mp3(name, fn())
        print("made", name)
    subprocess.run([sys.executable, os.path.join(ROOT, "tools", "sfx.py"), "synth"], check=True)


if __name__ == "__main__":
    main()
