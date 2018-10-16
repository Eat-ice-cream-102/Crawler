import re
import pandas as pd
from pymongo import MongoClient
import os
from urllib.request import urlretrieve
import mysql.connector
import pymysql
import base64


#set mongodDB connection
engine = "mongodb://localhost:27017"
client = MongoClient(engine)
db = client.wine

tb_wine = db.new1_re_wine
cu = tb_wine.find()
url = []
for i in cu:
    a = i['recommend_produce_picture_url']
    url.append(a)

for i in url:
    local = os.path.join('/Users/nola/Documents/python/picture/%s.jpg' %x)
    urlretrieve(i, local)
    x += 1