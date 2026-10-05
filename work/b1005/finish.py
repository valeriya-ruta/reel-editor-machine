# -*- coding: utf-8 -*-
"""Finish reels once their cloud plates exist: download the plate artifact,
swap it in, re-mix the sound, rebuild, render on HeyGen, verify, deliver.

    python work/b1005/finish.py <plate-run-id> 23 24 26 ...

Nothing heavy runs locally: the plate came from GitHub (plate.yml), the render
from HeyGen (tools/hfrender.py). The mix is an audio pass with the video copied.
"""
import json
import os
import shutil
import subprocess
import sys

ROOT = "C:/Users/Ruta/Desktop/reels-2026-09"
REPO = "valeriya-ruta/reel-editor-machine"
DELIVER = "C:/Users/Ruta/Desktop/Reels 5-11 Oct"
ARCHIVE = "E:/Reels archive"


def sh(cmd, cwd=ROOT):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def frames(path):
    rc, out = sh(["ffprobe", "-v", "error", "-count_packets", "-select_streams", "v",
                  "-show_entries", "stream=nb_read_packets", "-of", "csv=p=0", path])
    return int(out.strip().splitlines()[0])


def main():
    run = sys.argv[1]
    dl = "E:/reels-work/plates-%s" % run
    if not os.path.isdir(dl):
        rc, out = sh(["gh", "run", "download", run, "--repo", REPO, "-D", dl])
        if rc:
            sys.exit("download failed: " + out[-300:])
    for nn in sys.argv[2:]:
        art = [d for d in os.listdir(dl) if d.startswith("plate-%s-" % nn)]
        if not art:
            print("r%s: no plate artifact" % nn)
            continue
        base = os.path.join(dl, art[0])
        new_voice = os.path.join(base, "reel-%s" % nn, "assets", "voice.mp4")
        new_cut = json.load(open(os.path.join(base, "work", "r%s" % nn, "cut.json"), encoding="utf-8"))
        old_cut = json.load(open(os.path.join(ROOT, "work", "r%s" % nn, "cut.json"), encoding="utf-8"))
        same = [(c["src_in"], c["frames"]) for c in new_cut["clips"]] == \
               [(c["src_in"], c["frames"]) for c in old_cut["clips"]]
        nf = frames(new_voice)
        print("r%s: plate %d frames, timeline %s" % (nn, nf, "unchanged" if same else "CHANGED"))
        if not same:
            print("   skipping — timeline differs, needs a look")
            continue
        reel = os.path.join(ROOT, "reel-%s" % nn)
        shutil.copyfile(new_voice, os.path.join(reel, "assets", "voice.mp4"))
        rc, out = sh(["python", os.path.join(ROOT, "tools", "sfx.py"), "mix", nn])
        if rc:
            print("   mix failed: " + out[-300:]); continue
        rc, out = sh(["python", "build.py"], cwd=reel)
        if rc:
            print("   build failed: " + out[-300:]); continue
        if len(sys.argv) > 2 and os.environ.get("NO_RENDER"):
            continue
        old = os.path.join(reel, "renders", "REEL-%s.mp4" % nn)
        if os.path.exists(old):
            os.replace(old, old.replace(".mp4", "-prev.mp4"))
        rc, out = sh(["python", os.path.join(ROOT, "tools", "hfrender.py"), "reel-%s" % nn])
        print("   " + out.strip().replace("\n", "\n   "))
        if rc or not os.path.exists(old):
            continue
        rf = frames(old)
        rc2, vol = sh(["ffmpeg", "-nostdin", "-i", old, "-vn", "-af", "volumedetect", "-f", "null", "-"])
        mean = [l for l in vol.splitlines() if "mean_volume" in l]
        ok = abs(rf - nf) <= 1 and mean
        print("   render %d frames vs plate %d, %s -> %s" % (rf, nf, mean[0].split("]")[-1].strip() if mean else "NO AUDIO",
                                                         "OK" if ok else "CHECK"))
        if ok:
            shutil.copyfile(old, os.path.join(DELIVER, "REEL-%s.mp4" % nn))
            shutil.copyfile(old, os.path.join(ARCHIVE, "REEL-%s.mp4" % nn))
            print("   delivered")


if __name__ == "__main__":
    main()
