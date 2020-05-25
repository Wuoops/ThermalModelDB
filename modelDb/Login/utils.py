from dao.uitlsPlus import *
# 用户类
class Users():
    def getUserInfo(self,userId):
        sql = 'select * from d_users where user_id = %s'
        args = (userId,)
        ut = Utils()
        uList = ut.searchOneP(sql,args)
        return uList


    def __init__(self,userId):
        uList = self.getUserInfo(userId)
        self.userId = userId
        self.userName = uList[1]
        self.fullname = uList[3]

