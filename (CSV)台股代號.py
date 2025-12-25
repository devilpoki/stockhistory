import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

# 定義抓取資料的函式
def fetch_data(url):
    # 送出GET請求
    response = requests.get(url)
    response.encoding = 'big5'  # 設置編碼
    soup = BeautifulSoup(response.text, 'html.parser')

    # 打印HTML，檢查表格結構
    # print(soup.prettify())  # 可以檢查表格的結構

    # 找到股票資料表格
    table = soup.find('table', class_='h4')

    # 檢查是否成功找到表格
    if table:
        print("Table found!")
    else:
        print("Table not found!")

    # 取得表格的標題
    headers = [header.get_text(strip=True) for header in table.find_all('th')]

    # 如果標題為空，則可能要手動處理
    if not headers:
        print("No headers found, trying another way to extract columns...")
        # headers = ['Column{}'.format(i) for i in range(1, 11)]  # 假設最多10列
        headers = ["頁面編號","國際證券編碼","有價證券代號","有價證券名稱","市場別","有價證券別","產業別","公開發行/上市(櫃)/發行日","CFICode","備註"]

    # 取得表格的每一行資料
    rows = []
    for row in table.find_all('tr')[1:]:  # 跳過表頭
        cols = row.find_all('td')
        if len(cols) > 1:
            row_data = [col.get_text(strip=True) for col in cols]
            rows.append(row_data)

    # 返回DataFrame
    return pd.DataFrame(rows, columns=headers)

# 網址1
url1 = 'https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=1&issuetype=1&industry_code=&Page=1&chklike=Y'

# 網址2
url2 = 'https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=2&issuetype=4&industry_code=&Page=1&chklike=Y'

# 抓取資料
df1 = fetch_data(url1)
df2 = fetch_data(url2)

# 刪除第一,二欄（頁面編號,國際證券編碼)
df1 = df1.iloc[:, 2:]
df2 = df2.iloc[:, 2:]

# 🔑 若欄位超過 8，保留前 8 欄
df1 = df1.iloc[:, :7]
df2 = df2.iloc[:, :7]

# 合併兩個DataFrame
df_combined = pd.concat([df1, df2], ignore_index=True)

# 顯示合併後的DataFrame
print(df_combined)

df_combined.to_csv('D:\\TWSE 台股\\台股股票代號.csv', index=False, encoding='utf-8-sig')
df_combined.to_csv('D:\\TWSE 台股\\台股股票代號.txt', sep=',', index=False, encoding='utf-8-sig')

