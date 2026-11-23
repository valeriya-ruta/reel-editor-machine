# -*- coding: utf-8 -*-
"""Match each cloud transcript (E:/reels-work/asr1012/<clip>/utt.jsonl) to a
script in work/r30..r40/script.txt by word-bigram overlap. Prints a score table
and the best assignment."""
import glob, json, os, re

ROOT = "C:/Users/Ruta/Desktop/reels-2026-09"
ASR = "E:/reels-work/asr1012"


def toks(s):
    return re.findall(r"[a-zа-яіїєґ0-9']+", s.lower().replace("’", "'").replace("ʼ", "'"))


def grams(t):
    return set(zip(t, t[1:]))


scripts = {n: grams(toks(open("%s/work/r%d/script.txt" % (ROOT, n), encoding="utf-8").read()))
           for n in range(30, 41)}
for d in sorted(glob.glob(ASR + "/c*/utt.jsonl")):
    clip = os.path.basename(os.path.dirname(d))
    text = " ".join(json.loads(l)["text"] for l in open(d, encoding="utf-8"))
    g = grams(toks(text))
    sc = sorted(((len(g & s) / max(1, len(s)), n) for n, s in scripts.items()), reverse=True)
    print(clip, " ".join("r%d=%.2f" % (n, v) for v, n in sc[:3]), "|", text[:70])
