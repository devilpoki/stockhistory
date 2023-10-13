import pandas as pd
import requests
from io import StringIO
from datetime import datetime


year = 112
month = 8
    
# 假如是西元，轉成民國
if year > 1990:
    year -= 1911

# 上市
siiurl = 'https://mops.twse.com.tw/nas/t21/sii/t21sc03_'+str(year)+'_'+str(month) + '.html'
if year <= 98:
    siiurl = 'https://mops.twse.com.tw/nas/t21/sii/t21sc03_'+str(year)+'_'+str(month)+'.html'
# 上櫃   
otcurl = 'https://mops.twse.com.tw/nas/t21/otc/t21sc03_'+str(year)+'_'+str(month) + '.html'
if year <= 98:
    otcurl = 'https://mops.twse.com.tw/nas/t21/otc/t21sc03_'+str(year)+'_'+str(month)+'.html'        

    
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}

siires = requests.get(siiurl , headers = headers)
otcres = requests.get(otcurl , headers = headers)
siires.encoding = 'big5hkscs'
otcres.encoding = 'big5hkscs'


dfs = pd.read_html(StringIO(siires.text), encoding='big5hkscs')
dfo = pd.read_html(StringIO(otcres.text), encoding='big5hkscs')

siidf = pd.concat([df for df in dfs if df.shape[1] <= 11 and df.shape[1] > 5])
otcdf = pd.concat([df for df in dfo if df.shape[1] <= 11 and df.shape[1] > 5])

# 上市
if 'levels' in dir(siidf.columns):
    siidf.columns = siidf.columns.get_level_values(1)
else:
    siidf = siidf[list(range(0,10))]
    column_index = siidf.index[(siidf[0] == '公司代號')][0]
    siidf.columns = siidf.iloc[column_index]
    
siidf['當月營收'] = pd.to_numeric(siidf['當月營收'], 'coerce')
# siidf = siidf[~siidf['當月營收'].isnull()]
siidf = siidf[~(siidf.isin(['合計', '總計']))].dropna()

# 上櫃
if 'levels' in dir(otcdf.columns):
    otcdf.columns = otcdf.columns.get_level_values(1)
else:
    otcdf = otcdf[list(range(0,10))]
    column_index = otcdf.index[(otcdf[0] == '公司代號')][0]
    otcdf.columns = otcdf.iloc[column_index]
    
otcdf['當月營收'] = pd.to_numeric(otcdf['當月營收'], 'coerce')
siidf = siidf[~siidf['當月營收'].isnull()]
otcdf = otcdf[~(otcdf.isin(['合計', '總計']))].dropna()

# 上市 上櫃合併
frame = [siidf, otcdf]
df = pd.concat(frame)

# 新增資料年月欄位
if len(str(month)) == 1:
    month = '0' + str(month)
else:
    month
    
datamonth = str( int(1911) + year) + '-' + str(month) + '-' + str('01')
df.insert( 0 , '資料年月', datamonth)

df.to_csv('D:/TWSE 台股/營收/' +  datamonth  + '.csv', index = False, encoding= 'utf-8-sig')