"""Cut a chibi pose off its white background into a transparent PNG.

    python scripts/cutout.py <raw.png> public/chibi/<pose>.png

The generator draws her on plain white with a closed dark-brown outline, so the
background is exactly the near-white region connected to the image border.
Whites inside the outline (the top, eye highlights, a question mark) are not
connected to the border and stay opaque. The anti-aliased rim is un-mixed from
white so the outline keeps its soft edge on any background.

All poses keep the generator's full canvas (head-top to knees), so swapping one
pose PNG for another keeps her scale and anchor without per-pose offsets.
"""
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

# A pixel is "paper" if every channel is this bright and it is nearly grey.
WHITE_MIN = 232
GREY_SPREAD = 22
# Width of the rim (px) whose alpha is recovered from how far it is from white.
RIM = 3
# Darkest value of the outline; a rim pixel this dark is fully opaque.
LINE = 70
# Output height. Her closest shot shows the canvas ~1600 px tall, so 1800 keeps
# her sharp without shipping the generator's 2528 px original.
HEIGHT = 1800


def cutout(src: str, dst: str) -> None:
    rgb = np.asarray(Image.open(src).convert("RGB")).astype(np.float32)
    lo = rgb.min(axis=2)
    hi = rgb.max(axis=2)
    paper = (lo >= WHITE_MIN) & ((hi - lo) <= GREY_SPREAD)

    labels, _ = ndimage.label(paper)
    edge = np.unique(np.concatenate([labels[0], labels[-1], labels[:, 0], labels[:, -1]]))
    edge = edge[edge != 0]
    bg = np.isin(labels, edge)
    # Close pin-holes the generator leaves in the outline's own anti-aliasing.
    bg = ndimage.binary_opening(bg, iterations=1)

    alpha = np.where(bg, 0.0, 1.0)
    rim = ndimage.binary_dilation(bg, iterations=RIM) & ~bg
    lum = rgb.mean(axis=2)
    rim_a = np.clip((255.0 - lum) / (255.0 - LINE), 0.0, 1.0)
    alpha[rim] = rim_a[rim]

    # Un-mix the rim from white: c = a*fg + (1-a)*255  ->  fg = (c - (1-a)*255) / a
    a3 = alpha[..., None]
    fg = np.where(a3 > 0.02, (rgb - (1.0 - a3) * 255.0) / np.maximum(a3, 1e-3), rgb)
    out = np.dstack([np.clip(fg, 0, 255), alpha * 255.0]).astype(np.uint8)
    im = Image.fromarray(out, "RGBA")
    if im.height > HEIGHT:
        # Resize premultiplied so the transparent white doesn't haze the outline.
        w = round(im.width * HEIGHT / im.height)
        im = im.convert("RGBa").resize((w, HEIGHT), Image.LANCZOS).convert("RGBA")
    im.save(dst, optimize=True)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    cutout(sys.argv[1], sys.argv[2])
