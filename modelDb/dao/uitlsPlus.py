import pymysql.cursors

class Utils(object):
    def __init__(self):
        self.connectDB()
    def connectDB(self):
        self.connect = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='Shipc=123',
        db='model_db',
        charset='utf8'
        )

        # 获取游标
        self.cursor = self.connect.cursor()


    def close(self):
        # 关闭连接
        self.cursor.close()
        self.connect.close()
    #查询一条
    def searchOneP(self,sql,arg):
        self.cursor.execute(sql,arg)
        result=self.cursor.fetchone()
        return result
    def searchOne(self,sql):
        self.cursor.execute(sql)
        result=self.cursor.fetchone()
        return result
    #查询多条
    def searchListP(self,sql,args):
        self.cursor.execute(sql,args)
        result=self.cursor.fetchall()
        return result
    def searchList(self,sql):
        self.cursor.execute(sql)
        result=self.cursor.fetchall()
        return result
    #x修改
    def modifyP(self,sql,args):
        self.cursor.execute(sql,args)
        # self.connect.commit()
    #批量修改
    def multiple_modeify(self,sql,args):
        self.cursor.executemany(sql,args)
        # self.connect.commit()

    #创建，返回rowid
    def create(self,sql,args):
        self.cursor.execute(sql,args)
        # self.connect.commit()
        return self.cursor.lastrowid

    def commit(self):
        self.connect.commit()
