import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from pymongo import MongoClient
import os
from urllib.request import urlretrieve
import mysql.connector
import pymysql
import base64


# 商品
_id = 1

# set mongodDB connection
engine = "mongodb://localhost:27017"
client = MongoClient(engine)
db = client.wine
tb = db.new1_re_wine
cu = tb.find()

# set sql connection


mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    passwd="pwd",
    database="amazon"
)

mycursor = mydb.cursor()

x = 23
for i in cu:
    fp = open("/Users/wujinxuan/Documents/python/picture/{}.jpg".format(x), 'rb')
    img = fp.read()
    fp.close()
    sql = (
        "insert into amazon_produce(produce_no,picture_url,price,produce_name,produce_url,category_no) "
        "value(%s,%s,%s,%s,%s,%s)")
    realprice = float(i['price'].strip('$'))
    con = (str(_id), img, realprice, i['produce_name'], "", 4)
    mycursor.execute(sql, con)
    _id += 1
    x += 1
    mydb.commit()

mycursor.close()
mydb.close()


# 推薦商品

db = client.wine
tb = db.new_wine
cu = tb.find()
re_id = 1
x = 267
for i in cu:
    try:
        fp = open("/Users/wujinxuan/Documents/python/picture/{}.jpg".format(x), 'rb')
        img = fp.read()
        fp.close()
        sql = (
            "insert into recommend_produce(re_produce_no,ori_produce,recommend_produce,recommend_produce_picture_url,"
            "recommend_produce_price,recommend_produce_url) value(%s,%s,%s,%s,%s,%s)")
        realprice = float(i['recommend_produce_price'].strip('$'))
        con = (re_id, i['ori_produce'], i['recommend_produce'], "", realprice, img)
        mycursor.execute(sql, con)
        re_id += 1
        x += 1
        mydb.commit()
    except:
        print('error')

#關閉mysql mongo
mycursor.close()
mydb.close()
