from dao.daoUtils import *
from dao.uitlsPlus import *
import re
#初始查询列表返一个列表
def recyBinsearch(queryDict):
    # 查询数据
    if queryDict == {} :
        sql =  " SELECT * FROM model_db.v_recyclebin"
        res = searchData(sql)
        return res
    else :
        for k ,v in  queryDict.items():
            if k != 'page':
                sql = 'SELECT * FROM model_db.v_recyclebin where '+str(k)+' = ' +"'%s'" %v
            else:
                sql =  " SELECT * FROM model_db.v_recyclebin"
            res = searchData(sql)
            return res
def rollbackUtil(id):
    sql = "update d_materials set iswork = 1 where id = %s"
    up = Utils()
    rid = up.create(sql,id)
    up.commit()
    up.close()

def getRecyList(name):
    sql ="select distinct "+str(name)+" from v_recyclebin"
    data = searchData(sql)
    list = []
    for i in data:
        list.append(i[0])
    return list

#回收站检索
def reSearch(search):
    s = str(search).split(' ')
    sql = 'select * from v_searchlist where iswork = 0 and name = %s'
    resSql = 'select * from v_recyclebin where id = %s'
    u = Utils()
    rList=[]
    for i in s :
        i=[i,]
        res =u.searchListP(sql,i)
        for j in res:
            id = [j[0],]
            rList.append(u.searchOneP(resSql,id))

    return rList


# search = 'Intel Nvidia EagleStream asd 123'
# reSearch(search)
