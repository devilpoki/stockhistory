import requests
import pandas as pd
import numpy as np
import csv

# 一些參數：
# TYPEK => 市場別
# sii>上市
# otc>上櫃
# rotc>興櫃
# pub>公開發行

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}

def get_資產負債表(TYPEK, year ,season):
    url = 'https://mops.twse.com.tw/mops/web/ajax_t163sb04'
    parameter =  {'encodeURIComponent':1, 'step':1, 'firstin': '1', 'off':1, 'TYPEK': TYPEK, 'year': str(year), 'season': str(season)}    
    
    res = requests.post(url, data= parameter, headers = headers )    
    res.encoding = 'utf8'
    
    if TYPEK == 'sii':
        df = pd.read_html(res.text)[3]
        df = df.replace('--','0')            
        
    else:
        df = pd.read_html(res.text)
        df = df.replace('--','0') 
        df = df[2]
        # df = pd.concat([df.squeeze() for df in dfo_subset] , ignore_index = True)
        
    
    df.insert(1, '年度', year)
    df.insert(2, '季別', season)
    return df

data = get_資產負債表('sii', 112,1)
for i in range(112, 110, -1):
    抓取= get_資產負債表('sii', i , 1)
    data = pd.concat([data, 抓取])
    print(data)

     
data.to_csv('d:/TWSE 台股/資產負債表/資產負債表.csv' ,  index=False, encoding= 'utf-8-sig')