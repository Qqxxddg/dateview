import re

raw = open(r"D:\dataview-workspace\DataView_布局文件[0-统计看板].dv.json", encoding="utf-8").read()
ids = sorted(set(re.findall(r"SQL\d+", raw)))
print("SQL IDs:", ids)
print("--- source fields ---")
for m in re.finditer(r'"source"\s*:\s*"(SQL[^"]+)"', raw):
    ctx = raw[max(0, m.start() - 80) : m.end() + 40].replace("\n", " ")
    print(ctx[:220])
    print()
