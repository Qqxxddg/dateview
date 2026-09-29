# -*- coding: utf-8 -*-
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
PATH = r'D:\dataview-workspace\DataView_DataMeta_Server_TAS接口服务等_7_20260929093032.dv.json'
data = json.load(open(PATH, encoding='utf-8'))
print('top type:', type(data), 'len:', len(data) if isinstance(data, (list, dict)) else '-')

# find SQL09091542 / SQL21343641 definitions
raw = open(PATH, encoding='utf-8').read()
for sid in ['SQL09091542', 'SQL21343641']:
    idx = raw.find(sid)
    print(sid, 'first idx:', idx)

# structural walk
def find_nodes(o, key_hits, path='$'):
    out = []
    if isinstance(o, dict):
        sid = o.get('sourceId') or o.get('id') or o.get('code')
        if sid in key_hits:
            out.append((path, o))
        for k, v in o.items():
            out += find_nodes(v, key_hits, path + '.' + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            out += find_nodes(v, key_hits, path + f'[{i}]')
    return out

nodes = find_nodes(data, {'SQL09091542', 'SQL21343641'})
print('found nodes:', len(nodes))
for p, n in nodes[:4]:
    print()
    print('PATH:', p)
    # print key fields without huge blobs first
    for k in ['sourceId', 'id', 'name', 'code', 'type', 'resultFormat', 'inputParams', 'outputParams']:
        if k in n:
            print(k, ':', json.dumps(n[k], ensure_ascii=False)[:800])
    for k in ['sql', 'sqlText', 'content', 'definition', 'script', 'params']:
        if k in n:
            v = n[k]
            s = v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)
            print(k, '(len', len(s), ') :', s[:1500])
