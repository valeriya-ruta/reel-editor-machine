#!/bin/sh
# Reel 12 mattes, strictly one after another.
cd /c/Users/Ruta/Desktop/reels-2026-09
for spec in "0.000 7.500 post" "17.950 24.800 room" "34.850 37.450 tada"; do
  set -- $spec
  echo "=== matte $3 $(date +%H:%M:%S)"
  python tools/matte.py reel-12 "$1" "$2" "$3" || echo "MATTE FAILED $3"
done
echo "=== mattes done $(date +%H:%M:%S)"
