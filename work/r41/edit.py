# -*- coding: utf-8 -*-
"""Reel 41 — cut by hand from her raw take.

    CUT_SCRATCH=<dir> python work/r41/edit.py           # plan -> cut.json, cut.txt, words.json
    CUT_SCRATCH=<dir> python work/r41/edit.py --render  # plate -> reel-41/assets/voice.mp4

Unplanned reel, so there is no script for tools/cut.py to align against: the
takes are picked here, by hand, off work/r41/utt.jsonl. Her brief: *"waaaay
simpler — just cut out bad takes, pauses (except the one in the beginning)"*,
the vibe *"unplanned content, didn't even bother to edit a lot"*. So: last take
wins on every fumble, silences over ~0.45 s go, and the framing only steps
100 <-> 110 on a cut (tools/cutcam.py's rule, nothing slides) plus one closeup
on the repeated «Це настільки просто».

Rendering reuses tools/cut.py: same crop, same per-clip ffmpeg, same audio
splice with 8 ms fades.
"""
import json
import os
import subprocess
import sys
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import cut  # noqa: E402

cut.FRAMES["punch"] = (1.40, 0.0)
FPS = cut.FPS

# (raw in, raw out, framing, why). Edges are nudged to the quietest 10 ms
# within ±80 ms below; times here are read off utt.jsonl + silences.txt.
PLAN = [
    (1.15, 11.45, "base", "Це не запланований рілс … як я це роблю."),
    (11.45, 16.55, "in", "Сьогодні я зняла 12 нових рілсів. Ось вони в мене в галереї …"),
    # dropped 16.55-23.72: «І це інтепер. Тепер я показую свої рухи.» and the
    # glasses pause. v1 kept the pause; her review cut 0:16 to «Перше».
    (23.72, 32.60, "base", "Перше, що треба зробити … закинути їх на комп'ютер."),
    (32.60, 40.52, "in", "Але я люблю робити все в хмарі … в хмарі."),
    (40.84, 43.36, "base", "Тому перше, що я роблю … на Google Диск."),
    # dropped 43.36-45.40: she gets up and picks the phone up
    (45.40, 46.26, "base", "У мене є"),
    (46.60, 49.10, "base", "папочка, в якій я завантажила всі ці рілси."),
    # dropped 49.1-60.1: «Далі, я…» «Де?» «Далі я беру посилання.» ×2 — false starts
    (60.12, 64.26, "base", "Далі я відкриваю доступ для усіх до цієї папки. Беру посилання"),
    # dropped 64.26-70.6: «і вставляю сюди…» — said again whole at 70.7
    (70.60, 72.30, "base", "І вставляю сюди в Клод."),
    (73.34, 75.26, "base", "І все, ось він в мене тут працює."),
    # dropped 75.26-97.2: the first «почекати годинки дві» take, «Коли…», «Тепер мені.»
    (97.20, 101.24, "base", "Тепер мені треба просто почекати 2-3 годинки, поки я працюю, він це все"),
    (101.47, 106.36, "in", "підготує і потім видасть мені файли … свої правки."),
    (106.36, 112.84, "base", "І якщо мені все подобається … з Edits."),
    # dropped 112.84-122.0: «Все.», the pause, «Тому це для…» «…для тих» — false starts
    (122.00, 126.04, "in", "Тому цей рілс був для всіх тих, хто не вірить, що це настільки просто."),
    (126.04, 127.26, "punch", "Це настільки просто."),
    # dropped 127.26-134.1: the first CTA take
    (134.10, 138.80, "base", "І якщо я тебе переконала … пиши плюс в коментарі."),
]


def main():
    scr = os.environ.get("CUT_SCRATCH", "E:/reels-work")
    src = open(os.path.join(HERE, "SOURCE.txt"), encoding="utf-8").read().strip()
    utts = [json.loads(l) for l in open(os.path.join(HERE, "utt.jsonl"), encoding="utf-8")]
    wd = os.path.join(scr, "r41")
    os.makedirs(wd, exist_ok=True)
    wav = os.path.join(wd, "full48.wav")
    if not os.path.exists(wav):
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", src, "-vn", "-ac", "2",
                        "-ar", "48000", "-c:a", "pcm_s16le", wav], check=True)
    sr, audio = cut.read_wav(wav)
    env, hop = cut.envelope(audio, sr)

    # nudge every edge that removes content to the quietest moment nearby;
    # an edge shared by two clips (a zoom step, nothing removed) stays put
    segs = [list(p) for p in PLAN]
    for i, s in enumerate(segs):
        if i == 0 or abs(segs[i - 1][1] - s[0]) > 0.01:
            s[0] = round(cut.quietest(env, hop, s[0] - 0.08, s[0] + 0.08), 3)
        if i == len(segs) - 1 or abs(segs[i + 1][0] - s[1]) > 0.01:
            s[1] = round(cut.quietest(env, hop, s[1] - 0.08, s[1] + 0.08), 3)
        elif i + 1 < len(segs):
            segs[i + 1][0] = s[1]

    clips, t = [], 0.0
    for i, (a, b, frame, why) in enumerate(segs):
        n = max(1, int(round((b - a) * FPS)))
        clips.append({"i": i, "src_in": a, "frames": n, "dur": round(n / FPS, 4),
                      "tl": round(t, 4), "frame": frame, "text": why})
        t += n / FPS
    total = round(t, 4)

    # her words on the output timeline -> words.json for tools/align.py
    words = [dict(w) for u in utts for w in u["words"]]
    out_words = []
    for c in clips:
        a, b = c["src_in"], c["src_in"] + c["dur"]
        for w in words:
            mid = (w["s"] + w["e"]) / 2
            if a <= mid < b:
                out_words.append({"w": w["w"], "s": round(max(c["tl"], c["tl"] + w["s"] - a), 3),
                                  "e": round(c["tl"] + min(w["e"], b) - a, 3)})
    out_words.sort(key=lambda w: w["s"])
    json.dump({"text": " ".join(w["w"] for w in out_words), "words": out_words},
              open(os.path.join(HERE, "words.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    no_paint = [[c["tl"], round(c["tl"] + c["dur"], 3)] for c in clips if c["frame"] == "punch"]
    json.dump({"source": src, "duration": total, "clips": clips, "no_paint": no_paint, "flags": []},
              open(os.path.join(HERE, "cut.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    with open(os.path.join(HERE, "cut.txt"), "w", encoding="utf-8") as f:
        f.write("raw %.1fs -> plate %.2fs, %d clips (hand cut, see edit.py for the drops)\n\nCLIPS\n"
                % (len(audio) / sr, total, len(clips)))
        for c in clips:
            f.write("  %6.2f  src %7.2f  %5.2fs  %-6s %s\n"
                    % (c["tl"], c["src_in"], c["dur"], c["frame"], c["text"]))
    print("plan: %d clips, %.2fs" % (len(clips), total))
    if "--render" not in sys.argv:
        return

    segdir = os.path.join(wd, "segs")
    os.makedirs(segdir, exist_ok=True)
    lst = []
    for c in clips:
        p = os.path.join(segdir, "c_%.3f_%d_%s.mp4" % (c["src_in"], c["frames"], c["frame"]))
        lst.append(p)
        if os.path.exists(p):
            continue
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", "%.4f" % c["src_in"],
                        "-i", src, "-an", "-vf", cut.crop_filter(c["frame"], (0.5, 0.45)) + ",fps=30",
                        "-frames:v", str(c["frames"]), "-c:v", "libx264", "-crf", "17",
                        "-preset", "fast", "-pix_fmt", "yuv420p", "-r", "30", p + ".tmp.mp4"], check=True)
        os.replace(p + ".tmp.mp4", p)
        print("  clip %d done" % c["i"], flush=True)
    with open(os.path.join(segdir, "list.txt"), "w") as f:
        for p in lst:
            f.write("file '%s'\n" % p)
    vcat = os.path.join(wd, "video.mp4")
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0",
                    "-i", os.path.join(segdir, "list.txt"), "-c", "copy", vcat], check=True)

    fade = int(0.008 * sr)
    parts = []
    for c in clips:
        a0, n = int(round(c["src_in"] * sr)), int(round(c["frames"] / FPS * sr))
        seg = audio[a0:a0 + n].copy()
        if len(seg) < n:
            seg = np.vstack([seg, np.zeros((n - len(seg), audio.shape[1]), np.float32)])
        ramp = np.linspace(0, 1, fade)[:, None]
        seg[:fade] *= ramp
        seg[-fade:] *= ramp[::-1]
        parts.append(seg)
    vo = np.vstack(parts)
    owav = os.path.join(wd, "voice.wav")
    with wave.open(owav, "w") as f:
        f.setnchannels(vo.shape[1]); f.setsampwidth(2); f.setframerate(sr)
        f.writeframes(np.clip(vo, -32768, 32767).astype(np.int16).tobytes())
    out = os.path.join(ROOT, "reel-41", "assets", "voice.mp4")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", vcat, "-i", owav, "-map", "0:v",
                    "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
                    out], check=True)
    fr = subprocess.run(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v", "-show_entries",
                         "stream=nb_read_packets", "-of", "csv=p=0", out], capture_output=True, text=True).stdout.strip()
    print("PLATE FRAMES %s  DUR = %.3f" % (fr, (int(fr) - 0.5) / 30.0))


if __name__ == "__main__":
    main()
