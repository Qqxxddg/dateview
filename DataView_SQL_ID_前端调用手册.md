# DataView SQL / 数据源 ID — 前端调用手册

> 来源：`DataView_DataMeta_Server_TAS接口服务等_7_20260929093032.dv.json`  
> 用途：前端布局 / 脚本通过 **数据源 ID（sourceId）** 调用服务端查询，**不要直连数据库**。  
> 字段说明：`入参`/`出参` 取自管理端 inputParams / outputParams；SQL 全文见管理端「数据源配置」。

---

## 1. 前端如何调用

### 1.1 布局 JSON 中作为数据源

```json
{
  "id": "<实例id>",
  "source": "SQL1818567",
  "interval": "${constant.RefreshHzForAmr}",
  "params": { "text": false, "data": null },
  "resultFormat": "map",
  "preHandler": "/* 可选：收集筛选项，return 查询参数对象 */",
  "handler": "/* 可选：回调名 */",
  "binds": [{ "refName": "#cardX", "template": "/* 绑定渲染 */" }]
}
```

### 1.2 脚本内主动查询

```js
// this.doQueryData(sourceId, paramsJsonString, resultType)
let res = await this.doQueryData('SQL19040310', '{}', 'list')
let rows = res.data.data

// 带参数示例
let res2 = await this.doQueryData(
  'SQL09091542',
  JSON.stringify({ mapcodes: 'MAP01', robotcodes: 'AMR001' }),
  'list'
)
```

### 1.3 参数与返回约定

| 约定 | 说明 |
|------|------|
| `${paramName}` | SQL 占位符，由 preHandler / params 注入 |
| `[col in (${param})]` | **可选条件**：参数为空时整段丢弃 |
| `resultFormat: 'map'` | 布局绑定常用 |
| `doQueryData(..., 'list')` | 脚本取行数组常用 |
| 返回结构 | `res.data.data` 为结果；行字段见各数据源「出参」 |

### 1.4 状态码约定（设备类查询通用）

| status2 | 含义 |
|---------|------|
| 0 | 离线 |
| 1 | 运行 |
| 2 | 充电 |
| 3 | 空闲 |
| 4 | 异常 |

---

## 2. 服务连接一览

| 服务名 | serverId | 类型 | 主机:端口 | 库/前缀 | 账号 | 数据源数 |
|--------|----------|------|-----------|---------|------|----------|
| **DATABUS-DB** | `20250513104951` | jdbc/postgresql | `postgres-0-stolon-async.middleware:5432` | databus-rcs | iwms | 4 |
| **DATABUS接口服务** | `20250528121111` | http/http | `databus-rcs.default:80` | /databus-rcs | — | 24 |
| **DATAMETA_DB** | `JDBC0950531` | jdbc/postgresql | `postgres-0-stolon-async.middleware:5432` | datameta | datameta | 197 |
| **CMS_DB** | `JDBC20223541` | jdbc/postgresql | `postgres-0-stolon-async.middleware:5432` | cms_web | cms_web | 105 |
| **CMS接口服务** | `cmsRestApi` | http/http | `rcms.default:80` | — | — | 4 |
| **DATAMETA接口API** | `datametaAPI` | http/http | `datameta.default:80` | — | — | 6 |
| **TAS接口服务** | `tasRestApi` | http/http | `rtas.default:80` | — | — | 3 |

> JDBC 均为 PostgreSQL，主机相同，密码不在导出中（只存服务端）。

---

## 3. 数据源目录（按服务）

### 3.1 DATABUS-DB

- **serverId**: `20250513104951`
- **连接**: `postgres-0-stolon-async.middleware:5432` · endpoint=`databus-rcs` · jdbc/postgresql

| sourceId | 名称 | 分类 | 入参 | 出参 |
|----------|------|------|------|------|
| `getWorkRangeDetail` | 根据序号获取班次时间范围 | 班次/时间范围 | `periodId`:String | `start_time`(起始时间):String, `end_time`(结束时间):String |
| `20250513105335379` | 获取班次列表 | 班次/时间范围 | — | `period_name`(班次名称):String, `period_id`(班次序号):String |
| `SQL09312961` | 查询班次(带跨天判断-根据ID查询) | 班次/时间范围 | `ranges`:String | `range_time_start`:String, `cmp`:String, `range_time_end`:String, `id`:String |
| `SQL10265761` | 班次下拉SQL | 班次/时间范围 | `id`:String | `range_time_start`:String, `cmp`:String, `range_time_end`:String, `name`:String, `id`:String |

<details><summary>SQL / 接口内容摘要</summary>

| sourceId | 名称 | content |
|----------|------|---------|
| `getWorkRangeDetail` | 根据序号获取班次时间范围 | `select to_char(start_time, 'HH24:MI:SS') AS start_time, to_char(end_time, 'HH24:MI:SS') AS end_time from db_period where period_id = ${perio...` |
| `20250513105335379` | 获取班次列表 | `select period_id, period_name from db_period` |
| `SQL09312961` | 查询班次(带跨天判断-根据ID查询) | `select id,range_time_start,range_time_end, case when range_time_start>range_time_end then '>' else '<' end as cmp from ( select period_id as...` |
| `SQL10265761` | 班次下拉SQL | `select period_id\|\|''as id,period_name as name, to_char(start_time,'HH24:MI:SS') as range_time_start, to_char(end_time,'HH24:MI:SS') as range...` |

</details>

### 3.2 DATABUS接口服务

- **serverId**: `20250528121111`
- **连接**: `databus-rcs.default:80` · endpoint=`/databus-rcs` · http/http

| sourceId | 名称 | 分类 | 入参 | 出参 |
|----------|------|------|------|------|
| `REST197151855e8` | 任务耗时-派车耗时 | 任务统计 | `startTime`:String, `endTime`:String, `mapCode`:String, `taskChainType`:None, `range`:String, `siteInfo`:None | 见 SQL / 接口返回 |
| `REST19715185626` | 任务耗时-取货耗时 | 任务统计 | `startTime`:String, `endTime`:String, `mapCode`:String, `taskChainType`:None, `range`:String, `siteInfo`:None | 见 SQL / 接口返回 |
| `REST197151855ds` | 任务总效率(站点) | 任务统计 | `startTime`:String, `endTime`:String, `mapCode`:String, `taskChainType`:None, `siteInfo`:None, `range`:String | 见 SQL / 接口返回 |
| `REST197151855d8` | 任务总效率 | 任务统计 | `startTime`:String, `endTime`:String, `mapCode`:String, `taskChainType`:None, `range`:String | 见 SQL / 接口返回 |
| `REST197151855ce` | 任务耗时-送货耗时 | 任务统计 | `startTime`:String, `endTime`:String, `mapCode`:String, `taskChainType`:None, `range`:String, `siteInfo`:None | 见 SQL / 接口返回 |
| `20250619200519195` | 拣选场景任务量总览 | 任务统计 | `startTime`:String, `endTime`:String, `mapCode`:String, `siteInfo`:None, `workRange`:String, `model`:String | 见 SQL / 接口返回 |
| `20250530171116984` | 子任务详情 | 任务统计 | `mapCode`:None, `amrCode`:None, `taskStatus`:None | `map_name`, `task_chain_code`, `create_time`, `task_status`, `amr_code`, `carrier_code`, `start_slot_code`, `start_x`, `start_y`, `end_slot_code`, `end_x`, `end_y` |
| `REST1971518562s` | 任务耗时-取货耗时(站点) | 任务统计 | `startTime`:String, `endTime`:String, `mapCode`:String, `taskChainType`:None, `range`:String, `siteInfo`:None | 见 SQL / 接口返回 |
| `REST1971518558s` | 任务耗时-派车耗时(站点) | 任务统计 | `startTime`:String, `endTime`:String, `mapCode`:String, `taskChainType`:None, `range`:String, `siteInfo`:None | 见 SQL / 接口返回 |
| `REST1971518555s` | 任务耗时-送货耗时(站点) | 任务统计 | `startTime`:String, `endTime`:String, `mapCode`:String, `taskChainType`:None, `range`:String, `siteInfo`:None | 见 SQL / 接口返回 |
| `REST197151856b1` | 工作站点准点率 | 地图/站点/热力 | `startTime`:String, `endTime`:String, `taskMode`:String, `mapCode`:String, `taskChainType`:None, `range`:String, `siteInfo`:None | 见 SQL / 接口返回 |
| `REST1971518570s` | 超时详情(站点) | 地图/站点/热力 | `startTIme`:String, `endTime`:String, `mapCode`:String, `siteInfo`:None, `taskChainType`:None, `range`:String | 见 SQL / 接口返回 |
| `20250623205406257` | 工作站点效率 | 地图/站点/热力 | `startTime`:String, `endTime`:String, `mapCode`:String, `siteInfo`:None, `workRange`:String, `taskMode`:String | 见 SQL / 接口返回 |
| `REST19716907e88` | 工作台效率 | 效率/等待 | `model`, `startTime`, `endTime`, `mapCode`, `taskType`, `workRange` | `series`, `seriesData`, `xAxis` |
| `REST19715185681` | 生产场景效率总览 | 效率/等待 | `startTime`:String, `endTime`:String, `mapCode`:String, `taskChainType`:None, `range`:String | 见 SQL / 接口返回 |
| `REST1971518570e` | 超时详情 | 效率/等待 | `startTime`, `endTime`, `mapCode`, `taskChainType`, `range` | 见 SQL / 接口返回 |
| `REST19715185714` | 单车效率 | 效率/等待 | `startTime`:String, `endTime`:String, `mapCode`:String, `amrCode`:None, `range`:String, `taskMode`:String | 见 SQL / 接口返回 |
| `REST19716907e94` | 车等人统计 | 效率/等待 | `mapCode`, `startTime`, `endTime`, `taskType`, `workRange`, `siteInfo` | `sumTime`, `avgTime`, `siteInfo`, `allAvgTime`, `maxTime`, `minTime` |
| `REST19716907e98` | 车等人详情 | 效率/等待 | `mapCode`, `startTime`, `endTime`, `taskType`, `workRange`, `siteInfo` | `mapCode`, `mapName`, `siteName`, `siteCoor`, `deliveryTask`, `deliveryCreateTime`, `deliveryTime`, `removeTask`, `removeCreateTime`, `removeTime`, `allTimes` |
| `REST1971a17e585` | 人等车统计-- | 效率/等待 | `mapCode`:String, `startTime`:String, `endTime`:String, `taskType`:String, `model`:String, `workRange`:String, `siteInfo`:String | `xAxis`, `allTimes`, `dispatchTimes`, `delayTimes`, `avgAllTimes`, `avgDispatchTimes`, `avgDelayTimes`, `allTimeAvgLabel`, `allTimeMaxLabel`, `allTimeMinLabel`, `dispatchTimeAvgLabel`, `dispatchTimeMaxLabel`, `dispatchTimeMinLabel`, `delayTimeAvgLabel`, `delayTimeMaxLabel`, `delayTimeMinLabel` |
| `REST1971a17e5ae` | 人等车详情-- | 效率/等待 | `mapCode`:String, `model`:String, `taskType`:String, `startTime`:String, `endTime`:String, `workRange`:String, `siteInfo`:String | `mapCode`, `mapName`, `siteName`, `siteCoor`, `deliveryTask`, `deliveryCreateTime`, `deliveryTime`, `removeTask`, `removeCreateTime`, `removeTime`, `allTimes` |
| `20250704160810980` | 拣选场景等待时间总览 | 效率/等待 | `startTime`:String, `endTime`:String, `mapCode`:String, `siteInfo`:None, `workRange`:String, `model`:String | 见 SQL / 接口返回 |
| `REST19715185703` | 分配指标统计 | 其他 | `mapCode`, `startTime`, `endTime`, `amrCategory` | `xAxis`, `seriesData`, `serieses` |
| `REST1971690d02b` | 算法耗时统计 | 其他 | `mapCode`, `startTime`, `endTime` | `timestamps`, `trpTimes`, `mrtaTimes`, `macgTimes`, `mapfTimes`, `maxTrpTime`, `maxMrtaTime`, `maxMacgTime`, `maxMapfTime`, `avgTrpTime`, `avgMrtaTime`, `avgMacgTime`, `avgMapfTime` |

<details><summary>SQL / 接口内容摘要</summary>

| sourceId | 名称 | content |
|----------|------|---------|
| `REST197151855e8` | 任务耗时-派车耗时 | `/statistical/task/allotTime` |
| `REST19715185626` | 任务耗时-取货耗时 | `/statistical/task/dispatchTime` |
| `REST197151855ds` | 任务总效率(站点) | `/statistical/task/taskOverTimeSite` |
| `REST197151855d8` | 任务总效率 | `/statistical/task/taskOverTime` |
| `REST197151855ce` | 任务耗时-送货耗时 | `/statistical/task/workTime` |
| `20250619200519195` | 拣选场景任务量总览 | `/statistical/task/workbenchTasks` |
| `20250530171116984` | 子任务详情 | `/statistical/task/subTaskDetail` |
| `REST1971518562s` | 任务耗时-取货耗时(站点) | `/statistical/task/dispatchTimeSite` |
| `REST1971518558s` | 任务耗时-派车耗时(站点) | `/statistical/task/allotTimeSite` |
| `REST1971518555s` | 任务耗时-送货耗时(站点) | `/statistical/task/workTimeSite` |
| `REST197151856b1` | 工作站点准点率 | `/statistical/task/workbenchOverTime` |
| `REST1971518570s` | 超时详情(站点) | `/statistical/task/overTimeSite` |
| `20250623205406257` | 工作站点效率 | `/statistical/task/workbenchRate` |
| `REST19716907e88` | 工作台效率 | `/statistical/workbench/efficiency` |
| `REST19715185681` | 生产场景效率总览 | `/statistical/task/taskTypeOverTime` |
| `REST1971518570e` | 超时详情 | `/statistical/task/overTime` |
| `REST19715185714` | 单车效率 | `/statistical/amr/deviceTask` |
| `REST19716907e94` | 车等人统计 | `/statistical/workbench/amrAwait` |
| `REST19716907e98` | 车等人详情 | `/statistical/workbench/amrAwaitDetail` |
| `REST1971a17e585` | 人等车统计-- | `/statistical/workbench/manAwait` |
| `REST1971a17e5ae` | 人等车详情-- | `/statistical/workbench/manAWaitDetail` |
| `20250704160810980` | 拣选场景等待时间总览 | `/statistical/task/workbenchTimes` |
| `REST19715185703` | 分配指标统计 | `/statistical/algorithmic/algAllotData` |
| `REST1971690d02b` | 算法耗时统计 | `/statistical/algorithmic/algTimeData` |

</details>

### 3.3 DATAMETA_DB

- **serverId**: `JDBC0950531`
- **连接**: `postgres-0-stolon-async.middleware:5432` · endpoint=`datameta` · jdbc/postgresql

| sourceId | 名称 | 分类 | 入参 | 出参 |
|----------|------|------|------|------|
| `getTRPAmrCode` | 获取大小车设备编号 | 设备状态/开动率 | — | `amr_type_name`:String, `amr_category`:String, `amr_code`:String |
| `getTRPAmrCodeByTypeCode` | 获取大小车设备编号(设备类型) | 设备状态/开动率 | `amrType`:String | `amr_code` |
| `getTRPAmrType` | 获取大小车设备类型 | 设备状态/开动率 | — | `amr_type_name`:String, `amr_type_code`:String, `amr_category`:String |
| `SQL20345228` | 设备看板-当日地图开动率TOP5 | 设备状态/开动率 | — | `map_code`:String, `rate`:Double |
| `SQL18420368` | EMQ-设备运行-分月 | 设备状态/开动率 | `startTime`:String, `endTime`:String, `mapcodes`:String, `ranges`:String, `robotcodes`:String | 见 SQL / 接口返回 |
| `SQL21343296` | MQ任务量-执行状态 | 设备状态/开动率 | `startTime`:String, `endTime`:String, `ranges`:String, `mapcodes`:String, `taskTypes`:String | `task_status`:String, `count`:Integer |
| `SQL0924422` | 设备看板-设备7日在线趋势 | 设备状态/开动率 | `mapcodes`:String | `map_code`:String, `online`:Double, `time`:String |
| `SQL10414798` | EMQ-在线时长-设备&地图 | 设备状态/开动率 | `mapcodes`:String, `startTime`:String, `endTime`:String | `在线`:Double, `robotcode`:String, `mapcode`:String |
| `SQL21343641` | EMQ-AMR状态(设备&地图) | 设备状态/开动率 | `mapcodes`:String | `status2`:String, `robotcode`:String, `mapcode`:String |
| `SQL10163245` | EMQ-AMR-设备下拉 | 设备状态/开动率 | `startTime`:String, `endTime`:String | `robotcode`:String |
| `SQL14032699` | EMQ-在线时长-设备 | 设备状态/开动率 | `mapcodes`:String, `startTime`:String, `endTime`:String | `在线`:Double, `robotcode`:String |
| `SQL20403129` | 设备看板-昨日地图开动率 | 设备状态/开动率 | `mapcodes`:String | `map_code`:String, `rate`:Double |
| `SQL20460630` | 设备看板-近7日平均开动率 | 设备状态/开动率 | `mapcodes`:String | `map_code`:String, `rate`:Double |
| `SQL13535336` | 设备看板-设备实时分布 | 设备状态/开动率 | `mapcodes`:String | `map_code`:String, `count`:Integer, `status2`:String |
| `SQL10490248` | EMQ-开动率-设备-分月 | 设备状态/开动率 | `startTime`:String, `endTime`:String, `mapcodes`:String, `ranges`:String, `robotcodes`:String | 见 SQL / 接口返回 |
| `SQL15563862` | MQ-设备-任务量-分月 | 设备状态/开动率 | `robotcodes`:String, `mapcodes`:String, `startTime`:String, `endTime`:String, `ranges`:String, `taskTypes`:String | 见 SQL / 接口返回 |
| `SQL15162557` | MQ-设备任务-TOP10 | 设备状态/开动率 | `mapcodes`:String, `startTime`:String, `endTime`:String, `ranges`:String, `taskTypes`:String | `count`:Integer, `robotcode`:String |
| `SQL18391767` | EMQ-设备运行-分日 | 设备状态/开动率 | `startTime`:String, `endTime`:String, `mapcodes`:String, `ranges`:String, `robotcodes`:String | 见 SQL / 接口返回 |
| `SQL15535661` | MQ-设备-任务量-分日 | 设备状态/开动率 | `robotcodes`:String, `mapcodes`:String, `startTime`:String, `endTime`:String, `ranges`:String, `taskTypes`:String | 见 SQL / 接口返回 |
| `SQL15121556` | MQ-设备任务统计 | 设备状态/开动率 | `mapcodes`:String, `startTime`:String, `endTime`:String, `ranges`:String, `taskTypes`:String | `count`:Integer, `robotcode`:String |
| `SQL15402059` | MQ-设备类型-下拉 | 设备状态/开动率 | `startTime`:String, `endTime`:String, `range`:String, `mapcodes`:String, `ranges`:String, `taskTypes`:String | `count`:Integer, `robotcode`:String |
| `SQL15501460` | MQ-设备-任务量-分时 | 设备状态/开动率 | `robotcodes`:String, `mapcodes`:String, `startTime`:String, `endTime`:String, `ranges`:String, `taskTypes`:String | 见 SQL / 接口返回 |
| `SQL21544742` | EMQ-AMR状态(地图) | 设备状态/开动率 | `mapcodes`:String | `空闲`:Double, `充电`:Double, `离线`:Double, `运行`:Double, `异常`:Double, `设备总数`:Double, `mapcode`:String |
| `SQL1819468` | 当日-设备分布情况 | 设备状态/开动率 | `mapcodes`:String | `baterry`:Double, `map_code`:String, `count`:Integer |
| `SQL211659102` | MQ-内嵌-设备下拉 | 设备状态/开动率 | `mapcodes`:String, `startTime`:String, `endTime`:String, `ranges`:String, `taskTypes`:String | `count`:Integer, `robotcode`:String |
| `SQL10583751` | EMQ-开动率-地图-分月 | 设备状态/开动率 | `startTime`:String, `endTime`:String, `mapcodes`:String, `ranges`:String, `robotcodes`:String | 见 SQL / 接口返回 |
| `SQL10544549` | EMQ-开动率-地图-分时 | 设备状态/开动率 | `startTime`:String, `endTime`:String, `mapcodes`:String, `ranges`:String, `robotcodes`:String | 见 SQL / 接口返回 |
| `SQL10102343` | EMQ开动率-地图维度 | 设备状态/开动率 | `mapcodes`:String, `startTime`:String, `endTime`:String, `ranges`:String | `rate`:Double, `mapcode`:String |
| `SQL10564050` | EMQ-开动率-地图-分日 | 设备状态/开动率 | `startTime`:String, `endTime`:String, `mapcodes`:String, `ranges`:String, `robotcodes`:String | 见 SQL / 接口返回 |
| `SQL10415546` | EMQ-开动率-设备-分时 | 设备状态/开动率 | `startTime`:String, `endTime`:String, `mapcodes`:String, `ranges`:String, `robotcodes`:String | 见 SQL / 接口返回 |
| `SQL10354697` | EMQ-在线时长-地图 | 设备状态/开动率 | `mapcodes`:String, `startTime`:String, `endTime`:String | `map_code`:String, `在线`:Double |
| `SQL1540405` | RCS-开动率-设备-分月 | 设备状态/开动率 | `startTime`, `endTime`, `mapcodes`, `ranges`, `robotcodes` | 见 SQL / 接口返回 |
| `SQL21252231` | 设备看板-7日地图开动率趋势TOP | 设备状态/开动率 | `mapcodes`:String | `map_code`:String, `rate`:Double, `time`:String |
| `SQL1530341` | 设备看板-当日设备在线统计 | 设备状态/开动率 | `mapcodes`:String | `map_code`:String, `online`:Double |
| `SQL10472147` | EMQ-开动率-设备-分日 | 设备状态/开动率 | `startTime`:String, `endTime`:String, `mapcodes`:String, `ranges`:String, `robotcodes`:String | 见 SQL / 接口返回 |
| `SQL09371021` | AMR_STATUS_DPS | 设备状态/开动率 | `mapcodes`:String | `status2`:String, `robotcode`:String, `mapcode`:String, `baterry2`:Double, `timestamp`:Date |
| `SQL1403592` | RCS开动率-地图维度 | 设备状态/开动率 | `mapcodes`:String, `startTime`:String, `endTime`:String, `ranges`:String | `rate`:Double, `mapcode`:String |
| `SQL1401221` | RCS开动率-设备维度 | 设备状态/开动率 | `mapcodes`:String, `startTime`:String, `endTime`:String, `ranges`:String, `robotcodes`:String | `rate`:Double, `robotcode`:String |
| `SQL1430253` | RCS-开动率-设备-分时 | 设备状态/开动率 | `startTime`:String, `endTime`:String, `mapcodes`:String, `ranges`:String, `robotcodes`:String | 见 SQL / 接口返回 |
| `SQL1539224` | RCS-开动率-设备-分日 | 设备状态/开动率 | `startTime`, `endTime`, `mapcodes`, `ranges`, `robotcodes` | 见 SQL / 接口返回 |
| `SQL1548237` | RCS-开动率-地图-分日 | 设备状态/开动率 | `startTime`, `endTime`, `mapcodes`, `ranges`, `robotcodes` | 见 SQL / 接口返回 |
| `SQL1549308` | RCS-开动率-地图-分月 | 设备状态/开动率 | `startTime`:String, `endTime`:String, `mapcodes`:String, `ranges`:String, `robotcodes`:String | 见 SQL / 接口返回 |
| `SQL10255922` | AMR_STATUS_COUNT | 设备状态/开动率 | `mapcodes`:String | `count`:Integer, `status2`:String |
| `SQL1546396` | RCS-开动率-地图-分时 | 设备状态/开动率 | `startTime`:String, `endTime`:String, `mapcodes`:String, `ranges`:String, `robotcodes`:String | 见 SQL / 接口返回 |
| `SQL223836101` | EMQ-内嵌-设备下拉 | 设备状态/开动率 | `startTime`:String, `endTime`:String, `mapcodes`:String, `ranges`:String, `param`:None | `空闲`:Double, `充电`:Double, `离线`:Double, `在线`:Double, `运行`:Double, `异常`:Double, `robotcode`:String, `设备总数`:Double |
| `SQL18365566` | EMQ-设备运行-分时 | 设备状态/开动率 | `startTime`:String, `endTime`:String, `mapcodes`:String, `ranges`:String, `robotcodes`:String, `param`:None | 见 SQL / 接口返回 |
| `SQL10142344` | EMQ开动率-设备维度 | 设备状态/开动率 | `mapcodes`:String, `startTime`:String, `endTime`:String, `ranges`:String, `robotcodes`:String | `rate`:Double, `robotcode`:String |
| `SQL101423442` | EMQ开动率-设备维度2 | 设备状态/开动率 | `mapcodes`:String, `startTime`:String, `endTime`:String, `ranges`:String, `robotcodes`:String | `rate`:Double, `robotcode`:String |
| `SQL15562118` | 看板-实时设备数(多地图) | 设备状态/开动率 | `starttime`:String, `endtime`:String, `mapcodes`:String | `map_code`:String, `amr_count`:Double |
| `SQL213609106` | RCS_AGV_地图下拉 | 设备状态/开动率 | `startTime`:String, `endTime`:String | `mapcode`:String |
| `SQL1818567` | 当日-设备运行情况 | 设备状态/开动率 | `mapcodes`:String, `robotcodes`:String | `空闲`:Double, `充电`:Double, `离线`:Double, `运行`:Double, `异常`:Double, `设备总数`:Double |
| `SQL15555517` | 看板-实时设备数(单地图) | 设备状态/开动率 | `sbtype`:String, `mapcode`:String, `starttime`:String, `endtime`:String | `sbtime`:String, `amr_count`:Double |
| `SQL10481725` | 看板-在线时长趋势-日 | 设备状态/开动率 | `mapcodes`:String, `ranges`:String, `dTime1`:String, `dTime2`:String, `robotcodes`:String, `dmCase`:String, `_startTime`:String, `_endTime`:String, `rangeCase1`:String, `range_start`:String, `range_end`:String, `rangeCase2`:String | `online`, `d_time` |
| `SQL21072840` | EMQ-AMR-地图下拉 | 设备状态/开动率 | `mapcodes`:String, `startTime`:String, `endTime`:String, `ranges`:String | `rate`:Double, `mapcode`:String |
| `SQL09091542` | 设备-实时状态 | 设备状态/开动率 | `mapcodes`:String, `robotcodes`:String | `robot_code`:String, `baterry`:Double, `map_code`:String, `rowid`:Integer, `status`:String, `timestamp`:Date |
| `SQL09122443` | 设备-运行时长 | 设备状态/开动率 | `mapcodes`:String, `robotcodes`:String, `startTime`:String, `endTime`:String, `rangeCase`:String, `range_start`:String, `range_end`:String, `dateCase`:String, `_startTime`:String, `_endTime`:String | `robot_code`, `map_code`, `空闲`, `充电`, `离线`, `运行`, `异常` |
| `SQL102023120` | 在线时长-设备 | 设备状态/开动率 | `mapcodes`:String, `time_start`:String, `time_end`:String, `paramCase`:String, `_startTime`:String, `_endTime`:String, `ktCase`:String, `range_start`:String, `range_end`:String | `online`, `amr_code` |
| `SQL112155104` | 开动率-地图-趋势 | 设备状态/开动率 | `dTime1`:String, `mapcodes`:String, `robotcodes`:String, `paramCase1`:String, `_startTime`:String, `_endTime`:String, `isInRange`:String, `ltSql1Case`:String, `range_start`:String, `ytSql1Case`:String, `range_end`:String, `dTime2`:String, `paramCase2`:String, `ltSql2Case`:String, `ytSql2Case`:String | 见 SQL / 接口返回 |
| `SQL171032109` | 开动率-设备 | 设备状态/开动率 | `mapcodes`:String, `ranges`:String, `paramCase`:String, `_startTime`:String, `_endTime`:String, `ktCase`:String, `range_end`:String, `range_start`:String, `isInRange`:String | `rate`, `amr_code` |
| `SQL171234110` | 开动率-设备-趋势 | 设备状态/开动率 | `mapcodes`:String, `robotcodes`:String, `paramCase1`:String, `_startTime`:String, `_endTime`:String, `isInRange`:String, `ltSql1Case`:String, `range_start`:String, `ytSql1Case`:String, `range_end`:String, `paramCase2`:String, `ltSql2Case`:String, `ytSql2Case`:String, `dTime1`:String, `dTime2`:String | 见 SQL / 接口返回 |
| `SQL095121119` | 在线时长-地图 | 设备状态/开动率 | `mapcodes`:String, `time_start`:String, `time_end`:String, `paramCase`:String, `_startTime`:String, `_endTime`:String, `ktCase`:String, `range_start`:String, `range_end`:String | `map_code`, `online` |
| `SQL192549133` | EMQ-设备运行 | 设备状态/开动率 | `mapcodes`:String, `paramCase`:String, `_startTime`:String, `_endTime`:String, `ktCase`:String, `range_start`:String, `range_end`:String, `ranges`:String | `空闲`, `充电`, `离线`, `运行`, `异常`, `robotcode`, `mapcode` |
| `SQL104053121` | 在线时长-设备-趋势 | 设备状态/开动率 | `dTime1`:String, `mapcodes`:String, `robotcodes`:String, `ranges`:String, `paramCase`:String, `_startTime`:String, `_endTime`:String, `ltSql1Case`:String, `range_start`:String, `ytSql1Case`:String, `range_end`:String, `dTime2`:String, `ltSql2Case`:String, `ytSql2Case`:String | 见 SQL / 接口返回 |
| `SQL104237122` | 在线时长-地图-趋势 | 设备状态/开动率 | `dTime1`:String, `mapcodes`:String, `robotcodes`:String, `ranges`:String, `paramCase`:String, `_startTime`:String, `_endTime`:String, `ltSql1Case`:String, `range_start`:String, `ytSql1Case`:String, `range_end`:String, `dTime2`:String, `ltSql2Case`:String, `ytSql2Case`:String | 见 SQL / 接口返回 |
| `SQL20374439` | EMQ-设备运行统计 | 设备状态/开动率 | `mapcode`:String, `startTime`:String, `endTime`:String, `ranges`:String, `mapcodes`:String | `空闲`:Double, `充电`:Double, `离线`:Double, `运行`:Double, `异常`:Double, `robotcode`:String, `mapcode`:String |
| `SQL142720105` | 开动率-地图 | 设备状态/开动率 | `mapcodes`:String, `ranges`:String, `paramCase`:String, `_startTime`:String, `_endTime`:String, `ktCase`:String, `range_start`:String, `range_end`:String, `isInRange`:String | `rate`:Double, `mapcode`:String |
| `SQL17455123` | 看板-开动率趋势-日 | 设备状态/开动率 | `mapcodes`:String, `ranges`:String, `dTime1`:String, `dTime2`:String, `robotcodes`:String, `paramCase`:String, `_startTime`:String, `_endTime`:String, `rangeCase1`:String, `range_start`:String, `range_end`:String, `rangeCase2`:String | `rate`, `d_time` |
| `SQL21054912` | 看板-任务状态统计 | 设备状态/开动率 | `mapcodes`:String, `starttime`:String, `endtime`:String, `range`:String | `status_end`:Integer, `status_start`:Integer, `status_cancel`:Integer, `status_allot`:Integer |
| `SQL12340648` | RCS_AMR_MAP | 设备状态/开动率 | `mapcodes`:String, `startTime`:String, `endTime`:String | `空闲`:Double, `充电`:Double, `运行`:Double, `异常`:Double, `mapcode`:String |
| `SQL15224749` | 5-任务统计-状态 | 设备状态/开动率 | `starttime`:String, `endtime`:String, `range`:String, `tasktype`:String, `mapcode`:String, `tasktypes`:String, `mapcodes`:String | `status_end`:Integer, `status_start`:Integer, `status_cancel`:Integer, `status_allot`:Integer |
| `SQL104033118` | RCS_AMR_STATUS_地图下拉 | 设备状态/开动率 | `startTime`:String, `endTime`:String | `mapcode`:String |
| `SQL10121164` | 下拉-设备运行-设备 | 设备状态/开动率 | `startTime`:String, `endTime`:String | `robotcode`:String |
| `SQL142036108` | RCS_AGV_COUNT | 设备状态/开动率 | `mapcodes`:String | `count`:Integer, `status2`:String |
| `SQL1612323` | 任务看板-任务量-执行状态 | 设备状态/开动率 | `mapcodes`:String, `taskTypes`:String, `startTime`:String | `task_status`:String, `map_code`:String, `count`:Integer |
| `SQL14393374` | 趋势-地图运行-分日 | 设备状态/开动率 | `mapcodes`:String, `ranges`:String, `startTime`:String, `endTime`:String | 见 SQL / 接口返回 |
| `SQL180533113` | TAS_SUB_TASK_AMR | 设备状态/开动率 | `mapcodes`:String, `startTime`:String, `endTime`:String | `task_chain_type`:String, `count`:Integer, `robotcode`:String |
| `SQL141546107` | RCS_AGV_STATUS | 设备状态/开动率 | `mapcodes`:String | `count`:Integer, `status2`:String |
| `SQL15033975` | 趋势-地图运行-分月 | 设备状态/开动率 | `mapcodes`:String, `ranges`:String, `startTime`:String, `endTime`:String | 见 SQL / 接口返回 |
| `SQL10514662` | RCS_AGV_STATUS_ROBOT | 设备状态/开动率 | `mapcodes`:String | `status2`:String, `robotcode`:String, `mapcode`:String |
| `SQL21565924` | 开动率趋势1 | 设备状态/开动率 | `mapcodes`:String, `startTime`:String, `endTime`:String | `agg_time`:Date, `空闲`:Double, `充电`:Double, `运行`:Double, `异常`:Double |
| `SQL2014154` | ON_TIME_DEVICE | 设备状态/开动率 | `mapcodes`:String, `startTime`:String, `endTime`:String | `在线`:Double, `robotcode`:String, `mapcode`:String |
| `SQL144759109` | RCS_AMR_TIME | 设备状态/开动率 | `mapcodes`:String, `startTime`:String, `endTime`:String, `ranges`:String, `robotcodes`:String | `空闲`:Double, `充电`:Double, `运行`:Double, `异常`:Double, `robotcode`:String |
| `SQL17082861` | 趋势-设备运行-分日 | 设备状态/开动率 | `mapcode`:String, `startTime`:String, `endTime`:String, `ranges`:String, `robotcodes`:String, `mapcodes`:String | `空闲`:Double, `充电`:Double, `time`:String, `运行`:Double, `异常`:Double |
| `SQL13514666` | 下拉-任务量-设备 | 设备状态/开动率 | `startTime`:String, `endTime`:String, `ranges`:String | `robotcode`:String |
| `SQL17203824` | 任务量统计-设备top10 | 设备状态/开动率 | `mapcodes`:String, `startTime`:String, `endTime`:String, `ranges`:String, `taskTypes`:String | 见 SQL / 接口返回 |
| `SQL13422849` | 趋势-地图运行-分时 | 设备状态/开动率 | `mapcodes`:String, `startTime`:String, `endTime`:String, `ranges`:String | `agg_time`:Date, `空闲`:Double, `充电`:Double, `运行`:Double, `异常`:Double, `mapcode`:String |
| `SQL17482123` | 开动率指标 | 设备状态/开动率 | `mapcodes`:String, `startTime`:String, `endTime`:String | `空闲`:Double, `充电`:Double, `运行`:Double, `异常`:Double, `robotcode`:String |
| `SQL15151767` | 趋势-任务量-设备-分时 | 设备状态/开动率 | `mapcodes`:String, `startTime`:String, `endTime`:String, `ranges`:String, `taskTypes`:String | 见 SQL / 接口返回 |
| `SQL15313668` | 趋势-任务量-设备-分日 | 设备状态/开动率 | `mapcodes`:String, `startTime`:String, `endTime`:String, `ranges`:String, `taskTypes`:String, `robotcodes`:String | 见 SQL / 接口返回 |
| `SQL08570161` | RCS_AGV_STATUS_MAP | 设备状态/开动率 | `mapcodes`:String | `空闲`:Integer, `充电`:Integer, `离线`:Integer, `运行`:Integer, `异常`:Integer, `mapcode`:String |
| `SQL145212110` | RCS_AMR_RUN_RATE | 设备状态/开动率 | `mapcodes`:String, `startTime`:String, `endTime`:String, `robotcodes`:String, `ranges`:String | `agg_time`:Date, `空闲`:Double, `充电`:Double, `运行`:Double, `异常`:Double, `robotcode`:String |
| `SQL09373165` | 趋势-任务量-设备-分月 | 设备状态/开动率 | `mapcodes`:String, `startTime`:String, `endTime`:String, `ranges`:String, `taskTypes`:String, `robotcodes`:String | 见 SQL / 接口返回 |
| `SQL17151723` | 任务量统计-设备 | 设备状态/开动率 | `mapcodes`:String, `startTime`:String, `endTime`:String, `ranges`:String, `taskTypes`:String | `count`:Integer, `robotcode`:String |
| `SQL205006105` | RCS_AGV_UPDATA | 设备状态/开动率 | `mapcode`:String, `startTime`:String, `endTime`:String, `ranges`:String | `空闲`:Double, `充电`:Double, `运行`:Double, `异常`:Double, `robotcode`:String, `mapcode`:String |
| `SQL17140663` | 趋势-设备运行-分月 | 设备状态/开动率 | `mapcode`:String, `startTime`:String, `endTime`:String, `ranges`:String, `robotcodes`:String | `空闲`:Double, `充电`:Double, `time`:String, `运行`:Double, `异常`:Double |
| `SQL17124962` | 趋势-设备运行-分时 | 设备状态/开动率 | `mapcode`:String, `startTime`:String, `endTime`:String, `ranges`:String, `robotcodes`:String | `空闲`:Double, `充电`:Double, `time`:String, `运行`:Double, `异常`:Double |
| `getTRPTaskChainCode` | 获取时段内TRP任务编号 | 任务统计 | `startTime`:String, `endTime`:String, `mapCode`:String, `lineCode`:String, `areaCode`:String, `workType`:String | `task_chain_code` |
| `getTRPTaskCount` | 获取大小车任务统计 | 任务统计 | `hour_date`:String, `day_date`:String, `month_date`:String, `queryDateLength`:String, `taskType`:String, `mapCode`:String, `lineCode`:String, `areaCode`:String, `workType`:String | `total_count`, `querydate` |
| `getTRPTaskCountNF` | 获取大小车任务统计(待完成) | 任务统计 | `queryDateLength`:String, `taskType`:String, `mapCode`:String, `lineCode`:String, `areaCode`:String, `workType`:String, `hour_date`:String, `day_date`:String, `month_date`:String | `total_count`, `querydate` |
| `SQL20224495` | MQ任务量-地图 | 任务统计 | `taskTypes`:String, `mapcodes`:String, `startTime`:String, `endTime`:String, `ranges`:String | `map_code`:String, `count`:Integer |
| `SQL15081055` | MQ-地图任务统计 | 任务统计 | `mapcodes`:String, `startTime`:String, `endTime`:String, `ranges`:String, `taskTypes`:String | `map_code`:String, `count`:Integer |
| `SQL16420092` | MQ任务-类型-分时 | 任务统计 | `mapcodes`:String, `startTime`:String, `endTime`:String, `ranges`:String, `taskTypes`:String | 见 SQL / 接口返回 |
| `SQL182130114` | TAS_SUB_TASK_MAP | 任务统计 | `mapcodes`:String, `startTime`:String, `endTime`:String | `count`:Integer, `range`:Integer, `mapcode`:String |
| `SQL16434293` | MQ任务-类型-分日 | 任务统计 | `mapcodes`, `startTime`, `endTime`, `ranges`, `taskTypes` | 见 SQL / 接口返回 |
| `SQL16442594` | MQ任务-类型-分月 | 任务统计 | `mapcodes`:String, `startTime`:String, `endTime`:String, `ranges`:String, `taskTypes`:String | 见 SQL / 接口返回 |
| `SQL14523853` | MQ-任务类型-下拉 | 任务统计 | `startTime`:String, `endTime`:String, `range`:String, `mapcodes`:String, `ranges`:String, `taskTypes`:String | `task_chain_type`:String, `count`:Integer |
| `SQL15230158` | MQ-任务类型统计 | 任务统计 | `mapcodes`:String, `startTime`:String, `endTime`:String, `ranges`:None, `taskTypes`:String | `task_chain_type`:String, `count`:Integer |
| `SQL16042763` | MQ-地图-任务量-分月 | 任务统计 | `robotcodes`:String, `mapcodes`:String, `startTime`:String, `endTime`:String, `ranges`:String, `taskTypes`:String | 见 SQL / 接口返回 |
| `SQL1432318` | 任务看板-近7日地图任务量 | 任务统计 | `mapcodes`:String | `map_code`:String, `count`:Integer, `time`:String |
| `SQL14500252` | MQ-任务单统计 | 任务统计 | `startTime`:String, `endTime`:String, `range`:String, `taskTypes`:String, `ranges`:String | `avg_exec_time`:String, `avg_empty_run_time`:String, `avg_reply_time`:String, `reply_time`:String, `empty_run_time`:String, `avg_eft_time`:String, `task_chain_type`:String, `exec_time`:String, `count`:Integer, `eft_time`:String, `carrier_lift_time`:String, `avg_carrier_lift_time`:String |
| `SQL1436099` | 任务看板-近7日地图平均任务量 | 任务统计 | `mapcodes`:String | `map_code`:String, `sum`:Double |
| `SQL16093165` | MQ-地图-任务量-分时 | 任务统计 | `robotcodes`:String, `mapcodes`:String, `startTime`:String, `endTime`:String, `ranges`:String, `taskTypes`:String | 见 SQL / 接口返回 |
| `SQL16064064` | MQ-地图-任务量-分日 | 任务统计 | `robotcodes`:String, `mapcodes`:String, `startTime`:String, `endTime`:String, `ranges`:String, `taskTypes`:String | 见 SQL / 接口返回 |
| `SQL11402481` | 5-任务统计-任务量 | 任务统计 | `tasktypes`:String, `mapcodes`:String, `starttime`:String, `endtime`:String, `range`:String | `map_code`:String, `count`:Integer |
| `SQL16290884` | 5-任务统计-按月趋势 | 任务统计 | `tasktypes`:String, `starttime`:String, `endtime`:String, `range`:String, `mapcodes`:String | `map_code`:String, `counts`:Integer, `d_time`:String |
| `SQL16380991` | 任务量-趋势 | 任务统计 | `dTime1`:String, `robotcodes`:String, `mapcodes`:String, `dTime2`:String, `tmCase`:String, `_startTime`:String, `_endTime`:String, `rangeCase1`:String, `range_start`:String, `range_end`:String, `rangeCase2`:String | 见 SQL / 接口返回 |
| `SQL202952114` | 6-任务类型统计-作业比按月趋势 | 任务统计 | `tasktypes`:String, `range`:String, `starttime`:String, `endtime`:String | `work_scale`:Double, `task_chain_type`:String, `d_time`:String |
| `SQL202721112` | 6-任务类型统计-作业比按时趋势 | 任务统计 | `tasktypes`:String, `range`:String, `starttime`:String, `endtime`:String | `work_scale`:Double, `task_chain_type`:String, `d_time`:String |
| `SQL213507102` | 6-任务类型统计-任务量按日趋势 | 任务统计 | `tasktypes`:String, `range`:String, `starttime`:String, `endtime`:String, `selrange`:Integer | `counts`:Integer, `task_chain_type`:String, `d_time`:String |
| `SQL21050111` | 看板-任务数量趋势(单地图) | 任务统计 | `sbtype`:Integer, `endtime`:String, `mapcode`:String, `starttime`:String, `range`:String | `sbtime`:String, `counts`:Integer |
| `SQL11373715` | 看板-任务数量趋势(多地图) | 任务统计 | `starttime`:String, `endtime`:String, `mapcodes`:String, `range`:String | `counts`:Integer, `mapcode`:String |
| `SQL16162082` | 5-任务统计-按时趋势 | 任务统计 | `tasktypes`:String, `starttime`:String, `endtime`:String, `range`:String, `mapcodes`:String | `map_code`:String, `counts`:Integer, `d_time`:String |
| `SQL16284383` | 5-任务统计-按日趋势 | 任务统计 | `tasktypes`:String, `starttime`:String, `endtime`:String, `range`:String, `mapcodes`:String, `selrange`:Integer=0 | `map_code`:String, `counts`:Integer, `d_time`:String |
| `SQL210304100` | 6-任务类型统计-任务量 | 任务统计 | `tasktypes`:String, `range`:String, `starttime`:String, `endtime`:String | `counts`:Integer, `task_chain_type`:String |
| `SQL213356101` | 6-任务类型统计-任务量按时趋势 | 任务统计 | `tasktypes`:String, `range`:String, `starttime`:String, `endtime`:String | `counts`:Integer, `task_chain_type`:String, `d_time`:String |
| `SQL145313106` | 6-任务类型统计-任务表格 | 任务统计 | `tasktypes`:String, `range`:String, `starttime`:String, `endtime`:String | `avg_execute_time`:Double, `avg_work_time`:Double, `avg_mileage`:Double, `work_scale`:Double, `avg_dispatch_time`:Double, `avg_speed`:Double, `counts`:Integer, `task_chain_type`:String, `avg_produce_time`:Double, `avg_remove_carrier`:Double, `avg_allot_time`:Double, `avg_battery`:0 |
| `SQL165801108` | 6-任务类型统计-时长按日趋势 | 任务统计 | `time1`:None, `time2`:None, `tasktypes`:String, `range`:String, `starttime`:String, `endtime`:String, `selrange`:Integer | `task_chain_type`:String, `d_time`:String, `avg_time`:0 |
| `SQL194831111` | 6-任务类型统计-时长按月趋势 | 任务统计 | `tasktypes`:String, `range`:String, `starttime`:String, `endtime`:String, `time1`:None, `time2`:None | `avg_time`:0, `task_chain_type`:0, `d_time`:0 |
| `SQL164825107` | 6-任务类型统计-时长按时趋势 | 任务统计 | `tasktypes`:String, `range`:String, `starttime`:String, `endtime`:String, `time1`:None, `time2`:None | `avg_time`:0, `task_chain_type`:0, `d_time`:0 |
| `SQL202845113` | 6-任务类型统计-作业比按日趋势 | 任务统计 | `tasktypes`:String, `range`:String, `starttime`:String, `endtime`:String, `selrange`:Integer | `work_scale`:Double, `task_chain_type`:String, `d_time`:String |
| `SQL213550103` | 6-任务类型统计-任务量按月趋势 | 任务统计 | `tasktypes`:String, `range`:String, `starttime`:String, `endtime`:String | `counts`:Integer, `task_chain_type`:String, `d_time`:String |
| `SQL15202628` | 看板-任务平均数据 | 任务统计 | `mapcodes`:String, `starttime`:String, `endtime`:String, `range`:String | `exec_scale`:Double, `task_type`:String, `avg_task_time`:Double |
| `SQL1549091` | 6-任务类型统计-执行时间按时统计趋势 | 任务统计 | `tasktypes`:String, `range`:String, `starttime`:String, `endtime`:String | `task_chain_type`:String, `d_time`:String, `avg_time`:Double |
| `SQL1607342` | 6-任务类型统计-执行时间按日统计趋势 | 任务统计 | `starttime`:String, `endtime`:String, `selrange`:String, `tasktypes`:String, `range`:String | `task_chain_type`:String, `d_time`:String, `avg_time`:Double |
| `SQL1609233` | 6-任务类型统计-执行时间按月统计趋势 | 任务统计 | `tasktypes`:String, `range`:String, `starttime`:String, `endtime`:String | `task_chain_type`:String, `d_time`:String, `avg_time`:Double |
| `SQL12230243` | 任务单-类型下拉 | 任务统计 | `startTime`:String, `endTime`:String, `range`:String, `ranges`:String | `task_chain_type`:String |
| `SQL2043137` | 任务看板-地图(任务量TOP10) | 任务统计 | `mapcodes`:String | `map_code`:String, `count`:Integer |
| `SQL2025316` | 任务看板-任务类型(任务量TOP10) | 任务统计 | `mapcodes`:String | `task_chain_type`:String, `count`:Integer |
| `SQL1538132` | 任务看板-任务量-昨日 | 任务统计 | `mapcodes`:String | `map_code`:String, `count`:Integer |
| `SQL1754475` | 任务看板-任务类型当日趋势 | 任务统计 | `mapcodes`:String | `task_chain_type`:String, `count`:Integer, `time`:String |
| `SQL1648474` | 任务看板-地图当日任务量趋势 | 任务统计 | `mapcodes`:String | `map_code`:String, `count`:Integer, `time`:String |
| `SQL16484742` | 任务看板-地图当日任务量趋势2 | 任务统计 | `mapcodes`:String | `map_code`:String, `count`:Integer, `time`:String |
| `SQL1429201` | 任务看板-任务量-今日 | 任务统计 | `startTime`:String, `endTime`:String, `range`:String, `taskTypes`:String | `map_code`:String, `count`:Integer |
| `SQL163925112` | TAS_SUB_TASK_TYPE | 任务统计 | `mapcodes`:String, `startTime`:String, `endTime`:String, `range`:String, `taskTypes`:String | `task_chain_type`:String, `count`:Integer, `range`:Integer, `time`:String |
| `SQL15480721` | TAS_TASK_TYPE_COUNT | 任务统计 | `mapcodes`:String, `startTime`:String, `endTime`:String, `ranges`:String, `taskTypes`:String | `task_chain_type`:String, `count`:Integer, `range`:Integer |
| `SQL192915116` | TAS_地图下拉 | 任务统计 | `startTime`:String, `endTime`:String | `map_code`:String |
| `SQL163851111` | TAS_SUB_TASK_TIME | 任务统计 | `mapcodes`:String, `startTime`:String, `endTime`:String, `range`:String, `taskTypes`:String | `avg_exec_time`:String, `avg_empty_run_time`:String, `avg_reply_time`:String, `reply_time`:String, `empty_run_time`:String, `task_chain_type`:String, `count`:Integer, `exec_time`:String, `range`:Integer, `carrier_lift_time`:String, `avg_carrier_lift_time`:String |
| `SQL17111122` | 任务量统计-地图 | 任务统计 | `mapcodes`:String, `startTime`:String, `endTime`:String, `ranges`:String, `taskTypes`:String | `map_code`:String, `count`:Integer |
| `SQL192230115` | TAS_任务类型下拉 | 任务统计 | `startTime`:String, `endTime`:String | `task_chain_type`:String |
| `SQL19531972` | 趋势-任务量-地图-分日 | 任务统计 | `mapcodes`:String, `startTime`:String, `endTime`:String, `ranges`:String, `taskTypes`:String | 见 SQL / 接口返回 |
| `SQL15532469` | 趋势-任务量-地图-分月 | 任务统计 | `mapcodes`:String, `startTime`:String, `endTime`:String, `ranges`:String, `taskTypes`:String | 见 SQL / 接口返回 |
| `SQL12062442` | 任务单统计-SQL | 任务统计 | `startTime`:String, `endTime`:String, `range`:String, `taskTypes`:String, `ranges`:None, `sort`:None | `avg_exec_time`:String, `avg_empty_run_time`:String, `avg_reply_time`:String, `reply_time`:String, `empty_run_time`:String, `avg_eft_time`:String, `task_chain_type`:String, `exec_time`:String, `count`:Integer, `eft_time`:String, `carrier_lift_time`:String, `avg_carrier_lift_time`:String |
| `SQL18200670` | 趋势-任务量-地图-分时 | 任务统计 | `mapcodes`:String, `startTime`:String, `endTime`:String, `ranges`:String, `taskTypes`:String | 见 SQL / 接口返回 |
| `SQL15441316` | 看板-MTBF-在线时长 | 告警/故障 | `mapcodes`:String, `time_start`:String, `time_end`:String, `paramCase`:String, `range_start`:String, `range_end`:String, `psCase`:String, `range_hour`:String | `online` |
| `SQL112609120` | 设备故障对应在线时长统计 | 告警/故障 | `mapcodes`:String, `startTime`:String, `endTime`:String | `在线`:Double, `robotcode`:String, `mapcode`:String |
| `SQL16583493` | 3-充电统计-充电桩按日趋势 | 充电/电量 | `starttime`:String, `endtime`:String, `range`:String, `mapcodes`:String, `amrcode`:String, `chargers`:String, `selrange`:Integer | `charge_code`:String, `scale`:Double, `d_time`:String |
| `SQL16154531` | 看板-充电数据 | 充电/电量 | `mapcodes`:String, `starttime`:String, `endtime`:String, `range`:String | `map_code`:String, `scale`:String, `battery`:Double, `amr_code`:String, `success`:0 |
| `SQL202406141` | 2-设备详情-充电数据-按时 | 充电/电量 | `starttime`:String, `endtime`:String, `range`:String, `mapcodes`:String, `amrcode`:String | `counts`:0, `scale`:0, `d_time`:0 |
| `SQL15230390` | 3-充电统计-设备充电数据 | 充电/电量 | `starttime`:String, `endtime`:String, `range`:String, `mapcodes`:String, `amrcode`:String, `chargers`:String | `counts`:Integer, `abnormal_count`:Integer, `success_scale`:Double, `avg_charge_battery`:Double, `avg_consume_battery`:Double, `amr_code`:String, `charge_time`:String |
| `SQL14184787` | 3-充电统计-设备按时趋势 | 充电/电量 | `starttime`:String, `endtime`:String, `range`:String, `mapcodes`:String, `amrcode`:String, `chargers`:String | `scale`:Double, `amr_code`:String, `d_time`:String |
| `SQL17260495` | 3-充电统计-耗电量按时趋势 | 充电/电量 | `starttime`:String, `endtime`:String, `range`:String, `mapcodes`:String, `amrcode`:String | `battery`:Double, `amr_code`:String, `d_time`:String |
| `SQL14234789` | 3-充电统计-设备按月趋势 | 充电/电量 | `starttime`:String, `endtime`:String, `range`:String, `mapcodes`:String, `amrcode`:String, `chargers`:String | `scale`:Double, `amr_code`:String, `d_time`:String |
| `SQL14214288` | 3-充电统计-设备按日趋势 | 充电/电量 | `starttime`:String, `endtime`:String, `range`:String, `mapcodes`:String, `amrcode`:String, `chargers`:String, `selrange`:Integer | `scale`:Double, `amr_code`:String, `d_time`:String |
| `SQL17275396` | 3-充电统计-耗电量按日趋势 | 充电/电量 | `starttime`:String, `endtime`:String, `range`:String, `mapcodes`:String, `amrcode`:String, `selrange`:Integer | `battery`:Double, `amr_code`:String, `d_time`:String |
| `SQL17291497` | 3-充电统计-耗电量按月趋势 | 充电/电量 | `starttime`:String, `endtime`:String, `range`:String, `mapcodes`:String, `amrcode`:String | `battery`:Double, `amr_code`:String, `d_time`:String |
| `SQL154524124` | 2-设备详情-充电次数按日趋势 | 充电/电量 | `starttime`:String, `endtime`:String, `range`:String, `mapcodes`:String, `amrcode`:String | `counts`:Integer, `success_scale`:Double, `amr_code`:String, `d_time`:String |
| `SQL213308142` | 2-设备详情-充电数据-按日 | 充电/电量 | `starttime`:String, `endtime`:String, `selrange`:String, `range`:String, `mapcodes`:String, `amrcode`:String | `scale`:0, `counts`:0, `d_time`:0 |
| `SQL16564692` | 3-充电统计-充电桩按时趋势 | 充电/电量 | `starttime`:String, `endtime`:String, `range`:String, `mapcodes`:String, `amrcode`:String, `chargers`:String | `charge_code`:String, `scale`:Double, `d_time`:String |
| `SQL17021994` | 3-充电统计-充电桩按月趋势 | 充电/电量 | `starttime`:String, `endtime`:String, `range`:String, `mapcodes`:String, `amrcode`:String, `chargers`:String | `charge_code`:String, `scale`:Double, `d_time`:String |
| `SQL213054161` | 1-设备状态-充电桩利用率 | 充电/电量 | `endtime`:String, `starttime`:String, `range`:String, `mapcodes`:String, `chargercount`:Integer | `charge_use`:String, `charge_time`:String |
| `SQL214606143` | 2-设备详情-充电数据-按月 | 充电/电量 | `starttime`:String, `endtime`:String, `range`:String, `mapcodes`:String, `amrcode`:String | `counts`:0, `d_time`:0, `scale`:0 |
| `SQL195308126` | 1-设备状态-充电数据 | 充电/电量 | `starttime`:String, `endtime`:String, `range`:String, `mapcodes`:String, `amrcode`:String | `counts`:Integer, `success_scale`:Double, `amr_code`:String |
| `SQL154803125` | 2-设备详情-充电次数按月趋势 | 充电/电量 | `starttime`:String, `endtime`:String, `range`:String, `mapcodes`:String, `amrcode`:String | `counts`:Integer, `success_scale`:Double, `amr_code`:String, `d_time`:String |
| `SQL154355123` | 2-设备详情-充电次数按时趋势 | 充电/电量 | `starttime`:String, `endtime`:String, `range`:String, `mapcodes`:String, `amrcode`:String | `counts`:Integer, `success_scale`:Double, `amr_code`:String, `d_time`:String |
| `SQL19391798` | 3-充电统计-充电桩数据 | 充电/电量 | `starttime`:String, `endtime`:String, `range`:String, `mapcodes`:String, `amrcode`:String, `chargers`:String | `avg_charge_time`:String, `counts`:Integer, `little_time`:Integer, `abnormal_count`:Integer, `charge_code`:String, `abnormal_scale`:Double, `charge_time`:String, `charge_use`:0 |
| `sqlQueryLifts` | 获取电梯列表 | 地图/站点/热力 | — | `lift_code`:String, `lift_name`:String |
| `SQL15005554` | MQ-地图下拉 | 地图/站点/热力 | `startTime`:String, `endTime`:String, `range`:String, `ranges`:String | `map_code`:String, `count`:Integer |
| `SQL15170041` | 储位热力图 | 地图/站点/热力 | `starttime`:String, `endtime`:String, `mapcode`:String, `range`:String | `counts`:Double, `site_code`:String |
| `SQL14164048` | 轨迹热力图 | 地图/站点/热力 | `mapcode`:String, `starttime`:String, `endtime`:String, `timeslimit`:Integer, `range`:String | `counts`:Integer, `cooy`:Integer, `coox`:Integer, `times`:0 |
| `SQL2013293` | ON_TIME_MAP | 地图/站点/热力 | `mapcodes`:String, `startTime`:String, `endTime`:String | `在线`:Double, `mapcode`:String |
| `getTimeSlots` | 获取划分时间段 | 班次/时间范围 | — | `generate_series`:Integer |
| `SQL1848179` | 计算当前班次 | 班次/时间范围 | — | `range_end`:Date, `name`:String, `range_start`:Date, `id`:Integer |
| `SQL11170614` | 计算上个同班次 | 班次/时间范围 | — | `range_end`:Date, `range_start`:Date, `id`:Integer |
| `SQL18502919` | 查询班次(带跨天判断) | 班次/时间范围 | — | `range_time_start`:String, `cmp`:String, `range_time_end`:String, `id`:Integer |
| `SQL21280647` | 看板-获取时间查询范围 | 班次/时间范围 | `type`:String, `range`:String | `start_time`:String, `end_time`:String |
| `SQL19521699` | 计算班次-根据当前时间自动联动日期 | 班次/时间范围 | `ranges`:String | `range_end`:Date, `range_time_start`:String, `cmp`:String, `name`:String, `range_start`:Date, `range_time_end`:String, `id`:Integer |
| `SQL10280613` | 开动率-当前班次 | 班次/时间范围 | `time_start`:String, `time_end`:String, `paramCase`:String, `range_time_start`:String, `range_time_end`:String, `psCase`:String, `range_hour`:String, `mapcodes`:String | `rate` |
| `SQL180551181` | 获取当日生产计划 | 班次/时间范围 | — | `range_type_id`:Integer |
| `getWorkbenchWaitTimes` | 获取拣选场景等待时间总览 | 效率/等待 | `startTime`:String, `endTime`:String, `workRange`:String, `mapCode`:String, `siteInfo`:String, `model`:String | `site_name`, `avg_man_times`, `avg_amr_times` |
| `getManAwaitDetail` | 人等车详情-db | 效率/等待 | `mapCode`:String, `startTime`:String, `endTime`:String, `workRange`:String, `taskType`:String, `siteInfo`:String, `subTaskCode`:String, `model`:String | `site_name`, `site_coor`, `map_code`, `delivery_task`, `create_delivery_time`, `delivery_time`, `remove_task`, `create_remove_time`, `remove_time`, `man_await_times`, `delivery_carrier_code`, `remove_carrier_code` |
| `getAmrAwaitDetail` | 车等人详情-db | 效率/等待 | `mapCode`:String, `startTime`:String, `endTime`:String, `workRange`:String, `taskType`:String, `siteInfo`:String | `site_coor`, `map_code`, `delivery_task`, `remove_task`, `create_delivery_time`, `delivery_time`, `create_remove_time`, `remove_time`, `amr_await_times`, `site_name`, `delivery_carrier_code`, `remove_carrier_code` |
| `getCTUFullLoadRate` | 获取CTU满载率 | 效率/等待 | `startTime`:String, `endTime`:String, `mapCode`:String, `amrCode`:String | `map_name`, `amr_code`, `layer`, `loadtime`, `fullloadrate` |
| `getTRPDetail` | 获取大小车出入库详情 | 下拉/字典/列表 | `mapCode`:String, `amrType`:String, `amrCode`:String, `startTime`:String, `endTime`:String, `range`:String | `map_code`, `amr_type_name`, `amr_code`, `out_number`, `out_avg_time`, `out_time`, `in_number`, `in_avg_time`, `in_time`, `all_task_time`, `in_break_number` |
| `getCTUAmrCode` | 获取CTU车号-下拉 | 下拉/字典/列表 | — | `amr_name`:String, `amr_code`:String |
| `getCTUAmrCodeByType` | 获取CTU车号(车型) | 下拉/字典/列表 | `amrType`:String | `amr_code` |
| `getCTUAmrType` | 获取CTU车型-下拉 | 下拉/字典/列表 | — | `amr_type_name`:String |
| `SQL103550144` | 测试 | 其他 | `starttime`:String, `endtime`:String | `d_time`:0 |

<details><summary>SQL / 接口内容摘要</summary>

| sourceId | 名称 | content |
|----------|------|---------|
| `getTRPAmrCode` | 获取大小车设备编号 | `select amr_type_name,amr_category,amr_code from dps_sync_amr da left join dps_sync_amr_type dat on da.type_code = dat.amr_type_code where da...` |
| `getTRPAmrCodeByTypeCode` | 获取大小车设备编号(设备类型) | `select da.amr_code from dps_sync_amr da left join dps_sync_amr_type dat on dat.amr_type_code = da.type_code where dat.amr_type_code in (${am...` |
| `getTRPAmrType` | 获取大小车设备类型 | `select amr_type_name,amr_category,amr_type_code from dps_sync_amr_type where amr_category in ('10','40')` |
| `SQL20345228` | 设备看板-当日地图开动率TOP5 | `select map_code,case when ("运行"+"空闲"+"异常")=0 then 0 else "运行"/("运行"+"空闲"+"异常") end as rate from ( select map_code ,SUM (CASE WHEN status2='1...` |
| `SQL18420368` | EMQ-设备运行-分月 | `select COALESCE("运行",0) as "运行", COALESCE("充电",0) as "充电",COALESCE("空闲",0) as "空闲",COALESCE("异常",0) as "异常",COALESCE("离线",0) as "异常",time ,r...` |
| `SQL21343296` | MQ任务量-执行状态 | `select task_status,count(1) from ( select task_chain_code,task_chain_type,map_code,case when task_status='10' then '9' else task_status end ...` |
| `SQL0924422` | 设备看板-设备7日在线趋势 | `select map_code,online,s.time from ( select map_code,sum(times) as online,to_char(agg_time,'yyyy-mm-dd') as "d_time" from emq_agv_view_001 w...` |
| `SQL10414798` | EMQ-在线时长-设备&地图 | `select amr_code as robotcode,map_code as mapcode,sum(times) as "在线" from emq_agv_view_001 where status2 in ('1','2','3','4') and [map_code i...` |
| `SQL21343641` | EMQ-AMR状态(设备&地图) | `select map_code as mapcode,amr_code as robotcode,status2 from (select * from (SELECT ROW_NUMBER() OVER (partition BY map_code,amr_code ORDER...` |
| `SQL10163245` | EMQ-AMR-设备下拉 | `select distinct amr_code as robotcode from emq_agv_view_001 where [agg_time >=${startTime}] and [agg_time < ${endTime}]` |
| `SQL14032699` | EMQ-在线时长-设备 | `select amr_code as robotcode,sum(times) as "在线" from emq_agv_view_001 where status2 in ('1','2','3','4') and [map_code in (${mapcodes})] and...` |
| `SQL20403129` | 设备看板-昨日地图开动率 | `select map_code,case when ("运行"+"空闲"+"异常")=0 then 0 else "运行"/("运行"+"空闲"+"异常") end as rate from ( select map_code ,SUM (CASE WHEN status2='1...` |
| `SQL20460630` | 设备看板-近7日平均开动率 | `select map_code,case when ("运行"+"空闲"+"异常")=0 then 0 else "运行"/("运行"+"空闲"+"异常") end as rate from ( select map_code ,SUM (CASE WHEN status2='1...` |
| `SQL13535336` | 设备看板-设备实时分布 | `select map_code,status2,count(1) from (select * from (SELECT ROW_NUMBER() OVER (partition BY map_code,amr_code ORDER BY timestamp desc)rowId...` |
| `SQL10490248` | EMQ-开动率-设备-分月 | `select amr_code as robotcode,rate,n.time from ( select amr_code,case when "运行"=0 then 0 else "运行"/("运行"+"空闲"+"异常") end as rate,d_time from (...` |
| `SQL15563862` | MQ-设备-任务量-分月 | `select robotcode,time,count from ( select amr_code as robotcode,d_time,count(*) from ( select distinct task_chain_code,task_chain_type,amr_c...` |
| `SQL15162557` | MQ-设备任务-TOP10 | `select amr_code as robotcode,count(*) from ( select distinct task_chain_code,task_chain_type,amr_code from tbl_sub_task where amr_code is no...` |
| `SQL18391767` | EMQ-设备运行-分日 | `select COALESCE("运行",0) as "运行", COALESCE("充电",0) as "充电",COALESCE("空闲",0) as "空闲",COALESCE("异常",0) as "异常",COALESCE("离线",0) as "异常",time ,r...` |
| `SQL15535661` | MQ-设备-任务量-分日 | `select robotcode,time,count from ( select amr_code as robotcode,d_time,count(*) from ( select distinct task_chain_code,task_chain_type,amr_c...` |
| `SQL15121556` | MQ-设备任务统计 | `select amr_code as robotcode,count(*) from ( select distinct task_chain_code,task_chain_type,amr_code from tbl_sub_task where amr_code is no...` |
| `SQL15402059` | MQ-设备类型-下拉 | `select amr_code as robotcode,count(*) from ( select distinct task_chain_code,task_chain_type,amr_code from tbl_sub_task where amr_code is no...` |
| `SQL15501460` | MQ-设备-任务量-分时 | `select robotcode,time,count from ( select amr_code as robotcode,d_time,count(*) from ( select distinct task_chain_code,task_chain_type,amr_c...` |
| `SQL21544742` | EMQ-AMR状态(地图) | `select mapcode,sum("运行"+"充电"+"空闲"+"异常"+"离线") as "设备总数",sum("运行") as "运行",sum("充电") as "充电" ,sum("空闲") as "空闲",sum("异常") as "异常",sum("离线") as...` |
| `SQL1819468` | 当日-设备分布情况 | `select map_code,count(1),avg(baterry2) as baterry from (select * from (SELECT ROW_NUMBER() OVER (partition BY map_code,amr_code ORDER BY tim...` |
| `SQL211659102` | MQ-内嵌-设备下拉 | `select amr_code as robotcode,count(*) from ( select distinct task_chain_code,task_chain_type,amr_code from tbl_sub_task where amr_code is no...` |
| `SQL10583751` | EMQ-开动率-地图-分月 | `select map_code as mapcode,rate,n.time from ( select map_code,case when "运行"=0 then 0 else "运行"/("运行"+"空闲"+"异常") end as rate,d_time from ( s...` |
| `SQL10544549` | EMQ-开动率-地图-分时 | `select map_code as mapcode,rate,n.time from ( select map_code,case when "运行"=0 then 0 else "运行"/("运行"+"空闲"+"异常") end as rate,d_time from ( s...` |
| `SQL10102343` | EMQ开动率-地图维度 | `select map_code as mapcode,case when "运行"=0 then 0 else "运行"/("运行"+"空闲"+"异常") end as rate from ( select map_code ,SUM (CASE WHEN status2='1'...` |
| `SQL10564050` | EMQ-开动率-地图-分日 | `select map_code as mapcode,rate,n.time from ( select map_code,case when "运行"=0 then 0 else "运行"/("运行"+"空闲"+"异常") end as rate,d_time from ( s...` |
| `SQL10415546` | EMQ-开动率-设备-分时 | `select amr_code as robotcode,rate,n.time from ( select amr_code,case when "运行"=0 then 0 else "运行"/("运行"+"空闲"+"异常") end as rate,d_time from (...` |
| `SQL10354697` | EMQ-在线时长-地图 | `select map_code,sum(times) as "在线" from emq_agv_view_001 where status2 in ('1','2','3','4') and [map_code in (${mapcodes})] and [agg_time >=...` |
| `SQL1540405` | RCS-开动率-设备-分月 | `select robotcode as robotcode,rate,n.time from ( select robotcode,case when "运行"=0 then 0 else "运行"/("运行"+"空闲"+"异常") end as rate,d_time from...` |
| `SQL21252231` | 设备看板-7日地图开动率趋势TOP | `select map_code,s.time,case when sum("运行"+"空闲"+"异常")=0 then 0 else sum("运行")/sum("运行"+"空闲"+"异常") end as rate from ( select map_code ,SUM (CA...` |
| `SQL1530341` | 设备看板-当日设备在线统计 | `select map_code,sum(times) as online from emq_agv_view_001 where status2 in ('1','2','3','4') and [map_code in (${mapcodes})] and agg_time>=...` |
| `SQL10472147` | EMQ-开动率-设备-分日 | `select amr_code as robotcode,rate,n.time from ( select amr_code,case when "运行"=0 then 0 else "运行"/("运行"+"空闲"+"异常") end as rate,d_time from (...` |
| `SQL09371021` | AMR_STATUS_DPS | `SELECT * FROM (SELECT ROW_NUMBER() OVER (partition BY mapcode,robotcode,timestamp ORDER BY timestamp desc)rowId,status2, mapcode, robotcode,...` |
| `SQL1403592` | RCS开动率-地图维度 | `select mapcode as mapcode,case when "运行"=0 then 0 else "运行"/("运行"+"空闲"+"异常") end as rate from ( select mapcode ,SUM (CASE WHEN status2='1' t...` |
| `SQL1401221` | RCS开动率-设备维度 | `select robotcode as robotcode,case when "运行"=0 then 0 else "运行"/("运行"+"空闲"+"异常") end as rate from ( select robotcode ,SUM (CASE WHEN status2...` |
| `SQL1430253` | RCS-开动率-设备-分时 | `select robotcode as robotcode,rate,n.time from ( select robotcode,case when "运行"=0 then 0 else "运行"/("运行"+"空闲"+"异常") end as rate,d_time from...` |
| `SQL1539224` | RCS-开动率-设备-分日 | `select robotcode as robotcode,rate,n.time from ( select robotcode,"运行"/("运行"+"空闲"+"异常") as rate,d_time from ( select robotcode ,SUM (CASE WH...` |
| `SQL1548237` | RCS-开动率-地图-分日 | `select mapcode as mapcode,rate,n.time from ( select mapcode,"运行"/("运行"+"空闲"+"异常") as rate,d_time from ( select mapcode ,SUM (CASE WHEN statu...` |
| `SQL1549308` | RCS-开动率-地图-分月 | `select mapcode as mapcode,rate,n.time from ( select mapcode ,case when "运行"=0 then 0 else "运行"/("运行"+"空闲"+"异常") end as rate,d_time from ( se...` |
| `SQL10255922` | AMR_STATUS_COUNT | `select t.status2,count(1) from (SELECT * FROM (SELECT ROW_NUMBER() OVER (partition BY mapcode,robotcode,timestamp ORDER BY timestamp desc)ro...` |
| `SQL1546396` | RCS-开动率-地图-分时 | `select mapcode as mapcode,rate,n.time from ( select mapcode,case when "运行"=0 then 0 else "运行"/("运行"+"空闲"+"异常") end as rate,d_time from ( sel...` |
| `SQL223836101` | EMQ-内嵌-设备下拉 | `select robotcode,sum("运行"+"充电"+"空闲"+"异常"+"离线") as "设备总数",sum("运行"+"充电"+"空闲"+"异常") as "在线",sum("运行") as "运行",sum("充电") as "充电" ,sum("空闲") as ...` |
| `SQL18365566` | EMQ-设备运行-分时 | `select COALESCE("运行",0) as "运行", COALESCE("充电",0) as "充电",COALESCE("空闲",0) as "空闲",COALESCE("异常",0) as "异常",COALESCE("离线",0) as "离线", COALES...` |
| `SQL10142344` | EMQ开动率-设备维度 | `select amr_code as robotcode,case when "运行"=0 then 0 else "运行"/("运行"+"空闲"+"异常") end as rate from ( select amr_code ,SUM (CASE WHEN status2='...` |
| `SQL101423442` | EMQ开动率-设备维度2 | `select amr_code as robotcode,case when "运行"=0 then 0 else "运行"/("运行"+"空闲"+"异常"+"充电") end as rate from ( select amr_code ,SUM (CASE WHEN stat...` |
| `SQL15562118` | 看板-实时设备数(多地图) | `select round(online_time / (extract (EPOCH FROM (end_time - start_time)))::numeric) as amr_count, map_code from ( select round(sum(times)/10...` |
| `SQL213609106` | RCS_AGV_地图下拉 | `select distinct mapcode from rcs_agv_view_001 where (([begin_date >=${startTime}] and [begin_date < ${endTime}]) or ([end_date >=${startTime...` |
| `SQL1818567` | 当日-设备运行情况 | `select sum("运行"+"充电"+"空闲"+"异常"+"离线") as "设备总数",sum("运行") as "运行",sum("充电") as "充电" ,sum("空闲") as "空闲",sum("异常") as "异常",sum("离线") as "离线" fr...` |
| `SQL15555517` | 看板-实时设备数(单地图) | `select sbtime, case when divide=0 then 0 else round(online_time / divide::numeric) end as amr_count from( select sbtime, online_time, case w...` |
| `SQL10481725` | 看板-在线时长趋势-日 | `select sum("运行"+"空闲"+"异常"+"充电") as online,d_time from ( select SUM (CASE WHEN status2='1' then times else 0 END) as "运行" ,SUM (CASE WHEN sta...` |
| `SQL21072840` | EMQ-AMR-地图下拉 | `select map_code as mapcode,case when "运行"=0 then 0 else "运行"/("运行"+"空闲"+"异常") end as rate from ( select map_code ,SUM (CASE WHEN status2='1'...` |
| `SQL09091542` | 设备-实时状态 | `SELECT * FROM (SELECT ROW_NUMBER() OVER (partition BY map_code,amr_code ORDER BY "timestamp" desc)rowId,status2 as status, map_code, amr_cod...` |
| `SQL09122443` | 设备-运行时长 | `select amr_code as robot_code,map_code ,SUM (CASE WHEN status2='1' then times else 0 END) as "运行" ,SUM (CASE WHEN status2='2' then times els...` |
| `SQL102023120` | 在线时长-设备 | `select sum(times) as online,amr_code from emq_agv_view_001 where status2 in ('1','2','3','4') and 1=1 and [map_code in (${mapcodes})] and 1=...` |
| `SQL112155104` | 开动率-地图-趋势 | `select map_code,case when sum("运行"+"充电")=0 then 0 else sum("运行"+"充电")/sum("运行"+"充电"+"空闲"+"异常") end as rate,d_time from ( select map_code ,SU...` |
| `SQL171032109` | 开动率-设备 | `select amr_code as amr_code,case when "运行"+"充电"=0 then 0 else ("运行"+"充电")/("运行"+"充电"+"空闲"+"异常") end as rate from ( select amr_code ,SUM (CAS...` |
| `SQL171234110` | 开动率-设备-趋势 | `select amr_code,case when sum("运行"+"充电")=0 then 0 else sum("运行"+"充电")/sum("运行"+"充电"+"空闲"+"异常") end as rate,d_time from ( select amr_code ,SU...` |
| `SQL095121119` | 在线时长-地图 | `select sum(times) as online,map_code from emq_agv_view_001 where status2 in ('1','2','3','4') and 1=1 and [map_code in (${mapcodes})] and 1=...` |
| `SQL192549133` | EMQ-设备运行 | `select amr_code as robotcode,map_code as mapcode ,SUM (CASE WHEN status2='1' then times else 0 END) as "运行" ,SUM (CASE WHEN status2='2' then...` |
| `SQL104053121` | 在线时长-设备-趋势 | `select sum("运行"+"空闲"+"异常"+"充电") as online,d_time,amr_code from ( select SUM (CASE WHEN status2='1' then times else 0 END) as "运行" ,SUM (CASE...` |
| `SQL104237122` | 在线时长-地图-趋势 | `select sum("运行"+"空闲"+"异常"+"充电") as online,d_time,map_code from ( select SUM (CASE WHEN status2='1' then times else 0 END) as "运行" ,SUM (CASE...` |
| `SQL20374439` | EMQ-设备运行统计 | `select amr_code as robotcode,map_code as mapcode ,SUM (CASE WHEN status2='0' then times else 0 END) as "离线" ,SUM (CASE WHEN status2='1' then...` |
| `SQL142720105` | 开动率-地图 | `select map_code as mapcode,case when "运行"+"充电"=0 then 0 else ("运行"+"充电")/("运行"+"充电"+"空闲"+"异常") end as rate from ( select map_code ,SUM (CASE...` |
| `SQL17455123` | 看板-开动率趋势-日 | `select case when sum("运行"+"充电")=0 then 0 else sum("运行"+"充电")/sum("运行"+"充电"+"空闲"+"异常") end as rate,d_time from ( select SUM (CASE WHEN status...` |
| `SQL21054912` | 看板-任务状态统计 | `select max(case when status = '-1' then counts else null end) as status_allot, max(case when status = '2' then counts else null end) as stat...` |
| `SQL12340648` | RCS_AMR_MAP | `select mapcode ,SUM (CASE WHEN status2='1' then times else 0 END) as "运行" ,SUM (CASE WHEN status2='2' then times else 0 END) as "充电" ,SUM (C...` |
| `SQL15224749` | 5-任务统计-状态 | `select max(case when status = '-1' then counts else null end) as status_allot, max(case when status = '2' then counts else null end) as stat...` |
| `SQL104033118` | RCS_AMR_STATUS_地图下拉 | `select distinct mapcode from rcs_agv_view_001 where [agg_time>=${startTime}] and [agg_time< ${endTime}]` |
| `SQL10121164` | 下拉-设备运行-设备 | `select distinct robotcode\|\|'' as robotcode from rcs_agv_view_001 where [agg_time>=${startTime}] and [agg_time< ${endTime}] order by robotcod...` |
| `SQL142036108` | RCS_AGV_COUNT | `select t.status2,count(1) from (SELECT * FROM (SELECT ROW_NUMBER() OVER (partition BY mapcode,robotcode,timestamp ORDER BY timestamp desc)ro...` |
| `SQL1612323` | 任务看板-任务量-执行状态 | `select map_code,task_status,count(1) from ( select task_chain_code,task_chain_type,map_code,case when task_status='10' then '9' else task_st...` |
| `SQL14393374` | 趋势-地图运行-分日 | `select COALESCE("运行",0) as "运行", COALESCE("充电",0) as "充电",COALESCE("空闲",0) as "空闲",COALESCE("异常",0) as "异常",time,mapcode from ( select mapco...` |
| `SQL180533113` | TAS_SUB_TASK_AMR | `select t.amr_code as robotcode,range,count(*) from (select distinct task_chain_code,task_chain_type,range,amr_code from tas_sub_task where [...` |
| `SQL141546107` | RCS_AGV_STATUS | `select t.status2,count(1) from (SELECT * FROM (SELECT ROW_NUMBER() OVER (partition BY mapcode,robotcode,timestamp ORDER BY timestamp desc)ro...` |
| `SQL15033975` | 趋势-地图运行-分月 | `select COALESCE("运行",0) as "运行", COALESCE("充电",0) as "充电",COALESCE("空闲",0) as "空闲",COALESCE("异常",0) as "异常",time,mapcode from ( select mapco...` |
| `SQL10514662` | RCS_AGV_STATUS_ROBOT | `select robotcode,mapcode, status2 from (SELECT * FROM (SELECT ROW_NUMBER() OVER (partition BY mapcode,robotcode ORDER BY timestamp desc)rowI...` |
| `SQL21565924` | 开动率趋势1 | `select agg_time ,SUM (CASE WHEN status2='1' then times else 0 END) as "运行" ,SUM (CASE WHEN status2='2' then times else 0 END) as "充电" ,SUM (...` |
| `SQL2014154` | ON_TIME_DEVICE | `select mapcode,robotcode ,SUM (CASE WHEN status2 in ('1','2','3','4') then times else 0 END) as "在线" from rcs_agv_view_001 where [mapcode in...` |
| `SQL144759109` | RCS_AMR_TIME | `select robotcode ,SUM (CASE WHEN status2='1' then times else 0 END) as "运行" ,SUM (CASE WHEN status2='2' then times else 0 END) as "充电" ,SUM ...` |
| `SQL17082861` | 趋势-设备运行-分日 | `select COALESCE("运行",0) as "运行", COALESCE("充电",0) as "充电",COALESCE("空闲",0) as "空闲",COALESCE("异常",0) as "异常",time ,robotcode from ( select ro...` |
| `SQL13514666` | 下拉-任务量-设备 | `select distinct amr_code as robotcode from tas_sub_task where (task_status='9' or task_status='10') and amr_code is not null and [create_tim...` |
| `SQL17203824` | 任务量统计-设备top10 | `select amr_code as robotcode,count(*) from ( select distinct task_chain_code,task_chain_type,amr_code from tbl_sub_task where amr_code is no...` |
| `SQL13422849` | 趋势-地图运行-分时 | `select COALESCE("运行",0) as "运行", COALESCE("充电",0) as "充电",COALESCE("空闲",0) as "空闲",COALESCE("异常",0) as "异常",time,mapcode from ( select mapco...` |
| `SQL17482123` | 开动率指标 | `select robotcode ,SUM (CASE WHEN status2='1' then times else 0 END) as "运行" ,SUM (CASE WHEN status2='2' then times else 0 END) as "充电" ,SUM ...` |
| `SQL15151767` | 趋势-任务量-设备-分时 | `select robotcode,time,count from ( select amr_code as robotcode,d_time,count(*) from ( select distinct task_chain_code,task_chain_type,amr_c...` |
| `SQL15313668` | 趋势-任务量-设备-分日 | `select robotcode,time,count from ( select amr_code as robotcode,d_time,count(*) from ( select distinct task_chain_code,task_chain_type,amr_c...` |
| `SQL08570161` | RCS_AGV_STATUS_MAP | `select mapcode ,SUM (CASE WHEN status2='1' and date_part('second', now()-timestamp)<2 then 1 else 0 END) as "运行" ,SUM (CASE WHEN status2='2'...` |
| `SQL145212110` | RCS_AMR_RUN_RATE | `select COALESCE("运行",0) as "运行", COALESCE("充电",0) as "充电",COALESCE("空闲",0) as "空闲",COALESCE("异常",0) as "异常",time as agg_time ,robotcode from...` |
| `SQL09373165` | 趋势-任务量-设备-分月 | `select robotcode,time,count from ( select amr_code as robotcode,d_time,count(*) from ( select distinct task_chain_code,task_chain_type,amr_c...` |
| `SQL17151723` | 任务量统计-设备 | `select amr_code as robotcode,count(*) from ( select distinct task_chain_code,task_chain_type,amr_code from tbl_sub_task where amr_code is no...` |
| `SQL205006105` | RCS_AGV_UPDATA | `select robotcode,mapcode ,SUM (CASE WHEN status2='1' then times else 0 END) as "运行" ,SUM (CASE WHEN status2='2' then times else 0 END) as "充...` |
| `SQL17140663` | 趋势-设备运行-分月 | `select COALESCE("运行",0) as "运行", COALESCE("充电",0) as "充电",COALESCE("空闲",0) as "空闲",COALESCE("异常",0) as "异常",time ,robotcode from ( select ro...` |
| `SQL17124962` | 趋势-设备运行-分时 | `select COALESCE("运行",0) as "运行", COALESCE("充电",0) as "充电",COALESCE("空闲",0) as "空闲",COALESCE("异常",0) as "异常",time ,robotcode from ( select ro...` |
| `getTRPTaskChainCode` | 获取时段内TRP任务编号 | `select tt.task_chain_code from tbl_task tt left join ( select task_chain_code,task_chain_type,create_time,map_code,derive, row_number() over...` |
| `getTRPTaskCount` | 获取大小车任务统计 | `select count(*) as total_count, case when ${queryDateLength} = 7 then foo1.month_date when ${queryDateLength} = 10 then foo1.day_date else f...` |
| `getTRPTaskCountNF` | 获取大小车任务统计(待完成) | `select count(*) as total_count, case when ${queryDateLength} = 7 then foo1.month_date when ${queryDateLength} = 10 then foo1.day_date else f...` |
| `SQL20224495` | MQ任务量-地图 | `select map_code, count(*) from ( select task_chain_code,task_chain_type,map_code,case when task_status='10' then '9' else task_status end as...` |
| `SQL15081055` | MQ-地图任务统计 | `select map_code, count(*) from ( select distinct task_chain_code,task_chain_type,map_code from tbl_sub_task where map_code is not null and (...` |
| `SQL16420092` | MQ任务-类型-分时 | `select task_chain_type,count,s.time from ( select task_chain_type,d_time,count(*) as count from ( select distinct task_chain_code,task_chain...` |
| `SQL182130114` | TAS_SUB_TASK_MAP | `select t.map_code as mapcode,"range",count(*) from (select distinct task_chain_code,task_chain_type,map_code,range from tas_sub_task where [...` |
| `SQL16434293` | MQ任务-类型-分日 | `select task_chain_type,count,s.time from ( select task_chain_type,d_time,count(*) as count from ( select distinct task_chain_code,task_chain...` |
| `SQL16442594` | MQ任务-类型-分月 | `select task_chain_type,count,s.time from ( select task_chain_type,d_time,count(*) as count from ( select distinct task_chain_code,task_chain...` |
| `SQL14523853` | MQ-任务类型-下拉 | `select t.task_chain_type,count(*) from ( select distinct task_chain_code,task_chain_type from tbl_task where (task_status='9' or task_status...` |
| `SQL15230158` | MQ-任务类型统计 | `select t.task_chain_type,count(*) from ( select distinct task_chain_code,task_chain_type,"range" from tbl_task where (task_status='9' or tas...` |
| `SQL16042763` | MQ-地图-任务量-分月 | `select map_code,time,count from ( select map_code,d_time,count(*) from ( select distinct task_chain_code,task_chain_type,map_code,to_char(cr...` |
| `SQL1432318` | 任务看板-近7日地图任务量 | `select time,map_code,count from ( select map_code,d_time, count(*) from ( select task_chain_code,task_chain_type,map_code,to_char(create_tim...` |
| `SQL14500252` | MQ-任务单统计 | `select t1.task_chain_type,reply_time,exec_time,eft_time,carrier_lift_time,empty_run_time,count,reply_time/count as avg_reply_time,exec_time/...` |
| `SQL1436099` | 任务看板-近7日地图平均任务量 | `select map_code,sum(count) as sum from ( select time,map_code,count from ( select map_code,d_time, count(*) from ( select task_chain_code,ta...` |
| `SQL16093165` | MQ-地图-任务量-分时 | `select map_code,time,count from ( select map_code,d_time,count(*) from ( select distinct task_chain_code,task_chain_type,map_code,to_char(cr...` |
| `SQL16064064` | MQ-地图-任务量-分日 | `select map_code,time,count from ( select map_code,d_time,count(*) from ( select distinct task_chain_code,task_chain_type,map_code,to_char(cr...` |
| `SQL11402481` | 5-任务统计-任务量 | `select map_code, count(*) from ( SELECT ROW_NUMBER() OVER (partition BY ts.task_chain_code ORDER BY ts.update_time desc) rowId, ts.map_code,...` |
| `SQL16290884` | 5-任务统计-按月趋势 | `select map_code,timer.d_time,counts from ( select map_code,d_time, count(*) as counts from ( select map_code, to_char(create_time,'yyyy-mm')...` |
| `SQL16380991` | 任务量-趋势 | `select d_time, sum(counts) as count from ( (select d_time, count(*) as counts from ( select (CASE WHEN ${dTime1} = '1' THEN to_char(create_t...` |
| `SQL202952114` | 6-任务类型统计-作业比按月趋势 | `select work_scale, task_chain_type, timer.d_time from ( select round((sum(work_time)::numeric / sum(execute_time)::numeric) * 100, 2) as wor...` |
| `SQL202721112` | 6-任务类型统计-作业比按时趋势 | `select work_scale, task_chain_type, timer.d_time from ( select round((sum(work_time)::numeric / sum(execute_time)::numeric) *100, 2) as work...` |
| `SQL213507102` | 6-任务类型统计-任务量按日趋势 | `select timer.d_time, counts, task_chain_type from ( select count(1) as counts, task_chain_type, d_time from ( select row_number() over(parti...` |
| `SQL21050111` | 看板-任务数量趋势(单地图) | `select count(1) as counts, case when ${sbtype}=1 then to_char(create_time, 'yyyy-mm-dd hh24') --当日,按时间趋势 when ${sbtype}=2 then to_char(creat...` |
| `SQL11373715` | 看板-任务数量趋势(多地图) | `select count(1) as counts, map_code as mapcode from ( select row_number() over(partition by ts.task_chain_code order by ts.update_time desc ...` |
| `SQL16162082` | 5-任务统计-按时趋势 | `select map_code,timer.d_time,counts from ( select map_code,d_time, count(*) as counts from ( select map_code, to_char(create_time,'yyyy-mm-d...` |
| `SQL16284383` | 5-任务统计-按日趋势 | `select map_code,timer.d_time,counts from ( select map_code,d_time, count(*) as counts from ( SELECT ROW_NUMBER() OVER (partition BY ts.task_...` |
| `SQL210304100` | 6-任务类型统计-任务量 | `select count(1) as counts, task_chain_type from ( select row_number() over(partition by ts.task_chain_code order by ts.update_time desc null...` |
| `SQL213356101` | 6-任务类型统计-任务量按时趋势 | `select timer.d_time, counts, task_chain_type from ( select count(1) as counts, task_chain_type, d_time from ( select row_number() over(parti...` |
| `SQL145313106` | 6-任务类型统计-任务表格 | `select task_chain_type, count(1) as counts, round(sum(execute_time)::numeric/count(1), 2) as avg_execute_time, round(sum(produce_time)::nume...` |
| `SQL165801108` | 6-任务类型统计-时长按日趋势 | `select avg_time, task_chain_type, timer.d_time from ( select round(sum(times)::numeric/count(1), 2) as avg_time, task_chain_type, d_time fro...` |
| `SQL194831111` | 6-任务类型统计-时长按月趋势 | `select avg_time, task_chain_type, timer.d_time from ( select round(sum(times)::numeric/count(1), 2) as avg_time, task_chain_type, d_time fro...` |
| `SQL164825107` | 6-任务类型统计-时长按时趋势 | `select avg_time, task_chain_type, timer.d_time from ( select round(sum(times)::numeric/count(1), 2) as avg_time, task_chain_type, d_time fro...` |
| `SQL202845113` | 6-任务类型统计-作业比按日趋势 | `select work_scale, task_chain_type, timer.d_time from ( select round((sum(work_time)::numeric / sum(execute_time)::numeric) * 100, 2) as wor...` |
| `SQL213550103` | 6-任务类型统计-任务量按月趋势 | `select timer.d_time, counts, task_chain_type from ( select count(1) as counts, task_chain_type, d_time from ( select row_number() over(parti...` |
| `SQL15202628` | 看板-任务平均数据 | `select round((task_time::numeric/counts)/60::numeric, 1) as avg_task_time, round((exec_time/task_time)*100::numeric) as exec_scale, task_typ...` |
| `SQL1549091` | 6-任务类型统计-执行时间按时统计趋势 | `select avg_time, task_chain_type, timer.d_time from ( select round((sum(execute_time)::numeric)::numeric/count(1), 2) as avg_time, task_chai...` |
| `SQL1607342` | 6-任务类型统计-执行时间按日统计趋势 | `select avg_time, task_chain_type, timer.d_time from ( select round((sum(execute_time)::numeric)::numeric/count(1), 2) as avg_time, task_chai...` |
| `SQL1609233` | 6-任务类型统计-执行时间按月统计趋势 | `select avg_time, task_chain_type, timer.d_time from ( select round((sum(execute_time)::numeric)::numeric/count(1), 2) as avg_time, task_chai...` |
| `SQL12230243` | 任务单-类型下拉 | `select distinct task_chain_type from tbl_task where [create_time >=${startTime}] and [create_time < ${endTime}] and [range in (${ranges})] o...` |
| `SQL2043137` | 任务看板-地图(任务量TOP10) | `select map_code,count(*) from ( select task_chain_code,task_chain_type,map_code from ( SELECT ROW_NUMBER() OVER (partition BY task_chain_cod...` |
| `SQL2025316` | 任务看板-任务类型(任务量TOP10) | `select task_chain_type,count(*) from ( select task_chain_code,task_chain_type from ( SELECT ROW_NUMBER() OVER (partition BY task_chain_code,...` |
| `SQL1538132` | 任务看板-任务量-昨日 | `select map_code,count(*) from ( select task_chain_code,task_chain_type,map_code from (SELECT ROW_NUMBER() OVER (partition BY task_chain_code...` |
| `SQL1754475` | 任务看板-任务类型当日趋势 | `select time,task_chain_type,count from ( select task_chain_type,d_time, count(*) from ( select task_chain_code,task_chain_type,to_char(creat...` |
| `SQL1648474` | 任务看板-地图当日任务量趋势 | `select time,map_code,count from ( select map_code,d_time, count(*) from ( select task_chain_code,task_chain_type,map_code,to_char(create_tim...` |
| `SQL16484742` | 任务看板-地图当日任务量趋势2 | `select time,map_code,count from ( select map_code,d_time, count(*) from ( select task_chain_code,task_chain_type,map_code,to_char(create_tim...` |
| `SQL1429201` | 任务看板-任务量-今日 | `select map_code,count(*) from ( select task_chain_code,task_chain_type,map_code from (SELECT ROW_NUMBER() OVER (partition BY task_chain_code...` |
| `SQL163925112` | TAS_SUB_TASK_TYPE | `select t.task_chain_type,"range",to_char(create_time,'yyyy-mm-dd hh24:00:00') as "time",count(*) from ( select distinct task_chain_code,task...` |
| `SQL15480721` | TAS_TASK_TYPE_COUNT | `select t.task_chain_type,"range",count(*) from ( select distinct task_chain_code,task_chain_type,"range" from tas_sub_task where [map_code i...` |
| `SQL192915116` | TAS_地图下拉 | `select distinct map_code from tbl_sub_task where [begin_date >=${startTime}] and [begin_date < ${endTime}] order by map_code asc` |
| `SQL163851111` | TAS_SUB_TASK_TIME | `select t1.task_chain_type,t1.range,t1.count,reply_time,reply_time/count as avg_reply_time ,carrier_lift_time,carrier_lift_time/count as avg_...` |
| `SQL17111122` | 任务量统计-地图 | `select map_code, count(*) from ( select distinct task_chain_code,task_chain_type,map_code from tbl_sub_task where map_code is not null and [...` |
| `SQL192230115` | TAS_任务类型下拉 | `select distinct task_chain_type from tbl_sub_task where [begin_date >=${startTime}] and [begin_date < ${endTime}] order by task_chain_type a...` |
| `SQL19531972` | 趋势-任务量-地图-分日 | `select map_code,time,count from ( select map_code,d_time, count(*) from ( select task_chain_code,task_chain_type,map_code,to_char(create_tim...` |
| `SQL15532469` | 趋势-任务量-地图-分月 | `select map_code,time,count from ( select map_code,d_time, count(*) from ( select task_chain_code,task_chain_type,map_code,to_char(create_tim...` |
| `SQL12062442` | 任务单统计-SQL | `select t1.task_chain_type as task_chain_type,reply_time,exec_time,eft_time,carrier_lift_time,empty_run_time,count,reply_time/count as avg_re...` |
| `SQL18200670` | 趋势-任务量-地图-分时 | `select time,map_code,count from ( select map_code,d_time, count(*) from ( select task_chain_code,task_chain_type,map_code,to_char(create_tim...` |
| `SQL15441316` | 看板-MTBF-在线时长 | `select sum(times) as online from emq_agv_view_001 where status2 in ('1','2','3','4') and [map_code in (${mapcodes})] and agg_time >=current_...` |
| `SQL112609120` | 设备故障对应在线时长统计 | `select mapcode,robotcode ,SUM (CASE WHEN status2 in ('1','2','3','4') then times else 0 END) as "在线" from rcs_agv_view_001 where [map_id in ...` |
| `SQL16583493` | 3-充电统计-充电桩按日趋势 | `select charge_code, timer.d_time, "scale" from ( select concat(coo_x, '-', coo_y, '-', map_code) as charge_code, d_time, 100 - round((sum(ch...` |
| `SQL16154531` | 看板-充电数据 | `select b.amr_code, b.map_code, b.battery, c.success, case when c."scale" is null then '未充电' else c."scale" end as "scale" from ( select roun...` |
| `SQL202406141` | 2-设备详情-充电数据-按时 | `select counts,timer.d_time, "scale" from ( select count(1)as counts,d_time, round((sum(chargesuccess)*100)/count(1)::numeric) as "scale" fro...` |
| `SQL15230390` | 3-充电统计-设备充电数据 | `select --case when charge.amr_code is null then task.amr_code --else charge.amr_code end as amr_code, amr_code, counts, charge_time, avg_cha...` |
| `SQL14184787` | 3-充电统计-设备按时趋势 | `select amr_code, timer.d_time, "scale" from ( select amr_code, d_time, 100 - round((sum(chargesuccess)*100)/count(1)::numeric) as "scale" fr...` |
| `SQL17260495` | 3-充电统计-耗电量按时趋势 | `select amr_code, timer.d_time, battery from ( select amr_code, to_char(task_start_time,'yyyy-mm-dd hh24') as d_time, sum(cast(start_battery ...` |
| `SQL14234789` | 3-充电统计-设备按月趋势 | `select amr_code, timer.d_time, "scale" from ( select amr_code, d_time, 100 - round((sum(chargesuccess)*100)/count(1)::numeric) as "scale" fr...` |
| `SQL14214288` | 3-充电统计-设备按日趋势 | `select amr_code, timer.d_time, "scale" from ( select amr_code, d_time, 100 - round((sum(chargesuccess)*100)/count(1)::numeric) as "scale" fr...` |
| `SQL17275396` | 3-充电统计-耗电量按日趋势 | `select amr_code, timer.d_time, battery from ( select amr_code, case when substring(${starttime}, 12, 2)::numeric <= substring(${endtime}, 12...` |
| `SQL17291497` | 3-充电统计-耗电量按月趋势 | `select amr_code, timer.d_time, battery from ( select amr_code, to_char(task_start_time,'yyyy-mm') as d_time, sum(cast(start_battery as numer...` |
| `SQL154524124` | 2-设备详情-充电次数按日趋势 | `select amr_code, success_scale, counts, timer.d_time from ( select count(1) as counts, d_time, amr_code, round(sum(success)::numeric/count(1...` |
| `SQL213308142` | 2-设备详情-充电数据-按日 | `select counts, timer.d_time, "scale" from ( select count(1)as counts, d_time, round((sum(chargesuccess)*100)/count(1)::numeric) as "scale" f...` |
| `SQL16564692` | 3-充电统计-充电桩按时趋势 | `select charge_code, timer.d_time, "scale" from ( select concat(coo_x, '-', coo_y, '-', map_code) as charge_code, d_time, 100 - round((sum(ch...` |
| `SQL17021994` | 3-充电统计-充电桩按月趋势 | `select charge_code, timer.d_time, "scale" from ( select concat(coo_x, '-', coo_y, '-', map_code) as charge_code, d_time, 100 - round((sum(ch...` |
| `SQL213054161` | 1-设备状态-充电桩利用率 | `select round((charge_time * 100)::numeric / (extract (EPOCH FROM (end_time - start_time))*${chargercount})::numeric, 2) as charge_use, charg...` |
| `SQL214606143` | 2-设备详情-充电数据-按月 | `select counts, timer.d_time, "scale" from ( select count(1)as counts, d_time, round((sum(chargesuccess)*100)/count(1)::numeric) as "scale" f...` |
| `SQL195308126` | 1-设备状态-充电数据 | `select count(1) as counts, amr_code, round(sum(success)::numeric/count(1), 2) * 100 as success_scale from ( select amr_code, case when extra...` |
| `SQL154803125` | 2-设备详情-充电次数按月趋势 | `select amr_code, success_scale, counts, timer.d_time from ( select count(1) as counts, d_time, amr_code, round(sum(success)::numeric/count(1...` |
| `SQL154355123` | 2-设备详情-充电次数按时趋势 | `select amr_code, success_scale, counts, timer.d_time from ( select count(1) as counts, d_time, amr_code, round(sum(success)::numeric/count(1...` |
| `SQL19391798` | 3-充电统计-充电桩数据 | `select * from ( select concat(coo_x, '-', coo_y, '-', map_code) as charge_code, count(1) as counts, round(sum(extract (EPOCH FROM (charge_fi...` |
| `sqlQueryLifts` | 获取电梯列表 | `select distinct lift_code, lift_name from dps_sync_lift` |
| `SQL15005554` | MQ-地图下拉 | `select map_code, count(*) from ( select distinct task_chain_code,task_chain_type,map_code from tbl_sub_task where map_code is not null and (...` |
| `SQL15170041` | 储位热力图 | `select coox, cooy, sum(counts) as counts from ( select start_x as coox, start_y as cooy, count(1) as counts from tbl_sub_task where start_x ...` |
| `SQL14164048` | 轨迹热力图 | `select coox, cooy, sum(counts) as counts, sum(stay_times) as times from ( select pos_x as coox, pos_y as cooy, case when ${timeslimit} <> 0 ...` |
| `SQL2013293` | ON_TIME_MAP | `select mapcode ,SUM (CASE WHEN status2 in ('1','2','3','4') then times else 0 END) as "在线" from rcs_agv_view_001 where [mapcode in (${mapcod...` |
| `getTimeSlots` | 获取划分时间段 | `select generate_series(0, 23, 1)` |
| `SQL1848179` | 计算当前班次 | `select id,name,date(now())+range_time_start as range_start,date(now())+range_time_end as range_end from dps_work_range where localtime betwe...` |
| `SQL11170614` | 计算上个同班次 | `select id,date(now())+range_time_start -interval'24h'as range_start,date(now())+range_time_end-interval'24h' as range_end from dps_work_rang...` |
| `SQL18502919` | 查询班次(带跨天判断) | `select id,range_time_start,range_time_end, case when range_time_start>range_time_end then '>' else '<' end as cmp from ( select id,range_tim...` |
| `SQL21280647` | 看板-获取时间查询范围 | `select * from ( select case when range_time_start < range_time_end then case when ${type}='day' then to_char(current_date + range_time_start...` |
| `SQL19521699` | 计算班次-根据当前时间自动联动日期 | `select id,name,range_start,range_end,range_time_start,range_time_end, case when range_time_start>range_time_end then '>' else '<' end as cmp...` |
| `SQL10280613` | 开动率-当前班次 | `select case when ("运行"+"充电")=0 then 0 else ("运行"+"充电")/("运行"+"充电"+"空闲"+"异常") end as rate from ( select SUM (CASE WHEN status2='1' then times...` |
| `SQL180551181` | 获取当日生产计划 | `select range_type_id from dps_work_plan where work_date = current_date` |
| `getWorkbenchWaitTimes` | 获取拣选场景等待时间总览 | `select site_name, round(avg(man_await_times)::numeric / 60, 2) as avg_man_times, round(avg(amr_await_times)::numeric / 60, 2) as avg_amr_tim...` |
| `getManAwaitDetail` | 人等车详情-db | `select site_name , concat(coo_x, ',', coo_y) as site_coor, concat(site_name, ',', coo_x, ',', coo_y) as site_info, map_code , delivery_task ...` |
| `getAmrAwaitDetail` | 车等人详情-db | `select site_name , concat(coo_x, ',', coo_y) as site_coor, concat(site_name, ',', coo_x, ',', coo_y) as site_info, map_code , delivery_task ...` |
| `getCTUFullLoadRate` | 获取CTU满载率 | `select t1.map_name, t1.amr_code, t1.layer, t1.loadtime, ROUND(t1.loadtime::numeric / (foo3.total_online_time ::numeric/1000 * t1.layer), 2) ...` |
| `getTRPDetail` | 获取大小车出入库详情 | `select coalesce(t1.map_code,t2.map_code,t3.map_code) as map_code, coalesce(t1.amr_type_name,t2.amr_type_name,t3.amr_type_name) as amr_type_n...` |
| `getCTUAmrCode` | 获取CTU车号-下拉 | `select da.amr_code,da.amr_name from dps_sync_amr da,dps_sync_amr_type dat where da.type_code = dat.amr_type_code and dat.amr_category = '40'` |
| `getCTUAmrCodeByType` | 获取CTU车号(车型) | `select da.amr_code from dps_sync_amr_type dat, dps_sync_amr da where dat.amr_type_code = da.type_code and dat.amr_category = '40' and dat.am...` |
| `getCTUAmrType` | 获取CTU车型-下拉 | `select amr_type_name from dps_sync_amr_type where amr_category='40'` |
| `SQL103550144` | 测试 | `SELECT to_char(generate_series(to_date(${starttime},'yyyy-mm'), to_date(${endtime},'yyyy-mm'), '1month'),'yyyy-mm') as d_time` |

</details>

### 3.4 CMS_DB

- **serverId**: `JDBC20223541`
- **连接**: `postgres-0-stolon-async.middleware:5432` · endpoint=`cms_web` · jdbc/postgresql

| sourceId | 名称 | 分类 | 入参 | 出参 |
|----------|------|------|------|------|
| `getBinStatusCounts` | 大小车仓位状态 | 设备状态/开动率 | `mapCode`:String, `channelCode`:String | `task_in_c`:Integer, `disabled_c`:Integer, `is_empty_n`:Integer, `task_empty_n`:Integer, `wait_out_c`:Integer, `map_name`:String, `is_full_n`:Integer, `task_full_n`:Integer, `channel_code`:String, `is_full_c`:Integer, `map_code`:String, `all_count_c`:Integer, `wait_in_c`:Integer, `task_out_c`:Integer, `is_empty_c`:Integer, `name` |
| `20250523160918482` | 设备列表 | 设备状态/开动率 | `mapCode`:String | `amrcode`(AMR编号):String |
| `SQL1059321` | TAS-设备列表 | 设备状态/开动率 | — | `robot_code`:String |
| `SQL15565830` | 获取任务类型 | 任务统计 | — | `type_name`:String, `type_code`:String |
| `SQL20402243` | 任务数量统计 | 任务统计 | `mapcodes`:String, `startTime`:String, `endTime`:String | `task_chain_type`:String, `count`:Integer |
| `SQL20355442` | 任务各时间统计 | 任务统计 | `mapcodes`:String, `startTime`:String, `endTime`:String | `reply_time`:String, `empty_run_time`:String, `task_chain_type`:String, `exec_time`:String, `carrier_lift_time`:String |
| `getAmrAlarmDetailBatch` | 获取设备告警明细(批量) | 告警/故障 | `startTime`:String, `endTime`:String, `rssId`:String, `amrCode`:String | `source_code`, `main_type_code`, `minor_type_code`, `begin_time`, `end_time`, `param1`, `param2`, `times` |
| `SQL170031105` | 设备看板-MTBF-7日TOP5 | 告警/故障 | — | `map_code`:String, `mtbf`:Double |
| `getAmrAlarmDetail` | 获取设备告警明细 | 告警/故障 | `startTime`:String, `endTime`:String, `rssId`:String, `amrCode`:String | `source_code`, `main_type_code`, `minor_type_code`, `begin_time`, `end_time`, `param1`, `param2`, `times` |
| `getAmrFaultDetail` | 获取设备故障明细 | 告警/故障 | `range1`:String, `range2`:String, `mapCode`:String, `amrCode`:String, `startTime`:String, `endTime`:String, `rangeCode`:String | `rss_id`, `map_code`, `amr_code`, `begin_time`, `end_time`, `times`, `map_name` |
| `getFaultTotal` | 获取故障数据汇总 | 告警/故障 | `startTime`:String, `endTime`:String, `rangeCode`:String, `range1`:String, `range2`:String, `mapCode`:String, `amrCode`:String | `counts`, `times` |
| `SQL13521283` | CMS设备告警-地图-分时 | 告警/故障 | `mapcodes`:String, `startTime`:String, `endTime`:String | 见 SQL / 接口返回 |
| `SQL15075123` | 告警看板-近7日地图告警 | 告警/故障 | `mapcodes`:String | `map_code`:String, `count`:Integer |
| `SQL10153572` | CMS设备告警-设备告警 | 告警/故障 | `mapcodes`:String, `startTime`:String, `endTime`:String, `robotcodes`:String | `fault_times`:Integer, `source_code`:String |
| `SQL10140371` | CMS设备告警-设备告警TOP10 | 告警/故障 | `mapcodes`:String, `startTime`:String, `endTime`:String | `fault_times`:Integer, `source_code`:String |
| `SQL17545489` | CMS告警-子类型-分时 | 告警/故障 | `mapcodes`:String, `startTime`:String, `endTime`:String, `param`:None | 见 SQL / 接口返回 |
| `SQL16012426` | 告警看板-近7日告警类型趋势 | 告警/故障 | `mapcodes`:String | `map_code`:String, `count`:Integer, `time`:String |
| `SQL16241541` | 告警看板-当日告警类型TOP5 | 告警/故障 | — | `count`:Integer, `alarm_sub_type`:String |
| `SQL10191073` | CMS设备告警-地图下拉 | 告警/故障 | `startTime`:String, `endTime`:String | `fault_times`:Integer, `mapcode`:String |
| `SQL13464921` | 告警看板-设备告警-当日设备TOP5 | 告警/故障 | — | `count`:Integer, `source_code`:String |
| `SQL22091133` | 设备看板-当日平均MTBF-TOP | 告警/故障 | — | `map_code`:String, `fault_times`:Integer |
| `SQL22053232` | 设备看板-当日平均MTTR-TOP | 告警/故障 | — | `map_code`:String, `mttr`:Double |
| `SQL17353927` | 告警看板-设备告警-类型TOP5 | 告警/故障 | — | `count`:Integer, `alarm_sub_type`:String |
| `SQL14140787` | CMS设备告警-设备-分日 | 告警/故障 | `mapcodes`:String, `startTime`:String, `endTime`:String, `robotcodes`:String | 见 SQL / 接口返回 |
| `SQL14063486` | CMS设备告警-地图-分月 | 告警/故障 | `mapcodes`:String, `startTime`:String, `endTime`:String | 见 SQL / 接口返回 |
| `SQL15040738` | 告警看板-告警子类型字典 | 告警/故障 | — | `name`:1, `key`:1 |
| `SQL14050885` | CMS设备告警-地图-分日 | 告警/故障 | `mapcodes`:String, `startTime`:String, `endTime`:String | 见 SQL / 接口返回 |
| `SQL13362281` | CMS设备告警-地图TOP10 | 告警/故障 | `mapcodes`:String, `startTime`:String, `endTime`:String | `map_code`:String, `fault_times`:Integer |
| `SQL181645106` | 设备看板-MTTR-7日TOP5 | 告警/故障 | `mapcodes`:String | `map_code`:String, `mttr`:Double |
| `SQL14151088` | CMS设备告警-设备-分月 | 告警/故障 | `mapcodes`:String, `startTime`:String, `endTime`:String, `robotcodes`:String | 见 SQL / 接口返回 |
| `SQL09502170` | CMS设备告警-地图告警 | 告警/故障 | `mapcodes`:String, `startTime`:String, `endTime`:String, `robotcodes`:String | `map_code`:String, `fault_times`:Integer |
| `SQL1453033` | 告警子类型 | 告警/故障 | `param`:None | `alarmtypename`:String, `alarmtypecode`:String |
| `SQL13492782` | CMS设备告警-设备下拉 | 告警/故障 | `mapcodes`:String, `startTime`:String, `endTime`:String, `robotcodes`:String | `fault_times`:Integer, `robotcode`:String |
| `SQL141541100` | AMS&EMQ-故障率-设备 | 告警/故障 | `mapcodes`:String, `startTime`:String, `endTime`:String | `fault_time`:Double, `fault_times`:Integer, `amr_code`:String |
| `SQL10510781` | 告警看板-昨日地图告警 | 告警/故障 | `mapcodes`:String | `map_code`:String, `count`:Integer |
| `SQL15462825` | 告警看板-今日地图告警 | 告警/故障 | `mapcodes`:String | `map_code`:String, `count`:Integer |
| `SQL095056104` | 设备告警-内嵌-设备下拉 | 告警/故障 | `mapcodes`:String, `startTime`:String, `endTime`:String, `robotcodes`:String | `fault_times`:Integer, `robotcode`:String |
| `SQL13572622` | 告警看板-告警类型TOP5 | 告警/故障 | — | `map_code`:String, `count`:Integer |
| `SQL23293961` | 告警数据-告警来源-下拉 | 告警/故障 | `mapcodes`:String, `startTime1`:String, `endTime1`:String, `startTime2`:String, `endTime2`:String, `sourceCodes`:None, `module`:String, `class`:String, `param`:String, `sort`:String | `source_code`:String |
| `SQL13523684` | CMS设备告警-设备-分时 | 告警/故障 | `mapcodes`:String, `startTime`:String, `endTime`:String, `robotcodes`:String | 见 SQL / 接口返回 |
| `SQL14170121` | 告警看板-设备告警-季度TOP5 | 告警/故障 | — | `count`:Integer, `source_code`:String |
| `SQL10314091` | CMS告警-子类型-分月 | 告警/故障 | `mapcodes`:String, `startTime`:String, `endTime`:String, `param`:None | 见 SQL / 接口返回 |
| `SQL10301590` | CMS告警-子类型-分日 | 告警/故障 | `mapcodes`:String, `startTime`:String, `endTime`:String, `param`:None | 见 SQL / 接口返回 |
| `SQL09403934` | 设备看板-MTBF趋势 | 告警/故障 | `mapcodes`:String | `map_code`:String, `mtbf`:Double, `time`:String |
| `SQL1431022` | 告警主类型 | 告警/故障 | — | `alarmtypename`:String, `alarmtypecode`:String |
| `SQL14252827` | 看板-告警-设备TOP20 | 告警/故障 | `mapcodes`:String, `pmCase`:String, `time_start`:String, `time_end`:String, `rangeCase`:String, `range_start`:String, `range_end`:String | `count`, `source_code` |
| `SQL17435837` | 告警看板-3季设备告警趋势 | 告警/故障 | `sourceCodes`:String | `count`:Integer, `time`:String, `source_code`:String |
| `SQL10033235` | 设备看板-MTTR趋势 | 告警/故障 | `mapcodes`:String | `map_code`:String, `mttr`:Double, `time`:String |
| `SQL17194043` | 告警看板-近7日告警TOP5趋势 | 告警/故障 | `mapcodes`:String, `alarmSubTypes`:String | `count`:Integer, `alarm_sub_type`:String, `time`:String |
| `SQL17020142` | 告警看板-近7日告警类型TOP5 | 告警/故障 | — | `count`:Integer, `alarm_sub_type`:String |
| `SQL1529176` | 告警热力图查询 | 告警/故障 | `mapcode`:String, `maintypeparam`:None, `subtypeparam`:None, `timeCase`:String, `startRange`:String, `endRange`:String, `sqlCase`:String, `starttime`:String, `endtime`:String | `counts`, `cooy`, `coox`, `type` |
| `SQL090057128` | 告警次数-设备 | 告警/故障 | `mapcodes`:String, `robotcodes`:String, `alarmTypes`:String, `mainAlarmTypes`:String, `paramCase`:String, `_startTime`:String, `_endTime`:String, `ktCase`:String, `range_start`:String, `range_end`:String | `fault_times`, `amr_code` |
| `SQL091004130` | 告警次数-设备-趋势 | 告警/故障 | `dTime1`:String, `faultClasses`:String, `mapcodes`:String, `paramCase`:String, `_startTime`:String, `_endTime`:String, `ltSql1Case`:String, `range_start`:String, `ytSql1Case`:String, `range_end`:String, `alarmTypes`:String, `mainAlarmTypes`:String, `dTime2`:String, `alarmClasses`:String, `ltSql2Case`:String, `ytSql2Case`:String | 见 SQL / 接口返回 |
| `SQL15234529` | 看板-告警子类型字典 | 告警/故障 | — | `name`:String, `key`:String |
| `SQL09210045` | 设备-告警次数 | 告警/故障 | `mapcodes`:String, `robotcodes`:String, `rangeCase`:String, `range_start`:String, `range_end`:String, `dateCase`:String, `_startTime`:String, `_endTime`:String | `robot_code`, `map_code`, `count` |
| `SQL114415102` | 告警数据-地图下拉选项 | 告警/故障 | `startTime`:String, `endTime`:String | `map_code`:String |
| `SQL17101985` | 告警-类型-TOP10 | 告警/故障 | `mapcodes`:String, `robotcodes`:String, `pmCase`:String, `_startTime`:String, `_endTime`:String, `rangeCase`:String, `range_start`:String, `range_end`:String | `count`, `alarm_sub_type` |
| `SQL13551526` | 看板-告警-类型TOP20 | 告警/故障 | `mapcodes`:String, `pmCase`:String, `time_start`:String, `time_end`:String, `rangeCase`:String, `range_start`:String, `range_end`:String | `count`, `alarm_sub_type` |
| `SQL085843127` | 告警次数-地图 | 告警/故障 | `faultClasses`:String, `mapcodes`:String, `paramCase`:String, `_startTime`:String, `_endTime`:String, `ktCase`:String, `range_start`:String, `range_end`:String, `alarmTypes`:String, `robotcodes`:String, `mainAlarmTypes`:String | `map_code`, `fault_times` |
| `SQL12094725` | 设备故障次数 | 告警/故障 | `mapcodes`:String, `startTime`:String, `endTime`:String | `count`:Integer |
| `SQL090833129` | 告警次数-地图-趋势 | 告警/故障 | `dTime1`:String, `mapcodes`:String, `paramCase`:String, `_startTime`:String, `_endTime`:String, `ltSql1Case`:String, `range_start`:String, `ytSql1Case`:String, `range_end`:String, `alarmTypes`:String, `dTime2`:String, `alarmClasses`:String, `ltSql2Case`:String, `ytSql2Case`:String, `mainAlarmTypes`:String | 见 SQL / 接口返回 |
| `SQL114149132` | 告警类型-趋势-统计 | 告警/故障 | `dTime1`:String, `mapcodes`:String, `paramCase`:String, `_startTime`:String, `_endTime`:String, `ltSql1Case`:String, `range_start`:String, `ytSql1Case`:String, `range_end`:String, `alarmTypes`:String, `mainAlarmTypes`:String, `dTime2`:String, `ltSql2Case`:String, `ytSql2Case`:String | 见 SQL / 接口返回 |
| `SQL113715131` | 告警类型-统计 | 告警/故障 | `mapcodes`:String, `paramCase`:String, `_startTime`:String, `_endTime`:String, `ktCase`:String, `range_start`:String, `range_end`:String, `alarmTypes`:String, `mainAlarmTypes`:String | `count`, `alarm_sub_type` |
| `SQL09134344` | 设备-故障时长 | 告警/故障 | `mapcodes`:String, `robotcodes`:String, `rangeCase`:String, `range_start`:String, `range_end`:String, `dateCase`:String, `_startTime`:String, `_endTime`:String | `robot_code`, `fault_time`, `map_code`, `fault_times` |
| `SQL084613116` | 故障时长&次数-趋势-设备 | 告警/故障 | `dTime1`:String, `mapcodes`:String, `robotcodes`:String, `paramCase`:String, `_startTime`:String, `_endTime`:String, `ltSql1Case`:String, `range_start`:String, `ytSql1Case`:String, `range_end`:String, `dTime2`:String, `ltSql2Case`:String, `ytSql2Case`:String | 见 SQL / 接口返回 |
| `SQL08054124` | 看板-故障时长趋势-日 | 告警/故障 | `mapcodes`:String, `dTime1`:String, `dTime2`:String, `robotcodes`:String, `pmCase`:String, `_startTime`:String, `_endTime`:String, `rangeCase1`:String, `range_start`:String, `range_end`:String, `rangeCase2`:String | `fault_times`, `d_time` |
| `SQL0933224` | 设备告警-子类型字典 | 告警/故障 | `classes`, `param` | `name`:String, `key`:String |
| `SQL085630118` | 故障时长&次数-地图 | 告警/故障 | `mapcodes`:String, `robotcodes`:String, `paramCase`:String, `_startTime`:String, `_endTime`:String, `ktCase`:String, `range_start`:String, `range_end`:String | `fault_time`, `map_code`, `fault_times` |
| `SQL085503117` | 故障时长&次数-设备 | 告警/故障 | `mapcodes`:String, `robotcodes`:String, `paramCase`:String, `_startTime`:String, `_endTime`:String, `ktCase`:String, `range_start`:String, `range_end`:String | `fault_time`, `fault_times`, `amr_code` |
| `SQL22115421` | 看板-MTBF-故障次数 | 告警/故障 | `mapcodes`:String, `time_start`:String, `time_end`:String, `param0Case`:String, `range_start`:String, `range_end`:String, `ps0Case`:String, `range_hour`:String | `fault_time`, `fault_times` |
| `SQL0951585` | 设备告警-类型统计 | 告警/故障 | `mapcodes`:String, `param`:String, `alarmTypes`:String | `count`:Integer, `alarm_sub_type`:String |
| `SQL084431115` | 故障时长&次数-趋势-地图 | 告警/故障 | `dTime1`:String, `mapcodes`:String, `robotcodes`:String, `paramCase`:String, `_startTime`:String, `_endTime`:String, `ltSql1Case`:String, `range_start`:String, `ytSql1Case`:String, `range_end`:String, `dTime2`:String, `ltSql2Case`:String, `ytSql2Case`:String | 见 SQL / 接口返回 |
| `SQL1703282` | 设备告警主类型 | 告警/故障 | — | `name`:String, `key`:String |
| `SQL1706053` | 设备告警子类型 | 告警/故障 | `classes`:String, `param`:None | `name`:String, `key`:String |
| `SQL20055751` | 告警子类列表 | 告警/故障 | `parentCodes`:String, `typeCode`:String | `name`:String, `id`:String |
| `SQL11040225` | AMS_FAULT_DEVICE10 | 告警/故障 | `mapcodes`:String, `startTime`:String, `endTime`:String | `fault_time`:Double, `fault_times`:Integer, `amr_code`:String |
| `SQL17452511` | TAS-告警大类统计 | 告警/故障 | `mapcodes`:String, `startTime`:String, `endTime`:String, `param`:None | `main_type_code`:Integer, `count`:Integer, `alarm_module`:Integer |
| `SQL105856119` | 故障率地图下拉 | 告警/故障 | `startTime`, `endTime` | `mapcode`:String |
| `SQL1602142` | AMS_FAULT_DEVICE | 告警/故障 | `mapcodes`:String, `startTime`:String, `endTime`:String | `map_code`:String, `fault_time`:Double, `fault_times`:Integer, `amr_code`:String |
| `SQL1601231` | AMS_FAULT_MAP | 告警/故障 | `mapcodes`:String, `startTime`:String, `endTime`:String | `map_code`:String, `fault_time`:Double, `fault_times`:Integer |
| `SQL17465512` | TAS-告警子类统计 | 告警/故障 | `mapcodes`:String, `startTime`:String, `endTime`:String, `param`:None | `minor_type_code`:Integer, `main_type_code`:Integer, `count`:Integer, `alarm_module`:Integer |
| `SQL14445827` | 故障次数等相关统计总 | 告警/故障 | `mapcodes`:String, `startTime`:String, `endTime`:String | `fault_time`:String, `fault_times`:Integer, `?column?`:String |
| `SQL19580450` | 告警主类列表 | 告警/故障 | `module`:String, `class`:String | `name`:String, `key`:String |
| `SQL0935187` | TAS-告警子类型 | 告警/故障 | `alarm_module`:String, `main_type_code`:String, `minor_type_code`:String, `module`:String | `name`:String, `key`:String |
| `SQL13083026` | 故障率相关统计_TBL | 告警/故障 | `mapcodes`:String, `startTime`:String, `endTime`:String | `map_code`:String, `fault_time`:String, `fault_times`:Integer, `amr_code`:String |
| `SQL0926296` | TAS-告警主类型 | 告警/故障 | `alarm_module`:String, `main_type_code`:String, `module`:String | `name`:String, `key`:String |
| `SQL204913101` | 告警数据表 | 告警/故障 | `mapcodes`:String, `module`:String, `class`:String, `param`:None, `ps`:String, `sort`:None, `sourceCodes`:String, `startTime`:String, `endTime`:String, `alarmStatus`:String | `end_date`:Date, `alarm_guid`:String, `begin_date`:Date, `time_interval`:String, `content`:String, `update_time`:Date, `update_user`:String, `alarm_status`:String, `id`:String, `alarm_x`:Integer, `alarm_y`:Integer, `create_time`:Date, `alarm_classification`:Integer, `main_type_code`:Integer, `log_level`:Integer, `start_inform_flag`:String, `alarm_module`:Integer, `is_show`:Integer, `param1`:String, `param2`:String, `elc_map_code`:String, `end_inform_flag`:String, `minor_type_code`:Integer, `create_user`:String, `source_code`:String, `org_code`:String |
| `SQL1645249` | ALARM_TYPE_BIG | 告警/故障 | — | `name`:String, `key`:String |
| `SQL17004610` | ALARM_TYPE_SMALL | 告警/故障 | `param`:None, `classes`:String | `name`:String, `key`:String |
| `SQL21321086` | 3-充电统计-充电桩列表 | 充电/电量 | `mapcodes`:String | `code`:String |
| `SQL1949571` | 1-设备状态-获取充电桩个数 | 充电/电量 | `mapcodes`:String | `count`:Integer |
| `20251014113311927` | 获取通道列表 | 地图/站点/热力 | — | `code`:String, `name`:String |
| `20250424110809611` | 获取地图 | 地图/站点/热力 | — | `map_code`(地图编号):String, `map_name`(地图名称):String |
| `getBinInOutCount` | 获取仓位出入库空满数 | 地图/站点/热力 | `mapCode`:String | `is_full`:Integer, `task_empty`:Integer, `channel_code`:String, `task_full`:Integer, `is_empty`:Integer, `map_name` |
| `getAreaByMapCode` | 获取区域(地码) | 地图/站点/热力 | `mapCode`:String | `area_code`, `area_name`, `map_code` |
| `getAreaName` | 获取区域名称-下拉 | 地图/站点/热力 | — | `area_name`:String, `area_code`:String |
| `SQL1111381` | 地图列表 | 地图/站点/热力 | — | `mapname`:String, `mapcode`:String |
| `SQL19040310` | TAS地图列表 | 地图/站点/热力 | — | `map_code`:String, `map_name`:String |
| `SQL15492246` | 获取地图站点坐标 | 地图/站点/热力 | `mapcode`:String | `coo_y`:Double, `coo_x`:Double, `site_code`:String |
| `getSiteInfos` | 获取工作台列表 | 下拉/字典/列表 | `mapCode`:String | `site_name`(站点信息) |
| `20250617151022899` | 获取车类型 | 下拉/字典/列表 | `key`:None | `amrTypeCode`, `amrTypeName` |
| `20250618152553842` | 获取车型系列 | 下拉/字典/列表 | `mapCode`:String | `amr_category` |
| `getCacheBinInOutCount` | 获取缓存位出入库数量 | 下拉/字典/列表 | `mapCode`:String | `channel_code`, `map_name`, `is_empty`, `is_full`, `wait_out`, `wait_in`, `task_out`, `task_in`, `all_count`, `disabled_count` |
| `getLineByMapCode` | 获取输送线(地码) | 下拉/字典/列表 | `mapCode`:String | `eqp_code`, `eqp_name`, `map_code` |
| `getLineName` | 获取输送线名称-下拉 | 下拉/字典/列表 | — | `map_code`:String, `eqp_name`:String, `eqp_code`:String |

<details><summary>SQL / 接口内容摘要</summary>

| sourceId | 名称 | content |
|----------|------|---------|
| `getBinStatusCounts` | 大小车仓位状态 | `select f3.disabled_c + f3.is_empty_c + f3.is_full_c + f3.wait_out_c + f3.wait_in_c as all_count_c, f3.*, ce.map_name, cc."name" from ( selec...` |
| `20250523160918482` | 设备列表 | `select amr_code as amrcode from cms_amr where 1=1 and [map_code = ${mapCode}]` |
| `SQL1059321` | TAS-设备列表 | `select amr_code as robot_code from cms_amr` |
| `SQL15565830` | 获取任务类型 | `select code as type_code, type_name, 1 as biz from cms_biz_group_type union select key_ as type_code, case when s.field_value is null then t...` |
| `SQL20402243` | 任务数量统计 | `select t.task_chain_type,count(*) from (select distinct task_chain_code,task_chain_type from tbl_sub_task where [map_code in (${mapcodes})] ...` |
| `SQL20355442` | 任务各时间统计 | `select task_chain_type ,EXTRACT(EPOCH FROM sum(task_start_time-send_task_time))/3600 as reply_time ,EXTRACT(EPOCH FROM sum(end_time-create_t...` |
| `getAmrAlarmDetailBatch` | 获取设备告警明细(批量) | `select source_code, main_type_code, minor_type_code, param1, param2, alarm_x \|\| ',' \|\| alarm_y as coordinate, to_char(begin_date, 'yyyy-mm-d...` |
| `SQL170031105` | 设备看板-MTBF-7日TOP5 | `select map_code,trunc(extract(epoch FROM (online_time/fault_times))::numeric) as mtbf from( select map_code,count(1) as fault_times,current_...` |
| `getAmrAlarmDetail` | 获取设备告警明细 | `select source_code, main_type_code, minor_type_code, param1, param2, alarm_x \|\| ',' \|\| alarm_y as coordinate, to_char(begin_date, 'yyyy-mm-d...` |
| `getAmrFaultDetail` | 获取设备故障明细 | `select rss_id, ca.map_code, cm.map_name, amr_code, to_char(begin_date, 'yyyy-mm-dd hh24:mi:ss') as begin_time, to_char(end_date, 'yyyy-mm-dd...` |
| `getFaultTotal` | 获取故障数据汇总 | `select count(1) as counts, round(cast(sum(EXTRACT(EPOCH FROM end_date-begin_date))/60 as NUMERIC), 2) as times from cms_amr_alarm_statistic ...` |
| `SQL13521283` | CMS设备告警-地图-分时 | `select map_code, s.time,fault_times from ( select map_code,d_time,count(1) as fault_times from ( select elc_map_code as map_code,to_char(beg...` |
| `SQL15075123` | 告警看板-近7日地图告警 | `select map_code,count(*) from ( select alarm_module\|\|'-'\|\|main_type_code\|\|'-'\|\|minor_type_code as alarm_sub_type,elc_map_code as map_code ,t...` |
| `SQL10153572` | CMS设备告警-设备告警 | `select source_code,count(1) as fault_times from ( select source_code from cms_alarm_log where alarm_module=1 and elc_map_code is not null an...` |
| `SQL10140371` | CMS设备告警-设备告警TOP10 | `select source_code,count(1) as fault_times from ( select source_code from cms_alarm_log where alarm_module=1 and elc_map_code is not null an...` |
| `SQL17545489` | CMS告警-子类型-分时 | `select alarm_module\|\|'-'\|\|main_type_code\|\|'-'\|\|minor_type_code as alarm_sub_type, s.time,count from ( select alarm_module,main_type_code,min...` |
| `SQL16012426` | 告警看板-近7日告警类型趋势 | `select time,map_code,count from ( select map_code,d_time, count(*) from ( select alarm_module\|\|'-'\|\|main_type_code\|\|'-'\|\|minor_type_code as ...` |
| `SQL16241541` | 告警看板-当日告警类型TOP5 | `select alarm_sub_type,count(*) from ( select alarm_module\|\|'-'\|\|main_type_code\|\|'-'\|\|minor_type_code as alarm_sub_type,source_code from cms_...` |
| `SQL10191073` | CMS设备告警-地图下拉 | `select map_code as mapcode,count(1) as fault_times from ( select source_code,elc_map_code as map_code from cms_alarm_log where alarm_module=...` |
| `SQL13464921` | 告警看板-设备告警-当日设备TOP5 | `select source_code,count(*) from ( select alarm_module\|\|'-'\|\|main_type_code\|\|'-'\|\|minor_type_code as alarm_sub_type,source_code from cms_ala...` |
| `SQL22091133` | 设备看板-当日平均MTBF-TOP | `select map_code,count(1) as fault_times from ( select map_code from cms_amr_alarm_statistic where map_code is not null and map_code!='' and ...` |
| `SQL22053232` | 设备看板-当日平均MTTR-TOP | `select map_code,trunc(extract(epoch FROM (fault_time/fault_times/60))::numeric) as mttr from( select map_code,sum(ft_time) as fault_time,cou...` |
| `SQL17353927` | 告警看板-设备告警-类型TOP5 | `select alarm_sub_type,count(*) from ( select alarm_module\|\|'-'\|\|main_type_code\|\|'-'\|\|minor_type_code as alarm_sub_type,source_code from cms_...` |
| `SQL14140787` | CMS设备告警-设备-分日 | `select source_code as robotcode, s.time,fault_times from ( select source_code,d_time,count(1) as fault_times from ( select source_code,to_ch...` |
| `SQL14063486` | CMS设备告警-地图-分月 | `select map_code, s.time,fault_times from ( select map_code,d_time,count(1) as fault_times from ( select elc_map_code as map_code,to_char(beg...` |
| `SQL15040738` | 告警看板-告警子类型字典 | `select type_code\|\|'-'\|\|parent_code\|\|'-'\|\|alarm_type_code as key,t.field_value as name from ( select distinct type_code,parent_code,alarm_typ...` |
| `SQL14050885` | CMS设备告警-地图-分日 | `select map_code, s.time,fault_times from ( select map_code,d_time,count(1) as fault_times from ( select elc_map_code as map_code,to_char(beg...` |
| `SQL13362281` | CMS设备告警-地图TOP10 | `select map_code,count(1) as fault_times from ( select source_code,elc_map_code as map_code from cms_alarm_log where alarm_module=1 and elc_m...` |
| `SQL181645106` | 设备看板-MTTR-7日TOP5 | `select map_code,trunc(extract(epoch FROM (fault_time/fault_times))::numeric) as mttr from ( select map_code,sum(end_date-begin_date) as faul...` |
| `SQL14151088` | CMS设备告警-设备-分月 | `select source_code as robotcode, s.time,fault_times from ( select source_code,d_time,count(1) as fault_times from ( select source_code,to_ch...` |
| `SQL09502170` | CMS设备告警-地图告警 | `select map_code,count(1) as fault_times from ( select elc_map_code as map_code from cms_alarm_log where alarm_module=1 and elc_map_code is n...` |
| `SQL1453033` | 告警子类型 | `select concat(type_code, '-', parent_code, '-', alarm_type_code) as alarmTypeCode, case when gsl.field_value is null then cat.alarm_type_nam...` |
| `SQL13492782` | CMS设备告警-设备下拉 | `select source_code as robotcode,count(1) as fault_times from ( select source_code from cms_alarm_log where alarm_module=1 and elc_map_code i...` |
| `SQL141541100` | AMS&EMQ-故障率-设备 | `select amr_code,sum(ft_time) as fault_time,count(1) as fault_times from ( select amr_code,round(cast(EXTRACT(EPOCH FROM end_date-begin_date)...` |
| `SQL10510781` | 告警看板-昨日地图告警 | `select map_code, count(*) from ( select alarm_module\|\|'-'\|\|main_type_code\|\|'-'\|\|minor_type_code as alarm_sub_type,elc_map_code as map_code f...` |
| `SQL15462825` | 告警看板-今日地图告警 | `select map_code,count(*) from ( select alarm_module\|\|'-'\|\|main_type_code\|\|'-'\|\|minor_type_code as alarm_sub_type,elc_map_code as map_code ,t...` |
| `SQL095056104` | 设备告警-内嵌-设备下拉 | `select robotcode,count(1) as fault_times from ( select source_code as robotcode from cms_alarm_log where alarm_module=1 and elc_map_code is ...` |
| `SQL13572622` | 告警看板-告警类型TOP5 | `select elc_map_code as map_code,count(*) from ( select alarm_module\|\|'-'\|\|main_type_code\|\|'-'\|\|minor_type_code as alarm_sub_type,elc_map_cod...` |
| `SQL23293961` | 告警数据-告警来源-下拉 | `select distinct source_code from cms_alarm_log where [elc_map_code in (${mapcodes})] and [begin_date >=${startTime1}] and [begin_date < ${en...` |
| `SQL13523684` | CMS设备告警-设备-分时 | `select source_code as robotcode, s.time,fault_times from ( select source_code,d_time,count(1) as fault_times from ( select source_code,to_ch...` |
| `SQL14170121` | 告警看板-设备告警-季度TOP5 | `select source_code,count(*) from ( select alarm_module\|\|'-'\|\|main_type_code\|\|'-'\|\|minor_type_code as alarm_sub_type,source_code from cms_ala...` |
| `SQL10314091` | CMS告警-子类型-分月 | `select alarm_module\|\|'-'\|\|main_type_code\|\|'-'\|\|minor_type_code as alarm_sub_type, s.time,count from ( select alarm_module,main_type_code,min...` |
| `SQL10301590` | CMS告警-子类型-分日 | `select alarm_module\|\|'-'\|\|main_type_code\|\|'-'\|\|minor_type_code as alarm_sub_type, s.time,count from ( select alarm_module,main_type_code,min...` |
| `SQL09403934` | 设备看板-MTBF趋势 | `select time,map_code,count as fault_times from ( select map_code,d_time, sum(fault_times) as count from ( select map_code,count(1) as fault_...` |
| `SQL1431022` | 告警主类型 | `select concat(type_code, '-', alarm_type_code) as alarmTypeCode, case when gsl.field_value is null then cat.alarm_type_name else gsl.field_v...` |
| `SQL14252827` | 看板-告警-设备TOP20 | `select source_code,count(*) from ( select alarm_module\|\|'-'\|\|main_type_code\|\|'-'\|\|minor_type_code as alarm_sub_type,source_code from cms_ala...` |
| `SQL17435837` | 告警看板-3季设备告警趋势 | `select source_code,n.time,count from ( select source_code,week_day1,count(1) as count from ( select source_code,to_char(end_date-((extract (...` |
| `SQL10033235` | 设备看板-MTTR趋势 | `select time,map_code,mttr from ( select map_code,d_time, trunc(extract(epoch FROM (fault_time/fault_times))::numeric) as mttr from ( select ...` |
| `SQL17194043` | 告警看板-近7日告警TOP5趋势 | `select time,alarm_sub_type,count from ( select alarm_sub_type,d_time, count(*) from ( select alarm_module\|\|'-'\|\|main_type_code\|\|'-'\|\|minor_t...` |
| `SQL17020142` | 告警看板-近7日告警类型TOP5 | `select alarm_sub_type,count(*) from ( select alarm_module\|\|'-'\|\|main_type_code\|\|'-'\|\|minor_type_code as alarm_sub_type,source_code,end_date ...` |
| `SQL1529176` | 告警热力图查询 | `select coo_x as cooX, coo_y as cooY, 0 as counts, 'site' as type from cms_site where [map_code=${mapcode}] union all select case when alarm_...` |
| `SQL090057128` | 告警次数-设备 | `select source_code as amr_code,count(1) as fault_times from ( select source_code from cms_alarm_log where alarm_module=1 and elc_map_code is...` |
| `SQL091004130` | 告警次数-设备-趋势 | `select source_code as amr_code,d_time,sum(fault_times) as fault_times from ( select source_code,d_time,count(1) as fault_times from ( select...` |
| `SQL15234529` | 看板-告警子类型字典 | `select type_code\|\|'-'\|\|parent_code\|\|'-'\|\|alarm_type_code as key, name from ( select distinct type_code,parent_code,alarm_type_code,glory_sys...` |
| `SQL09210045` | 设备-告警次数 | `select source_code as robot_code,elc_map_code as map_code,count(*) from ( select alarm_module\|\|'-'\|\|main_type_code\|\|'-'\|\|minor_type_code as ...` |
| `SQL114415102` | 告警数据-地图下拉选项 | `select distinct elc_map_code as map_code from cms_alarm_log where elc_map_code is not null and TRIM(elc_map_code)<>'' and (([begin_date >=${...` |
| `SQL17101985` | 告警-类型-TOP10 | `select alarm_sub_type,count(*) from ( select alarm_module\|\|'-'\|\|main_type_code\|\|'-'\|\|minor_type_code as alarm_sub_type,source_code from cms_...` |
| `SQL13551526` | 看板-告警-类型TOP20 | `select alarm_sub_type,count(*) from ( select alarm_module\|\|'-'\|\|main_type_code\|\|'-'\|\|minor_type_code as alarm_sub_type,source_code from cms_...` |
| `SQL085843127` | 告警次数-地图 | `select map_code,count(1) as fault_times from ( select elc_map_code as map_code from cms_alarm_log where alarm_module=1 and elc_map_code is n...` |
| `SQL12094725` | 设备故障次数 | `select count(1) from cms_amr_alarm_statistic where [map_code in (${mapcodes})] and [begin_date >=${startTime}] and [end_date < ${endTime}]` |
| `SQL090833129` | 告警次数-地图-趋势 | `select map_code,d_time,sum(fault_times) as fault_times from ( select map_code,d_time,count(1) as fault_times from ( select elc_map_code as m...` |
| `SQL114149132` | 告警类型-趋势-统计 | `select alarm_module\|\|'-'\|\|main_type_code\|\|'-'\|\|minor_type_code as alarm_sub_type,d_time,sum(count) as count from ( select alarm_module,main_...` |
| `SQL113715131` | 告警类型-统计 | `select alarm_module\|\|'-'\|\|main_type_code\|\|'-'\|\|minor_type_code as alarm_sub_type,count(*) from cms_alarm_log where [elc_map_code in (${mapco...` |
| `SQL09134344` | 设备-故障时长 | `select sum(ft_time) as fault_time,count(1) as fault_times,amr_code as robot_code,map_code from ( select round(cast(EXTRACT(EPOCH FROM end_da...` |
| `SQL084613116` | 故障时长&次数-趋势-设备 | `select sum(fault_time) as fault_time,sum(fault_times) as fault_times,"d_time",amr_code from ( select sum(ft_time) as fault_time,count(1) as ...` |
| `SQL08054124` | 看板-故障时长趋势-日 | `select sum(fat_time) as fault_time,sum(fat_times) as fault_times,"d_time" from ( select sum(ft_time) as fat_time,count(1) as fat_times,"d_ti...` |
| `SQL0933224` | 设备告警-子类型字典 | `select type_code\|\|'-'\|\|parent_code\|\|'-'\|\|alarm_type_code as key, name from ( select distinct type_code,parent_code,alarm_type_code,glory_sys...` |
| `SQL085630118` | 故障时长&次数-地图 | `select sum(ft_time) as fault_time,count(1) as fault_times,map_code from ( select round(cast(EXTRACT(EPOCH FROM end_date-begin_date)/3600 as ...` |
| `SQL085503117` | 故障时长&次数-设备 | `select sum(ft_time) as fault_time,count(1) as fault_times,amr_code from ( select round(cast(EXTRACT(EPOCH FROM end_date-begin_date)/3600 as ...` |
| `SQL22115421` | 看板-MTBF-故障次数 | `select sum(ft_time) as fault_time,count(1) as fault_times from ( select round(cast(EXTRACT(EPOCH FROM end_date-begin_date)/3600 as NUMERIC),...` |
| `SQL0951585` | 设备告警-类型统计 | `select alarm_module\|\|'-'\|\|main_type_code\|\|'-'\|\|minor_type_code as alarm_sub_type,count(*) from cms_alarm_log where [elc_map_code in (${mapco...` |
| `SQL084431115` | 故障时长&次数-趋势-地图 | `select sum(s.fat_time) as fault_time,sum(s.fat_times) as fault_times,"d_time",map_code from ( select sum(ft_time) as fat_time,count(1) as fa...` |
| `SQL1703282` | 设备告警主类型 | `select type_code\|\|'-'\|\|alarm_type_code as key,field_value as name from ( select distinct type_code,alarm_type_code,glory_sys_lang.field_valu...` |
| `SQL1706053` | 设备告警子类型 | `select type_code\|\|'-'\|\|parent_code\|\|'-'\|\|alarm_type_code as key, name from ( select distinct type_code,parent_code,alarm_type_code,glory_sys...` |
| `SQL20055751` | 告警子类列表 | `select type_code\|\|'-'\|\|parent_code\|\|'-'\|\|alarm_type_code as id,glory_sys_lang.field_value as name from cms_alarm_type join glory_sys_lang on...` |
| `SQL11040225` | AMS_FAULT_DEVICE10 | `select amr_code,sum(ft_time) as fault_time,count(1) as fault_times from ( select amr_code,round(cast(EXTRACT(EPOCH FROM end_date-begin_date)...` |
| `SQL17452511` | TAS-告警大类统计 | `select alarm_module,main_type_code,count(*) from cms_alarm_log where [elc_map_code in (${mapcodes})] and [begin_date >=${startTime}] and [en...` |
| `SQL105856119` | 故障率地图下拉 | `select distinct map_code as mapcode from cms_amr_alarm_statistic where map_code is not null and map_code!='' and [end_date >=${startTime}] a...` |
| `SQL1602142` | AMS_FAULT_DEVICE | `select amr_code,map_code,count(1) as fault_times,sum(ft_time) as fault_time from ( select amr_code,map_code,round(cast(EXTRACT(EPOCH FROM en...` |
| `SQL1601231` | AMS_FAULT_MAP | `select map_code,count(1) as fault_times,sum(ft_time) as fault_time,count(1) as fault_times from ( select amr_code,map_code,round(cast(EXTRAC...` |
| `SQL17465512` | TAS-告警子类统计 | `select alarm_module,main_type_code,minor_type_code,count(*) from cms_alarm_log where [elc_map_code in (${mapcodes})] and [begin_date >=${sta...` |
| `SQL14445827` | 故障次数等相关统计总 | `select sum(ft_time) as fault_time,count(1) as fault_times ,[EXTRACT(EPOCH FROM (to_timestamp(${endTime},'yyyy-mm-dd hh24:MI:SS')-to_timestam...` |
| `SQL19580450` | 告警主类列表 | `select type_code\|\|'-'\|\|alarm_type_code as key,glory_sys_lang.field_value as name from cms_alarm_type join glory_sys_lang on cms_alarm_type.a...` |
| `SQL0935187` | TAS-告警子类型 | `select type_code\|\|'-'\|\|parent_code\|\|'-'\|\|alarm_type_code as key,name from ( select distinct type_code,parent_code,alarm_type_code,glory_sys_...` |
| `SQL13083026` | 故障率相关统计_TBL | `select amr_code,map_code,sum(ft_time) as fault_time,count(1) as fault_times from ( select amr_code,map_code,EXTRACT(EPOCH FROM end_date-begi...` |
| `SQL0926296` | TAS-告警主类型 | `select type_code\|\|'-'\|\|alarm_type_code as key,name from ( select distinct type_code,parent_code,alarm_type_code,glory_sys_lang.field_value a...` |
| `SQL204913101` | 告警数据表 | `select * from cms_alarm_log where [elc_map_code in (${mapcodes})] and [source_code in (${sourceCodes})] and [alarm_module=${module}] and [al...` |
| `SQL1645249` | ALARM_TYPE_BIG | `select type_code\|\|'-'\|\|alarm_type_code as key,field_value as name from ( select distinct type_code,alarm_type_code,glory_sys_lang.field_valu...` |
| `SQL17004610` | ALARM_TYPE_SMALL | `select type_code\|\|'-'\|\|parent_code\|\|'-'\|\|alarm_type_code as key, name from ( select distinct type_code,parent_code,alarm_type_code,glory_sys...` |
| `SQL21321086` | 3-充电统计-充电桩列表 | `select concat(coo_x, '-', coo_y, '-',map_code) as code from cms_site where site_type in ('11', '35') and [map_code in (${mapcodes})] order b...` |
| `SQL1949571` | 1-设备状态-获取充电桩个数 | `select count(1) from cms_site where site_type in ('11', '35') and [map_code in (${mapcodes})]` |
| `20251014113311927` | 获取通道列表 | `select code, "name" from cms_channel` |
| `20250424110809611` | 获取地图 | `select map_code, map_name from cms_elc_map order by map_code` |
| `getBinInOutCount` | 获取仓位出入库空满数 | `select f3.*, ce.map_name from ( select channel_code, map_code, max(case when status = 'task_empty' then counts else 0 end) as task_empty, --...` |
| `getAreaByMapCode` | 获取区域(地码) | `select area_code,area_name,cm.map_code from cms_elc_map cm, cms_area ca where cm.map_code = ca.map_code and ca.area_category = '1' and cm.ma...` |
| `getAreaName` | 获取区域名称-下拉 | `select area_code,area_name from cms_area where area_category = '1'` |
| `SQL1111381` | 地图列表 | `select map_code as mapCode, map_name as mapName from cms_elc_map order by mapCode` |
| `SQL19040310` | TAS地图列表 | `select map_code,map_name from cms_elc_map order by map_code` |
| `SQL15492246` | 获取地图站点坐标 | `select coo_x, coo_y, site_code from cms_site where [map_code = ${mapcode}]` |
| `getSiteInfos` | 获取工作台列表 | `select distinct site_name as site_name from cms_site where 1=1 and site_type = '10' and [map_code = ${mapCode}]` |
| `20250617151022899` | 获取车类型 | `select amr_type_code as amrTypeCode, CASE WHEN amr_type_name LIKE '[amrType.name.]%' THEN regexp_replace(amr_type_name, '^\[amrType\.name\.\...` |
| `20250618152553842` | 获取车型系列 | `select distinct ct.amr_category from cms_amr ca left join cms_amr_type ct on ca.type_code = ct.amr_type_code where 1=1 and [ca.map_code = ${...` |
| `getCacheBinInOutCount` | 获取缓存位出入库数量 | `select f3.disabled_count + f3.is_empty + f3.is_full + f3.wait_out + f3.wait_in as all_count, f3.*, ce.map_name from ( select channel_code, m...` |
| `getLineByMapCode` | 获取输送线(地码) | `select ci.eqp_code,ci.eqp_name,cm.map_code from cms_elc_map cm,cms_eqp_info ci where cm.map_code = ci.map_code and cm.map_code in (${mapCode...` |
| `getLineName` | 获取输送线名称-下拉 | `select eqp_code,eqp_name,map_code from cms_eqp_info where eqp_type in ('line','uline')` |

</details>

### 3.5 CMS接口服务

- **serverId**: `cmsRestApi`
- **连接**: `rcms.default:80` · endpoint=`` · http/http

| sourceId | 名称 | 分类 | 入参 | 出参 |
|----------|------|------|------|------|
| `getAmrTypeName` | 获取AMR车型名 | 设备状态/开动率 | — | `key`, `name` |
| `getAlarmTypeFromCms` | 获取告警类型 | 告警/故障 | `isParent`:String, `parentCode`:String, `typeCode`:String, `classification`:String | `name`, `key` |
| `getAmrTypes` | 获取车型列表 | 下拉/字典/列表 | — | `key`(AMR类型编号), `name`(AMR类型名称) |
| `getBizTypeFromCms` | 获取业务组 | 下拉/字典/列表 | — | `key`, `name` |

<details><summary>SQL / 接口内容摘要</summary>

| sourceId | 名称 | content |
|----------|------|---------|
| `getAmrTypeName` | 获取AMR车型名 | `/api/permit/dataMetaService/amrTypeName` |
| `getAlarmTypeFromCms` | 获取告警类型 | `/api/permit/dataMetaService/alarmTypes?isParent=${isParent}&parentCode=${parentCode}&typeCode=${typeCode}&classification=${classification}` |
| `getAmrTypes` | 获取车型列表 | `/api/permit/dataMetaService/amrTypeName` |
| `getBizTypeFromCms` | 获取业务组 | `/api/permit/dataMetaService/bizTypes` |

</details>

### 3.6 DATAMETA接口API

- **serverId**: `datametaAPI`
- **连接**: `datameta.default:80` · endpoint=`` · http/http

| sourceId | 名称 | 分类 | 入参 | 出参 |
|----------|------|------|------|------|
| `getTRPTaskTotal` | 获取大小车时段任务总量 | 任务统计 | — | 见 SQL / 接口返回 |
| `getTaskSankey` | 获取任务桑基数据 | 任务统计 | — | 见 SQL / 接口返回 |
| `getLiftTaskDetail` | 获取电梯任务明细 | 任务统计 | — | 见 SQL / 接口返回 |
| `getTaskDetail` | 获取任务明细 | 任务统计 | — | 见 SQL / 接口返回 |
| `getTaskTotal` | 获取时段任务总量 | 任务统计 | — | 见 SQL / 接口返回 |
| `getCTUHourlyLoadRate` | 获取CTU分时满载率 | 效率/等待 | — | 见 SQL / 接口返回 |

<details><summary>SQL / 接口内容摘要</summary>

| sourceId | 名称 | content |
|----------|------|---------|
| `getTRPTaskTotal` | 获取大小车时段任务总量 | `/datameta/api/statistics/trpTaskTotal` |
| `getTaskSankey` | 获取任务桑基数据 | `/datameta/api/statistics/taskSankey` |
| `getLiftTaskDetail` | 获取电梯任务明细 | `/datameta/api/statistics/liftTaskDetail` |
| `getTaskDetail` | 获取任务明细 | `/datameta/api/statistics/taskDetail` |
| `getTaskTotal` | 获取时段任务总量 | `/datameta/api/statistics/taskTotal` |
| `getCTUHourlyLoadRate` | 获取CTU分时满载率 | `/datameta/api/statistics/ctuHourlyLoadRate` |

</details>

### 3.7 TAS接口服务

- **serverId**: `tasRestApi`
- **连接**: `rtas.default:80` · endpoint=`` · http/http

| sourceId | 名称 | 分类 | 入参 | 出参 |
|----------|------|------|------|------|
| `getTaskTypes` | 获取任务流程 | 任务统计 | — | `key`(流程编号), `name`(流程名称) |
| `getTRPTaskType` | 获取大小车任务类型 | 任务统计 | — | `key`, `name` |
| `getTaskTypeFromTas` | 获取任务流程 | 任务统计 | — | `key`, `name` |

<details><summary>SQL / 接口内容摘要</summary>

| sourceId | 名称 | content |
|----------|------|---------|
| `getTaskTypes` | 获取任务流程 | `/api/datametaService/taskTypes` |
| `getTRPTaskType` | 获取大小车任务类型 | `api/datametaService/getTrpProcess` |
| `getTaskTypeFromTas` | 获取任务流程 | `/api/datametaService/taskTypes` |

</details>

---

## 4. 前端常用速查

### 4.1 当前统计看板已在用

| sourceId | 名称 | 所属服务 | 入参 | 出参 | 典型用途 |
|----------|------|----------|------|------|----------|
| `SQL1818567` | 当日-设备运行情况 | DATAMETA_DB | `mapcodes`,`robotcodes` | 设备总数/运行/充电/空闲/异常/离线 | card7 五态柱状 |
| `SQL1819468` | 当日-设备分布情况 | DATAMETA_DB | `mapcodes`,`robotcodes` | map_code, count, baterry | card6 设备分布 |
| `SQL19040310` | TAS地图列表 | CMS_DB | — | map_code, map_name | 脚本 mapMap |
| `SQL10265761` | 班次下拉SQL | DATABUS-DB | `id` | id,name,range… | 班次筛选 |
| `SQL21280647` | 看板-获取时间查询范围 | DATAMETA_DB | `type` 等 | 时间范围 | 班次时间窗 |
| `SQL15202628` | 看板-任务平均数据 | DATAMETA_DB | 时间/地图等 | avg_task_time… | 任务平均 |
| `SQL16154531` | 看板-充电数据 | DATAMETA_DB | `mapcodes` 等 | amr_code,map,battery,success | 充电列表 |

### 4.2 与「逐车状态」最相关（改造 `SQL_AMR_STATUS_ROWS` 可参考）

| sourceId | 名称 | 入参 | 出参 | 说明 |
|----------|------|------|------|------|
| `SQL09091542` | 设备-实时状态 | `mapcodes`,`robotcodes` | `robot_code`,`status`,`map_code`,`baterry`,`timestamp`… | **最接近** `{amr_code,status}` |
| `SQL21343641` | EMQ-AMR状态(设备&地图) | `mapcodes` | `mapcode`,`robotcode`,`status2` | 按车出状态码 |
| `SQL09371021` | AMR_STATUS_DPS | 地图/时间 | 明细字段 | 状态明细流 |
| `SQL10255922` | AMR_STATUS_COUNT | `mapcodes` | `status2`,`count` | 仅汇总 |

**建议**：在 DATAMETA_DB 基于 `SQL09091542` 裁剪为 `amr_code, status`（status 映射中文或保留 status2），
管理端保存后把生成的 sourceId 填进布局 `source`（替换 `SQL_AMR_STATUS_ROWS`）。

### 4.3 状态类查询参数传法示例

```js
// 筛选：#select0 地图（ALL→null），#select1 日期
let mapCls = this.$component('#select0')
let mapcodes = mapCls && mapCls.tmpValue && mapCls.tmpValue !== 'ALL' && mapCls.tmpValue !== 'all'
  ? mapCls.tmpValue : null
this.$model('mapcodes', mapcodes)
return { mapcodes }  // 作为 doQueryData / source 请求参数
```

---

## 5. 通用入参名对照

| 参数名 | 含义 | 常见取值 |
|--------|------|----------|
| `mapcodes` / `mapCode` / `mapcode` | 地图筛选 | `ALL`/`all`→null；多值逗号分隔 |
| `robotcodes` / `robotcode` | 设备筛选 | 车号，多值逗号分隔 |
| `startTime` / `endTime` | 时间范围 | `yyyy-mm-dd hh24:mi:ss` |
| `date` / `begin_date` | 日期 | 与 `#select1` 绑定 |
| `type` | 时间粒度 | day 等 |
| `taskChainType` / `taskType` | 任务类型 | 下拉选中值 |
| `range` / `workRange` | 班次/时段 | 班次 id |

---

## 6. 注意事项

1. **只通过 sourceId 调用**，前端不写连接串、不直连 PostgreSQL。
2. sourceId 大小写敏感，与管理端「数据源配置」一致。
3. SQL 里 `[...]` 为可选条件；参数不传则该条件不生效。
4. 导出不含密码；连接凭证只在服务端「服务配置」。
5. 本清单以导出时间点为准；变更后以管理端列表为准。
6. 出参字段名是前端读结果的依据（如 `res.data.data[0].robot_code`）。
