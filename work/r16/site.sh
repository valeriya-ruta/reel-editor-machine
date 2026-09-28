#!/bin/sh
# Reel 16 — her client's landing page (work/media/r16/site-scroll.mp4, a phone
# screen recording, VFR) cut for the glass phone in the funnel takeover.
# The recording has no status bar or browser chrome; only the scrollbar at the
# right edge (x > 1056) and a strip under the sticky button are cropped.
#   out 0.00-1.40  the hero, 1x               (comp 18.45-19.85, on «сайт»)
#   out 1.40-3.30  src 1.40-6.50 at ~2.7x     («де розписано все про вебінар»)
#   out 3.30-4.00  src 6.50-7.20, 1x           («на сайті є кнопка»)
#   then frozen to 9.80 s (the phone docks and stays)
#   sh work/heavy.sh sh work/r16/site.sh
cd /c/Users/Ruta/Desktop/reels-2026-09
IN=work/media/r16/site-scroll.mp4
OUT=reel-16/assets
ffmpeg -v error -y -i $IN -filter_complex "\
[0:v]fps=30,crop=1056:1900:0:0,scale=540:972,setsar=1,split=3[a][b][c];\
[a]trim=0:1.4,setpts=PTS-STARTPTS[a1];\
[b]trim=1.4:6.5,setpts=(PTS-STARTPTS)/2.684[b1];\
[c]trim=6.5:7.2,setpts=PTS-STARTPTS[c1];\
[a1][b1][c1]concat=n=3:v=1:a=0,fps=30,tpad=stop_mode=clone:stop_duration=7,trim=duration=9.8,format=yuv420p[out]" \
  -map "[out]" -an -c:v libx264 -crf 17 -preset veryfast -movflags +faststart $OUT/site.mp4
ffmpeg -v error -y -ss 0.30 -i $IN -vf "crop=1056:1900:0:0,scale=540:972" -frames:v 1 -q:v 2 $OUT/site-hero.jpg
ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames,width,height,r_frame_rate \
  -of compact $OUT/site.mp4
# the host's photo off the landing page, for the webinar card
ffmpeg -v error -y -ss 17.3 -i $IN -vf "crop=780:780:147:696,scale=424:424" -frames:v 1 -q:v 2 $OUT/host.jpg
