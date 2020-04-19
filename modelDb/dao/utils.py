from dao.uitlsPlus import *

def getUserList():
    sql='select user_id, owner_name from d_users'
    obj = Utils()
    userList = obj.searchList(sql)
    obj.close()
    return userList
def getBranchList():
    sql = 'select * from m_source'
    obj = Utils()
    branchList = obj.searchList(sql)
    obj.close()
    return branchList

def changeListToDIct(list):
    dic={}
    for i in list:
        dic[i[0]]=i[1]
    return dic
