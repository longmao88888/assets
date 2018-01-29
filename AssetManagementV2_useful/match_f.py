#! usr/bin/evn python3
# -*- coding:utf-8 -*-


import re
import easygui


testnum=50


# 进行资产编码匹配
def assetcodematch(cursor, assetcode0, stationlist,resultinfo):
    for station in stationlist:
        assetcode = assetcode0
        if station == "c基站":
            assetcode = assetcode0[:4]+"00"+assetcode0[-5:]
        sql = "select STATIONID from %s where IDENTIFIER like '%%%s%%' " % (station, assetcode)
        cursor.execute(sql)
        result = cursor.fetchall()
        b = len(result)
        if b >= 1:
            resultinfo ="编码匹配成功。"
            break
    if b ==0:
        resultinfo +='编码匹配失败。'
    return b, result, resultinfo


# 进行资产名称匹配
def assetnamematch(cursor, assetinfo, stationlist,resultinfo):
    assetname = assetinfo[2]

    assetname = re.sub("[A-Za-z0-9\[\`\~\!\@\#\$\^\&\*\(\)\="
                       "\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%]", "", assetname)
    if len(stationlist) == 1:
        sql = "select STATIONID,NAME1,NAMEINEMS,STANDARD_NAME from %s where NAME1 like '%%%s%%' or NAMEINEMS like '%%%s%%'or STANDARD_NAME like '%%%s%%' " \
              % (stationlist[0], assetname, assetname, assetname,)
    else:
        sql = "select STATIONID,NAME1,NAMEINEMS,STANDARD_NAME from %s where NAME1 like '%%%s%%' or NAMEINEMS like '%%%s%%'or STANDARD_NAME like '%%%s%%' union ALL \
          select STATIONID,NAME1,NAMEINEMS,STANDARD_NAME from %s where NAME1 like '%%%s%%' or NAMEINEMS like '%%%s%%'or STANDARD_NAME like '%%%s%%' union ALL \
          select STATIONID,NAME1,NAMEINEMS,STANDARD_NAME from %s where NAME1 like '%%%s%%' or NAMEINEMS like '%%%s%%'or STANDARD_NAME like '%%%s%%' union ALL \
          select STATIONID,NAME1,NAMEINEMS,STANDARD_NAME from %s where NAME1 like '%%%s%%' or NAMEINEMS like '%%%s%%'or STANDARD_NAME like '%%%s%%' " \
              % (stationlist[0], assetname, assetname, assetname, stationlist[1], assetname, assetname, assetname,
                 stationlist[2], assetname, assetname, assetname, stationlist[3], assetname, assetname, assetname)
    cursor.execute(sql)
    result = cursor.fetchall()
    b = len(result)
    if b == 0:
        resultinfo += "名称匹配失败。"
    if b >= 1:
        resultinfo ="名称匹配成功。"

    return b, result, resultinfo


# 进行资产地址匹配
def assetaddrmatch(cursor, assetaddr, stationlist, resultinfo,area):
    assetaddr = re.sub("[A-Za-z0-9\[\`\~\!\@\#\$\^\&\*\(\)\="
                       "\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%]", "", assetaddr)
    assetaddr = assetaddr.lstrip("广东省").lstrip("佛山市").lstrip(area).lstrip("区")
    for station in stationlist:
        sql = "select STATIONID from %s where CUS_ENTITY_ROOM like '%%%s%%' or DEVICE_LOCATE_ADD_ADDRESS_FULL_NAME like '%%%s%%' \
              or ADDRESS_DESC like '%%%s%%' " % (station, assetaddr, assetaddr, assetaddr)
        cursor.execute(sql)
        result = cursor.fetchall()
        b = len(result)
        if b > 0:
            break
            resultinfo = "地址匹配成功。"
    if b == 0:
        resultinfo += "地址匹配失败。"
    return b, result, resultinfo


# 数据库中存在的资产表和基站表
def areaandstationlist(cursor):
    area = (u'禅城', u'南海', u'顺德', u'三水', u'高明')
    station = (u'l基站', u'c基站', u'c室分站', u'c直放站')
    # 查询数据库数据表格
    cursor.execute('show tables')
    tables = ()
    for i in cursor.fetchall():
        tables = tables + i

    area = [i for i in area if i in tables]
    station = [i for i in station if i in tables]
    return area, station


# 资产匹配基站函数
def assetmatch(cursor, area, stationlist, f):
    matchcount = 0
    failcount = 0
    # 需要匹配资产个数
    cursor.execute("select count(*)  from %s where 主资产号 is not NULL " % area)
    linenum = cursor.fetchone()[0]
    print(linenum)

    # 增加资产编号字段STATIONID
    sql = "SHOW COLUMNS FROM %s LIKE 'STATIONID'" % area
    cursor.execute(sql)
    if cursor.fetchone() is None:
        sql = "ALTER TABLE %s ADD COLUMN `STATIONID`  varchar(255) NULL FIRST " % area
        cursor.execute(sql)
    # else:
    #     Yes_or_No = easygui.buttonbox("资产表中已经含有STATIONID\n是否更新STATIONID?", choices=['Yes', 'No'])
    #     if Yes_or_No == 'No':
    #         return None
    stationlist0 = stationlist
    # 逐行选择资产表中信息去匹配基站
    for i in range(linenum):
        print(linenum, ":", i)
        info = ""
        b = 0
        stationhascode = [u'c基站', u'l基站']
        sql = "select 主资产号,地址,基站（机房）名称,基站（机房）编码,类,项,目 from %s limit %d,1" % (area, i)
        cursor.execute(sql)
        assetinfo = cursor.fetchone()  # 资产信息
        stationlist = stationlist0

        if len(assetinfo[0]) == 0: #主资产号为空
            info += '主资产号为空！'
        else:
            # 根据资产信息进行匹配
            stationlisthascode = [i for i in stationhascode if i in stationlist]
            if len(assetinfo[3]) != 9:
                info += '基站（机房）编码为空或有误。'
            else:
                if len(stationlisthascode) != 0:
                    b, result, info = assetcodematch(cursor, assetinfo[3], stationlisthascode,info)#编码匹配

            if b == 0:
                if len(assetinfo[2]) == 0:
                    info += '基站（机房）名称为空。'
                else:
                    b, result, info = assetnamematch(cursor, assetinfo, stationlist, info)  # 名称匹配
            if b == 0:
                if len(assetinfo[1]) == 0:
                    info += '基站（机房）地址为空。 '
                else:
                    b, result, info = assetaddrmatch(cursor, assetinfo[1], stationlist, info,area)  # 地址匹配

        if b < 1:
            info += "匹配失败。"
            failcount += 1
        else:
            matchcount += 1
            if b == 1:
                info = result[0][0]
            else:
                tempresult = [result[i][0] for i in range(b)]
                result = list(set(tempresult))#去除重复项
                b = len(result)
                if b ==1:
                    info = result[0]
                else:
                    if b>10:
                        result=result[0:10]
                    info += str(b)+"基站:"+','.join(result)

        # 更新基站表
        cursor.execute("ALTER TABLE %s" % area)
        sqlinsert = "UPDATE %s SET STATIONID = '%s' where 主资产号 = '%s'" % (area, info, assetinfo[0])
        cursor.execute(sqlinsert)

    # 输出匹配结果统计
    info = "%s共匹配%d个资产，%d个资产匹配成功,%d个资产未匹配成功。\n" % (area, matchcount + failcount, matchcount, failcount)
    # 匹配统计结果保存
    print(info)
    f.write(info)
    return 1


#根据英文简称返回区域名
def areaname(areaid):
    areachn = [u'禅城', u'南海', u'顺德', u'三水', u'高明']
    areaeng = ['CC', 'NH', 'SD', 'SS', 'GM']
    area = [areachn[i] for i in range(5) if areaeng[i] == areaid]
    return area[0]


#根据英文简称返回基站类型名
def stationame(stationid):
    stationchn = (u'l基站', u'c基站', u'c室分站', u'c直放站')
    stationeng = ['JZ', 'JZ','SF','SF']
    station = [stationchn[i] for i in range(4) if stationeng[i] == stationid]
    return station
