# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
PATH = r'D:\dataview-workspace\DataView_布局文件[0-统计看板].dv.json'
outer = json.load(open(PATH, encoding='utf-8'))
content = json.loads(outer[0]['content'])
page = content['pages'][0]
el = next(e for e in page['elements'] if e.get('refName') == '#card7')
print('element keys:', list(el.keys()))
for k, v in el.items():
    if k in ('props', 'option', 'events'):
        print(f'--- {k} ---')
        print(json.dumps(v, ensure_ascii=False, indent=1)[:2500])
    else:
        print(k, '=', json.dumps(v, ensure_ascii=False)[:200])

# chargedata events for reference
el2 = next(e for e in page['elements'] if e.get('refName') == '#chargedata')
print()
print('chargedata element keys:', list(el2.keys()))
print('chargedata events:', json.dumps(el2.get('events'), ensure_ascii=False))
print('chargedata defaultValue:', (el2.get('option') or {}).get('defaultValue', '')[:200])

# locales tail
locs = content['locales']
print()
print('locales n:', len(locs), '| last 3:', json.dumps(locs[-3:], ensure_ascii=False))
