import pandas as pd
import requests as req
import numpy
from datetime import datetime


def getTW_IR():
    interestRateTable = pd.read_html("https://tradingeconomics.com/taiwan/interest-rate")
    interestRateTable = interestRateTable[0]
    # string to datetime
    interestRateTable['Calendar'] = pd.to_datetime(interestRateTable['Calendar'], format="%Y-%m-%d")

    # 只留下 Calendar 與 Actual 欄位
    columns = ['Calendar', 'Actual']
    interestRateTable = interestRateTable[columns]

    # 把有空值的row 拿掉
    interestRateTable = interestRateTable.dropna(axis=0)

    # 把 interest rate 轉為數值
    interestRateTable['Actual'] = interestRateTable['Actual'].str.replace("%", "", regex=True)
    interestRateTable['Actual'] = interestRateTable['Actual'].astype(float)

    # sort datetime 降冪 時間最大的在最上面, 要記得ignore index 否則index 不會變動
    # 如果不要更動index的話就不要加ignore_index
    interestRateTable = interestRateTable.sort_values('Calendar', axis=0, ascending=False, ignore_index=True)

    TW_IR = interestRateTable['Actual'][0]

    print('TW_IR=' + str(TW_IR))


def getHK_IR():
    url = 'https://api.hkma.gov.hk/public/market-data-and-statistics/daily-monetary-statistics/daily-figures-interbank-liquidity'
    r = req.get(url)
    result = r.json()
    HK_IR = result['result']['records'][0]['disc_win_base_rate']
    HK_IR = str(HK_IR)
    print('HK_IR=' + HK_IR)


getTW_IR()
getHK_IR()
