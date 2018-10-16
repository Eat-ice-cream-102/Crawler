import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from pymongo import MongoClient

headers = {
    'Cookie': 'x-wl-uid=1D3mI3DGkEMlPJnihWyg+tU0wPqJJAoodFiRsEVfdsmjRc0EFu6FI9YY4jw82qDJVOlHewN3z43Y=; skin=noskin; '
              'csm-hit=tb:s-QQGG2FVXR2N2MS4R0SJS|1534918092554&adb:adblk_no; ubid-main=132-2781961-7637055; '
              'session-id=139-9315588-3367423; session-id-time=2082787201l; '
              'session-token="ZPmRT82fS2nzNs8EcYFQ80ytvCQjd/kUgnWiNW8lSZe9pBAOvx5cynLL8Nn7t1ZfbPtxLf2uDBBmoCjqbOXvm7muS'
              'mpWSYdIRRosBsP+mkKLonWB0lekjkPbnDMunIhqAZa3INKyBQG9lSbFpkfdH7bMM6Jat+qq1owZoIaRbMURurWejf8X80Y2pKeVSOerr'
              'MnjwbKPcRqcTUgy7gx4yPZ96ET98VoNhMyhm6gcIg4FTtOBA4OArnBuM/5bN8Tpvs5YdhgVoCY="',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/57.0.2987.133 Safari/537.36'
}


#set mongodDB connection
engine = "mongodb://localhost:27017"
client = MongoClient(engine)
db = client.clock

tb = db.clockdata
tb_reclock = db.re_clockdata

#爬蟲
ori_url = 'https://www.amazon.com'
url = "https://www.amazon.com/s/ref=nb_sb_noss_1?url=search-alias%3Daps&field-keywords=alarm+clock&rh=" \
     "i%3Aaps%2Ck%3Aalarm+clock"
res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, 'lxml')

urls = []
for i in soup.select(' .s-access-detail-page'):
    num = i.get('href').find("https://www.amazon.com")
    if num == -1:
        append_amazon = "https://www.amazon.com{}".format(i.get('href'))
        urls.append(append_amazon)
    else:
        urls.append(i.get('href'))

data = []
data_detail = []
for i in urls[1:2]:
    name = dict()
    res = requests.get(i, headers=headers)
    soup = BeautifulSoup(res.text, 'lxml')
    findname = soup.select('.a-list-item .a-declarative  .imgTagWrapper .a-dynamic-image')[0]
    # produce name
    name['produce_name'] = findname.attrs['alt']
    # picture url
    src = findname.attrs['data-a-dynamic-image']
    if len(src) > 2:
        picture_url = src.split('\"')
        name['picture_url'] = picture_url[1]
    else:
        name['picture_url'] = ""
    # price
    price = soup.select('.a-color-price')[0].text
    st_price = price.strip()
    name['price'] = st_price
    # produce url
    name['produce_url'] = i
    data.append(name)
    recommend_pages = dict()
    for j in soup.select('.a-carousel .a-carousel-card')[0:10]:
        try:
            recommend_pages["ori_produce"] = findname.attrs['alt']
            recommend_pages["recommend_produce"] = j.select('.a-link-normal')[0].attrs['title']
            rnum = j.select('.a-link-normal')[1].get('href').find("https://www.amazon.com")

            if rnum == -1:
                append_amazon = "https://www.amazon.com{}".format(j.select('.a-link-normal')[1].get('href'))
                recommend_pages["recommend_produce_url"] = append_amazon
            else:
                recommend_pages["recommend_produce_url"] = j.select('.a-link-normal')[1].get('href')
            recommend_pages["recommend_produce_picture_url"] = j.select('.a-link-normal .a-dynamic-image')[0].get('src')
            recommend_pages["recommend_produce_price"] = j.select('.a-row  .a-color-price')[0].text
        except:
            print('error')
        print(data_detail)
        data_detail.append(recommend_pages)
        df_de = pd.DataFrame(data_detail)
        tb_reclock.insert_many(df_de.to_dict(orient='record'))
    df = pd.DataFrame(data)
    df_de = pd.DataFrame(data_detail)
    #insert to mongo
    tb.insert_many(df.to_dict(orient='record'))

#clear
cu = tb_reclock.find()
df = pd.DataFrame(list(cu))
# 刪除空直
df = df.dropna()
# 刪除重複
df = df.drop_duplicates(["ori_produce", "recommend_produce"])
tb_clear_shoes.insert_many(df.to_dict(orient='record'))

#關閉 mongo
mycursor.close()