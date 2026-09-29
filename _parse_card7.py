# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

PATH = r'C:\Users\acer\Desktop\DataView_布局文件[0-统计看板].dv.json'
with open(PATH, encoding='utf-8') as f:
    data = json.load(f)
content = json.loads(data[0]['content'])
page = content['pages'][0]

# card7 element
el = next(e for e in page['elements'] if e.get('refName') == '#card7')
print('=== #card7 element ===')
print('elName:', el.get('elName'), '| title:', el.get('title'), '| layout:', el.get('layout'))
print('--- props ---')
print(json.dumps(el.get('props'), ensure_ascii=False, indent=1))
print('--- option ---')
print(json.dumps(el.get('option'), ensure_ascii=False, indent=1))
print('--- events ---')
print(json.dumps(el.get('events'), ensure_ascii=False, indent=1))

# the source bound to card7: SQL1818567
print()
print('=== source SQL1818567 (page level) ===')
src = next(s for s in page['sources'] if s.get('source') == 'SQL1818567')
print(json.dumps(src, ensure_ascii=False, indent=1))
