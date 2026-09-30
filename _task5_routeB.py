# -*- coding: utf-8 -*-
"""任务5路线B：页面级 source(SQL09091542) + binds setData 喂 #card7；移除组件级 source 防重复请求"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
PATH = r'D:\dataview-workspace\DataView_布局文件[0-统计看板].dv.json'

BIND_TEMPLATE = r"""console.log('card7 rows bind', data)
let card = this.$component('#card7')
let rows = []
if (Array.isArray(data)) {
    rows = data
} else if (data && Array.isArray(data.data)) {
    rows = data.data
} else if (data && Array.isArray(data.list)) {
    rows = data.list
}
if (!rows || rows.length === 0) {
    rows = [{amr_code: '-', status: '暂无数据'}]
    card.setData(rows)
    return rows
}
const STATUS_MAP = {'0': '离线', '1': '运行', '2': '充电', '3': '空闲', '4': '异常'};
const ORDER = {'异常': 0, '离线': 1, '运行': 2, '充电': 3, '空闲': 4};
for (let i = 0; i < rows.length; i++) {
    let r = rows[i] || {}
    rows[i] = r
    let code = (r.status !== undefined && r.status !== null) ? String(r.status) : ''
    let st = STATUS_MAP[code]
    let amr = (r.robot_code !== undefined && r.robot_code !== null && r.robot_code !== '') ? String(r.robot_code) : ((r.amr_code !== undefined && r.amr_code !== null) ? String(r.amr_code) : '-')
    r.amr_code = amr
    r.status = (st !== undefined) ? st : (code === '' ? '-' : code)
}
rows.sort((a, b) => {
    let pa = ORDER[a.status] !== undefined ? ORDER[a.status] : 99
    let pb = ORDER[b.status] !== undefined ? ORDER[b.status] : 99
    if (pa !== pb) return pa - pb
    if (a.amr_code < b.amr_code) return -1
    if (a.amr_code > b.amr_code) return 1
    return 0
})
card.setData(rows)
return rows"""

PAGE_SOURCE = {
    "id": "20260929173000001",
    "source": "SQL09091542",
    "interval": "${constant.RefreshHzForAmr}",
    "params": {
        "text": False,
        "data": [
            {"field": "mapcodes", "type": "String", "value": ""},
            {"field": "robotcodes", "type": "String", "value": ""},
        ],
    },
    "resultFormat": "list",
    "enhanceBefore": "",
    "handler": "",
    "binds": [{"refName": "#card7", "template": BIND_TEMPLATE}],
    "preHandler": "beforeSourceQuery_1",
    "postHandler": "",
}

outer = json.load(open(PATH, encoding='utf-8'))
content = json.loads(outer[0]['content'])
page = content['pages'][0]

# 1) 移除组件级 source（防重复轮询）
el = next(e for e in page['elements'] if e.get('refName') == '#card7')
el['option']['sources'] = []

# 2) 两份页面级列表都挂上新 source（与任务 1 结论一致的双写策略）
for lst in (content['option']['sources'], page['sources']):
    # 幂等：先删同 id / 同 source 的旧条目
    lst[:] = [s for s in lst if s.get('source') != 'SQL09091542' and s.get('id') != PAGE_SOURCE['id']]
    lst.append(json.loads(json.dumps(PAGE_SOURCE)))

# 3) 确认 beforeSourceQuery_1 仍在脚本中（preHandler 依赖它）
assert 'beforeSourceQuery_1' in page['script'], 'beforeSourceQuery_1 missing from page script'

outer[0]['content'] = json.dumps(content, ensure_ascii=False)
with open(PATH, 'w', encoding='utf-8') as f:
    json.dump(outer, f, ensure_ascii=False, indent=2)

c2 = json.loads(json.load(open(PATH, encoding='utf-8'))[0]['content'])
p2 = c2['pages'][0]
el2 = next(e for e in p2['elements'] if e.get('refName') == '#card7')
print('component sources:', el2['option']['sources'])
for name, lst in (('content.option', c2['option']['sources']), ('pages[0]', p2['sources'])):
    hit = [s for s in lst if s.get('source') == 'SQL09091542']
    print(name, 'SQL09091542 entries:', len(hit), '| total sources:', len(lst))
print('binds target:', hit[0]['binds'][0]['refName'] if hit else None)
print('preHandler:', hit[0]['preHandler'] if hit else None)
