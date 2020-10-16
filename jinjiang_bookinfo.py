# 晋江图书信息类
class JJBook:
    author = ''  # 作者
    name = ''  # 名字
    originality = ''  # 原创性
    disposition = ''  # 性向
    times = ''  # 时代
    type = ''  # 类型
    style = ''  # 风格
    word_number = 0  # 字数
    score = 0  # 总分
    pub_date = ''  # 发布日期
    web_url = ''  # 主页
    tags = []  # 标签
    leading = []  # 主角
    supporting = []  # 配角

    def __init__(self):
        pass

    # 将类转换为字典，以便于使用json.dumps()和打印输出
    def toDict(self):
        return {
            'author': self.author,
            'name': self.name,
            'originality': self.originality,
            'disposition': self.disposition,
            'times': self.times,
            'type': self.type,
            'style': self.style,
            'word_number': self.word_number,
            'score': self.score,
            'pub_date': self.pub_date,
            'web_url': self.web_url,
            'tags': self.tags,
            'leading': self.leading,
            'supporting': self.supporting
        }

    def print_myself(self):
        print(self.toDict())
