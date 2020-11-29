import json

path_from="D:/大三上/云计算/data/"
path_to="D:/大三上/云计算/data/"

text=open(path_from+"tags_by_year.json",'rb').read().decode("utf-8")
text=json.loads(text)
ans={}

for key in text:
    for key2 in text:
        if key2[1:5]<=key[1:5] and key[6:]==key2[6:]:#以key为基准
            if key in ans:
                ans[key]=ans[key]+text[key2]
            else:
                ans[key]=text[key2]
print(ans)
with open(path_to+"tags_data.json","w") as file_obj:
    json.dump(ans,file_obj,ensure_ascii=False)