# -*- coding: utf-8 -*-
"""Where her face is, frame by frame, on a reel's plate.

    python tools/facemap.py 01            # reel-01/assets/base.mp4 -> work/r01/face.json
    python tools/facemap.py 01 --sheet    # + a contact sheet with the boxes drawn
    python tools/facemap.py 01 --flat     # reel-01/assets/voice.mp4 -> work/r01/face_flat.json

Two maps, because the half-screens move her. `--flat` maps the plate as cut
(voice.mp4, before any half-screen is baked in): the build lays the beats out
from it. The default maps base.mp4 as it will be rendered (after
tools/halfscreen.py): tools/safezone.js checks the graphics against it.

Ruta, 2026-11-17: "make sure that nothing is going on her face ... They should
always go under her chin or behind her head." Her selfie framing moves a lot
(she leans in, the cut steps the scale), so where her chin is cannot be
guessed once per reel. This samples the plate at 10 fps with OpenCV's YuNet
face detector and stores, per sample:

    t      plate seconds
    box    [x0, y0, x1, y1] of the face, 1080x1920 plate pixels
    eyes   y of the eye line
    mouth  y of the mouth line
    chin   y of the chin (box bottom, pushed down to cover the jaw)
    top    estimated top of her hair

The face box is what nothing may touch (tools/safezone.js reads it), and
`face_band(t0, t1)` in a build gives the lowest chin and the highest hair
over a beat, so a graphic can be placed under the chin or above the head.

Model: work/_scratch/models/yunet.onnx (face_detection_yunet_2023mar, from
huggingface.co/opencv/face_detection_yunet). A sample with no face found
keeps the previous one.
"""
import json
import os
import subprocess
import sys

import cv2
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL = os.path.join(ROOT, "work", "_scratch", "models", "yunet.onnx")
URL = "https://huggingface.co/opencv/face_detection_yunet/resolve/main/face_detection_yunet_2023mar.onnx"
FPS = 10
W, H = 540, 960          # detect at half size, report in plate pixels


def frames(path):
    p = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-i", path, "-an", "-vf",
                          "fps=%d,scale=%d:%d" % (FPS, W, H), "-f", "rawvideo", "-pix_fmt", "bgr24", "-"],
                         stdout=subprocess.PIPE)
    n = W * H * 3
    while True:
        buf = p.stdout.read(n)
        if len(buf) < n:
            break
        yield np.frombuffer(buf, np.uint8).reshape(H, W, 3)


def main():
    nn = sys.argv[1].zfill(2)
    flat = "--flat" in sys.argv
    plate = os.path.join(ROOT, "reel-" + nn, "assets", "voice.mp4" if flat else "base.mp4")
    if not os.path.exists(MODEL):
        os.makedirs(os.path.dirname(MODEL), exist_ok=True)
        subprocess.run(["curl", "-sSL", "-o", MODEL, URL], check=True)
    det = cv2.FaceDetectorYN.create(MODEL, "", (W, H), 0.6, 0.3, 5)
    out, last = [], None
    k = 2.0 * 1080 / (W * 2)   # = 2.0: half size -> plate
    for i, img in enumerate(frames(plate)):
        _, faces = det.detect(img)
        if faces is not None and len(faces):
            f = max(faces, key=lambda r: r[2] * r[3])
            x, y, w, h = [float(v) * k for v in f[:4]]
            ey = (f[5] + f[7]) / 2 * k                    # eye line
            my = (f[11] + f[13]) / 2 * k                  # mouth corners
            chin = max(y + h, my + 0.55 * (my - ey))     # jaw below the box edge
            top = ey - 1.25 * (chin - ey)                 # top of her hair, roughly
            last = {"box": [round(x), round(y), round(x + w), round(chin)],
                    "eyes": round(ey), "mouth": round(my), "chin": round(chin), "top": round(top)}
        if last:
            out.append(dict(last, t=round(i / float(FPS), 2)))
    path = os.path.join(ROOT, "work", "r" + nn, "face_flat.json" if flat else "face.json")
    json.dump(out, open(path, "w"), indent=0)
    ch = [r["chin"] for r in out]
    print("face.json: %d samples; chin y %d-%d (median %d); eyes y %d-%d"
          % (len(out), min(ch), max(ch), int(np.median(ch)),
             min(r["eyes"] for r in out), max(r["eyes"] for r in out)))
    if "--sheet" in sys.argv:
        sheet(plate, out, os.path.join(ROOT, "work", "r" + nn, "face_flat_sheet.jpg" if flat else "face_sheet.jpg"))


def sheet(plate, rows, path):
    picks = rows[::max(1, len(rows) // 24)][:24]
    tiles = []
    for r in picks:
        img = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", str(r["t"]), "-i", plate,
                              "-frames:v", "1", "-vf", "scale=270:480", "-f", "rawvideo",
                              "-pix_fmt", "bgr24", "-"], capture_output=True).stdout
        im = np.frombuffer(img, np.uint8).reshape(480, 270, 3).copy()
        s = 270 / 1080.0
        x0, y0, x1, y1 = [int(v * s) for v in r["box"]]
        cv2.rectangle(im, (x0, y0), (x1, y1), (0, 0, 255), 2)
        cv2.line(im, (0, int(r["chin"] * s)), (269, int(r["chin"] * s)), (0, 255, 255), 1)
        cv2.putText(im, "%.1f" % r["t"], (4, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        tiles.append(im)
    rows_img = [np.hstack(tiles[i:i + 8]) for i in range(0, len(tiles), 8)]
    cv2.imwrite(path, np.vstack(rows_img))
    print("sheet:", path)


if __name__ == "__main__":
    main()
