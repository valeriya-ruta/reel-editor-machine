#!/bin/sh
# reel 20 validation pass: check, review, then the snapshot sheet, each under the heavy lock
#   sh work/r20/pass.sh [times]
cd /c/Users/Ruta/Desktop/reels-2026-09
AT=${1:-"0,1.5,3.5,5.4,6.5,7.2,8.9,9.9,11.4,14.0,16.0,18.6,20.2,21.3,23.4,25.0,27.8,30.0,31.8,32.9,34.2,35.5,36.8,39.2,41.8,43.5,46.8,48.2,50.7,53.6,55.5,57.5,59.0,61.0,62.6,64.2,66.2,67.4,69.1,70.8,72.4,73.5,74.3,74.9,76.5,79.8,82.8,83.3,85.3,89.8,93.0,93.93"}
OUT=${2:-snap}
echo "=== check $(date +%T)"
sh work/heavy.sh sh -c "cd reel-20 && ../hf check" 2>&1 | tr '\r' '\n' | grep -a -v "^\s*$" | tail -40
echo "=== review $(date +%T)"
sh work/heavy.sh sh -c "PYTHONIOENCODING=utf-8 python tools/review.py reel-20" 2>&1 | tail -40
echo "=== snapshot $(date +%T)"
rm -rf reel-20/study/$OUT
sh work/heavy.sh sh -c "cd reel-20 && ../hf snapshot --at $AT -o study/$OUT" 2>&1 | tr '\r' '\n' | grep -a -v "^\s*$" | tail -15
echo "=== pass done $(date +%T)"
