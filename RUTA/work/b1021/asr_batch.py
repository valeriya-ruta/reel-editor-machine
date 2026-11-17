# One whisper process for the whole batch — work/b1005/asr_batch.py on
# faster-whisper (CPU, int8), for the cloud container. Same packing: utterances
# (speech between silences) go in <=26 s windows; any utterance that looks like
# it hides a restart (a word over 1.2 s, or speech with too few words) is re-run
# alone. Output per take: work/b1021/asr/<stem>/utt.jsonl + silences.txt,
# saved as it goes. The take -> reel mapping happens after (match.py).
#
#   python work/b1021/asr_batch.py <raw dir>
import json, os, re, subprocess, sys, wave
import numpy as np
from faster_whisper import WhisperModel

RAW = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
m = WhisperModel("medium", device="cpu", compute_type="int8", cpu_threads=4)


def spans_of(src, wd):
    sil_p = wd + "/silences.txt"
    if not os.path.exists(sil_p):
        r = subprocess.run(["ffmpeg", "-nostdin", "-i", src, "-vn", "-af", "silencedetect=noise=-30dB:d=0.18",
                            "-f", "null", "-"], capture_output=True, text=True, encoding="utf-8", errors="replace")
        open(sil_p, "w").write(" ".join(re.findall(r"silence_(?:start|end): [\d.]+", r.stderr)))
    toks = open(sil_p).read().split()
    ev = [(toks[i], float(toks[i + 1])) for i in range(0, len(toks), 2)]
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src],
                               capture_output=True, text=True).stdout)
    spans, cur = [], 0.0
    for kind, t in ev:
        if kind == "silence_start:":
            if t - cur > 0.15:
                spans.append((cur, t))
        else:
            cur = t
    if (not ev or ev[-1][0] == "silence_end:") and dur - cur > 0.15:
        spans.append((cur, dur))
    return spans


_pcm = {}


def pcm(wav16):
    # the whole take as float32 @16k, once: faster-whisper takes an array, which
    # also keeps PyAV (version-fragile) out of the decode
    if wav16 not in _pcm:
        _pcm.clear()
        with wave.open(wav16) as f:
            _pcm[wav16] = np.frombuffer(f.readframes(f.getnframes()), np.int16).astype(np.float32) / 32768.0
    return _pcm[wav16]


def run(wav16, a, b):
    a0 = max(0, a - 0.12)
    x = pcm(wav16)
    chunk = x[int(a0 * 16000):int((b + 0.12) * 16000)]
    segs, _ = m.transcribe(chunk, language="uk", word_timestamps=True, condition_on_previous_text=False,
                           beam_size=5, vad_filter=False)
    return [{"w": x.word.strip(), "s": round(a0 + x.start, 3), "e": round(a0 + x.end, 3)}
            for s in segs for x in (s.words or [])]


def suspicious(a, b, words):
    if any(w["e"] - w["s"] > 1.2 for w in words):
        return True
    return (b - a) > 1.2 and len(words) < (b - a) / 0.9


for name in sorted(os.listdir(RAW)):
    if not name.endswith(".mp4"):
        continue
    stem = name[:-4]
    wd = os.path.join(HERE, "asr", stem)
    os.makedirs(wd, exist_ok=True)
    if os.path.exists(wd + "/.asr-done"):
        continue
    src = os.path.join(RAW, name)
    wav16 = wd + "/a16.wav"
    if not os.path.exists(wav16):
        subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", src, "-vn", "-ac", "1", "-ar", "16000",
                        wav16], check=True)
    spans = spans_of(src, wd)
    out = wd + "/utt.jsonl"
    done = set()
    if os.path.exists(out):
        for line in open(out, encoding="utf-8"):
            done.add(json.loads(line)["k"])
    todo = [k for k in range(len(spans)) if k not in done]
    while todo:
        chunk = [todo[0]]
        for k in todo[1:]:
            if k == chunk[-1] + 1 and spans[k][1] - spans[chunk[0]][0] <= 26.0:
                chunk.append(k)
            else:
                break
        todo = todo[len(chunk):]
        words = run(wav16, spans[chunk[0]][0], spans[chunk[-1]][1])
        per = {k: [] for k in chunk}
        for w in words:
            mid = (w["s"] + w["e"]) / 2
            k = min(chunk, key=lambda k: 0 if spans[k][0] - 0.1 <= mid <= spans[k][1] + 0.1
                    else min(abs(mid - spans[k][0]), abs(mid - spans[k][1])))
            per[k].append(w)
        with open(out, "a", encoding="utf-8") as f:
            for k in chunk:
                a, b = spans[k]
                ws = per[k]
                how = "pack"
                if suspicious(a, b, ws):
                    ws = run(wav16, a, b)
                    how = "solo"
                f.write(json.dumps({"k": k, "a": round(a, 3), "b": round(b, 3), "how": how,
                                    "text": " ".join(w["w"] for w in ws), "words": ws}, ensure_ascii=False) + "\n")
        print(stem, "chunk", chunk[0], "-", chunk[-1], "of", len(spans), flush=True)
    open(wd + "/.asr-done", "w").write("ok")
    print("DONE", stem, len(spans), flush=True)
print("ALL DONE", flush=True)
