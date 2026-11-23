#!/usr/bin/env python3
"""Generate aggregated subscription files for hongguo-web and MarcoMovie.

Upstream: hafrey1/LunaTV-config (LunaTV-config.json -> api_site mapping).
The upstream repo already runs its own health check (report.md), so we simply
sync the full source list and regenerate both subscriptions; no probing here.
"""

import json
import os
import re
import sys
import urllib.request

UPSTREAM_URL = (
    "https://raw.githubusercontent.com/hafrey1/LunaTV-config/"
    "refs/heads/main/LunaTV-config.json"
)

# Raw URLs of the generated files inside this repository. hongguo-web uses
# updateUrl to auto-check upstream updates; keep in sync with repo/branch.
REPO_OWNER = os.environ.get("REPO_OWNER", "summerscar")
REPO_NAME = os.environ.get("REPO_NAME", "config")
BRANCH = os.environ.get("BRANCH", "main")
RAW_BASE = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/refs/heads/{BRANCH}/media"
HONGGUO_URL = f"{RAW_BASE}/hongguo-web.js"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_DIR = os.path.join(ROOT, "media")
HONGGUO_OUT = os.path.join(MEDIA_DIR, "hongguo-web.js")
MARCO_OUT = os.path.join(MEDIA_DIR, "marcomovie.json")
TVBOX_OUT = os.path.join(MEDIA_DIR, "tvbox.json")
TVBOX_NORMAL_OUT = os.path.join(MEDIA_DIR, "tvbox-normal.json")
TVBOX_ADULT_OUT = os.path.join(MEDIA_DIR, "tvbox-adult.json")

UA = "Mozilla/5.0 (compatible; config-generator/1.0)"


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def source_id(key):
    """Make a stable hongguo-web source id (allowed: [\\w.-]{1,64})."""
    sid = re.sub(r"[^A-Za-z0-9]+", "_", key).strip("_")
    if not sid:
        sid = "src"
    return "ltv_" + sid[:56]


def strip_proxy(api):
    """Unwrap upstream CORS proxy prefix (?url=<real>) when present."""
    m = re.search(r"[?&]url=([^&]+)", api)
    if m:
        from urllib.parse import unquote

        return unquote(m.group(1))
    return api


def load_upstream():
    data = fetch_json(UPSTREAM_URL)
    sites = data.get("api_site", {})
    if not sites:
        raise RuntimeError("upstream api_site is empty")
    result = []
    seen = set()
    for key, meta in sites.items():
        api = strip_proxy(str(meta.get("api", "")))
        if not api:
            continue
        sid = source_id(key)
        if sid in seen:
            continue
        seen.add(sid)
        result.append(
            {
                "id": sid,
                "name": str(meta.get("name", "")),
                "api": api,
            }
        )
    return result


HONGGUO_TEMPLATE = r"""// hongguo-web 全源聚合订阅 —— 由 GitHub Action 每日从 LunaTV-config 同步生成
// 导入：hongguo-web「源 -> +新增」填入源地址 URL（本文件 raw 链接），导入一次即可。
// 文件带 updateUrl，后续会自动检查上游更新（脚本内版本随上游同步递增）。
var APIS = __APIS__;
var IDS = Object.keys(APIS);
var spider = {
  id: 'lunatv_all',
  name: 'LunaTV全源聚合',
  version: '__VERSION__',
  updateUrl: '__UPDATE_URL__',
  home: async function () {
    try {
      var res = await fetch(APIS[IDS[0]].api + '?ac=list', { timeoutMs: 15000 });
      var data = JSON.parse(await res.text());
      var raw = data.class || [];
      var byid = {};
      for (var i = 0; i < raw.length; i++) byid[String(raw[i].type_id)] = raw[i];
      var classes = [];
      for (var j = 0; j < raw.length; j++) {
        var c = raw[j];
        if (!c || c.type_id === undefined) continue;
        var tid = String(c.type_id);
        var nm = String(c.type_name || '');
        var pid = String(c.type_pid || '0');
        if (pid !== '0' && byid[pid] && String(byid[pid].type_name || '') !== nm)
          nm = String(byid[pid].type_name) + ' / ' + nm;
        classes.push({ type_id: tid, type_name: nm });
      }
      if (!classes.length) classes.push({ type_id: '1', type_name: '全部' });
      return { class: classes, filters: {} };
    } catch (e) { return { class: [{ type_id: '1', type_name: '全部' }], filters: {} }; }
  },
  category: async function (tid, page) {
    page = Number(page) || 1;
    var t = String(tid);
    var params = '?ac=detail&pg=' + page;
    if (t.indexOf('Y|') === 0) {
      var parts = t.split('|');
      params += '&t=' + parts[1] + '&year=' + parts[2];
    } else {
      params += '&t=' + t;
    }
    var res = await fetch(APIS[IDS[0]].api + params, { timeoutMs: 15000 });
    var data = JSON.parse(await res.text());
    var list = (data.list || []).map(function (v) {
      return { vod_id: IDS[0] + '||' + v.vod_id, vod_name: String(v.vod_name || ''), vod_pic: String(v.vod_pic || ''), vod_remarks: String(v.vod_remarks || '') + ' [' + APIS[IDS[0]].name + ']' };
    });
    return { page: page, pagecount: Number(data.pagecount) || page, hasMore: !!data.pagecount && page < Number(data.pagecount), list: list };
  },
  detail: async function (id) {
    var parts = String(id).split('||');
    var sid = parts.length > 1 ? parts[0] : IDS[0];
    var vid = parts.length > 1 ? parts[1] : id;
    var res = await fetch(APIS[sid].api + '?ac=detail&ids=' + vid, { timeoutMs: 15000 });
    var data = JSON.parse(await res.text());
    var v = (data.list || [])[0] || {};
    if (!v.vod_id) throw new Error('EMPTY');
    return { list: [{ vod_id: String(v.vod_id), vod_name: String(v.vod_name || ''), vod_pic: String(v.vod_pic || ''), vod_remarks: String(v.vod_remarks || ''), vod_tag: String(v.vod_class || ''), vod_play_from: String(v.vod_play_from || '默认线路'), vod_play_url: String(v.vod_play_url || '') }] };
  },
  search: async function (wd, quick, page) {
    page = Number(page) || 1;
    var word = String(wd || '').trim();
    if (!word) return { page: 1, pagecount: 1, hasMore: false, list: [] };
    var tasks = IDS.map(function (sid) {
      return fetch(APIS[sid].api + '?ac=detail&wd=' + encodeURIComponent(word) + '&pg=' + page, { timeoutMs: 10000 })
        .then(async function (res) {
          var data = JSON.parse(await res.text());
          return (data.list || []).map(function (v) {
            return { vod_id: sid + '||' + v.vod_id, vod_name: String(v.vod_name || ''), vod_pic: String(v.vod_pic || ''), vod_remarks: String(v.vod_remarks || '') + ' [' + APIS[sid].name + ']' };
          });
        }).catch(function () { return []; });
    });
    var groups = await Promise.all(tasks);
    var list = [];
    for (var i = 0; i < groups.length; i++) list = list.concat(groups[i]);
    return { page: page, pagecount: page, hasMore: false, list: list };
  },
  play: function (flag, id) {
    var url = String(id || '');
    if (/^https?:\/\//.test(url)) return { parse: 0, url: url };
    return { parse: 0, url: '', error: 'MISSING_STREAM' };
  }
};
globalThis.spider = spider;
"""


def version_stamp():
    """x.y.z version derived from UTC date so auto-update sees changes daily."""
    from datetime import datetime, timezone

    now = datetime.now(timezone.utc)
    return f"{now.year}.{now.month}.{now.day}"


def write_hongguo(sources):
    apis = {s["id"]: {"name": s["name"], "api": s["api"]} for s in sources}
    code = (
        HONGGUO_TEMPLATE.replace("__APIS__", json.dumps(apis, ensure_ascii=False, indent=2))
        .replace("__VERSION__", version_stamp())
        .replace("__UPDATE_URL__", HONGGUO_URL)
    )
    with open(HONGGUO_OUT, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"wrote {HONGGUO_OUT} ({len(apis)} APIs, version {version_stamp()})")


def build_sites(sources, adult=None):
    """TVBox/MarcoMovie-compatible site array (all type=1 MacCMS APIs).

    adult=None -> all sources; True -> only 🔞 sources; False -> only normal ones.
    """
    sites = []
    seen_keys = set()
    for s in sources:
        is_adult = "🔞" in s.get("name", "")
        if adult is True and not is_adult:
            continue
        if adult is False and is_adult:
            continue
        from urllib.parse import urlparse

        host = urlparse(s["api"]).netloc or s["id"]
        key = host
        if key in seen_keys:
            key = s["id"]
        seen_keys.add(key)
        sites.append(
            {
                "key": key,
                "name": s["name"],
                "type": 1,
                "api": s["api"],
                "searchable": 1,
                "quickSearch": 1,
                "changeable": 0,
            }
        )
    return sites


def write_marco(sites):
    config = {"sites": sites}
    with open(MARCO_OUT, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"wrote {MARCO_OUT} ({len(sites)} sites)")


def write_tvbox(sites, out=TVBOX_OUT):
    """Full TVBox config: sites + live TV + standard empty shell fields."""
    config = {
        "spider": "",
        "wallpaper": "",
        "logo": "",
        "sites": sites,
        "lives": [
            {
                "name": "APTV直播",
                "type": 0,
                "url": "https://raw.githubusercontent.com/Kimentanm/aptv/master/m3u/iptv.m3u",
                "playerType": 2,
            }
        ],
        "rules": [],
    }
    with open(out, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"wrote {out} ({len(sites)} sites)")


def main():
    os.makedirs(MEDIA_DIR, exist_ok=True)
    sources = load_upstream()
    print(f"upstream sources: {len(sources)}")
    write_hongguo(sources)
    write_marco(build_sites(sources))
    # TVBox: three flavors — all / normal(🎬) / adult(🔞), all with the same live TV.
    write_tvbox(build_sites(sources), TVBOX_OUT)
    write_tvbox(build_sites(sources, adult=False), TVBOX_NORMAL_OUT)
    write_tvbox(build_sites(sources, adult=True), TVBOX_ADULT_OUT)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"generate failed: {exc}", file=sys.stderr)
        sys.exit(1)
