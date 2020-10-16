import json

if __name__ == '__main__':
    path = '../data/page1-10.json'
    file = open(path, encoding='gb18030')
    data = json.load(file)
    print(data[0])
