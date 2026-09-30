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

