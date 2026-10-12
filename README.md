# boopfun.com

BOOPFUN LIMITED 的公司主页。托管在 Firebase Hosting，项目 `boopfun-web`。

| 站点 | 域名 | 内容 |
|---|---|---|
| `boopfun-main` | `boopfun.com` | 本仓库的 `public/` |
| `boopfun-web` | `legal.boopfun.com` | 法律文件，源码由 `boopfun-limited/boopfun-legal` 仓库管理，部署入口以该仓库 README 的「部署」一节为准 |

## 首页维护

首页为无构建依赖的静态 HTML / CSS：`public/index.html`、`public/styles.css`。
游戏展示仅使用商店横版 feature graphic，按原始 **1024 × 500** 比例完整显示；
不要把图片固定为其它高度，也不要换成竖版玩法截图。网页图片为 WebP，
首屏加载三张，其余延迟加载；不依赖外部字体或 JavaScript。

- Arrows Out：`arrows/docs/store-listing/en-US/images/featureGraphic.png`
- Arrows 3D：`arrows-3d/Docs/store-listing/en-US/images/featureGraphic.png`
- Water Sort：`water_sort/docs/store-listing/en-US/images/featureGraphic.png`
- Sudoku：`sudoku/docs/store/feature-graphic-1024x500.png`
- boopdoku：从 [Google Play 正式商店页](https://play.google.com/store/apps/details?id=com.boopfun.boopdoku) 的公开 feature graphic 获取。

上述源码路径相对于各兄弟仓；优化后的发布文件位于 `public/assets/*-feature.webp`。
商店入口以 [BOOPFUN 开发者页](https://play.google.com/store/apps/developer?id=BOOPFUN) 为准，
五款游戏均指向各自的正式 Google Play 页面。`social.png` 为分享预览图；
`robots.txt` 与 `sitemap.xml` 指向主域名。

本地预览：

```bash
python3 -m http.server 8765 --bind 127.0.0.1 --directory public
```

修改后检查桌面与手机宽度、图片自然比例与显示比例、五个商店入口及隐私链接。
保留 `public/app-ads.txt`，发布后按下文核对线上与源码一致。

> 首页维护：GPT-6（2026-10-12，官网重设计、横版商店素材与下载入口）；Kimi（2026-10-12，视觉美化、Google Play 官方徽标）

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

> 文档维护：Claude Opus 5（2026-09-06）；GPT-6（2026-09-08，Unity Ads 卖方清单来源与部署说明）；Claude Opus 5（2026-09-15，追加 AppLovin / Meta / Pangle 的授权行）；Claude Opus 5.5（2026-09-24，法律站源码改指 `boopfun-limited/boopfun-legal`）
