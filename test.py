from bs4 import BeautifulSoup

if __name__ == '__main__':
    html = '''
    <a class='you' href='http://you.com'>yeah!</a>
    <a align='left'>woo</a>
    '''
    bs = BeautifulSoup(html, 'html.parser')
    tags = bs.find_all('a', align='left')
    for i in tags:
        print(i.get('href'))
