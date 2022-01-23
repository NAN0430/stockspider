

import pymysql
import csv
import pandas as pd
import time

conn= pymysql.connect(host='127.0.0.1',
                      port=3306,
                      user='root',
                      password="111",
                      charset='utf8')
cursor = conn.cursor()


# #创建数据库stockDataBase
# sqlSentence1 = "create database stockDataBase"
# cursor.execute(sqlSentence1)#选择使用当前数据库


sqlSentence2 = "use stockDataBase;"
cursor.execute(sqlSentence2)



daytime = time.strftime("%Y.%m.%d", time.localtime()) 
print(daytime)

fileName=("asharestock"+daytime+".csv")
data = pd.read_csv(fileName, encoding="utf8")
#创建数据表，如果数据表已经存在，会跳过继续执行下面的步骤print('创建数据表stock_%s'% fileName)
try:
    sqlSentence3 = "create table stock"  + "(股票代码 VARCHAR(10),名称 VARCHAR(10),日期 date,收盘价 float,涨跌幅 float,涨跌额 float,成交量 bigint,成交额 bigint,振幅 float, 最高价 float,最低价 float,昨日收盘价 float,开盘价 float,量比 float,换手率 float,市盈率 float,市净率 float,总市值 bigint,流通市值 bigint)"
    cursor.execute(sqlSentence3)
except Exception as e:
    print(e)


#迭代读取表中每行数据，依次存储
print('正在存储')
length = len(data)
for i in range(0, length):
    record = tuple(data.loc[i])
    #插入数据语句
    try:
        sqlSentence4 = "insert into stock" + "(股票代码,名称,日期, 收盘价,涨跌幅,涨跌额,成交量,成交额,振幅,最高价,最低价,昨日收盘价,开盘价,量比,换手率,市盈率,市净率,总市值,流通市值) values ('%s','%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % record
        #插入数据库处理成空值
        sqlSentence4 = sqlSentence4.replace("-,","null,").replace(",-)",",null)")  
        cursor.execute(sqlSentence4)
    except Exception as e:
        print(sqlSentence4)
        #如果以上插入过程出错，跳过这条数据记录，继续往下进行
        print(e)
        break

#关闭游标，提交，关闭数据库连接
cursor.close()
conn.commit()
conn.close()

# connRead= pymysql.connect(host='127.0.0.1',
#                       port=3306,
#                       user='root',
#                       password="111",
#                       charset='utf8')
# cursorRead = connRead.cursor()
# cursorRead.execute("use stockDataBase;")
# #查询数据库并打印内容
# cursorRead.execute('select * from stock')
# results = cursorRead.fetchall()
# for row in results:
#     print(row)

#关闭游标，提交，关闭数据库连接
# cursor.close()
# conn.commit()
# conn.close()
