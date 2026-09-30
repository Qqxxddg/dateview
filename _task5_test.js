// 任务5验证 v2：含真实响应 wrapper 形态 + 就地改造语义
const fs = require('fs');

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
  const fn = new Function('data', postSrc);
  return fn.call(ctx, rows);
}
function runPre(params, ctx) {
  const fn = new Function('data', preSrc);
  return fn.call(ctx, params);
}

(async () => {
  console.log('== 真实响应 wrapper {code,data:[rows]} ==');
  let out = await runPost({
    code: '0', message: null, total: 2, success: true,
    data: [
      { rowid: 1, status: '3', map_code: 'BB', robot_code: '13541', baterry: 93 },
      { rowid: 1, status: '2', map_code: 'BB', robot_code: '13593', baterry: 83 },
    ]
  }, makeThis());
  assert(out.length === 2, 'wrapper 解析出行');
  assert(out[0].amr_code === '13593' && out[0].status === '充电', 'status 2→充电 且充电排前于空闲');
  assert(out[1].amr_code === '13541' && out[1].status === '空闲', 'status 3→空闲');

  console.log('== 排序优先级（就地）==');
  let ctx = makeThis();
  let rows = [
    { robot_code: 'AMR-010', status: '3' },
    { robot_code: 'AMR-002', status: '4' },
    { robot_code: 'AMR-001', status: '1' },
    { robot_code: 'AMR-003', status: '0' },
    { robot_code: 'AMR-004', status: '2' },
  ];
  out = await runPost(rows, ctx);
  assert(out === rows, '返回就地改造的原数组引用');
  assert(out.map(r => r.status).join(',') === '异常,离线,运行,充电,空闲', '排序=异常→离线→运行→充电→空闲');
  assert(out[0].amr_code === 'AMR-002', '异常首位');

  console.log('== 未知状态排尾不丢行 ==');
  out = await runPost([
    { robot_code: 'A', status: '维修中' },
    { robot_code: 'B', status: '1' },
    { robot_code: 'C', status: '9' },
  ], makeThis());
  assert(out.length === 3, '3 行全保留');
  assert(out[0].status === '运行' && out[1].status === '维修中' && out[2].status === '9', '未知排尾、同级车号升序');

  console.log('== 空/错降级 ==');
  out = await runPost([], makeThis());
  assert(out.length === 1 && out[0].status === '暂无数据', '空数组→占位行');
  out = await runPost({ code: '0', data: [] }, makeThis());
  assert(out[0].status === '暂无数据', 'wrapper 空 data→占位行');
  out = await runPost(null, makeThis());
  assert(out[0].status === '暂无数据', 'null→占位行');

  console.log('== 同内容防跳顶 ==');
  ctx = makeThis();
  const a = await runPost([{ robot_code: 'X', status: '1' }], ctx);
  const b = await runPost([{ robot_code: 'X', status: '1' }], ctx);
  assert(a === b, '同内容返回同一数组引用');
  const c = await runPost([{ robot_code: 'Y', status: '1' }], ctx);
  assert(c !== b && c[0].amr_code === 'Y', '内容变化返回新数组');

  console.log('== preHandler 归一 ==');
  ctx = makeThis();
  let p = runPre({ mapcodes: '', robotcodes: '' }, ctx);
  assert(p.mapcodes === null, 'ALL→null');
  assert(ctx.models.date === 'day', 'model.date 记录');

  console.log();
  if (failed === 0) console.log('ALL PASS');
  else { console.log('FAILED:', failed); process.exit(1); }
})();
