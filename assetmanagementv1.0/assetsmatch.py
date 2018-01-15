#!usr/bin/env python3
# -*- coding:utf-8 -*-

import pymysql
import time
from match_f import areaandstationlist,assetmatch,stationmatch

starttime = time.clock()
# 连接数据库
db = pymysql.connect("localhost", "root", "", "assetsmanagement", charset='utf8')
cursor = db.cursor()

# 查询数据库中的表格
(arealist, stationlist) = areaandstationlist(cursor)
#打开保存匹配结果文件
f = open('result.txt','w+')
# 资产匹配基站
for area in arealist:
    assetmatch(cursor, area, stationlist, f)

f.close()

f = open('result.txt','a+')
# 基站匹配资产
for station in stationlist:
    stationmatch(cursor,station,arealist,f)
f.close()
db.close()
print(time.clock()-starttime)