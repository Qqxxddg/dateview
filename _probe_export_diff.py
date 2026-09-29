# -*- coding: utf-8 -*-
"""对比导出文件与工作区文件的 #card7 差异，提取渲染规则 schema"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

NEW = r'D:\dataview-workspace\DataView_布局文件[0-统计看板].dv1.json'
OLD = r'D:\dataview-workspace\DataView_布局文件[0-统计看板].dv.json'

def load(path):
    outer = json.load(open(path, encoding='utf-8'))
    return outer, json.loads(outer[0]['content'])

new_outer, new_c = load(NEW)
old_outer, old_c = load(OLD)

new_el = next(e for e in new_c['pages'][0]['elements'] if e.get('refName') == '#card7')
old_el = next(e for e in old_c['pages'][0]['elements'] if e.get('refName') == '#card7')

print('=== new #card7 keys ===')
print(list(new_el.keys()))
print()
print('=== new filterRule / colors / enhance / props.diff ===')
opt = new_el.get('option') or {}
props = new_el.get('props') or {}
print('option.filterRule:', json.dumps(opt.get('filterRule'), ensure_ascii=False, indent=1))
print('option keys:', list(opt.keys()))
print('props.colors:', json.dumps(props.get('colors'), ensure_ascii=False))
print('props.enhance:', json.dumps(props.get('enhance'), ensure_ascii=False)[:500])
print('props.columns:', json.dumps(props.get('columns'), ensure_ascii=False, indent=1)[:1500])

# full option/props diff vs old
import difflib
for name in ('option', 'props'):
    a = json.dumps(old_el.get(name), ensure_ascii=False, indent=1).splitlines()
    b = json.dumps(new_el.get(name), ensure_ascii=False, indent=1).splitlines()
    diff = list(difflib.unified_diff(a, b, lineterm=''))
    print()
    print(f'=== {name} diff ({len(diff)} lines) ===')
    for l in diff[:80]:
        print(l)

# events diff
print()
print('events old:', json.dumps(old_el.get('events'), ensure_ascii=False))
print('events new:', json.dumps(new_el.get('events'), ensure_ascii=False))
