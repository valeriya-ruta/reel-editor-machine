# -*- coding: utf-8 -*-
"""Cut a long horizontal take (course / YouTube video) into a 16:9 plate.

    python tools/cutlong.py work/udc-tutorial            # plan -> cut.json, cut.txt, words.json
    python tools/cutlong.py work/udc-tutorial --render   # plate -> work/udc-tutorial/plate.mp4

tools/cut.py is built for her vertical reels: a script to align against, a 9:16
crop of a rotated phone file. A long tutorial has no script, so here the
retakes are marked by hand in `cut-fix.json` from the transcript (`drop`: raw
seconds), and the rest is mechanical:

- every pause between two kept words longer than GAP_MAX shrinks to GAP_MAX
  (SENT_GAP after a full stop) — the cut sits in the quietest part of the gap;
- a cut that removed real content changes the framing (100 % <-> 108 %), so a
  jump reads as an edit, never as a glitch (her rule from the reels: pure scale
  steps, centred, nothing slides);
- a clip held longer than SPLIT_OVER gets a framing change at a sentence end.

Inputs in the work dir: SOURCE.txt (raw file), segs.jsonl (faster-whisper with
word timings, tools-less: see asr_fw.py there), cut-fix.json.
"""
import json
import os
import re
import subprocess
import sys
import wave

import numpy as np

FPS = 30
OUT_W, OUT_H = 1920, 1080
FRAMES = {"base": 1.00, "in": 1.08}
GAP_MAX = 0.28           # a pause inside a thought
SENT_GAP = 0.42          # after a full stop / question
PAD_IN, PAD_OUT = 0.08, 0.14
SPLIT_OVER = 14.0
QUIET_MAX = 0.55         # a silence inside a clip longer than this ...
QUIET_KEEP = 0.26        # ... shrinks to this


def load(wd):
    segs = [json.loads(l) for l in open(os.path.join(wd, "segs.jsonl"), encoding="utf-8")]
    # Over a long segment whisper swallows repeated attempts, so the fumbles
    # she flagged were re-heard burst by burst (work dir burst_asr.py). Inside
    # those windows the burst words replace the long-pass words.
    bp = os.path.join(wd, "bursts.json")
    if os.path.exists(bp):
        for key, bursts in json.load(open(bp, encoding="utf-8")).items():
            a, b = (float(x) for x in key.split(","))
            for sg in segs:
                sg["words"] = [w for w in sg["words"] if not (a <= w["s"] < b)]
            segs.extend(bursts)
        segs.sort(key=lambda sg: sg["a"])
    W = []
    for si, s in enumerate(segs):
        for x in s["words"]:
            if x["w"].strip():
                W.append(dict(x, seg=si))
    return segs, W


def envelope(wav, hop=0.01):
    with wave.open(wav) as f:
        sr, n = f.getframerate(), f.getnframes()
        a = np.frombuffer(f.readframes(n), np.int16).astype(np.float32)
    h = int(sr * hop)
    m = len(a) // h
    return np.sqrt((a[: m * h].reshape(m, h) ** 2).mean(axis=1) + 1e-9), hop


def quietest(env, hop, lo, hi):
    a, b = max(0, int(lo / hop)), min(len(env) - 1, int(hi / hop))
    if b <= a:
        return (lo + hi) / 2
    return (a + int(np.argmin(env[a:b + 1]))) * hop + hop / 2


def plan(wd):
    segs, W = load(wd)
    fix = json.load(open(os.path.join(wd, "cut-fix.json"), encoding="utf-8"))
    drops = [tuple(d[:2]) for d in fix.get("drop", [])]
    end_at = fix.get("end")
    start_at = fix.get("start", 0.0)

    def dropped(w):
        mid = (w["s"] + w["e"]) / 2
        return any(a <= mid <= b for a, b in drops) or mid < start_at or (end_at and mid > end_at)

    kept = [w for w in W if not dropped(w)]
    env, hop = envelope(os.path.join(wd, "audio.wav"))

    # runs of kept words; a new run wherever content was removed or a pause is long
    runs, cur = [], []
    for i, w in enumerate(kept):
        if cur:
            prev = cur[-1]
            removed = any(prev["e"] - 0.01 <= x["s"] and x["e"] <= w["s"] + 0.01
                          for x in W if dropped(x))
            gap = w["s"] - prev["e"]
            limit = SENT_GAP if re.search(r"[.?!…]$", prev["w"]) else GAP_MAX
            if removed or gap > limit + 0.12:
                runs.append((cur, removed))
                cur = []
        cur.append(w)
    if cur:
        runs.append((cur, False))

    clips = []
    for ri, (ws, removed_after) in enumerate(runs):
        a = quietest(env, hop, ws[0]["s"] - 0.25, ws[0]["s"] - 0.02) - 0.03
        a = max(a, ws[0]["s"] - PAD_IN - 0.2, 0.0)
        tail = SENT_GAP if re.search(r"[.?!…]$", ws[-1]["w"]) else GAP_MAX
        b = quietest(env, hop, ws[-1]["e"] + 0.02, ws[-1]["e"] + tail) + 0.03
        clips.append({"a": round(a, 3), "b": round(b, 3), "real": removed_after or True,
                      "text": " ".join(x["w"] for x in ws), "words": ws})
    # mark which joins removed content (framing changes there) vs only a pause
    for i in range(len(clips) - 1):
        clips[i]["content_cut"] = runs[i][1]

    # split long clips at a sentence end, for a framing change
    out = []
    for c in clips:
        todo = [c]
        while todo:
            x = todo.pop(0)
            if x["b"] - x["a"] <= SPLIT_OVER:
                out.append(x)
                continue
            mid = (x["a"] + x["b"]) / 2
            cands = [(w0, w1) for w0, w1 in zip(x["words"], x["words"][1:])
                     if re.search(r"[.?!,]$", w0["w"]) and w0["e"] - x["a"] > 4 and x["b"] - w1["s"] > 4]
            if not cands:
                out.append(x)
                continue
            w0, w1 = min(cands, key=lambda p: abs(p[0]["e"] - mid) - (3 if p[0]["w"][-1] in ".?!" else 0))
            cut = round(quietest(env, hop, w0["e"], w1["s"]), 3)
            i = x["words"].index(w1)
            first = dict(x, b=cut, words=x["words"][:i], content_cut=False)
            second = dict(x, a=cut, words=x["words"][i:])
            first["text"] = " ".join(w["w"] for w in first["words"])
            second["text"] = " ".join(w["w"] for w in second["words"])
            todo[0:0] = [first, second]

    out = desilence(out, env, hop)

    # framing: alternate on every join; output timeline
    t, name = 0.0, "base"
    res = []
    for i, c in enumerate(out):
        # a sliver left by a silence cut keeps the framing: two zoom flips
        # inside a second read as a glitch, not an edit
        if i and (c["b"] - c["a"]) >= 1.0 and (out[i - 1]["b"] - out[i - 1]["a"]) >= 1.0:
            name = "in" if name == "base" else "base"
        n = max(1, int(round((c["b"] - c["a"]) * FPS)))
        res.append({"i": i, "src_in": c["a"], "frames": n, "dur": round(n / FPS, 4), "tl": round(t, 4),
                    "frame": name, "text": c["text"]})
        c["tl"] = t
        t += n / FPS
    # words on the output timeline
    words = []
    for c, r in zip(out, res):
        for w in c["words"]:
            words.append({"w": w["w"], "s": round(r["tl"] + max(w["s"], c["a"]) - c["a"], 3),
                          "e": round(r["tl"] + min(w["e"], c["a"] + r["dur"]) - c["a"], 3), "raw": w["s"]})
    return res, round(t, 4), words


def desilence(clips, env, hop):
    """Whisper stretches a word over a pause, so a gap between word timings is
    not the only dead air: her "awkward pause" notes (7:40, 12:25) sat inside
    single words. Any quiet stretch longer than QUIET_MAX inside a clip is cut
    down to QUIET_KEEP, judged on the audio itself."""
    thr = max(0.012, float(np.percentile(env, 30)) * 2.5)
    out = []
    for c in clips:
        i0, i1 = int(c["a"] / hop), int(c["b"] / hop)
        quiet, k = [], i0
        while k < i1:
            if env[k] < thr:
                j = k
                while j < i1 and env[j] < thr:
                    j += 1
                if (j - k) * hop >= QUIET_MAX and k > i0 and j < i1:
                    quiet.append((k * hop + QUIET_KEEP * 0.45, j * hop - QUIET_KEEP * 0.55))
                k = j
            else:
                k += 1
        if not quiet:
            out.append(c)
            continue
        edges = [c["a"]]
        for qa, qb in quiet:
            edges += [round(qa, 3), round(qb, 3)]
        edges.append(c["b"])
        pieces = [(edges[i], edges[i + 1]) for i in range(0, len(edges), 2)]
        # every word goes to the piece nearest its middle — a word whisper
        # stretched across the removed silence must not vanish from the subtitles
        groups = [[] for _ in pieces]
        for w in c["words"]:
            mid = (w["s"] + w["e"]) / 2
            k = min(range(len(pieces)), key=lambda q: 0 if pieces[q][0] <= mid < pieces[q][1]
                    else min(abs(mid - pieces[q][0]), abs(mid - pieces[q][1])))
            groups[k].append(w)
        for (pa, pb), ws in zip(pieces, groups):
            out.append(dict(c, a=pa, b=pb, words=ws, text=" ".join(w["w"] for w in ws)))
    return out


def crop(name):
    z = FRAMES[name]
    sw, sh = 3840, 2160
    cw, ch = int(sw / z) // 2 * 2, int(sh / z) // 2 * 2
    x, y = (sw - cw) // 2, (sh - ch) // 2
    y = max(0, y - int(ch * 0.02)) if z > 1 else 0      # keep her headroom when pushed in
    return "crop=%d:%d:%d:%d,scale=%d:%d:flags=lanczos" % (cw, ch, x, y, OUT_W, OUT_H)


def render(wd, clips, total):
    src = open(os.path.join(wd, "SOURCE.txt")).read().strip()
    segdir = os.path.join(wd, "segs")
    os.makedirs(segdir, exist_ok=True)
    lst = []
    for c in clips:
        p = os.path.join(segdir, "c_%.3f_%d_%s.mp4" % (c["src_in"], c["frames"], c["frame"]))
        lst.append(p)
        if os.path.exists(p):
            continue
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", "%.4f" % c["src_in"], "-i", src, "-an",
                        "-vf", crop(c["frame"]) + ",fps=30", "-frames:v", str(c["frames"]), "-c:v", "libx264",
                        "-crf", "17", "-preset", "fast", "-pix_fmt", "yuv420p", "-r", "30", p + ".tmp.mp4"],
                       check=True)
        os.replace(p + ".tmp.mp4", p)
        print("clip %d/%d" % (c["i"] + 1, len(clips)), flush=True)
    with open(os.path.join(segdir, "list.txt"), "w") as f:
        for p in lst:
            f.write("file '%s'\n" % os.path.abspath(p))
    vcat = os.path.join(wd, "video.mp4")
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i",
                    os.path.join(segdir, "list.txt"), "-c", "copy", vcat], check=True)
    # audio: the same spans from a 48 kHz stereo pull, 8 ms fades at every join
    wav48 = os.path.join(wd, "full48.wav")
    if not os.path.exists(wav48):
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", src, "-vn", "-ac", "2", "-ar", "48000",
                        "-c:a", "pcm_s16le", wav48], check=True)
    with wave.open(wav48) as f:
        sr = f.getframerate()
        a = np.frombuffer(f.readframes(f.getnframes()), np.int16).reshape(-1, 2).astype(np.float32)
    fade = int(0.008 * sr)
    parts = []
    for c in clips:
        a0 = int(round(c["src_in"] * sr))
        n = int(round(c["frames"] / FPS * sr))
        seg = a[a0:a0 + n].copy()
        if len(seg) < n:
            seg = np.vstack([seg, np.zeros((n - len(seg), 2), np.float32)])
        r = np.linspace(0, 1, fade)[:, None]
        seg[:fade] *= r
        seg[-fade:] *= r[::-1]
        parts.append(seg)
    audio = np.vstack(parts)
    awav = os.path.join(wd, "plate_audio.wav")
    with wave.open(awav, "w") as f:
        f.setnchannels(2); f.setsampwidth(2); f.setframerate(sr)
        f.writeframes(np.clip(audio, -32768, 32767).astype(np.int16).tobytes())
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", vcat, "-i", awav, "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-shortest", os.path.join(wd, "plate.mp4")], check=True)


def main():
    wd = sys.argv[1]
    clips, total, words = plan(wd)
    json.dump({"duration": total, "clips": clips}, open(os.path.join(wd, "cut.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    json.dump(words, open(os.path.join(wd, "words.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    with open(os.path.join(wd, "cut.txt"), "w", encoding="utf-8") as f:
        f.write("plate %.2fs, %d clips\n\n" % (total, len(clips)))
        for c in clips:
            f.write("%7.2f  src %7.2f  %5.2fs  %-4s %s\n" % (c["tl"], c["src_in"], c["dur"], c["frame"], c["text"]))
    print("plan: %d clips, %.1fs" % (len(clips), total))
    if "--render" in sys.argv:
        render(wd, clips, total)


if __name__ == "__main__":
    main()
