# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
PATH = r'D:\dataview-workspace\DataView_布局文件[0-统计看板].dv.json'
with open(PATH, encoding='utf-8') as f:
    data = json.load(f)
content = json.loads(data[0]['content'])
page = content['pages'][0]

for ref in ['#chargedata', '#taskavgdata']:
    el = next(e for e in page['elements'] if e.get('refName') == ref)
    print('=' * 30, ref, '=' * 30)
    print('elName:', el.get('elName'), '| id:', el.get('id'))
    print('layout:', json.dumps(el.get('layout'), ensure_ascii=False))
    print('events:', json.dumps(el.get('events'), ensure_ascii=False))
    print('props:')
    print(json.dumps(el.get('props'), ensure_ascii=False, indent=1))
    opt = el.get('option') or {}
    print('option keys:', list(opt.keys()))
    srcs = opt.get('sources') or []
    for s in srcs:
        print(' source:', s.get('source'), '| type:', s.get('type'), '| interval:', s.get('interval'), '| map:', s.get('map'))
        print('  preHandler:', (s.get('preHandler') or '')[:300])
        print('  postHandler:', (s.get('postHandler') or '')[:300])
    print(' other option:', json.dumps({k: v for k, v in opt.items() if k != 'sources'}, ensure_ascii=False)[:800])
    print()
