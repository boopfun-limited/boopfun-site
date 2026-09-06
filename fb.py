#!/usr/bin/env python3
"""Firebase Hosting REST 客户端（本机 firebase CLI 用不了，见 deploy.py 顶部注释）。

当模块用: from fb import api, access_token
当命令用: python3 fb.py GET projects/boopfun-web/sites/boopfun-main/customDomains/boopfun.com
"""
import json
import pathlib
import subprocess
import sys
import tempfile

API = "https://firebasehosting.googleapis.com/v1beta1"
OAUTH_CLIENT = "563584335869-fgrhgmd47bqnekij5i8b5pr03ho849e6.apps.googleusercontent.com"
OAUTH_SECRET = "j9iVZfS8kkCEFUPaAeJV0sAi"  # firebase-tools 的公开 client secret，非私密


def curl(*args, quiet=False):
    # --noproxy: 本机 HTTPS_PROXY=127.0.0.1:7890 对 *.googleapis.com 时好时坏
    #   （SSL_ERROR_SYSCALL），直连稳得多。firebase CLI 的失败多半也是同一原因。
    # --retry: 直连同样会偶发握手失败，整条链路是间歇性的（实测同一分钟内
    #   Google 10/10 通过而 github.com 直连挂掉）。重试即过。
    cmd = ["curl", "-sS", "--fail-with-body", "--noproxy", "*",
           "--retry", "5", "--retry-delay", "2", "--retry-all-errors",
           "--max-time", "120", *args]
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0:
        msg = f"curl 失败 ({r.returncode}): {r.stdout.decode()[:600]} {r.stderr.decode()[:300]}"
        if quiet:
            raise RuntimeError(msg)
        sys.exit(msg)
    return r.stdout


def access_token():
    cfg = json.load(open(pathlib.Path.home() / ".config/configstore/firebase-tools.json"))
    out = curl("https://oauth2.googleapis.com/token",
               "-d", f"client_id={OAUTH_CLIENT}", "-d", f"client_secret={OAUTH_SECRET}",
               "-d", f"refresh_token={cfg['tokens']['refresh_token']}",
               "-d", "grant_type=refresh_token")
    return json.loads(out)["access_token"]


def api(tok, method, url, body=None, blob=None):
    if not url.startswith("https://"):
        url = f"{API}/{url}"
    args = ["-X", method, "-H", f"Authorization: Bearer {tok}", url]
    tmp = None
    if blob is not None:
        tmp = tempfile.NamedTemporaryFile(delete=False)
        tmp.write(blob)
        tmp.close()
        args += ["-H", "Content-Type: application/octet-stream", "--data-binary", f"@{tmp.name}"]
    elif body is not None:
        args += ["-H", "Content-Type: application/json", "-d", json.dumps(body)]
    out = curl(*args)
    if tmp:
        pathlib.Path(tmp.name).unlink()
    return json.loads(out) if out.strip() else {}


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    method, path = sys.argv[1], sys.argv[2]
    payload = json.loads(sys.argv[3]) if len(sys.argv) > 3 else None
    print(json.dumps(api(access_token(), method, path, payload), indent=1, ensure_ascii=False))
