# config

媒体播放器聚合订阅。每天由 GitHub Actions 从上游 [hafrey1/LunaTV-config](https://github.com/hafrey1/LunaTV-config) 同步源列表并重新生成（上游自带健康检测，本仓库不再重复探测）。

## 订阅文件

| 播放器 | 文件 | 说明 |
|---|---|---|
| hongguo-web | `media/hongguo-web.js` | 全源聚合 JS 源，一次搜索并发查所有源，结果带源名徽标；首页分类保留父子层级，点击自动对源取详情 |
| MarcoMovie | `media/marcomovie.json` | TVBox 格式 `sites` 配置，每个源为 `type:1` 苹果 CMS 接口 |

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

## 自动更新

`.github/workflows/update.yml` 每天 UTC 00:00（北京时间 08:00）执行：

1. 拉取上游 `LunaTV-config.json` 的 `api_site`
2. 剥离 CORS 代理前缀、去重、转为稳定的 source id
3. 重新生成两个订阅文件
4. 如有变化则自动提交

也可在 Actions 页面手动触发 `workflow_dispatch`。

## 说明

- 源的实际可用性由上游维护；本仓库只做格式转换与同步。
- 内容版权归各平台所有，请遵守当地法律法规，仅作个人学习自用。
