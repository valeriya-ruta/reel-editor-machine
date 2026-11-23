# -*- coding: utf-8 -*-
"""Upload a finished reel to HeyGen's asset store and print its public URL.

    python3 tools/hfasset.py reel-56/renders/REEL-56.mp4     -> URL https://resource2.heygen.ai/video/.../original.mp4

Why: Buffer posts from a URL, and it can't read the render's signed S3 link
(reel 55, 2026-10-28). The asset URL it can. Same three calls as hfup.py:
direct-upload, PUT, complete. Under 200 MB per file (HeyGen's asset limit).
"""
import hashlib
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hfup import API, call  # noqa: E402


def main():
    path = os.path.abspath(sys.argv[1])
    cred = os.path.expanduser("~/.heygen/credentials")
    key = json.load(open(cred))["api_key"] if os.path.exists(cred) else os.environ.get("HEYGEN_API_KEY")
    data = open(path, "rb").read()
    sha = hashlib.sha256(data).hexdigest()
    st, txt = call("POST", API + "/v3/assets/direct-uploads", key,
                   {"filename": os.path.basename(path), "content_type": "video/mp4",
                    "size_bytes": len(data), "checksum_sha256": sha})
    if st != 200:
        sys.exit("init failed %d %s" % (st, txt[:300]))
    d = json.loads(txt).get("data") or json.loads(txt)
    st, txt = call("PUT", d["upload_url"], raw=data, headers=dict(d.get("upload_headers") or {}))
    if st != 200:
        sys.exit("upload failed %d %s" % (st, txt[:300]))
    for i in range(20):
        st, txt = call("POST", API + "/v3/assets/%s/complete" % d["asset_id"], key, {"checksum_sha256": sha})
        if st == 200:
            break
        time.sleep(min(15, 2 + 2 * i))
    if st != 200:
        sys.exit("complete failed %d %s" % (st, txt[:300]))
    print("asset", d["asset_id"])
    print("URL", (json.loads(txt).get("data") or {}).get("url"))


if __name__ == "__main__":
    main()
