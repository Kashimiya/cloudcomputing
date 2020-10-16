import re

if __name__ == '__main__':
    # html = '''
    # <a class="you" href="http://you.com">yeah!</a>
    # <a align="left" style="text-decoration:none;color: red;">woo</a>
    # '''
    # bs = BeautifulSoup(html, 'html.parser')
    # tags = bs.find_all('a', align='left')
    # for i in tags:
    #     print(i.get('style'))
    s = 'ni（sj）【jj】'
    s = s.replace('（', '(')
    s = s.replace('）', ')')
    a = re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", s)
    print(a)
