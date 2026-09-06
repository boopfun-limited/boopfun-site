# boopfun.com

BOOPFUN LIMITED 的公司主页。托管在 Firebase Hosting，项目 `boopfun-web`。

| 站点 | 域名 | 内容 |
|---|---|---|
| `boopfun-main` | `boopfun.com` | 本仓库的 `public/` |
| `boopfun-web` | `legal.boopfun.com` | 法律文件（目前是占位页，源码不在本仓库） |

## 部署

```bash
python3 deploy.py
```

**不要用 `firebase deploy`** —— 本机 firebase CLI 在 `firebasehosting.googleapis.com`
上稳定失败。原因与绕法写在 `deploy.py` / `fb.py` 顶部注释里，CLI 修好后可以换回去。

任意 API 调用：

```bash
python3 fb.py GET projects/boopfun-web/sites/boopfun-main/customDomains/boopfun.com
```

## DNS

在阿里云。`dns-snapshot-before.json` 是接管前的快照（含已删除的 4 条阿里云企业邮箱
CNAME 残留）。

🔴 **改 DNS 前先 `DescribeDomainRecords` 存快照，改完 diff 比对。**
飞书企业邮箱的 3 条 MX 与 2 条 TXT 绝对不能动，删了收不到邮件。

> 文档维护：Claude Opus 5（2026-09-06）
