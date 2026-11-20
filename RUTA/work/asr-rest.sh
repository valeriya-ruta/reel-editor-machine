#!/bin/sh
# The remaining four reels, serially. STYLE.md §7: never two heavy local jobs at
# once — but a cloud render is network-bound, so this is free time on the CPU.
PY=/c/Users/Ruta/AppData/Local/Programs/Python/Python313/python.exe
cd /c/Users/Ruta/Desktop/reels-2026-09
for n in r06 r08 r09 r10; do
  if [ -f work/$n/words.json ]; then
    echo "=== $n already done, skipping"
    continue
  fi
  echo "=== $n start $(date +%H:%M:%S)"
  "$PY" tools/asr.py work/$n/audio.wav work/$n/words.json medium 2>&1 | tail -1
  echo "=== $n done  $(date +%H:%M:%S)"
done
echo "ALL REMAINING ASR DONE"
