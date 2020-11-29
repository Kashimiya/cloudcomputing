# -*- coding:utf-8 -*-
import json

from wordcloud import WordCloud

path_from = "../done_data/name/"
path_to = "../pic/"

text_firstname = open(path_from + "date_firstname.json", 'rb').read().decode("utf-8")
text_firstname = json.loads(text_firstname)
text_lastname = open(path_from + "times_lastname.json", 'rb').read().decode("utf-8")
text_lastname = json.loads(text_lastname)
ans1 = {}
ans2 = {}
for key in text_firstname:
    temp = key[1:-1].split(',')
    if temp[0] in ans1:
        ans1[temp[0]][temp[1]] = text_firstname[key]
    else:
        ans1[temp[0]] = {temp[1]: text_firstname[key]}
for key in text_lastname:
    temp = key[1:-1].split(',')
    if temp[0] in ans2:
        ans2[temp[0]][temp[1]] = text_lastname[key]
    else:
        ans2[temp[0]] = {temp[1]: text_lastname[key]}
# 3.生成词云图，这里需要注意的是WordCloud默认不支持中文，所以这里需已下载好的中文字库
# 无自定义背景图：需要指定生成词云图的像素大小，默认背景颜色为黑色,统一文字颜色：mode='RGBA'和colormap='pink'
for item in ans1:
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
        # colormap='pink'
    )
    # 产生词云
    temp = dict(sorted(ans1[item].items(), key=lambda d: d[1], reverse=True))
    ans = {}
    i = 0
    for item1 in temp:
        if i >= 80:
            break
        ans[item1] = temp[item1]
        i = i + 1
    wc.generate_from_frequencies(ans)
    # 保存图片
    wc.to_file(path_to + item + "名.png")  # 按照设置的像素宽高度保存绘制好的词云图，比下面程序显示更清晰
for item in ans2:
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
        max_font_size=200,
        # 最小字体
        min_font_size=10,
        mode='RGBA'
        # colormap='pink'
    )
    # 产生词云
    temp = dict(sorted(ans2[item].items(), key=lambda d: d[1], reverse=True))
    ans = {}
    i = 0
    for item1 in temp:
        if i >= 80:
            break
        ans[item1] = temp[item1]
        i = i + 1
    wc.generate_from_frequencies(ans)
    # 保存图片
    wc.to_file(path_to + item + "姓.png")
