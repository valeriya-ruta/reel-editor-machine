# -*- coding: utf-8 -*-
"""Upload finished reels to her Google Drive ourselves, any size.

    python tools/driveup.py <folder-id> reel-45/renders/REEL-45.mp4 [...]

Why: the Drive connector uploads by carrying the whole file inside one tool
call, so a 25-50 MB reel can't go through it. This talks to the Drive API
directly with a service account (a robot Google account that sees only what
is shared with it) and a resumable upload in 16 MB pieces.

The credential is the service account's JSON key, read from the environment
variable GOOGLE_SA_JSON (the file's contents, raw or base64) and never
printed. A service account owns no storage of its own, so <folder-id> must
sit in a Shared drive where that account is a Content manager.
"""
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

SCOPE = "https://www.googleapis.com/auth/drive"
UPLOAD = "https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable&supportsAllDrives=true&fields=id,name,webViewLink"
CHUNK = 64 * 256 * 1024          # 16 MB, a multiple of 256 KiB as Drive asks


def b64url(b):
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


def key():
    raw = os.environ.get("GOOGLE_SA_JSON", "").strip()
    if not raw:
        sys.exit("GOOGLE_SA_JSON is not set: add the service account key in the environment settings")
    if not raw.startswith("{"):
        raw = base64.b64decode(raw).decode("utf-8")
    return json.loads(raw)


def token(sa):
    now = int(time.time())
    head = b64url(json.dumps({"alg": "RS256", "typ": "JWT"}).encode())
    claim = b64url(json.dumps({"iss": sa["client_email"], "scope": SCOPE, "aud": sa["token_uri"],
                               "iat": now, "exp": now + 3600}).encode())
    pk = serialization.load_pem_private_key(sa["private_key"].encode(), password=None)
    sig = b64url(pk.sign((head + "." + claim).encode(), padding.PKCS1v15(), hashes.SHA256()))
    body = urllib.parse.urlencode({"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
                                   "assertion": head + "." + claim + "." + sig}).encode()
    with urllib.request.urlopen(urllib.request.Request(sa["token_uri"], body), timeout=60) as r:
        return json.load(r)["access_token"]


def upload(tok, folder, path):
    size = os.path.getsize(path)
    meta = json.dumps({"name": os.path.basename(path), "parents": [folder]}).encode()
    req = urllib.request.Request(UPLOAD, meta, {
        "Authorization": "Bearer " + tok, "Content-Type": "application/json; charset=UTF-8",
        "X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(size)})
    with urllib.request.urlopen(req, timeout=60) as r:
        session = r.headers["Location"]
    with open(path, "rb") as f:
        at = 0
        while True:
            piece = f.read(CHUNK)
            end = at + len(piece) - 1
            req = urllib.request.Request(session, piece, method="PUT", headers={
                "Content-Length": str(len(piece)), "Content-Range": "bytes %d-%d/%d" % (at, end, size)})
            try:
                with urllib.request.urlopen(req, timeout=300) as r:
                    return json.load(r)                      # 200/201: the last piece landed
            except urllib.error.HTTPError as e:
                if e.code != 308:                            # 308 = "resume": send the next piece
                    raise SystemExit("upload of %s failed: HTTP %d %s" % (path, e.code, e.read()[:300]))
            at = end + 1


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    tok = token(key())
    for p in sys.argv[2:]:
        f = upload(tok, sys.argv[1], p)
        print("uploaded %s -> %s" % (f["name"], f.get("webViewLink", f["id"])))


if __name__ == "__main__":
    main()
