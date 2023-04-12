import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# IMDB website started from 1990

# Read IMDB data csv file
df = pd.read_csv('IMDB Top 250 Movies.csv')

# create global dataframe
dfGenre = pd.DataFrame()
groupbyGenredf = pd.DataFrame()
dfCertificate = pd.DataFrame()

# 檢查 dataframe 中是否有 null 的值 => False, the usability for this data is 10.0
print(df.isnull().values.any())

# 把數字顯示小數位後兩位, 並關掉科學記號
pd.set_option('display.float_format', lambda x: '{:.2f}'.format(x))


def columnStrip():
    # 針對string欄位多餘的空白做處理
    df['name'] = df['name'].str.strip()
    df['genre'] = df['genre'].str.strip()
    df['certificate'] = df['certificate'].str.strip()


# [year]
def checkYear():
    # 檢查 year 欄位是否皆為數字型態
    df['year'] = df['year'].astype(str)
    year_is_numeric = df['year'].str.isnumeric()
    year_isNot_numeric = [df[~year_is_numeric]]

    # 顯示結果
    print(year_isNot_numeric)

    # 觀察一下數據 理論上來說年份都要是數字 且是小於現在時間的年份
    # 確認時間年份值區間
    print(df['year'].max())
    print(df['year'].min())

    # 檢查年份欄位是否皆為四位數
    df['year_is_four_digits'] = df['year'].str.match(r'^\d{4}$')
    notFourDigit = df[df['year_is_four_digits'] == False]

    # 顯示結果
    print(notFourDigit)


def movieByYearVisualization():
    # 按照年份排序
    dfYear = df.sort_values(by=['year'])
    # 用 seaborn 畫圖比 matplotlib 好看
    sns.histplot(data=dfYear, x="year", binwidth=5, kde=True, shrink=0.8).set(
        title='Number of Movies in IMDB Top 250 by Year', xlabel='Year', ylabel='Number of Movies')
    # 成功的畫出圖代表該欄位所有的值都是數字, 且介於1921~2022 之間


# [rating]
def checkRating():
    # 檢查rating 是否皆為 float 型態
    try:
        df['rating'] = df['rating'].astype(float)
        print("所有值皆為float類型")
    except ValueError:
        print("存在非float類型的值")

    top_movies = df.nlargest(3, ['rating'])
    top_movies = top_movies[['name', 'rating']]

    # 顯示結果
    print(top_movies)


# [genre]
def generateGenredf():
    global df
    print(df.groupby(['genre'])['name'].count().size)
    # 總共有 104 種組合 每個電影最多三個分類
    # 把分類分成三個欄位
    global dfGenre
    genredf = df['genre'].str.split(',', expand=True)
    genredf.columns = ['genre1', 'genre2', 'genre3']

    # 合併到原dataframe
    df = df.merge(genredf, how='inner', left_index=True, right_index=True)

    # melt data
    dfGenre = pd.melt(df, id_vars=['name', 'rating', 'box_office'], value_vars=['genre1', 'genre2', 'genre3'],
                      var_name='genre', value_name='type')

    # 去除 type 為空的行
    dfGenre['type'] = dfGenre['type'].astype(str)
    dfGenre = dfGenre.replace('None', '')
    dfGenre = dfGenre[dfGenre['type'] != '']
    dfGenre = dfGenre
    # 顯示結果
    print(dfGenre)


def visualizeGenre():
    # genre / rating relation
    global dfGenre
    sns.countplot(dfGenre, y='type', order=dfGenre["type"].value_counts().index)


def genreHandling():
    global groupbyGenredf
    # df group by Genre
    dfGenre.loc[dfGenre['box_office'].str.endswith(")"), 'box_office'] = dfGenre['box_office'].str.replace(
        r' \(estimated\)', "", regex=True)
    dfGenre.loc[dfGenre['box_office'] == "Not Available", 'box_office'] = 0
    dfGenre['box_office'] = dfGenre['box_office'].astype('float64')

    groupbyGenredf = dfGenre.groupby(['type'])['box_office'].mean().reset_index()
    groupbyGenredf = groupbyGenredf.sort_values('box_office', ascending=False)


def visualizingGenre():
    global groupbyGenredf
    sns.barplot(groupbyGenredf, y='type', x='box_office').set(title='Mean Box Office by Movie Type',
                                                              xlabel='Mean Box Office')
    # plt.ticklabel_format(style='plain', axis='x')


# [certificate]

# 原始版 分級
# print(df['certificate'].unique())
# G（大眾級，所有人皆可觀看）
# PG（普通級，建議兒童在父母陪伴下觀看）
# PG-13（輔導級，十三歲以下需要有父母陪同觀看）
# R（十七歲以下需要有父母或監護人陪同觀看）=> 與台灣制度不同,美國限制級影片, 對於17歲以下只要有成人陪同即可觀賞

# Approved, Passed, GP, TV-PG = PG
# 13+ = PG-13
# 18+, TV-MA, X = R
# not rated, unrated and not available ==> the movies were not submitted for rating

def certificateHandling():
    global dfCertificate
    df.loc[df['certificate'] == 'Approved', 'certificate'] = 'PG'
    df.loc[df['certificate'] == 'Passed', 'certificate'] = 'PG'
    df.loc[df['certificate'] == 'GP', 'certificate'] = 'PG'
    df.loc[df['certificate'] == 'TV-PG', 'certificate'] = 'PG'
    df.loc[df['certificate'] == '13+', 'certificate'] = 'PG-13'
    df.loc[df['certificate'] == '18+', 'certificate'] = 'R'
    df.loc[df['certificate'] == 'TV-MA', 'certificate'] = 'R'
    df.loc[df['certificate'] == 'X', 'certificate'] = 'R'
    print(df['certificate'].unique())
    dfCertificate = df.drop(df[(df['certificate'] == 'Not Rated') | (df['certificate'] == 'Not Available') | (
                df['certificate'] == 'Unrated')].index)


def visualizingCertificate():
    colors = ['#f94144', '#f9844a', '#f9c74f', '#90be6d']
    sns.countplot(data=dfCertificate, x="certificate", order=dfCertificate["certificate"].value_counts().index,
                  palette=colors).set(title='Certificate Count', xlabel='Certificate')


# [run_time]

def runTimeHandling():
    global df
    # 將 “Ｘ時Ｘ分” 的格式轉換為 “Ｘ分鐘”
    df.loc[df['run_time'] == 'Not Available', 'run_time'] = '0h 0m'
    df.loc[~df['run_time'].str.contains("h"), 'run_time'] = '0h ' + df['run_time']
    df.loc[~df['run_time'].str.contains("m"), 'run_time'] = df['run_time'] + ' 0m'
    runtimedf = df['run_time'].str.split('h ', expand=True)
    runtimedf.columns = ['hour', 'min']
    runtimedf['hour'] = runtimedf['hour'].str.replace('h', '')
    runtimedf['min'] = runtimedf['min'].str.replace('m', '')

    # 注意有些時間沒有分鐘數的 一定要補上0 否則none type 這裡會無法做加總
    runtimedf['duration'] = runtimedf['hour'].astype(int) * 60 + runtimedf['min'].astype(int)

    df = df.merge(runtimedf, how='inner', left_index=True, right_index=True)


def runTimeVisualization():
    sns.histplot(data=df, x='duration', bins=20).set(title='Duration Count', xlabel='Duration (min)')


def runTimeScatterPlot():
    sns.scatterplot(data=df, x='rating', y='duration')


#
# [budget]
# 要確定這個欄位是否都為數值 （用isnumeric 查該欄位裡面的每一個str中的每一個值都是數值 ）
#
def budgetHandling():
    nonNumericalBudget = df.loc[:, ('budget', 'name')]
    nonNumericalBudget['isNumeric'] = df['budget'].str.isnumeric()
    # print(nonNumericalBudget[nonNumericalBudget['isNumeric']==False])

    # 要處理的數據 "$", "幣別", “not available”
    df['budget'] = df['budget'].str.replace("$", "", regex=True)

    # 不同幣別的數據只有三筆 所以這裡簡單查詢該年份的幣別轉換
    # 如果有很多不同幣別的 我會另外拉一張表 做年份跟匯率轉換
    df['exchange rate'] = 1
    df.loc[df['budget'].str.startswith("RF "), 'exchange rate'] = 1.3664
    df.loc[df['budget'].str.startswith("EM "), 'exchange rate'] = 0.14
    df.loc[df['budget'].str.startswith("RF "), 'budget'] = df['budget'].str.replace("RF ", "")
    df.loc[df['budget'].str.startswith("EM "), 'budget'] = df['budget'].str.replace("EM ", "")
    df.loc[df['budget'] == "Not Available", 'budget'] = 0
    df['budget'] = df['budget'].astype(float) * df['exchange rate']


# [box_office]

def boxOfficeHandling():
    # brackets 在字串中會被視為是符號 所以要加上 escape sequence "\" 在該符號前面
    df.loc[df['box_office'].str.endswith(")"), 'box_office'] = df['box_office'].str.replace(r' \(estimated\)', "",
                                                                                            regex=True)
    df.loc[df['box_office'] == "Not Available", 'box_office'] = 0

    # 因為前面將型態轉 str 現在要轉回來 float
    df['box_office'] = df['box_office'].astype('float64')
    TopBoxOffice = df.nlargest(3, ['box_office'])
    TopBoxOffice = TopBoxOffice[['name', 'box_office']]
    print(TopBoxOffice)


# [cast]
def castHandling():
    cast = ','.join(df['casts'])
    # comma separated string to list
    cast = cast.split(",")
    castdf = pd.DataFrame(cast)
    castdf.columns = ['cast']
    castdf = castdf.groupby(['cast'])['cast'].count().sort_values(ascending=False)
    castdf.to_csv('Cast.csv')


# [directors]
def directorHandling():
    director = ','.join(df['directors'])
    director = director.split(",")
    directordf = pd.DataFrame(director)
    directordf.columns = ['director']
    directordf = directordf.groupby(['director'])['director'].count().sort_values(ascending=False)
    directordf.to_csv('Director.csv')


# [writer]
def writerHandling():
    writer = ','.join(df['writers'])
    # comma separated string to list
    writer = writer.split(",")
    writerdf = pd.DataFrame(writer)
    writerdf.columns = ['writer']
    writerdf = writerdf.groupby(['writer'])['writer'].count().sort_values(ascending=False)
    writerdf.to_csv('Writer.csv')


# [gross profit margin]
def GrossProfitMargin():
    try:
        df['box_office'] = df['box_office'].astype(float)
        print("box_office所有值皆為float類型")
    except ValueError:
        print("box_office存在非float類型的值")
    try:
        df['budget'] = df['budget'].astype(float)
        print("budget所有值皆為float類型")
    except ValueError:
        print("budget存在非float類型的值")

    dfGorssProfitdf = df[(df['box_office'] != 0) & (df['budget'] != 0)]

    # show how may rows left
    # print(len(dfGorssProfitdf))
    dfGorssProfitdf2 = dfGorssProfitdf.copy()

    # find out hhe most money making film in IMDB top 250
    dfGorssProfitdf2.loc[:, 'GrossProfit'] = (dfGorssProfitdf['box_office'] - dfGorssProfitdf['budget']) / \
                                             dfGorssProfitdf['box_office']
    topGorssProfit = dfGorssProfitdf2.nlargest(3, ['GrossProfit'])
    topGorssProfit = topGorssProfit[['name', 'GrossProfit']]
    print(topGorssProfit)


columnStrip()
checkYear()

checkRating()
generateGenredf()
genreHandling()
certificateHandling()
runTimeHandling()
budgetHandling()
boxOfficeHandling()
castHandling()
directorHandling()
writerHandling()
GrossProfitMargin()

df.to_csv('ProcessedData.csv')

# [visualization] Please execute one at a time
# movieByYearVisualization()
# visualizeGenre()
# visualizingGenre()
visualizingCertificate()
# runTimeVisualization()
# runTimeScatterPlot()
plt.show()
