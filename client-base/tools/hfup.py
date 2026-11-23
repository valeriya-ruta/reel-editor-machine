# -*- coding: utf-8 -*-
"""Upload a reel project to HeyGen ourselves and print its asset_id.

    python tools/hfup.py reel-21          -> asset_id on the last line
    ./hf cloud render --asset-id <id> --aspect-ratio 9:16 -o reel-21/renders/REEL-21.mp4

Why: on 2026-10-05 `hyperframes cloud render` (0.8.33 and 0.8.105 alike) failed
every upload at the finalise step — HTTP 404 asset_not_found — while the same
three calls made by hand (POST /v3/assets/direct-uploads, PUT to the presigned
S3 URL, POST /v3/assets/{id}/complete) all succeed. So we do the upload and
hand the CLI only the asset_id, which skips its broken path.

The zip mirrors the CLI's: the project dir minus .hyperframesignore rules and
the usual dev clutter. The key is read from ~/.heygen/credentials and never
printed.
"""
import fnmatch
import hashlib
import io
import json
import os
import sys
import time
import urllib.error
import urllib.request
import zipfile

API = "https://api.heygen.com"
ALWAYS_SKIP = ["renders/", "snapshots/", "study/", ".git/", "node_modules/", "build.py", "sfx.json",
               "PLAN.md", ".hyperframesignore", "render*.log", "*.pyc", "__pycache__/"]


def rules(project):
    out = list(ALWAYS_SKIP)
    p = os.path.join(project, ".hyperframesignore")
    if os.path.exists(p):
        out += [l.strip() for l in open(p, encoding="utf-8") if l.strip() and not l.startswith("#")]
    return out


def skipped(rel, pats):
    for p in pats:
        if p.endswith("/"):
            if rel.startswith(p) or ("/" + p) in ("/" + rel):
                return True
        elif fnmatch.fnmatch(rel, p) or fnmatch.fnmatch(os.path.basename(rel), p):
            return True
    return False


def build_zip(project):
    pats = rules(project)
    buf = io.BytesIO()
    n = 0
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(project):
            for f in files:
                full = os.path.join(root, f)
                rel = os.path.relpath(full, project).replace("\\", "/")
                if rel.startswith(".") or skipped(rel, pats) or os.path.basename(rel).startswith("_"):
                    continue
                z.write(full, rel)
                n += 1
    return buf.getvalue(), n


def call(method, url, key=None, body=None, raw=None, headers=None):
    h = headers if headers is not None else {"X-Api-Key": key, "Content-Type": "application/json"}
    data = raw if raw is not None else (json.dumps(body).encode() if body is not None else None)
    r = urllib.request.Request(url, data=data, method=method, headers=h)
    try:
        with urllib.request.urlopen(r, timeout=600) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")


def main():
    project = os.path.abspath(sys.argv[1])
    key = json.load(open(os.path.expanduser("~/.heygen/credentials")))["api_key"]
    data, n = build_zip(project)
    sha = hashlib.sha256(data).hexdigest()
    print("zip: %d files, %.1f MB" % (n, len(data) / 1e6))
    st, txt = call("POST", API + "/v3/assets/direct-uploads", key,
                   {"filename": os.path.basename(project) + ".zip", "content_type": "application/zip",
                    "size_bytes": len(data), "checksum_sha256": sha})
    if st != 200:
        sys.exit("init failed %d %s" % (st, txt[:300]))
    d = json.loads(txt).get("data") or json.loads(txt)
    t0 = time.time()
    st, txt = call("PUT", d["upload_url"], raw=data, headers=dict(d.get("upload_headers") or {}))
    if st != 200:
        sys.exit("upload failed %d %s" % (st, txt[:300]))
    print("uploaded in %.0fs" % (time.time() - t0))
    # a bigger upload can take a while to become visible to the API; the CLI
    # gave up after ~8 s, which is one of the ways it failed on 2026-10-05
    for i in range(20):
        st, txt = call("POST", API + "/v3/assets/%s/complete" % d["asset_id"], key, {"checksum_sha256": sha})
        if st == 200:
            break
        time.sleep(min(15, 2 + 2 * i))
    if st != 200:
        sys.exit("complete failed %d %s" % (st, txt[:300]))
    try:
        url = (json.loads(txt).get("data") or {}).get("url")
    except ValueError:
        url = None
    if url:
        print("URL " + url)
    print(d["asset_id"])


if __name__ == "__main__":
    main()
