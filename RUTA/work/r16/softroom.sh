#!/bin/sh
# Reel 16 — the soft room behind her for the two "behind" stretches (STYLE.md
# §0 traps). Same recipe as work/r12/softroom.sh: each frame is
# blur(plate x (1-a)) / blur(1-a), a = her matte, in float so the divide does
# not ring dark inside her edge; the matte on top puts her back sharp.
#   sh work/heavy.sh sh work/r16/softroom.sh     (after work/r16/mattes.sh)
cd /c/Users/Ruta/Desktop/reels-2026-09
mkdir -p reel-16/assets/soft
SIGMA=26
for spec in "87 292 hook" "1945 2125 segs"; do
  set -- $spec
  F0=$1; F1=$2; NAME=$3
  echo "=== soft $NAME $(date +%H:%M:%S)"
  ffmpeg -v error -y -i reel-16/assets/base.mp4 -c:v libvpx-vp9 -i reel-16/assets/mattes/$NAME.webm \
    -filter_complex "\
[0:v]trim=start_frame=$F0:end_frame=$F1,setpts=PTS-STARTPTS,format=gbrpf32le[p];\
[1:v]format=yuva420p,alphaextract,negate,format=gbrpf32le,split[m1][m2];\
[p][m1]blend=all_mode=multiply[pm];\
[pm]gblur=sigma=$SIGMA[pb];\
[m2]gblur=sigma=$SIGMA[mb];\
[pb][mb]blend=all_mode=divide,format=yuv420p[out]" \
    -map "[out]" -frames:v $((F1 - F0)) -an -c:v libx264 -crf 18 -preset veryfast -r 30 reel-16/assets/soft/$NAME.mp4 \
    && ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames \
         -of default=nw=1:nk=1 reel-16/assets/soft/$NAME.mp4
done
