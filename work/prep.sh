#!/bin/sh
# Prepare one reel's plate and its no-paint analysis.
#   sh work/prep.sh 08
#
# Everything here is heavy and sequential on purpose (STYLE.md §7): the plate
# rescale, then the two detectors that read it. Run one reel at a time.
set -e
N="$1"
cd /c/Users/Ruta/Desktop/reels-2026-09
SRC=$(cat "work/r$N/SOURCE.txt")
mkdir -p "reel-$N/assets/fonts" "reel-$N/assets/logos" "reel-$N/renders"

# project skeleton, copied from the last reel that shipped
cp reel-07/hyperframes.json "reel-$N/"
sed 's/reel-07/reel-'"$N"'/' reel-07/package.json > "reel-$N/package.json"
printf '{ "id": "reel-%s", "name": "reel-%s" }' "$N" "$N" > "reel-$N/meta.json"
cp reel-07/assets/fonts/*.woff "reel-$N/assets/fonts/"
cp reel-07/assets/underlay.png "reel-$N/assets/"
# refined glass (STYLE.md §0, tools/glass.py): the lighter Product Sans cuts
# the cards need, and the grain the burgundy ground needs against banding
cp assets/fonts/ProductSans-*.ttf "reel-$N/assets/fonts/"
cp assets/grain.png "reel-$N/assets/"

echo "=== plate  $(date +%H:%M:%S)"
ffmpeg -nostdin -v error -y -i "$SRC" \
  -vf "scale=1080:1920:flags=lanczos" -r 30 \
  -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p \
  -c:a aac -b:a 192k "reel-$N/assets/base.mp4"

FRAMES=$(ffprobe -v error -count_frames -select_streams v \
  -show_entries stream=nb_read_frames -of default=nw=1:nk=1 "reel-$N/assets/base.mp4")
echo "PLATE FRAMES $FRAMES"
python -c "print('DUR = %.3f   # %s plate frames / 30' % (($FRAMES-0.5)/30.0, $FRAMES))"

echo "=== shots  $(date +%H:%M:%S)"
python tools/shots.py "reel-$N"
echo "=== pullouts  $(date +%H:%M:%S)"
python tools/pullouts.py "reel-$N"
echo "PREP DONE $(date +%H:%M:%S)"
