# -*- coding: utf-8 -*-
"""Reel 56 plate, v2: her intro and outro as filmed, and between them six
sections of footage, each fitted to her voiceover line (work/r56/vo.json).

    python3 work/r56/vo.py <her recording>     # first: finds her six lines
    python3 work/r56/mkplate.py                -> reel-56/assets/base.mp4 + work/r56/pieces.out.json

Her call on v1 (2026-11-17): "the part where I'm talking in the headphones,
just speed that part up, remove completely the text or the sounds … I'm gonna
record everything that's not the beginning, the intro or the outro". So the
middle has no sound of its own: only her voiceover, levelled to her intro.
Each section plays its source spans back to back, retimed to last exactly as
long as her words for it — the headphones part ends up ~7x, the prompt paste
~2.4x, the chat and the deck near real time.

She read it in her own words as one continuous take, so it plays as one
track from the end of the intro and every section is cut on her timing.
"""
import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SRC = os.path.join(ROOT, "work", "incoming", "r56")
OUT = os.path.join(ROOT, "reel-56", "assets", "base.mp4")
SEG = os.path.join(HERE, "seg")
CUT = os.path.join(SEG, "cut.mp4")          # the cut before her voiceover goes on
FPS = 30

C1, C2, C3, C4 = ("20261117_%s.mp4" % n for n in ("132849", "132924", "134447", "135042"))
INTRO = {"id": "A", "src": C1, "a": 1.60, "b": 12.65}      # «Сьогодні ввечері…Погнали!»
OUTRO = {"id": "G", "src": C1, "a": 13.45, "b": 16.00}     # «Якщо було корисно…підпишись.»
SECTIONS = [
    # source clip and spans, played back to back then retimed to her take's section (vo.json)
    {"id": "S1", "src": C2, "spans": [(0.90, 1.80), (2.70, 5.20)]},               # Claude → New
    {"id": "S2", "src": C2, "spans": [(5.40, 18.38)]},                            # prompt pasted → sent
    {"id": "S3", "src": C2, "spans": [(18.45, 60.60)]},                           # her in headphones
    {"id": "S4", "src": C3, "spans": [(0.80, 3.55), (6.78, 7.98)]},               # the base deck (unused: her take skips it)
    {"id": "S5", "src": C3, "spans": [(8.70, 12.40)]},                            # the voice notes in the chat
    # finished deck: the clean title slide, then her clicking through the slides (her note on
    # v2: "I want to show the slides … if the editing part … doesn't fit, cut that out")
    {"id": "S6", "src": C4, "spans": [(7.30, 8.30), (C3, 2.00, 7.70)]},
]


def ff(*args):
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y"] + list(args), check=True)


def enc_v():
    return ["-c:v", "libx264", "-crf", "17", "-preset", "fast", "-pix_fmt", "yuv420p"]


def camera(p, f):
    """a to-camera piece with her own sound, whole frames, de-clicked edges"""
    n = int(round((p["b"] - p["a"]) * FPS))
    d = n / float(FPS)
    ff("-ss", "%.3f" % p["a"], "-i", os.path.join(SRC, p["src"]), "-t", "%.4f" % d,
       "-vf", "scale=1080:1920:flags=lanczos,fps=%d,setsar=1" % FPS, "-frames:v", str(n),
       "-af", "apad,atrim=0:%.4f,afade=t=in:d=0.012,afade=t=out:st=%.4f:d=0.02" % (d, d - 0.02),
       *enc_v(), "-c:a", "pcm_s16le", "-ar", "48000", "-ac", "2", f)
    return n


def section(s, dur, f):
    """the section's spans back to back, retimed to dur, silent"""
    raw = os.path.join(SEG, s["id"] + "-raw.mp4")
    ins, chain = [], []
    spans = [x if len(x) == 3 else (s["src"],) + tuple(x) for x in s["spans"]]   # a span may name its clip
    for k, (clip, a, b) in enumerate(spans):
        ins += ["-ss", "%.3f" % a, "-t", "%.3f" % (b - a), "-i", os.path.join(SRC, clip)]
        chain.append("[%d:v]scale=1080:1920:flags=lanczos,fps=%d,setsar=1,setpts=PTS-STARTPTS[v%d]" % (k, FPS, k))
    chain.append("".join("[v%d]" % k for k in range(len(s["spans"]))) +
                 "concat=n=%d:v=1:a=0[v]" % len(s["spans"]))
    ff(*ins, "-filter_complex", ";".join(chain), "-map", "[v]", *enc_v(), "-an", raw)
    src_len = sum(b - a for _, a, b in spans)
    n = int(round(dur * FPS))
    speed = src_len / (n / float(FPS))
    # retime, then pad by holding the last frame if rounding left it a frame short
    ff("-i", raw, "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
       "-filter_complex", "[0:v]setpts=PTS/%.5f,fps=%d,tpad=stop_mode=clone:stop_duration=1[v]" % (speed, FPS),
       "-map", "[v]", "-map", "1:a", "-frames:v", str(n), "-t", "%.4f" % (n / float(FPS)),
       *enc_v(), "-c:a", "pcm_s16le", f)
    return n, speed


def rms_db(path, spans):
    import numpy as np
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
    v = np.concatenate([x[int(a * 16000):int(b * 16000)] for a, b in spans])
    return 20 * np.log10(np.sqrt((v ** 2).mean()) + 1e-9)


def main():
    vo = json.load(open(os.path.join(HERE, "vo.json")))
    by_id = {x["id"]: x for x in SECTIONS}
    os.makedirs(SEG, exist_ok=True)
    out, lst, t = [], [], 0
    f = os.path.join(SEG, "A.mov")
    n = camera(INTRO, f)
    out.append(dict(INTRO, t0=0.0, t1=round(n / float(FPS), 4)))
    lst.append(f)
    t += n
    t_vo = t / float(FPS)                         # her take's v0 lands here
    for sec in vo["sections"]:
        s = by_id[sec["id"]]
        # cut on her timing: this section ends where her next one begins (whole frames)
        end_f = int(round((t_vo + sec["b"] - vo["v0"]) * FPS))
        dur = (end_f - t) / float(FPS)
        f = os.path.join(SEG, s["id"] + ".mov")
        n, speed = section(s, dur, f)
        out.append(dict(s, t0=round(t / float(FPS), 4), t1=round((t + n) / float(FPS), 4), speed=round(speed, 3)))
        lst.append(f)
        t += n
    f = os.path.join(SEG, "G.mov")
    n = camera(OUTRO, f)
    out.append(dict(OUTRO, t0=round(t / float(FPS), 4), t1=round((t + n) / float(FPS), 4)))
    lst.append(f)
    t += n
    open(os.path.join(SEG, "list.txt"), "w").write("".join("file '%s'\n" % x for x in lst))
    ff("-f", "concat", "-safe", "0", "-i", os.path.join(SEG, "list.txt"), "-c:v", "copy",
       "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", CUT)
    # her take as one track from the end of the intro, levelled to her intro to camera
    a, b = vo["v0"], vo["speech_end"] + 0.35
    gain = rms_db(CUT, [(2.0, 9.0)]) - rms_db(vo["src"], [(a, b)])
    ms = int(round(t_vo * 1000))
    ff("-i", CUT, "-ss", "%.3f" % a, "-t", "%.3f" % (b - a), "-i", vo["src"], "-filter_complex",
       "[1:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=%.2fdB,afade=t=in:d=0.03,"
       "afade=t=out:st=%.3f:d=0.15,adelay=%d|%d[v];[0:a][v]amix=inputs=2:normalize=0:duration=first[a]"
       % (gain, b - a - 0.15, ms, ms),
       "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", OUT)
    out[0]["t_vo"] = round(t_vo, 4)
    out[0]["v0"] = vo["v0"]
    json.dump(out, open(os.path.join(HERE, "pieces.out.json"), "w"), indent=1)
    print("voiceover from %.2f s, gain %+.1f dB" % (t_vo, gain))
    print("PLATE %d frames, %.3f s" % (t, t / float(FPS)))
    for p in out[1:-1]:
        print("  %s %.2f-%.2f speed %.2fx" % (p["id"], p["t0"], p["t1"], p["speed"]))


main()
