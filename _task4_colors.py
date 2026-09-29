# -*- coding: utf-8 -*-
"""任务4：把渲染规则合并进交付布局文件（归一化为状态列文字着色）"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
PATH = r'D:\dataview-workspace\DataView_布局文件[0-统计看板].dv.json'

outer = json.load(open(PATH, encoding='utf-8'))
content = json.loads(outer[0]['content'])
el = next(e for e in content['pages'][0]['elements'] if e.get('refName') == '#card7')

# 归一化：type=cell（只染状态单元格）、field=status（目标字段=状态列）
# 条件字段 name=status、operator='='、值与色值沿用用户在 UI 配置的映射
colors = [
    {"type": "cell", "field": "status", "name": "status", "operator": "=", "value": "异常", "color": "#F86508", "backgroundColor": "#FFFFFF"},
    {"type": "cell", "field": "status", "name": "status", "operator": "=", "value": "运行", "color": "#09C184", "backgroundColor": "#FFFFFF"},
    {"type": "cell", "field": "status", "name": "status", "operator": "=", "value": "离线", "color": "#8A8A8A", "backgroundColor": "#FFFFFF"},
    {"type": "cell", "field": "status", "name": "status", "operator": "=", "value": "空闲", "color": "#0086FF", "backgroundColor": "#FFFFFF"},
    {"type": "cell", "field": "status", "name": "status", "operator": "=", "value": "充电", "color": "#35B8FF", "backgroundColor": "#FFFFFF"},
]
el['props']['colors'] = colors

# 验证
assert el['elName'] == 'dv-scrolltable'
assert len(el['props']['colors']) == 5
assert all(c['field'] == 'status' and c['type'] == 'cell' for c in colors)
vals = {c['value'] for c in colors}
assert vals == {'运行', '空闲', '充电', '异常', '离线'}
# 未配置规则的状态（维修中/暂无数据）走默认色、不丢行——无需配置即满足

outer[0]['content'] = json.dumps(content, ensure_ascii=False)
with open(PATH, 'w', encoding='utf-8') as f:
    json.dump(outer, f, ensure_ascii=False, indent=2)

# 回读
c2 = json.loads(json.load(open(PATH, encoding='utf-8'))[0]['content'])
el2 = next(e for e in c2['pages'][0]['elements'] if e.get('refName') == '#card7')
print('colors merged:', len(el2['props']['colors']))
for c in el2['props']['colors']:
    print(' ', c['value'], '->', c['color'], f"({c['type']}/{c['field']})")
print('task4 merge OK')
