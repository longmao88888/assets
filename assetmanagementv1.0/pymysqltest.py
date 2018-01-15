#!usr/bin/env python3
from flask import Flask, request, render_template,jsonify
import pymysql
from match_f import areaandstationlist, assetinfoquery, areaname, stationame

app = Flask(__name__)
app.config.from_object(__name__)

# 连接数据库
db = pymysql.connect("localhost", "root", "", "assetsmanagement", charset='utf8')
cursor = db.cursor()

#主页
@app.route('/', methods=['GET','POST'])
def index():
    queryerr = 0
    return render_template('index.html',queryerr=queryerr)

# 根据关键字查询对应基站
@app.route('/keywordquery', methods=['POST'])
def keywordquery():
    query = request.form['query']
    arealist,stationlist = areaandstationlist(cursor)
    info = []
    idinfo =[]
    global info0
    for station in stationlist:
        sql = "SELECT stationid,name1,IDENTIFIER,assetid FROM %s \
              WHERE stationid LIKE '%%%s%%' OR name1 LIKE  '%%%s%%'" % (station, query,query)
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 获取所有记录列表
            results = cursor.fetchall()
            if results != None:
                info.extend(results)
                idinfo.extend([i[3] for i in results])
        except:
            print("Error: unable to fetch data")
    if info == []:
        queryerr = 1
        return render_template('index.html', queryerr=queryerr)
    for i in range(len(idinfo)):
        if idinfo[i] is None:
            idinfo[i]="该基站未进行资产匹配！,".strip(',').split(',')
        else:
            idinfo[i] = idinfo[i].strip(',').split(',')
    info0 = info
    return render_template('keywordquery.html', assets=info, idinfo=idinfo)
#从基站id进来的入口
@app.route('/assetfromID',methods=['GET'])
def assetfromID():
    global stationid0
    global stationinfo0
    stationid0 = request.args.get("stationid")
    stationinfo = [i for i in info0 if stationid0 == i[0]]
    stationinfo0 =list(stationinfo[0])
    assetlist = stationinfo0[3].strip(',').split(',')
    areaid = stationid0[0:2]
    global ainfo0
    ainfo0=[]
    for i in assetlist:
        if 'found' in i:
            assetinfo1 = "none"
        else:
            assetinfo1 = assetinfoquery(cursor, i.strip(), areaid)
        if assetinfo1 is None:
            assetinfo1 = "none"
        ainfo0.extend(assetinfo1)
    return jsonify(list(ainfo0))
# 从主资产号进来的入口
@app.route('/queryinfo',methods= ['GET'])
def queryinfo():
    aid = request.args.get("aid")
    areaid = request.args.get("areaid")
    areaid = areaid[0:2]
    if 'found' in aid:
        assetinfo = "none"
    else:
        assetinfo = assetinfoquery(cursor,aid.strip(),areaid)
    if assetinfo == None:
        assetinfo = "none"
    global assetinfo0
    assetinfo0 = assetinfo
    return jsonify(list(assetinfo))
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