#!/bin/sh
# Scaffold reel-NN for a cut plate: project files from the last reel that
# shipped (reel-40), fonts, underlay and grain — what work/prep.sh copied, for
# the cloud container's paths.   sh work/b1021/scaffold.sh 41 42 ...
set -e
cd "$(dirname "$0")/../.."
for N in "$@"; do
  mkdir -p "reel-$N/assets/fonts" "reel-$N/renders"
  cp reel-40/hyperframes.json reel-40/.hyperframesignore "reel-$N/"
  sed 's/reel-40/reel-'"$N"'/' reel-40/package.json > "reel-$N/package.json"
  printf '{ "id": "reel-%s", "name": "reel-%s" }' "$N" "$N" > "reel-$N/meta.json"
  cp reel-07/assets/fonts/*.woff assets/fonts/ProductSans-*.ttf "reel-$N/assets/fonts/"
  cp reel-07/assets/underlay.png assets/grain.png "reel-$N/assets/"
  echo "reel-$N scaffolded"
done
