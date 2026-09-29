# -*- coding: utf-8 -*-
import json, sys, re
sys.stdout.reconfigure(encoding='utf-8')
PATH = r'D:\dataview-workspace\DataView_布局文件[0-统计看板].dv.json'
with open(PATH, encoding='utf-8') as f:
    data = json.load(f)
content = json.loads(data[0]['content'])
script = content.get('script') or ''
print('page script len:', len(script))

for name in ['onCard7Click', 'deviceStatusCallback', 'RefreshHzForAmr', 'beforeSourceQuery_1']:
    idx = script.find(name)
    print()
    print('===', name, 'at', idx, '===')
    if idx >= 0:
        print(script[idx:idx+700])

# constants / model
opt = content['option']
print()
print('page option keys:', list(opt.keys()) if isinstance(opt, dict) else type(opt))
if isinstance(opt, dict):
    consts = opt.get('constants') or {}
    print('constants:', json.dumps(consts, ensure_ascii=False)[:800])
