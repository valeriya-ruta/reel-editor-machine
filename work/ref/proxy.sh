#!/bin/sh
S="/e/Content/From tg"
OUT="C:/Users/Ruta/Desktop/reels-2026-09/reel-life/assets/clips"
i=0
while IFS= read -r f; do
  i=$((i+1))
  n=$(printf "c%02d" $i)
  ffmpeg -v error -y -i "$S/$f" \
    -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30" \
    -c:v libx264 -preset veryfast -crf 21 -pix_fmt yuv420p -an \
    -movflags +faststart "$OUT/$n.mp4"
  echo "done $n  <- $f"
done < "C:/Users/Ruta/Desktop/reels-2026-09/work/ref/clips.txt"
echo "ALL PROXIES DONE"
