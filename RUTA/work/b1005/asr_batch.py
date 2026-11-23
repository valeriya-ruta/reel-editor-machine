# One whisper process for the whole batch. Utterances (speech between silences)
# are packed into <=26 s windows — whisper pays for a full 30 s window per call,
# so one call per utterance cost ~4x. Any utterance that looks like it hides a
# restart (a word over 1.2 s, or speech with too few words) is re-run alone.
# Output per reel: work/rNN/utt.jsonl, one line per utterance, saved as it goes.
import whisper, json, subprocess, os, re
RAW = "C:/Users/Ruta/Downloads/"
ORDER = [("r21","20261005_131709"),("r22","20261005_132213"),("r23","20261005_131908"),
         ("r24","20261005_132416"),("r25","20261005_132900"),("r26","20261005_133142"),
         ("r27","20261005_133315"),("r28","20261005_133520"),("r29","20261005_133718")]
TMP = "E:/reels-work/asr"; os.makedirs(TMP, exist_ok=True)
m = whisper.load_model("medium")

def spans_of(src, wd):
    sil_p = wd + "/silences.txt"
    if not os.path.exists(sil_p):
        r = subprocess.run(["ffmpeg","-nostdin","-i",src,"-vn","-af","silencedetect=noise=-30dB:d=0.18","-f","null","-"],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        open(sil_p,"w").write(" ".join(re.findall(r"silence_(?:start|end): [\d.]+", r.stderr)))
    toks = open(sil_p).read().split()
    ev = [(toks[i], float(toks[i+1])) for i in range(0, len(toks), 2)]
    dur = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",src],
                               capture_output=True,text=True).stdout)
    spans, cur = [], 0.0
    for kind, t in ev:
        if kind == "silence_start:":
            if t - cur > 0.15: spans.append((cur, t))
        else: cur = t
    if (not ev or ev[-1][0] == "silence_end:") and dur - cur > 0.15: spans.append((cur, dur))
    return spans

def run(src, a, b):
    a0 = max(0, a - 0.12)
    wav = TMP + "/chunk.wav"
    subprocess.run(["ffmpeg","-nostdin","-v","error","-y","-ss","%.3f"%a0,"-to","%.3f"%(b+0.12),"-i",src,
                    "-vn","-ac","1","-ar","16000",wav], check=True)
    r = m.transcribe(wav, language="uk", word_timestamps=True, verbose=None, condition_on_previous_text=False)
    return [{"w": x["word"].strip(), "s": round(a0 + x["start"],3), "e": round(a0 + x["end"],3)}
            for s in r["segments"] for x in s.get("words", [])]

def suspicious(a, b, words):
    if any(w["e"] - w["s"] > 1.2 for w in words): return True
    return (b - a) > 1.2 and len(words) < (b - a) / 0.9

for rid, stem in ORDER:
    wd = "work/" + rid; os.makedirs(wd, exist_ok=True)
    if os.path.exists(wd + "/.asr-done"): continue
    src = RAW + stem + ".mp4"
    spans = spans_of(src, wd)
    out = wd + "/utt.jsonl"
    done = set()
    if os.path.exists(out):
        for line in open(out, encoding="utf-8"): done.add(json.loads(line)["k"])
    todo = [k for k in range(len(spans)) if k not in done]
    while todo:
        chunk = [todo[0]]
        for k in todo[1:]:
            if k == chunk[-1] + 1 and spans[k][1] - spans[chunk[0]][0] <= 26.0: chunk.append(k)
            else: break
        todo = todo[len(chunk):]
        words = run(src, spans[chunk[0]][0], spans[chunk[-1]][1])
        per = {k: [] for k in chunk}
        for w in words:
            mid = (w["s"] + w["e"]) / 2
            k = min(chunk, key=lambda k: 0 if spans[k][0] - 0.1 <= mid <= spans[k][1] + 0.1
                    else min(abs(mid - spans[k][0]), abs(mid - spans[k][1])))
            per[k].append(w)
        with open(out, "a", encoding="utf-8") as f:
            for k in chunk:
                a, b = spans[k]; ws = per[k]; how = "pack"
                if suspicious(a, b, ws):
                    ws = run(src, a, b); how = "solo"
                f.write(json.dumps({"k":k,"a":round(a,3),"b":round(b,3),"how":how,
                                    "text":" ".join(w["w"] for w in ws),"words":ws}, ensure_ascii=False)+"\n")
        print(rid, "chunk", chunk[0], "-", chunk[-1], "of", len(spans), flush=True)
    open(wd + "/.asr-done","w").write("ok")
    print("DONE", rid, len(spans), flush=True)
print("ALL DONE", flush=True)
