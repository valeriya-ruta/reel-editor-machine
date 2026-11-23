#!/bin/sh
# Reel 13 mattes, one heavy job at a time (work/heavy.sh), so a parallel
# build can interleave its own checks between them.
#   wall  12.40-18.60  the carousel wall behind her + the soft room under it
#   fan   54.10-56.70  five template slides fanned behind her head
cd /c/Users/Ruta/Desktop/reels-2026-09
for spec in "12.400 18.600 wall" "54.100 56.700 fan"; do
  set -- $spec
  echo "=== matte $3 $(date +%H:%M:%S)"
  sh work/heavy.sh python tools/matte.py reel-13 "$1" "$2" "$3" 2>&1 | tr '\r' '\n' | grep -v "Frame [0-9]*/" || echo "MATTE FAILED $3"
done
echo "=== mattes done $(date +%H:%M:%S)"
