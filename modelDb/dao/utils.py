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
# 获取版本信息
def getBranchInfoByMaterId(mid,branch):
    sql = """
    SELECT 
            name,
            (SELECT 
                    s.source_name
                FROM
                    m_source s
                WHERE
                    res.source = s.source) branch,
            MAX(pid) pid,
            creater,
            (select u.owner_name from d_users u where u.user_id =res.creater) creatername,
            res.source
        FROM
            d_model_resource res
        WHERE
            materialsid = %s
            AND res.source = %s
            AND iswork = 1    
        group by 
        name,res.source,creater
        ;
    """

    args = [mid,branch,]
    obj = Utils()
    resList = obj.searchOneP(sql,args)
    obj.close()

    return resList


# 获取版本迭代后的信息
def getBranchIterateInfo(mid,branch,creater,iswork):
    sql = """
    SELECT 
            name,
            (SELECT 
                    s.source_name
                FROM
                    m_source s
                WHERE
                    res.source = s.source) branch,
            MAX(pid) pid,
            creater,
            (select u.owner_name from d_users u where u.user_id =res.creater) creatername,
            res.source
        FROM
            d_model_resource res
        WHERE
            materialsid = %s
            AND res.source = %s
            AND iswork = %s 
            and creater = %s
        group by 
        name,res.source,creater ;
    """

    args = [mid,branch,iswork,creater]
    obj = Utils()
    resList = obj.searchOneP(sql,args)
    obj.close()

    return resList

# 将数据迭代到d_model_resource和d_res_path表
def iterate(mid,branch):
    #获取当前最新版本信息
    nowList = getBranchInfoByMaterId(mid,branch)
    name = nowList[0]
    pid = nowList[2]
    creater = nowList[3]
#     获取当前版本的resid
    nowresSql = 'select max(id) from d_model_resource where materialsid = %s and source = %s and iswork = 1'
    nowresargs = [mid,branch]
#判断 d_model_resource表  所需数据是否存在语句
    ismoodelsql = 'select * from d_model_resource where materialsid = %s  and source = %s and iswork =0'
    ismodelargs = [mid,branch]
# 用于删除d_model_resource表的sql
    deletemodel = 'delete from d_model_resource where materialsid = %s  and source = %s and iswork =0'
    deleteModelArgs = [mid,branch]
# 用于删除 d_res_path 表的sql
    deleteressql = 'delete from d_res_path where res_id = %s'
#     插入版本迭代信息
#     d_model_resource表语句
    modelsql = """insert into d_model_resource (name,materialsid,source ,pid,creater,iswork) 
                values (%s,%s,%s,%s,%s,%s);    
            """
    args = [name,mid,branch,pid+1,creater,0]
#    插入d_res_path语句
    ressql = """
        insert into d_res_path (pid,res_id,path,filename,suffix,remark,fileid,iswork)
        select b.pid+1 ,%s,b.path ,b.filename,b.suffix,b.remark,b.fileid,0
         from d_res_path  b 
         inner join
         (select max(pid) maxpid,fileid from d_res_path a  where res_id = %s and iswork = 1 group by fileid) a
         where res_id = %s
         and iswork = 1
         and a.fileid = b.fileid
         and a.maxpid = b.pid
        """

    obj = Utils()
    nowresId = obj.searchOneP(nowresSql,nowresargs)[0]
    ismodelexist = obj.searchListP(ismoodelsql,ismodelargs)
    # print(ismodelexist)
    if ismodelexist == ():
        resid = obj.create(modelsql,args)
        resArgs = [resid,nowresId,nowresId]
        resInsertres = obj.create(ressql,resArgs)
    elif ismodelexist.__len__() == 1 :
        resid = ismodelexist[0][0]

    elif ismodelexist.__len__() > 1:
        # 解除安全模式
        obj.modify('SET SQL_SAFE_UPDATES=0')
        for res in ismodelexist:
            resid = [res[0],]
            obj.modifyP(deleteressql,resid)
        obj.modifyP(deletemodel,deleteModelArgs)

        resid = obj.create(modelsql,args)
        resArgs = [resid,nowresId,nowresId]
        resInsertres = obj.create(ressql,resArgs)
    ismodelexist = obj.searchListP(ismoodelsql,ismodelargs)
    print(ismodelexist)
    obj.commit()
    obj.close()
    return resid


