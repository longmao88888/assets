#!usr/bin/env python3
# -*- coding:utf-8 -*-

import pymysql
import time
from match_f import areaandstationlist,assetmatch,stationidmatch,createstationinfotable,createinfo

starttime = time.clock()
# 连接数据库
db = pymysql.connect("localhost", "root", "", "资产", charset='gbk')
cursor = db.cursor()

# 查询数据库中的表格
(arealist, stationlist) = areaandstationlist(cursor)

# #删除插入的ASSETID和STATIONID。调试用。
# for i in arealist:
#     cursor.execute("alter table %s drop column stationid " % i)
# for i in stationlist:
#     cursor.execute("alter table %s drop column assetid " % i)

#打开保存匹配结果文件
f = open('result.txt','w+')
# 资产匹配基站
for area in arealist:
    assetmatch(cursor, area, stationlist, f)

# f.close()
#
# f = open('result.txt','a+')
# # 基站匹配资产
# station = u"站址"
# # createstationinfotable(cursor,stationlist)
# # createinfo(cursor,station)
# stationidmatch(cursor,station,arealist,f)
f.close()
db.close()
print(time.clock()-starttime)