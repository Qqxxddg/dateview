# -*- coding: utf-8 -*-
"""任务5修复2：postHandler 就地改造行数组 + 兼容 wrapper + 可过滤日志"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
PATH = r'D:\dataview-workspace\DataView_布局文件[0-统计看板].dv.json'

POST_HANDLER = r"""// 归一化(状态码->中文/robot_code->amr_code) + 排序 + 空错降级 + 同内容防跳顶
return new Promise((resolve) => {
    try {
        console.warn('===CARD7_POST=== input', typeof data, Array.isArray(data) ? ('array:' + data.length) : (data && Array.isArray(data.data) ? ('wrapper.data:' + data.data.length) : 'other'));
        const STATUS_MAP = {'0': '离线', '1': '运行', '2': '充电', '3': '空闲', '4': '异常'};
        const ORDER = {'异常': 0, '离线': 1, '运行': 2, '充电': 3, '空闲': 4};
        const EMPTY_ROW = [{amr_code: '-', status: '暂无数据'}];
        let rows = null;
        if (Array.isArray(data)) {
            rows = data;
        } else if (data && Array.isArray(data.list)) {
            rows = data.list;
        } else if (data && Array.isArray(data.data)) {
            rows = data.data;
        }
        if (!rows || rows.length === 0) {
            resolve(EMPTY_ROW);
            return;
        }
        for (let i = 0; i < rows.length; i++) {
            let r = rows[i] || {};
            rows[i] = r;
            let code = (r.status !== undefined && r.status !== null) ? String(r.status) : '';
            let st = STATUS_MAP[code];
            let amr = (r.robot_code !== undefined && r.robot_code !== null && r.robot_code !== '') ? String(r.robot_code) : ((r.amr_code !== undefined && r.amr_code !== null) ? String(r.amr_code) : '-');
            r.amr_code = amr;
            r.status = (st !== undefined) ? st : (code === '' ? '-' : code);
        }
        rows.sort((a, b) => {
            let pa = ORDER[a.status] !== undefined ? ORDER[a.status] : 99;
            let pb = ORDER[b.status] !== undefined ? ORDER[b.status] : 99;
            if (pa !== pb) return pa - pb;
            if (a.amr_code < b.amr_code) return -1;
            if (a.amr_code > b.amr_code) return 1;
            return 0;
        });
        let sig = rows.map((r) => r.amr_code + '|' + r.status).join(';');
        let lastSig = this.$container.$model('card7Sig');
        let last = this.$container.$model('card7Rows');
        if (lastSig === sig && Array.isArray(last)) {
            console.warn('===CARD7_POST=== same-sig reuse');
            resolve(last);
            return;
        }
        this.$container.$model('card7Sig', sig);
        this.$container.$model('card7Rows', rows);
        console.warn('===CARD7_POST=== resolve', rows.length, rows[0]);
        resolve(rows);
    } catch (e) {
        console.warn('===CARD7_POST=== error', e);
        resolve([{amr_code: '-', status: '暂无数据'}]);
    }
});"""

outer = json.load(open(PATH, encoding='utf-8'))
content = json.loads(outer[0]['content'])
el = next(e for e in content['pages'][0]['elements'] if e.get('refName') == '#card7')
el['option']['sources'][0]['postHandler'] = POST_HANDLER

outer[0]['content'] = json.dumps(content, ensure_ascii=False)
with open(PATH, 'w', encoding='utf-8') as f:
    json.dump(outer, f, ensure_ascii=False, indent=2)
print('postHandler rewritten, len', len(POST_HANDLER))
