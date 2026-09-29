# -*- coding: utf-8 -*-
"""任务5补充修复：参数绑定改静态空值（防 model 表达式取到 'all'/undefined）、preHandler 兜底不抛错"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
PATH = r'D:\dataview-workspace\DataView_布局文件[0-统计看板].dv.json'

outer = json.load(open(PATH, encoding='utf-8'))
content = json.loads(outer[0]['content'])
el = next(e for e in content['pages'][0]['elements'] if e.get('refName') == '#card7')
src = el['option']['sources'][0]

# 1) params 改静态空串（对齐页面级 SQL1818567 的已验证形态，避免 model.robotcodes 未定义/model.mapcodes='all' 泄漏进 SQL）
src['params'] = {
    "text": False,
    "data": [
        {"field": "mapcodes", "type": "String", "value": ""},
        {"field": "robotcodes", "type": "String", "value": ""},
    ],
}

# 2) preHandler 整体 try/catch，任何异常都不得阻断请求
src['preHandler'] = """// 取参：#select0 地图 -> mapcodes（ALL 归一 null）；#select1 日期 -> model.date
try {
    let mapCls = this.$container.$component('#select0')
    let mapcodes = null
    if (mapCls) {
        let v = (mapCls.tmpValue !== undefined && mapCls.tmpValue !== null && mapCls.tmpValue !== '') ? mapCls.tmpValue : mapCls.value
        if (v) {
            mapcodes = (v === 'ALL' || v === 'all') ? null : v
            this.$container.$model('mapcodes', v)
        }
    }
    let dateCls = this.$container.$component('#select1')
    if (dateCls) {
        let dv = dateCls.tmpValue !== undefined && dateCls.tmpValue !== null && dateCls.tmpValue !== '' ? dateCls.tmpValue : dateCls.value
        if (dv) {
            this.$container.$model('date', dv)
        }
    }
    data = data || {}
    data.mapcodes = mapcodes
    data.robotcodes = ''
    return data
} catch (e) {
    console.error('card7 preHandler error', e)
    return data || {}
}"""

# 3) postHandler 兼容数组 / {list:[...]} / map 形态输入
src['postHandler'] = """// 归一化(状态码->中文/robot_code->amr_code) + 排序 + 空错降级 + 同内容防跳顶
return new Promise((resolve) => {
    try {
        const STATUS_MAP = {'0': '离线', '1': '运行', '2': '充电', '3': '空闲', '4': '异常'};
        const ORDER = {'异常': 0, '离线': 1, '运行': 2, '充电': 3, '空闲': 4};
        const EMPTY_ROW = [{amr_code: '-', status: '暂无数据'}];
        let rows = [];
        if (Array.isArray(data)) {
            rows = data;
        } else if (data && Array.isArray(data.list)) {
            rows = data.list;
        } else if (data && Array.isArray(data.data)) {
            rows = data.data;
        }
        if (rows.length === 0) {
            resolve(EMPTY_ROW);
            return;
        }
        let norm = rows.map((r) => {
            r = r || {};
            let code = (r.status !== undefined && r.status !== null) ? String(r.status) : '';
            let st = STATUS_MAP[code];
            return {
                amr_code: (r.robot_code !== undefined && r.robot_code !== null && r.robot_code !== '') ? String(r.robot_code) : (r.amr_code !== undefined && r.amr_code !== null ? String(r.amr_code) : '-'),
                status: (st !== undefined) ? st : (code === '' ? '-' : code)
            };
        });
        norm.sort((a, b) => {
            let pa = ORDER[a.status] !== undefined ? ORDER[a.status] : 99;
            let pb = ORDER[b.status] !== undefined ? ORDER[b.status] : 99;
            if (pa !== pb) return pa - pb;
            if (a.amr_code < b.amr_code) return -1;
            if (a.amr_code > b.amr_code) return 1;
            return 0;
        });
        let last = this.$container.$model('card7Rows');
        if (Array.isArray(last) && last.length === norm.length) {
            let same = true;
            for (let i = 0; i < norm.length; i++) {
                if (last[i].amr_code !== norm[i].amr_code || last[i].status !== norm[i].status) {
                    same = false;
                    break;
                }
            }
            if (same) {
                resolve(last);
                return;
            }
        }
        this.$container.$model('card7Rows', norm);
        resolve(norm);
    } catch (e) {
        console.error('card7 postHandler error', e);
        resolve([{amr_code: '-', status: '暂无数据'}]);
    }
});"""

outer[0]['content'] = json.dumps(content, ensure_ascii=False)
with open(PATH, 'w', encoding='utf-8') as f:
    json.dump(outer, f, ensure_ascii=False, indent=2)

c2 = json.loads(json.load(open(PATH, encoding='utf-8'))[0]['content'])
s2 = next(e for e in c2['pages'][0]['elements'] if e.get('refName') == '#card7')['option']['sources'][0]
print('params:', json.dumps(s2['params'], ensure_ascii=False))
print('handlers updated, source:', s2['source'])
