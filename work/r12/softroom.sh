#!/bin/sh
# Reel 12 — the soft room behind her for b04's "behind" stretch (STYLE.md §0
# traps): blurring the plate itself smears her into a halo on moving footage,
# so each frame is blur(plate x (1-a)) / blur(1-a), with a = her matte. Her
# own pixels are filled from the room around her before the blur, and the
# matte on top puts her back sharp. Float precision: in 8-bit the divide
# rings dark just inside her edge, where the blurred mask is a level or two.
#   sh work/r12/softroom.sh      (after tools/matte.py reel-12 17.950 24.800 room)
cd /c/Users/Ruta/Desktop/reels-2026-09
F0=538; F1=745; SIGMA=26
mkdir -p reel-12/assets/soft
ffmpeg -v error -y -i reel-12/assets/base.mp4 -c:v libvpx-vp9 -i reel-12/assets/mattes/room.webm \
  -filter_complex "\
[0:v]trim=start_frame=$F0:end_frame=$F1,setpts=PTS-STARTPTS,format=gbrpf32le[p];\
[1:v]format=yuva420p,alphaextract,negate,format=gbrpf32le,split[m1][m2];\
[p][m1]blend=all_mode=multiply[pm];\
[pm]gblur=sigma=$SIGMA[pb];\
[m2]gblur=sigma=$SIGMA[mb];\
[pb][mb]blend=all_mode=divide,format=yuv420p[out]" \
  -map "[out]" -frames:v $((F1 - F0)) -an -c:v libx264 -crf 18 -preset veryfast -r 30 reel-12/assets/soft/room.mp4 \
  && ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames \
       -of default=nw=1:nk=1 reel-12/assets/soft/room.mp4
