# -*- coding: utf-8 -*-
"""任务5收尾：抽取 applyCard7Rows 公共函数 + onLoaded 立即首拉，消除首屏等待"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
PATH = r'D:\dataview-workspace\DataView_布局文件[0-统计看板].dv.json'

APPLY_FN = r"""
this.applyCard7Rows = (data) => {
    let card = this.$component('#card7')
    let rows = []
    if (Array.isArray(data)) {
        rows = data
    } else if (data && Array.isArray(data.data)) {
        rows = data.data
    } else if (data && Array.isArray(data.list)) {
        rows = data.list
    }
    if (!rows || rows.length === 0) {
        rows = [{amr_code: '-', status: '暂无数据'}]
        card.setData(rows)
        return rows
    }
    const STATUS_MAP = {'0': '离线', '1': '运行', '2': '充电', '3': '空闲', '4': '异常'};
    const ORDER = {'异常': 0, '离线': 1, '运行': 2, '充电': 3, '空闲': 4};
    for (let i = 0; i < rows.length; i++) {
        let r = rows[i] || {}
        rows[i] = r
        let code = (r.status !== undefined && r.status !== null) ? String(r.status) : ''
        let st = STATUS_MAP[code]
        let amr = (r.robot_code !== undefined && r.robot_code !== null && r.robot_code !== '') ? String(r.robot_code) : ((r.amr_code !== undefined && r.amr_code !== null) ? String(r.amr_code) : '-')
        r.amr_code = amr
        r.status = (st !== undefined) ? st : (code === '' ? '-' : code)
    }
    rows.sort((a, b) => {
        let pa = ORDER[a.status] !== undefined ? ORDER[a.status] : 99
        let pb = ORDER[b.status] !== undefined ? ORDER[b.status] : 99
        if (pa !== pb) return pa - pb
        if (a.amr_code < b.amr_code) return -1
        if (a.amr_code > b.amr_code) return 1
        return 0
    })
    card.setData(rows)
    return rows
}

this.initCard7Now = async () => {
    try {
        let res = await this.doQueryData('SQL09091542', JSON.stringify({mapcodes: null, robotcodes: ''}), 'list')
        let payload = res && res.data !== undefined ? res.data : res
        this.applyCard7Rows(payload)
    } catch (e) {
        console.error('initCard7Now error', e)
        this.applyCard7Rows(null)
    }
}
"""

BIND_CALL = r"""console.log('card7 rows bind', data)
return this.applyCard7Rows(data)"""

outer = json.load(open(PATH, encoding='utf-8'))
content = json.loads(outer[0]['content'])
page = content['pages'][0]
script = page['script']

# 1) 追加公共函数（幂等）
if 'this.applyCard7Rows' not in script:
    script = script + APPLY_FN

# 2) onLoaded 里插入立即首拉
if 'this.initCard7Now()' not in script:
    assert 'this.initDeviceRealTime()' in script
    script = script.replace('this.initDeviceRealTime()', 'this.initDeviceRealTime(); this.initCard7Now()', 1)

page['script'] = script

# 3) binds 模板改为调用公共函数
for lst in (content['option']['sources'], page['sources']):
    for s in lst:
        if s.get('source') == 'SQL09091542':
            s['binds'][0]['template'] = BIND_CALL

outer[0]['content'] = json.dumps(content, ensure_ascii=False)
with open(PATH, 'w', encoding='utf-8') as f:
    json.dump(outer, f, ensure_ascii=False, indent=2)

c2 = json.loads(json.load(open(PATH, encoding='utf-8'))[0]['content'])
sc = c2['pages'][0]['script']
print('applyCard7Rows present:', 'this.applyCard7Rows' in sc)
print('initCard7Now present:', 'this.initCard7Now' in sc)
print('onLoaded hooks initCard7Now:', sc.count('this.initCard7Now()') >= 2)  # 调用+定义
print('binds template now:')
print([s['binds'][0]['template'] for s in c2['pages'][0]['sources'] if s.get('source') == 'SQL09091542'][0])
