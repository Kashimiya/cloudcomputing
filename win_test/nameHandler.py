double_ln = [
    "欧阳", "太史", "端木", "上官", "司马", "东方", "独孤", "南宫", "万俟", "闻人", "夏侯", "诸葛", "尉迟",
    "公羊", "赫连", "澹台", "皇甫", "宗政", "濮阳", "公冶", "太叔", "申屠", "公孙", "慕容", "仲孙", "钟离",
    "长孙", "宇文", "司徒", "鲜于", "司空", "闾丘", "子车", "司寇", "巫马", "公西", "颛孙", "壤驷", "公良",
    "漆雕", "乐正", "宰父", "谷梁", "拓跋", "夹谷", "轩辕", "令狐", "段干", "百里", "呼延", "东郭", "南门",
    "西门", "羊舌", "微生", "公户", "第五", "公乘", "贯丘", "公皙", "南荣", "东里", "东宫", "仲长", "子书",
    "子桑", "即墨", "达奚", "褚师", "安陵", "完颜"
]

not_ln = [
    "阿", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十", "小", "大", "老"
]

not_name = [
    "人", "众", "炮灰", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O",
    "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "·", "皇帝", "皇后", "甲乙丙丁", "姐", "妹",
    "弟", "*", "了", "~", "教主", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "爸", "妈", "奶"
]

not_first_name = [
    "皇后", "帝", "王爷", "公主", "公子", "王后", "父亲", "母亲", "娘娘", "贵妃", "爷爷",
    "公公", "大帝", "姥", "姑", "姨", "爷", "老君", "老", "氏"
]


def is_double_ln(name):
    if name in double_ln: return True
    return False


def is_ln(name):
    if name in not_ln: return False
    return True


def is_name(name):
    for nn in not_name:
        if nn in name: return False
    return True


def is_fn(name):
    for nfn in not_first_name:
        if nfn in name: return False
    return True


def handle(name_list):
    last_name = []
    first_name = []
    for name in name_list:
        length = len(name)
        if not is_name(name):
            continue
        if length > 4:
            continue
        if length == 4:
            last_name.append(name[0:2])
            if is_fn(name[2:4]):
                first_name.append(name[2])
                first_name.append(name[3])
        if length == 3:
            if is_double_ln(name):
                last_name.append(name[0:2])
                first_name.append(name[2])
            else:
                if is_ln(name[0]):
                    last_name.append(name[0])
                if is_fn(name[1:3]):
                    first_name.append(name[1])
                    first_name.append(name[2])
        if length == 2:
            if is_ln(name[0]):
                last_name.append(name[0])
            if is_fn(name[1]):
                first_name.append(name[1])
    return [list(set(last_name)), list(set(first_name))]
