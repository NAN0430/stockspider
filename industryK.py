
'''
数据来源：同花顺-行情中心
http://q.10jqka.com.cn/thshy/detail
'''

from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time
import csv
import re
import time
import json

daytime = time.strftime("%Y.%m.%d", time.localtime())
print(daytime)

def get_cookie():
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(options=options)
        url = "http://q.10jqka.com.cn/thshy/"
        driver.get(url)
        # 获取cookie列表
        cookie = driver.get_cookies()
        return(cookie)
        driver.close()
        return cookie[0]['value']

def get_page_detail(url):
       headers = {
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
           'Referer': 'http://q.10jqka.com.cn/thshy/detail',
           'Cookie': 'v={}'.format(get_cookie())
       }
       try:
           response = requests.get(url, headers=headers)
           print(response)
           if response.status_code == 200:
               return response.text.encode('utf-8')
           return None
       except RequestException:
           print('请求页面失败', url)
           return None

def get_industry_list(url):
        html = get_page_detail(url)
        return (html)

def get_industry_codes(codes):
        instury_index_url = 'http://q.10jqka.com.cn/thshy/'
        html = get_industry_list(instury_index_url)
        bs = BeautifulSoup(html, "html.parser")
        list = bs.find('tbody').find_all("a", target="_blank")  
        print(type(list))
        print(len(list))
        industry =[["行业","链接"]]
        for line in list:
            industry.append([line.get_text(),str(line.get('href'))])
            href = str((line.get('href')))
            if (href.find('thshy') == -1) is False:
                ret = href.split("/")[-2]
                codes.append(ret)
        with open("industrylink.csv","w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(industry)
        return codes

def get_one_data(code_industry):
        url = 'http://d.10jqka.com.cn/v4/line/bk_' + code_industry + '/01/last.js'
        r = get_page_detail(url).decode('utf8')
        d = re.compile('"data":".*?"')
        data = re.findall(d,r)[0]
        data = data.replace("\"","").replace("data","").replace(":","")
        data = data.replace(",,,,0","").replace(",,,,,","")
        data1 = data.split(";")
        data2 = []
        for da in data1:  
            da1 = da.split(",")
            da1.extend([code_industry])
            data2.append(da1)
        return data2

def get_all_data(codes):
   # 保存文件
    daytime = time.strftime("%Y.%m.%d", time.localtime()) 
    with open("industrystock"+daytime+".csv","a") as csvfile:
        for code in codes:
            data = get_one_data(str(code))
            writer = csv.writer(csvfile)
            writer.writerows(data)

def main():
    headers = [['日期','开盘价','最高价','最低价',"收盘价",'成交量','未知','行业编号']]
    with open("industrystock"+daytime+".csv","a") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(headers)
    codes = []
    get_industry_codes(codes)
    get_all_data(codes)


main()


