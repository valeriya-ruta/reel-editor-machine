# -*- coding: utf-8 -*-
"""Compact cut review: every utterance with K (kept, wholly or partly) or
D (dropped) from work/rNN/cut.json.   python work/b1012/view.py 35"""
import json, sys

ROOT = "C:/Users/Ruta/Desktop/reels-2026-09"
for nn in sys.argv[1:]:
    cut = json.load(open("%s/work/r%s/cut.json" % (ROOT, nn), encoding="utf-8"))
    spans = [(c["src_in"], c["src_in"] + c["frames"] / 30.0) for c in cut["clips"]]
    print("=== r%s  plate %.1fs" % (nn, cut["duration"]))
    for l in open("%s/work/r%s/utt.jsonl" % (ROOT, nn), encoding="utf-8"):
        u = json.loads(l)
        if not u["text"].strip():
            continue
        kept = sum(max(0, min(b, u["b"]) - max(a, u["a"])) for a, b in spans)
        mark = "K" if kept > 0.6 * (u["b"] - u["a"]) else ("k" if kept > 0 else "D")
        print("%s %6.2f-%6.2f %s" % (mark, u["a"], u["b"], u["text"]))
