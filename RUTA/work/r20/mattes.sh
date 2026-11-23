#!/bin/sh
# Reel 20 mattes, one heavy job at a time (work/heavy.sh).
#   her0  0.00-7.50   shot 0: her on top of the clones (b01); the same clip is
#                     the clone/twin source for every later twin beat
#   tw2   81.00-83.80 her on top of the one clone that flickers in (b19)
cd /c/Users/Ruta/Desktop/reels-2026-09
for spec in "0.000 7.500 her0" "81.000 83.800 tw2"; do
  set -- $spec
  echo "=== matte $3 $(date +%H:%M:%S)"
  sh work/heavy.sh python tools/matte.py reel-20 "$1" "$2" "$3" 2>&1 | tr '\r' '\n' | grep -v "Frame [0-9]*/" || echo "MATTE FAILED $3"
done
echo "=== mattes done $(date +%H:%M:%S)"
