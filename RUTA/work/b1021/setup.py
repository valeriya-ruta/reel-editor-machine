# -*- coding: utf-8 -*-
"""Stage one take as reel NN: work/rNN/{SOURCE.txt, script.txt, utt.jsonl,
silences.txt}.   python work/b1021/setup.py 42 20261021_131316 needs"""
import os, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW = "/tmp/claude-0/-home-user-reel-editor-machine/cd246088-a040-50f5-93d6-6b9a5955beda/scratchpad/raw"
nn, stem, slug = sys.argv[1:4]
wd = "%s/work/r%s" % (ROOT, nn)
os.makedirs(wd, exist_ok=True)
open(wd + "/SOURCE.txt", "w").write("%s/%s.mp4\n" % (RAW, stem))
shutil.copy("%s/work/b1021/scripts/%s.txt" % (ROOT, slug), wd + "/script.txt")
for f in ("utt.jsonl", "silences.txt"):
    shutil.copy("%s/work/b1021/asr/%s/%s" % (ROOT, stem, f), wd + "/" + f)
print("r%s <- %s (%s)" % (nn, stem, slug))
