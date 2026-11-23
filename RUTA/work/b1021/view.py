# -*- coding: utf-8 -*-
"""Word-level cut review: every utterance of the raw take, each word marked
kept (plain) or [dropped], with the clip boundaries on the plate timeline.
    python work/b1021/view.py 41"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
for nn in sys.argv[1:]:
    wd = "%s/work/r%s" % (ROOT, nn)
    cut = json.load(open(wd + "/cut.json", encoding="utf-8"))
    spans = [(c["src_in"], c["src_in"] + c["frames"] / 30.0) for c in cut["clips"]]
    print("=== r%s  plate %.1fs  %d clips" % (nn, cut["duration"], len(cut["clips"])))
    for l in open(wd + "/utt.jsonl", encoding="utf-8"):
        u = json.loads(l)
        if not u["words"]:
            continue
        out = []
        for w in u["words"]:
            mid = (w["s"] + w["e"]) / 2
            k = any(a <= mid < b for a, b in spans)
            out.append(w["w"] if k else "[" + w["w"] + "]")
        print("%3d %6.2f-%6.2f %s" % (u["k"], u["a"], u["b"], " ".join(out)))
    # every real join (content removed), with the words either side as they will play
    allw = sorted((w for l in open(wd + "/utt.jsonl", encoding="utf-8") for w in json.loads(l)["words"]),
                  key=lambda w: w["s"])
    clips = cut["clips"]
    for p, c in zip(clips, clips[1:]):
        pe = p["src_in"] + p["frames"] / 30.0
        if abs(pe - c["src_in"]) <= 0.02:
            continue
        before = [w["w"] for w in allw if p["src_in"] <= (w["s"] + w["e"]) / 2 < pe][-3:]
        after = [w["w"] for w in allw if c["src_in"] <= (w["s"] + w["e"]) / 2 < c["src_in"] + c["frames"] / 30.0][:3]
        b0 = before[-1].lower().strip(".,!?–-—") if before else ""
        a0 = after[0].lower().strip(".,!?–-—") if after else ""
        flag = "  <<< DOUBLE?" if b0 and (b0 == a0 or (len(b0) >= 2 and a0.startswith(b0))) else ""
        print("  JOIN %6.2f  %s | %s%s" % (c["tl"], " ".join(before), " ".join(after), flag))
