#!/usr/bin/env python3
"""把 public/ 部署到 Firebase Hosting。

两个绕路，都是本机环境问题，不是设计选择：
1. firebase CLI 在 firebasehosting.googleapis.com 上稳定失败（curl 同一 URL 正常，
   IPv4/IPv6 都通，代理有无都试过），所以直接走 REST API。
2. HTTP 一律用 curl 子进程，不用 urllib —— 本机 HTTPS_PROXY 指向 127.0.0.1:7890，
   urllib 走它会随机 SSLEOFError，curl 不会。
CLI 或代理修好后可以简化，但在此之前别改回去。

用法: python3 deploy.py [--site boopfun-main]
"""
import gzip
import hashlib
import json
import pathlib
import sys

from fb import access_token, api, curl

ROOT = pathlib.Path(__file__).parent


def to_serving_config(cfg):
    """firebase.json 的 hosting 段 → REST 的 ServingConfig。

    两种格式不同，CLI 平时替你翻译：`source` 在 API 里叫 `glob`，
    内层 headers 是 map 而不是 [{key,value}]。
    """
    out = {k: cfg[k] for k in ("cleanUrls", "trailingSlash", "appAssociation") if k in cfg}
    if "headers" in cfg:
        out["headers"] = [
            {"glob": h["source"], "headers": {e["key"]: e["value"] for e in h["headers"]}}
            for h in cfg["headers"]
        ]
    for k in ("redirects", "rewrites"):
        if cfg.get(k):
            sys.exit(f"firebase.json 用到了 {k}，本脚本还没写它的格式翻译，先补上再部署")
    return out


def main():
    site = sys.argv[sys.argv.index("--site") + 1] if "--site" in sys.argv else "boopfun-main"
    cfg = json.load(open(ROOT / "firebase.json"))["hosting"]
    public = ROOT / cfg["public"]
    vcfg = to_serving_config(cfg)

    tok = access_token()

    version = api(tok, "POST", f"sites/{site}/versions", {"config": vcfg})["name"]
    print(f"version: {version}")

    blobs = {}
    for path in sorted(public.rglob("*")):
        if path.is_file():
            gz = gzip.compress(path.read_bytes(), mtime=0)
            blobs["/" + str(path.relative_to(public))] = (hashlib.sha256(gz).hexdigest(), gz)
    print(f"files: {', '.join(blobs)}")

    pop = api(tok, "POST", f"{version}:populateFiles",
              {"files": {p: h for p, (h, _) in blobs.items()}})
    required = pop.get("uploadRequiredHashes") or []
    upload_url = pop.get("uploadUrl", "")
    print(f"需上传 {len(required)} 个 blob")

    by_hash = {h: gz for h, gz in blobs.values()}
    for h in required:
        api(tok, "POST", f"{upload_url}/{h}", blob=by_hash[h])
        print(f"  uploaded {h[:12]}…")

    api(tok, "PATCH", f"{version}?update_mask=status", {"status": "FINALIZED"})
    rel = api(tok, "POST", f"sites/{site}/releases?versionName={version}")
    print(f"released: {rel.get('name', '?')}")

    url = f"https://{site}.web.app"
    got = curl("-L", url).decode()
    assert "BOOPFUN LIMITED" in got, f"部署后 {url} 内容不对:\n{got[:300]}"
    print(f"✓ {url} 已返回预期内容")


if __name__ == "__main__":
    main()
