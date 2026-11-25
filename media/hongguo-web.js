// hongguo-web 全源聚合订阅 —— 由 GitHub Action 每日从 LunaTV-config 同步生成
// 导入：hongguo-web「源 -> +新增」填入源地址 URL（本文件 raw 链接），导入一次即可。
// 文件带 updateUrl，后续会自动检查上游更新（脚本内版本随上游同步递增）。
var APIS = {
  "ltv_iqiyizyapi_com": {
    "name": "🎬-爱奇艺-",
    "api": "https://iqiyizyapi.com/api.php/provide/vod"
  },
  "ltv_dbzy_tv": {
    "name": "🎬豆瓣资源",
    "api": "https://caiji.dbzy5.com/api.php/provide/vod"
  },
  "ltv_mtzy_me": {
    "name": "🎬茅台资源",
    "api": "https://caiji.maotaizy.cc/api.php/provide/vod"
  },
  "ltv_wolongzyw_com": {
    "name": "🎬卧龙资源",
    "api": "https://wolongzyw.com/api.php/provide/vod"
  },
  "ltv_ikunzy_com": {
    "name": "🎬iKun资源",
    "api": "https://ikunzyapi.com/api.php/provide/vod"
  },
  "ltv_dyttzyapi_com": {
    "name": "🎬电影天堂",
    "api": "http://caiji.dyttzyapi.com/api.php/provide/vod"
  },
  "ltv_www_maoyanzy_com": {
    "name": "🎬猫眼资源",
    "api": "https://api.maoyanapi.top/api.php/provide/vod"
  },
  "ltv_cj_lzcaiji_com": {
    "name": "🎬量子资源",
    "api": "https://cj.lzcaiji.com/api.php/provide/vod"
  },
  "ltv_360zy_com": {
    "name": "🎬360 资源",
    "api": "https://360zyzz.com/api.php/provide/vod"
  },
  "ltv_jszyapi_com": {
    "name": "🎬极速资源",
    "api": "https://jszyapi.com/api.php/provide/vod"
  },
  "ltv_www_moduzy_net": {
    "name": "🎬魔都资源",
    "api": "https://www.mdzyapi.com/api.php/provide/vod"
  },
  "ltv_ffzyapi_com": {
    "name": "🎬非凡资源",
    "api": "https://api.ffzyapi.com/api.php/provide/vod"
  },
  "ltv_bfzy_tv": {
    "name": "🎬暴风资源",
    "api": "https://bfzyapi.com/api.php/provide/vod"
  },
  "ltv_zuida_xyz": {
    "name": "🎬最大资源",
    "api": "https://api.zuidapi.com/api.php/provide/vod"
  },
  "ltv_wujinzy_me": {
    "name": "🎬无尽资源",
    "api": "https://api.wujinapi.me/api.php/provide/vod"
  },
  "ltv_xinlangapi_com": {
    "name": "🎬新浪资源",
    "api": "https://api.xinlangapi.com/xinlangapi.php/provide/vod"
  },
  "ltv_api_wwzy_tv": {
    "name": "🎬旺旺资源",
    "api": "https://api.wwzy.tv/api.php/provide/vod"
  },
  "ltv_www_subozy_com": {
    "name": "🎬速播资源",
    "api": "https://subocaiji.com/api.php/provide/vod"
  },
  "ltv_jinyingzy_com": {
    "name": "🎬金鹰点播",
    "api": "https://jyzyapi.com/provide/vod/from/jinyingyun/at/json"
  },
  "ltv_p2100_net": {
    "name": "🎬飘零资源",
    "api": "https://p2100.net/api.php/provide/vod"
  },
  "ltv_api_ukuapi88_com": {
    "name": "🎬U酷影视",
    "api": "https://api.ukuapi88.com/api.php/provide/vod"
  },
  "ltv_api_guangsuapi_com": {
    "name": "🎬光速资源",
    "api": "https://api.guangsuapi.com/api.php/provide/vod"
  },
  "ltv_www_hongniuzy_com": {
    "name": "🎬红牛资源",
    "api": "https://www.hongniuzy2.com/api.php/provide/vod"
  },
  "ltv_caiji_moduapi_cc": {
    "name": "🎬魔都动漫",
    "api": "https://caiji.moduapi.cc/api.php/provide/vod"
  },
  "ltv_www_ryzyw_com": {
    "name": "🎬如意资源",
    "api": "https://cj.rycjapi.com/api.php/provide/vod"
  },
  "ltv_www_haohuazy_com": {
    "name": "🎬豪华资源",
    "api": "https://hhzyapi.com/api.php/provide/vod"
  },
  "ltv_bdzy1_com": {
    "name": "🎬百度云zy",
    "api": "https://api.apibdzy.com/api.php/provide/vod"
  },
  "ltv_lovedan_net": {
    "name": "🎬艾旦影视",
    "api": "https://lovedan.net/api.php/provide/vod"
  },
  "ltv_lzizy_net": {
    "name": "🎬量子影视",
    "api": "https://cj.lziapi.com/api.php/provide/vod"
  },
  "ltv_zuidazy_co": {
    "name": "🎬最大点播",
    "api": "https://zuidazy.me/api.php/provide/vod"
  },
  "ltv_wujinzy_com": {
    "name": "🎬无尽影视",
    "api": "https://api.wujinapi.com/api.php/provide/vod"
  },
  "ltv_wwzy_tv": {
    "name": "🎬旺旺短剧",
    "api": "https://wwzy.tv/api.php/provide/vod"
  },
  "ltv_1080zyk4_com": {
    "name": "🎬优质资源",
    "api": "https://api.yzzy-api.com/inc/apijson.php"
  },
  "ltv_www_huyaapi_com": {
    "name": "🎬虎牙资源",
    "api": "https://www.huyaapi.com/api.php/provide/vod"
  },
  "ltv_yayazy3_com": {
    "name": "🎬鸭鸭资源",
    "api": "https://cj.yayazy.net/api.php/provide/vod"
  },
  "ltv_suonizy_net": {
    "name": "🎬索尼资源",
    "api": "https://suoniapi.com/api.php/provide/vod"
  },
  "ltv_kuaichezy_com": {
    "name": "🎬快车资源",
    "api": "https://caiji.kuaichezy.org/api.php/provide/vod"
  },
  "ltv_shandianzy_com": {
    "name": "🎬闪电资源",
    "api": "https://xsd.sdzyapi.com/api.php/provide/vod"
  },
  "ltv_yhzy_cc": {
    "name": "🎬樱花资源",
    "api": "https://m3u8.apiyhzy.com/api.php/provide/vod"
  },
  "ltv_91md_me": {
    "name": "🔞麻豆视频",
    "api": "https://91md.me/api.php/provide/vod"
  },
  "ltv_155zy2_com": {
    "name": "🔞155-资源",
    "api": "https://155api.com/api.php/provide/vod"
  },
  "ltv_apiyutu_com": {
    "name": "🔞玉兔资源",
    "api": "https://apiyutu.com/api.php/provide/vod"
  },
  "ltv_fhapi9_com": {
    "name": "🔞番号资源",
    "api": "http://fhapi9.com/api.php/provide/vod"
  },
  "ltv_apilsbzy1_com": {
    "name": "🔞-老色逼-",
    "api": "https://apilsbzy1.com/api.php/provide/vod"
  },
  "ltv_xiaojizy_live": {
    "name": "🔞小鸡资源",
    "api": "https://api.xiaojizy.live/provide/vod"
  },
  "ltv_hsckzy_xyz": {
    "name": "🔞黄色仓库",
    "api": "https://hsckzy.xyz/api.php/provide/vod"
  },
  "ltv_apidanaizi_com": {
    "name": "🔞-大奶子-",
    "api": "https://apidanaizi.com/api.php/provide/vod"
  },
  "ltv_jkunzyapi_com": {
    "name": "🔞jkun资源",
    "api": "https://jkunzyapi.com/api.php/provide/vod"
  },
  "ltv_lbapi9_com": {
    "name": "🔞乐播资源",
    "api": "https://lbapi9.com/api.php/provide/vod"
  },
  "ltv_Naixxzy_com": {
    "name": "🔞奶香资源",
    "api": "https://Naixxzy.com/api.php/provide/vod"
  },
  "ltv_slapibf_com": {
    "name": "🔞森林资源",
    "api": "https://beiyong.slapibf.com/api.php/provide/vod"
  },
  "ltv_apilj_com": {
    "name": "🔞辣椒资源",
    "api": "https://apilj.com/api.php/provide/vod"
  },
  "ltv_shayuapi_com": {
    "name": "🔞鲨鱼资源",
    "api": "https://shayuapi.com/api.php/provide/vod"
  },
  "ltv_doudouzy_com": {
    "name": "🔞豆豆资源",
    "api": "https://api.douapi.cc/api.php/provide/vod"
  },
  "ltv_didizy_com": {
    "name": "🔞滴滴资源",
    "api": "https://api.ddapi.cc/api.php/provide/vod"
  },
  "ltv_heiliaozy_cc": {
    "name": "🔞黑料资源",
    "api": "https://www.heiliaozyapi.com/api.php/provide/vod"
  },
  "ltv_thzy8_me": {
    "name": "🔞桃花资源",
    "api": "https://thzy1.me/api.php/provide/vod"
  },
  "ltv_www_jingpinx_com": {
    "name": "🔞精品资源",
    "api": "https://www.jingpinx.com/api.php/provide/vod"
  },
  "ltv_ckzy_me": {
    "name": "🔞 CK-资源",
    "api": "https://ckzy.me/api.php/provide/vod"
  },
  "ltv_souavzyw_com": {
    "name": "🔞souavZY",
    "api": "https://api.souavzyw.net/api.php/provide/vod"
  },
  "ltv_www_xxibaozyw_com": {
    "name": "🔞细胞资源",
    "api": "https://www.xxibaozyw.com/api.php/provide/vod"
  },
  "ltv_xiangjiaozyw_com": {
    "name": "🔞香蕉资源",
    "api": "https://www.xiangjiaozyw.com/api.php/provide/vod"
  },
  "ltv_www_msnii_com": {
    "name": "🔞-美少女-",
    "api": "https://www.msnii.com/api/json.php"
  },
  "ltv_www_pgxdy_com": {
    "name": "🔞-黄AVZY",
    "api": "https://www.pgxdy.com/api/json.php"
  },
  "ltv_www_kxgav_com": {
    "name": "🔞白嫖资源",
    "api": "https://www.kxgav.com/api/json.php"
  },
  "ltv_xingba111_com": {
    "name": "🔞杏吧资源",
    "api": "https://xingba222.com/api.php/provide/vod"
  },
  "ltv_dadizy11_com": {
    "name": "🔞大地资源",
    "api": "https://dadiapi.com/feifei"
  },
  "ltv_semaozy1_com": {
    "name": "🔞色猫资源",
    "api": "https://caiji.semaozy.net/inc/apijson_vod.php/provide/vod"
  },
  "ltv_aosikazy_com": {
    "name": "🔞-奥斯卡-",
    "api": "https://aosikazy.com/api.php/provide/vod"
  }
};
var IDS = Object.keys(APIS);
var spider = {
  id: 'lunatv_all',
  name: 'LunaTV全源聚合',
  version: '2026.11.25',
  updateUrl: 'https://raw.githubusercontent.com/summerscar/config/refs/heads/main/media/hongguo-web.js',
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
