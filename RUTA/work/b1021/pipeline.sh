#!/bin/sh
# Wait for any running plate queue, then plate + join-check each reel in turn.
#   sh work/b1021/pipeline.sh 45 46 ...      (join-checks already-plated reels too)
cd "$(dirname "$0")/../.."
while pgrep -f "plates.sh" >/dev/null; do sleep 10; done
for N in "$@"; do
  [ -f "reel-$N/assets/voice.mp4" ] || sh work/b1021/plates.sh "$N"
  python3 -I work/b1021/joincheck.py "$N" 2>&1 | grep -v -i warning
done
echo "PIPELINE DONE"
