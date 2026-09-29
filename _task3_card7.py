# -*- coding: utf-8 -*-
"""任务3：#card7 元素骨架改造为 dv-scrolltable（elName/props/option/events）"""
import json, sys, copy
sys.stdout.reconfigure(encoding='utf-8')
PATH = r'D:\dataview-workspace\DataView_布局文件[0-统计看板].dv.json'

outer = json.load(open(PATH, encoding='utf-8'))
content = json.loads(outer[0]['content'])
page = content['pages'][0]
el = next(e for e in page['elements'] if e.get('refName') == '#card7')

before = copy.deepcopy(el)

sample = [
    {"amr_code": "AMR-001", "status": "运行"},
    {"amr_code": "AMR-002", "status": "空闲"},
    {"amr_code": "AMR-003", "status": "充电"},
    {"amr_code": "AMR-004", "status": "异常"},
    {"amr_code": "AMR-005", "status": "离线"},
    {"amr_code": "AMR-006", "status": "维修中"},
    {"amr_code": "-", "status": "暂无数据"},
    {"amr_code": "AMR-007", "status": "运行"},
    {"amr_code": "AMR-008", "status": "异常"},
    {"amr_code": "AMR-009", "status": "空闲"},
]

el['elName'] = 'dv-scrolltable'
el['props'] = {
    "scroll": True,
    "scrollType": "scroll",
    "speed": 2,
    "pageSize": 10,
    "pageInterval": 5,
    "showPageIndex": False,
    "border": False,
    "stripe": True,
    "rowHeight": 36,
    "thHeight": 40,
    "fontSize": 12,
    "enhance": "",
    "columns": [
        {"label": "$t3_carno", "field": "amr_code", "show": True, "width": "", "format": "", "manual": False},
        {"label": "$t3_status", "field": "status", "show": True, "width": "", "format": "", "manual": False},
    ],
    "colors": [],
    "cellBorderColor": "",
    "innerPadding": 0,
    "showStyle": "0",
    "theme": "green",
}
el['option'] = {
    "dynamic": False,
    "sources": [],
    "dataMaps": [],
    "filterRule": {"sort": [], "style": []},
    "defaultValue": json.dumps(sample, ensure_ascii=False, indent=2),
    "sourceEvent": {"name": "sourceAction", "children": []},
}
el['events'] = [
    {
        "name": "row-click",
        "children": [
            {"id": 1759112345678, "type": "func", "isEdit": False, "param": {"type": "default"}, "value": "onCard7RowClick"}
        ],
    }
]

# 验证：未授权字段保持不变
for k in ('icon', 'visible', 'layout', 'style', 'id', 'refName'):
    assert el[k] == before[k], f'field {k} changed unexpectedly'
assert el['layout'] == {"w": 435, "h": 310, "x": 26, "y": 456, "z": 37}
assert el['refName'] == '#card7'
assert el['elName'] == 'dv-scrolltable'
assert el['events'][0]['children'][0]['value'] == 'onCard7RowClick'
dv = json.loads(el['option']['defaultValue'])
assert len(dv) == 10 and all(set(r.keys()) == {'amr_code', 'status'} for r in dv)
assert {r['status'] for r in dv} >= {'运行', '空闲', '充电', '异常', '离线', '维修中', '暂无数据'}
assert [c['field'] for c in el['props']['columns']] == ['amr_code', 'status']

outer[0]['content'] = json.dumps(content, ensure_ascii=False)
with open(PATH, 'w', encoding='utf-8') as f:
    json.dump(outer, f, ensure_ascii=False, indent=2)

# 回读再验
outer2 = json.load(open(PATH, encoding='utf-8'))
content2 = json.loads(outer2[0]['content'])
el2 = next(e for e in content2['pages'][0]['elements'] if e.get('refName') == '#card7')
assert el2['elName'] == 'dv-scrolltable'
assert el2['props']['columns'][0]['label'] == '$t3_carno'
print('element keys:', list(el2.keys()))
print('elName:', el2['elName'], '| layout:', el2['layout'])
print('columns:', json.dumps(el2['props']['columns'], ensure_ascii=False))
print('events:', json.dumps(el2['events'], ensure_ascii=False))
print('option keys:', list(el2['option'].keys()))
print('defaultValue rows:', len(json.loads(el2['option']['defaultValue'])))
print('unchanged fields verified: icon/visible/layout/style/id/refName')
print('task3 OK')
