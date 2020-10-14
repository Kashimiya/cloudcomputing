from bs4 import BeautifulSoup
import network_utils


# 针对起点爬取排名的一个parse方法
# 可以当作示例使用
def parse_qidian_rank(page_html):
    names = []
    soup = BeautifulSoup(page_html, 'html.parser')
    # 选取div类标签，class为'book-img-text'
    books = soup.find_all('div', class_='book-img-text')
    download_soup = BeautifulSoup(str(books), 'html.parser')
    # 选取a类标签
    for name in download_soup.find_all('a'):
        names.append(name.string)
    return names


def format_qidian_rank(names):
    # 分别是书名/作者/小说类别/排名
    # 一本书下方有7个a类的标签
    # 0：书的封面 1：书名 2：作者 3：类别
    # 4：最新更新信息 5：书书籍详情按钮 6：加入书架按钮
    info = [[], [], [], []]
    for i in range(0, len(names), 7):
        info[0].append(names[i + 1])
        info[1].append(names[i + 2])
        info[2].append(names[i + 3])
        info[3].append((int)(i / 7 + 1))
    return info


# 包含可能会用到的起点的一些网址
class QidianPagesLib:
    # 起点中文网排行网址
    # page=1是指第一页
    qidian_book_rank_pages = {
        '起点月票榜': 'https://www.qidian.com/rank/yuepiao?style=1&page=1',
        '原创风云榜': 'https://www.qidian.com/rank/fengyun?style=1&page=1',
        '24小时热销榜': 'https://www.qidian.com/rank/hotsales?style=1&page=1',
        '阅读指数榜': 'https://www.qidian.com/rank/readIndex?style=1&page=1',
        '新增粉丝榜': 'https://www.qidian.com/rank/newFans?style=1&page=1',
        '推荐票榜': 'https://www.qidian.com/rank/recom?style=1&page=1',
        '收藏榜': 'https://www.qidian.com/rank/collect?style=1&page=1',
        'VIP更新榜': 'https://www.qidian.com/rank/vipup?style=1&page=1',
        'VIP收藏榜': 'https://www.qidian.com/rank/vipcollect?style=1&page=1',
        'VIP精品打赏榜': 'https://www.qidian.com/rank/vipreward?style=1&page=1',
        '签约作者新书榜': 'https://www.qidian.com/rank/signnewbook?style=1&page=1',
        '公众作者新书榜': 'https://www.qidian.com/rank/pubnewbook?style=1&page=1',
        '新人签约新书榜': 'https://www.qidian.com/rank/newsign?style=1&page=1',
        '新人作者新书榜': 'https://www.qidian.com/rank/newauthor?style=1&page=1',
    }
    # 起点女生排行是和一般起点排行不同体系的排行网，这里记录它们的前缀，只需更改一般排行网的网址即可得到女生排行
    # 示例：起点女生月票榜：
    # https://www.qidian.com/mm/rank/yuepiao?style=1&page=1
    qidian_girl_prefix = 'mm'
    # 打赏粉丝榜不分女生，也没有页数
    qidian_fan_rank_pages = {'打赏粉丝榜': 'https://www.qidian.com/rank/fans', }

    def __init__(self):
        pass


if __name__ == '__main__':
    # 爬取前3页作为测试
    urls = ["https://www.qidian.com/rank/hotsales?style=1&page={}".format(str(i)) for i in range(1, 4)]
    names = []
    for i in range(3):
        network_utils.net_wait(3)
        names = names + parse_qidian_rank(network_utils.get_full_page(urls[i]))
    info = format_qidian_rank(names)
    print(info)
