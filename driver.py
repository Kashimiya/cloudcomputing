import json

import jinjiang_utils as jju
import network_utils


class Driver:
    lib = jju.JinjiangPagesLib()

    def __init__(self):
        pass

    # start的范围: range(1,990,10)
    # 向本地写入第start页（包括）到start+10页（包括）的书籍信息
    # path: 目标文件夹
    def write_pages(self, start, path):
        base = self.lib.jinjiang_index
        target = path + 'page' + str(start) + '-' + str(start + 10) + '.json'
        postfix = '&page='
        all_infos = []
        for i in range(start, start + 11):
            page = postfix + str(i)
            url = base + page
            html = network_utils.get_full_page(url, self.lib.jinjiang_decode, mode=0)
            if html is None:
                print('索引页获取失败！索引页URL:', url)
            index_info = jju.parse_jinjiang_index(html)
            infos = jju.format_jinjiang_bookinfo(index_info)
            all_infos.extend(infos)
        with open(target, 'w') as file:
            for book in all_infos:
                json.dump(book, file)


if __name__ == '__main__':
    target_dir = '../data/'  # 目标文件夹
    start_page = 1  # 从第几页开始读
    driver = Driver()
    driver.write_pages(start_page, target_dir)
