from pyspark import SparkContext, SparkConf
from pyspark.rdd import RDD
from pyspark.streaming import StreamingContext
import json
import ast

path = '../done_data/type/type_by_year.json'


def open_result():
    try:
        result = open(path, 'r', encoding='utf-8')
        type_dict = json.load(result)
        result.close()
    except Exception as e:
        type_dict = {}
    return type_dict


# 把读入的字符串line处理成列表
def getList(line):
    date_disposition = line.split(';')
    date_disposition[0] = date_disposition[0][0:4]
    date_disposition[1] = date_disposition[1].replace("'", "")
    return date_disposition


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
    lines = ssc.textFileStream('../cleaned_data/type')

    print(lines)
    single = lines.map(getList)
    # date_disposition:    发表日期-性向 RDD

    date_disposition = single \
        .filter(lambda x: len(x[1]) > 0) \
        .map(lambda x: ((x[0][0:4], x[1]), 1)) \
        .reduceByKey(lambda x, y: x + y) \
        .foreachRDD(lambda x: writeFile(x))

    ssc.start()
    ssc.awaitTermination()
