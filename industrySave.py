

import pymysql
import pandas as pd
import time


#数据库名称和密码
#建立本地数据库连接(需要先开启数据库服务)
conn= pymysql.connect(host='127.0.0.1',
                      port=3306,user='root',
                      password="111",
                      charset='utf8')
cursor = conn.cursor()



sqlSentence2 = "use stockDataBase;"
cursor.execute(sqlSentence2)


daytime = time.strftime("%Y.%m.%d", time.localtime()) 
print(daytime)
print(type(daytime))



fileName=("industrystock"+daytime+".csv")
data = pd.read_csv(fileName, encoding="utf8")




#创建数据表，如果数据表已经存在，会跳过继续执行下面的步骤print('创建数据表stock_%s'% fileName)
try:
    sqlSentence3 = "create table industrydate"  + "(日期 date,开盘价 float,最高价 float,最低价 float,收盘价 float,成交量 bigint,未知 float,行业编号 bigint)"
    cursor.execute(sqlSentence3)
except Exception as e:
    print(e)


print('正在存储')
length = len(data)
for i in range(0, length):
    d = str(int(data.loc[i][0]))
    d = d[0:4]+"."+d[4:6]+"."+d[6:8]
    data.loc[i,"日期"]=d
    if(d == daytime):
        record = tuple(data.loc[i])
        print(record)
        #插入数据语句
        try:
            sqlSentence4 = "insert into industrydate" + "(日期,开盘价,最高价,最低价,收盘价,成交量,未知,行业编号)values ('%s',%s,%s,%s,%s,%s,%s,%s)" % record
            #获取的表中数据很乱，包含缺失值、Nnone、none等，插入数据库需要处理成空值 
            cursor.execute(sqlSentence4)
        except Exception as e:
            print(sqlSentence4)
            #如果以上插入过程出错，跳过这条数据记录，继续往下进行
            print(e)
            break

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
# cursorRead.execute('select * from industrydate')
# results = cursorRead.fetchall()
# for row in results:
#     print(row)





#
# cursorRead.close()
# connRead.commit()
# connRead.close()







# In[ ]:




