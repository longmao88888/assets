import pymysql
from flask import Flask, request, render_template
import jsonify

app=Flask(__name__)
app.config.from_object(__name__)

@app.route("/",methods=['GET'])
def index():
    return render_template("test.html")

@app.route("/test",methods=['GET','POST'])
def testdd():
    print("dd0000d")
    name1 = request.args.get('num')
    print(name1)

    return "test"


if __name__ == '__main__':
    app.run(debug=True)



# # # 连接数据库
# db = pymysql.connect("localhost", "root", "", "assetsmanagement", charset='utf8')
# cursor = db.cursor()
# cursor.execute("select count(*)  from c基站 where stationID is not NULL ")
# linecount = cursor.fetchone()[0]
# print(linecount)



# sql = "select STATIONID,NAME1,NAMEINEMS,IDENTIFIER,CUS_ENTITY_ROOM from %s where NAME1 like '%%%s%%' union all \
#        select STATIONID,NAME1,NAMEINEMS,IDENTIFIER,CUS_ENTITY_ROOM from %s where NAME1 like '%%%s%%' union all \
#        select STATIONID,NAME1,NAMEINEMS,IDENTIFIER,CUS_ENTITY_ROOM from %s where NAME1 like '%%%s%%' " \
#        % (u'l基站',u'禅城季华佛山中级人',u'c室分',u'顺德乐从信用社营业大',u'c基站',u'芦苞欧')
# cursor.execute(sql)
# result = cursor.fetchall()
# for  i in result:
#     print(i)

# #修改表结构
# arealist,stationlist =  areaandstationlist(cursor)
# for area in arealist:
#     cursor.execute("alter table %s DROP assetid" % area)


# for i in range(linecount):
#     cursor.execute("select stationid,IDENTIFIER from c基站 limit %d,1" % i)
#     info = cursor.fetchone()
#     if len(info[1]) <=9:
#         continue
#     info1 = info[1][:4]+info[1][-5:]
#     cursor.execute("alter table c基站")
#     cursor.execute("UPDATE c基站 SET IDENTIFIER = '%s' where stationID = '%s'" % (info1,info[0]))

# db.close()
# b="dff"
# a= ['a','b','c']
# b += "".join(a)
# aaa=",".join(a)
# print(b,a,aaa)