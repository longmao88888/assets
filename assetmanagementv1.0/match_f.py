#! usr/bin/evn python3
# -*- coding:utf-8 -*-


import re



# 进行资产名称匹配
def assetnamematch(cursor, assetinfo, stationlist):
    assetname = assetinfo[2]

    assetname = re.sub("[A-Za-z0-9\[\`\~\!\@\#\$\^\&\*\(\)\="
                       "\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%]", "", assetname)
    if len(stationlist) == 1:
        sql = "select STATIONID,IDENTIFIER,CUS_ENTITY_ROOM from %s where NAME1 like '%%%s%%' or NAMEINEMS like '%%%s%%'or STANDARD_NAME like '%%%s%%' " \
              % (stationlist[0], assetname, assetname, assetname,)
        cursor.execute(sql)
        result = cursor.fetchall()
        b = len(result)
        if b >= 1:  # 进行基站编码匹配
            info1 = [i for i in result if assetinfo[3] == i[1]]
            if len(info1) != 0:  # 匹配上则返回
                b = len(info1)
                result = info1
    if len(stationlist) == 4:
        b, result = assetcodematch(cursor, assetinfo[3], stationlist)
        if b == 0:
            sql = "select STATIONID,IDENTIFIER,CUS_ENTITY_ROOM from %s where NAME1 like '%%%s%%' or NAMEINEMS like '%%%s%%'or STANDARD_NAME like '%%%s%%' union ALL \
          select STATIONID,IDENTIFIER,CUS_ENTITY_ROOM from %s where NAME1 like '%%%s%%' or NAMEINEMS like '%%%s%%'or STANDARD_NAME like '%%%s%%' union ALL \
          select STATIONID,IDENTIFIER,CUS_ENTITY_ROOM from %s where NAME1 like '%%%s%%' or NAMEINEMS like '%%%s%%'or STANDARD_NAME like '%%%s%%' union ALL \
          select STATIONID,IDENTIFIER,CUS_ENTITY_ROOM from %s where NAME1 like '%%%s%%' or NAMEINEMS like '%%%s%%'or STANDARD_NAME like '%%%s%%' " \
                  % (stationlist[0], assetname, assetname, assetname, stationlist[1], assetname, assetname, assetname,
                     stationlist[2], assetname, assetname, assetname, stationlist[3], assetname, assetname, assetname)
            cursor.execute(sql)
            result = cursor.fetchall()
            b = len(result)

    return b, result


# 进行资产编码匹配
def assetcodematch(cursor, assetcode, stationlist):
    for station in stationlist:
        sql = "select STATIONID,IDENTIFIER,CUS_ENTITY_ROOM from %s where IDENTIFIER like '%%%s%%' " % (
        station, assetcode)
        cursor.execute(sql)
        result = cursor.fetchall()
        b = len(result)
        if b >= 1:
            break
    return b, result


# 进行资产地址匹配
def assetaddrmatch(cursor, assetaddr, stationlist):
    assetaddr = re.sub("[A-Za-z0-9\[\`\~\!\@\#\$\^\&\*\(\)\="
                       "\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%]", "", assetaddr)
    for station in stationlist:
        sql = "select STATIONID,IDENTIFIER,CUS_ENTITY_ROOM from \
              %s where CUS_ENTITY_ROOM like '%%%s%%' or DEVICE_LOCATE_ADD_ADDRESS_FULL_NAME like '%%%s%%' \
              or ADDRESS_DESC like '%%%s%%' " % (station, assetaddr, assetaddr, assetaddr)
        cursor.execute(sql)
        result = cursor.fetchall()
        b = len(result)
        if b >= 1:
            break
    return b, result


# 数据库中存在的资产表和基站表
def areaandstationlist(cursor):
    area = (u'禅城', u'南海', u'顺德', u'三水', u'高明')
    station = (u'l基站', u'c基站', u'c室分', u'c直放站')
    # 查询数据库数据表格
    cursor.execute('show tables')
    tables = ()
    for i in cursor.fetchall():
        tables = tables + i

    area = [i for i in area if i in tables]
    station = [i for i in station if i in tables]
    return area, station


# 基站ID匹配
def stationidmatch(cursor, stationid, area):
    sql = "select 主资产号 from %s where STATIONID LIKE '%%%s%%'" % (area, stationid)
    cursor.execute(sql)
    result = cursor.fetchall()
    b = len(result)
    return b, result


# 资产匹配函数
def assetmatch(cursor, area, stationlist, f):
    matchcount = 0
    failcount = 0
    # 需要匹配资产个数
    cursor.execute("select count(*)  from %s where 主资产号 is not NULL " % area)
    linecount = cursor.fetchone()[0]
    print(linecount)

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
    # 逐行选择资产表中信息去寻找基站
    for i in range(200):
        sql = "select 主资产号,地址,基站（机房）名称,基站（机房）编码,类,项,目 from %s limit %d,1" % (area, i)
        cursor.execute(sql)
        assetinfo = cursor.fetchone()  # 资产信息

        stationlist = stationlist0
        # 根据关键字缩小匹配基站范围
        if assetinfo[4] == '07' and assetinfo[5] == '03':
            if assetinfo[6] == '02':
                stationlist = [u'c基站']
            elif assetinfo[6] == '09':
                stationlist = [u'l基站']
            elif assetinfo[6] == '03':
                stationlist = [u'c直放站']
        if assetinfo[4] == '07' and assetinfo[5] == '04':
            stationlist = [u'c室分']

        if len(assetinfo[0]) == 0:
            print('主资产号 为空！')
            continue
        else:
            # 根据资产信息进行匹配
            if len(assetinfo[2]) == 0:
                if len(assetinfo[3]) == 0:
                    if len(assetinfo[1]) == 0:
                        b = 0
                        result = None
                    else:
                        b, result = assetaddrmatch(cursor, assetinfo[1], stationlist)
                else:
                    b, result = assetcodematch(cursor, assetinfo[3], stationlist)
            else:
                b, result = assetnamematch(cursor, assetinfo, stationlist)

        if b >= 1:
            if b > 10:
                b = 10
            info = str(b) + "STATIONID:" + "".join([result[i][0] for i in range(b)])
            matchcount += 1
        else:
            info = 'MATCH FAIL'
            failcount += 1

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


# 基站匹配函数
def stationmatch(cursor, station, arealist, f):
    areaCHN = [u'禅城', u'南海', u'顺德', u'三水', u'高明']
    area = ['CC', 'NH', 'SD', 'SS', 'GM']
    # 需要匹配站点个数
    cursor.execute("select count(*)  from %s where STATIONID is not NULL " % station)
    linecount = cursor.fetchone()[0]
    print(linecount)
    cc1 = 0
    cc2 = 0
    # 增加资产编号集合ASSETID
    sql = "SHOW COLUMNS FROM %s LIKE 'ASSETID'" % station
    cursor.execute(sql)
    if cursor.fetchone() == None:
        sql = "ALTER TABLE %s ADD COLUMN `ASSETID`  varchar(255) NULL FIRST" % station
        cursor.execute(sql)
    # else:
    #     Yes_or_No = easygui.buttonbox("资产表中已经含有ASSETID\n是否更新ASSETID?", choices=['Yes', 'No'])
    #     if Yes_or_No == 'No':
    #         return None
    cursor.execute("ALTER TABLE %s" % station)

    # 逐行选择基站表中信息去寻找资产
    for i in range(50):
        sql1 = "select Stationid from %s limit %d,1" % (station, i)
        cursor.execute(sql1)
        stationinfo = cursor.fetchone()  # 基站信息

        if len(stationinfo[0]) == 0:
            print('StationID 为空！')
            return
        else:
            stationarea = stationinfo[0][:2]
            assettable = [areaCHN[i] for i in range(len(area)) if stationarea == area[i]]  # 确定基站所在区
            b, result = stationidmatch(cursor, stationinfo[0], assettable[0])

        # 插入匹配到的assetID
        if b == 0:
            info = "MATCH FAIL"
            cc1 += 1
        else:
            if b > 10: b = 10
            info = ",".join([result[i][0] for i in range(b)])
            cc2 += 1

        # 更新基站表
        sqlinsert = "UPDATE %s SET ASSETID = '%s' where STATIONID = '%s'" % (station, info, stationinfo[0])
        cursor.execute(sqlinsert)

    # 输出匹配结果统计
    info = "%s共匹配%d个基站，其中%d个基站匹配成功，%d个基站未匹配成功。\n" % (station, cc1 + cc2, cc2, cc1)
    print(info)
    f.write(info)

    return 1


# 资产信息查询
def assetinfoquery(cursor, aid,areaid):
    # areaCHN = [u'禅城', u'南海', u'顺德', u'三水', u'高明']
    # area = ['CC', 'NH', 'SD', 'SS', 'GM']
    # areaid = [areaCHN[i] for i in range(len(area)) if area[i] == areaid]
    area = areaname(areaid)
    cursor.execute("select 主资产号,地址,基站（机房）编码,残值 from %s where 主资产号 like '%s'" % (area, aid))
    assetinfo = cursor.fetchone()
    # for areaid in areaCHN:
    #     sql ="select 主资产号,地址,基站（机房）编码,残值 from %s where 主资产号 like '%s'" % (areaid, aid)
    #     cursor.execute(sql)
    #     assetinfo = cursor.fetchone()
    #     if assetinfo != None:
    #         break

    return assetinfo


#根据英文简称返回区域名
def areaname(areaid):
    areachn = [u'禅城', u'南海', u'顺德', u'三水', u'高明']
    areaeng = ['CC', 'NH', 'SD', 'SS', 'GM']
    area = [areachn[i] for i in range(5) if areaeng[i] == areaid]
    return area[0]

#根据英文简称返回基站类型名
def stationame(stationid):
    stationchn = (u'l基站', u'c基站', u'c室分', u'c直放站')
    stationeng = ['JZ', 'JZ','SF','SF']
    station = [stationchn[i] for i in range(4) if stationeng[i] == stationid]
    return station