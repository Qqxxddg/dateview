# -*- coding: utf-8 -*-
import json, sys, re
sys.stdout.reconfigure(encoding='utf-8')
PATH = r'D:\dataview-workspace\DataView_布局文件[0-统计看板].dv.json'
with open(PATH, encoding='utf-8') as f:
    data = json.load(f)
content = json.loads(data[0]['content'])

loc = content.get('locales')
print('locales type:', type(loc))
if isinstance(loc, dict):
    for k, v in list(loc.items())[:5]:
        print(' locale', k, type(v), (list(v.keys())[:20] if isinstance(v, dict) else str(v)[:200]))
    # find keys of interest
    zh = loc.get('zh-CN') or loc.get('zh') or {}
    if isinstance(zh, dict):
        for key in ['deviceStatus', 'abnormal', 'offline', 'numT', 't1_amr_code', 't1_map_code']:
            print(' ', key, '=>', zh.get(key))
elif isinstance(loc, list):
    print(json.dumps(loc, ensure_ascii=False)[:3000])

# statusName occurrences context
raw = data[0]['content']
idx = raw.find('statusName')
print()
print('statusName context:', raw[max(0,idx-300):idx+300].replace('\\n', ' ')[:600])
