# -*- coding: utf-8 -*-
import json, re, sys
sys.stdout.reconfigure(encoding='utf-8')

PATH = r'C:\Users\acer\Desktop\DataView_布局文件[0-统计看板].dv.json'
with open(PATH, encoding='utf-8') as f:
    data = json.load(f)
content = json.loads(data[0]['content'])
page = content['pages'][0]

script = page.get('script') or ''
print('=== PAGE SCRIPT: function list ===')
for m in re.finditer(r'^\s*(?:async\s+)?(?:function\s+(\w+)|(\w+)\s*[=:]\s*(?:async\s*)?(?:function|\())', script, re.M):
    name = m.group(1) or m.group(2)
    line = script[:m.start()].count('\n') + 1
    print(f'  L{line}: {name}')

# onXxx handlers
print()
print('=== methods / handlers (this.onXxx =) ===')
for m in re.finditer(r'(?:this\.)?(on[A-Z]\w+)\s*[=:]\s*', script):
    pass
names = sorted(set(re.findall(r'\b(on[A-Z]\w+)\s*[=:]', script)))
print(names)

print()
print('=== $constant / model refs ===')
consts = sorted(set(re.findall(r'constant\.(\w+)', script)))
print('constants:', consts)
models = sorted(set(re.findall(r"\$model\(\s*['\"](\w+)['\"]", script)))
print('models referenced:', models)
sqls = sorted(set(re.findall(r"SQL\d+", script)))
print('SQLs in script:', sqls)

print()
print('=== PAGE-LEVEL SOURCES detail ===')
for s in page.get('sources') or []:
    print('-', s.get('id'), s.get('source'), 'interval:', s.get('interval'))
    print('  preHandler:', (s.get('preHandler') or '')[:400].replace('\n', ' | '))
    print('  handler:', s.get('handler'))
    print('  binds:', [b.get('refName') for b in (s.get('binds') or [])])
    print('  params:', json.dumps(s.get('params'), ensure_ascii=False)[:300])

print()
print('=== element option.sources (local) ===')
for i, e in enumerate(page['elements']):
    opt = e.get('option') or {}
    for s in (opt.get('sources') or []):
        print(f'[{i}] {e.get("refName")} -> {s.get("source")} interval={s.get("interval")}')
        ph = s.get('preHandler') or ''
        if ph:
            print('   preHandler:', ph[:350].replace('\n', ' | '))
        bh = s.get('binds') or []
        for b in bh:
            print('   bind ->', b.get('refName'), '| template len:', len(b.get('template') or ''))
