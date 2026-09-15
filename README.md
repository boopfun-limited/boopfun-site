# boopfun.com

BOOPFUN LIMITED 的公司主页。托管在 Firebase Hosting，项目 `boopfun-web`。

| 站点 | 域名 | 内容 |
|---|---|---|
| `boopfun-main` | `boopfun.com` | 本仓库的 `public/` |
| `boopfun-web` | `legal.boopfun.com` | 法律文件，源码由 `gthbj/arrows` 仓库的 `docs/legal/` 管理，部署入口以该仓库发布 runbook 为准 |

## 部署

```bash
python3 deploy.py
```

该命令按 `public/` 的完整文件集合发布。广告平台 app-ads.txt 授权文件的源码是
[`public/app-ads.txt`](public/app-ads.txt)，会随首页一同部署到
`https://boopfun.com/app-ads.txt`。修改广告平台授权记录时修改这份源码，
不要只在线上添加文件，否则下一次整站部署会将其移除。

该文件保留 AdMob 的 Google 授权行，并包含 2026-09-08 从 Unity Ads 后台
app-ads.txt 页面复制的完整 154 行卖方清单及 `ownerdomain=boopfun.com`。
后续更新 Unity 清单时重新从后台复制完整集合，保留 Google 授权行与所有者域名，
核对记录字段和重复项后按上述入口整站发布，并执行下方线上与源码比对。

2026-09-15 追加 AppLovin MAX（后台 Account > App-ads.txt Info 的整段）、Meta Audience Network（按 Meta for Developers 的 app-ads.txt 说明写 Business ID 行）与 Pangle（后台左下角的账户 ID 行，加 Pangle app-ads.txt 说明里的三行 PubMatic）。更新时各自从后台 / 说明重新复制，与已有行按「域名 + ID + 关系」去重。

部署后可核对线上授权记录与源码一致：

```bash
curl --fail --silent --show-error https://boopfun.com/app-ads.txt | cmp public/app-ads.txt -
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

> 文档维护：Claude Opus 5（2026-09-06）；GPT-6（2026-09-08，Unity Ads 卖方清单来源与部署说明）；Claude Opus 5（2026-09-15，追加 AppLovin / Meta / Pangle 的授权行）
