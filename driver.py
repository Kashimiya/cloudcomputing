import jinjiang_utils as jju
import network_utils


class Driver:
    lib = jju.JinjiangPagesLib()

    def __init__(self):
        pass

    # start的范围: range(1,990,10)
    # 向本地写入第start页的书籍信息
    # path: 目标文件夹
    def write_pages(self, start, path):
        base = self.lib.jinjiang_index
        target = path + 'page' + str(start) + '-' + str(start + 0) + '.json'
        postfix = '&page='
        all_infos = []
        for i in range(start, start + 1):
            page = postfix + str(i)
            url = base + page
            html = network_utils.get_full_page(url, self.lib.jinjiang_decode, mode=0)
            if html is None:
                print('索引页获取失败！索引页URL:', url)
                print('尝试重试')
                html = network_utils.get_full_page(url, self.lib.jinjiang_decode, mode=1)
                if html is None:
                    print('尝试失败！')
                    continue
                else:
                    print('再次获取成功！')
            index_info = jju.parse_jinjiang_index(html)
            infos = jju.format_jinjiang_bookinfo(index_info)
            all_infos.extend(infos)
        with open(target, 'w') as file:
            file.write('{\n')
            for i in range(len(all_infos)):
                file.write(str(all_infos[i].toDict()))
                print(str(all_infos[i].toDict()))
                if i != len(all_infos) - 1:
                    file.write(',')
                file.write('\n')
            file.write('}\n')


if __name__ == '__main__':
    target_dir = '../data/'  # 目标文件夹
    start_page = 1  # 从第几页开始读
    driver = Driver()
    driver.write_pages(start_page, target_dir)
