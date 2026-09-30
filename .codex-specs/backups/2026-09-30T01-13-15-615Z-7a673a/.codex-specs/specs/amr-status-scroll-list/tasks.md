# 实施任务

## 实施路径

全部改动收敛在单文件 `DataView_布局文件[0-统计看板].dv.json`。数据源直接复用服务端已有查询 **`SQL09091542`（设备-实时状态，DATAMETA_DB）**，无需服务端新开发；前端在 `postHandler` 完成 `status2` 代码→中文的归一化，下游组件按设计文档的数据契约 `{amr_code, status(中文)}` 消费。排序原则：先消不确定性（sources 双列表、着色机制），再增量搭建（locales → 元素骨架 → 数据源/脚本），新链路验证通过后拆旧链路，最后样例验证与联调。实现严格复用设计文档指定的既有模式（`#chargedata` 滚动表骨架、`onChargeRowClick` 跳转结构）。

**数据源事实（来自 `DataView_SQL_ID_前端调用手册.md` 与参考导出）**：

- `SQL09091542` 入参 `mapcodes`、`robotcodes`（`[...]` 可选条件，不传则丢弃）；出参 `robot_code`(车号)、`status`(**status2 代码**)、`map_code`、`baterry`、`timestamp` 等；SQL 已按 `partition BY map_code,amr_code ORDER BY timestamp desc` 取每车最新状态，`ORDER BY robot_code`。
- 状态码约定（手册 §1.4）：`0`=离线、`1`=运行、`2`=充电、`3`=空闲、`4`=异常。
- 调用只经数据源 ID，禁止直连数据库（与需求 2.1 一致）。

## 任务规则

- 每个勾选项是一个可独立验证的实施成果；本项目单文件改造，故 Files 均指向布局文件，但按 JSON 结构分区（元素/数据源/脚本/文案）拆分粒度。
- 机器标记 `_Requirements:` / `_Leverage:` / `_Depends on:` 保持英文键名（校验器解析用）；依赖无环。
- 改动行为的任务自带验证步骤；任务 8、9 为纯验证任务。

## 任务列表

- [x] 1. 确认运行时生效的页面级 sources 列表（消解 U1 歧义）
  - Files: `DataView_布局文件[0-统计看板].dv.json`（只读比对，不改交付配置）
  - 布局文件存在 `content.option.sources` 与 `pages[0].sources` 两份列表且 binds 已分歧。判定哪一份生效并把结论（生效列表路径 + 证据）写入任务记录，供任务 7 执行删除时遵循。
  - **结论（已生效）**：`pages[0].sources` 为运行时生效列表；`content.option.sources` 为历史遗留镜像。证据（2026-09-29 复跑 `_probe_task1.py` 确认布局文件未变）：①结构归属——`content.script` 为空（0），83k 脚本与 50 个元素仅在 `pages[0]`（`version 2.0` 以 page 对象承载），`content.option` 仅剩 background/scale/sources/buttonColor 遗留壳；②惯用法演进——5 处 binds 分歧中 `pages[0]` 侧为新写法（`$param()`、`return data`），`content.option` 侧为旧写法（直接 `setData`、`options.content=`），且 `pages[0]` 版含后续增量配置；③两列表 source id 与顺序完全一致（同源拷贝后单侧演进）。运行时复核项在任务 9 清单第⑨项；若实测相反，任务 7 双列表都删的处置不变，仅需更正本标注。
  - _Leverage: `_probe_task1.py` 取证输出；设计文档「错误处理 U1」；`DataView_SQL_ID_前端调用手册.md` §4.3_
  - _Requirements: 1.6_
  - _Depends on: none_

- [x] 2. 新增 locales 文案键
  - Files: `DataView_布局文件[0-统计看板].dv.json`（`content.locales`）
  - 新增 3 个键：`t3_carno`（车号/Vehicle）、`t3_status`（状态/Status）、`noData`（暂无数据/No data），格式对齐现有 `{"key","zh-CN","en-US"}` 条目；不改动既有键。
  - 验证：导出 JSON 后 `locales` 数组可被 `json.loads` 解析且键不重复。
  - _Leverage: 现有 locales 条目格式（如 `t1_ amr_code`）_
  - _Requirements: 1.2, 2.4_
  - _Depends on: none_

- [x] 3. `#card7` 元素骨架改造为 `dv-scrolltable`
  - Files: `DataView_布局文件[0-统计看板].dv.json`（`pages[0].elements` 中 `refName='#card7'`）
  - `elName` 由 `dv-chart` 改为 `dv-scrolltable`；`refName`、`layout`（x=26,y=456,w=435,h=310,z=37）保持原值。替换 props：`columns` 两列（`{label:'$t3_carno', field:'amr_code'}`、`{label:'$t3_status', field:'status'}`）、`scroll:true`、`scrollType:'scroll'`、`speed:2`、`showPageIndex:false`、`pageSize:10`、`pageInterval:5`、`rowHeight:36`、`thHeight:40`、`fontSize:12`、`border:false`、`stripe:true`、`theme:'green'`；option 改为滚动表结构（`dynamic:false`、`dataMaps:[]`、`filterRule:{sort:[],style:[]}`、`colors:[]`、`sourceEvent` 空）。events 改为 `row-click` → `onCard7RowClick`。写入 `defaultValue` 样例 8～10 行，**按前端契约形状** `{amr_code, status}`，status 为中文（五状态 + 未知状态 `维修中` + 占位 `暂无数据` 行形态各覆盖）。
  - 验证：JSON 可解析；元素除 `elName/props/option/events` 外字段与改造前一致。
  - _Leverage: `#chargedata` 元素的 props/option/events 结构_
  - _Requirements: 1.1, 1.2, 2.5, 6.1, 6.2_
  - _Depends on: 2_

- [x] 4. 状态着色机制验证与落地
  - Files: `DataView_布局文件[0-统计看板].dv.json`（`#card7` 的 `filterRule.style` / `colors` / `enhance`）
  - 用任务 3 的 `defaultValue` 样例在平台预览，按降级链择优并只保留一种实现：① `filterRule.style` 按 `status` 条件设色 ② `colors` 映射 ③ `enhance` 钩子。色值沿用原柱状图语义（运行=蓝绿、异常=橙红、离线=灰、空闲/充电=主色蓝、未知=默认）。三者均不可用时启用兜底方案（状态文字前缀 `●` + 默认色），并在任务记录中注明。
  - **结论（已落地）**：样式1/2/3 仅为 `showStyle` 皮肤预设，不按状态变色（用户实测）；生效机制为 **`props.colors` 字段渲染规则**（手册 4.2.2「目标字段/规则/字体颜色」），schema 实测自用户导出文件 `DataView_布局文件[0-统计看板].dv1.json`：`{type: 'row'|'cell', field, name, operator, value, color, backgroundColor}`。已归一化合并进交付文件 5 条规则（`type:'cell'`、目标字段 `field:'status'`、条件 `name:'status' operator:'=' value:<状态>`），色值：异常 `#F86508`、运行 `#09C184`、离线 `#8A8A8A`、空闲 `#0086FF`、充电 `#35B8FF`；未配置状态（维修中/暂无数据）走默认色且不丢行。`filterRule` 保持空（未使用）；`enhance` 未使用。
  - 验证：样例中五种状态颜色符合映射；未知状态为默认色且行不丢失。
  - _Leverage: 原 `#card7` dv-chart `itemStyle` 渐变色值_
  - _Requirements: 1.3_
  - _Depends on: 3_

- [x] 5. 组件级数据源与数据加工（`SQL09091542`）
  - Files: `DataView_布局文件[0-统计看板].dv.json`（`#card7.option.sources[0]`）
  - 新增元素级 source：`source: 'SQL09091542'`（现有 DATAMETA_DB 查询，**无需服务端新开发**）、`type:'common'`、`map:false`、`interval:'${constant.RefreshHzForAmr}'`。`preHandler` 内联迁移 `beforeSourceQuery_1` 取参逻辑：读 `#select0` → `mapcodes`（`ALL/all` 归一 null，多值逗号分隔照传）、`#select1` → `date` 写 `$model`（`SQL09091542` 入参仅 `mapcodes`/`robotcodes`，`robotcodes` 不传即查全车；`date` 仅入模型供点击参数用）；作用域用 `this.$container.$component`。`postHandler` 实现：
    1. **归一化**：每行映射为前端契约 `{amr_code: row.robot_code, status: 中文}`；`status2` 代码→中文（`0`→离线、`1`→运行、`2`→充电、`3`→空闲、`4`→异常，参考手册 §1.4）。
    2. **排序**：按 `['异常','离线','运行','充电','空闲']` 优先级、同级 `amr_code` 升序（`SQL09091542` 自带 `ORDER BY robot_code`，排序在归一化后重算以符合需求 4）。
    3. **未知状态**：代码外的 `status` 原样保留、排在队尾、着色走默认。
    4. **空/错降级**：返回空数组或异常时返回占位行 `{amr_code: '-', status: '暂无数据'}`（若任务 8 验证组件内置空态合格则省略占位行）。
    5. **防抖动**：比较新旧行序列，内容一致时返回上一次同一数组引用（防刷新跳顶）。
  - 验证：控制台以 `doQueryData('SQL09091542', JSON.stringify({mapcodes:null, robotcodes:null}), 'list')` 验证入参/出参与映射纯函数（输入含 `status:'1'` 等代码 → 输出中文）；排序函数输入乱序样例 → 输出符合优先级。
  - **实施记录（路线 B，组件级 source 已弃用）**：组件级 `option.sources` 实测可请求但结果不挂载（组件提示「图表关联数据为空」，`postHandler` 不执行），已改为**页面级 source + binds setData**（与改造前 `SQL1818567→#card7` 同构，双列表挂载、`preHandler: beforeSourceQuery_1`、`resultFormat: list`）。加工逻辑抽取为页面脚本 `this.applyCard7Rows(data)`（兼容 `{code,data:[…]}`/数组/list 形态，状态码→中文、`robot_code`→`amr_code`、排序、未知排尾、空错占位行、`card.setData(rows)`），binds 模板改为调用该函数；`onLoaded` 追加 `this.initCard7Now()` 立即首拉（`doQueryData('SQL09091542',…)`），消除首屏等待一个轮询周期的延迟。已用真实响应形态验证（`_task5_routeB_test.js`、`_task5_latency_test.js` 全过）；平台实测：Console `card7 rows bind` 打出 Array(9) 状态映射正确，表格可显示。
  - _Leverage: `#chargedata.option.sources` 骨架；`beforeSourceQuery_1` 取参逻辑；手册 §4.3 参数传法示例_
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 4.1, 4.2_
  - _Depends on: 3_

- [x] 6. 页面脚本：新增行点击处理并清理柱状遗留函数
  - Files: `DataView_布局文件[0-统计看板].dv.json`（`pages[0].script`）
  - 新增 `onCard7RowClick = (e) => {...}`：构造 `{date, ranges, starttime, endtime, mapcodes, statusName: e.status, amr_code: e.amr_code}` 写入 `sessionStorage['device-status-param']`，复用原 `onCard7Click` 的 `CmsVersion` 3/4/4.1 跳转分支；守卫 `e.status === '暂无数据'` 或行为空时不跳转。删除 `onCard7Click` 与 `beforeSourceQuery_1`（仅被退役源引用，函数删除以本任务为准）。
  - 验证：脚本中 `onCard7Click`/`beforeSourceQuery_1` 零引用；`onCard7RowClick` 出现且被元素 events 引用。
  - **实施记录**：`onCard7RowClick` 已落盘（行数据直传 `e`；守卫 `!row || !row.status || row.status === '暂无数据'` 不跳转；`pm` 含 `date/ranges/starttime/endtime/mapcodes/statusName/amr_code` 写入 `sessionStorage['device-status-param']`；CmsVersion 3/4/4.1 跳转分支自 `onCard7Click` 原样迁移）。`onCard7Click` 已删除（全文件零引用）。**计划修正**：`beforeSourceQuery_1` **保留**（路线 B 的 `SQL09091542` source `preHandler` 依赖它，非柱状遗留）。行为测试 `_task6_test.js` 全过（正常点击/占位守卫/空行守卫/v3/v4/v4.1 分支）。
  - _Leverage: `onCard7Click` 参数结构与跳转分支；`onChargeRowClick` 的 `(e)=>{...}` 行数据入参形态_
  - _Requirements: 1.6, 5.1, 5.2_
  - _Depends on: 3_

- [ ] 7. 退役柱状数据源并核对导出链路
  - Files: `DataView_布局文件[0-统计看板].dv.json`（`content.option.sources` / `pages[0].sources`、`pages[0].script` 的 `downloadCsv`）
  - 按任务 1 结论在**两份列表**中删除 `SQL1818567` 页面级 source（含 binds 柱状模板）；若任务 1 判定其中一份根本不参与运行时，两份仍都删，但任务记录注明生效列表。核对 `downloadCsv` 中 `$exportComponentData([... '#card7' ...])`：`dv-scrolltable` 支持导出则保留，否则移除 `'#card7'`。
  - 验证：`SQL1818567` 在文件中零引用；页面 JSON 可解析；`downloadCsv` 数组元素均为现存 refName。
  - **实施记录**：`SQL1818567` 已从 `content.option.sources` 与 `pages[0].sources` 各删 1 条（生效列表为 `pages[0].sources`，见任务 1 结论），全文件 `SQL1818567` 引用数 0；两列表现各 9 条（8 旧 + 1 新 `SQL09091542`）。`downloadCsv` 的 `$exportComponentData` 五个 refName（`#effectTrend/#card6/#card7/#taskcounttrend/#taskstatus`）均对应现存元素，`#card7` 保留（dv-scrolltable 有行数据与 setData）；实际导出能力并入任务 8 清单验证。
  - _Requirements: 1.6_
  - _Depends on: 1, 5, 6_

- [ ] 8. 样例数据集成验证（DataView 平台预览）
  - Files: `DataView_布局文件[0-统计看板].dv.json`（验证性，如发现问题以最小改动修复）
  - 清单：①列表渲染为「车号|状态」两列文字行 ②行数超过可视区（约 7 行）自动向上滚动并循环 ③行数未超可视区静止 ④状态着色符合映射 ⑤未知状态原样显示 ⑥空数据显示「暂无数据」 ⑦占位行点击不跳转 ⑧样例行点击写入 `device-status-param`（含 `amr_code`）并打开 CMS ⑨连续刷新 5 分钟无闪烁、滚动不跳顶 ⑩与改造前同区域截图对比布局无错位 ⑪`downloadCsv` 导出不报错（`#card7` 在 `$exportComponentData` 中，若 scrolltable 不支持导出则从数组移除该项）。
  - _Requirements: 1.2, 1.4, 1.5, 2.3, 2.4, 2.5, 3.3, 5.2, 6.3_
  - _Depends on: 4, 5, 6_

- [ ] 9. `SQL09091542` 真实数据联调验证
  - Files: `DataView_布局文件[0-统计看板].dv.json`（验证性，如发现问题以最小改动修复）
  - 无新增服务端开发依赖（`SQL09091542` 已存在）；服务端仅需保证该数据源权限可用。清单：①真实车辆行加载与滚动（车号来自 `robot_code`）②`status2` 代码→中文映射正确（抽样比对管理端查询结果与列表文字）③`#select0` 地图筛选生效（`mapcodes` 传参；`ALL` 时不筛）④`robotcodes` 不传时返回全车 ⑤刷新间隔符合 `${constant.RefreshHzForAmr}`、无闪烁跳顶 ⑥断开服务端请求显示「暂无数据」且其它模块轮询不受影响 ⑦整屏 `scale:true` 缩放下布局正确 ⑧点击行按 `CmsVersion` 正确打开 CMS ⑨运行时复核任务 1 结论（`pages[0].sources` 生效）。
  - _Requirements: 2.1, 2.2, 3.1, 3.2, 6.3_
  - _Depends on: 5, 7, 8_
