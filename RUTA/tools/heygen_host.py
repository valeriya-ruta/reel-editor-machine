# -*- coding: utf-8 -*-
"""Put a finished MP4 on HeyGen's asset store and print its public URL.

    python tools/heygen_host.py work/5y/out/5-years-part-1.mp4

Buffer (and Windsor) post from a URL, never from a local file, so a render
made on this machine needs a public home first. HeyGen's direct upload is
the one the pipeline already uses (tools/hfup.py, same three calls: init,
PUT to the presigned URL, complete); here it carries the MP4 itself rather
than a project zip. Max 200 MB per asset.

The API key comes from ~/.heygen/credentials when present; in the cloud
container the proxy injects it for api.heygen.com, so none is needed.
"""
import hashlib, json, os, sys, time, urllib.error, urllib.request

API = "https://api.heygen.com"


def _key_headers():
    p = os.path.expanduser("~/.heygen/credentials")
    h = {"Content-Type": "application/json"}
    if os.path.exists(p):
        h["X-Api-Key"] = json.load(open(p))["api_key"]
    return h


def call(method, url, body=None, raw=None, headers=None):
    h = headers if headers is not None else _key_headers()
    data = raw if raw is not None else (json.dumps(body).encode() if body is not None else None)
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data=data, method=method, headers=h),
                                    timeout=900) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")


def host(path):
    data = open(path, "rb").read()
    sha = hashlib.sha256(data).hexdigest()
    st, txt = call("POST", API + "/v3/assets/direct-uploads",
                   {"filename": os.path.basename(path), "content_type": "video/mp4",
                    "size_bytes": len(data), "checksum_sha256": sha})
    if st != 200:
        sys.exit(f"init failed {st} {txt[:300]}")
    d = json.loads(txt).get("data") or json.loads(txt)
    st, txt = call("PUT", d["upload_url"], raw=data, headers=dict(d.get("upload_headers") or {}))
    if st != 200:
        sys.exit(f"upload failed {st} {txt[:300]}")
    for i in range(20):
        st, txt = call("POST", API + f"/v3/assets/{d['asset_id']}/complete", {"checksum_sha256": sha})
        if st == 200:
            break
        time.sleep(min(15, 2 + 2 * i))
    if st != 200:
        sys.exit(f"complete failed {st} {txt[:300]}")
    body = json.loads(txt).get("data") or {}
    return d["asset_id"], body.get("url"), body


if __name__ == "__main__":
    asset, url, body = host(sys.argv[1])
    print("ASSET", asset)
    print("URL", url)
    if not url:
        print(json.dumps(body)[:800])
