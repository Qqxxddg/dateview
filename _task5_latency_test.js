// applyCard7Rows 行为测试（函数体从布局脚本抽取）
const fs = require('fs');
const body = fs.readFileSync('D:/dataview-workspace/_extract_apply.js', 'utf-8');
let failed = 0;
const assert = (c, m) => { console.log(c ? '  PASS' : '  FAIL', m); if (!c) failed++; };
const calls = [];
const ctx = { $component: () => ({ setData: d => calls.push(d) }) };
const expr = body.replace('this.applyCard7Rows = (data) =>', 'function (data)').trim();
const fn = new Function('return (' + expr + ')')();

let out = fn.call(ctx, { code: '0', data: [
  { robot_code: '13541', status: '3' },
  { robot_code: '13593', status: '2' },
  { robot_code: 'X', status: '4' },
] });
assert(out.length === 3, 'rows=3');
assert(out[0].status === '异常' && out[1].status === '充电' && out[2].status === '空闲', 'sort+map 异常→充电→空闲');
assert(calls.length === 1, 'setData called');

out = fn.call(ctx, []);
assert(out[0].status === '暂无数据' && calls.length === 2, 'empty placeholder + setData');

out = fn.call(ctx, null);
assert(out[0].status === '暂无数据', 'null → placeholder');

console.log(failed ? 'FAILED ' + failed : 'ALL PASS');
process.exit(failed ? 1 : 0);
