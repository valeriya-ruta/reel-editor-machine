# -*- coding: utf-8 -*-
"""Reel 41 plate: her intro, the 5-minute screen session as a time-lapse that
brakes into real time, then the last take of her outro.

    python3 work/r41/ramp.py          # plan only -> work/r41/cut.json
    python3 work/r41/ramp.py --render # plate    -> reel-41/assets/base.mp4

This reel is the one exception to "never re-cut her footage": it came as one
raw 364 s take (her talking, the laptop screen, her again) and her brief was
the cut itself:

  - intro as is; the switch from her face to the screen lands on her last
    word («Дивіться!» ends 7.55, her camera switch is at 7.61), no dead air
  - the long stretch of work super fast
  - the last bit of the screen slowed back to real time, so it reads as
    happening live, then straight to her
  - the outro is the last take (she says it twice: 333.1 and 349.8)
  - the whole reel well under a minute

The screen recording has two visible events near its end (frame-difference
probe over 280-333.5 s): the inbox switches to a profile at 311.7 and the
profile card changes at 313.1. Nothing moves after that, so the real-time
hold covers 310.6-313.8 and the 20 still seconds after it are dropped.

Speed map (output time -> source time):
  intro   1x
  fast    V x, constant
  brake   speed falls geometrically V -> 1 over BRAKE s
  hold    1x
  outro   1x
Audio: her voice on the two talking parts; across the time-lapse a soft
clock tick, one per TICK_EVERY source seconds, so the ticks slow down with
the picture and stop when it reaches real time (the hold has the room tone).
"""
import io
import json
import math
import os
import subprocess
import sys
import wave

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WORK = os.path.join(ROOT, "work", "r41")
SRC = os.environ.get("R41_SRC", "/home/user/src-r41/src.mp4")   # the raw take, see SOURCE.txt
OUT = os.path.join(ROOT, "reel-41", "assets", "base.mp4")
FPS = 30
W, H = 1080, 1920
SR = 48000

INTRO = (0.45, 7.61)          # her; 7.61 is her own camera switch to the screen
SCREEN_END = 313.80           # last frame of screen we keep
HOLD = 3.20                   # real-time tail, src 310.6 -> 313.8
BRAKE = 1.50                  # output seconds the speed takes to fall V -> 1
V = 27.0                      # time-lapse speed
OUTRO = (349.62, 363.95)      # take 2: «Дякую дуже ...» (voice 349.80-363.65)
VOICE_TAIL = 0.05             # intro audio runs a hair past the picture cut
TICK_EVERY = 6.0              # source seconds per tick


def plan():
    k = math.log(V) / BRAKE
    brake_src = (V - 1.0) / k                 # source seconds eaten by the brake
    r1 = SCREEN_END - HOLD                    # hold starts here (src)
    r0 = r1 - brake_src                       # brake starts here (src)
    t1 = INTRO[1] - INTRO[0]
    t2 = t1 + (r0 - INTRO[1]) / V
    t3 = t2 + BRAKE
    t4 = t3 + HOLD
    t5 = t4 + (OUTRO[1] - OUTRO[0])
    return {"V": V, "k": k, "r0": r0, "r1": r1, "t1": t1, "t2": t2, "t3": t3,
            "t4": t4, "dur_src": t5}


def src_of(t, p):
    """source second shown at output second t"""
    if t < p["t1"]:
        return INTRO[0] + t
    if t < p["t2"]:
        return INTRO[1] + V * (t - p["t1"])
    if t < p["t3"]:
        tau = t - p["t2"]
        return p["r0"] + V * (1.0 - math.exp(-p["k"] * tau)) / p["k"]
    if t < p["t4"]:
        return p["r1"] + (t - p["t3"])
    return OUTRO[0] + (t - p["t4"])


def frames(p):
    n = int(round(p["dur_src"] * FPS))
    return n, [src_of((i + 0.5) / FPS, p) for i in range(n)]


# ---------------------------------------------------------------- video

def decode(start, end):
    """frames of [start, end) at 30 fps, 1080x1920, as a generator of
    (src_time, bytes)"""
    cmd = ["ffmpeg", "-nostdin", "-v", "error", "-ss", "%.3f" % start, "-to", "%.3f" % end,
           "-i", SRC, "-an", "-vf", "fps=%d,scale=%d:%d:flags=lanczos" % (FPS, W, H),
           "-pix_fmt", "yuv420p", "-f", "rawvideo", "-"]
    pr = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1 << 24)
    size = W * H * 3 // 2
    i = 0
    try:
        while True:
            b = pr.stdout.read(size)
            if len(b) < size:
                break
            yield start + i / float(FPS), b
            i += 1
    finally:
        pr.kill()
        pr.wait()


def render_video(p, path):
    n, want = frames(p)
    enc = subprocess.Popen(
        ["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "yuv420p",
         "-s", "%dx%d" % (W, H), "-r", str(FPS), "-i", "-",
         "-c:v", "libx264", "-crf", "18", "-preset", "fast", "-pix_fmt", "yuv420p", path],
        stdin=subprocess.PIPE)
    # three decode passes: intro, screen (intro end -> SCREEN_END), outro
    spans = [(INTRO[0], INTRO[1]), (INTRO[1], SCREEN_END), (OUTRO[0], OUTRO[1] + 0.2)]
    i = 0
    for a, b in spans:
        prev = None
        for ts, fr in decode(a, b):
            # a decoded frame covers [ts - 1/60, ts + 1/60): it serves every
            # wanted output frame up to the end of that window
            while i < n and want[i] < b and want[i] < ts + 0.5 / FPS:
                enc.stdin.write(fr)
                i += 1
            prev = fr
            if i >= n or want[i] >= b:
                break
        while i < n and want[i] < b:          # ran off the end of the span
            enc.stdin.write(prev)
            i += 1
        print("span %.2f-%.2f done, %d/%d frames" % (a, b, i, n), flush=True)
    enc.stdin.close()
    enc.wait()
    assert i == n, (i, n)


# ---------------------------------------------------------------- audio

def load_audio():
    tmp = os.path.join(WORK, "src48.wav")
    if not os.path.exists(tmp):
        subprocess.check_call(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", SRC, "-vn",
                               "-ac", "2", "-ar", str(SR), tmp])
    w = wave.open(tmp)
    a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768.0
    return a.reshape(-1, 2)


def tick():
    """a soft wooden clock tick: a short noise burst through a resonance"""
    n = int(0.06 * SR)
    t = np.arange(n) / SR
    rng = np.random.RandomState(7)
    click = rng.randn(n) * np.exp(-t / 0.0025)
    body = np.sin(2 * np.pi * 1850 * t) * np.exp(-t / 0.012) + \
        0.5 * np.sin(2 * np.pi * 3100 * t) * np.exp(-t / 0.006)
    x = 0.35 * click + body
    return x / np.abs(x).max()


def fade(x, fi, fo):
    x = x.copy()
    a, b = int(fi * SR), int(fo * SR)
    if a:
        x[:a] *= np.linspace(0, 1, a)[:, None]
    if b:
        x[-b:] *= np.linspace(1, 0, b)[:, None]
    return x


def render_audio(p, path):
    src = load_audio()
    total = int(round(p["dur_src"] * SR))
    out = np.zeros((total, 2), np.float32)

    def place(t_out, s0, s1, fi=0.01, fo=0.01, gain=1.0):
        seg = fade(src[int(s0 * SR):int(s1 * SR)], fi, fo) * gain
        a = int(t_out * SR)
        seg = seg[:max(0, total - a)]
        out[a:a + len(seg)] += seg

    voice_peak = np.abs(src[int(OUTRO[0] * SR):int(OUTRO[1] * SR)]).max()
    place(0.0, INTRO[0], INTRO[1] + VOICE_TAIL, fi=0.02, fo=0.04)
    place(p["t3"], p["r1"], SCREEN_END, fi=0.15, fo=0.02)        # the real-time room
    place(p["t4"], OUTRO[0], OUTRO[1], fi=0.02, fo=0.12)

    # ticks: one each time the shown source time crosses a multiple of TICK_EVERY
    tk = tick() * voice_peak * 10 ** (-16 / 20.0)
    ticks = []
    t = p["t1"]
    last = math.floor(src_of(t, p) / TICK_EVERY)
    while t < p["t3"]:
        cur = math.floor(src_of(t, p) / TICK_EVERY)
        if cur != last:
            ticks.append(round(t, 3))
            last = cur
        t += 1.0 / SR * 16
    for t in ticks:
        a = int(t * SR)
        seg = tk[:max(0, total - a)]
        out[a:a + len(seg), 0] += seg
        out[a:a + len(seg), 1] += seg
    p["ticks"] = len(ticks)

    pcm = (np.clip(out, -1, 1) * 32767).astype(np.int16)
    w = wave.open(path, "wb")
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
    w.close()


def main():
    p = plan()
    n, want = frames(p)
    p["frames"] = n
    p["DUR"] = round((n - 0.5) / FPS, 3)
    p["intro"] = INTRO
    p["outro"] = OUTRO
    p["screen_end"] = SCREEN_END
    print(json.dumps({k: (round(v, 3) if isinstance(v, float) else v) for k, v in p.items()}))
    if "--render" in sys.argv:
        vid = os.path.join(WORK, "plate_v.mp4")
        aud = os.path.join(WORK, "plate_a.wav")
        render_audio(p, aud)
        render_video(p, vid)
        subprocess.check_call(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", vid, "-i", aud,
                               "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac",
                               "-b:a", "192k", "-shortest", OUT])
        print("PLATE", OUT)
    json.dump({k: v for k, v in p.items()}, io.open(os.path.join(WORK, "cut.json"), "w"),
              indent=1)


if __name__ == "__main__":
    main()
