import json
import time

# 源
path_dic1 = {
    "name": '../data/',
    "type": '../data/',
    "tag": '../data/'
}

# 目的
path_dic2 = {
    "name": '../cleaned_data/name/',
    "type": '../cleaned_data/type/',
    "tag": '../cleaned_data/tag/'
}


def getFileList(usr):
    import os
    file_list = os.listdir(path_dic1[usr])
    return file_list


# 晋江百家姓
def nameCount(usr):
    import nameHandler
    for filename in getFileList(usr):
        print(filename)
        try:
            f1 = open(path_dic1[usr]  # 源文件夹目录
                      + filename
                      , 'r', encoding='utf-8')
            f2 = open(path_dic2[usr]  # 目标文件夹目录
                      + filename[0:len(filename) - 5]
                      + '.txt'
                      , 'w', encoding='utf-8-sig')
            # 个别非法字符过滤处理
            file1 = json.loads(f1.read().replace('\\', '').replace('	', ''))
            for line in file1:
                # line为源文件里的一条记录
                # nameHandler处理主角+配角列表，返回去重的姓、名列表
                last_first_name = nameHandler.handle(line['leading'] + line['supporting'])
                last_name = last_first_name[0]
                first_name = last_first_name[1]
                times = line['times']
                pub_date = line['pub_date'][0:10]
                f2.write(pub_date + ";" + times + ";"
                         + last_name.__str__() + ";"
                         + first_name.__str__() + "\n")
            time.sleep(2)
        except Exception:
            print(filename + ":error\n")
            continue


def typeCount(usr):
    for filename in getFileList(usr):
        print(filename)
        try:
            f1 = open(path_dic1[usr] + filename, 'r', encoding='utf-8')
            f2 = open(path_dic2[usr] + filename[0:len(filename) - 5] + '.txt', 'w', encoding='utf-8-sig')
            file1 = json.loads(f1.read().replace('\\', '').replace('	', ''))
            for line in file1:
                disposition = line['disposition']
                pub_date = line['pub_date'][0:10]
                f2.write(pub_date + ";" + disposition + "\n")
            time.sleep(2)
        except Exception:
            print(filename + ":error\n")
            continue


def tagCount(usr):
    for filename in getFileList(usr):
        print(filename)
        try:
            f1 = open(path_dic1[usr] + filename, 'r', encoding='utf-8')
            f2 = open(path_dic2[usr] + filename[0:len(filename) - 5] + '.txt', 'w', encoding='utf-8-sig')
            file1 = json.loads(f1.read().replace('\\', '').replace('	', ''))
            for line in file1:
                tags = line['tags']
                pub_date = line['pub_date'][0:10]
                score = line["score"]
                f2.write(pub_date + ";" + tags.__str__() + ";" + score + "\n")
            time.sleep(2)
        except Exception:
            print(filename + ":error\n")
            continue
