#-*- coding:utf-8 -*-
import matplotlib.pyplot as plt
import jieba
from wordcloud import WordCloud

path_from="D:/大三上/云计算/cloud_data/name/"
path_to="D:/大三上/云计算/爬虫/wordcloudtest/pic/"

def getFileList():
    import os
    file_list = os.listdir(path_from)
    return file_list
# 1.读入txt文本数据
for filename in getFileList():
        print(filename)
        f1 = open(path_from + filename, 'rb')
        text = f1.read().decode("utf-8")
        text=str(text)
        #print(text)
        # 2.分词
        temp = text.split('\n')
        temp3=[]#姓氏
        temp4=[]#名
        flag=True
        for item in temp:
                temp1=item.split(';')
                for item1 in temp1:
                        # print(flag)
                        if len(item1)==0:
                                break
                        if item1=="None" or item1=="one":
                                continue
                        if flag:
                                if item1[0]=='[':
                                        temp2=item1[2:-2]
                                        # print(temp2)
                                        if temp2!='':
                                                temp3.extend(temp2.split(("', '")))
                                        flag=False
                        else:
                                if item1[0]=='[':
                                        temp2=item1[2:-3]
                                        # print(temp2)
                                        if temp2 != '':
                                                temp4.extend(temp2.split(("', '")))
                                        flag=True
        # print(type(cut_text))
        # 必须给个符号分隔开分词结果来形成字符串,否则不能绘制词云
        ans1={}
        for item in temp3:
                if ans1.keys().__contains__(item):
                        ans1[item]=ans1[item]+1
                else:
                        ans1[item]=1
        ans2={}
        for item in temp4:
                if ans2.keys().__contains__(item):
                        ans2[item]=ans2[item]+1
                else:
                        ans2[item]=1
        # 3.生成词云图，这里需要注意的是WordCloud默认不支持中文，所以这里需已下载好的中文字库
        # 无自定义背景图：需要指定生成词云图的像素大小，默认背景颜色为黑色,统一文字颜色：mode='RGBA'和colormap='pink'
        wc = WordCloud(
                # 设置字体，不指定就会出现乱码
                # 设置背景色
                font_path="STKAITI.TTF",
                background_color='white',
                # 设置背景宽
                width=500,
                # 设置背景高
                height=350,
                # 最大字体
                max_font_size=50,
                # 最小字体
                min_font_size=10,
                mode='RGBA'
                #colormap='pink'
                )
        # 产生词云
        wc.generate_from_frequencies(ans1)
        # 保存图片
        wc.to_file(path_to+filename[:-4]+"姓.png") # 按照设置的像素宽高度保存绘制好的词云图，比下面程序显示更清晰
        wc.generate_from_frequencies(ans2)
        wc.to_file(path_to+filename[:-4]+"名.png") # 按照设置的像素宽高度保存绘制好的词云图，比下面程序显示更清晰