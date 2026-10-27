#!/bin/bash
# UDC tutorial: plate -> demo (4 parallel chunks) -> plate|demo|plate + subtitles -> final.
# Run from the repo root. Spans and frame numbers come from work/r41/demo.json.
set -e
W=work/r41
read T0 T1 <<<"$(python3 -c "import json;d=json.load(open('$W/demo.json'));print(d['t0'],d['t1'])")"
F0=$(python3 -c "print(round($T0*30))"); F1=$(python3 -c "print(round($T1*30))")
N=$((F1 - F0)); C=$(( (N + 3) / 4 ))

if [ ! -f $W/demo.mp4 ]; then
  for i in 0 1 2 3; do
    a=$((i * C)); b=$(( (i + 1) * C )); [ $b -gt $N ] && b=$N
    python3 tools/demo.py $W/demo.json $W/plate.mp4 $W/demo_$i.mp4 $a $b > $W/demo_$i.log 2>&1 &
  done
  wait
  printf "file '%s'\n" "$PWD/$W/demo_0.mp4" "$PWD/$W/demo_1.mp4" "$PWD/$W/demo_2.mp4" "$PWD/$W/demo_3.mp4" > $W/demo_list.txt
  ffmpeg -nostdin -v error -y -f concat -safe 0 -i $W/demo_list.txt -c copy $W/demo.mp4
fi

# picture: plate before the demo, the demo, plate after it; sound: the plate throughout.
# Each piece is encoded on its own with the subtitles burned at its real
# timeline offset, then the pieces are joined without re-encoding. (One
# filter graph with concat decodes all inputs at once and buffers the idle
# ones until the container runs out of memory — twice, at ~9 min.)
T0S=$(python3 -c "print('%.6f' % ($F0/30))"); T1S=$(python3 -c "print('%.6f' % ($F1/30))")
X="-c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p -fps_mode passthrough -an"
SUB="ass=$W/subs.ass:fontsdir=assets/fonts"
ffmpeg -nostdin -v error -y -i $W/plate.mp4 -frames:v $F0 -vf "$SUB" $X $W/p_a.mp4 &
ffmpeg -nostdin -v error -y -i $W/demo.mp4 -vf "setpts=PTS-STARTPTS+$T0S/TB,$SUB,setpts=PTS-STARTPTS" $X $W/p_b.mp4 &
ffmpeg -nostdin -v error -y -ss $T1S -i $W/plate.mp4 -vf "setpts=PTS-STARTPTS+$T1S/TB,$SUB,setpts=PTS-STARTPTS" $X $W/p_c.mp4 &
wait
printf "file '%s'\n" "$PWD/$W/p_a.mp4" "$PWD/$W/p_b.mp4" "$PWD/$W/p_c.mp4" > $W/final_list.txt
ffmpeg -nostdin -v error -y -f concat -safe 0 -i $W/final_list.txt -i $W/plate.mp4 -map 0:v -map 1:a \
 -c:v copy -c:a aac -b:a 192k -movflags +faststart $W/UDC-tutorial.mp4
