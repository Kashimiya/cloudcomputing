from pyspark import SparkContext, SparkConf
from pyspark.rdd import RDD
from pyspark.streaming import StreamingContext
import json
import ast

path = '../done_data/tag/tags_by_year.json'


def open_result():
    try:
        result = open(path, 'r', encoding='utf-8')
        tag_dict = json.load(result)
        result.close()
    except Exception as e:
        tag_dict = {}
    return tag_dict


# 把读入的字符串line处理成列表
def getList(line):
    date_tags = line.split(';')
    date_tags[0] = date_tags[0][0:4].replace("'", "")
    date_tags[1] = date_tags[1].replace("'", "").replace("None", '').replace('[', '').replace(']', '').replace(' ', '')
    date_tags[2] = float(date_tags[2])/1000000
    print(date_tags)
    return date_tags


# 把姓、名的列表展开
def tagMap(lst):
    tag_lst = lst[1].split(',')
    return ((lst[0], tag, lst[2]) for tag in tag_lst)


def scoreMap(lst):
    return (lst[0], lst[1]), lst[2]


def writeFile(rdd: RDD):
    num = rdd.count()
    if num > 0:
        result_dic = open_result()
        print(result_dic)
        rdd_c = rdd.collect()
        lst = ast.literal_eval(str(rdd_c))
        for item in lst:
            key = item[0]
            value = item[1]
            if str(key).replace("'", '') in result_dic.keys():
                result_dic[str(key).replace("'", '')] = result_dic[str(key).replace("'", '')] + value
            else:
                result_dic[str(key).replace("'", '')] = value
        result = open(path, 'w', encoding='utf-8')
        result.write(json.dumps(result_dic).encode('gb18030').decode('unicode_escape'))
        result.close()


def start():
    conf = SparkConf()
    conf.setAppName('TestDStream')
    conf.setMaster('local')
    sc = SparkContext(conf=conf)
    ssc = StreamingContext(sc, 3)
    lines = ssc.textFileStream('../cleaned_data/tag')

    print(lines)
    single = lines.map(getList)

    date_tags = single \
        .flatMap(tagMap) \
        .filter(lambda x: len(x[1]) > 0) \
        .map(scoreMap) \
        .reduceByKey(lambda x, y: x + y) \
        .foreachRDD(writeFile)

    ssc.start()
    ssc.awaitTermination()
