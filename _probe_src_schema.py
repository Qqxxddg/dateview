# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
PATH = r'D:\dataview-workspace\DataView_布局文件[0-统计看板].dv.json'
outer = json.load(open(PATH, encoding='utf-8'))
content = json.loads(outer[0]['content'])
el = next(e for e in content['pages'][0]['elements'] if e.get('refName') == '#chargedata')
src = (el['option']['sources'] or [])[0]
print('source keys:', list(src.keys()))
print(json.dumps(src, ensure_ascii=False, indent=1)[:4000])
