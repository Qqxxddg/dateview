# -*- coding: utf-8 -*-
import json, sys, re
sys.stdout.reconfigure(encoding='utf-8')
PATH = r'D:\dataview-workspace\DataView_布局文件[0-统计看板].dv.json'
with open(PATH, encoding='utf-8') as f:
    data = json.load(f)
content = json.loads(data[0]['content'])
page = content['pages'][0]

# all sources incl. component-level: scan postHandlers/preHandlers for status-related keywords
def scan_sources(srcs, owner):
    for s in srcs or []:
        txt = json.dumps(s, ensure_ascii=False)
        flags = []
        for kw in ['amr_code', 'status', '运行', '空闲', '离线', '异常', '充电']:
            c = txt.count(kw)
            if c: flags.append(f'{kw}x{c}')
        print(owner, '|', s.get('source'), '|', ','.join(flags) if flags else '-')

scan_sources(page.get('sources'), 'page')
for e in page['elements']:
    opt = e.get('option') or {}
    if isinstance(opt, dict) and opt.get('sources'):
        scan_sources(opt.get('sources'), e.get('refName'))

# charging data postHandler: what fields per row
el = next(e for e in page['elements'] if e.get('refName') == '#chargedata')
src = (el['option']['sources'] or [])[0]
print()
print('chargedata postHandler:')
print(src.get('postHandler', '')[:1500])
