# -*- coding: utf-8 -*-
"""Make the basic sound-effects kit in assets/sfx/ (Ruta, 2026-11-05: "basic
sound effects should be included (typing, whooshing etc)").

    python tools/sfxkit.py

Synthesised, so the folder carries its own kit and needs nothing from Ruta's
laptop. Names are the ones tools/sfx.py already levels: click-soft, click,
key-press, typing, pop, whoosh-short, whoosh, ping, notification, sparkle,
kaching. To use a better recorded sound, drop a file with the same name into
assets/sfx/ (wav/mp3) and it wins.
"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sfx import KIT, SR, bandnoise, write_wav, synth_kaching  # noqa: E402

rng = np.random.default_rng(11)


def env(n, attack, decay):
    t = np.arange(n) / SR
    return np.clip(t / max(attack, 1e-4), 0, 1) * np.exp(-t / decay)


def click(dur=0.03, lo=2500, hi=9000, decay=0.004, body=0.0):
    n = int(SR * dur)
    x = bandnoise(n, lo, hi, rng) * env(n, 0.0003, decay)
    if body:
        t = np.arange(n) / SR
        x += body * np.sin(2 * np.pi * 900 * t) * np.exp(-t / 0.006)
    return x / np.abs(x).max()


def key_press():
    a = click(0.05, 1500, 7000, 0.006, 0.4)
    b = click(0.05, 800, 3000, 0.010) * 0.35       # the key coming back up
    out = np.zeros(int(SR * 0.12))
    out[:len(a)] += a
    i = int(SR * 0.06)
    out[i:i + len(b)] += b
    return out / np.abs(out).max()


def typing(secs=1.6):
    out = np.zeros(int(SR * secs))
    t = 0.02
    while t < secs - 0.12:
        k = key_press() * rng.uniform(0.55, 1.0)
        i = int(t * SR)
        out[i:i + len(k)] += k[: len(out) - i]
        t += rng.uniform(0.07, 0.16)
    return out / np.abs(out).max()


def pop():
    n = int(SR * 0.12)
    t = np.arange(n) / SR
    f = 380 + 900 * np.exp(-t / 0.012)               # quick downward pitch
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.001, 0.03)
    x += 0.25 * click(0.12, 3000, 9000, 0.003)
    return x / np.abs(x).max()


def whoosh(secs):
    n = int(SR * secs)
    t = np.arange(n) / SR
    x = np.zeros(n)
    # a band of noise that sweeps up then down, swelling to the middle
    for lo, hi, g in ((300, 1200, 1.0), (1200, 3500, 0.6), (3500, 8000, 0.25)):
        x += g * bandnoise(n, lo, hi, rng)
    shape = np.sin(np.pi * np.clip(t / secs, 0, 1)) ** 2.2
    x *= shape
    return x / np.abs(x).max()


def bell(f0, secs, partials=((1, 1, 0.5), (2.01, 0.4, 0.3), (3.0, 0.2, 0.15))):
    n = int(SR * secs)
    t = np.arange(n) / SR
    x = sum(a * np.sin(2 * np.pi * f0 * r * t) * np.exp(-t / d) for r, a, d in partials)
    x *= np.clip(t / 0.002, 0, 1)
    return x / np.abs(x).max()


def notification():
    a, b = bell(1318.5, 0.5), bell(1760.0, 0.7)
    out = np.zeros(int(SR * 0.85))
    out[:len(a)] += a * 0.8
    i = int(SR * 0.11)
    out[i:i + len(b)] += b[: len(out) - i]
    return out / np.abs(out).max()


def sparkle():
    out = np.zeros(int(SR * 0.9))
    for k, f in enumerate((2637, 3136, 3951, 4699, 5274)):
        b = bell(f, 0.45, ((1, 1, 0.12), (2.0, 0.3, 0.06)))
        i = int(SR * (0.06 * k + rng.uniform(0, 0.02)))
        out[i:i + len(b)] += b[: len(out) - i] * (1 - 0.12 * k)
    return out / np.abs(out).max()


KITS = {
    "click-soft": lambda: click(0.03, 1500, 6000, 0.003) * 0.7,
    "click": lambda: click(0.04, 2000, 9000, 0.005, 0.5),
    "key-press": key_press,
    "typing": typing,
    "pop": pop,
    "whoosh-short": lambda: whoosh(0.35),
    "whoosh": lambda: whoosh(0.7),
    "ping": lambda: bell(1760.0, 0.6),
    "notification": notification,
    "sparkle": sparkle,
}

if __name__ == "__main__":
    os.makedirs(KIT, exist_ok=True)
    for name, fn in KITS.items():
        if any(os.path.exists(os.path.join(KIT, name + e)) for e in (".mp3", ".m4a")):
            continue
        a = fn()
        n = len(a)
        a = a * np.minimum(1, (n - np.arange(n)) / (0.01 * SR))   # no click at the end
        write_wav(os.path.join(KIT, name + ".wav"), a * 0.89)
    synth_kaching()
    print("kit ->", KIT, sorted(os.listdir(KIT)))
