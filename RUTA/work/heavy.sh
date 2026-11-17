#!/bin/sh
# Serialise heavy jobs across parallel reel builds: sh work/heavy.sh <command...>
# (mattes, snapshots, hf check, ffmpeg passes). A mkdir lock, because Git Bash
# has no flock. A stale lock older than 45 min is broken automatically.
L=/c/Users/Ruta/Desktop/reels-2026-09/work/.heavy.lock
while ! mkdir "$L" 2>/dev/null; do
  if [ -n "$(find "$L" -maxdepth 0 -mmin +45 2>/dev/null)" ]; then rmdir "$L" 2>/dev/null; fi
  sleep 3
done
trap 'rmdir "$L" 2>/dev/null' EXIT INT TERM
"$@"
