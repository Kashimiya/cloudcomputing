import gzip
import random
import time
import urllib.request


def net_wait(second):
    # 避免操作太快被封ip,两次请求之间需要等待
    time.sleep(random.random() * second)


# mode
# 0 for 晋江/需要解压
# 1 for 起点/不需要解压
def get_full_page(page_url, decode='utf-8', mode=0):
    try:
        # 查看headers的方法
        # 打开想访问的网站：F12
        # 点击network一栏
        # 如果下方的内容为空就随便点这个网站的一个url
        # 下面出现内容之后随便点击一个，找到request headers一栏
        # 复制其中的User-Agent一栏到这里
        # 有需要也可以复制Refer一栏
        headers = {
            'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          r'Chrome/74.0.3729.169 Safari/537.36'}
        req = urllib.request.Request(url=page_url, headers=headers)
        response = urllib.request.urlopen(req)
        # 晋江的网页需要解压
        if mode == 0:
            return gzip.decompress(response.read()).decode(decode, 'ignore')
        # 起点的不需要
        elif mode == 1:
            return response.read().decode(decode)
    except Exception as msg:
        print('网页获取错误:', msg)
