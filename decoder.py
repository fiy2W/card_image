import math


def read_conf(path):
    with open(path, 'r', encoding='utf8') as f:
        strs = f.readlines()

    table = []
    for s in strs:
        if s[0] == '#':
            continue
        table.append(s.split(' '))
    return table


def make_setcode_dict(setcode_table):
    setcode_dict = {}

    for line in setcode_table:
        if line[0] == '!setname':
            setcode_dict[line[1]] = line[2]
    return setcode_dict


static_dict = {
    'ot': {
        1: 'ocg', 2:'tcg', 3:'ocg&tcg',
    },
    'type': {
        -1: '怪兽', -2: '魔法', -3: '陷阱',
        -5: '通常', -6: '效果', -7: '融合', -8: '仪式', -9: '陷阱怪兽',
        -10: '灵魂', -11: '同盟', -12: '二重', -13: '调整', -14: '同调', -15: '衍生物',
        -17: '速攻', -18: '永续', -19: '装备', -20: '场地', -21: '反击',
        -22: '反转', -23: '卡通', -24: '超量', -25: '灵摆', -26: '特殊召唤', -27: '连接'
    },
    'race': {
        0: 'none', 1: '战士', 2: '魔法师', 3: '天使', 4: '恶魔',
        5: '不死', 6: '机械', 7: '水', 8: '炎', 9: '岩石',
        10: '鸟兽', 11: '植物', 12: '昆虫', 13: '雷', 14: '龙',
        15: '兽', 16: '兽战士', 17: '恐龙', 18: '鱼', 19: '海龙',
        20: '爬虫类', 21: '念动力', 22: '幻神兽', 23: '创造神', 24: '幻龙',
        25: '电子界',
    },
    'attribute': {
        0: 'none', 1: '地', 2: '水', 3: '炎', 4: '风', 5: '光', 6: '暗', 7: '神',
    },
    'category': {
        -1: '魔陷破坏', -2: '怪兽破坏', -3: '卡片除外', -4: '送去墓地', -5: '返回手卡',
        -6: '返回卡组', -7: '手卡破坏', -8: '卡组破坏', -9: '抽卡辅助', -10: '卡组检索',
        -11: '卡片回收', -12: '表示形式', -13: '控制权', -14: '攻守变化', -15: '穿刺伤害',
        -16: '多次攻击', -17: '攻击限制', -18: '直接攻击', -19: '特殊召唤', -20: '衍生物',
        -21: '种族相关', -22: '属性相关', -23: 'LP伤害', -24: 'LP回复', -25: '破坏耐性',
        -26: '效果耐性', -27: '指示物', -28: '幸运', -29: '融合相关', -30: '同调相关',
        -31: '超量相关', -32: '效果无效',
    },
}


setcode_dict = make_setcode_dict(read_conf('strings.conf'))


def log_decode(code):
    if code <= 0:
        return 0
    else:
        return int(math.log2(code) + 1)


def setcode_decode(code):
    hexcode = hex(code)[2:]
    setcode = []
    while len(hexcode) > 0:
        c = int('0x'+hexcode[-4:], 16)
        if c == 0:
            break
        setcode.append(hex(c))
        hexcode = hexcode[:-4]
    return setcode


def setcode_trans(setcode):
    setcode_new = []
    for sc in setcode:
        setcode_new.append(setcode_dict[sc])
    return setcode_new


def fill_code(code, length):
    code = code[2:].zfill(length)
    return code


def cate_decode(code):
    if code < 0:
        num = bin(~code)
        nums = num[:1] + num[2:]
        new_n = ''
        for n in nums:
            new_n += str(1 - int(n))
        num = new_n
    else:
        num = bin(code)
    return num


def bincode_trans(code, key):
    code_list = []
    for i in range(len(code)):
        idx = - i - 1
        if code[idx] == '1':
            code_list.append(static_dict[key][idx])
    return code_list