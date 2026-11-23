#!/bin/sh
# Reel 15 mattes, strictly one after another, each under the shared heavy lock
# (reels 13 and 14 build in parallel — work/W40-brief.md §7).
#   contacts — b05, three contact cards float behind her head (21.85-27.25)
#   orbit    — b16, SendPulse's integrations ripple out behind her (72.90-79.00)
cd /c/Users/Ruta/Desktop/reels-2026-09
for spec in "21.850 27.250 contacts" "72.900 79.000 orbit"; do
  set -- $spec
  echo "=== matte $3 $(date +%H:%M:%S)"
  sh work/heavy.sh python tools/matte.py reel-15 "$1" "$2" "$3" || echo "MATTE FAILED $3"
done
echo "=== mattes done $(date +%H:%M:%S)"
