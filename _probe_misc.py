# -*- coding: utf-8 -*-
import json, sys, re
sys.stdout.reconfigure(encoding='utf-8')
PATH = r'D:\dataview-workspace\DataView_布局文件[0-统计看板].dv.json'
with open(PATH, encoding='utf-8') as f:
    data = json.load(f)
raw = data[0]['content']
content = json.loads(raw)
page = content['pages'][0]

print('beforeSourceQuery_1 count in raw:', raw.count('beforeSourceQuery_1'))
# who references it
for s in page['sources']:
    if s.get('preHandler') == 'beforeSourceQuery_1':
        print('  page source uses it:', s.get('source'))
# definition location
script = page['script']
idx = script.find('beforeSourceQuery_1')
print('in page script at:', idx)
if idx >= 0:
    print(script[idx:idx+500])

# 暂无数据
print()
print('暂无数据 count:', raw.count('暂无数据'))
print('无数据 count:', raw.count('无数据'))

# locales keys list
locs = content.get('locales') or []
print()
print('locale keys:', [l.get('key') for l in locs])
# does any locale have 暂无
for l in locs:
    if '暂无' in json.dumps(l, ensure_ascii=False):
        print('locale with 暂无:', l)
