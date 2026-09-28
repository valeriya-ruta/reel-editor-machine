#!/bin/sh
# Reel 17 — the soft room behind the wall (b01) and the Drafts folder (b07).
# STYLE.md §0 trap: blurring the plate smears her into a halo on moving
# footage, so each frame is blur(plate x (1-a)) / blur(1-a) with a = her
# matte, in float. Her own pixels are filled from the room around her; the
# matte on top puts her back.
#   sh work/heavy.sh sh work/r17/softroom.sh   (after both mattes)
cd /c/Users/Ruta/Desktop/reels-2026-09
SIGMA=26
mkdir -p reel-17/assets/soft
for spec in "0 169 wall" "456 603 drafts"; do
  set -- $spec
  F0=$1; F1=$2; N=$3
  ffmpeg -v error -y -i reel-17/assets/base.mp4 -c:v libvpx-vp9 -i reel-17/assets/mattes/$N.webm \
    -filter_complex "\
[0:v]trim=start_frame=$F0:end_frame=$F1,setpts=PTS-STARTPTS,format=gbrpf32le[p];\
[1:v]format=yuva420p,alphaextract,negate,format=gbrpf32le,split[m1][m2];\
[p][m1]blend=all_mode=multiply[pm];\
[pm]gblur=sigma=$SIGMA[pb];\
[m2]gblur=sigma=$SIGMA[mb];\
[pb][mb]blend=all_mode=divide,format=yuv420p[out]" \
    -map "[out]" -frames:v $((F1 - F0)) -an -c:v libx264 -crf 18 -preset veryfast -r 30 reel-17/assets/soft/$N.mp4 \
    && echo "soft $N frames: $(ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames \
         -of default=nw=1:nk=1 reel-17/assets/soft/$N.mp4)"
done
