# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

PATH = r'C:\Users\acer\Desktop\DataView_布局文件[0-统计看板].dv.json'
with open(PATH, encoding='utf-8') as f:
    data = json.load(f)
content = json.loads(data[0]['content'])
page = content['pages'][0]
els = page['elements']

def short(v, n=180):
    s = json.dumps(v, ensure_ascii=False) if not isinstance(v, str) else v
    return s if len(s) <= n else s[:n] + '...'

for i, e in enumerate(els):
    el = e.get('elName')
    title = e.get('title')
    ref = e.get('refName')
    layout = e.get('layout')
    opt = e.get('option') or {}
    props = e.get('props') or {}
    print(f'--- [{i}] {ref} | elName={el} | title={title}')
    print(f'    layout={short(layout, 300)}')
    # option summary
    if isinstance(opt, dict):
        keys = list(opt.keys())
        print(f'    option keys={keys[:25]}')
        for k in ('type','chartType','title','text','data','sources','binds','series','columns','rows','xAxis','yAxis'):
            if k in opt:
                print(f'      {k}={short(opt[k])}')
    if isinstance(props, dict) and props:
        print(f'    props={short(props, 400)}')
    ev = e.get('events')
    if ev:
        print(f'    events={short(ev, 300)}')
    print()
