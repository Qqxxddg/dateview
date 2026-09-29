# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
PATH = r'D:\dataview-workspace\DataView_布局文件[0-统计看板].dv.json'
with open(PATH, encoding='utf-8') as f:
    data = json.load(f)
content = json.loads(data[0]['content'])
script = content['pages'][0]['script']
print('page script len:', len(script))

for name in ['onCard7Click', 'initDeviceRealTime']:
    idx = script.find(name)
    print()
    print('===', name, 'at', idx, '===')
    if idx >= 0:
        print(script[idx:idx+1200])

# constants definition for RefreshHzForAmr
raw = data[0]['content']
idx = raw.find('"RefreshHzForAmr"')
print()
print('RefreshHzForAmr def idx:', idx)
if idx >= 0:
    print(raw[idx-100:idx+200])
# maybe in model
model = content.get('model')
print()
print('model:', json.dumps(model, ensure_ascii=False)[:800] if model else None)
