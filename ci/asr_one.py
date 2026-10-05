# Same logic as work/b1005/asr_batch.py in the reel repo: utterances between
# silences, packed into <=26 s whisper windows; anything that looks like it hides
# a restart (a word > 1.2 s, too few words for its length) is re-run alone.
import json, os, re, subprocess, sys
import whisper
src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
r = subprocess.run(["ffmpeg", "-nostdin", "-i", src, "-vn", "-af", "silencedetect=noise=-30dB:d=0.18", "-f", "null", "-"],
                   capture_output=True, text=True, errors="replace")
sil = " ".join(re.findall(r"silence_(?:start|end): [\d.]+", r.stderr))
open(out + "/silences.txt", "w").write(sil)
toks = sil.split()
ev = [(toks[i], float(toks[i + 1])) for i in range(0, len(toks), 2)]
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src],
                           capture_output=True, text=True).stdout)
spans, cur = [], 0.0
for kind, t in ev:
    if kind == "silence_start:":
        if t - cur > 0.15: spans.append((cur, t))
    else: cur = t
if (not ev or ev[-1][0] == "silence_end:") and dur - cur > 0.15: spans.append((cur, dur))
m = whisper.load_model("medium")

def run(a, b):
    a0 = max(0, a - 0.12)
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", "%.3f" % a0, "-to", "%.3f" % (b + 0.12), "-i", src,
                    "-vn", "-ac", "1", "-ar", "16000", "chunk.wav"], check=True)
    res = m.transcribe("chunk.wav", language="uk", word_timestamps=True, verbose=None, condition_on_previous_text=False)
    return [{"w": x["word"].strip(), "s": round(a0 + x["start"], 3), "e": round(a0 + x["end"], 3)}
            for s in res["segments"] for x in s.get("words", [])]

def suspicious(a, b, words):
    if any(w["e"] - w["s"] > 1.2 for w in words): return True
    return (b - a) > 1.2 and len(words) < (b - a) / 0.9

todo = list(range(len(spans)))
with open(out + "/utt.jsonl", "w", encoding="utf-8") as f:
    while todo:
        chunk = [todo[0]]
        for k in todo[1:]:
            if k == chunk[-1] + 1 and spans[k][1] - spans[chunk[0]][0] <= 26.0: chunk.append(k)
            else: break
        todo = todo[len(chunk):]
        words = run(spans[chunk[0]][0], spans[chunk[-1]][1])
        per = {k: [] for k in chunk}
        for w in words:
            mid = (w["s"] + w["e"]) / 2
            k = min(chunk, key=lambda k: 0 if spans[k][0] - 0.1 <= mid <= spans[k][1] + 0.1
                    else min(abs(mid - spans[k][0]), abs(mid - spans[k][1])))
            per[k].append(w)
        for k in chunk:
            a, b = spans[k]; ws = per[k]; how = "pack"
            if suspicious(a, b, ws):
                ws = run(a, b); how = "solo"
            f.write(json.dumps({"k": k, "a": round(a, 3), "b": round(b, 3), "how": how,
                                "text": " ".join(w["w"] for w in ws), "words": ws}, ensure_ascii=False) + "\n")
        print("chunk", chunk[0], "-", chunk[-1], "of", len(spans), flush=True)
print("DONE", len(spans))
