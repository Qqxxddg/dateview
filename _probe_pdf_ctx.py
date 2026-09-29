# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
s = open(r'D:\dataview-workspace\_dataview_manual_full.txt', encoding='utf-8').read()
print('--- 默认数据 contexts ---')
for m in re.finditer('默认数据', s):
    i = m.start()
    print(s[max(0,i-200):i+200].replace('\n', ' '))
    print('====')
print()
print('--- 表格 sample contexts (first 6) ---')
c = 0
for m in re.finditer('表格', s):
    i = m.start()
    chunk = s[max(0,i-120):i+120].replace('\n', ' ')
    print(chunk)
    print('----')
    c += 1
    if c >= 6: break
print()
print('--- head 1500 ---')
print(s[:1500])
