#!usr/bin/etc python3
# -*- coding:utf-8 -*-
import pymysql
from match_f import areaandstationlist,  areaname


# 连接数据库
db = pymysql.connect("localhost", "root", "", "资产", charset='utf8')
cursor = db.cursor()


# 创建站址索引信息表
def createstationinfotable(cursor):

    # sql= "CREATE TABLE `站址` ( `ID`  varchar(255) NULL ,\
    # `CRRU`  varchar(255) NULL ,\
    # `C基站`  varchar(255) NULL ,\
    # `C室分站`  varchar(255) NULL ,\
    # `C直放站`  varchar(255) NULL ,\
    # `LRRU`  varchar(255) NULL ,\
    # `L基站`  varchar(255) NULL )"
    # cursor.execute(sql)
    return 1


def loadstationinfo(cursor,table,stationlist):
    # 建立STATION ID列数据
    allid=[]
    for stationtype in stationlist:
        sql = "select stationid from %s where stationid is not null" % (stationtype)
        cursor.execute(sql)
        result = cursor.fetchall()
        temp = [i[0] for i in result]
        allid.extend(temp)
        #去重
    allid = list(set(allid))
    print(allid)
    for i in allid:
        cursor.execute("alter table %s" % table)
        sql = "insert into %s (ID) values ('%s')" % (table, i)
        cursor.execute(sql)
    return allid


def createinfo(cursor,station):
    stationlist = ['crru', 'c基站', 'c室分站', 'c直放站', 'lrru', 'l基站']
    cursor.execute("select ID from %s where ID is not null" % station)
    allid = cursor.fetchall()
    for i in allid:
        result = []
        for stationtype in stationlist:
            cursor.execute("select count(*) from %s where stationid = '%s'" % (stationtype, i[0]))
            a = cursor.fetchone()
            result.extend(str(a[0]))
        cursor.execute("alter table %s" % station)
        cursor.execute("update %s set crru='%s',c基站='%s', c室分站='%s', c直放站='%s', lrru='%s', l基站='%s' where ID ='%s' " % (station, result[0], result[1], result[2], result[3], result[4], result[5], i[0]))
    return 1

def createassetinfo(cursor,table,assetlist):
    cursor.execute("select count(*) from %s where id is not null" % table)
    linecount = cursor.fetchone()[0]
    print(linecount)
    # linecount =10
    for i in range(0,linecount):
        cursor.execute("select id from %s limit %d,1 " %(table,i))
        stationid =cursor.fetchone()[0]
        try:
            area = areaname(stationid[0:2])
            sql = "select 主资产号 from %s where stationid like '%%%s%%'" % (area, stationid)
            cursor.execute(sql)
            result = cursor.fetchall()
            b =len(result)
            assetinfo =[i[0] for i in result]
            assetinfo = ",".join(assetinfo)
        except:
            print(sql)
            return 0
        cursor.execute("alter table %s" % table)
        cursor.execute("update %s set 资产信息= '%s',资产个数='%d' where id = '%s'" % (table,assetinfo,b,stationid))
    return 1


if __name__ == "__main__":
    table = u'站址'
    arealist,stationlist = areaandstationlist(cursor)
    loadstationinfo(cursor,table,stationlist)
    createinfo(cursor, table)
    createassetinfo(cursor,table,arealist)