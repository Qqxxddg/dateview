# 实施任务

## 实施路径

全部前端改动收敛在单文件 `DataView_布局文件[0-统计看板].dv.json`。服务端按契约提供「设备号 + 告警类型编码」行查询（占位 `SQL_CARD9_DEVICE_REASON`，或改造 `SQL14252827` 的 GROUP BY）；**服务端 SQL 开发不在本任务列表**。前端复用 `#card7` 已验证的「页面级 source + `applyXxxRows` + row-click」模式，原因名复用已有 `$model('alarmTypeMap')`（`SQL0935187` / 备选 `SQL15234529`）。

排序原则：先文案与组件骨架（locales → `#card9` 元素），再数据链路（source 绑定 + `applyCard9Rows`），再交互（`onCard9RowClick`），最后清理退役项与整体验收。新链路用 `defaultValue` 样例可独立于服务端验证。

**既有事实（来自现版布局与 `DataView_SQL_ID_前端调用手册.md` / DataMeta 导出）**：

- `#card9` 现为 `dv-chart`，layout `{x:500,y:780,w:461,h:279,z:20}`，页面级 source `id=20230625143018702` / `SQL14252827`，`preHandler: beforeSourceQuery_6`，`resultFormat: map`，binds 写 `field1=source_code`、`field2=count`，且误写 `#card7.setData`。
- `SQL14252827` 入参：`mapcodes, pmCase, time_start, time_end, rangeCase, range_start, range_end`；出参：`count, source_code`（按设备聚合）。契约要求改为行级 `source_code + alarm_sub_type`。
- 运行时生效 sources 为 `pages[0].sources`（`amr-status-scroll-list` 任务 1 结论）；`content.option.sources` 为历史镜像，**两处同改**。
- `alarmTypeMap` 由 `beforeSourceQuery_7` 用 `SQL0935187` 构建；`applyCard7Rows` / `onCard7RowClick` 为直接模板。
- 标题模板 `#item20230612130623400` 内容为 `${this.$text('$topDevices')}`，locales 键 `topDevices` 现值「TOP20告警设备」。

## 任务规则

- 每个勾选项是一个可独立验证的实施成果；本项目单文件改造，Files 指向布局文件，按 JSON 分区（locales / 元素 / source / 脚本）拆分。
- 机器标记 `_Requirements:` / `_Leverage:` / `_Depends on:` 保持英文键名；依赖无环。
- 改动行为的任务自带验证步骤；任务 7 为清理核对，任务 8 为联调验收。

## 任务列表

- [x] 1. 更新 locales 文案（标题与列头）
  - Files: `DataView_布局文件[0-统计看板].dv.json`（`content.locales` / `pages[0]` 若含 locales 副本则同改）
  - 修改键 `topDevices`：zh-CN「设备告警原因」、en-US「Device Alarm Reasons」。新增键 `t4_device`（设备号/Device）、`t4_reason`（告警原因/Reason），格式对齐现有 `{"key","zh-CN","en-US"}` 条目。不改动其它键（含仍被使用的 `times`）。
  - 验证：JSON 可解析；`topDevices` 新值生效；新键不与既有 key 重复。
  - _Leverage: 现有 locales 条目（如 `t3_carno`、`topTypes`）_
  - _Requirements: 1.6_
  - _Depends on: none_

- [x] 2. `#card9` 元素骨架改造为 `dv-scrolltable`
  - Files: `DataView_布局文件[0-统计看板].dv.json`（`pages[0].elements` 中 `refName='#card9'`，id=`item20230627135942297`）
  - `elName` 由 `dv-chart` 改为 `dv-scrolltable`；`refName`、`layout`（x=500,y=780,w=461,h=279,z=20）保持不变。替换 props（对齐 `#card7`）：`columns` 两列 `{label:'$t4_device', field:'source_code'}`、`{label:'$t4_reason', field:'reason_name'}`；`scroll:true`、`scrollType:'scroll'`、`speed:2`、`showPageIndex:false`、`pageSize:10`、`pageInterval:5`、`rowHeight:36`（若 5 行不够可调 32）、`thHeight:40`、`fontSize:12`、`border:false`、`stripe:true`、`theme:'green'`、`innerPadding:0`、`showStyle:'0'`、`colors:[]`。option 改为滚动表结构（`dynamic:false`、`dataMaps:[]`、`filterRule:{sort:[],style:[]}`、`sources:[]`、`sourceEvent` 空）。events 改为 `row-click` → `onCard9RowClick`（结构同 `#card7`）。写入 `defaultValue` 样例 8～10 行，形状 `{source_code, reason_name}`，覆盖：同设备多原因、未知原因、占位行 `{source_code:'-', reason_name:'暂无数据'}`。
  - 验证：JSON 可解析；整页不再把 `#card9` 当 chart 使用；layout 与改造前一致；样例可驱动表格显示。
  - _Leverage: `#card7` 的 props/option/events；`#chargedata` 的 row-click 事件结构_
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 2.5, 7.1, 7.2, 7.3, 7.4_
  - _Depends on: 1_

- [x] 3. 页面级 source 绑定改造 + `applyCard9Rows` 行加工
  - Files: `DataView_布局文件[0-统计看板].dv.json`（`pages[0].sources` 与 `content.option.sources` 中 id=`20230625143018702`；`pages[0].script`）
  - **source 位点**（双列表同改）：`interval` 保持 `${constant.RefreshHz}`；`preHandler` 保持 `beforeSourceQuery_6`；`resultFormat` 改为 `list`；`source` 字段在服务端就绪前可暂留 `SQL14252827` 并在任务记录标注待替换为 `SQL_CARD9_DEVICE_REASON`（或服务端改造后的实际 ID），**不得**在前端伪造 SQL。`binds[0].template` 改为 `return this.applyCard9Rows(data)`，删除 `field1/field2` 映射与 `#card7.setData`。
  - **新增 `this.applyCard7Rows` 同构的 `applyCard9Rows(data)`**：
    1. 取 `#card9`，无则 warn 返回 null；
    2. 归一入参（数组 / `data.data` / `data.list`）；
    3. 空则占位行 `[{source_code:'-', reason_name:'暂无数据'}]` 并 `setData`；
    4. 字段：`source_code`（兼容 `robot_code`/`amr_code`，缺失 `'-'`）；`reason_name` 优先，否则 `alarm_sub_type` 查 `this.$model('alarmTypeMap')`，未命中显示编码，全空显示「未知原因」；保留原始 `alarm_sub_type` 于行上供点击用；
    5. 排序：`source_code` 升序，同设备内 `reason_name` 升序；
    6. `card.setData(rows)` 返回 rows。
  - 若 `alarmTypeMap` 为空：`applyCard9Rows` 内补拉 `SQL0935187`（失败再试 `SQL15234529`），仍失败则降级原样编码。
  - 验证：用 defaultValue 与模拟 `list` 响应跑 `applyCard9Rows`（映射/排序/空态/字典未命中）；binds 模板不再引用 `#card7`；双列表 source 配置一致。
  - _Leverage: `applyCard7Rows`；`SQL09091542`→`#card7` 的 binds 形态；`beforeSourceQuery_7` 的 `alarmTypeMap` 构建_
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 4.1, 4.2, 4.3, 5.1, 5.2, 5.3, 8.1_
  - _Depends on: 2_

- [ ] 4. 筛选参数与 `beforeSourceQuery_6` 兼容确认
  - Files: `DataView_布局文件[0-统计看板].dv.json`（`pages[0].script` 的 `beforeSourceQuery_6`，只读确认；若入参名与新 SQL 契约不一致则最小改动）
  - 确认返回参数覆盖契约入参 `mapcodes, pmCase, time_start, time_end, rangeCase, range_start, range_end`。服务端若沿用 `SQL14252827` 入参则**零改动**；若新 SQL 增删入参，仅同步 `beforeSourceQuery_6` 的 return 字段，不改筛选 UI。
  - 验证：切换 `#select0`/`#select1`/班次后，source 请求参数字段齐全；不回归其它使用 `beforeSourceQuery_6` 的逻辑（仅 card9 使用则更简单）。
  - _Leverage: 现有 `beforeSourceQuery_6` 全文_
  - _Requirements: 4.1, 4.2_
  - _Depends on: 3_

- [ ] 5. 行点击 `onCard9RowClick` 并替换柱状点击
  - Files: `DataView_布局文件[0-统计看板].dv.json`（`pages[0].script`）
  - 新增 `onCard9RowClick = (e) => {...}`：`e` 为行对象；守卫空行或 `reason_name === '暂无数据'` 不跳转。`pm = {date, ranges, starttime, endtime, mapcodes, source_code: e.source_code, reason_name: e.reason_name, alarm_sub_type: e.alarm_sub_type}` 写入 `sessionStorage['alarm-device-param']`。CMS 跳转分支**原样保留**原 `onCard9Click`（`CmsVersion` 3→`cms_506010`；4→`20230707084105967`；4.1→同页 https/iframe）。删除 `onCard9Click`（柱状 `e.event.name` 语义不存在）。
  - 验证：脚本 `onCard9Click` 零引用；元素 events 指向 `onCard9RowClick`；点击参数含设备号与原因（不再把设备号写入 `pm.status`）。
  - _Leverage: `onCard7RowClick` 结构；原 `onCard9Click` 跳转 URL_
  - _Requirements: 6.1, 6.2, 6.3, 1.6_
  - _Depends on: 2_

- [ ] 6. 标题与列头联调（视觉）
  - Files: `DataView_布局文件[0-统计看板].dv.json`（locales 已在任务 1；必要时微调 `#item20230612130623400`）
  - 预览标题显示「设备告警原因」；表格列头显示「设备号 / 告警原因」。若 locales 已生效则本任务仅目视确认；若标题模板未引用 `$topDevices` 再改模板。
  - 验证：大屏预览标题与列头正确；无「TOP20告警设备 / 次数 / 次」露出（`times` 键仅在仍使用的他处出现）。
  - _Leverage: 任务 1 的 locales_
  - _Requirements: 1.6, 7.2_
  - _Depends on: 1, 2_

- [ ] 7. 退役项清理与双列表一致性
  - Files: `DataView_布局文件[0-统计看板].dv.json`（元素 props、source binds、`pages[0].script`）
  - 核对删除：① `#card9` 的 chart `props.options`（bar/ECharts 全量）已不存在；② binds 中 `field1/field2` 与 `#card7.setData` 已不存在；③ `onCard9Click` 已不存在；④ Y 轴 `$times` 对 card9 的引用已不存在。`content.option.sources` 与 `pages[0].sources` 中 card9 源配置一致。`handleDownloadCsv` 列表不含 `#card9` 则保持不动。
  - 验证：全文件搜索 `onCard9Click`、`field2`（card9 绑定内）、`#card7').setData`（card9 路径）零残留；页面 JSON 可解析。
  - _Leverage: 任务 3、5 的改动结果_
  - _Requirements: 1.6, 1.7, 8.1, 8.2_
  - _Depends on: 3, 5_

- [ ] 8. 整体验收（样例 + 联调清单）
  - Files: 无新改动（验证任务）；记录写入任务备注
  - **样例模式**（服务端未就绪）：用 `defaultValue` 验证 ≥5 行可读、超行滚动循环、同设备多原因相邻、未知原因兜底、空态「暂无数据」且点击不跳转。
  - **联调模式**（服务端 SQL 就绪）：替换实际 sourceId 后验证筛选联动、`RefreshHz` 刷新、原因名与 `#alarmTypeTopCard` 一致、点击进 CMS（3/4/4.1）。
  - 验证：对照需求 1–8 验收标准逐条勾选；失败项回对应任务修复，不得跳过。
  - _Leverage: 需求文档验收标准；设计文档「测试策略」_
  - _Requirements: 1.1–1.7, 2.1–2.5, 3.1–3.4, 4.1–4.3, 5.1–5.3, 6.1–6.3, 7.1–7.4, 8.1–8.2_
  - _Depends on: 4, 6, 7_
