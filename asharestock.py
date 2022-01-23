


'''
数据来源：东方财富网-行情中心
http://quote.eastmoney.com/center
'''

import requests
import re
import pandas as pd
import json
import csv
import time


daytime = time.strftime("%Y.%m.%d", time.localtime()) 
print(daytime)


#用get方法访问服务器并提取页面数据
def getHtml(page):
    url = "http://22.push2.eastmoney.com/api/qt/clist/get?cb=jQuery1124047020254114968596_1642468382421&pn="+str(page)+"&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152"
    headers = {
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
        "Host": "22.push2.eastmoney.com",
        "Connection": "keep-aliv",
    }
    while True:
        try:
            r = requests.get(url,headers)
            d = re.compile('"data":({.*)}\);')
            data = re.findall(d,r.text)[0]
            data1 = json.loads(data)
            return data1['diff']
        except:
            return False

#获取单个页面股票数据
def getOnePageStock(page):
    data = getHtml(page)
    result = []
    count = 1
    
    for line in data:
        result.append([line['f12'],line['f14'],daytime,line['f2'], line['f3'],
                       line['f4'],line['f5'],line['f6'],line['f7'],
                       line['f15'],line['f16'],line['f17'],line['f18'],
                       line['f10'],line['f8'],line['f9'],line['f23'],
                       line['f20'],line['f21']
                      ])
        count+=1
    #print(result)
    return result

def saveOnePage(page,data):
   # 保存文件
    with open("asharestock"+daytime+".csv","a") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
    
    
    return True

def main():
    page = 1
    #自动爬取多页，并在结束时停止
    headers = [['股票代码', '名称','日期','收盘价', '涨跌幅',
               '涨跌额','成交量','成交额','振幅',
               '最高','最低','今开','昨收',
               '量比','换手率','市盈率','市净率',
               '总市值','流通市值']];
    with open("asharestock"+daytime+".csv","a") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(headers)
    while True: 
        if getHtml(page)!= False:
            d = getOnePageStock(page)
            saveOnePage(page,d)
            print("已加载第"+str(page)+"页")
            page +=1
        else:
            break


main()




