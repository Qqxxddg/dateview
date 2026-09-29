// 任务5验证：postHandler / preHandler 行为测试（与布局文件中字符串同源）
const fs = require('fs');
const { execSync } = require('child_process');

// 从布局文件提取处理器源码，保证测的就是落盘代码
const outer = JSON.parse(fs.readFileSync('D:/dataview-workspace/DataView_布局文件[0-统计看板].dv.json', 'utf-8'));
const content = JSON.parse(outer[0].content);
const el = content.pages[0].elements.find(e => e.refName === '#card7');
const src = el.option.sources[0];
const postSrc = src.postHandler;
const preSrc = src.preHandler;

let failed = 0;
function assert(cond, msg) {
  if (cond) { console.log('  PASS', msg); }
  else { console.log('  FAIL', msg); failed++; }
}

// --- mock this ---
function makeThis() {
  const models = {};
  return {
    models,
    $container: {
      $model(k, v) { if (arguments.length === 2) { models[k] = v; return v; } return models[k]; },
      $component(name) {
        if (name === '#select0') return { tmpValue: 'ALL', value: null };
        if (name === '#select1') return { tmpValue: 'day', value: null };
        return null;
      }
    }
  };
}

async function runPost(rows, ctx) {
  // postHandler 体是 "return new Promise(...)" —— 包成函数
  const fn = new Function('data', postSrc);
  return fn.call(ctx, rows);
}

function runPre(params, ctx) {
  const fn = new Function('data', preSrc);
  return fn.call(ctx, params);
}

(async () => {
  console.log('== postHandler: 状态码映射 + 排序 ==');
  let ctx = makeThis();
  let out = await runPost([
    { robot_code: 'AMR-010', status: '3' }, // 空闲
    { robot_code: 'AMR-002', status: '4' }, // 异常
    { robot_code: 'AMR-001', status: '1' }, // 运行
    { robot_code: 'AMR-003', status: '0' }, // 离线
    { robot_code: 'AMR-004', status: '2' }, // 充电
  ], ctx);
  assert(out.map(r => r.status).join(',') === '异常,离线,运行,充电,空闲', '排序=异常→离线→运行→充电→空闲');
  assert(out[0].amr_code === 'AMR-002' && out[0].status === '异常', 'AMR-002 异常 首位');
  assert(out[4].amr_code === 'AMR-010', '同状态车号升序');

  console.log('== postHandler: 未知状态原样排尾 + 不丢行 ==');
  out = await runPost([
    { robot_code: 'A', status: '维修中' },
    { robot_code: 'B', status: '1' },
    { robot_code: 'C', status: '9' },
  ], makeThis());
  assert(out.length === 3, '3 行全保留');
  assert(out[0].status === '运行', '已知状态排前');
  assert(out[1].status === '维修中' && out[2].status === '9', '未知状态排尾、同级按车号升序、原样保留');

  console.log('== postHandler: 空数据降级 ==');
  out = await runPost([], makeThis());
  assert(out.length === 1 && out[0].status === '暂无数据', '空数组→占位行');
  out = await runPost(null, makeThis());
  assert(out[0].status === '暂无数据', 'null→占位行');

  console.log('== postHandler: 同内容返回同一引用（防跳顶）==');
  ctx = makeThis();
  const rows = [{ robot_code: 'X', status: '1' }];
  const a = await runPost(rows, ctx);
  const b = await runPost([{ robot_code: 'X', status: '1' }], ctx);
  assert(a === b, '内容一致时返回同一数组引用');
  const c = await runPost([{ robot_code: 'Y', status: '1' }], ctx);
  assert(c !== b && c[0].amr_code === 'Y', '内容变化时返回新数组');

  console.log('== preHandler: mapcodes 归一 ==');
  ctx = makeThis();
  let p = runPre({ mapcodes: '', robotcodes: '' }, ctx);
  assert(p.mapcodes === null, 'ALL→null');
  assert(ctx.models.mapcodes === 'ALL', 'model.mapcodes 记录原值');
  assert(ctx.models.date === 'day', 'model.date 记录');
  assert(p.robotcodes === '', 'robotcodes 不传');

  ctx = makeThis();
  ctx.$container.$component = (n) => n === '#select0' ? { tmpValue: 'MAP01,MAP02', value: null } : { tmpValue: null, value: null };
  p = runPre({}, ctx);
  assert(p.mapcodes === 'MAP01,MAP02', '多值逗号照传');

  console.log();
  if (failed === 0) console.log('ALL PASS');
  else { console.log('FAILED:', failed); process.exit(1); }
})();
