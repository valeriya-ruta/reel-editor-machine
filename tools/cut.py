# -*- coding: utf-8 -*-
"""Cut her raw take into a plate: drop the silences and the fumbled takes,
give every clip its own framing, punch in on the jokes.

    python tools/cut.py 21            # plan  -> work/r21/cut.json + cut.txt
    python tools/cut.py 21 --render   # plate -> reel-21/assets/voice.mp4

Inputs, all in work/rNN/: SOURCE.txt (the raw file), utt.jsonl (one whisper
pass per utterance, from work/b1005/utt_batch.py), script.txt (her words from
the app), optional cut-fix.json (manual drops / keeps / punches).

**Last take wins** (her rule, 2026-10-05): when she fumbles a line and says it
again, every earlier attempt goes, however many there were. Each ASR word is
aligned to the script with a Viterbi pass that may jump *back* in the script;
a backward jump is a restart, and everything from the first earlier attempt at
that script position onward is dropped.

Framing follows tools/cutcam.py: never the same crop twice across a cut, small
steps, centred on her face. `punch` is the closeup for a joke or a punchline;
those spans go to the build's NO_PAINT list (STYLE.md §4a — her closeups are
comedy, and now I am the one making them).
"""
import difflib
import json
import os
import re
import subprocess
import sys
import wave

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRATCH = os.environ.get("CUT_SCRATCH", "E:/reels-work")   # heavy intermediates off C:
FPS = 30
SRC_W, SRC_H = 2160, 3840          # her phone files are 3840x2160 rotated -90
OUT_W, OUT_H = 1080, 1920

# zoom, and how far the crop moves toward her face (0 = frame centre, 1 = face centre).
# Her note, 2026-10-05: "the cuts are a bit jumpy … i keep moving a bit left and
# right instead of it being a pure pull in pull out (100 > 110 > 100 but XY stay
# 0)". So every framing is centred: the cut is a pure scale step, nothing slides.
FRAMES = {
    "base":  (1.00, 0.0),
    "in":    (1.10, 0.0),
    "punch": (1.50, 0.0),          # the closeup — comedy, so properly close
}
CYCLE = ["base", "in"]

PAD_IN, PAD_OUT = 0.07, 0.10       # around a kept utterance
GAP_KEEP = 0.16                    # a removed silence still leaves this much air
SENT_GAP = 0.30                    # ... and this much after a full stop
SPLIT_OVER = 5.5                   # clips longer than this get a zoom cut inside
MAX_DROP_WORDS = 40                # a restart that would drop more is flagged, not cut

# ---------------------------------------------------------------- alignment

_LAT = [("sh", "ш"), ("ch", "ч"), ("th", "т"), ("ee", "і"), ("oo", "у"), ("ph", "ф"),
        ("a", "а"), ("b", "б"), ("c", "к"), ("d", "д"), ("e", "е"), ("f", "ф"), ("g", "г"),
        ("h", "х"), ("i", "і"), ("j", "дж"), ("k", "к"), ("l", "л"), ("m", "м"), ("n", "н"),
        ("o", "о"), ("p", "п"), ("q", "к"), ("r", "р"), ("s", "с"), ("t", "т"), ("u", "у"),
        ("v", "в"), ("w", "в"), ("x", "кс"), ("y", "і"), ("z", "з")]
_FOLD = str.maketrans({"ї": "і", "й": "и", "є": "е", "ґ": "г", "ё": "е", "ы": "и",
                       "э": "е", "ъ": "", "ь": "", "'": "", "’": "", "ʼ": "", "и": "і"})
_SPOKEN = {"claude": "клод", "chatgpt": "чатджіпіті", "gpt": "джіпіті", "ai": "еі",
           "obs": "обс", "youtube": "ютуб", "notion": "ноушн", "threads": "тредс",
           "windsor": "віндзор", "clarity": "кларіті", "google": "гугл", "edits": "едітс",
           "analytics": "аналітікс", "microsoft": "майкрософт", "webinar": "вебінар",
           "stars": "старс", "way4pay": "вейфорпей", "figma": "фігма", "agi": "аджіай"}


def norm(w):
    w = w.lower()
    w = re.sub(r"[^\w']+", "", w)
    if w in _SPOKEN:
        w = _SPOKEN[w]
    if re.search(r"[a-z]", w):
        for a, b in _LAT:
            w = w.replace(a, b)
    return w.translate(_FOLD)


def tokens(text):
    out = []
    for raw in re.findall(r"[\w'’ʼ\-]+|\d+", text):
        for part in raw.split("-"):
            if part.strip("'’ʼ"):
                out.append(part)
    return out


def sim(a, b):
    if not a or not b:
        return 0.0
    if a == b:
        return 1.0
    return difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()


def emit(a, b):
    s = sim(a, b)
    # short words match anything a bit; make them earn it
    if min(len(a), len(b)) <= 2 and s < 1.0:
        s *= 0.6
    return 1.6 * (1.0 - s)


INS = 1.0          # an ASR word that is not in the script
SKIP = 0.45        # per script word she did not say
JUMP_F = 3.0       # cap on a long forward skip
BACK_NEAR = 0.8    # restart a few words back
BACK_FAR = 2.4     # restart from far back
BACK_PAUSE = 0.55  # restart right after a pause — the usual fumble


def viterbi(words, script, boundary):
    """words: normalised ASR words; script: normalised script words;
    boundary[i]: True if a pause precedes ASR word i.
    Returns (match index or None, kind) per ASR word; kind in m/r/i."""
    M = len(script)
    INF = 1e9
    prev = [INF] * (M + 1)
    prev[0] = 0.0
    back = []
    for i, w in enumerate(words):
        cur = [INF] * (M + 1)
        bp = [None] * (M + 1)
        # forward source for matching script word j: best prev[p], p <= j
        lin_v, lin_p = INF, None
        pre_v, pre_p = INF, None
        fwd = [None] * M
        for j in range(M):
            if prev[j] + 0 < lin_v + SKIP:
                lin_v, lin_p = prev[j], j
            else:
                lin_v += SKIP
            if prev[j] < pre_v:
                pre_v, pre_p = prev[j], j
            fwd[j] = (lin_v, lin_p) if lin_v <= pre_v + JUMP_F else (pre_v + JUMP_F, pre_p)
        # backward source: best prev[p], p > j+1 (restart)
        suf = [None] * (M + 1)
        sv, sp = INF, None
        for p in range(M, 0, -1):
            if prev[p] < sv:
                sv, sp = prev[p], p
            suf[p - 1] = (sv, sp)
        for j in range(M):
            e = emit(w, script[j])
            v, p = fwd[j]
            kind = "m"
            sb_v, sb_p = suf[j] if suf[j] else (INF, None)
            if sb_p is not None:
                dist = sb_p - (j + 1)
                pen = BACK_PAUSE if boundary[i] else (BACK_NEAR if dist <= 8 else BACK_FAR)
                if sb_v + pen < v:
                    v, p, kind = sb_v + pen, sb_p, "r"
            if v + e < cur[j + 1]:
                cur[j + 1] = v + e
                bp[j + 1] = (p, kind, j)
        for p in range(M + 1):
            if prev[p] + INS < cur[p]:
                cur[p] = prev[p] + INS
                bp[p] = (p, "i", None)
        back.append(bp)
        prev = cur
    # backtrace
    p = min(range(M + 1), key=lambda q: prev[q])
    out = []
    for i in range(len(words) - 1, -1, -1):
        src, kind, j = back[i][p]
        out.append((j, kind))
        p = src
    return out[::-1]


def plan_takes(utts, script_text, fix):
    script = [norm(t) for t in tokens(script_text)]
    W = []
    for u in utts:
        for n, x in enumerate(u["words"]):
            W.append(dict(x, k=u["k"], first=(n == 0), n=norm(x["w"])))
    W = [w for w in W if w["n"]]
    path = viterbi([w["n"] for w in W], script, [w["first"] for w in W])
    for w, (j, kind) in zip(W, path):
        w["j"], w["kind"] = j, kind

    # "keep" spans (raw seconds) are lines she added on purpose: they never
    # trigger a restart and are never dropped by one
    keep = [tuple(x) for x in fix.get("keep", [])]

    def held(x):
        return any(a - 0.05 <= x["s"] and x["e"] <= b + 0.05 for a, b in keep)

    kept, dropped, flags = [], [], []
    for idx, w in enumerate(W):
        if w["kind"] == "r" and not held(w):
            cut_at = next((q for q, kw in enumerate(kept)
                           if kw["j"] is not None and kw["j"] >= w["j"]), None)
            if cut_at is not None:
                gone = kept[cut_at:]
                if len(gone) > MAX_DROP_WORDS:
                    flags.append("restart at %.2fs would drop %d words (%.2f-%.2f) — kept, CHECK"
                                 % (w["s"], len(gone), gone[0]["s"], gone[-1]["e"]))
                else:
                    # the new take's own lead-in (words of this utterance said
                    # before the restart point) belongs to the take that wins
                    lead = [x for x in gone if x["k"] == w["k"] or held(x)]
                    gone = [x for x in gone if not (x["k"] == w["k"] or held(x))]
                    if gone:
                        dropped.append(gone)
                    kept = kept[:cut_at] + lead
        kept.append(w)
    # manual drops / keeps (seconds in the raw file)
    for a, b in fix.get("drop", []):
        kept = [w for w in kept if not (w["s"] >= a - 0.05 and w["e"] <= b + 0.05)]
    return W, kept, dropped, flags, script


# ---------------------------------------------------------------- audio helpers

def read_wav(path):
    with wave.open(path) as f:
        sr, ch, n = f.getframerate(), f.getnchannels(), f.getnframes()
        a = np.frombuffer(f.readframes(n), dtype=np.int16).reshape(-1, ch).astype(np.float32)
    return sr, a


def envelope(a, sr, hop=0.01):
    mono = a.mean(axis=1)
    h = int(sr * hop)
    n = len(mono) // h
    return np.sqrt((mono[: n * h].reshape(n, h) ** 2).mean(axis=1) + 1e-9), hop


def quietest(env, hop, lo, hi):
    a, b = max(0, int(lo / hop)), min(len(env) - 1, int(hi / hop))
    if b <= a:
        return (lo + hi) / 2
    return (a + int(np.argmin(env[a:b + 1]))) * hop + hop / 2


# ---------------------------------------------------------------- segments

def word_est(w):
    """How long she takes to say a word, roughly: her read is ~6 letters/s
    plus an attack. Generous on purpose — this only trims what is clearly not
    the word."""
    n = len(re.sub(r"[^\w]", "", w))
    return 0.14 + 0.075 * n


def build_segments(utts, kept, env, hop, punch_words):
    by_k = {u["k"]: u for u in utts}
    utt_words = {}
    for u in utts:
        utt_words[u["k"]] = [x for x in u["words"] if norm(x["w"])]
    keep_ids = {(w["k"], w["s"], w["e"]) for w in kept}

    # runs of consecutive kept words inside one utterance
    runs = []
    for u in utts:
        ws = utt_words[u["k"]]
        cur = []
        for x in ws:
            if (u["k"], x["s"], x["e"]) in keep_ids:
                cur.append(x)
            elif cur:
                runs.append((u["k"], cur)); cur = []
        if cur:
            runs.append((u["k"], cur))

    segs = []
    for k, ws in runs:
        u = by_k[k]
        allw = utt_words[k]
        whole_start = ws[0] is allw[0]
        whole_end = ws[-1] is allw[-1]
        if whole_start:
            a = max(0.0, u["a"] - PAD_IN)
            # Whisper stretches the first word over whatever came before it —
            # her stepping back, a hand on the mic (her notes on reel 21, 0:09
            # and 0:19). Noise is not silence, so silencedetect lets it in.
            # Start on the word itself.
            w0 = ws[0]
            est = word_est(w0["w"])
            if w0["e"] - w0["s"] > est + 0.22:
                onset = w0["e"] - est
                a = max(a, quietest(env, hop, onset - 0.14, onset + 0.02) - 0.03)
        else:
            a = quietest(env, hop, ws[0]["s"] - 0.16, ws[0]["s"] + 0.02) - 0.02
        if whole_end:
            b = u["b"] + PAD_OUT + (SENT_GAP - GAP_KEEP if re.search(r"[.?!…]$", ws[-1]["w"]) else 0)
            w1 = ws[-1]
            est = word_est(w1["w"])
            if w1["e"] - w1["s"] > est + 0.30:          # the same, after the last word
                b = min(b, quietest(env, hop, w1["s"] + est, w1["s"] + est + 0.16) + 0.06)
        else:
            b = quietest(env, hop, ws[-1]["e"] - 0.02, ws[-1]["e"] + 0.16) + 0.02
        segs.append({"k": k, "a": a, "b": b, "text": " ".join(x["w"] for x in ws),
                     "mid_in": not whole_start, "mid_out": not whole_end})

    # merge segments that are only a short breath apart; trim long gaps
    out = []
    for s in segs:
        if out and s["a"] - out[-1]["b"] < 0.05:
            out[-1]["b"] = s["b"]; out[-1]["text"] += " " + s["text"]
            out[-1]["mid_out"] = s["mid_out"]
        else:
            out.append(dict(s))
    # a long clip gets a framing change at a sentence or breath boundary even
    # with nothing cut there — one framing held 9 s reads as a static camera
    kept_w = sorted(kept, key=lambda w: w["s"])
    final = []
    todo = list(out)
    while todo:
        s = todo.pop(0)
        if s["b"] - s["a"] <= SPLIT_OVER:
            final.append(s); continue
        ws = [w for w in kept_w if s["a"] <= w["s"] and w["e"] <= s["b"]]
        mid = (s["a"] + s["b"]) / 2
        cands = []
        for w0, w1 in zip(ws, ws[1:]):
            gap = w1["s"] - w0["e"]
            if re.search(r"[.,?!:;—]$", w0["w"]) or gap >= 0.12:
                cut = quietest(env, hop, w0["e"] - 0.02, max(w0["e"] + 0.02, w1["s"] + 0.02))
                if cut - s["a"] >= 2.0 and s["b"] - cut >= 2.0:
                    cands.append(cut)
        if not cands:
            final.append(s); continue
        cut = min(cands, key=lambda c: abs(c - mid))
        first = dict(s, b=cut, mid_out=False)
        second = dict(s, a=cut, mid_in=False, zoomcut=True)
        first["text"] = " ".join(w["w"] for w in ws if w["e"] <= cut + 0.05)
        second["text"] = " ".join(w["w"] for w in ws if w["s"] >= cut - 0.05)
        todo[0:0] = [first, second]
    out = final
    for s in out:
        s["a"] = round(s["a"], 3); s["b"] = round(s["b"], 3)
    return out


def split_for_punch(segs, punch_spans, env, hop):
    """A closeup covers its line, not the whole clip around it: cut the clip at
    the punch span's edges (a zoom cut, nothing removed) so only the line itself
    goes close."""
    out = []
    for s in segs:
        parts = [s]
        for a, b in punch_spans:
            nxt = []
            for p in parts:
                for edge in (a, b):
                    if p["a"] + 0.4 < edge < p["b"] - 0.4:
                        c = round(quietest(env, hop, edge - 0.12, edge + 0.12), 3)
                        nxt_p = dict(p, a=c, mid_in=False)
                        p = dict(p, b=c, mid_out=False)
                        nxt.append(p)
                        p = nxt_p
                nxt.append(p)
            parts = nxt
        out.extend(parts)
    return out


def frame_plan(segs, punch_spans):
    clips, t, ci, last = [], 0.0, 0, None
    for i, s in enumerate(segs):
        n = max(1, int(round((s["b"] - s["a"]) * FPS)))
        dur = n / FPS
        ov = sum(max(0.0, min(s["b"], b) - max(s["a"], a)) for a, b in punch_spans)
        punch = ov >= 0.5 * (s["b"] - s["a"])
        if punch:
            name = "punch"
        else:
            gap = s["a"] - segs[i - 1]["b"] if i else 0.0
            ci += 3 if gap >= 1.8 else 1
            name = CYCLE[ci % len(CYCLE)]
            if name == last:
                ci += 1; name = CYCLE[ci % len(CYCLE)]
        clips.append({"i": i, "src_in": s["a"], "frames": n, "dur": round(dur, 4),
                      "tl": round(t, 4), "frame": name, "text": s["text"]})
        t += dur
        last = name
    return clips, round(t, 4)


def crop_filter(name, face):
    spec = FRAMES[name]
    z, pull = spec[0], spec[1]
    dx = spec[2] if len(spec) > 2 else 0.0
    cw, ch = int(SRC_W / z) // 2 * 2, int(SRC_H / z) // 2 * 2
    fx, fy = face
    cx = 0.5 + (fx - 0.5) * pull + dx
    cy = 0.5 + (fy - 0.5) * pull
    x = int(min(max(cx * SRC_W - cw / 2, 0), SRC_W - cw))
    y = int(min(max(cy * SRC_H - ch / 2, 0), SRC_H - ch))
    return "crop=%d:%d:%d:%d,scale=%d:%d:flags=lanczos" % (cw, ch, x, y, OUT_W, OUT_H)


# ---------------------------------------------------------------- main

def main():
    nn = sys.argv[1]
    render = "--render" in sys.argv
    wd = os.path.join(ROOT, "work", "r" + nn)
    src = open(os.path.join(wd, "SOURCE.txt"), encoding="utf-8").read().strip()
    if os.environ.get("CUT_RAW"):                       # the cloud runner's copy
        src = os.path.join(os.environ["CUT_RAW"], os.path.basename(src))
    utts = [json.loads(l) for l in open(os.path.join(wd, "utt.jsonl"), encoding="utf-8")]
    utts.sort(key=lambda u: u["a"])
    script_text = open(os.path.join(wd, "script.txt"), encoding="utf-8").read()
    fixp = os.path.join(wd, "cut-fix.json")
    fix = json.load(open(fixp, encoding="utf-8")) if os.path.exists(fixp) else {}
    face = tuple(fix.get("face", (0.5, 0.45)))

    scr = os.path.join(SCRATCH, "r" + nn)
    os.makedirs(scr, exist_ok=True)
    wav = os.path.join(scr, "full48.wav")
    if not os.path.exists(wav):
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", src, "-vn",
                        "-ac", "2", "-ar", "48000", "-c:a", "pcm_s16le", wav], check=True)
    sr, audio = read_wav(wav)
    env, hop = envelope(audio, sr)

    W, kept, dropped, flags, script = plan_takes(utts, script_text, fix)
    segs = build_segments(utts, kept, env, hop, None)
    punch_spans = [tuple(p) for p in fix.get("punch", [])]
    segs = split_for_punch(segs, punch_spans, env, hop)
    clips, total = frame_plan(segs, punch_spans)

    if "--dry" in sys.argv:
        old = json.load(open(os.path.join(wd, "cut.json"), encoding="utf-8"))
        ok = {(c["src_in"], c["frames"]) for c in old["clips"]}
        diff = [c for c in clips if (c["src_in"], c["frames"]) not in ok]
        print("dry: %.2fs -> %.2fs, %d clips differ" % (old["duration"], total, len(diff)))
        for c in diff:
            print("   %6.2f src %7.2f %5.2fs %s" % (c["tl"], c["src_in"], c["dur"], c["text"][:50]))
        return

    # kept words on the output timeline -> work/rNN/words.json for tools/align.py
    out_words = []
    for c in clips:
        a, b = c["src_in"], c["src_in"] + c["dur"]
        for w in kept:
            mid = (w["s"] + w["e"]) / 2
            # a word whisper stretched back over a trimmed lead-in still
            # belongs to the clip that holds its end
            if a <= mid < b or (w["s"] < a < w["e"] - 0.12 and w["e"] <= b):
                out_words.append({"w": w["w"],
                                  "s": round(max(0.0, c["tl"] + max(w["s"], a) - a), 3),
                                  "e": round(c["tl"] + min(w["e"], b) - a, 3)})
    out_words.sort(key=lambda w: w["s"])
    json.dump({"text": " ".join(w["w"] for w in out_words), "words": out_words},
              open(os.path.join(wd, "words.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    # NO_PAINT spans on the output timeline: the closeups
    no_paint = [[c["tl"], round(c["tl"] + c["dur"], 3)] for c in clips if c["frame"] == "punch"]
    json.dump({"source": src, "face": face, "duration": total, "clips": clips,
               "no_paint": no_paint, "flags": flags},
              open(os.path.join(wd, "cut.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    # human-readable review: what was dropped, in raw-file seconds
    with open(os.path.join(wd, "cut.txt"), "w", encoding="utf-8") as f:
        f.write("raw %.1fs -> plate %.2fs, %d clips\n" % (len(audio) / sr, total, len(clips)))
        for fl in flags:
            f.write("FLAG " + fl + "\n")
        f.write("\nDROPPED TAKES\n")
        for g in dropped:
            f.write("  %.2f-%.2f  %s\n" % (g[0]["s"], g[-1]["e"], " ".join(x["w"] for x in g)))
        f.write("\nUNMATCHED (kept)\n")
        for w in kept:
            if w["kind"] == "i":
                f.write("  %.2f %s\n" % (w["s"], w["w"]))
        f.write("\nCLIPS\n")
        for c in clips:
            f.write("  %6.2f  src %7.2f  %5.2fs  %-6s %s\n"
                    % (c["tl"], c["src_in"], c["dur"], c["frame"], c["text"]))
        said = [norm(t) for t in tokens(" ".join(w["w"] for w in kept))]
        hit = {w["j"] for w in kept if w["j"] is not None}
        miss = [i for i in range(len(script)) if i not in hit]
        f.write("\nSCRIPT WORDS NOT HEARD: %d of %d\n" % (len(miss), len(script)))
    print("plan: %d clips, %.2fs; dropped %d takes; %d flags"
          % (len(clips), total, len(dropped), len(flags)))
    if not render:
        return

    # ---- render: one ffmpeg per clip (accurate seek), then concat; audio in numpy
    segdir = os.path.join(scr, "segs")
    os.makedirs(segdir, exist_ok=True)
    lst = []
    for c in clips:
        # keyed by what the clip IS, so a re-plan never reuses a stale clip
        p = os.path.join(segdir, "c_%.3f_%d_%s_%s.mp4" % (c["src_in"], c["frames"], c["frame"],
                                                         "%.2f-%.2f" % tuple(face)))
        lst.append(p)
        if os.path.exists(p):
            continue
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", "%.4f" % c["src_in"],
                        "-i", src, "-an", "-vf", crop_filter(c["frame"], face) + ",fps=30",
                        "-frames:v", str(c["frames"]), "-c:v", "libx264", "-crf", "17",
                        "-preset", "fast", "-pix_fmt", "yuv420p", "-r", "30", p + ".tmp.mp4"],
                       check=True)
        os.replace(p + ".tmp.mp4", p)
    with open(os.path.join(segdir, "list.txt"), "w") as f:
        for p in lst:
            f.write("file '%s'\n" % p.replace("\\", "/"))
    vcat = os.path.join(scr, "video.mp4")
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0",
                    "-i", os.path.join(segdir, "list.txt"), "-c", "copy", vcat], check=True)

    fade = int(0.008 * sr)
    parts = []
    for c in clips:
        a0 = int(round(c["src_in"] * sr))
        n = int(round(c["frames"] / FPS * sr))
        seg = audio[a0:a0 + n].copy()
        if len(seg) < n:
            seg = np.vstack([seg, np.zeros((n - len(seg), audio.shape[1]), np.float32)])
        ramp = np.linspace(0, 1, fade)[:, None]
        seg[:fade] *= ramp
        seg[-fade:] *= ramp[::-1]
        parts.append(seg)
    vo = np.vstack(parts)
    owav = os.path.join(scr, "voice.wav")
    with wave.open(owav, "w") as f:
        f.setnchannels(vo.shape[1]); f.setsampwidth(2); f.setframerate(sr)
        f.writeframes(np.clip(vo, -32768, 32767).astype(np.int16).tobytes())
    reel = os.path.join(ROOT, "reel-" + nn, "assets")
    os.makedirs(reel, exist_ok=True)
    out = os.path.join(reel, "voice.mp4")
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", vcat, "-i", owav,
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-movflags", "+faststart", out], check=True)
    fr = subprocess.run(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v",
                         "-show_entries", "stream=nb_read_packets", "-of", "csv=p=0", out],
                        capture_output=True, text=True).stdout.strip()
    print("PLATE FRAMES %s  DUR = %.3f" % (fr, (int(fr) - 0.5) / 30.0))


if __name__ == "__main__":
    main()
