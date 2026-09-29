import json
import re
from collections import defaultdict

path = r"D:\dataview-workspace\DataView_DataMeta_Server_TAS接口服务等_7_20260929093032.dv.json"
out = r"D:\dataview-workspace\DataView_SQL_ID_前端调用手册.md"
data = json.load(open(path, encoding="utf-8"))


def brief_sql(content: str, n=140) -> str:
    s = re.sub(r"\s+", " ", content or "").strip()
    return s if len(s) <= n else s[:n] + "..."


def parse_params(raw):
    if not raw:
        return []
    items = raw
    if isinstance(raw, str):
        try:
            items = json.loads(raw)
        except Exception:
            return []
    if isinstance(items, dict):
        items = [items]
    if not isinstance(items, list):
        return []
    result = []
    for p in items:
        if not isinstance(p, dict):
            if isinstance(p, str):
                result.append(p)
            continue
        name = p.get("field") or p.get("name") or p.get("paramName") or p.get("code") or ""
        typ = p.get("type") or ""
        default = p.get("value") if p.get("value") is not None else p.get("defaultValue")
        text = p.get("text") or ""
        result.append({"name": name, "type": typ, "default": default, "text": text})
    return result


def fmt_params(params, with_text=True):
    if not params:
        return "—"
    parts = []
    for p in params:
        name = p.get("name") or "?"
        bit = f"`{name}`"
        if p.get("text") and with_text:
            bit += f"({p['text']})"
        if p.get("type"):
            bit += f":{p['type']}"
        if p.get("default") not in (None, ""):
            bit += f"={p['default']}"
        parts.append(bit)
    return ", ".join(parts)


param_pat = re.compile(r"\$\{([a-zA-Z_][a-zA-Z0-9_]*)\}")


def content_params(content: str):
    seen, outl = set(), []
    for m in param_pat.finditer(content or ""):
        if m.group(1) not in seen:
            seen.add(m.group(1))
            outl.append(m.group(1))
    return outl


def category_of(name, content):
    # name weighs more than sql body
    name_l = (name or "").lower()
    rules = [
        ("充电/电量", ["充电", "charge", "电量", "耗电", "battery", "充电桩"]),
        ("告警/故障", ["告警", "故障", "alarm", "fault", "mtbf", "mttr"]),
        ("班次/时间范围", ["班次", "period", "时间查询", "时间段", "同班次", "生产计划"]),
        ("设备状态/开动率", ["设备", "amr", "运行", "开动", "在线", "状态", "分布", "实时", "robot", "agv"]),
        ("任务统计", ["任务", "task", "工单", "子任务", "tAS_".lower(), "trp"]),
        ("地图/站点/热力", ["地图", "map", "站点", "热力", "区域", "坐标", "site", "通道", "仓位", "电梯"]),
        ("效率/等待", ["效率", "等待", "人等车", "车等人", "准点", "超时", "满载"]),
        ("下拉/字典/列表", ["下拉", "字典", "列表", "类型", "获取"]),
    ]
    # prefer name matches first
    for cat, kws in rules:
        if any(k in name_l for k in kws):
            return cat
    text_l = (content or "")[:150].lower()
    for cat, kws in rules:
        if any(k in text_l for k in kws):
            return cat
    return "其他"


lines = []
A = lines.append

A("# DataView SQL / 数据源 ID — 前端调用手册")
A("")
A("> 来源：`DataView_DataMeta_Server_TAS接口服务等_7_20260929093032.dv.json`  ")
A("> 用途：前端布局 / 脚本通过 **数据源 ID（sourceId）** 调用服务端查询，**不要直连数据库**。  ")
A("> 字段说明：`入参`/`出参` 取自管理端 inputParams / outputParams；SQL 全文见管理端「数据源配置」。")
A("")
A("---")
A("")

A("## 1. 前端如何调用")
A("")
A("### 1.1 布局 JSON 中作为数据源")
A("")
A("```json")
A("{")
A('  "id": "<实例id>",')
A('  "source": "SQL1818567",')
A('  "interval": "${constant.RefreshHzForAmr}",')
A('  "params": { "text": false, "data": null },')
A('  "resultFormat": "map",')
A('  "preHandler": "/* 可选：收集筛选项，return 查询参数对象 */",')
A('  "handler": "/* 可选：回调名 */",')
A('  "binds": [{ "refName": "#cardX", "template": "/* 绑定渲染 */" }]')
A("}")
A("```")
A("")
A("### 1.2 脚本内主动查询")
A("")
A("```js")
A("// this.doQueryData(sourceId, paramsJsonString, resultType)")
A("let res = await this.doQueryData('SQL19040310', '{}', 'list')")
A("let rows = res.data.data")
A("")
A("// 带参数示例")
A("let res2 = await this.doQueryData(")
A("  'SQL09091542',")
A("  JSON.stringify({ mapcodes: 'MAP01', robotcodes: 'AMR001' }),")
A("  'list'")
A(")")
A("```")
A("")
A("### 1.3 参数与返回约定")
A("")
A("| 约定 | 说明 |")
A("|------|------|")
A("| `${paramName}` | SQL 占位符，由 preHandler / params 注入 |")
A("| `[col in (${param})]` | **可选条件**：参数为空时整段丢弃 |")
A("| `resultFormat: 'map'` | 布局绑定常用 |")
A("| `doQueryData(..., 'list')` | 脚本取行数组常用 |")
A("| 返回结构 | `res.data.data` 为结果；行字段见各数据源「出参」 |")
A("")
A("### 1.4 状态码约定（设备类查询通用）")
A("")
A("| status2 | 含义 |")
A("|---------|------|")
A("| 0 | 离线 |")
A("| 1 | 运行 |")
A("| 2 | 充电 |")
A("| 3 | 空闲 |")
A("| 4 | 异常 |")
A("")
A("---")
A("")

A("## 2. 服务连接一览")
A("")
A("| 服务名 | serverId | 类型 | 主机:端口 | 库/前缀 | 账号 | 数据源数 |")
A("|--------|----------|------|-----------|---------|------|----------|")
for s in data:
    A(
        f"| **{s.get('serverName')}** | `{s.get('serverId')}` | {s.get('serverType')}/{s.get('subServerType')} "
        f"| `{s.get('host')}:{s.get('port')}` | {s.get('endpoint') or '—'} | {s.get('username') or '—'} "
        f"| {len(s.get('sources') or [])} |"
    )
A("")
A("> JDBC 均为 PostgreSQL，主机相同，密码不在导出中（只存服务端）。")
A("")
A("---")
A("")

A("## 3. 数据源目录（按服务）")
A("")

sec = 0
for s in data:
    sec += 1
    sname = s.get("serverName")
    A(f"### 3.{sec} {sname}")
    A("")
    A(f"- **serverId**: `{s.get('serverId')}`")
    A(f"- **连接**: `{s.get('host')}:{s.get('port')}` · endpoint=`{s.get('endpoint') or ''}` · {s.get('serverType')}/{s.get('subServerType')}")
    A("")
    srcs = s.get("sources") or []
    groups = defaultdict(list)
    for src in srcs:
        groups[category_of(src.get("sourceName") or "", src.get("content") or "")].append(src)

    A("| sourceId | 名称 | 分类 | 入参 | 出参 |")
    A("|----------|------|------|------|------|")
    order = [
        "设备状态/开动率",
        "任务统计",
        "告警/故障",
        "充电/电量",
        "地图/站点/热力",
        "班次/时间范围",
        "效率/等待",
        "下拉/字典/列表",
        "其他",
    ]
    for cat in order:
        for src in groups.get(cat, []):
            sid = src.get("sourceId") or ""
            name = (src.get("sourceName") or "").replace("|", "\\|")
            ins = parse_params(src.get("inputParams"))
            outs = parse_params(src.get("outputParams"))
            if not ins:
                cps = content_params(src.get("content") or "")
                in_s = ", ".join(f"`{c}`" for c in cps) if cps else "—"
            else:
                in_s = fmt_params(ins)
            out_s = fmt_params(outs, with_text=True) if outs else "见 SQL / 接口返回"
            # escape pipes inside
            in_s = in_s.replace("|", "\\|")
            out_s = out_s.replace("|", "\\|")
            A(f"| `{sid}` | {name} | {cat} | {in_s} | {out_s} |")
    A("")

    A("<details><summary>SQL / 接口内容摘要</summary>")
    A("")
    A("| sourceId | 名称 | content |")
    A("|----------|------|---------|")
    for cat in order:
        for src in groups.get(cat, []):
            sid = src.get("sourceId") or ""
            name = (src.get("sourceName") or "").replace("|", "\\|")
            brief = brief_sql(src.get("content") or "").replace("|", "\\|").replace("`", "'")
            A(f"| `{sid}` | {name} | `{brief}` |")
    A("")
    A("</details>")
    A("")

A("---")
A("")

A("## 4. 前端常用速查")
A("")
A("### 4.1 当前统计看板已在用")
A("")
A("| sourceId | 名称 | 所属服务 | 入参 | 出参 | 典型用途 |")
A("|----------|------|----------|------|------|----------|")
A("| `SQL1818567` | 当日-设备运行情况 | DATAMETA_DB | `mapcodes`,`robotcodes` | 设备总数/运行/充电/空闲/异常/离线 | card7 五态柱状 |")
A("| `SQL1819468` | 当日-设备分布情况 | DATAMETA_DB | `mapcodes`,`robotcodes` | map_code, count, baterry | card6 设备分布 |")
A("| `SQL19040310` | TAS地图列表 | CMS_DB | — | map_code, map_name | 脚本 mapMap |")
A("| `SQL10265761` | 班次下拉SQL | DATABUS-DB | `id` | id,name,range… | 班次筛选 |")
A("| `SQL21280647` | 看板-获取时间查询范围 | DATAMETA_DB | `type` 等 | 时间范围 | 班次时间窗 |")
A("| `SQL15202628` | 看板-任务平均数据 | DATAMETA_DB | 时间/地图等 | avg_task_time… | 任务平均 |")
A("| `SQL16154531` | 看板-充电数据 | DATAMETA_DB | `mapcodes` 等 | amr_code,map,battery,success | 充电列表 |")
A("")
A("### 4.2 与「逐车状态」最相关（改造 `SQL_AMR_STATUS_ROWS` 可参考）")
A("")
A("| sourceId | 名称 | 入参 | 出参 | 说明 |")
A("|----------|------|------|------|------|")
A("| `SQL09091542` | 设备-实时状态 | `mapcodes`,`robotcodes` | `robot_code`,`status`,`map_code`,`baterry`,`timestamp`… | **最接近** `{amr_code,status}` |")
A("| `SQL21343641` | EMQ-AMR状态(设备&地图) | `mapcodes` | `mapcode`,`robotcode`,`status2` | 按车出状态码 |")
A("| `SQL09371021` | AMR_STATUS_DPS | 地图/时间 | 明细字段 | 状态明细流 |")
A("| `SQL10255922` | AMR_STATUS_COUNT | `mapcodes` | `status2`,`count` | 仅汇总 |")
A("")
A("**建议**：在 DATAMETA_DB 基于 `SQL09091542` 裁剪为 `amr_code, status`（status 映射中文或保留 status2），")
A("管理端保存后把生成的 sourceId 填进布局 `source`（替换 `SQL_AMR_STATUS_ROWS`）。")
A("")
A("### 4.3 状态类查询参数传法示例")
A("")
A("```js")
A("// 筛选：#select0 地图（ALL→null），#select1 日期")
A("let mapCls = this.$component('#select0')")
A("let mapcodes = mapCls && mapCls.tmpValue && mapCls.tmpValue !== 'ALL' && mapCls.tmpValue !== 'all'")
A("  ? mapCls.tmpValue : null")
A("this.$model('mapcodes', mapcodes)")
A("return { mapcodes }  // 作为 doQueryData / source 请求参数")
A("```")
A("")
A("---")
A("")

A("## 5. 通用入参名对照")
A("")
A("| 参数名 | 含义 | 常见取值 |")
A("|--------|------|----------|")
A("| `mapcodes` / `mapCode` / `mapcode` | 地图筛选 | `ALL`/`all`→null；多值逗号分隔 |")
A("| `robotcodes` / `robotcode` | 设备筛选 | 车号，多值逗号分隔 |")
A("| `startTime` / `endTime` | 时间范围 | `yyyy-mm-dd hh24:mi:ss` |")
A("| `date` / `begin_date` | 日期 | 与 `#select1` 绑定 |")
A("| `type` | 时间粒度 | day 等 |")
A("| `taskChainType` / `taskType` | 任务类型 | 下拉选中值 |")
A("| `range` / `workRange` | 班次/时段 | 班次 id |")
A("")
A("---")
A("")

A("## 6. 注意事项")
A("")
A("1. **只通过 sourceId 调用**，前端不写连接串、不直连 PostgreSQL。")
A("2. sourceId 大小写敏感，与管理端「数据源配置」一致。")
A("3. SQL 里 `[...]` 为可选条件；参数不传则该条件不生效。")
A("4. 导出不含密码；连接凭证只在服务端「服务配置」。")
A("5. 本清单以导出时间点为准；变更后以管理端列表为准。")
A("6. 出参字段名是前端读结果的依据（如 `res.data.data[0].robot_code`）。")
A("")

open(out, "w", encoding="utf-8").write("\n".join(lines))
print("wrote", out)
print("lines", len(lines))
