# -*- coding: utf-8 -*-
"""任务2：locales 新增 t3_carno / t3_status / noData"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
PATH = r'D:\dataview-workspace\DataView_布局文件[0-统计看板].dv.json'

outer = json.load(open(PATH, encoding='utf-8'))
content = json.loads(outer[0]['content'])

existing = {l.get('key') for l in content['locales']}
print('existing keys n:', len(existing))
for k in ('t3_carno', 't3_status', 'noData'):
    if k in existing:
        raise SystemExit(f'key already exists: {k}')

new_keys = [
    {"key": "t3_carno", "zh-CN": "车号", "en-US": "Vehicle"},
    {"key": "t3_status", "zh-CN": "状态", "en-US": "Status"},
    {"key": "noData", "zh-CN": "暂无数据", "en-US": "No data"},
]
content['locales'].extend(new_keys)

outer[0]['content'] = json.dumps(content, ensure_ascii=False)
with open(PATH, 'w', encoding='utf-8') as f:
    json.dump(outer, f, ensure_ascii=False, indent=2)

# 验证
outer2 = json.load(open(PATH, encoding='utf-8'))
content2 = json.loads(outer2[0]['content'])
keys = [l.get('key') for l in content2['locales']]
assert len(keys) == len(set(keys)), 'duplicate keys'
for k in ('t3_carno', 't3_status', 'noData'):
    assert keys.count(k) == 1, f'{k} missing or duplicated'
    entry = next(l for l in content2['locales'] if l['key'] == k)
    print('added:', entry)
# 确认既有键未改动数量关系
assert len(keys) == 58 + 3, len(keys)
print('locales n:', len(keys), '| parse OK | keys unique OK')
