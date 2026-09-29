# 实施任务

## 实施路径

全部改动收敛在单文件 `DataView_布局文件[0-统计看板].dv.json`。排序原则：先消除不确定性（sources 双列表权威性、着色机制），再做增量搭建（locales → 元素骨架 → 数据源/脚本），新链路验证通过后才拆旧链路（`SQL1818567` 等），最后用样例数据离线验证、服务端就绪后联调。实现严格复用设计文档指定的既有模式（`#chargedata` 滚动表骨架、`onChargeRowClick` 跳转结构），不新增平台之外的技术形态。

## 任务规则

- 每个勾选项是一个可独立验证的实施成果；本项目单文件改造，故 Files 均指向布局文件，但按 JSON 结构分区（元素/数据源/脚本/文案）拆分粒度。
- 机器标记 `_Requirements:` / `_Leverage:` / `_Depends on:` 保持英文键名（校验器解析用）；依赖无环。
- 改动行为的任务自带验证步骤；任务 8、9 为纯验证任务。

## 任务列表

- [ ] 1. 确认运行时生效的页面级 sources 列表（消解 U1 歧义）
  - Files: `DataView_布局文件[0-统计看板].dv.json`（只读比对，不改交付配置）
  - 布局文件存在 `content.option.sources` 与 `pages[0].sources` 两份列表且 binds 已分歧。在 DataView 平台运行页面，以差异点为探针（如 `#card6` 绑定模板：`mapName.$param('content',...)` vs `mapName.options.content=...`）判定哪一份生效，把结论（生效列表路径 + 证据）写入任务记录，供任务 7 执行删除时遵循。
  - **结论记录（静态取证，`_probe_task1.py`）**：生效列表为 **`pages[0].sources`**；`content.option.sources` 为历史遗留镜像（同 id 同序，binds 停留旧写法）。证据：①结构归属——`content.script` 为空、83k 脚本与 50 个元素仅在 `pages[0]`（`version 2.0` 以 page 对象为承载容器），`content.option` 仅剩 background/scale/sources/buttonColor 遗留壳；②惯用法演进——5 处 binds 分歧中 `pages[0]` 侧均为新写法（`$param()` API、`return data` 传值管道），`content.option` 侧为旧写法（直接 `setData`、`options.content=`），且 `pages[0]` 版含后续增量配置（如 taskstatus 的 zlevel/center/legend），属活跃编辑面；③两列表 source id 与顺序完全一致，符合「同源拷贝后单侧演进」的分叉特征。说明：平台运行时探针（DataView 在服务端）无法在本机执行，运行时复核已并入任务 9 清单第 7 项；若实测与结论不符，任务 7 的处置（双列表都删）不变，仅需更正本记录标注。
  - _Leverage: `_probe_misc.py`/`_probe_task1.py` 取证输出；设计文档「错误处理 U1」_
  - _Requirements: 1.6_
  - _Depends on: none_

- [ ] 2. 新增 locales 文案键
  - Files: `DataView_布局文件[0-统计看板].dv.json`（`content.locales`）
  - 新增 3 个键：`t3_carno`（车号/Vehicle）、`t3_status`（状态/Status）、`noData`（暂无数据/No data），格式对齐现有 `{"key","zh-CN","en-US"}` 条目；不改动既有键。
  - 验证：导出 JSON 后 `locales` 数组可被 `json.loads` 解析且键不重复。
  - _Leverage: 现有 locales 条目格式（如 `t1_ amr_code`）_
  - _Requirements: 1.2, 2.4_
  - _Depends on: none_

- [ ] 3. `#card7` 元素骨架改造为 `dv-scrolltable`
  - Files: `DataView_布局文件[0-统计看板].dv.json`（`pages[0].elements` 中 `refName='#card7'`）
  - `elName` 由 `dv-chart` 改为 `dv-scrolltable`；`refName`、`layout`（x=26,y=456,w=435,h=310,z=37）保持原值。替换 props：`columns` 两列（`amr_code`/`status`，label 用 `$t3_carno`/`$t3_status`）、`scroll:true`、`scrollType:'scroll'`、`speed:2`、`showPageIndex:false`、`pageSize:10`、`pageInterval:5`、`rowHeight:36`、`thHeight:40`、`fontSize:12`、`border:false`、`stripe:true`、`theme:'green'`；option 改为滚动表结构（`dynamic:false`、`dataMaps:[]`、`filterRule:{sort:[],style:[]}`、`colors:[]`、`sourceEvent` 空）。events 改为 `row-click` → `onCard7RowClick`。写入 `defaultValue` 样例 8～10 行（覆盖五状态 + 未知状态 `维修中` + 占位 `暂无数据` 行形态），字段严格 `{amr_code, status}`。
  - 验证：JSON 可解析；元素除 `elName/props/option/events` 外字段与改造前一致。
  - _Leverage: `#chargedata` 元素的 props/option/events 结构_
  - _Requirements: 1.1, 1.2, 2.5, 6.1, 6.2_
  - _Depends on: 2_

- [ ] 4. 状态着色机制验证与落地
  - Files: `DataView_布局文件[0-统计看板].dv.json`（`#card7` 的 `filterRule.style` / `colors` / `enhance`）
  - 用任务 3 的 `defaultValue` 样例在平台预览，按降级链择优并只保留一种实现：① `filterRule.style` 按 `status` 条件设色 ② `colors` 映射 ③ `enhance` 钩子。色值沿用原柱状图语义（运行=蓝绿、异常=橙红、离线=灰、空闲/充电=主色蓝、未知=默认）。三者均不可用时启用兜底方案（状态文字前缀 `●` + 默认色），并在任务记录中注明。
  - 验证：样例中五种状态颜色符合映射；未知状态为默认色且行不丢失。
  - _Leverage: 原 `#card7` dv-chart `itemStyle` 渐变色值_
  - _Requirements: 1.3_
  - _Depends on: 3_

- [ ] 5. 组件级数据源与数据加工
  - Files: `DataView_布局文件[0-统计看板].dv.json`（`#card7.option.sources[0]`）
  - 新增元素级 source：`source` 暂用占位 `SQL_AMR_STATUS_ROWS`（**实现时替换为服务端实际 SQL ID**）、`type:'common'`、`map:false`、`interval:'${constant.RefreshHzForAmr}'`。`preHandler` 内联迁移 `beforeSourceQuery_1` 取参逻辑（`#select0`→`mapcodes`（ALL/all 归一 null）、`#select1`→`date`，写 `$model` 并返回查询参数；作用域用 `this.$container.$component`）。`postHandler` 实现：①排序（异常→离线→运行→充电→空闲，同级 `amr_code` 升序）②未知状态原样保留排尾 ③空数组/异常返回占位行 `{amr_code:'-', status:'暂无数据'}`（若任务 8 验证组件内置空态合格则省略占位行）④行序列内容未变时返回上一次同一数组引用（防刷新跳顶）。
  - 验证：控制台验证排序纯函数（输入乱序样例 → 输出符合优先级）；`defaultValue` 移除后联调前仍可切回样例数据自测。
  - _Leverage: `#chargedata.option.sources` 的 preHandler/postHandler/defaultValue 骨架；`beforeSourceQuery_1` 取参逻辑_
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 4.1, 4.2_
  - _Depends on: 3_

- [ ] 6. 页面脚本：新增行点击处理并清理柱状遗留函数
  - Files: `DataView_布局文件[0-统计看板].dv.json`（`pages[0].script`）
  - 新增 `onCard7RowClick = (e) => {...}`：构造 `{date, ranges, starttime, endtime, mapcodes, statusName: e.status, amr_code: e.amr_code}` 写入 `sessionStorage['device-status-param']`，复用原 `onCard7Click` 的 `CmsVersion` 3/4/4.1 跳转分支；守卫 `e.status === '暂无数据'` 或行为空时不跳转。删除 `onCard7Click` 与 `beforeSourceQuery_1`（仅被退役源引用，任务 1 后执行删除亦可，但函数删除以本任务为准）。
  - 验证：脚本中 `onCard7Click`/`beforeSourceQuery_1` 零引用；`onCard7RowClick` 出现且被元素 events 引用。
  - _Leverage: `onCard7Click` 参数结构与跳转分支；`onChargeRowClick` 的 `(e)=>{...}` 行数据入参形态_
  - _Requirements: 1.6, 5.1, 5.2_
  - _Depends on: 3_

- [ ] 7. 退役柱状数据源并核对导出链路
  - Files: `DataView_布局文件[0-统计看板].dv.json`（`content.option.sources` / `pages[0].sources`、`pages[0].script` 的 `downloadCsv`）
  - 按任务 1 结论在**两份列表**中删除 `SQL1818567` 页面级 source（含 binds 柱状模板）；若任务 1 判定其中一份根本不参与运行时，两份仍都删，但任务记录注明生效列表。核对 `downloadCsv` 中 `$exportComponentData([... '#card7' ...])`：`dv-scrolltable` 支持导出则保留，否则移除 `'#card7'`。
  - 验证：`SQL1818567` 在文件中零引用；页面 JSON 可解析；`downloadCsv` 数组元素均为现存 refName。
  - _Requirements: 1.6_
  - _Depends on: 1, 5, 6_

- [ ] 8. 样例数据集成验证（DataView 平台预览）
  - Files: `DataView_布局文件[0-统计看板].dv.json`（验证性，如发现问题以最小改动修复）
  - 清单：①列表渲染为「车号|状态」两列文字行 ②行数超过可视区（约 7 行）自动向上滚动并循环 ③行数未超可视区静止 ④状态着色符合映射 ⑤未知状态原样显示 ⑥空数据显示「暂无数据」 ⑦占位行点击不跳转 ⑧样例行点击写入 `device-status-param`（含 `amr_code`）并打开 CMS ⑨连续刷新 5 分钟无闪烁、滚动不跳顶 ⑩与改造前同区域截图对比布局无错位。
  - _Requirements: 1.2, 1.4, 1.5, 2.3, 2.4, 2.5, 3.3, 5.2, 6.3_
  - _Depends on: 4, 5, 6_

- [ ] 9. 服务端就绪后联调验证
  - Files: `DataView_布局文件[0-统计看板].dv.json`（将 `SQL_AMR_STATUS_ROWS` 占位替换为实际 SQL ID；验证性修复最小改动）
  - 阻塞条件：服务端提供实际 SQL ID 且查询按契约返回 `{amr_code, status}` 行数组（后端不在本 spec 范围）。清单：①真实数据加载与滚动 ②`#select0/#select1` 筛选生效（仅显示筛选内车辆）③刷新间隔符合 `${constant.RefreshHzForAmr}` ④断开服务端请求显示「暂无数据」且其它模块轮询不受影响 ⑤整屏 `scale:true` 缩放下布局正确 ⑥点击行按 `CmsVersion` 正确打开 CMS ⑦运行时复核任务 1 结论（`pages[0].sources` 生效）：观察 `#card6` 绑定差异行为（`$param()` 新写法生效即印证）。
  - _Requirements: 2.1, 2.2, 3.1, 3.2, 6.3_
  - _Depends on: 5, 7, 8_
