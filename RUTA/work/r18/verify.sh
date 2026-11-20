#!/bin/sh
# Reel 18 double check (W40-brief §5): review, check, snapshots — one lock hold.
cd /c/Users/Ruta/Desktop/reels-2026-09
AT="${AT:-0,1.9,3.0,5.4,6.3,9.3,11.0,16.4,20.1,21.8,22.5,23.5,24.4,25.9,27.6,28.9,31.5,33.8,34.7,35.7,36.4,36.9,37.4,38.8,40.8,42.3,45.2,46.6,48.0,50.0,51.6,52.5,53.8,56.4,58.6,60.4,61.2,63.3,64.6,66.5,67.5,69.0,70.4,70.55}"
echo "=== review $(date +%T)"; python tools/review.py reel-18
if [ -z "$NOCHECK" ]; then echo "=== check $(date +%T)"; (cd reel-18 && ../hf check); fi
echo "=== snap $(date +%T)"; rm -rf reel-18/study/snap; (cd reel-18 && ../hf snapshot --at "$AT" --no-end -o study/snap --describe false --timeout 20000)
echo "=== done $(date +%T)"
