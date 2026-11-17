# -*- coding: utf-8 -*-
"""Match each take's transcript (work/b1021/asr/<stem>/utt.jsonl) to a script in
work/b1021/scripts/*.txt by word-bigram overlap. Prints a score table."""
import glob, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))


def toks(s):
    return re.findall(r"[a-zа-яіїєґ0-9']+", s.lower().replace("’", "'").replace("ʼ", "'"))


def grams(t):
    return set(zip(t, t[1:]))


scripts = {os.path.basename(p)[:-4]: grams(toks(open(p, encoding="utf-8").read()))
           for p in glob.glob(HERE + "/scripts/*.txt")}
for d in sorted(glob.glob(HERE + "/asr/*/utt.jsonl")):
    stem = os.path.basename(os.path.dirname(d))
    text = " ".join(json.loads(l)["text"] for l in open(d, encoding="utf-8"))
    g = grams(toks(text))
    sc = sorted(((len(g & s) / max(1, len(s)), n) for n, s in scripts.items()), reverse=True)
    print(stem, " ".join("%s=%.2f" % (n, v) for v, n in sc[:3]), "|", text[:80])
