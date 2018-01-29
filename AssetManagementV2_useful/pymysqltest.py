#!usr/bin/env python3
from flask import Flask, request, render_template,jsonify
import pymysql
from match_f import areaandstationlist, areaname, stationame

app = Flask(__name__)
app.config.from_object(__name__)

# 连接数据库
db = pymysql.connect("localhost", "root", "", "资产", charset='utf8')
cursor = db.cursor()


# 主页
@app.route('/', methods=['GET','POST'])
def index():
    queryerr = 0
    return render_template('index.html',queryerr=queryerr)


# 根据关键字查询对应基站
@app.route('/keywordquery', methods=['POST'])
def keywordquery():
    query = request.form['query']
    arealist,stationlist = areaandstationlist(cursor)
    station = u'站址'
    info = []
    idinfo =[]
    global info0
    sql = "SELECT id,crru,c基站,c室分站,c直放站,lrru,l基站,资产个数 FROM %s WHERE id LIKE '%%%s%%' " % (station, query)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        results = cursor.fetchall()
        if results != None:
            info = list(results)
    except:
        print("Error: unable to fetch data")
    if info == []:
        queryerr = 1
        return render_template('index.html', queryerr=queryerr)
    # for i in range(len(idinfo)):
    #     if idinfo[i] is None:
    #         idinfo[i]="该基站未进行资产匹配！,".strip(',').split(',')
    #     else:
    #         idinfo[i] = idinfo[i].strip(',').split(',')
    info0 = info
    return render_template('keywordquery.html', assets=info)

#资源详细信息
@app.route('/clickdetailinfo',methods=['GET'])
def clickdetailinfo():
    stationid = request.args.get('stationid')
    stationtype = request.args.get('stationtype')
    print(stationtype)
    result = None
    if stationtype != '资产':#资源查询
        sql = "select stationid,name1 from %s where stationid = '%s'" % (stationtype, stationid)
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
        except Exception:
            print('资源查询失败。')
    else:#资产查询
        # sql = "select 资产信息 from 站址 where stationid = '%s'" % stationid
        try:
            # cursor.execute(sql)
            # result = cursor.fetchall()
            # assetlist = result.strip(',').split(',')
            # print(assetlist)
            area = areaname(stationid[0:2])
            # result=[]
            # for assetid in assetlist:
            sql = "select 主资产号,地址,基站（机房）编码,基站（机房）名称 from %s where stationid like '%%%s%%'" % (area, stationid)
            cursor.execute(sql)
            result = cursor.fetchall()
            # result.extend(res)
        except Exception:
            print('资产查询失败。')
    return jsonify(list(result))



# 保存修改后的资产信息
@app.route('/saveinfo',methods=['POST'])
def saveinfo():
    newinfo = request.get_json()
    newinfolist = [newinfo[str(i)] for i in range(len(newinfo))]
    area = areaname(newinfolist[1])
    cursor.execute("ALTER TABLE %s" % area)
    isadd = False
    addstr ="";
    if(newinfolist[2] == 0):#主资产ID入口，不增加资产
        for k in range(3,len(newinfolist)):
            if assetinfo0[k-3] != newinfolist[k]:
                sql="update %s SET 地址 = '%s' where 主资产号 like '%s'" % (area, newinfolist[4],newinfolist[3])
                cursor.execute(sql)
                break
    else:
        if (newinfolist[0]*4+4) <= len(ainfo0):
            for i in range(3, len(newinfolist)):
                if ainfo0[newinfolist[0]*4+i] != newinfolist[i]:
                    try:
                        cursor.execute("update %s SET 地址 = '%s' where 主资产号 = '%s'" %
                               (area, newinfolist[4],newinfolist[3]))
                    except:
                        print("保存出错")
                    break
        else:#新增资产保存
            isadd = True
            sql="insert into %s (主资产号,地址) VALUES ('%s','%s')" % (area, newinfolist[3], newinfolist[4])
            cursor.execute(sql)
            print('插入成功。')
            addstr = newinfolist[3]

        if isadd:
            #将新资产号添加至基站的资产列表中
            # tempstr=[i[3] for i in info0 if stationid0 == i[0]]
            addstr =stationinfo0[3]+','+addstr
            stationinfo0[3] = addstr
            station = stationame(stationid0[2:4])
            for j in station:
                try:
                    sql ="update %s set ASSETID='%s' where stationid='%s'" % (j,addstr,stationid0)
                    cursor.execute(sql)
                except:
                    print('新增记录保存失败。')
    return "success"


if __name__ == '__main__':
    app.run(debug=True)
    db.close()