#!/bin/sh
# Reel 18 matte, under the shared heavy lock (work/W40-brief.md §7).
#   her — b08-b10, the screen recording fills the frame and she is cut out
#         into the bottom-right corner (22.00-37.10, ~454 frames)
cd /c/Users/Ruta/Desktop/reels-2026-09
echo "=== matte her $(date +%H:%M:%S)"
sh work/heavy.sh python tools/matte.py reel-18 22.000 37.100 her || echo "MATTE FAILED her"
echo "=== mattes done $(date +%H:%M:%S)"
