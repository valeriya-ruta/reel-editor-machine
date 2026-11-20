#!/bin/sh
# Scaffold reel-NN for the Google x Excalidraw look (STYLE.md §0b).  sh work/b1120/scaffold.sh 45
set -e
N="$1"; cd "$(dirname "$0")/../.."
mkdir -p "reel-$N/assets/fonts" "reel-$N/renders"
cp reel-40/hyperframes.json "reel-$N/"
sed 's/reel-40/reel-'"$N"'/' reel-40/package.json > "reel-$N/package.json"
printf '{ "id": "reel-%s", "name": "reel-%s" }' "$N" "$N" > "reel-$N/meta.json"
printf 'study/\nrenders/\nassets/voice.mp4\nbuild.py\nsfx.json\nPLAN.md\n' > "reel-$N/.hyperframesignore"
cp assets/fonts/Excalifont.ttf assets/fonts/ProductSans-Bold.ttf assets/fonts/gsans/*.woff2 "reel-$N/assets/fonts/"
cp style-test/assets/underlay.png "reel-$N/assets/"
[ -d assets/sfx ] || REELS_SCRATCH=${REELS_SCRATCH:-work/scratch} python3 tools/sfx.py synth >/dev/null
echo "scaffolded reel-$N"
