# config

媒体播放器聚合订阅与规则集。由 GitHub Actions 从上游 [hafrey1/LunaTV-config](https://github.com/hafrey1/LunaTV-config) 同步生成（上游自带健康检测，本仓库不再重复探测）。

## 文件

| 文件 | 用于 | 说明 |
|---|---|---|
| `media/hongguo-web.js` | hongguo-web | 全源聚合 JS 源，一次搜索并发查所有源，结果带源名徽标；首页分类保留父子层级，点击自动对源取详情 |
| `media/marcomovie.json` | MarcoMovie | TVBox 格式 `sites` 配置，每个源为 `type:1` 苹果 CMS 接口 |
| `media/media-domains.yaml` | Clash / Mihomo | 媒体播放 CDN 域名规则集，包含 m3u8 主地址及其切片/TS 域名，供代理分流（通常设 DIRECT 直连） |

## 导入方式

### hongguo-web

1. 网页顶栏「源」→「＋ 新增」，打开「导入数据源」弹窗
2. 「源地址 URL」填：
   ```
   https://raw.githubusercontent.com/summerscar/config/refs/heads/main/media/hongguo-web.js
   ```
3. 点导入。文件内带 `updateUrl`，之后会自动检查上游更新；也可以随时在管理面板点「检查源更新」手动触发。

### MarcoMovie

1. 在应用的配置导入处填入订阅地址：
   ```
   https://raw.githubusercontent.com/summerscar/config/refs/heads/main/media/marcomovie.json
   ```
2. 或下载 `media/marcomovie.json` 本地导入。

## Clash / Mihomo 媒体域名规则集

`media/media-domains.yaml` 是每个源抽取样例剧集、递归解析 m3u8（主播放列表 → 子播放列表 → TS 切片）得到的播放域名集合，格式为 Clash rule-set YAML（`payload` 里是裸域名）。用 YAML 而非 `.mrs` 是为了可读、方便查找与维护，且 CI 无需额外二进制。

订阅地址：

```
https://raw.githubusercontent.com/summerscar/config/refs/heads/main/media/media-domains.yaml
```

Mihomo 配置示例（把这些域名直连，避免国内 CDN 绕代理）：

```yaml
rule_providers:
  media:
    type: http
    format: yaml
    behavior: domain
    url: https://raw.githubusercontent.com/summerscar/config/refs/heads/main/media/media-domains.yaml
    path: ./rule_sets/media.yaml
    interval: 86400

rules:
  - RULE-SET(media, DIRECT)
```

> 老版本 Clash 若不支持 rule provider，可直接把 `payload` 下的域名复制进自己的 `DOMAIN-SUFFIX` 规则。若你的客户端确实需要 `.mrs`，可用 `mihomo convert-ruleset domain yaml media-domains.yaml media-domains.mrs` 本地转换（该格式二进制、不便人工维护，故仓库默认提供 YAML）。

## 自动更新

| Workflow | 频率 | 内容 |
|---|---|---|
| `.github/workflows/update.yml` | 每天 UTC 00:00（北京 08:00） | 拉取上游 `api_site`，剥离代理前缀、去重、生成两个订阅文件，有变化则提交 |
| `.github/workflows/update-media-rules.yml` | 每周一 UTC 01:00（北京 09:00） | 抽样每个源、递归解析 m3u8 提取播放域名，重新生成规则集，有变化则提交 |

两个 workflow 均支持在 Actions 页面手动触发 `workflow_dispatch`。规则集任务若抓取异常（域名少于 10 个）会放弃提交，避免把坏数据写进仓库。

## 说明

- 源的实际可用性由上游维护；本仓库只做格式转换与同步。
- 内容版权归各平台所有，请遵守当地法律法规，仅作个人学习自用。
