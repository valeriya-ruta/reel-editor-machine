# contact sheet of shoot.js frames:  python3 tools/sheet.py <outprefix> t1 t2 ... -> <outprefix>-sheet.jpg
import sys
from PIL import Image, ImageDraw
pre, ts = sys.argv[1], sys.argv[2:]
cols = min(4, len(ts)); rows = (len(ts) + cols - 1) // cols
W, H = 300, 533
c = Image.new("RGB", (W * cols, H * rows), "white")
for i, t in enumerate(ts):
    im = Image.open("%s-%s.png" % (pre, t)).convert("RGB").resize((W, H))
    ImageDraw.Draw(im).text((8, 8), t, fill=(255, 0, 0))
    c.paste(im, ((i % cols) * W, (i // cols) * H))
c.save(pre + "-sheet.jpg", quality=80)
