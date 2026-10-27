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
# Each segment opens the plate on its own input: splitting one input into two
# trims makes ffmpeg buffer every frame up to the second trim (~20k raw 1080p
# frames) and the container runs out of memory.
T1S=$(python3 -c "print('%.6f' % ($F1/30))")
ffmpeg -nostdin -v error -stats -y -i $W/plate.mp4 -i $W/demo.mp4 -ss $T1S -i $W/plate.mp4 -filter_complex "
 [0:v]trim=start_frame=0:end_frame=$F0,setpts=PTS-STARTPTS[a];
 [1:v]setpts=PTS-STARTPTS[b];
 [2:v]setpts=PTS-STARTPTS[c];
 [a][b][c]concat=n=3:v=1:a=0,ass=$W/subs.ass:fontsdir=assets/fonts[v]" \
 -map "[v]" -map 0:a -c:v libx264 -crf 18 -preset fast -pix_fmt yuv420p -r 30 \
 -c:a aac -b:a 192k -movflags +faststart $W/UDC-tutorial.mp4
