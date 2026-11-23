# -*- coding: utf-8 -*-
"""Render a reel in the HeyGen cloud without the CLI's broken paths.

    python tools/hfrender.py reel-22            -> reel-22/renders/REEL-22.mp4

2026-10-05: `hyperframes cloud render` failed two ways — its upload died at the
finalise step (404 asset_not_found) and, given an uploaded asset, its poll
reported 404 "render not found" for a render that in fact completed in 5 s.
The API itself is fine. So: tools/hfup.py uploads, this submits with the
asset_id, polls GET /v3/hyperframes/renders/{id} itself, and downloads the
video with parallel ranged GETs (the CDN throttles a single stream —
memory: reel-speed-lessons).

Billing: the API wallet (~$0.23–0.47 a render). Never renders on her laptop —
her rule, 2026-10-05.
"""
import json
import os
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API = "https://api.heygen.com"


def key():
    p = os.path.expanduser("~/.heygen/credentials")
    if os.path.exists(p):
        return json.load(open(p))["api_key"]
    # the cloud container: the egress proxy adds X-Api-Key for api.heygen.com
    # itself (a network secret), so no key ever sits on the machine
    return os.environ.get("HEYGEN_API_KEY")


def auth(h):
    k = key()
    if k:
        h["X-Api-Key"] = k
    return h


def call(method, path, body=None):
    r = urllib.request.Request(API + path, method=method,
                               data=json.dumps(body).encode() if body is not None else None,
                               headers=auth({"Content-Type": "application/json"}))
    try:
        with urllib.request.urlopen(r, timeout=120) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8", "replace") or "{}")
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode("utf-8", "replace") or "{}")
        except ValueError:
            return e.code, {}


def find(obj, *names):
    """first value under any of `names`, searching nested dicts"""
    if isinstance(obj, dict):
        for n in names:
            if n in obj and obj[n]:
                return obj[n]
        for v in obj.values():
            got = find(v, *names)
            if got:
                return got
    return None


def download(url, out, parts=10):
    req = urllib.request.Request(url, headers={"Range": "bytes=0-0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        total = int(r.headers["Content-Range"].split("/")[1])
    step = total // parts + 1
    chunks = [None] * parts

    def get(i):
        a, b = i * step, min(total - 1, (i + 1) * step - 1)
        for attempt in range(5):
            try:
                rq = urllib.request.Request(url, headers={"Range": "bytes=%d-%d" % (a, b)})
                with urllib.request.urlopen(rq, timeout=300) as r:
                    chunks[i] = r.read()
                if len(chunks[i]) == b - a + 1:
                    return
            except Exception:
                time.sleep(2 + attempt * 2)
    th = [threading.Thread(target=get, args=(i,)) for i in range(parts)]
    for t in th:
        t.start()
    for t in th:
        t.join()
    if any(c is None for c in chunks):
        sys.exit("download incomplete")
    with open(out + ".part", "wb") as f:
        for c in chunks:
            f.write(c)
    os.replace(out + ".part", out)
    return total


def main():
    reel = sys.argv[1].rstrip("/\\")
    nn = reel.split("-")[-1]
    project = os.path.join(ROOT, reel)
    out = os.path.join(project, "renders", "REEL-%s.mp4" % nn)
    os.makedirs(os.path.dirname(out), exist_ok=True)

    up = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "hfup.py"), project],
                        capture_output=True, text=True)
    if up.returncode:
        sys.exit("upload failed: " + (up.stderr or up.stdout)[-400:])
    asset = up.stdout.strip().splitlines()[-1].strip()
    print(up.stdout.strip().splitlines()[0], "| asset", asset)

    st, res = call("POST", "/v3/hyperframes/renders", {
        "project": {"type": "asset_id", "asset_id": asset},
        "aspect_ratio": "9:16", "fps": 30, "quality": "standard", "title": "REEL-%s" % nn})
    rid = find(res, "render_id", "id")
    if st not in (200, 201, 202) or not rid:
        sys.exit("submit failed %s %s" % (st, json.dumps(res)[:400]))
    print("render", rid)

    t0 = time.time()
    url = None
    while time.time() - t0 < 60 * 40:
        time.sleep(10)
        st, res = call("GET", "/v3/hyperframes/renders/%s" % rid)
        status = find(res, "status") if st == 200 else "pending(%s)" % st
        if status == "completed":
            url = find(res, "video_url", "url")
            break
        if status == "failed":
            sys.exit("render failed: %s" % json.dumps(res)[:600])
    if not url:
        sys.exit("render did not finish in 40 min (id %s)" % rid)
    print("rendered in %.0fs" % (time.time() - t0))
    n = download(url, out)
    print("saved %s (%.1f MB)" % (out, n / 1e6))


if __name__ == "__main__":
    main()
