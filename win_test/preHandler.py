import time
import json

# 源
path_dic1 = {
    "fbj": 'D:/cloud/new_data/',
    "why": '',
    "zjy": '',
    "wxy": ''
}

# 目的
path_dic2 = {
    "fbj": 'D:/cloud/cleaned_data/',
    "why": '',
    "zjy": '',
    "wxy": ''
}

usr = "fbj"


def getFileList():
    import os
    file_list = os.listdir(path_dic1[usr])
    return file_list


# 晋江百家姓
def fbj():
    import nameHandler
    for filename in getFileList():
        print(filename)
        f1 = open(path_dic1[usr] + filename, 'r', encoding='utf-8')
        f2 = open(path_dic2[usr] + filename[0:len(filename) - 5] + '.txt', 'w', encoding='utf-8-sig')
        file1 = json.loads(f1.read().replace('\\','').replace('	',''))
        for line in file1:
            last_first_name = nameHandler.handle(line['leading'] + line['supporting'])
            last_name = last_first_name[0]
            first_name = last_first_name[1]
            times = line['times']
            pub_date=line['pub_date'][0:10]
            f2.write(pub_date+";"+times+";"+last_name.__str__()+";"+first_name.__str__()+"\n")
        time.sleep(2)


if __name__ == '__main__':
    fbj()
