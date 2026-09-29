import json
import re
from collections import defaultdict, Counter

path = r"D:\dataview-workspace\DataView_DataMeta_Server_TAS接口服务等_7_20260929093032.dv.json"
data = json.load(open(path, encoding="utf-8"))

# collect all sources with server
rows = []
for s in data:
    sname = s.get("serverName")
    for src in s.get("sources") or []:
        content = src.get("content") or ""
        rows.append(
            {
                "server": sname,
                "id": src.get("sourceId") or src.get("id"),
                "name": src.get("sourceName") or "",
                "content": content,
            }
        )

print("total sources:", len(rows))

# extract table names from SQL
table_pat = re.compile(
    r"(?:from|join|FROM|JOIN)\s+([a-zA-Z_][a-zA-Z0-9_]*)", re.I
)
tables = Counter()
by_table = defaultdict(list)
for r in rows:
    found = set(table_pat.findall(r["content"]))
    for t in found:
        if t.lower() in ("select", "case", "when", "then", "else", "end", "as", "and", "or", "on", "left", "inner", "outer", "full", "union", "where", "group", "order", "by", "limit", "with", "distinct", "generate_series"):
            continue
        tables[t] += 1
        by_table[t].append(f"{r['id']}|{r['name']}")

print("\n=== 表出现次数 TOP ===")
for t, c in tables.most_common(30):
    print(f"  {t}: {c}")

# classify by keyword in name/content
categories = {
    "设备/AMR状态": ["设备", "AMR", "amr", "status", "状态", "运行", "开动率", "在线"],
    "任务/工单": ["任务", "task", "TASK", "工单", "子任务"],
    "告警/故障": ["告警", "故障", "alarm", "fault", "ALARM", "FAULT", "MTBF", "MTTR"],
    "充电": ["充电", "charge", "battery", "电量"],
    "地图/站点": ["地图", "map", "站点", "site", "区域"],
    "班次/时间": ["班次", "period", "时间", "time", "时段"],
    "效率/统计看板": ["效率", "统计", "看板", "趋势", "TOP"],
    "下拉/字典": ["下拉", "字典", "列表", "获取"],
}

def classify(name, content):
    text = name + " " + content[:200]
    hits = []
    for cat, kws in categories.items():
        if any(k in text for k in kws):
            hits.append(cat)
    return hits or ["其他"]

cat_map = defaultdict(list)
for r in rows:
    for c in classify(r["name"], r["content"]):
        cat_map[c].append(r)

print("\n=== 按业务主题（可重叠） ===")
for cat, items in sorted(cat_map.items(), key=lambda x: -len(x[1])):
    print(f"\n## {cat} ({len(items)})")
    for r in items[:8]:
        sql1 = re.sub(r"\s+", " ", r["content"])[:90]
        print(f"   {r['id']} | {r['name']} | {r['server'][:12]}")
        print(f"      {sql1}...")
    if len(items) > 8:
        print(f"   ... 另有 {len(items)-8} 条")

# show full SQL of the 3 status-related ones
print("\n\n======== 关键语句全文 ========")
for want in ["SQL1818567", "SQL09091542", "SQL10255922", "SQL21343641"]:
    for r in rows:
        if r["id"] == want:
            print(f"\n----- {r['id']} | {r['name']} | {r['server']} -----")
            print(r["content"][:1500])
            break
