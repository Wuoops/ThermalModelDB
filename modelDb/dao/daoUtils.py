import pymysql.cursors

# 连接数据库
def connDB():
    connect = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='Shipc=123',
        db='model_db',
        charset='utf8'
    )

    # 获取游标
    cursor = connect.cursor()
    return  connect,cursor

def closeConn(connect,cursor):
    # 关闭连接
    cursor.close()
    connect.close()

# 查询数据
def searchDataP(sql,parameter):
    conn,cursor = connDB()
    cursor.execute(sql % parameter)
    result=[]

    # print(parameter)
    for row in cursor.fetchall():
        # print(row)
        result.append(row)
    # print('共查找出', cursor.rowcount, '条数据')
    closeConn(conn,cursor)
    return result
# 查询数据
def searchData(sql):
    conn,cursor = connDB()
    cursor.execute(sql)
    result=[]
    for row in cursor.fetchall():
        # print(row)
        result.append(row)
    print('共查找出', cursor.rowcount, '条数据')
    closeConn(conn,cursor)
    return result
#查询一条
def searchOne(sql,arg):
    conn,cursor = connDB()
    cursor.execute(sql,arg)
    result=cursor.fetchone()
    closeConn(conn,cursor)
    return result

def runSql(sql,parameter):
    conn,cursor = connDB()
    cursor.execute(sql % parameter)
    #提交
    conn.commit()
    #关闭连接
    closeConn(conn,cursor)
    print('成功执行', cursor.rowcount, '条数据')

