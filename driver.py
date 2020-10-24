import json

import jinjiang_utils as jju
import network_utils


class Driver:
    lib = jju.JinjiangPagesLib()
    yearlib = ['fbsj2010=2010', 'fbsj2011=2011', 'fbsj2012=2012', 'fbsj2013=2013'
        , 'fbsj2014=2014', 'fbsj2015=2015', 'fbsj2016=2016', 'fbsj2017=2017'
        , 'fbsj2018=2018', 'fbsj24=24']

    # 初始化: 登录网址，建立会话
    def __init__(self, url, option_path):
        self.session = network_utils.login(url, option_path=option_path)
        pass

    # year的范围: range(10,20)
    # 向本地写入第start页的书籍信息
    # path: 目标文件夹
    def write_pages(self, start, path, year):
        base = 'http://www.jjwxc.net/bookbase.php?fw0=0&' + self.yearlib[
            int(year % 10)] + '&ycx0=0&xx0=0&mainview0=0&sd0=0&lx0=0&fg0=0&collectiontypes=ors&null=0&searchkeywords='
        target = path + str(year) + 'page' + str(start) + '-' + str(start + 9) + '.json'
        postfix = '&page='
        all_infos = []
        for i in range(start, start + 10):
            page = postfix + str(i)
            url = base + page
            html = network_utils.get_full_page(url, self.session, encoding=self.lib.jinjiang_decode)
            if html is None:
                print('索引页获取失败！索引页URL:', url)
                print('尝试重试')
                html = network_utils.get_full_page(url, self.session, encoding=self.lib.jinjiang_decode, mode=1)
                if html is None:
                    print('尝试失败！')
                    continue
                else:
                    print('再次获取成功！')
            print('--------------------正在爬取第', i, '页--------------------')
            index_info = jju.parse_jinjiang_index(html)
            infos = jju.format_jinjiang_bookinfo(index_info, session=self.session)
            all_infos.extend(infos)
        with open(target, 'w', encoding='utf-8') as file:
            file.write('[\n')
            for i in range(len(all_infos)):
                file.write(json.dumps(all_infos[i].__dict__).encode('gb18030').decode('unicode_escape'))
                if i != len(all_infos) - 1:
                    file.write(',')
                file.write('\n')
            file.write(']\n')


if __name__ == '__main__':
    target_dir = '../data/'  # 目标文件夹
    driver = Driver('http://www.jjwxc.net/', 'C:\\Users\\Kashimiya\\AppData\\Local\\Google\\Chrome\\User Data1')
    # 19代表2019-2020年
    for i in range(1, 200, 10):
        driver.write_pages(i, target_dir, year=13)
