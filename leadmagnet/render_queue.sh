#!/bin/bash
# Render every beat part whose index.html is newer than its out.mp4, then
# stitch a beat's parts into beats/<id>/out.mp4. Loops until beats/STOP.
cd "$(dirname "$0")/beats"
rm -f STOP
while [ ! -f STOP ]; do
  did=0
  for p in b*/parts/p*/; do
    p=${p%/}
    [ -f STOP ] && break
    if [ ! -f $p/out.mp4 ] || [ $p/index.html -nt $p/out.mp4 ]; then
      s=$(date +%s)
      (cd $p && npx --yes hyperframes@0.8.33 render -o out.tmp.mp4 --workers 4 --crf 17 > render.log 2>&1 && mv out.tmp.mp4 out.mp4) \
        && echo "rendered $p in $(( $(date +%s)-s ))s" || echo "FAILED $p"
      rm -rf $p/work-*
      did=1
    fi
  done
  for b in b*/; do
    b=${b%/}
    n=$(ls -d $b/parts/p* 2>/dev/null | wc -l); m=$(ls $b/parts/p*/out.mp4 2>/dev/null | wc -l)
    if [ "$n" -gt 0 ] && [ "$n" = "$m" ] && { [ ! -f $b/out.mp4 ] || [ -n "$(find $b/parts -name out.mp4 -newer $b/out.mp4)" ]; }; then
      ls $b/parts/p*/out.mp4 | sed "s|^|file '$PWD/|; s|$|'|" > $b/parts/list.txt
      ffmpeg -v error -y -f concat -safe 0 -i $b/parts/list.txt -c copy $b/out.mp4 && echo "stitched $b"
    fi
  done
  [ $did = 0 ] && sleep 10
done
echo "queue stopped"
