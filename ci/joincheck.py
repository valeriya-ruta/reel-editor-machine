# Listen to every join of a finished plate (her REEL-31 note, 2026-10-12: a cut
# 0.08 s late kept the first «в» of a retake -> «Напиши в… в коментарях», which
# the plan could not show). Re-transcribe 1.4 s either side of each join and
# flag a word or a word-start that repeats across it.
#   python ci/joincheck.py reel-NN/assets/voice.mp4 work/rNN/cut.json out.txt
import json, re, subprocess, sys
import whisper

src, cutp, outp = sys.argv[1:4]
cut = json.load(open(cutp, encoding="utf-8"))
joins = [c["tl"] for c in cut["clips"][1:]]
m = whisper.load_model("medium")


def norm(w):
    return re.sub(r"[^\w']", "", w.lower())


lines = []
for t in joins:
    a = max(0.0, t - 1.4)
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", "%.3f" % a, "-to", "%.3f" % (t + 1.4),
                    "-i", src, "-vn", "-ac", "1", "-ar", "16000", "j.wav"], check=True)
    r = m.transcribe("j.wav", language="uk", word_timestamps=True, condition_on_previous_text=False, verbose=None)
    ws = [(norm(x["word"]), a + x["start"], a + x["end"]) for s in r["segments"] for x in s.get("words", [])]
    ws = [w for w in ws if w[0]]
    for (w0, s0, e0), (w1, s1, e1) in zip(ws, ws[1:]):
        near = abs(e0 - t) < 0.5 or abs(s1 - t) < 0.5
        same = w0 == w1 or (len(w0) >= 2 and w1.startswith(w0)) or (len(w1) >= 2 and w0.startswith(w1))
        if near and same:
            lines.append("REPEAT at %.2f: «%s» %.2f-%.2f then «%s» %.2f-%.2f" % (t, w0, s0, e0, w1, s1, e1))
    print("join %.2f: %s" % (t, " ".join(w[0] for w in ws)), flush=True)
open(outp, "w", encoding="utf-8").write("\n".join(lines) + ("\n" if lines else "clean\n"))
print("\n".join(lines) or "clean")
