# -*- coding: utf-8 -*-
"""Cut the 22-min raw take into a 1920x1080 plate.

    python3 leadmagnet/cut.py            # plan  -> leadmagnet/edl.json
    python3 leadmagnet/cut.py --render   # plate -> $LM_SRC/plate.mp4 (+ plate.wav)

Silences come from the audio envelope, not from Whisper: anything quieter than
SIL_DB for longer than MIN_SIL is squeezed down to a breath. DROPS are the
fumbled lines, by source time; every edge is snapped to the quietest 10 ms
nearby so no cut lands inside a syllable.

Framing alternates base / in (pure centred scale, her rule from the reels:
"100 > 110 > 100 but XY stay 0") so the jump cuts read as punch-ins.
"""
import json, os, subprocess, sys, wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.environ.get("LM_SRC", "/home/user/lm-src")
RAW = os.path.join(SRC_DIR, "raw.bin")
WAV = os.path.join(SRC_DIR, "audio48k.wav")
FPS = 30
OUT_W, OUT_H = 1920, 1080

SIL_DB = -38.0      # quieter than this is silence
MIN_SIL = 0.40      # shorter pauses are left alone
KEEP_AIR = 0.22     # a squeezed pause keeps this much
BREAK_AIR = 0.70    # ... and this much at a chapter break (pause > 3 s)
SNAP = 0.15         # search radius for the quietest point at a drop edge

# Fumbled lines, source seconds. Her call on the retake: the last take wins.
DROPS = [
    (0.00, 0.60, "lead-in"),
    (1011.60, 1026.40, "retake: keep only «Так от, є секретний промт… І є телеграм-бот.»"),
    (1077.50, 1079.60, "«На комп'ютер.» repeated"),
    (1082.50, 1085.00, "«На комп'ютері.» repeated"),
    (1200.40, 1204.50, "«Тому, як би.»"),
    (1251.40, 1255.10, "«і зможеш вже постати все.» — said again right after"),
]

FRAMES = {"base": 1.00, "in": 1.10}


def envelope():
    w = wave.open(WAV)
    sr = w.getframerate()
    a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32)
    a = a.reshape(-1, w.getnchannels()).mean(1) / 32768
    hop = sr // 100
    n = len(a) // hop
    r = np.sqrt((a[: n * hop].reshape(n, hop) ** 2).mean(1))
    return 20 * np.log10(r + 1e-9), n / 100.0


def quietest(db, t):
    i0, i1 = int((t - SNAP) * 100), int((t + SNAP) * 100)
    i0 = max(i0, 0)
    return (i0 + int(np.argmin(db[i0:i1]))) / 100.0


def plan():
    db, total = envelope()
    quiet = db < SIL_DB
    # silent runs
    sil, i, n = [], 0, len(quiet)
    while i < n:
        if quiet[i]:
            j = i
            while j < n and quiet[j]:
                j += 1
            if (j - i) / 100 >= MIN_SIL:
                sil.append((i / 100, j / 100))
            i = j
        else:
            i += 1
    removed = []
    for a, b in sil:
        air = BREAK_AIR if b - a > 3.0 else KEEP_AIR
        lead = min(0.12, air / 2) if air == KEEP_AIR else air * 0.55
        tail = air - lead
        if b - a > air:
            removed.append((a + lead, b - tail, "pause"))
    for a, b, why in DROPS:
        a2 = quietest(db, a) if a > 0 else 0.0
        removed.append((a2, quietest(db, b), why))
    removed.sort()
    # merge overlapping removals
    merged = []
    for a, b, why in removed:
        if merged and a <= merged[-1][1] + 0.05:
            merged[-1] = (merged[-1][0], max(merged[-1][1], b), merged[-1][2] if merged[-1][2] != "pause" else why)
        else:
            merged.append((a, b, why))
    # keeps = complement, frame-quantised in output time
    keeps, t = [], 0.0
    for a, b, why in merged:
        if a - t > 0.05:
            keeps.append([t, a, why])
        t = b
    if total - t > 0.05:
        keeps.append([t, total, "end"])
    # a sliver with no word in it is a breath or a click: drop it
    words = [w for sg in json.load(open(os.path.join(HERE, "transcript.json")))["segments"]
             for w in sg["words"]]
    keeps = [k_ for k_ in keeps if k_[1] - k_[0] >= 0.5 or
             any(w["s"] < k_[1] and w["e"] > k_[0] for w in words)]
    segs, out, k, prev = [], 0, 0, 99.0
    for s, e, why in keeps:
        nf = max(1, round((e - s) * FPS))
        if prev >= 1.5:          # no zoom step after a sliver: it would flicker
            k += 1
        frame = ["base", "in"][k % 2]
        prev = e - s
        segs.append({"src": round(s, 3), "nf": nf, "out": out, "frame": frame, "cut_after": why})
        out += nf
    edl = {"fps": FPS, "frames": out, "duration": out / FPS, "segments": segs,
           "drops": [list(d) for d in DROPS]}
    json.dump(edl, open(os.path.join(HERE, "edl.json"), "w"), indent=1, ensure_ascii=False)
    print(f"{len(segs)} segments, {out/FPS/60:.2f} min (source {total/60:.2f} min)")
    return edl


def src_to_out(edl, t):
    """Map a source time to plate time (None if it was cut)."""
    for s in edl["segments"]:
        d = s["nf"] / FPS
        if s["src"] <= t < s["src"] + d:
            return s["out"] / FPS + (t - s["src"])
    return None


def render(edl):
    tmp = os.path.join(SRC_DIR, "segs")
    os.makedirs(tmp, exist_ok=True)
    lst = []
    for i, s in enumerate(edl["segments"]):
        f = os.path.join(tmp, f"s{i:04d}.mp4")
        lst.append(f"file '{f}'")
        if os.path.exists(f):
            continue
        z = FRAMES[s["frame"]]
        cw, ch = int(3840 / z) // 2 * 2, int(2160 / z) // 2 * 2
        vf = (f"crop={cw}:{ch}:{(3840-cw)//2}:{(2160-ch)//2},scale={OUT_W}:{OUT_H}:flags=lanczos,"
              f"fps={FPS},format=yuv420p")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s['src']:.3f}", "-i", RAW,
                        "-frames:v", str(s["nf"]), "-an", "-vf", vf, "-c:v", "libx264",
                        "-preset", "veryfast", "-crf", "17", "-g", "60", f], check=True)
        print("seg", i, flush=True)
    open(os.path.join(tmp, "list.txt"), "w").write("\n".join(lst) + "\n")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i",
                    os.path.join(tmp, "list.txt"), "-c", "copy",
                    os.path.join(SRC_DIR, "plate_v.mp4")], check=True)
    # audio: exact-length pieces with 6 ms fades at every joint
    w = wave.open(WAV)
    sr, ch = w.getframerate(), w.getnchannels()
    a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1, ch).astype(np.float32)
    parts, fade = [], int(0.006 * sr)
    ramp = np.linspace(0, 1, fade)[:, None]
    for s in edl["segments"]:
        i0 = int(round(s["src"] * sr))
        n = int(round(s["nf"] / FPS * sr))
        p = a[i0:i0 + n].copy()
        if len(p) < n:
            p = np.vstack([p, np.zeros((n - len(p), ch), np.float32)])
        p[:fade] *= ramp
        p[-fade:] *= ramp[::-1]
        parts.append(p)
    out = np.clip(np.vstack(parts), -32768, 32767).astype(np.int16)
    o = wave.open(os.path.join(SRC_DIR, "plate.wav"), "w")
    o.setnchannels(ch); o.setsampwidth(2); o.setframerate(sr)
    o.writeframes(out.tobytes()); o.close()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(SRC_DIR, "plate_v.mp4"),
                    "-i", os.path.join(SRC_DIR, "plate.wav"), "-c:v", "copy", "-c:a", "aac",
                    "-b:a", "192k", "-shortest", os.path.join(SRC_DIR, "plate.mp4")], check=True)
    print("plate done")


if __name__ == "__main__":
    edl = plan()
    if "--render" in sys.argv:
        render(edl)
