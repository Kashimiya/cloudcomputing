import re

from bs4 import BeautifulSoup

import network_utils
from jinjiang_bookinfo import JJBook


#  输入：原结构，如'\n                                    原创-纯爱-架空历史-爱情                                '
#  输出：目标结构，如['原创','纯爱','架空历史','剧情']
def get_features(feat):
    feat = re.sub("\n| ", '', feat)
    return feat.split('-')


#  输入：原结构，如'\n                                    轻松                                '
#  输出：目标结构，如'轻松'
def get_style(style):
    return re.sub("\n| ", '', style)


# 替换全角括号
def replaceAllFullWidth(s):
    a = s.replace('（', '(')
    a = a.replace('）', ')')
    a = a.replace('【', '[')
    a = a.replace('】', ']')
    a = a.replace('，', ',')
    a = a.replace('、', ',')
    return a


# 针对晋江索引网站的爬取
def parse_jinjiang_index(page_html):
    if page_html is None:
        return [[], []]
    names_a = []
    names_td = []
    soup = BeautifulSoup(page_html, 'html.parser')
    # 选取table类标签，class为cytable，获取书本列表
    books = soup.find_all('table', class_='cytable')
    dowload_soup = BeautifulSoup(str(books), 'html.parser')
    # 选取a类标签，获取0 作者、1 书名、2 书籍首页
    for name in dowload_soup.find_all('a'):
        names_a.append(name.string)
        if name.get('title') is not None:
            names_a.append('http://www.jjwxc.net/' + name.get('href'))
    # 选取td类标签，筛选到的有6个
    # 0 原创性-性向-时代-类型
    # 1 风格 2 包含着是否完结的一个html，个人感觉没必要 3 字数
    # 4 作品积分 5 发表时间
    for name in dowload_soup.find_all('td'):
        if name.get('class') is not None:
            continue
        elif name.get('align') == 'left':
            continue
        else:
            names_td.append(name.string)
    return [names_a, names_td]


# 针对晋江书本主页的信息爬取
def parse_jinjiang_onebook(page_html):
    if page_html is None:
        return [['GET FAILED'], ['GET FAILED'], ['GET FAILED']]
    tags = []
    leading = []
    supporting = []
    soup = BeautifulSoup(page_html, 'html.parser')
    # 选取div类标签，class为smallreadbody，获取书本介绍栏
    all_info = soup.find_all('div', class_='smallreadbody')
    download_soup = BeautifulSoup(str(all_info), 'html.parser')
    # 选取a类标签，style为text-decoration:none;color: red;，获取标签
    for tag in download_soup.find_all('a', style='text-decoration:none;color: red;'):
        tags.append(tag.string)
    # 选取span类标签，class为bluetext，获取主角和配角
    for info in download_soup.find_all('span', class_='bluetext'):
        info_strs = info.string.split(' ┃ ')
        if len(info_strs[0]) > 9:
            leading_str = info_strs[0][9:]
            leading_str = replaceAllFullWidth(leading_str)
            leading_str = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", leading_str)
            leading = leading_str.split(',')
        if len(info_strs[1]) > 3:
            supporting_str = info_strs[1][3:]
            supporting_str = replaceAllFullWidth(supporting_str)
            supporting_str = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", supporting_str)
            supporting = supporting_str.split(',')
    return [tags, leading, supporting]


# 获取书籍首页信息以及
# 格式化输出晋江书籍信息
# index_info: 索引页包含的信息
# count: 每一页最多爬几本书，默认-1即所有
# return 书籍(JJBook)数组
def format_jinjiang_bookinfo(index_info, count=-1):
    res = []
    counter = 0
    for i in range(0, int(len(index_info[0]) / 3)):
        if count != -1 and counter >= count:
            return res
        temp = JJBook()
        temp.author = index_info[0][3 * i]
        temp.name = index_info[0][3 * i + 1]
        temp.web_url = index_info[0][3 * i + 2]
        features = get_features(index_info[1][6 * i])
        temp.originality = features[0]
        temp.disposition = features[1]
        temp.times = features[2]
        temp.type = features[3]
        temp.style = get_style(index_info[1][6 * i + 1])
        temp.word_number = index_info[1][6 * i + 3]
        temp.score = index_info[1][6 * i + 4]
        temp.pub_date = index_info[1][6 * i + 5]
        network_utils.net_wait(2)
        onebook_html = network_utils.get_full_page(temp.web_url, 'gb18030', mode=0)
        if onebook_html is None:
            print('图书主页获取失败！主页URL:', temp.web_url)
            print('尝试重试')
            onebook_html = network_utils.get_full_page(temp.web_url, 'gb18030', mode=1)
            if onebook_html is None:
                print('尝试失败！')
                continue
            else:
                print('尝试成功！')
        counter += 1
        onebook_info = parse_jinjiang_onebook(onebook_html)
        temp.tags = onebook_info[0]
        temp.leading = onebook_info[1]
        temp.supporting = onebook_info[2]
        res.append(temp)
    return res


class JinjiangPagesLib:
    # 晋江索引网址，以下是参数列表
    # 以下采用简写，格式是xx？=？（xx是参数名，？是选项。如fw0=0）
    # fw: 范围 0不限 1全站 2完结半价 3VIP库
    # fbsj: 发布时间 0 2 3 6 12 24 2018-2003
    # 分别表示不限、2月内，3月内，6月内，1年内，2年内，xxxx年（2003-2018年中的一年内）
    # ycx: 原创性 0不限 1原创 2衍生
    # xx: 性向 0不限 1言情 2纯爱 3百合 4女尊 5无CP
    # mainview: 视角 0不限 1男主 2女主 3主攻 4主受 5互攻 6不明
    # sd: 时代 0不限 1近代现代 2古色古香 3=4架空历史 4=5幻想未来
    # lx: 类型
    # 0-10 不限、爱情、武侠、奇幻、仙侠、游戏、传奇、科幻、童话、惊悚、悬疑
    # 11=16 12=17 13=20 14=18 15=19 剧情、轻小说、古典衍生、东方衍生、西方衍生
    # 16=21 17=22 18=23 19=24 20=25 21=26 其他衍生、儿歌、散文、寓言、童谣、历史故事
    # fg: 风格 0-5 不限、悲剧、正剧、轻松、爆笑、暗黑
    # colltiontypes: ors求并集 ands求交集
    # null: 没有标签
    # bq标签，见pic/bq.jpg
    # -1   134  125  124  75   137  64   60   19   68
    # 66   122  185  83   6    33   208  135  81   20
    # 56   39   173  26   96   72   47   17   42   32
    # 99   62   1    57   4    92   128  206  82   90
    # 52   21   12   138  132  18   54   24   142  27
    # 41   74   30   143  136  205  65   127  5    145
    # 49   11   78   13   14   126  70   144  86   29
    # 15   25   61   23   101  139  184  38   59   97
    # 95   121  45   69   73   237  28   91   189  16
    # 2    174  191  35   178  103  46   175  67   51
    # 186  201  55   181  37   98   53   183  85   31
    # 141  94   48   177  22   180  192  199  58   196
    # 130  84   87   63   140  44   123  10   89   36
    # 8    79   215  148  50   190  188  182  7    80
    # 210  198  197
    # searchkeywords: 关键词，一般没用
    # 在末尾加入&page=x表示第x页
    jinjiang_index = 'http://www.jjwxc.net/bookbase.php?' \
                     'fw0=0&' \
                     'fbsj0=0&' \
                     'ycx0=0&' \
                     'xx0=0&' \
                     'mainview0=0&' \
                     'sd0=0&' \
                     'lx0=0&' \
                     'fg0=0&' \
                     'sortType=0&' \
                     'isfinish=0&' \
                     'collectiontypes=ors&searchkeywords='

    # 编码格式
    jinjiang_decode = 'gb18030'

    # 晋江前缀
    jinjiang_prefix = 'http://www.jjwxc.net/'

    def __init__(self):
        pass


if __name__ == '__main__':
    # 测试
    lib = JinjiangPagesLib()
    url = lib.jinjiang_index
    index_info = parse_jinjiang_index(network_utils.get_full_page(url, lib.jinjiang_decode, mode=0))
    infos = format_jinjiang_bookinfo(index_info, 10)
    for info in infos:
        info.print_myself()
