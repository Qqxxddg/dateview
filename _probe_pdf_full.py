# -*- coding: utf-8 -*-
"""从 dataview-config-manual.pdf 全文提取中搜 scrolltable 相关文档"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

try:
    import pypdfium2 as pdfium
except ImportError:
    print('pypdfium2 missing'); raise SystemExit(1)

PDF = r'D:\dataview-workspace\dataview-config-manual.pdf'
doc = pdfium.PdfDocument(PDF)
print('pages:', len(doc))
texts = []
for i in range(len(doc)):
    try:
        t = doc[i].get_textpage().get_text_range()
    except Exception:
        t = ''
    texts.append(t)
full = '\n'.join(texts)
open(r'D:\dataview-workspace\_dataview_manual_full.txt', 'w', encoding='utf-8').write(full)
print('extracted chars:', len(full))
for kw in ['scrolltable', '滚动', 'defaultValue', '默认数据', 'filterRule', 'enhance', 'showStyle', '样式1', 'colors', '表格']:
    print(kw, '=>', full.count(kw))
