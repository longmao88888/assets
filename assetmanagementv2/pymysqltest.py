#!usr/bin/env python3
from flask import Flask, request, render_template
import pymysql

app = Flask(__name__)
app.config.from_object(__name__)

#连接数据库
db = pymysql.connect("localhost", "root", "", "assetsmanagement", charset='utf8')
cursor = db.cursor()

#测试连接数据库
# cursor.execute("SELECT VERSION()")
# data = cursor.fetchone()
#print("Database version: %s " % data)

@app.route('/',methods=['GET'])
def query():
    return render_template('assets.html')


@app.route('/assetsquery',methods=['POST'])
def sqlquery():
    sqlquery=request.form['query']


# SQL 查询语句
    sqlquery="%"+sqlquery+"%"
    sql = "SELECT * FROM 顺德 WHERE 主资产号 LIKE '%s' OR 地址 LIKE  '%s'" % (sqlquery,sqlquery)
    print(sql)
    try:
        # 执行SQL语句
        queryerr = 1
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        if results[0]==None:
            queryerr=0
    except:
        print("Error: unable to fetch data")
        queryerr = 0


    if queryerr==0:
        msg = '未查询到相关结果，请确认输入是否正确'
        return render_template('assetserr.html',msg=msg)

    assets = results
    return render_template('AssetTable.html', assets=assets)


if __name__ == '__main__':
    app.run()
    db.close()