# Requirements Document

## Introduction

统计看板「设备实时运行情况」模块（`#card7`，标题键 `$deviceStatus`）当前是一张状态汇总柱状图：`SQL1818567` 返回「运行/空闲/充电/异常/离线」五类计数，前端按 `field1`/`field2` 渲染 5 根柱子。运营人员只能看到各状态的数量，无法看到具体是哪一台车处于什么状态，出问题时无法定位到车。

本需求将该模块改为**逐台车的文字行自动滚动展示**：每一行是一辆车（车号 + 状态），列表超出可视区域时自动向上滚动循环，让全部车辆状态都能被看到。

**范围边界（明确声明）**：本 spec 只负责**前端设计与实现**（布局文件 `DataView_布局文件[0-统计看板].dv.json` 中的组件、脚本与样式）。数据库连接与 SQL 查询在**服务器端（DataView 服务端）**进行，不在本机执行；服务端需提供一个返回逐车状态的查询，前端只定义并消费其数据契约，不实现、不直连数据库。

## Product Alignment

本仓库不存在 `.codex-specs/steering/product.md`（steering 目录未建立），无产品导向文档可对齐。本需求与现有看板的产品意图一致：在深色大屏上实时呈现 AMR 运行态势；改动将「汇总数字」细化到「逐车明细」，提升异常定位效率，不改变看板的其它模块与交互入口。

## Requirements

### Requirement 1: 逐车文字行滚动列表替代柱状图

**User story:** 作为看板使用者，我希望在「设备实时运行情况」模块中逐行看到每台车的车号和状态并自动滚动，以便在不打开明细页的情况下掌握全部车辆的实时状态。

#### Acceptance Criteria

1. WHEN 页面加载完成 THEN 模块 `#card7` 原位置（x=26, y=456, 435×310）渲染为文字行列表而非柱状图，且模块标题仍为 `$deviceStatus`（设备实时运行情况）。
2. WHEN 列表收到服务端数据 THEN 每一行 SHALL 至少包含两个字段：**车号**与**状态**，同一行内车号在前、状态在后，一行只表示一台车。
3. WHEN 状态值为 运行/空闲/充电/异常/离线 之一 THEN 状态文字 SHALL 按既有配色语义着色（运行=蓝绿系、异常=橙红系、离线=灰系、空闲与充电沿用主色系），与原柱状图颜色语义一致。
4. WHEN 行数超过可视区域可容纳的行数 THEN 列表 SHALL 自动向上滚动并在到底后循环回到顶部，滚动平滑、无需人工干预。
5. WHEN 行数未超过可视区域 THEN 列表 SHALL 静止显示，不出现空白行占位滚动。
6. WHEN 模块被点击或刷新 THEN 原柱状图的 ECharts 实例与 `onCard7Click` 柱状点击逻辑 SHALL 不再被创建或触发（避免残留死代码报错）。

### Requirement 2: 服务端数据契约（前端只消费，不连库）

**User story:** 作为前端实现者，我需要一个明确的数据契约，使服务端提供的逐车状态查询能直接驱动列表渲染。

#### Acceptance Criteria

1. WHEN 前端发起本模块数据请求 THEN 请求 SHALL 通过 DataView 平台已有的数据源机制（页面 source / `$queryData`）提交，由**服务端**执行 SQL；前端 SHALL NOT 直连数据库或在本机保存连接凭据。
2. WHEN 服务端返回数据 THEN 返回 SHALL 为行数组，每行至少包含字段：`amr_code`（车号，字符串）与 `status`（状态，取值 运行/空闲/充电/异常/离线 之一）。
3. WHEN `status` 为协议外的未知值 THEN 前端 SHALL 原样显示该状态文字并使用默认色，不抛错、不丢行。
4. IF 服务端返回空数组或请求失败 THEN 模块 SHALL 显示占位文案「暂无数据」，不显示错误堆栈、不影响页面其它模块。
5. WHEN 服务端查询尚未就绪（联调前） THEN 前端 SHALL 能使用与数据契约同形的本地样例数据独立验证渲染与滚动（仅用于开发验证，不进入交付配置）。

### Requirement 3: 刷新频率与筛选参数沿用现状

**User story:** 作为看板使用者，我希望列表的刷新和筛选行为与模块原来一致，不因改造而退化。

#### Acceptance Criteria

1. WHEN 页面运行中 THEN 列表数据 SHALL 按既有刷新间隔 `${constant.RefreshHzForAmr}` 轮询刷新，与改造前一致。
2. WHEN 用户在 `#select0`（地图）或 `#select1`（日期）中切换筛选 THEN 后续刷新请求 SHALL 携带与现状相同的筛选参数（`mapcodes` 等），列表仅展示符合筛选条件的车辆。
3. WHEN 刷新返回的新数据与当前展示数据不同 THEN 列表 SHALL 更新行内容；SHALL NOT 因单次刷新导致滚动位置跳回顶部造成闪烁（滚动进度在刷新间保持连续）。

### Requirement 4: 排序规则

**User story:** 作为看板使用者，我希望需要关注的车辆优先出现在视野里。

#### Acceptance Criteria

1. WHEN 列表渲染 THEN 行 SHALL 按状态优先级排序：异常 → 离线 → 运行 → 充电 → 空闲；同状态内按车号升序。
2. WHEN 单次刷新数据量变化 THEN 排序 SHALL 重新计算，始终保持上述规则。

### Requirement 5: 点击交互

**User story:** 作为看板使用者，我希望点击某台车仍能进入既有的明细/监控入口。

#### Acceptance Criteria

1. WHEN 用户点击列表中的某一行 THEN 前端 SHALL 将该行的 `amr_code` 与 `status` 写入 `sessionStorage['device-status-param']`（沿用原 `onCard7Click` 的参数结构，新增 `amr_code` 字段），并执行与原点击一致的 CMS 跳转逻辑（按 `CmsVersion` 分支）。
2. WHEN 用户点击「暂无数据」占位 THEN 不发生跳转。

### Requirement 6: 布局与视觉一致性

**User story:** 作为看板使用者，我希望改造后的模块与整屏风格无缝融合。

#### Acceptance Criteria

1. WHEN 模块渲染 THEN 其外框位置、尺寸（435×310）与层级（z=37）SHALL 与改造前一致，不影响相邻模块（`#item20230612130352210` 标题等）。
2. WHEN 列表展示 THEN 背景 SHALL 保持看板深色底（`rgba(24,29,77,1)` 体系），文字为白色系，行高与字号在 435×310 内保证 ≥6 行可读（以实际 `rowHeight` 为准）。
3. WHEN 滚动动画运行 THEN 动画 SHALL 平滑匀速，不出现抖动、闪烁或与页面整体缩放（`scale: true`）冲突的错位。

## Non-Functional Requirements

- **Performance:** 车辆数达到 200 台时，列表渲染与滚动 SHALL 保持流畅（无可见卡顿）；单次刷新的数据处理 SHALL 在前端一个刷新周期内完成，不堆积请求。
- **Security:** 前端 SHALL NOT 内置数据库连接串、账号或任何服务端凭据；所有数据经 DataView 平台数据源代理获取。
- **Reliability:** 服务端接口异常 SHALL 被前端捕获并降级为「暂无数据」占位；单个模块失败 SHALL NOT 影响看板其它模块的轮询。
- **Usability:** 状态色对文字有足够对比度；滚动列表在远距离大屏观看下仍可辨识车号与状态。
