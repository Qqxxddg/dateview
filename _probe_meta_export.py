import json
import re
from collections import Counter

path = r"D:\dataview-workspace\DataView_DataMeta_Server_TAS接口服务等_7_20260929093032.dv.json"
raw = open(path, encoding="utf-8").read()

# top-level structure
try:
    data = json.loads(raw)
    print("type:", type(data).__name__)
    if isinstance(data, dict):
        print("top keys:", list(data.keys())[:40])
        for k, v in data.items():
            if isinstance(v, list):
                print(f"  {k}: list len={len(v)}")
            elif isinstance(v, dict):
                print(f"  {k}: dict keys={list(v.keys())[:20]}")
            else:
                s = str(v)
                print(f"  {k}: {type(v).__name__} = {s[:120]}")
    elif isinstance(data, list):
        print("list len:", len(data))
        if data:
            print("first item type:", type(data[0]).__name__)
            if isinstance(data[0], dict):
                print("first item keys:", list(data[0].keys())[:30])
except Exception as e:
    print("json load failed:", e)
    print("head:", raw[:500])

# SQL ids
ids = sorted(set(re.findall(r"SQL\d+", raw)))
print("\nSQL IDs count:", len(ids))
print("SQL IDs:", ids[:50])

# look for jdbc / connection related strings
for kw in ["jdbc", "JDBC", "postgres", "oracle", "password", "username", "host", "port", "database", "ip", "服务", "数据源"]:
    c = raw.count(kw)
    if c:
        print(f"count[{kw}] = {c}")
