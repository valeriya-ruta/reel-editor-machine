#!/bin/sh
# Render cut plates one after another: sh work/b1021/plates.sh 42 43 44
cd "$(dirname "$0")/../.."
export CUT_MOTION=1 CUT_SCRATCH=/tmp/claude-0/-home-user-reel-editor-machine/cd246088-a040-50f5-93d6-6b9a5955beda/scratchpad/cut
for N in "$@"; do
  echo "=== r$N start $(date +%H:%M:%S)"
  python3 tools/cut.py "$N" --render 2>&1 | tail -2
  echo "=== r$N done $(date +%H:%M:%S)"
done
