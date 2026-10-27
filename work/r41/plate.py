# -*- coding: utf-8 -*-
"""Reel 41 plate: three raw takes -> one landscape 1920x1080 @30 YouTube cut.

    python work/r41/plate.py            # plan only  -> work/r41/timeline.json
    python work/r41/plate.py --render   # plate      -> reel-41/assets/voice.mp4

Her brief, 2026-10-27 (the first long landscape video — YouTube, recorded 16:9,
so none of the 9:16 framing applies):

- open on her «shhh», then her recording the reel on the phone; after two
  seconds of that, sped up and black & white;
- the take where she shows the upload to Google Drive is b-roll while she
  explains how the videos get made;
- the clip ending in 23 (scrolling) is b-roll for the Sunday analytics and
  ideas routine;
- the 48-second piece about not checking the videos + scheduling goes in
  after she talks about the editing;
- cut every bad try and every pause.

The decision list is EDL below: hand-made off the per-utterance ASR
(u151122.jsonl), last take wins. Audio is the A-roll; b-roll only replaces
picture. Everything is frame-quantised: each span is `round(len/speed*30)`
frames and exactly that many samples of audio, so picture and voice never drift.

The front camera mirrors, so the phone screens read backwards in the raw
files. B-roll is flipped back (`hflip`), her talking head is left as filmed.
"""
import json
import os
import subprocess
import sys
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
INC = os.path.join(ROOT, "work", "incoming", "r41")
SRC = {"M": os.path.join(INC, "20261027_151122.mp4"),      # the long take
       "S": os.path.join(INC, "20261027_152423.mp4"),      # scrolling, silent
       "B": os.path.join(INC, "20261027_152651.mp4")}      # the 48 s add-on
FPS, SR = 30, 48000
SW, SH = 3840, 2160
OW, OH = 1920, 1080
SCR = os.environ.get("CUT_SCRATCH", os.path.join(HERE, "scratch"))

# zoom, vertical anchor (0 = crop top, 0.5 = centred). A jump cut is hidden by
# a pure scale step, never a slide (her note on the reel cuts, 2026-10-05).
FRAMES = {
    "base": (1.00, 0.5),
    "in":   (1.14, 0.30),
    "close": (1.32, 0.26),
}

# ---------------------------------------------------------------- the cut
# (source, in, out[, options]). Times are source seconds, cut on word edges.
# options: speed, bw, frame, gain (dB on the audio), atempo (pitch-safe speed)
def load_edl():
    sys.path.insert(0, HERE)
    import edl  # noqa: E402
    return edl


def words(src):
    f = {"M": "u151122.jsonl", "B": "u152651.jsonl"}.get(src)
    if not f:
        return []
    out = []
    for line in open(os.path.join(HERE, f), encoding="utf-8"):
        out += json.loads(line)["words"]
    return out


SPLIT_EVERY = 9.0      # a long span gets a framing change at a word gap about this often


TIGHT = 0.36          # a pause longer than this inside a kept span ...
KEEP_AFTER, KEEP_BEFORE = 0.12, 0.08   # ... is cut down to this much air


def silences(src):
    f = {"M": "sil_151122.txt", "B": "sil_152651.txt"}.get(src)
    if not f:
        return []
    return [tuple(float(x) for x in l.split()) for l in open(os.path.join(HERE, f)) if len(l.split()) == 2]


def tighten(edl_, W):
    """her v1 note: tighten the pauses. Every real pause (silencedetect,
    -36 dB, 0.28 s+) of TIGHT or longer inside a talking span becomes a cut
    that keeps KEEP_AFTER + KEEP_BEFORE of air. Measured on the audio, not
    on whisper's word edges, which stretch into the silence."""
    res = []
    for sp in edl_:
        src, a, b = sp[0], sp[1], sp[2]
        o = dict(sp[3]) if len(sp) > 3 else {}
        if src not in W or o.get("speed", 1.0) != 1.0 or o.get("frame") is not None:
            res.append((src, a, b, o))
            continue
        cur = a
        for s0, s1 in silences(src):
            if s0 > cur + 0.3 and s1 < b - 0.2 and s1 - s0 >= TIGHT:
                res.append((src, cur, round(s0 + KEEP_AFTER, 3), o))
                o = {k: v for k, v in o.items() if k != "tag"}
                cur = round(s1 - KEEP_BEFORE, 3)
        res.append((src, cur, b, o))
    return res


def plan():
    e = load_edl()
    out, t = [], 0
    W = {s: words(s) for s in ("M", "B")}
    for i, sp in enumerate(tighten(e.EDL, W)):
        src, a, b = sp[0], sp[1], sp[2]
        o = dict(sp[3]) if len(sp) > 3 else {}
        speed = o.get("speed", 1.0)
        n = int(round((b - a) / speed * FPS))
        out.append({"i": i, "src": src, "a": a, "b": b, "speed": speed, "frames": n,
                    "start": t, "bw": o.get("bw", False), "frame": o.get("frame"),
                    "gain": o.get("gain", 0.0), "tag": o.get("tag", "")})
        t += n
    # framing inside each span: (frame offset, framing). Alternate base / in at
    # every cut; split long spans at a word gap; punch in on the CLOSE lines.
    cyc, k = ["base", "in"], 0
    for sp in out:
        if sp["frame"] is not None:
            sp["segs"] = [(0, sp["frame"])]
            continue
        cuts = [0]
        if sp["speed"] == 1.0:
            gaps = [(w2["s"] + w1["e"]) / 2 for w1, w2 in zip(W[sp["src"]], W[sp["src"]][1:])
                    if w2["s"] - w1["e"] >= 0.18 and sp["a"] + 2.5 < (w2["s"] + w1["e"]) / 2 < sp["b"] - 2.5]
            last = sp["a"]
            for g in gaps:
                if g - last >= SPLIT_EVERY:
                    cuts.append(int(round((g - sp["a"]) * FPS)))
                    last = g
        segs = []
        for c in cuts:
            segs.append([c, cyc[k % 2]])
            k += 1
        if sp["src"] == "M":
            for ca, cb in e.CLOSE:
                if sp["a"] <= ca < sp["b"]:
                    f0 = int(round((ca - sp["a"]) * FPS))
                    f1 = min(sp["frames"], int(round((cb - sp["a"]) * FPS)))
                    prev = [s for s in segs if s[0] <= f0][-1][1]
                    segs = [s for s in segs if not (f0 <= s[0] < f1)]
                    segs.append([f0, "close"])
                    if f1 < sp["frames"]:
                        segs.append([f1, "in" if prev == "base" else "base"])
                    segs.sort()
        sp["segs"] = [tuple(s) for s in segs]
    rolls = []
    for (anchor, length, src, s_in, speed, frame) in e.BROLL:
        cand = [x for x in out if x["src"] == "M" and x["speed"] == 1.0 and x["b"] > anchor]
        sp = min(cand, key=lambda x: x["a"])
        anchor = max(anchor, sp["a"])
        f0 = sp["start"] + int(round((anchor - sp["a"]) * FPS))
        n = int(round(length * FPS))
        rolls.append({"f0": f0, "frames": n, "src": src, "a": s_in, "speed": speed, "frame": frame})
    rolls.sort(key=lambda r: r["f0"])
    for r1, r2 in zip(rolls, rolls[1:]):
        # tightened pauses pull anchors closer: the earlier shot gives way
        r1["frames"] = min(r1["frames"], r2["f0"] - r1["f0"])
    return out, rolls, t


def pieces(spans, rolls):
    """The video track as a list of encodable pieces: each span's framing
    segments, cut around the b-roll windows."""
    res = []
    for sp in spans:
        s0 = sp["start"]
        bounds = [x[0] for x in sp["segs"]] + [sp["frames"]]
        for (c0, fr), c1 in zip(sp["segs"], bounds[1:]):
            g0, g1 = s0 + c0, s0 + c1
            cur = g0
            for r in rolls:
                r0, r1 = r["f0"], r["f0"] + r["frames"]
                if r1 <= cur or r0 >= g1:
                    continue
                if r0 > cur:
                    res.append(dict(sp, kind="a", frame=fr, f0=cur, n=r0 - cur,
                                    src_in=sp["a"] + (cur - s0) / FPS * sp["speed"]))
                a0, e0 = max(r0, cur), min(r1, g1)
                res.append({"kind": "b", "f0": a0, "n": e0 - a0, "src": r["src"],
                            "src_in": r["a"] + (a0 - r0) / FPS * r["speed"], "speed": r["speed"],
                            "frame": r["frame"], "bw": False})
                cur = e0
            if cur < g1:
                res.append(dict(sp, kind="a", frame=fr, f0=cur, n=g1 - cur,
                                src_in=sp["a"] + (cur - s0) / FPS * sp["speed"]))
    # merge neighbours that are one continuous shot (same source run, same framing)
    merged = []
    for p in res:
        q = merged[-1] if merged else None
        if (q and q["kind"] == p["kind"] == "a" and q["src"] == p["src"] and q["frame"] == p["frame"]
                and q["speed"] == p["speed"] and q.get("bw") == p.get("bw")
                and abs(q["src_in"] + q["n"] / FPS * q["speed"] - p["src_in"]) < 0.02):
            q["n"] += p["n"]
        else:
            merged.append(dict(p))
    return merged


def vfilter(p):
    f = []
    fr = p["frame"]
    flip = False
    if isinstance(fr, dict):                 # b-roll framing: zoom about a point
        z, cx, cy, flip = fr.get("z", 1.0), fr.get("cx", 0.5), fr.get("cy", 0.5), fr.get("flip", True)
        cw, ch = int(SW / z) // 2 * 2, int(SH / z) // 2 * 2
        x = int(min(max(cx * SW - cw / 2, 0), SW - cw))
        y = int(min(max(cy * SH - ch / 2, 0), SH - ch))
    else:
        z, ay = FRAMES[fr]
        cw, ch = int(SW / z) // 2 * 2, int(SH / z) // 2 * 2
        x = (SW - cw) // 2
        y = int((SH - ch) * ay)
    f.append("setpts=(PTS-STARTPTS)/%.6f" % p["speed"])
    f.append("fps=%d" % FPS)
    f.append("crop=%d:%d:%d:%d" % (cw, ch, x, y))
    if flip:
        f.append("hflip")
    f.append("scale=%d:%d:flags=lanczos" % (OW, OH))
    if p.get("bw"):
        f.append("hue=s=0,eq=contrast=1.12:brightness=-0.02")
    f.append("format=yuv420p")
    return ",".join(f)


def enc_piece(p, path):
    pre = max(0.0, p["src_in"] - 0.0)
    cmd = ["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", "%.4f" % pre, "-i", SRC[p["src"]],
           "-an", "-vf", vfilter(p), "-frames:v", str(p["n"]),
           "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p",
           "-r", str(FPS), "-video_track_timescale", "15360", path]
    subprocess.run(cmd, check=True)
    got = subprocess.run(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v",
                          "-show_entries", "stream=nb_read_packets", "-of", "csv=p=0", path],
                         capture_output=True, text=True).stdout.strip()
    if int(got) != p["n"]:
        # the source ran out (end of file): pad with the last frame
        tmp = path + ".pad.mp4"
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", path, "-vf",
                        "tpad=stop_mode=clone:stop=%d" % (p["n"] - int(got)), "-frames:v", str(p["n"]),
                        "-c:v", "libx264", "-preset", "fast", "-crf", "17", "-pix_fmt", "yuv420p",
                        "-r", str(FPS), "-video_track_timescale", "15360", tmp], check=True)
        os.replace(tmp, path)


def audio_of(src):
    os.makedirs(SCR, exist_ok=True)
    w = os.path.join(SCR, "a48_%s.wav" % src)
    if not os.path.exists(w):
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", SRC[src], "-vn", "-ac", "2",
                        "-ar", str(SR), "-c:a", "pcm_s16le", w], check=True)
    with wave.open(w) as f:
        a = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).reshape(-1, 2)
    return a.astype(np.float32)


def stretch(seg, speed):
    """pitch-safe speed-up through ffmpeg atempo (the fast-forward stays a voice)"""
    os.makedirs(SCR, exist_ok=True)
    i, o = os.path.join(SCR, "st_in.wav"), os.path.join(SCR, "st_out.wav")
    with wave.open(i, "w") as f:
        f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR)
        f.writeframes(np.clip(seg, -32768, 32767).astype(np.int16).tobytes())
    chain, s = [], speed
    while s > 2.0:
        chain.append("atempo=2.0"); s /= 2.0
    chain.append("atempo=%.5f" % s)
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", i, "-af", ",".join(chain), o], check=True)
    with wave.open(o) as f:
        return np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).reshape(-1, 2).astype(np.float32)


def build_audio(spans, path):
    cache = {}
    fade = int(0.010 * SR)
    parts = []
    for sp in spans:
        if sp["src"] not in cache:
            cache[sp["src"]] = audio_of(sp["src"])
        a = cache[sp["src"]]
        n = int(round(sp["frames"] / FPS * SR))
        a0 = int(round(sp["a"] * SR))
        if sp["speed"] != 1.0:
            raw = a[a0:int(round(sp["b"] * SR))].copy()
            seg = stretch(raw, sp["speed"])
        else:
            seg = a[a0:a0 + n].copy()
        if len(seg) < n:
            seg = np.vstack([seg, np.zeros((n - len(seg), 2), np.float32)])
        seg = seg[:n] * (10 ** (sp["gain"] / 20.0))
        ramp = np.linspace(0, 1, fade)[:, None]
        seg[:fade] *= ramp
        seg[-fade:] *= ramp[::-1]
        parts.append(seg)
    vo = np.vstack(parts)
    with wave.open(path, "w") as f:
        f.setnchannels(2); f.setsampwidth(2); f.setframerate(SR)
        f.writeframes(np.clip(vo, -32768, 32767).astype(np.int16).tobytes())


def main():
    spans, rolls, total = plan()
    ps = pieces(spans, rolls)
    for p in ps:
        p.pop("segs", None)
    tl = {"fps": FPS, "frames": total, "duration": round(total / FPS, 3),
          "spans": spans, "broll": rolls}
    json.dump(tl, open(os.path.join(HERE, "timeline.json"), "w", encoding="utf-8"), indent=1)
    print("spans %d  b-roll %d  pieces %d  -> %d frames = %.2f s"
          % (len(spans), len(rolls), len(ps), total, total / FPS))
    if "--render" not in sys.argv:
        return
    os.makedirs(SCR, exist_ok=True)
    only = None
    if "--only" in sys.argv:
        only = set(int(x) for x in sys.argv[sys.argv.index("--only") + 1].split(","))
    lst, todo = [], []
    for j, p in enumerate(ps):
        path = os.path.join(SCR, "p%04d.mp4" % j)
        lst.append(path)
        sig = json.dumps({k: p[k] for k in ("kind", "src", "src_in", "n", "speed", "frame", "bw")}, sort_keys=True)
        sigp = path + ".sig"
        if os.path.exists(path) and os.path.exists(sigp) and open(sigp).read() == sig and (only is None or j not in only):
            continue
        todo.append((p, path, sig, sigp))

    def run(job):
        p, path, sig, sigp = job
        enc_piece(p, path)
        open(sigp, "w").write(sig)
        print("piece %s" % os.path.basename(path), flush=True)
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(3) as ex:
        list(ex.map(run, todo))
    cat = os.path.join(SCR, "concat.txt")
    with open(cat, "w") as f:
        for p in lst:
            f.write("file '%s'\n" % p)
    vcat = os.path.join(SCR, "video.mp4")
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", cat,
                    "-c", "copy", vcat], check=True)
    wav = os.path.join(SCR, "voice.wav")
    build_audio(spans, wav)
    out = os.path.join(ROOT, "reel-41", "assets", "voice.mp4")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", vcat, "-i", wav, "-map", "0:v", "-map", "1:a",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out], check=True)
    fr = subprocess.run(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v",
                         "-show_entries", "stream=nb_read_packets", "-of", "csv=p=0", out],
                        capture_output=True, text=True).stdout.strip()
    print("PLATE FRAMES %s (planned %d)  DUR = %.3f" % (fr, total, (int(fr) - 0.5) / FPS))


if __name__ == "__main__":
    main()
