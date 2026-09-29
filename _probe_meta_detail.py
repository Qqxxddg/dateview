import json
from collections import defaultdict

path = r"D:\dataview-workspace\DataView_DataMeta_Server_TAS接口服务等_7_20260929093032.dv.json"
data = json.load(open(path, encoding="utf-8"))

print(f"servers: {len(data)}\n")
for i, s in enumerate(data):
    print("=" * 70)
    print(f"[{i}] serverName = {s.get('serverName')}")
    print(f"    serverId   = {s.get('serverId')}")
    print(f"    serverType = {s.get('serverType')} / sub={s.get('subServerType')}")
    print(f"    host:port  = {s.get('host')}:{s.get('port')}")
    print(f"    endpoint   = {s.get('endpoint')}")
    print(f"    username   = {s.get('username')}")
    print(f"    password   = {'***set***' if s.get('password') else '(empty)'}")
    print(f"    status     = {s.get('status')}  remark={s.get('remark')}")
    opt = s.get("option")
    if opt:
        print(f"    option     = {str(opt)[:300]}")
    srcs = s.get("sources") or []
    print(f"    sources    = {len(srcs)}")
    # group by type
    types = defaultdict(list)
    for src in srcs:
        types[src.get("dataType") or src.get("type") or "?"].append(src)
    for t, items in types.items():
        print(f"      type={t}: {len(items)}")
    # print each source: id, name, brief content
    for src in srcs:
        sid = src.get("source") or src.get("sourceId") or src.get("id")
        name = src.get("sourceName") or src.get("name") or ""
        dt = src.get("dataType") or src.get("type") or ""
        content = (src.get("content") or src.get("sql") or "").replace("\n", " ")
        if len(content) > 100:
            content = content[:100] + "..."
        keys = list(src.keys())
        print(f"      - {sid} | {name} | {dt} | {content}")
    if i == 0:
        print("    [first source keys]", list((srcs[0] if srcs else {}).keys()))
