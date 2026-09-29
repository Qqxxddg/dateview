import json

path = r"D:\dataview-workspace\DataView_DataMeta_Server_TAS接口服务等_7_20260929093032.dv.json"
data = json.load(open(path, encoding="utf-8"))

# find a few sources with inputParams populated
shown = 0
for s in data:
    for src in s.get("sources") or []:
        ip = src.get("inputParams")
        op = src.get("outputParams")
        if ip or op:
            print("sourceId:", src.get("sourceId"), "|", src.get("sourceName"))
            print("  inputParams type:", type(ip).__name__, "value:", json.dumps(ip, ensure_ascii=False)[:500] if ip else None)
            print("  outputParams type:", type(op).__name__, "value:", json.dumps(op, ensure_ascii=False)[:500] if op else None)
            print()
            shown += 1
            if shown >= 8:
                break
    if shown >= 8:
        break

# also check full source key sample for SQL1818567 and SQL09091542
for want in ["SQL1818567", "SQL09091542"]:
    for s in data:
        for src in s.get("sources") or []:
            if src.get("sourceId") == want:
                print("==== FULL KEYS", want, "====")
                for k, v in src.items():
                    if k in ("content",):
                        print(f"  {k}: <sql len={len(v or '')}>")
                    else:
                        print(f"  {k}: {json.dumps(v, ensure_ascii=False)[:300] if not isinstance(v, str) else v[:300]}")
