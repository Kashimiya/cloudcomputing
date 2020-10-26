# -*-coding:utf-8-*-
import csv
import codecs
import os
import shutil


def trans(path):
    jsonData = codecs.open(path + '.json', 'r', 'utf-8')
    csvfile = open(path + '_mid.csv', 'w', newline='')
    csvout = open(path + '_to_add.csv', 'w', newline='')

    writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
    keys = ["date", "type", "value", "name"]
    writer.writerow(keys)  # 将属性列表写入csv中
    for line in jsonData:
        if line == '{\n' or line == '}\n':
            continue
        raw_data = line.replace('\"', '').replace(' ', '').replace('(', '').replace(':', '').replace(')', ',').replace(',\n', '')
        data = raw_data.split(',')
        data[0] += "-01-01"
        data.append(data[1])
        writer.writerow(data)

    jsonData.close()
    csvfile.close()
    with open(path + '_mid.csv') as csvin, csvout:
        reader = csv.DictReader(csvin)
        keys = ["name", "type", "value", "date"]
        writer = csv.writer(csvout, delimiter=',', quoting=csv.QUOTE_ALL)
        writer.writerow(keys)
        writer = csv.DictWriter(csvout, fieldnames=["name", "type", "value", "date"])
        for row in reader:
            writer.writerow(row)
    csvout.close()
    shutil.copyfile(path + '_to_add.csv', path + '_to_add1.csv')
    os.remove(path + '_mid.csv')

    csv_add = open(path + '_to_add.csv', 'r', newline='')

    csvfin = open(path + '.csv', 'w', newline='')
    # add by year
    dict_reader = csv.DictReader(csv_add)

    # 默认数据按照年份排序
    for row in dict_reader:
        if int(row['date'][0:4]) > 2010:
            csv_add1 = open(path + '_to_add1.csv', 'r', newline='')
            dict_reader1 = csv.DictReader(csv_add1)
            for rows in dict_reader1:
                if rows['name'] == row['name'] and int(rows['date'][0:4]) == int(row['date'][0:4]) - 1:
                    row['value'] = str(float(rows['value']) + float(row['value']))
            csv_add1.close()
        # print(row)
    csv_add.close()

    csv_add = open(path + '_to_add.csv', 'r', newline='')
    dict_reader2 = csv.DictReader(csv_add)

    keys = ["name", "type", "value", "date"]
    writer = csv.writer(csvfin, delimiter=',', quoting=csv.QUOTE_ALL)
    writer.writerow(keys)
    writer = csv.DictWriter(csvfin, fieldnames=["name", "type", "value", "date"])
    for row in dict_reader2:
        writer.writerow(row)
    csvfin.close()
    os.remove(path + '_to_add.csv')
    os.remove(path + '_to_add1.csv')


if __name__ == '__main__':
    path = str("/Users/wangxinyi/Desktop/done_data/tag/tags_by_year")  # 获取path参数
    trans(path)
