#!/bin/bash
# Delivery encode for the Artifact page: 2-pass H.264 sized to fit an
# artifact version (<= ~240 MB), split into 14 MB chunks + parts.json.
set -e
SRC=${LM_SRC:-/home/user/lm-src}
D=$(dirname "$0")/delivery
cd "$SRC"
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 final.mp4)
VB=$(python3 -c "print(int((235*8*1024*1024/$DUR - 128000)/1000))")
echo "video bitrate ${VB}k for ${DUR}s"
ffmpeg -v error -stats -y -i final.mp4 -c:v libx264 -preset medium -b:v ${VB}k -pass 1 -passlogfile x264 -an -f mp4 /dev/null
ffmpeg -v error -stats -y -i final.mp4 -c:v libx264 -preset medium -b:v ${VB}k -pass 2 -passlogfile x264 -c:a aac -b:a 128k -movflags +faststart deliver.mp4
rm -f "$OLDPWD/$D"/chunk_* 2>/dev/null || true
cd "$OLDPWD"
split -b 14m -d -a 2 --additional-suffix=.mp4 "$SRC/deliver.mp4" "$D/chunk_"
python3 - "$D" "$SRC/deliver.mp4" <<'PY'
import json, os, sys
d, f = sys.argv[1], sys.argv[2]
parts = sorted(p for p in os.listdir(d) if p.startswith("chunk_"))
json.dump({"size": os.path.getsize(f), "parts": parts}, open(os.path.join(d, "parts.json"), "w"))
print(len(parts), "chunks", os.path.getsize(f) // 1048576, "MB")
PY
