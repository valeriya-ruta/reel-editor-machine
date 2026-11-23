# Per-utterance ASR for the 2026-11-20 batch (faster-whisper port of work/b1005/utt_batch.py).
import json, subprocess, os, re, sys
from faster_whisper import WhisperModel
RAW = "work/inbox-1120/"
ORDER = [("r41","20261120_133314"), ("r42","20261120_133702"), ("r43","20261120_133928"), ("r44","20261120_134134"), ("r45","20261120_134413"), ("r46","20261120_134603"), ("r47","20261120_134834"), ("r48","20261120_135006"), ("r49","20261120_135335"), ("r50","20261120_135523"), ("r51","20261120_135706"), ("r52","20261120_135854"), ("r53","20261120_140030"), ("r54","20261120_140234"), ("r55","20261120_140447"), ("r56","20261120_140714")]
if len(sys.argv) > 1: ORDER = [o for o in ORDER if o[0] in sys.argv[1:]]
m = WhisperModel("medium", device="cpu", compute_type="int8", cpu_threads=4)
for rid, stem in ORDER:
    wd = "work/%s" % rid; os.makedirs(wd + "/utt", exist_ok=True)
    src = RAW + stem + ".mp4"
    open(wd + "/SOURCE.txt", "w").write(os.path.abspath(src) + "\n")
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
    if ev and ev[-1][0] == "silence_end:" and dur - cur > 0.15: spans.append((cur, dur))
    if not ev: spans = [(0, dur)]
    out = wd + "/utt.jsonl"; done = set()
    if os.path.exists(out):
        for line in open(out, encoding="utf-8"): done.add(json.loads(line)["k"])
    for k, (a, b) in enumerate(spans):
        if k in done: continue
        wav = "%s/utt/u%03d.wav" % (wd, k); a0 = max(0, a - 0.12)
        subprocess.run(["ffmpeg","-nostdin","-v","error","-y","-ss","%.3f"%a0,"-to","%.3f"%(b+0.12),"-i",src,
                        "-vn","-ac","1","-ar","16000",wav], check=True)
        segs, _ = m.transcribe(wav, language="uk", word_timestamps=True, condition_on_previous_text=False, beam_size=5)
        segs = list(segs)
        words = [{"w": x.word.strip(), "s": round(a0 + x.start,3), "e": round(a0 + x.end,3)}
                 for s in segs for x in (s.words or [])]
        with open(out, "a", encoding="utf-8") as f:
            f.write(json.dumps({"k":k,"a":round(a,3),"b":round(b,3),"text":" ".join(s.text.strip() for s in segs),"words":words}, ensure_ascii=False)+"\n")
        os.remove(wav)
    open(wd + "/.asr-done","w").write("ok")
    print("DONE", rid, len(spans), flush=True)
print("ALL DONE", flush=True)
