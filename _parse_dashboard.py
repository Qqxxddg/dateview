# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

PATH = r'C:\Users\acer\Desktop\DataView_布局文件[0-统计看板].dv.json'
with open(PATH, encoding='utf-8') as f:
    data = json.load(f)
content = json.loads(data[0]['content'])
page = content['pages'][0]

print('page name:', page['name'], 'size:', page['width'], 'x', page['height'])
print('page option:', json.dumps(page.get('option'), ensure_ascii=False)[:1500])
print('page sources count:', len(page.get('sources') or []))
print('page script len:', len(page.get('script') or ''))
print('events:', json.dumps(page.get('events'), ensure_ascii=False)[:500])
print('extendStyle:', json.dumps(page.get('extendStyle'), ensure_ascii=False)[:500])
print('defaultForm:', json.dumps(page.get('defaultForm'), ensure_ascii=False)[:800])
print()

els = page['elements']
print('elements count:', len(els))
for i, e in enumerate(els):
    if not isinstance(e, dict):
        print(f'[{i}] NON-DICT {type(e)}')
        continue
    t = e.get('type')
    eid = e.get('id')
    ref = e.get('refName')
    title = e.get('name') or e.get('title') or ''
    box = (e.get('x'), e.get('y'), e.get('width'), e.get('height'))
    # try to get inner component type
    inner = e.get('option', {})
    itype = ''
    if isinstance(inner, dict):
        itype = inner.get('type') or inner.get('chartType') or ''
    label = ''
    if isinstance(inner, dict):
        label = inner.get('title') or inner.get('text') or ''
    print(f'[{i}] type={t} innerType={itype} id={eid} ref={ref} box={box} title={label!r}')
