# -*- coding: utf-8 -*-
"""The double check she asked for (2026-10-21: "i was tired so i did some
mistakes ... cut it out + doublecheck in the end"). Listens to the CUT plate,
not the raw take, so it catches what the cutter itself introduced — REEL-31
shipped a doubled «в» at a join.

    python work/b1021/joincheck.py 41 [42 ...]

Per reel: whisper on the whole plate (cached in work/rNN/plate-words.json),
then whisper again on a 4 s window around every real join (content removed
there), and flags
  DOUBLE   the same word twice in a row (or a half-word then the word) at a join
  REPEAT   a 2+ word run said twice within 6 s that the script says once
  EXTRA    plate words the script does not have, next to a join (a fumble left in)
  MISSING  3+ consecutive script words the plate does not have (a cut ate a line)
Writes work/rNN/joincheck.txt; prints one line per reel.
"""
import difflib
import json
import os
import subprocess
import sys
import wave

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from cut import norm, tokens  # noqa: E402

_m = None


def model():
    global _m
    if _m is None:
        from faster_whisper import WhisperModel
        _m = WhisperModel("medium", device="cpu", compute_type="int8", cpu_threads=4)
    return _m


def asr(x, off=0.0):
    segs, _ = model().transcribe(x, language="uk", word_timestamps=True, condition_on_previous_text=False,
                                 beam_size=5, vad_filter=False)
    return [{"w": w.word.strip(), "s": round(off + w.start, 3), "e": round(off + w.end, 3)}
            for s in segs for w in (s.words or [])]


def pcm16(path):
    wav = path + ".a16.wav"
    if not os.path.exists(wav) or os.path.getmtime(wav) < os.path.getmtime(path):
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", path, "-vn", "-ac", "1", "-ar", "16000",
                        wav], check=True)
    with wave.open(wav) as f:
        return np.frombuffer(f.readframes(f.getnframes()), np.int16).astype(np.float32) / 32768.0


def ntoks(ws):
    out = []
    for w in ws:
        for t in tokens(w["w"]):
            n = norm(t)
            if n:
                out.append((n, w))
    return out


def doubled(seq, lo, hi):
    """same word twice in a row, or a fragment followed by the word it starts"""
    hits = []
    for (a, wa), (b, wb) in zip(seq, seq[1:]):
        if not (lo <= wb["s"] <= hi or lo <= wa["e"] <= hi):
            continue
        if a == b or (len(a) >= 2 and len(b) > len(a) + 1 and b.startswith(a)):
            hits.append("%s %s @%.2f" % (wa["w"], wb["w"], wb["s"]))
    return hits


def check(nn):
    wd = os.path.join(ROOT, "work", "r" + nn)
    plate = os.path.join(ROOT, "reel-" + nn, "assets", "voice.mp4")
    cut = json.load(open(os.path.join(wd, "cut.json"), encoding="utf-8"))
    script = [norm(t) for t in tokens(open(os.path.join(wd, "script.txt"), encoding="utf-8").read())]
    script = [t for t in script if t]
    x = pcm16(plate)
    cache = os.path.join(wd, "plate-words.json")
    stamp = os.path.getmtime(plate)
    words = None
    if os.path.exists(cache):
        c = json.load(open(cache, encoding="utf-8"))
        if c.get("stamp") == stamp:
            words = c["words"]
    if words is None:
        words = asr(x)
        json.dump({"stamp": stamp, "words": words}, open(cache, "w", encoding="utf-8"), ensure_ascii=False, indent=0)

    clips = cut["clips"]
    joins = []
    for p, c in zip(clips, clips[1:]):
        if abs(p["src_in"] + p["dur"] - c["src_in"]) > 0.02:
            joins.append(c["tl"])

    seq = ntoks(words)
    report, flags = [], 0
    # DOUBLE, from the whole-plate pass and from a solo pass around each join
    for t in joins:
        a = max(0.0, t - 2.0)
        b = min(len(x) / 16000.0, t + 2.0)
        solo = ntoks(asr(x[int(a * 16000):int(b * 16000)], a))
        hits = sorted(set(doubled(seq, t - 0.9, t + 0.9) + doubled(solo, t - 0.9, t + 0.9)))
        ctx = " ".join(w["w"] for w in words if t - 2.0 <= w["s"] <= t + 2.0)
        if hits:
            flags += 1
            report.append("DOUBLE  join %6.2f  %s   | %s" % (t, "; ".join(hits), ctx))
    # REPEAT: a 2-3 word run said twice within 6 s, more often than the script has it
    sc = " ".join(script)
    for n in (3, 2):
        for i in range(len(seq) - n):
            run = [s[0] for s in seq[i:i + n]]
            if sum(len(r) for r in run) < 6:
                continue
            for j in range(i + n, len(seq) - n + 1):
                if seq[j][1]["s"] - seq[i][1]["s"] > 6.0:
                    break
                if [s[0] for s in seq[j:j + n]] == run and sc.count(" ".join(run)) < 2:
                    flags += 1
                    report.append("REPEAT  %6.2f / %6.2f  «%s»" % (seq[i][1]["s"], seq[j][1]["s"],
                                                                   " ".join(s[1]["w"] for s in seq[i:i + n])))
                    break
    # EXTRA near joins / MISSING script runs
    said = [s[0] for s in seq]
    sm = difflib.SequenceMatcher(None, script, said, autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op in ("insert", "replace") and j2 > j1:
            ws = [seq[k][1] for k in range(j1, j2)]
            near = [t for t in joins if ws[0]["s"] - 0.8 <= t <= ws[-1]["e"] + 0.8]
            if near and op == "insert":
                report.append("EXTRA   %6.2f  «%s»  (join %.2f)%s" % (ws[0]["s"], " ".join(w["w"] for w in ws),
                                                                   near[0], "" if j2 - j1 < 6 else "  [improvised?]"))
        if op in ("delete", "replace") and i2 - i1 >= 3 and (op == "delete" or (i2 - i1) - (j2 - j1) >= 3):
            at = seq[j1][1]["s"] if j1 < len(seq) else cut["duration"]
            report.append("MISSING %6.2f  «%s»" % (at, " ".join(script[i1:i2])))
    with open(os.path.join(wd, "joincheck.txt"), "w", encoding="utf-8") as f:
        f.write("plate %.2fs, %d joins, %d words heard\n" % (cut["duration"], len(joins), len(words)))
        f.write("\n".join(report) + "\n")
        f.write("\nPLATE TRANSCRIPT\n" + " ".join(w["w"] for w in words) + "\n")
    print("r%s: %d joins, %d DOUBLE/REPEAT flags, %d EXTRA, %d MISSING"
          % (nn, len(joins), flags, sum(r.startswith("EXTRA") for r in report),
             sum(r.startswith("MISSING") for r in report)), flush=True)


if __name__ == "__main__":
    for nn in sys.argv[1:]:
        check(nn)
