#!/bin/bash
# Render every reel part whose index.html is newer than its out.mp4; stitch
# each reel's parts into rNN/video.mp4. Loops until reels/STOP exists.
cd "$(dirname "$0")"
rm -f STOP
while [ ! -f STOP ]; do
  did=0
  for p in r0*/parts/p*/; do
    p=${p%/}; [ -f STOP ] && break
    [ -f ${p%/parts/*}/plate.mp4 ] || continue
    if [ ! -f $p/out.mp4 ] || [ $p/index.html -nt $p/out.mp4 ]; then
      s=$(date +%s)
      (cd $p && npx --yes hyperframes@0.8.33 render -o out.tmp.mp4 --workers 4 --crf 17 > render.log 2>&1 && mv out.tmp.mp4 out.mp4) \
        && echo "rendered $p in $(( $(date +%s)-s ))s" || echo "FAILED $p"
      rm -rf $p/work-*; did=1
    fi
  done
  for r in r0*/; do
    r=${r%/}
    n=$(ls -d $r/parts/p* 2>/dev/null | wc -l); m=$(ls $r/parts/p*/out.mp4 2>/dev/null | wc -l)
    if [ "$n" -gt 0 ] && [ "$n" = "$m" ] && { [ ! -f $r/video.mp4 ] || [ -n "$(find $r/parts -name out.mp4 -newer $r/video.mp4)" ]; }; then
      ls $r/parts/p*/out.mp4 | sed "s|^|file '$PWD/|; s|$|'|" > $r/parts/list.txt
      ffmpeg -v error -y -f concat -safe 0 -i $r/parts/list.txt -c copy $r/video.mp4 && echo "stitched $r"
    fi
  done
  [ $did = 0 ] && sleep 10
done
echo "queue stopped"
