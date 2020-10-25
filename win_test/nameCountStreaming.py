from pyspark import SparkContext, SparkConf
from pyspark.rdd import RDD
from pyspark.streaming import StreamingContext
import json
import ast
import preHandler
import time

path = ['D:/cloud/done_data/name/times_lastname.json', 'D:/cloud/done_data/name/date_firstname.json']
time.sleep(10)
preHandler.nameCount()


def open_result(f_type):
    if f_type == 0:
        try:
            result1 = open(path[0], 'r', encoding='utf-8')
            name_dict1 = json.load(result1)
            result1.close()
        except Exception as e:
            name_dict1 = {}
        return name_dict1
    else:
        try:
            result2 = open(path[1], 'r', encoding='utf-8-sig')
            name_dict2 = json.load(result2)
            result2.close()
        except Exception as e:
            name_dict2 = {}
        return name_dict2


# 把读入的字符串line处理成列表
def getList(line):
    date_times_ln_fn = line.split(';')
    date_times_ln_fn[2] = date_times_ln_fn[2][1:len(date_times_ln_fn[2]) - 2].replace("'", "")
    date_times_ln_fn[3] = date_times_ln_fn[3][1:len(date_times_ln_fn[3]) - 2].replace("'", "")
    return date_times_ln_fn


# 把姓、名的列表展开
def nameMap(lst, nametype):
    ln_lst = lst[2].split(',')
    fn_lst = lst[3].split(',')
    if nametype == 0:
        n_lst = ln_lst
    else:
        n_lst = fn_lst
    return ((lst[0], lst[1], n.replace(' ', '')) for n in n_lst)


def writeFile(rdd: RDD, f_type):
    num = rdd.count()
    if num > 0:
        result_dic = open_result(f_type)
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
        result = open(path[f_type], 'w', encoding='utf-8')
        result.write(json.dumps(result_dic).encode('gb18030').decode('unicode_escape'))
        result.close()

def start():

    conf = SparkConf()
    conf.setAppName('TestDStream')
    conf.setMaster('local')
    sc = SparkContext(conf=conf)
    ssc = StreamingContext(sc, 3)
    lines = ssc.textFileStream('D:/cloud/cleaned_data/name')

    print(lines)
    single = lines.map(getList)
    # date_times_ln:    发表日期-时代-姓 RDD
    date_times_ln = single \
        .flatMap(lambda x: nameMap(x, 0)) \
        .filter(lambda x: len(x[2]) > 0)

    date_times_ln.pprint(20)
    # date_times_ln:    发表日期-时代-名 RDD
    date_times_fn = single \
        .flatMap(lambda x: nameMap(x, 1)) \
        .filter(lambda x: len(x[2]) > 0)

    # 对姓的两种reduce:按照发表日期或按照时代
    # map 把(pub_date,ln)作为key，映射value为出现次数1（pub_date取年份）
    # reduceByKey 把key相同的项的值加起来

    times_ln = date_times_ln \
        .map(lambda x: ((x[1], x[2]), 1)) \
        .reduceByKey(lambda x, y: x + y) \
        .foreachRDD(lambda x: writeFile(x, 0))

    date_fn = date_times_fn \
        .map(lambda x: ((x[0][0:4], x[2]), 1)) \
        .reduceByKey(lambda x, y: x + y) \
        .foreachRDD(lambda x: writeFile(x, 1))

    ssc.start()
    ssc.awaitTermination()
