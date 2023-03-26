import time

import pandas as pd
import requests
from bs4 import BeautifulSoup
import sys, json

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

keyword = '電視'
page = 25

Chrome_driver_path = r'/Users/bonniefu/Desktop/chromedriver 2.exe'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('User-Agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36"')
driver = webdriver.Chrome(executable_path=Chrome_driver_path,chrome_options=chrome_options)

# momo 網站需用selenium 抓取, request 抓取不到資料
def getMomoTVList(keyword,page):
    df = pd.DataFrame()
    for i in range (1,page+1):
        url ='https://www.momoshop.com.tw/search/searchShop.jsp?keyword='+keyword+'&searchType=1&curPage='+str(i)+'&_isFuzzy=0&showType=chessboardType'
        driver.get(url)
        # beautiful soup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        # 找到指定的ul元素
        ul = soup.find('ul', {'class': 'clearfix'})
        for li in ul.find_all('li'):
            # 找到li元素下的h3和span元素
            h3 = li.find('h3', {'class': 'prdName'})
            price = li.find('span', {'class': 'price'})

            # 提取元素的文本內容
            productName = h3.text.strip()
            price_text = price.text.strip()
            newdf = pd.DataFrame({'prodName':productName,'price':price_text}, index=[0])
            df = pd.concat([df,newdf], ignore_index=True)
            df.to_csv('momo_output.csv', index=False)


# ETMall
# ETmall： pageIndex = 當前頁面-1 (要從0開始)
def getETMallTVList(keyword,page):
    ETMallDf = pd.DataFrame()
    for i in range(0,page+1):
        ETMall_url='https://www.etmall.com.tw/Search?keyword='+ keyword + '&PageIndex='+ str(i)
        driver.get(ETMall_url)
        ETMall_soup = BeautifulSoup(driver.page_source, "html.parser")

        ul = ETMall_soup.find('div', {'id': 'SearchProductList'})

        for li in ul.find_all('li'):
            if li is not None:
                productName = li.find('p', {'class': 'n-name'})
                priceList = li.find_all('span', {'class': 'n-price--16'})
                if productName is not None:
                    productName = productName.text.strip()
                price = []
                realprice = ''
                for i in priceList:
                    price.append(i.text.strip())
                if price:
                    realprice = price[1]
                newETMalldf = pd.DataFrame({'prodName': productName, 'price': realprice}, index=[0])
                ETMallDf = pd.concat([ETMallDf,newETMalldf], ignore_index=True)

    ETMallDf = ETMallDf.dropna(subset=['prodName'])
    ETMallDf.to_csv('ETMall_output.csv',index=False)

getMomoTVList(keyword,page)
getETMallTVList(keyword,page)