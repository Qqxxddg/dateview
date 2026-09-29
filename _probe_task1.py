# -*- coding: utf-8 -*-
"""任务1取证：content.option.sources vs pages[0].sources 权威性判定"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
PATH = r'D:\dataview-workspace\DataView_布局文件[0-统计看板].dv.json'
data = json.load(open(PATH, encoding='utf-8'))
content = json.loads(data[0]['content'])
page = content['pages'][0]

print('=== 1. 结构归属 ===')
print('content.script len:', len(content.get('script') or ''))
print('pages[0].script len:', len(page.get('script') or ''))
print('content.option keys:', list((content.get('option') or {}).keys()))
print('pages[0] keys:', list(page.keys()))
print('pages[0].option keys:', list((page.get('option') or {}).keys()))
print('content.option.sources n:', len((content.get('option') or {}).get('sources') or []))
print('pages[0].sources n:', len(page.get('sources') or []))
print('pages[0].elements n:', len(page.get('elements') or []))
print('content has elements?', 'elements' in content)
print('content.version:', content.get('version'), '| content.type:', content.get('type'))

print()
print('=== 2. 惯用法演进（binds 写法）===')
a = content['option']['sources']
b = page['sources']
for x, y in zip(a, b):
    xt, yt = json.dumps(x.get('binds'), ensure_ascii=False), json.dumps(y.get('binds'), ensure_ascii=False)
    if xt != yt:
        xa = 'setData调用' if '.setData(' in xt and 'return' not in xt.split('setData')[0][-30:] else ''
        # simpler flags
        def flags(t):
            f = []
            if 'card.setData(' in t and '// let card' not in t and '//card.setData' not in t:
                f.append('直接setData')
            if 'return data' in t:
                f.append('return data')
            if 'options.content =' in t:
                f.append('options.content=')
            if '$param(' in t:
                f.append('$param()')
            return ','.join(f)
        print(f"{x.get('source')}: content.option[{flags(xt)}]  vs  pages[0][{flags(yt)}]")

print()
print('=== 3. 页面脚本中与 card7/sources 相关的初始化 ===')
script = page.get('script') or ''
idx = script.find('initDeviceRealTime =')
if idx >= 0:
    print(script[idx:idx+900])
print()
print('SQL1818567 in script:', script.count('SQL1818567'))
print('card.setData in script:', script.count('card.setData'))
print('setData( in script:', script.count('.setData('))

print()
print('=== 4. 两列表 source 顺序与 id 是否一致 ===')
print('content ids:', [s.get('id') for s in a])
print('pages   ids:', [s.get('id') for s in b])
print('same id order:', [s.get('id') for s in a] == [s.get('id') for s in b])
