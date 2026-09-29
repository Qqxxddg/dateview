# -*- coding: utf-8 -*-
"""任务5：#card7 组件级数据源 SQL09091542 + preHandler/postHandler"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
PATH = r'D:\dataview-workspace\DataView_布局文件[0-统计看板].dv.json'

PRE_HANDLER = r"""// 取参：#select0 地图 -> mapcodes（ALL 归一 null）；#select1 日期 -> model.date
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
data.mapcodes = mapcodes
return data"""

POST_HANDLER = r"""// 归一化(状态码->中文/robot_code->amr_code) + 排序 + 空错降级 + 同内容防跳顶
return new Promise((resolve) => {
    try {
        const STATUS_MAP = {'0': '离线', '1': '运行', '2': '充电', '3': '空闲', '4': '异常'};
        const ORDER = {'异常': 0, '离线': 1, '运行': 2, '充电': 3, '空闲': 4};
        const EMPTY_ROW = [{amr_code: '-', status: '暂无数据'}];
        let rows = Array.isArray(data) ? data : [];
        if (rows.length === 0) {
            resolve(EMPTY_ROW);
            return;
        }
        let norm = rows.map((r) => {
            let code = (r.status !== undefined && r.status !== null) ? String(r.status) : '';
            let st = STATUS_MAP[code];
            return {
                amr_code: (r.robot_code !== undefined && r.robot_code !== null) ? String(r.robot_code) : '-',
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

SOURCE = {
    "id": "20260929160000001",
    "source": "SQL09091542",
    "type": "common",
    "interval": "${constant.RefreshHzForAmr}",
    "map": False,
    "preHandler": PRE_HANDLER,
    "postHandler": POST_HANDLER,
    "params": {
        "data": [
            {"field": "mapcodes", "type": "String", "valueType": "expression", "value": "model.mapcodes"},
            {"field": "robotcodes", "type": "String", "valueType": "expression", "value": "model.robotcodes"},
        ]
    },
    "filterRule": {"sort": [], "style": []},
    "mapping": [],
}

outer = json.load(open(PATH, encoding='utf-8'))
content = json.loads(outer[0]['content'])
el = next(e for e in content['pages'][0]['elements'] if e.get('refName') == '#card7')
el['option']['sources'] = [SOURCE]

# 验证
assert el['option']['sources'][0]['source'] == 'SQL09091542'
assert el['option']['sources'][0]['interval'] == '${constant.RefreshHzForAmr}'
assert el['option']['defaultValue']  # 样例保留
assert len(el['props']['colors']) == 5  # 任务4着色保留
assert el['events'][0]['children'][0]['value'] == 'onCard7RowClick'

outer[0]['content'] = json.dumps(content, ensure_ascii=False)
with open(PATH, 'w', encoding='utf-8') as f:
    json.dump(outer, f, ensure_ascii=False, indent=2)

c2 = json.loads(json.load(open(PATH, encoding='utf-8'))[0]['content'])
el2 = next(e for e in c2['pages'][0]['elements'] if e.get('refName') == '#card7')
s = el2['option']['sources'][0]
print('source:', s['source'], '| type:', s['type'], '| map:', s['map'], '| interval:', s['interval'])
print('params fields:', [p['field'] for p in s['params']['data']])
print('preHandler len:', len(s['preHandler']), '| postHandler len:', len(s['postHandler']))
print('task5 write OK')
