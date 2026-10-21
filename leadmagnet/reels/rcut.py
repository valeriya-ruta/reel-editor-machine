# -*- coding: utf-8 -*-
"""Cut the 8 lead-magnet reels out of the 4K take, vertical.

    python3 leadmagnet/reels/rcut.py            # plan all -> reels/rNN/cut.json
    python3 leadmagnet/reels/rcut.py --render   # + rNN/plate.mp4 (1080x1920) + voice.wav

A reel is a list of kept word ranges (indices into words.json, Whisper's words
of the raw take). Each range becomes a source span; inside it every pause
longer than MIN_SIL is squeezed to a breath. Framing alternates base / in
(pure centred scale) across cuts, like her other reels.

cut.json carries, per segment, the source start and the reel start, so the
build can map any source time (a word, a long-video beat) onto the reel.
"""
import json, os, subprocess, sys, wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.environ.get("LM_SRC", "/home/user/lm-src")
RAW = os.path.join(SRC, "raw.bin")
WAV = os.path.join(SRC, "audio48k.wav")
FPS = 30
W = json.load(open(os.path.join(HERE, "words.json")))

SIL_DB, MIN_SIL, AIR, PAD_IN, PAD_OUT = -38.0, 0.30, 0.14, 0.06, 0.12
ZOOM = {"base": 1.0, "in": 1.05}

# kept word ranges (inclusive), from her brief of 2026-10-21
REELS = {
    1: [(1956, 1974), (1977, 1992), (1998, 2051), (2055, 2094), (2097, 2126)],
    2: [(2580, 2593), (2596, 2613), (2668, 2706), (2710, 2715), (2727, 2738), (2740, 2744),
        (2755, 2758), (2761, 2768), (2789, 2808), (2895, 2911), (2928, 2934), (2937, 2942),
        (2956, 2968), (3017, 3032)],
    3: [(997, 1094)],
    4: [(38, 157)],
    5: [(656, 761)],
    6: [(1455, 1460), (1482, 1485), (1503, 1530), (1537, 1630), (1653, 1684), (1707, 1769)],
    7: [(250, 349)],
    8: [(2163, 2264), (2268, 2275), (2286, 2296)],
}


def envelope():
    w = wave.open(WAV)
    sr = w.getframerate()
    a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)
    a = a.reshape(-1, w.getnchannels()).mean(1) / 32768
    hop = sr // 100
    n = len(a) // hop
    r = np.sqrt((a[: n * hop].reshape(n, hop) ** 2).mean(1))
    return 20 * np.log10(r + 1e-9)


DB = None


def quiet(t0, t1):
    i0, i1 = max(0, int(t0 * 100)), int(t1 * 100)
    return (i0 + int(np.argmin(DB[i0:i1]))) / 100.0 if i1 > i0 else t0


def spans_for(ranges):
    out = []
    for a, b in ranges:
        s = W[a][1] - PAD_IN
        e = W[b][2] + PAD_OUT
        # snap the edges into the quietest 10 ms nearby so no syllable is clipped
        s = quiet(s - 0.12, s + 0.04)
        e = quiet(e - 0.04, e + 0.15)
        # squeeze pauses inside
        cur = s
        i = int(s * 100)
        while i < int(e * 100):
            if DB[i] < SIL_DB:
                j = i
                while j < int(e * 100) and DB[j] < SIL_DB:
                    j += 1
                if (j - i) / 100 >= MIN_SIL:
                    cut_a = i / 100 + AIR / 2
                    cut_b = j / 100 - AIR / 2
                    if cut_a - cur > 0.05:
                        out.append([cur, cut_a])
                    cur = cut_b
                i = j
            else:
                i += 1
        if e - cur > 0.05:
            out.append([cur, e])
    return out


def plan(k):
    spans = spans_for(REELS[k])
    segs, out, n, prev = [], 0, 0, 9
    for s, e in spans:
        nf = max(1, round((e - s) * FPS))
        if prev >= 1.2:
            n += 1
        segs.append({"src": round(s, 3), "nf": nf, "out": out, "frame": ["base", "in"][n % 2]})
        prev = e - s
        out += nf
    d = os.path.join(HERE, "r%02d" % k)
    os.makedirs(d, exist_ok=True)
    j = {"fps": FPS, "frames": out, "duration": out / FPS, "segments": segs, "ranges": REELS[k]}
    json.dump(j, open(os.path.join(d, "cut.json"), "w"), indent=1)
    return j


def render(k, j):
    d = os.path.join(HERE, "r%02d" % k)
    tmp = os.path.join(SRC, "rsegs%02d" % k)
    os.makedirs(tmp, exist_ok=True)
    lst = []
    for i, s in enumerate(j["segments"]):
        f = os.path.join(tmp, "s%03d.mp4" % i)
        lst.append("file '%s'" % f)
        z = ZOOM[s["frame"]]
        ch = int(2160 / z) // 2 * 2
        cw = int(ch * 9 / 16) // 2 * 2
        vf = ("crop=%d:%d:%d:%d,scale=1080:1920:flags=lanczos,fps=30,format=yuv420p"
              % (cw, ch, (3840 - cw) // 2, (2160 - ch) // 2))
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "%.3f" % s["src"], "-i", RAW,
                        "-frames:v", str(s["nf"]), "-an", "-vf", vf, "-c:v", "libx264",
                        "-preset", "veryfast", "-crf", "16", "-g", "30", f], check=True)
    open(os.path.join(tmp, "list.txt"), "w").write("\n".join(lst) + "\n")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i",
                    os.path.join(tmp, "list.txt"), "-c", "copy", os.path.join(d, "plate.mp4")], check=True)
    subprocess.run(["rm", "-rf", tmp])
    w = wave.open(WAV)
    sr, ch = w.getframerate(), w.getnchannels()
    a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1, ch).astype(np.float32)
    parts, fade = [], int(0.006 * sr)
    ramp = np.linspace(0, 1, fade)[:, None]
    for s in j["segments"]:
        i0 = int(round(s["src"] * sr))
        n = int(round(s["nf"] / FPS * sr))
        p = a[i0:i0 + n].copy()
        p[:fade] *= ramp
        p[-fade:] *= ramp[::-1]
        parts.append(p)
    o = wave.open(os.path.join(d, "voice.wav"), "w")
    o.setnchannels(ch); o.setsampwidth(2); o.setframerate(sr)
    o.writeframes(np.clip(np.vstack(parts), -32768, 32767).astype(np.int16).tobytes()); o.close()


if __name__ == "__main__":
    DB = envelope()
    ks = [int(x) for x in sys.argv[1:] if x.isdigit()] or sorted(REELS)
    for k in ks:
        j = plan(k)
        print("r%02d %d segs %.1fs" % (k, len(j["segments"]), j["duration"]))
        if "--render" in sys.argv:
            render(k, j)
