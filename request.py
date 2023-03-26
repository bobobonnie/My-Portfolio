import requests
import pandas as pd
import json
from bs4 import BeautifulSoup
import sys, json
import urllib.request as ur
import requests
import re
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

keyword = '電視'
page = 50
df_all = pd.DataFrame()
# PCHome 取得該購物網站上 關鍵字為電視 的清單
def getPCHomeTVList(keyword,page):
    df_all = pd.DataFrame()
    for i in range(1,page):
        url = 'https://ecshweb.pchome.com.tw/search/v3.3/all/results?q='+keyword+'&page=' + str(i)
        res = requests.get(url)
        data = res.json()
        data = data['prods']
        df = pd.read_json(json.dumps(data))
        df = df[['name', 'price']]
        df = df.rename(columns={'name': 'prodName'})

        df_all = pd.concat([df_all,df])
        df_all.to_csv('output.csv', index=False)


getPCHomeTVList(keyword,page)


