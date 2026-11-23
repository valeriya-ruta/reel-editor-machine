# -*- coding: utf-8 -*-
"""Save finished reels into her Google Drive, any size.

    python tools/driveup.py reel-45/renders/REEL-45.mp4 [...]

Why: the Drive connector uploads by carrying the whole file inside one tool
call, so a 25-60 MB reel can't go through it. Instead a small Apps Script of
hers (tools/drive-hook.gs, deployed as a web app) opens a Drive upload for
each file, and the file goes straight to Drive in 16 MB pieces.

The web app's URL is read from the env var REELS_DRIVE_HOOK and never
printed: anyone holding it can add files to that folder. The folder is
REELS_DRIVE_FOLDER, else "Reels".
"""
import json
import os
import sys
import urllib.error
import urllib.request

CHUNK = 64 * 256 * 1024          # 16 MB, a multiple of 256 KiB as Drive asks


def session(path):
    hook = os.environ.get("REELS_DRIVE_HOOK", "").strip()
    if not hook:
        sys.exit("REELS_DRIVE_HOOK is not set: add the Apps Script web app URL in the environment settings")
    body = json.dumps({"name": os.path.basename(path), "size": os.path.getsize(path),
                       "folder": os.environ.get("REELS_DRIVE_FOLDER", "Reels")}).encode()
    req = urllib.request.Request(hook, body, {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:   # Apps Script answers via a redirect; urllib follows it
        return json.load(r)["upload"]


def upload(path):
    url, size = session(path), os.path.getsize(path)
    with open(path, "rb") as f:
        at = 0
        while True:
            piece = f.read(CHUNK)
            end = at + len(piece) - 1
            req = urllib.request.Request(url, piece, method="PUT", headers={
                "Content-Length": str(len(piece)), "Content-Range": "bytes %d-%d/%d" % (at, end, size)})
            try:
                with urllib.request.urlopen(req, timeout=300) as r:
                    return json.load(r)                      # 200/201: the last piece landed
            except urllib.error.HTTPError as e:
                if e.code != 308:                            # 308 = "resume": send the next piece
                    raise SystemExit("upload of %s failed: HTTP %d %s" % (path, e.code, e.read()[:300]))
            at = end + 1


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for p in sys.argv[1:]:
        f = upload(p)
        print("uploaded %s -> %s" % (f["name"], f.get("webViewLink", f["id"])))


if __name__ == "__main__":
    main()
