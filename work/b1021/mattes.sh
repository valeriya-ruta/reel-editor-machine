#!/bin/sh
# Cut every matte a reel's index.html asks for, one after another, skipping
# those already made:   sh work/b1021/mattes.sh 41
cd "$(dirname "$0")/../.."
for N in "$@"; do
  python3 - "$N" <<'PY' | while read name a b; do
import re, sys
h = open("reel-%s/index.html" % sys.argv[1], encoding="utf-8").read()
for m in re.finditer(r'id="matte-(\w+)"[^>]*?data-start="([\d.]+)" data-duration="([\d.]+)"', h, re.S):
    s, d = float(m.group(2)), float(m.group(3))
    # +1 ms: matte.py floors start*fps, and f0/30*30 can land a hair under f0
    print(m.group(1), "%.4f" % (s + 0.001), "%.4f" % (s + d - 1 / 30.0))
PY
    if [ -f "reel-$N/assets/mattes/$name.webm" ]; then echo "r$N $name: have it"; continue; fi
    echo "=== r$N $name $a-$b start $(date +%H:%M:%S)"
    # stdin from /dev/null: npx would otherwise eat the rest of this loop's list;
    # the progress bar goes to a log, only the summary line comes back
    mkdir -p work/r$N/mattelog
    python3 tools/matte.py "reel-$N" "$a" "$b" "$name" < /dev/null > "work/r$N/mattelog/$name.log" 2>&1
    tr '\r' '\n' < "work/r$N/mattelog/$name.log" | grep -E "Removed background|! asked|failed" | tail -2
  done
done
echo "MATTES DONE"
