#!/bin/sh
# Reel 17 mattes, one heavy job at a time (work/heavy.sh), so a parallel
# build can interleave its own checks between them.
#   wall    0.00-5.60   her reels on a wall behind her + the soft room (b01-b02)
#   drafts 15.20-20.07  the Drafts folder, reels flying out of it (b07); ends
#                       one frame before her 20.10 cut
cd /c/Users/Ruta/Desktop/reels-2026-09
for spec in "0.000 5.600 wall" "15.200 20.066 drafts"; do
  set -- $spec
  echo "=== matte $3 $(date +%H:%M:%S)"
  sh work/heavy.sh python tools/matte.py reel-17 "$1" "$2" "$3" 2>&1 | tr '\r' '\n' | grep -v "Frame [0-9]*/" || echo "MATTE FAILED $3"
done
echo "=== mattes done $(date +%H:%M:%S)"
echo "=== softroom $(date +%H:%M:%S)"
sh work/heavy.sh sh work/r17/softroom.sh
echo "=== softroom done $(date +%H:%M:%S)"
