# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
PATH = r'D:\dataview-workspace\DataView_布局文件[0-统计看板].dv.json'
with open(PATH, encoding='utf-8') as f:
    data = json.load(f)
content = json.loads(data[0]['content'])
script = content['pages'][0]['script']

for name in ['onChargeRowClick', 'onTaskRowClick']:
    idx = script.find(name)
    print('===', name, 'at', idx, '===')
    if idx >= 0:
        print(script[idx:idx+800])
    print()

# search whole raw for filterRule with non-empty style/sort, colors non-empty, enhance usage
raw = data[0]['content']
import re
# find "style": [ ... ] non-empty in filterRule context
for m in re.finditer(r'"filterRule":\s*\{[^}]*\}', raw):
    s = m.group(0)
    if '"style": [' in s and '"style": []' not in s or '"sort": [' in s and '"sort": []' not in s:
        print('filterRule sample:', s[:500])
        break
else:
    print('no non-empty filterRule found in raw')

# colors non-empty
for m in re.finditer(r'"colors":\s*\[(?!\])[^\]]*\]', raw):
    print('colors sample:', m.group(0)[:300])
    break
else:
    print('no non-empty colors found')

# enhance non-empty
for m in re.finditer(r'"enhance":\s*"(?!")[^"]{5,400}"', raw):
    print('enhance sample:', m.group(0)[:400])
    break
else:
    print('no non-empty enhance found')
