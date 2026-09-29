# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
s = open(r'D:\dataview-workspace\_dataview_manual_full.txt', encoding='utf-8').read()
# find chapter content positions
for m in ['3.2.3', '表格元件', '表格属性', '查询表格', '样式']:
    idx = s.find(m, 2000)  # skip TOC
    print(m, '->', idx)

# print from 表格元件 section onwards (second occurrence, past TOC)
i = s.find('表格元件', 3000)
j = s.find('图表元件', i) if i > 0 else -1
print()
print('=== 3.2.3 表格元件 章节 ===')
print(s[i:i+3500] if i > 0 else 'not found')
print()
i2 = s.find('表格属性', 3000)
print('=== 表格属性 章节 ===')
print(s[i2:i2+3500] if i2 > 0 else 'not found')
