# -*- coding: utf-8 -*-
"""Take cloud plates in: download the plate.yml artifacts of a run, put each
reel's voice.mp4 / cut.json / cut.txt / words.json in place, align captions.

    python work/b1012/intake.py <plate-run-id> 31 32 ...
"""
import os, shutil, subprocess, sys

ROOT = "C:/Users/Ruta/Desktop/reels-2026-09"
REPO = "valeriya-ruta/reel-editor-machine"
run = sys.argv[1]
dl = "E:/reels-work/plates-%s" % run
if not os.path.isdir(dl):
    subprocess.run(["gh", "run", "download", run, "--repo", REPO, "-D", dl], check=True)
for nn in sys.argv[2:]:
    art = [d for d in os.listdir(dl) if d.startswith("plate-%s-" % nn)]
    if not art:
        print("r%s: no plate artifact" % nn); continue
    base = os.path.join(dl, art[0])
    shutil.copy(os.path.join(base, "reel-%s" % nn, "assets", "voice.mp4"), "%s/reel-%s/assets/voice.mp4" % (ROOT, nn))
    for f in ("cut.json", "cut.txt", "words.json"):
        shutil.copy(os.path.join(base, "work", "r%s" % nn, f), "%s/work/r%s/%s" % (ROOT, nn, f))
    wd = "%s/work/r%s" % (ROOT, nn)
    p = subprocess.run([sys.executable, ROOT + "/tools/align.py", wd + "/words.json", wd + "/script.txt",
                        wd + "/captions.json"], capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    open(wd + "/align.txt", "w", encoding="utf-8").write(p.stdout + p.stderr)
    fr = subprocess.run(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v", "-show_entries",
                         "stream=nb_read_packets", "-of", "csv=p=0", "%s/reel-%s/assets/voice.mp4" % (ROOT, nn)],
                        capture_output=True, text=True).stdout.strip()
    moved = open(wd + "/cut.txt", encoding="utf-8").read().count(" -> ") - 1
    print("r%s: plate %s frames (DUR %.3f), align rc=%d, review lines %d, edges moved %d"
          % (nn, fr, (int(fr) - 0.5) / 30, p.returncode, p.stdout.count("REVIEW"), max(0, moved)))
