
本项目通过在[东方财富-行情中心](http://quote.eastmoney.com/center/)、[同花顺-行情中心](http://q.10jqka.com.cn/thshy/)爬取相关数据
爬虫
asharestock.py爬取东方财富每只股每日最新数据
industryK.py爬取同花顺各行业的k线数据，每个行业约130天
stockK.ipynb爬取东方财富上海及深圳每只股的k线数据，每只股均是从发售日开始的。
其中北京的因为页面改版为图片，无法获取
存储
ashareSave.py创建stock表及添加数据
industryK.py创建industrydate表及添加每日最新数据，第一次上传把==改为!=
stockK.ipynb保存数据到stock
定时运行
timestart.ipynb 每天晚上就定时运行
量化分析
candlestick chart.ipynb 近100天的k线数据
MACD.ipynb 近100天的MACD指标
OBV.ipynb 近100天的OBV指标