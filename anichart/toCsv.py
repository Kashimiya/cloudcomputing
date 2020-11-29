import codecs
import csv
import os


def trans(path):
    jsonData = codecs.open(path + '.json', 'r', 'gb2312')
    csvfile = open(path + '_mid.csv', 'w', newline='')
    csvout = open(path + '_to_add.csv', 'w', newline='')

    writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_ALL)
    keys = ["date", "type", "value", "name"]
    writer.writerow(keys)  # 将属性列表写入csv中
    for line in jsonData:
        if line == '{\n' or line == '}':
            continue
        raw_data = line.replace('\"', '').replace(' ', '').replace('(', '').replace(':', '').replace(')', ',').replace(
            ',\n', '')
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
    os.remove(path + '_mid.csv')
    # adder()

    # 输出累加后的文件
    csvfin = open(path + '.csv', 'w', newline='')
    csv_adder = open(path + '_to_add.csv', 'r', newline='')
    dict_reader2 = csv.DictReader(csv_adder)

    keys = ["name", "type", "value", "date"]
    writer = csv.writer(csvfin, delimiter=',', quoting=csv.QUOTE_ALL)
    writer.writerow(keys)
    writer = csv.DictWriter(csvfin, fieldnames=["name", "type", "value", "date"], extrasaction='ignore')
    for row in dict_reader2:
        writer.writerow(row)

    csvfin.close()
    os.remove(path + '_to_add.csv')


if __name__ == '__main__':
    path = str("./tags_by_year")  # 获取path参数
    trans(path)
