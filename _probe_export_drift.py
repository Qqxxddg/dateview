# -*- coding: utf-8 -*-
"""全局对比导出文件与工作区文件，评估漂移规模"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
NEW = r'D:\dataview-workspace\DataView_布局文件[0-统计看板].dv1.json'
OLD = r'D:\dataview-workspace\DataView_布局文件[0-统计看板].dv.json'

def load(p):
    o = json.load(open(p, encoding='utf-8'))
    return o, json.loads(o[0]['content'])

no, nc = load(NEW)
oo, oc = load(OLD)

# outer metadata
for k in no[0]:
    if no[0].get(k) != oo[0].get(k) and k != 'content':
        print('outer diff', k, ':', str(oo[0].get(k))[:80], '->', str(no[0].get(k))[:80])

# content top-level
for k in set(list(nc.keys()) + list(oc.keys())):
    a, b = json.dumps(oc.get(k), ensure_ascii=False, sort_keys=True), json.dumps(nc.get(k), ensure_ascii=False, sort_keys=True)
    if a != b:
        print('content key diff:', k, 'len', len(a), '->', len(b))

# elements-by-refName diff
def els(c):
    return {e.get('refName'): e for e in c['pages'][0]['elements']}
eo, en = els(oc), els(nc)
print('elements n:', len(eo), '->', len(en))
for ref in sorted(set(eo) | set(en)):
    a = json.dumps(eo.get(ref), ensure_ascii=False, sort_keys=True)
    b = json.dumps(en.get(ref), ensure_ascii=False, sort_keys=True)
    if a != b:
        print('element diff:', ref, '(old len', len(a), 'new len', len(b), ')')

# pages script / sources
po, pn = oc['pages'][0], nc['pages'][0]
print('script same:', po.get('script') == pn.get('script'))
print('sources same:', json.dumps(po.get('sources'), sort_keys=True) == json.dumps(pn.get('sources'), sort_keys=True))
print('content.option.sources same:', json.dumps(oc['option'].get('sources'), sort_keys=True) == json.dumps(nc['option'].get('sources'), sort_keys=True))
print('locales same:', json.dumps(oc.get('locales'), sort_keys=True) == json.dumps(nc.get('locales'), sort_keys=True))
