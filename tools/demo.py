# -*- coding: utf-8 -*-
"""Screen demo, tutorial style: her screenshots play as a smooth live demo while
she talks, and she sits in a rounded box beside them.

    python tools/demo.py <spec.json> <plate.mp4> <out.mp4>

Her direction, 2026-10-27 (STYLE.md "Screen demos are tutorial style"):
smooth ease in and out, a BIG cursor so it is obvious where she clicks, every
unnecessary or personal detail blurred, the pressed button ringed in a
hand-drawn (Excalidraw-style) stroke, and her in a rectangle framed wide —
head and shoulders with headroom, never cropped at the top.

The spec (times are on the plate's own timeline, seconds):

    {"t0": 120.0, "t1": 260.0,            # the span this renders
     "shots": [{"img": "claude-home.png", "at": 121.0,
                "steps": [{"at": 123.4, "target": "customize", "click": true,
                           "zoom": 1.3}]}, ...]}

Click targets and blur rects come from app-screenshots/claude-demo.json. The
renderer reads the plate for the span (her, full frame), so the way in and the
way out are one continuous move: she shrinks into the box as the screen rises,
and grows back to full frame when it leaves.
"""
import json
import math
import os
import random
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOTS = os.path.join(ROOT, "app-screenshots")
W, H, FPS = 1920, 1080, 30

# layout: the screen big on the left, her box on the right. Nothing below
# y ~ 860 but the subtitle line, and that ends 120 px above the bottom: her
# note, 2026-10-27 — "not too low otherwise they will be hidden by the YT
# line" (YouTube's progress bar and controls).
CARD = (52, 56, 1296, 810)          # x, y, w, h  (screenshots are ~1.6:1)
CARD_R = 26
PIP = (1408, 298, 456, 570)         # 4:5, waist-up from the full source height
PIP_R = 30
# her crop inside the 16:9 plate: full height, 4:5 wide, centred on her
PIP_SRC = (0.5, 0.5)                 # centre of the crop, as a fraction of the plate

RING = (224, 32, 75)                 # brand red #e0204b
INTRO, OUTRO = 0.9, 0.8              # the shrink into the box / the grow back
XFADE = 0.55                         # one screenshot to the next
MOVE = 0.75                          # cursor travel to a target


# ---------------------------------------------------------------- easing

def ease(x):
    """easeInOutCubic — every move starts and lands softly."""
    x = min(max(x, 0.0), 1.0)
    return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def ease_out(x):
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** 3


def lerp(a, b, t):
    return a + (b - a) * t


# ---------------------------------------------------------------- assets

def load_shot(name, spec):
    im = Image.open(os.path.join(SHOTS, name)).convert("RGB")
    for x, y, w, h in spec.get("blur", []):
        box = (x, y, x + w, y + h)
        im.paste(im.crop(box).filter(ImageFilter.GaussianBlur(10)), box)
    return im


def rounded_mask(w, h, r, ss=4):
    m = Image.new("L", (w * ss, h * ss), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w * ss - 1, h * ss - 1), r * ss, fill=255)
    return m.resize((w, h), Image.LANCZOS)


def shadow(w, h, r, blur=34, alpha=95, spread=6):
    pad = blur * 3
    s = Image.new("L", (w + 2 * pad, h + 2 * pad), 0)
    ImageDraw.Draw(s).rounded_rectangle((pad - spread, pad - spread + 14, pad + w + spread, pad + h + spread + 14),
                                        r + spread, fill=alpha)
    return s.filter(ImageFilter.GaussianBlur(blur)), pad


def background():
    """A calm warm ground — her off-white with a breath of pink at the corners."""
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    base = np.array([242, 240, 241], np.float32)
    pink = np.array([255, 214, 226], np.float32)
    d1 = np.exp(-(((x - 1820) / 900) ** 2 + ((y - 60) / 600) ** 2))
    d2 = np.exp(-(((x - 120) / 800) ** 2 + ((y - 1060) / 520) ** 2)) * 0.7
    k = np.clip(d1 + d2, 0, 1)[..., None]
    img = base * (1 - k) + pink * k
    rng = np.random.default_rng(7)
    img += rng.normal(0, 1.6, (H, W, 1))
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))


def cursor_sprite(h=78):
    """A big arrow: white body, near-black outline, soft shadow."""
    ss = 4
    pts = [(0, 0), (0, 17.0), (4.3, 13.2), (7.1, 19.6), (10.2, 18.3), (7.4, 12.1), (13.2, 12.1)]
    sc = h * ss / 20.0
    P = [(x * sc + 6 * ss, y * sc + 6 * ss) for x, y in pts]
    size = (int(14.5 * sc + 14 * ss), int(20.5 * sc + 14 * ss))
    im = Image.new("RGBA", size, (0, 0, 0, 0))
    sh = Image.new("L", size, 0)
    ImageDraw.Draw(sh).polygon([(x + 3 * ss, y + 5 * ss) for x, y in P], fill=110)
    sh = sh.filter(ImageFilter.GaussianBlur(5 * ss))
    im.paste((0, 0, 0, 255), (0, 0), sh)
    d = ImageDraw.Draw(im)
    d.polygon(P, fill=(255, 255, 255, 255))
    d.line(P + [P[0]], fill=(23, 20, 28, 255), width=int(1.35 * ss * h / 40), joint="curve")
    im = im.resize((size[0] // ss, size[1] // ss), Image.LANCZOS)
    return im, (6, 6)                       # the hotspot, in sprite pixels


def rough_ring(cx, cy, rx, ry, seed):
    """Two loose passes round the target, like a marker ring in Excalidraw:
    not closed, a little overshoot, a little wobble."""
    rnd = random.Random(seed)
    passes = []
    for p in range(2):
        a0 = rnd.uniform(-2.6, -1.9)
        span = 2 * math.pi + rnd.uniform(0.25, 0.5)
        ox, oy = rnd.uniform(-4, 4), rnd.uniform(-3, 3)
        sx, sy = 1 + rnd.uniform(-0.05, 0.07), 1 + rnd.uniform(-0.06, 0.08)
        ph1, ph2 = rnd.uniform(0, 6.28), rnd.uniform(0, 6.28)
        pts = []
        n = 90
        for i in range(n + 1):
            u = i / n
            a = a0 + span * u
            wob = 1 + 0.035 * math.sin(3 * a + ph1) + 0.02 * math.sin(5 * a + ph2)
            r_grow = 1 + 0.06 * u                       # the second lap drifts out a touch
            pts.append((cx + ox + rx * sx * wob * r_grow * math.cos(a),
                        cy + oy + ry * sy * wob * r_grow * math.sin(a)))
        passes.append(pts)
    return passes


# ---------------------------------------------------------------- the camera

class Shot:
    def __init__(self, d, catalog):
        self.name = d["img"]
        spec = catalog[self.name]
        self.img = load_shot(self.name, spec)
        self.targets = spec["targets"]
        self.at = d["at"]
        self.steps = sorted(d.get("steps", []), key=lambda s: s["at"])
        self.cam0 = tuple(d.get("cam", (0.5, 0.5, 1.0)))   # focus x, focus y (fractions), zoom

    def target_centre(self, name):
        x, y, w, h = self.targets[name]
        return x + w / 2.0, y + h / 2.0

    def cam(self, t):
        """Focus point and zoom: eases toward each step's target as the cursor
        travels there; a step without zoom keeps the overview."""
        iw, ih = self.img.size
        fx, fy, z = self.cam0[0] * iw, self.cam0[1] * ih, self.cam0[2]
        for s in self.steps:
            tz = s.get("zoom")
            if tz is None:
                continue
            gx, gy = self.target_centre(s["target"])
            start = s["at"] - MOVE - 0.35
            k = ease((t - start) / (MOVE + 0.35))
            fx, fy, z = lerp(fx, gx, k), lerp(fy, gy, k), lerp(z, tz, k)
            if "release" in s:                        # zoom back out after the click
                k2 = ease((t - s["release"]) / 0.7)
                fx, fy = lerp(fx, self.cam0[0] * iw, k2), lerp(fy, self.cam0[1] * ih, k2)
                z = lerp(z, self.cam0[2], k2)
        return fx, fy, z

    def view(self, t, w, h):
        """The screenshot as seen through the card at time t, w x h pixels."""
        iw, ih = self.img.size
        fx, fy, z = self.cam(t)
        s = min(w / iw, h / ih) * z                   # screen px per image px
        vw, vh = w / s, h / s
        x0 = min(max(fx - vw / 2, 0), iw - vw) if vw < iw else (iw - vw) / 2
        y0 = min(max(fy - vh / 2, 0), ih - vh) if vh < ih else (ih - vh) / 2
        out = self.img.transform((w, h), Image.AFFINE, (1 / s, 0, x0, 0, 1 / s, y0),
                                 resample=Image.BICUBIC, fillcolor=(250, 249, 247))
        return out, (x0, y0, s)


# ---------------------------------------------------------------- render

def plate_frames(plate, t0, n):
    p = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-ss", "%.4f" % t0, "-i", plate,
                          "-frames:v", str(n), "-an", "-vf", "scale=%d:%d" % (W, H),
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    fb = W * H * 3
    for _ in range(n):
        b = p.stdout.read(fb)
        if len(b) < fb:
            break
        yield Image.frombytes("RGB", (W, H), b)
    p.stdout.close()
    p.wait()


def main():
    spec = json.load(open(sys.argv[1], encoding="utf-8"))
    plate, out = sys.argv[2], sys.argv[3]
    catalog = json.load(open(os.path.join(SHOTS, "claude-demo.json"), encoding="utf-8"))
    shots = [Shot(d, catalog) for d in spec["shots"]]
    t0, t1 = spec["t0"], spec["t1"]
    n = int(round((t1 - t0) * FPS))

    bg = background()
    cx, cy, cw, ch = CARD
    card_mask = rounded_mask(cw, ch, CARD_R)
    card_sh, card_pad = shadow(cw, ch, CARD_R)
    px, py, pw, ph = PIP
    cur, hot = cursor_sprite()

    # every step on one list, with the shot it belongs to
    steps = []
    for si, s in enumerate(shots):
        for st in s.steps:
            steps.append((st["at"], si, st))
    steps.sort(key=lambda x: x[0])

    def shot_at(t):
        i = 0
        for k, s in enumerate(shots):
            if t >= s.at:
                i = k
        return i

    enc = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
                            "-s", "%dx%d" % (W, H), "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "17",
                            "-preset", "medium", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)

    for f, her in enumerate(plate_frames(plate, t0, n)):
        t = t0 + f / FPS
        k_in = ease((t - t0) / INTRO)
        k_out = ease((t1 - t) / OUTRO)
        k = min(k_in, k_out)                           # 0 = her full frame, 1 = the demo layout

        frame = bg.copy() if k > 0 else her.copy()
        if k > 0:
            # --- the screen card: rises and sharpens in, sinks out
            si = shot_at(t)
            view, (x0, y0, sc) = shots[si].view(t, cw, ch)
            # cross-fade from the previous shot
            if si > 0 and t - shots[si].at < XFADE:
                pv, _ = shots[si - 1].view(t, cw, ch)
                view = Image.blend(pv, view, ease((t - shots[si].at) / XFADE))
            off = int(lerp(70, 0, k))
            a = int(255 * k)
            cm = card_mask if a == 255 else card_mask.point(lambda v: v * a // 255)
            shm = card_sh if a == 255 else card_sh.point(lambda v: v * a // 255)
            frame.paste((60, 20, 32), (cx - card_pad, cy - card_pad + off), shm)
            # the ring and the cursor are drawn on the card, so they ride the camera
            layer = view.convert("RGBA")
            d = ImageDraw.Draw(layer)
            for at, sj, st in steps:
                if sj != si or t < at - 0.05:
                    continue
                end = st.get("ring_end", at + 2.4)
                if not st.get("ring", True) or t > end + 0.35:
                    continue
                tx, ty, tw, th = shots[sj].targets[st["target"]]
                rx = (tw / 2 + 14) * sc
                ry = (th / 2 + 12) * sc
                ccx = (tx + tw / 2 - x0) * sc
                ccy = (ty + th / 2 - y0) * sc
                prog = ease_out((t - at + 0.05) / 0.55)
                fade = 1 - ease((t - end) / 0.35)
                col = RING + (int(255 * fade),)
                for pi, pts in enumerate(rough_ring(ccx, ccy, rx, ry, hash(st["target"]) & 0xffff)):
                    pp = min(max(prog * 1.6 - pi * 0.6, 0), 1)
                    m = max(2, int(len(pts) * pp))
                    if pp > 0:
                        d.line(pts[:m], fill=col, width=max(4, int(5.5 * min(sc, 1.6))), joint="curve")
            # cursor: travels to each target, presses on the click
            pos = None
            for at, sj, st in steps:
                if sj != si:
                    continue
                gx, gy = shots[sj].target_centre(st["target"])
                # land low-right of centre so the tip does not cover the label
                _, _, tw_, th_ = shots[sj].targets[st["target"]]
                gx += st.get("dx", min(tw_ * 0.3, 28))
                gy += st.get("dy", th_ * 0.3)
                if pos is None:
                    pos = st.get("from", (gx + 160, gy + 120))
                if t >= at - MOVE:
                    u = ease((t - (at - MOVE)) / MOVE)
                    pos = (lerp(pos[0], gx, u), lerp(pos[1], gy, u))
            if pos is not None:
                press = 1.0
                for at, sj, st in steps:
                    if sj == si and st.get("click", True) and 0 <= t - at < 0.28:
                        press = 1 - 0.18 * math.sin(math.pi * (t - at) / 0.28)
                        rr = 10 + 46 * ease_out((t - at) / 0.28)
                        sx, sy = (pos[0] - x0) * sc, (pos[1] - y0) * sc
                        d.ellipse((sx - rr, sy - rr, sx + rr, sy + rr),
                                  outline=RING + (int(200 * (1 - (t - at) / 0.28)),), width=5)
                cs = cur if press == 1.0 else cur.resize((int(cur.width * press), int(cur.height * press)), Image.LANCZOS)
                sx, sy = (pos[0] - x0) * sc - hot[0] * press, (pos[1] - y0) * sc - hot[1] * press
                layer.alpha_composite(cs, (int(sx), int(sy)))
            frame.paste(layer.convert("RGB"), (cx, cy + off), cm)

        # --- her: full frame shrinking into the box (or the box growing back)
        if k > 0:
            sw, sh_ = her.size
            # the box crop: full height, 4:5 wide, centred on her
            bw = int(sh_ * pw / ph)
            bx = int(PIP_SRC[0] * sw - bw / 2)
            # interpolate the source window from the full frame to the box crop
            src = (lerp(0, bx, k), 0, lerp(sw, bx + bw, k), sh_)
            dst = (lerp(0, px, k), lerp(0, py, k), lerp(W, px + pw, k), lerp(H, py + ph, k))
            dw, dh = int(round(dst[2] - dst[0])), int(round(dst[3] - dst[1]))
            hb = her.resize((dw, dh), Image.BICUBIC, box=src)
            r = int(lerp(0, PIP_R, k))
            m = rounded_mask(dw, dh, max(r, 1), ss=2) if r > 0 else None
            if k > 0.05:
                sh2, pad2 = shadow(dw, dh, max(r, 1), blur=24, alpha=int(110 * k))
                frame.paste((40, 10, 20), (int(dst[0]) - pad2, int(dst[1]) - pad2), sh2)
            frame.paste(hb, (int(dst[0]), int(dst[1])), m)
            if k > 0.5:                                 # a thin white rim, like a window
                rim = Image.new("L", (dw, dh), 0)
                ImageDraw.Draw(rim).rounded_rectangle((1, 1, dw - 2, dh - 2), r, outline=255, width=4)
                frame.paste((255, 255, 255), (int(dst[0]), int(dst[1])), rim.point(lambda v: v * (k - 0.5) * 2))
        enc.stdin.write(frame.tobytes())
        if f % 150 == 0:
            print("demo %5d/%d" % (f, n), flush=True)
    enc.stdin.close()
    enc.wait()


if __name__ == "__main__":
    main()
