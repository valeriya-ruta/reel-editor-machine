#!/bin/sh
# Reel 57 FULL 1: her current RUTA app, real screen recordings from ruta.media/ruta-app
# (app-screenshots/site-2026-11/), re-encoded constant 30 fps, keyframe every 15 frames,
# no audio, sped up where the slot is short:  name speed
cd "$(dirname "$0")/../.."
for p in "home 1" "braindump 2" "stories 1.5" "reel 2" "car-types 2"; do
  set -- $p
  ffmpeg -nostdin -v error -y -i app-screenshots/site-2026-11/vid-$1.mp4 -an \
    -vf "setpts=PTS/$2,fps=30" -c:v libx264 -crf 18 -preset medium -g 15 -keyint_min 15 -sc_threshold 0 \
    -pix_fmt yuv420p -movflags +faststart reel-57/assets/app/$1.mp4
  echo "$1 x$2 $(ffprobe -v error -count_packets -show_entries stream=nb_read_packets,r_frame_rate -of csv=p=0 reel-57/assets/app/$1.mp4)"
done
