# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
s = open(r'D:\dataview-workspace\DataView_SQL_ID_前端调用手册.md', encoding='utf-8').read()

idx = s.find('### 4.2')
print(s[idx:idx+2500])
print()
print('=' * 60)

for sid in ['SQL09091542', 'SQL21343641', 'SQL09371021']:
    # find all occurrences
    occ = [m.start() for m in re.finditer(re.escape(sid), s)]
    print()
    print('####', sid, 'hits:', occ)
    # print the richest occurrence: prefer one in a details table with SQL text
    shown = 0
    for i in occ:
        chunk = s[max(0, i - 100):i + 1000]
        if 'select' in chunk.lower() or '入参' in chunk or 'status2' in chunk:
            print('--- at', i, '---')
            print(chunk)
            shown += 1
            if shown >= 2:
                break
