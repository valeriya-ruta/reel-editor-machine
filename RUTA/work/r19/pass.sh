#!/bin/sh
# Reel 19 validation pass: build, check, then the snapshot sheet — each heavy
# step under the shared lock (work/heavy.sh).  sh work/r19/pass.sh "<times>"
cd /c/Users/Ruta/Desktop/reels-2026-09
(cd reel-19 && PYTHONIOENCODING=utf-8 python build.py)
echo "=== check $(date +%T)"
sh work/heavy.sh sh -c "cd reel-19 && ../hf check" 2>&1 | tr '\r' '\n' | sed 's/\x1b\[[0-9;]*m//g' | grep -a -v "^\s*$" | tail -60
echo "=== snapshot $(date +%T)"
rm -rf reel-19/study/snap
sh work/heavy.sh sh -c "cd reel-19 && ../hf snapshot --at '$1' --no-end --timeout 30000 --describe false -o study/snap" 2>&1 | tr '\r' '\n' | sed 's/\x1b\[[0-9;]*m//g' | grep -a -v "^\s*$" | tail -15
echo "=== pass done $(date +%T)"
