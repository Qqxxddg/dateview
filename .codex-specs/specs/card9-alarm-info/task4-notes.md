## 任务 4 实施记录（2026-09-30）

### 结论：零改动

`beforeSourceQuery_6` 返回 `fm4_1`，已覆盖数据契约 / `SQL14252827` 全部入参：

| 契约字段 | 返回 | 来源 |
|---------|------|------|
| mapcodes | ✓ | `#select0` 或全地图 `SQL19040310` |
| time_start / time_end | ✓ | `$model('starttime'/'endtime')` |
| pmCase | ✓ | 固定 1（时间窗生效） |
| rangeCase | ✓ | 0/1/2（班次跨天/当日） |
| range_start / range_end | ✓ | `$model('selrange')` + `SQL09312961` |

- 使用方：仅 card9 源 `20230625143018702`（`content.option.sources` 与 `pages[0].sources` 同源），无其它模块回归风险。
- 服务端若沿用 `SQL14252827` 入参名，**无需修改** `beforeSourceQuery_6`。
- 待服务端新 SQL 若增删入参，仅同步 return 字段。

### 观察（不属本任务修复范围）

`rangeCase` 在 if/else 内用 `let rangeCase = 1/2` 遮蔽了外层 `let rangeCase = 0`，导致 `fm4_1.rangeCase` 恒为 0。属改造前既有行为，与本次契约兼容性无关；若联调发现班次过滤异常再单开修复。
