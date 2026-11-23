# -*- coding: utf-8 -*-
"""Study material for one reference reel: cuts, visual events, contact sheets.

    python tools/refstudy.py <video.mp4> <out_dir> [words.json]

Writes into out_dir:
    events.json   every frame-to-frame change above the noise: hard cuts
                  (whole frame changes) and overlay events (a sticker, a word,
                  a zoom step: part of the frame changes), with times
    stats.txt     shot lengths, event rate, and (with words.json) speech rate,
                  word gaps, and the music/voice level split
    sheet_NN.jpg  2 frames a second, 8 x 4 per sheet, each stamped with its time
    frame_T.png   nothing by default; use `--at 12.4,12.6` for full-size frames

Why: a client's LOOK.md is taken from her reference reels, scene by scene.
Reading a reel off contact sheets alone misses what happens between frames
(how a word arrives, how long it stays), so events.json gives the exact times
to zoom in on, and the transcript gives the word each event lands on.
"""
import json
import os
import subprocess
import sys

import numpy as np

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FPS = 30
W, H = 72, 128          # analysis size for frame differences


def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", path], capture_output=True, text=True).stdout
    return float(out.strip())


def frames(path):
    p = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", path, "-an", "-vf",
                        "fps=%d,scale=%d:%d,format=gray" % (FPS, W, H), "-f", "rawvideo", "-"],
                       capture_output=True, check=True)
    return np.frombuffer(p.stdout, np.uint8).reshape(-1, H, W).astype(np.float32)


def events(fr):
    """Per frame: the share of pixels that changed a lot, and where.
    A hard cut changes most of the frame; an overlay pops in one region."""
    d = np.abs(np.diff(fr, axis=0))
    big = d > 28
    share = big.mean(axis=(1, 2))
    rows = big.mean(axis=2)            # which heights changed
    out = []
    floor = max(0.02, float(np.median(share)) * 4)
    i = 0
    while i < len(share):
        if share[i] > floor:
            j = i
            while j + 1 < len(share) and share[j + 1] > floor:
                j += 1
            k = i + int(np.argmax(share[i:j + 1]))
            band = rows[k]
            hot = np.nonzero(band > 0.25)[0]
            y0, y1 = (int(hot[0] * 1920 / H), int((hot[-1] + 1) * 1920 / H)) if len(hot) else (0, 0)
            kind = "cut" if share[k] > 0.45 else "overlay"
            out.append({"t": round((k + 1) / FPS, 2), "kind": kind,
                        "share": round(float(share[k]), 3), "y": [y0, y1],
                        "frames": j - i + 1})
            i = j + 1
        else:
            i += 1
    return out


def sheets(path, out_dir, dur):
    n_per = 32
    total = int(dur * 2)
    for s in range(0, total, n_per):
        t0 = s / 2.0
        out = os.path.join(out_dir, "sheet_%02d.jpg" % (s // n_per + 1))
        vf = ("fps=2,scale=180:320,drawtext=fontfile=%s:text='%%{pts\\:hms\\:%.2f}':x=4:y=4:"
              "fontsize=15:fontcolor=yellow:box=1:boxcolor=black@0.7,tile=8x4:padding=4:color=black"
              % (FONT, t0))
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", "%.2f" % t0, "-t", "16",
                        "-i", path, "-vf", vf, "-frames:v", "1", out], check=True)


def audio_stats(path, words):
    p = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", path, "-vn", "-ac", "1",
                        "-ar", "16000", "-f", "s16le", "-"], capture_output=True, check=True)
    a = np.frombuffer(p.stdout, np.int16).astype(np.float32) / 32768.0
    hop = 160

    def rms(t0, t1):
        seg = a[int(t0 * 16000):int(t1 * 16000)]
        return float(np.sqrt((seg ** 2).mean() + 1e-12)) if len(seg) else 0.0
    v = [rms(w["s"], w["e"]) for w in words if w["e"] - w["s"] > 0.08]
    g = [rms(x["e"] + 0.03, y["s"] - 0.03) for x, y in zip(words, words[1:]) if y["s"] - x["e"] > 0.20]
    db = lambda x: 20 * np.log10(max(x, 1e-9))
    return (db(np.median(v)) if v else None, db(np.median(g)) if g else None, len(g))


def main():
    src, out_dir = sys.argv[1], sys.argv[2]
    wpath = sys.argv[3] if len(sys.argv) > 3 and not sys.argv[3].startswith("--") else None
    os.makedirs(out_dir, exist_ok=True)
    dur = probe(src)
    if "--at" in sys.argv:
        for t in sys.argv[sys.argv.index("--at") + 1].split(","):
            subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", t, "-i", src,
                            "-frames:v", "1", os.path.join(out_dir, "frame_%s.png" % t)], check=True)
        return
    ev = events(frames(src))
    json.dump(ev, open(os.path.join(out_dir, "events.json"), "w"), indent=0)
    sheets(src, out_dir, dur)
    cuts = [e["t"] for e in ev if e["kind"] == "cut"]
    shots = np.diff([0.0] + cuts + [dur])
    lines = ["duration %.2f s" % dur,
             "hard cuts %d (one every %.2f s); median shot %.2f s, shortest %.2f s, longest %.2f s"
             % (len(cuts), dur / max(1, len(cuts)), float(np.median(shots)), float(shots.min()), float(shots.max())),
             "visual events (cuts + overlays) %d: one every %.2f s"
             % (len(ev), dur / max(1, len(ev)))]
    if wpath:
        words = json.load(open(wpath, encoding="utf-8"))["words"]
        span = words[-1]["e"] - words[0]["s"]
        gaps = np.array([y["s"] - x["e"] for x, y in zip(words, words[1:])])
        lines.append("words %d, %.2f words/s over the spoken span" % (len(words), len(words) / span))
        lines.append("word gaps: median %.2f s; %d%% under 0.20 s; %d over 0.30 s; longest %.2f s"
                     % (float(np.median(gaps)), int(100 * (gaps < 0.20).mean()), int((gaps > 0.30).sum()),
                        float(gaps.max())))
        v, g, n = audio_stats(src, words)
        if v is not None and g is not None:
            lines.append("level: voice %.1f dBFS, between words %.1f dBFS (%d gaps) -> bed %.1f dB under voice"
                         % (v, g, n, v - g))
    open(os.path.join(out_dir, "stats.txt"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
