# -*- coding: utf-8 -*-
import json, sys, re
sys.stdout.reconfigure(encoding='utf-8')
PATH = r'D:\dataview-workspace\DataView_布局文件[0-统计看板].dv.json'
with open(PATH, encoding='utf-8') as f:
    raw = f.read()

fields = sorted(set(re.findall(r'[a-z_]*status[a-z_]*', raw, re.I)))
print('status fields:', fields)
print('运行/空闲/充电/异常/离线 counts:', raw.count('运行'), raw.count('空闲'), raw.count('充电'), raw.count('异常'), raw.count('离线'))

data = json.loads(raw)
content = json.loads(data[0]['content'])
print('content keys:', list(content.keys()))

# text / multilingual definitions
for key in content:
    if 'text' in key.lower() or 'lang' in key.lower() or 'i18n' in key.lower():
        v = json.dumps(content[key], ensure_ascii=False)
        print(key, '=>', v[:2000])

# top-level data[0] keys besides content
print('data[0] keys:', list(data[0].keys()))
for k in data[0]:
    if k != 'content':
        v = json.dumps(data[0][k], ensure_ascii=False)
        print(k, '=>', v[:1000])
