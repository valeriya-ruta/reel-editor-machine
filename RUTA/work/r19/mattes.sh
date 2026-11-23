#!/bin/sh
# Reel 19 mattes + soft rooms, one heavy job at a time (work/heavy.sh).
#   hook   1.70-8.40   the carousel wall and the slop slides behind her (b01-b02)
#   slice 40.40-44.40  one long text sliced into slides behind her (b08)
# Soft room (STYLE.md §0 trap): blur(plate x (1-a)) / blur(1-a), a = her matte,
# so her silhouette never smears into a halo on moving footage.
cd /c/Users/Ruta/Desktop/reels-2026-09
SIGMA=26
mkdir -p reel-19/assets/soft
for spec in "1.702 8.400 hook" "40.402 44.400 slice"; do
  set -- $spec
  echo "=== matte $3 $(date +%H:%M:%S)"
  sh work/heavy.sh python tools/matte.py reel-19 "$1" "$2" "$3" 2>&1 | tr '\r' '\n' | grep -v "Frame [0-9]*/" || echo "MATTE FAILED $3"
done
for spec in "51 253 hook" "1212 1333 slice"; do
  set -- $spec
  F0=$1; F1=$2; N=$3
  echo "=== soft $N $(date +%H:%M:%S)"
  sh work/heavy.sh ffmpeg -v error -y -i reel-19/assets/base.mp4 -c:v libvpx-vp9 -i reel-19/assets/mattes/$N.webm \
    -filter_complex "\
[0:v]trim=start_frame=$F0:end_frame=$F1,setpts=PTS-STARTPTS,format=gbrpf32le[p];\
[1:v]format=yuva420p,alphaextract,negate,format=gbrpf32le,split[m1][m2];\
[p][m1]blend=all_mode=multiply[pm];\
[pm]gblur=sigma=$SIGMA[pb];\
[m2]gblur=sigma=$SIGMA[mb];\
[pb][mb]blend=all_mode=divide,format=yuv420p[out]" \
    -map "[out]" -frames:v $((F1 - F0)) -an -c:v libx264 -crf 18 -preset veryfast -r 30 reel-19/assets/soft/$N.mp4 \
    && ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames \
         -of default=nw=1:nk=1 reel-19/assets/soft/$N.mp4 || echo "SOFT FAILED $N"
done
echo "=== mattes done $(date +%H:%M:%S)"
