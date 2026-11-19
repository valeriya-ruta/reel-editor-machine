# -*- coding: utf-8 -*-
"""Per-utterance ASR of one raw take: silences found first, then one whisper
pass per spoken span. Resumable, saved as it goes. Output: work/rNN/utt.jsonl,
which tools/cut.py reads.

    python tools/utt.py 01        # reads work/r01/SOURCE.txt

Copied from Ruta's reel-editor-machine (work/b1005/utt_batch.py); only the
batch list became one reel read from SOURCE.txt. Detection is unchanged:
ffmpeg silencedetect at -30 dB, 0.18 s minimum.
"""
import whisper, json, subprocess, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
nn = sys.argv[1].zfill(2)
_src = open("work/r%s/SOURCE.txt" % nn, encoding="utf-8").read().strip()
if not os.path.isabs(_src):
    _src = os.path.join(ROOT, _src)
ORDER = [("r" + nn, _src)]
m = whisper.load_model(sys.argv[2] if len(sys.argv) > 2 else "medium")
for rid, stem in ORDER:
    wd = "work/%s" % rid; os.makedirs(wd + "/utt", exist_ok=True)
    src = stem
    sil_p = wd + "/silences.txt"
    if not os.path.exists(sil_p):
        r = subprocess.run(["ffmpeg","-nostdin","-i",src,"-vn","-af","silencedetect=noise=-30dB:d=0.18","-f","null","-"],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        open(sil_p,"w").write(" ".join(re.findall(r"silence_(?:start|end): [\d.]+", r.stderr)))
    toks = open(sil_p).read().split()
    ev = [(toks[i], float(toks[i+1])) for i in range(0, len(toks), 2)]
    dur = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",src],
                               capture_output=True,text=True).stdout)
    # speech spans = complement of silences
    spans, cur = [], 0.0
    for kind, t in ev:
        if kind == "silence_start:":
            if t - cur > 0.15: spans.append((cur, t))
        else: cur = t
    if ev and ev[-1][0] == "silence_end:" and dur - cur > 0.15: spans.append((cur, dur))
    if not ev: spans = [(0, dur)]
    out = wd + "/utt.jsonl"
    done = set()
    if os.path.exists(out):
        for line in open(out, encoding="utf-8"): done.add(json.loads(line)["k"])
    for k, (a, b) in enumerate(spans):
        if k in done: continue
        wav = "%s/utt/u%03d.wav" % (wd, k)
        a0 = max(0, a - 0.12)
        subprocess.run(["ffmpeg","-nostdin","-v","error","-y","-ss","%.3f"%a0,"-to","%.3f"%(b+0.12),"-i",src,
                        "-vn","-ac","1","-ar","16000",wav], check=True)
        r = m.transcribe(wav, language="uk", word_timestamps=True, verbose=None, condition_on_previous_text=False)
        words = [{"w": x["word"].strip(), "s": round(a0 + x["start"],3), "e": round(a0 + x["end"],3)}
                 for s in r["segments"] for x in s.get("words", [])]
        with open(out, "a", encoding="utf-8") as f:
            f.write(json.dumps({"k":k,"a":round(a,3),"b":round(b,3),"text":r["text"].strip(),"words":words}, ensure_ascii=False)+"\n")
        os.remove(wav)
    open(wd + "/.asr-done","w").write("ok")
    print("DONE", rid, len(spans), flush=True)
print("ALL DONE", flush=True)
