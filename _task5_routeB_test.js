// 路线B验证：binds 模板归一化 + setData 行为
const fs = require('fs');
const outer = JSON.parse(fs.readFileSync('D:/dataview-workspace/DataView_布局文件[0-统计看板].dv.json', 'utf-8'));
const content = JSON.parse(outer[0].content);
const src = content.pages[0].sources.find(s => s.source === 'SQL09091542');
const tpl = src.binds[0].template;

let failed = 0;
const assert = (c, m) => { console.log(c ? '  PASS' : '  FAIL', m); if (!c) failed++; };

function run(data) {
  const calls = [];
  const ctx = {
    $component: (ref) => {
      assert(ref === '#card7', 'binds 指向 #card7');
      return { setData: (d) => calls.push(d) };
    }
  };
  const fn = new Function('data', tpl);
  const ret = fn.call(ctx, data);
  return { calls, ret };
}

console.log('== wrapper 响应（真实形态）==');
let { calls, ret } = run({
  code: '0', total: 2, success: true,
  data: [
    { robot_code: '13541', status: '3' },
    { robot_code: '13593', status: '2' },
    { robot_code: '99999', status: '4' },
  ]
});
assert(calls.length === 1, 'setData 调用 1 次');
assert(ret.length === 3, '返回 3 行');
assert(ret[0].amr_code === '99999' && ret[0].status === '异常', '异常首位');
assert(ret[1].status === '充电' && ret[2].status === '空闲', '充电→空闲 顺序');
assert(calls[0] === ret, 'setData 与 return 同一数组');

console.log('== 纯数组输入 ==');
({ calls, ret } = run([{ robot_code: 'A', status: '1' }]));
assert(ret[0].status === '运行' && ret[0].amr_code === 'A', '1→运行');

console.log('== 空数据 → 占位行 ==');
({ calls, ret } = run([]));
assert(ret.length === 1 && ret[0].status === '暂无数据', '空→占位行且 setData');
assert(calls.length === 1, '占位行也 setData');

console.log('== 未知状态 ==');
({ calls, ret } = run([{ robot_code: 'Z', status: '维修中' }]));
assert(ret[0].status === '维修中', '未知状态原样');

console.log();
if (!failed) console.log('ALL PASS'); else { console.log('FAILED', failed); process.exit(1); }
