#!/bin/sh
# Render every animation window of reel 41 locally, two at a time.
# (A window is a few seconds; the whole set is ~3 min of graphics.)
cd "$(dirname "$0")/../../demo/w" || exit 1
ls -d */ | tr -d / | xargs -P 2 -I{} sh -c 'cd {} && npx --yes hyperframes@0.8.33 render -o renders/out.mp4 --quiet --workers 2 > render.log 2>&1 && echo "done {}" || echo "FAILED {}"'
