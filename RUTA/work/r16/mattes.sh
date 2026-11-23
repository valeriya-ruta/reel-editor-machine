#!/bin/sh
# Reel 16 mattes, strictly one after another, each under the heavy lock.
#   hook  2.90-9.70   the contact card + three sources behind her as she walks in
#   segs  64.85-70.80 the crowd of cards sorting into columns behind her
cd /c/Users/Ruta/Desktop/reels-2026-09
for spec in "2.900 9.700 hook" "64.850 70.800 segs"; do
  set -- $spec
  echo "=== matte $3 $(date +%H:%M:%S)"
  sh work/heavy.sh python tools/matte.py reel-16 "$1" "$2" "$3" || echo "MATTE FAILED $3"
done
echo "=== mattes done $(date +%H:%M:%S)"
