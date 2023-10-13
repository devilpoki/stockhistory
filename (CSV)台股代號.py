import requests
import pandas as pd
import random
import time
import csv

# 上市
urlmark1 = "https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=1&issuetype=1&industry_code=&Page=1&chklike=Y"

# 上櫃
urlmark2 = 'https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=2&issuetype=4&industry_code=&Page=1&chklike=Y'

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}

res1 = requests.get(urlmark1 , headers = headers)
res2 = requests.get(urlmark2 , headers = headers)
#print(res.text)

df1 = pd.read_html(res1.text)[0]
#print(df1)
df1= df1.drop([0,1,5,8,9],axis = 1)
df1.columns = df1.iloc[0]
df1 = df1.iloc[1:]

# df = df.set_index("有價證券代號")

######
df2 = pd.read_html(res2.text)[0]
df2= df2.drop([0,1,5,8,9],axis = 1)
df2.columns = df2.iloc[0]
df2= df2.iloc[1:]
# print(df2)

# 兩個datafram 合併
frames = [df1, df2]
df = pd.concat(frames)
# print(df)

df.to_csv('D:/TWSE 台股/台股股票代號.csv', index=False, encoding= 'big5hkscs')

######  Goodinfo 現金流量網址 +  股號

stock_num = df['有價證券代號']
urlbase  = 'https://goodinfo.tw/tw/StockCashFlow.asp?STOCK_ID='
urls = [urlbase + str(stock) for stock in stock_num]


# 生成一個隨機的秒數，範圍可以自行調整
# random_seconds = random.randint(3, 9)  # 生成0到59之間的隨機整數
# time.sleep(random_seconds)
# print(urls)


# 將Goodinfo 網址加上 股票代號 urls 結果寫成csv
csv_file_name = 'D:/TWSE 台股/Goodinfo網址加股票代號.csv'
with open(csv_file_name, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerows([[url] for url in urls])
    


#===========================================  csv 讀出股號
# import csv
# from itertools import islice

# fn = 'd:/TWSE 台股/台股股票代號.csv'

# with open(fn) as csvfile:
#     csvReader = csv.reader(csvfile)
#     listReader = list(csvReader)
    
# for row in islice(listReader, 1, None):
#     print(row[0])