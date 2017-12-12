#!usr/bin/env python3
# -*- coding:utf-8 -*-

import re
import pymysql


# 连接数据库
db = pymysql.connect("localhost", "root", "", "assetsmanagement", charset='utf8')
cursor = db.cursor()


# 获取资产个数
cursor.execute("select count(*)  from 顺德 where ID is not NULL ")
linecount = cursor.fetchone()[0]
print(linecount)
# 逐行选择资产表中基站（机房）名称去配置基站
for i in range(1,5):
    sql1 = "select 基站（机房）名称 from 顺德 limit %d,1" % i
    cursor.execute(sql1)
    asset = cursor.fetchone()[0]
    # 提取中文名称并查询
    asset1 = re.sub("[A-Za-z0-9\[\`\~\!\@\#\$\^\&\*\(\)\="
                    "\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%]", "", asset)
    sql2 = "select * from l基站 where NAME like '%%%s%%'" % asset1
    cursor.execute(sql2)
    b = len(cursor.fetchall())
    # 若全称未查询到，则选取最后四个字进行匹配
    if b == 0 and len(asset1) > 4:
        sql2 = "select * from l基站 where NAME like '%%%s%%'" % asset1[-5:-1]
        cursor.execute(sql2)
        b = len(cursor.fetchall())

    # 资产表中插入匹配到的基站ID STATIONID
    if b == 0:
        info = "%s Not found" % asset
    elif b != 1:
        info = "资产对应到%d个基站，需确认" % b
    else:
        info = cursor.fetchall()[0][0]
    #增加第一列STATIONID
    # sql3="ALTER TABLE `顺德`" \
    #      "ADD COLUMN `STATIONID`  varchar(255) NULL FIRST"
    # cursor.execute(sql3)

    cursor.execute("ALTER TABLE 顺德")
    sqlinsert = "UPDATE 顺德 SET STATIONID = '%s' where 基站（机房）名称 like '%s'" % (info, asset)
    print(sqlinsert)
    cursor.execute(sqlinsert)
db.close()