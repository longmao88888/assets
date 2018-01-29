#! usr/bin/env python3
# -*- coding:utf-8 -*-

import pymysql
from match_f import areaandstationlist,stationIDmatch,infocompare

db = pymysql.connect("localhost", "root", "", "assetsmanagement", charset='utf8')
cursor = db.cursor()

arealist,stationlist = areaandstationlist(cursor)

for area in arealist:
    cursor.execute("select count(*) from %s where STATIONID IS NOT NULL" % area)
    countline=cursor.fetchone()[0]
    for i in range(2):
        sql="select * from %s limit %d,1" % (area, i)
        cursor.execute(sql)
        assetinfo=cursor.fetchone()
        stationinfo = stationIDmatch(cursor,assetinfo[0],stationlist)
        if stationinfo != None:
            infocompresult = infocompare(assetinfo,stationinfo)
        else:
            print("该资产对应的STATIONID在基站表中未查询到")