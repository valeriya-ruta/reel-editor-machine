#!/bin/sh
# Scaffold reel NN from reel-00 and point it at its raw take.
#   sh tools/newreel.sh 01 raw/IMG_0861.MOV
# Adapted from Ruta's work/prep.sh (project skeleton copied from the last reel).
set -e
N="$1"; SRC="$2"
cd "$(dirname "$0")/.."
mkdir -p "work/r$N" "reel-$N/assets/fonts" "reel-$N/renders"
[ -n "$SRC" ] && printf '%s\n' "$SRC" > "work/r$N/SOURCE.txt"
for f in hyperframes.json .hyperframesignore; do cp "reel-00/$f" "reel-$N/"; done
sed 's/reel-00/reel-'"$N"'/' reel-00/package.json > "reel-$N/package.json"
printf '{ "id": "reel-%s", "name": "reel-%s" }' "$N" "$N" > "reel-$N/meta.json"
[ -f "reel-$N/build.py" ] || sed 's/^NN = "00"/NN = "'"$N"'"/' reel-00/build.py > "reel-$N/build.py"
cp assets/fonts/* "reel-$N/assets/fonts/"
[ -d assets/emoji ] && mkdir -p "reel-$N/assets/emoji" && cp assets/emoji/*.png "reel-$N/assets/emoji/" 2>/dev/null || true
echo "reel-$N ready. Next: python tools/utt.py $N"
