import random
import time

import requests
import requests.cookies as rc
from selenium import webdriver


# 登录目标网站
# url: 要登录的网站
# option_path: chrome浏览器配置项路径
def login(url, option_path):
    option = webdriver.ChromeOptions()
    option.add_argument('--user-data-dir='
                        + option_path)
    driver = webdriver.Chrome(options=option)  # 使用谷歌chrome登录，电脑没有chrome的自行下载
    driver.get(url)
    time.sleep(3)
    allcookies = driver.get_cookies()  # 获取浏览器所有的cookie
    driver.quit()
    print("成功获取cookies！")
    s = requests.session()
    try:
        c = rc.RequestsCookieJar()
        for i in allcookies:
            c.set(i['name'], i['value'])
        s.cookies.update(c)
    except Exception as msg:
        print(u'添加cookies时出错：', msg)

    return s


def net_wait(second):
    # 避免操作太快被封ip,两次请求之间需要等待
    time.sleep(random.random() * second)


# 获取网页源代码
# page_url: 网页url
# session: 当前会话
def get_full_page(page_url, session, encoding='utf-8', mode=0):
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
        response = session.get(url=page_url, headers=headers)
        if mode == 0:
            response.encoding = encoding
        elif mode == 1:
            response.encoding = response.apparent_encoding
        return response.text
    except Exception as msg:
        print('网页获取错误:', msg)
