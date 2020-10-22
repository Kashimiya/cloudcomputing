from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext


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


conf = SparkConf()
conf.setAppName('TestDStream')
conf.setMaster('local')
sc = SparkContext(conf=conf)
ssc = StreamingContext(sc, 3)
lines = ssc.textFileStream('D:/cloud/cleaned_data')

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

# date_ln = date_times_ln \
#     .map(lambda x: ((x[0][0:4], x[2]), 1)) \
#     .reduceByKey(lambda x, y: x + y) \
#     .saveAsTextFiles('D:/cloud/done_data/date_lastname')
times_ln = date_times_ln \
    .map(lambda x: ((x[1], x[2]), 1)) \
    .reduceByKey(lambda x, y: x + y) \
    #    .saveAsTextFiles('D:/cloud/done_data/times_lastname')

date_fn = date_times_fn \
    .map(lambda x: ((x[0][0:4], x[2]), 1)) \
    .reduceByKey(lambda x, y: x + y) \
    #    .saveAsTextFiles('D:/cloud/done_data/date_firstname')
# times_fn = date_times_fn \
#     .map(lambda x: ((x[1], x[2]), 1)) \
#     .reduceByKey(lambda x, y: x + y) \
#     .saveAsTextFiles('D:/cloud/done_data/times_firstname')

ssc.start()
ssc.awaitTermination()
