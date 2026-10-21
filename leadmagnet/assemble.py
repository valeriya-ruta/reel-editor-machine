# -*- coding: utf-8 -*-
"""Final film: plate + beat renders + subtitles + sound design.

    python3 leadmagnet/assemble.py            -> $LM_SRC/final.mp4

Beat renders replace the plate in their windows (each starts and ends on the
full-frame camera, so the joins are invisible). SFX cues are read straight
out of each beat's generated page: clicks, typing, flashes, pops.
"""
import json, os, re, subprocess, sys, wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.environ.get("LM_SRC", "/home/user/lm-src")
SR = 48000
FPS = 30


def synth():
    rng = np.random.default_rng(3)

    def env(n, a, d):
        t = np.arange(n) / SR
        return np.minimum(1, t / a) * np.exp(-t / d)
    n = int(0.05 * SR)
    click = rng.standard_normal(n) * env(n, 0.0008, 0.006)
    click = np.convolve(click, np.ones(6) / 6, "same") * 0.5
    keys = []
    for i in range(6):
        k = rng.standard_normal(int(0.03 * SR)) * env(int(0.03 * SR), 0.0005, 0.004 + i * 0.0005)
        keys.append(np.convolve(k, np.ones(4) / 4, "same") * 0.22)
    n = int(0.55 * SR)
    t = np.arange(n) / SR
    noise = rng.standard_normal(n)
    sm = np.convolve(noise, np.ones(40) / 40, "same")
    whoosh = sm * np.sin(np.pi * t / t[-1]) ** 2 * 1.6
    n = int(0.09 * SR)
    t = np.arange(n) / SR
    pop = np.sin(2 * np.pi * (520 + 2600 * t) * t) * env(n, 0.002, 0.025) * 0.28
    n = int(0.25 * SR)
    t = np.arange(n) / SR
    draw = np.convolve(rng.standard_normal(n), np.ones(3) / 3, "same") * 0.05 * np.sin(np.pi * t / t[-1])
    return dict(click=click, keys=keys, whoosh=whoosh, pop=pop, draw=draw)


def cues(beat_dir, t0):
    html = open(os.path.join(beat_dir, "index.html")).read()
    out = []
    for m in re.finditer(r"LM\.click\(tl,([0-9.]+)\)", html):
        out.append((t0 + float(m.group(1)), "click", 0))
    for m in re.finditer(r"LM\.flash\(tl,([0-9.]+)", html):
        out.append((t0 + float(m.group(1)) - 0.25, "whoosh", 0))
    for m in re.finditer(r'LM\.type\(tl,([0-9.]+),"[^"]+",("(?:[^"\\]|\\.)*"),(\d+)', html):
        n = len(json.loads(m.group(2)))
        out.append((t0 + float(m.group(1)), "type", n / float(m.group(3))))
    for m in re.finditer(r'LM\.pop\(tl,"[^"]+",([0-9.]+)', html):
        out.append((t0 + float(m.group(1)), "pop", 0))
    for m in re.finditer(r'LM\.(?:ex)\(tl,([0-9.]+),', html):
        out.append((t0 + float(m.group(1)), "draw", 0))
    return out


def main():
    beats = []
    for b in sorted(os.listdir(os.path.join(HERE, "beats"))):
        d = os.path.join(HERE, "beats", b)
        if os.path.exists(os.path.join(d, "out.mp4")) and os.path.exists(os.path.join(d, "beat.json")):
            j = json.load(open(os.path.join(d, "beat.json")))
            beats.append((j["t0"], j["t1"], d))
    print("beats:", len(beats))
    # ---- audio
    w = wave.open(os.path.join(SRC, "plate.wav"))
    ch = w.getnchannels()
    voice = np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, ch).astype(np.float32) / 32768
    mono = np.zeros(len(voice), np.float32)
    K = synth()
    allc = []
    for t0, t1, d in beats:
        allc += cues(d, t0)
    last = {}
    for t, n, dur in sorted(allc):
        if t - last.get(n, -9) < (0.12 if n != "draw" else 0.6):
            continue
        last[n] = t
        i = int(t * SR)
        if n == "type":
            k = 0
            tt = t
            while tt < t + dur:
                s = K["keys"][k % 6]
                j = int(tt * SR)
                if j + len(s) < len(mono):
                    mono[j:j + len(s)] += s
                tt += 0.055 + 0.03 * ((k * 7) % 5) / 5
                k += 1
            continue
        s = K[n]
        if i + len(s) < len(mono) and i >= 0:
            mono[i:i + len(s)] += s * {"click": 0.9, "whoosh": 0.35, "pop": 0.6, "draw": 0.8}[n]
    mix = voice + mono[:, None] * 0.55
    mix = np.clip(mix, -1, 1)
    o = wave.open(os.path.join(SRC, "final.wav"), "w")
    o.setnchannels(ch); o.setsampwidth(2); o.setframerate(SR)
    o.writeframes((mix * 32767).astype(np.int16).tobytes()); o.close()
    print("cues:", len(allc))
    if "--audio-only" in sys.argv:
        return
    # ---- video
    args = ["ffmpeg", "-v", "error", "-stats", "-y", "-i", os.path.join(SRC, "plate_v.mp4")]
    for t0, t1, d in beats:
        args += ["-itsoffset", f"{t0:.4f}", "-i", os.path.join(d, "out.mp4")]
    args += ["-i", os.path.join(SRC, "final.wav")]
    fg, last = [], "0:v"
    for k, (t0, t1, d) in enumerate(beats):
        fg.append(f"[{last}][{k + 1}:v]overlay=enable='between(t,{t0:.4f},{t1 - 0.001:.4f})':eof_action=pass[v{k}]")
        last = f"v{k}"
    fonts = os.path.join(HERE, "hf", "assets", "fonts")
    fg.append(f"[{last}]subtitles={os.path.join(HERE, 'subs.ass')}:fontsdir={fonts},format=yuv420p[vout]")
    args += ["-filter_complex", ";".join(fg), "-map", "[vout]", "-map", f"{len(beats) + 1}:a",
             "-c:v", "libx264", "-preset", os.environ.get("LM_PRESET", "veryfast"), "-crf", "20", "-r", "30",
             "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", os.path.join(SRC, "final.mp4")]
    if "--dry" in sys.argv:
        print(" ".join(args)[:2000]); return
    subprocess.run(args, check=True)
    print("final done")


if __name__ == "__main__":
    main()
