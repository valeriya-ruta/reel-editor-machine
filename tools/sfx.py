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
SCRATCH = os.environ.get("REELS_SCRATCH", "E:/reels-work")   # cloud: set to work/scratch
CACHE = os.path.join(SCRATCH, "sfxcache")
SR = 48000

# peak of the effect, in dB below the peak of her voice
LEVEL = {
    "click-soft": 14, "click": 14, "key-press": 15, "typing": 17,
    "pop": 13, "whoosh-short": 15, "whoosh": 15, "whoosh-cinematic": 18,
    "kaching": 10, "notification": 13, "ping": 15, "chime": 17, "sparkle": 18,
    "impact-bass-1": 16, "pencil": 19, "riser": 20, "glitch-1": 20,
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


def _env(n, a, d):
    t = np.arange(n) / SR
    return np.clip(t / max(a, 1e-4), 0, 1) * np.exp(-np.clip(t - a, 0, None) / d)


def synth_kit():
    """The rest of the kit, synthesised so a fresh cloud checkout can mix sound
    without her local assets/sfx. If her .mp3 originals are present they win
    (mix() looks for .mp3 first). 'pencil' is new with the Google x Excalidraw
    look (STYLE.md §0b): a marker scratching on a whiteboard, under a draw-on."""
    rng = np.random.default_rng(11)

    def save(name, a):
        a = a / (np.abs(a).max() + 1e-9)
        write_wav(os.path.join(KIT, name + ".wav"), a * 0.89)

    def click(f0, n_ms, hp):
        n = int(SR * n_ms / 1000)
        t = np.arange(n) / SR
        return (bandnoise(n, hp, 9000, rng) * 0.6 + np.sin(2 * np.pi * f0 * t) * 0.5) * _env(n, 0.0008, 0.006)
    save("click", click(2200, 40, 2500))
    save("click-soft", click(1500, 50, 1200) * 0.7)
    save("key-press", click(1800, 35, 3000))
    # typing: a run of key presses with human jitter
    n = int(SR * 1.2); a = np.zeros(n); t = 0.0
    while t < 1.1:
        i = int(t * SR); k = click(1600 + rng.uniform(-300, 300), 30, 2800) * rng.uniform(0.5, 1)
        a[i:i + len(k)] += k[: n - i]; t += rng.uniform(0.07, 0.13)
    save("typing", a)
    # pop: a pitched bubble, quick downward glide
    n = int(SR * 0.16); t = np.arange(n) / SR
    f = 900 * np.exp(-t / 0.05) + 380
    save("pop", np.sin(2 * np.pi * np.cumsum(f) / SR) * _env(n, 0.002, 0.04))
    # whoosh: band noise sweeping up then down, swelled
    for name, dur, lo, hi in (("whoosh-short", 0.42, 300, 5000), ("whoosh", 0.7, 200, 4000)):
        n = int(SR * dur); t = np.arange(n) / SR
        x = bandnoise(n, lo, hi, rng)
        sw = np.sin(np.pi * t / dur) ** 2
        # crude moving filter: blend a low and a high band by position
        xl = bandnoise(n, lo, lo * 4, rng)
        mixp = np.sin(np.pi * t / dur)
        save(name, (x * mixp + xl * (1 - mixp)) * sw)
    # ping / notification: two soft sine bells
    def bell(fs, dur):
        n = int(SR * dur); t = np.arange(n) / SR; o = np.zeros(n)
        for k, (f, t0) in enumerate(fs):
            tt = np.clip(t - t0, 0, None)
            o += (t >= t0) * (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(2 * np.pi * 2.01 * f * tt)) * np.exp(-tt / 0.22)
        return o
    save("ping", bell([(1568, 0)], 0.6))
    save("notification", bell([(1175, 0), (1568, 0.11)], 0.8))
    save("chime", bell([(1047, 0), (1319, 0.08), (1568, 0.16)], 1.0))
    # sparkle: a scatter of tiny high glints
    n = int(SR * 0.7); a = np.zeros(n); t = np.arange(n) / SR
    for k in range(9):
        t0 = rng.uniform(0, 0.45); f = rng.uniform(3500, 7500); tt = np.clip(t - t0, 0, None)
        a += (t >= t0) * np.sin(2 * np.pi * f * tt) * np.exp(-tt / 0.06) * rng.uniform(0.3, 1)
    save("sparkle", a)
    # pencil: marker on a whiteboard — grainy band noise with stroke-rate wobble
    n = int(SR * 0.9); t = np.arange(n) / SR
    x = bandnoise(n, 1800, 7000, rng)
    strokes = 0.55 + 0.45 * np.abs(np.sin(2 * np.pi * 3.2 * t + rng.uniform(0, 3)))
    grain = 0.7 + 0.3 * bandnoise(n, 20, 120, rng)
    save("pencil", x * strokes * grain * np.minimum(1, t / 0.03) * np.minimum(1, (0.9 - t) / 0.15))
    print("kit:", sorted(os.listdir(KIT)))


def mix(nn):
    reel = os.path.join(ROOT, "reel-" + nn)
    voice = os.path.join(reel, "assets", "voice.mp4")
    cues = json.load(open(os.path.join(reel, "sfx.json"), encoding="utf-8"))
    tmp = os.path.join(SCRATCH, "r" + nn)
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
            p = os.path.join(KIT, name + ".mp3")
            if not os.path.exists(p):           # the synthesised kit (python tools/sfx.py synth)
                p = os.path.join(KIT, name + ".wav")
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
                    "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-crf", "17", "-preset", "fast",
                    "-pix_fmt", "yuv420p", "-r", "30", "-g", "30", "-keyint_min", "30",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", base], check=True)
    # a keyframe every second: the local renderer seeks the plate per frame and
    # freezes on sparse keyframes (the cut's concat leaves gaps of 5 s+)
    print("mixed %d cues -> %s" % (len(cues), base))


if __name__ == "__main__":
    if sys.argv[1] == "synth":
        os.makedirs(KIT, exist_ok=True)
        synth_kaching()
        synth_kit()
    elif sys.argv[1] == "mix":
        mix(sys.argv[2])
