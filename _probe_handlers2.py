# -*- coding: utf-8 -*-
import json, sys, re
sys.stdout.reconfigure(encoding='utf-8')
PATH = r'D:\dataview-workspace\DataView_布局文件[0-统计看板].dv.json'
with open(PATH, encoding='utf-8') as f:
    data = json.load(f)
content = json.loads(data[0]['content'])

# search recursively for handler definitions
hits = []
def walk(o, path=''):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ('handlers', 'events', 'script', 'enhance') and isinstance(v, (str, list, dict)):
                s = json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v
                if 'onCard7Click' in s or 'RefreshHzForAmr' in s:
                    hits.append((path + '/' + k, s[:500]))
            walk(v, path + '/' + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, path + f'[{i}]')
    elif isinstance(o, str):
        if 'onCard7Click' in o and 'function' in o:
            hits.append((path, o[:600]))

walk(content)
for p, s in hits[:10]:
    print('PATH:', p)
    print(s[:600])
    print('---')

# find RefreshHzForAmr constant definition anywhere
raw = data[0]['content']
idx = raw.find('RefreshHzForAmr')
print('RefreshHzForAmr first idx:', idx)
print(raw[max(0,idx-200):idx+200])
