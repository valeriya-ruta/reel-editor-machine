# -*- coding: utf-8 -*-
"""Hand-fix individual caption tokens after align.py has done the hard part.

    python tools/patchcaps.py work/r07/captions.json work/r07/caption-patch.json

align.py binds script spelling to ASR timing and settles wording, but it works
on *blocks*. A stray punctuation token — a lone `?»,` where she improvised
inside a quotation, an orphaned opening guillemet — survives that, and at one
word per caption a stray token is a visible flash of garbage on screen.

The patch file is a list, matched by time so it survives a re-run of align:

    [{"at": 23.500, "drop": true},
     {"at": 22.540, "set": "«А"}]

`at` matches the caption whose start is within 60 ms. Anything that matches
nothing is reported rather than ignored, because a silently-skipped patch means
the reel ships with the garbage still in it.
"""
import io
import json
import sys

TOL = 0.060


def main():
    caps_path, patch_path = sys.argv[1], sys.argv[2]
    doc = json.load(io.open(caps_path, encoding="utf-8"))
    caps = doc["words"]
    patches = json.load(io.open(patch_path, encoding="utf-8"))

    out, applied, dropped = [], 0, 0
    hit = set()
    for c in caps:
        p = next((p for i, p in enumerate(patches)
                  if abs(p["at"] - c["s"]) < TOL and i not in hit), None)
        if p is not None:
            hit.add(patches.index(p))
            if p.get("drop"):
                dropped += 1
                continue
            print("  %7.3f  [%s] -> [%s]" % (c["s"], c["w"], p["set"]))
            c["w"] = p["set"]
            applied += 1
        out.append(c)

    missed = [p for i, p in enumerate(patches) if i not in hit]
    for p in missed:
        print("  !! no caption at %.3f — patch not applied" % p["at"])

    doc["words"] = out
    io.open(caps_path, "w", encoding="utf-8").write(
        json.dumps(doc, ensure_ascii=False, indent=1))
    print("patched %d, dropped %d, missed %d -> %d captions"
          % (applied, dropped, len(missed), len(out)))
    if missed:
        sys.exit(1)


main()
