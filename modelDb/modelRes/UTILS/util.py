from dao.uitlsPlus import *
import os
from config import Config

def resourceModel(mid):

    # mid = request.GET.get('id')
    sql = """
         SELECT
        `name`,
        `materialsid`,
        (
            SELECT
                u.owner_name
            FROM
                d_users u
            WHERE
                u.user_id = r.creater
        ) username,
        (select ce.source_name from m_source ce where ce.source = r.source) sourcename,
        (select ce.color from m_source ce where ce.source = r.source) color,
		source,max(pid) latest
    FROM
        d_model_resource r
        where materialsid = %s
        group by source,name,materialsid,creater      
    """
    obj = Utils()
    list = obj.searchListP(sql,mid)
    obj.close()
    return list


def getUsers():
    obj = Utils()
    sql = 'select * from d_users'
    uList = obj.searchList(sql)
    return uList


#文件上传并返回文件信息列表
def FileUpload(file,ftpPath):
    fileNameList = []
    suffixList = []

    for obj in file:
        suffix = os.path.splitext(str(obj.name))[1]
        fileNameList.append(str(obj.name))
        suffixList.append(str(suffix))
        f = open(ftpPath+'/'+obj.name, 'wb')
        for chunk in obj.chunks():
            f.write(chunk)
        f.close()

    return fileNameList,suffixList

#文件上传并重命名并返回文件信息列表
def FileUploadRename(file,ftpPath,fileName):
    for obj in file:
        f = open(ftpPath+'/'+fileName, 'wb')
        for chunk in obj.chunks():
            f.write(chunk)
        f.close()


#判断文件夹是否存在，如果不存在则创建一个
def mkdir_p(path):
    if (os.path.exists(path) == False):
        os.mkdir(path)

#清空文件夹中的所有文件
def deleteFileFromPath(path):
    if (os.path.exists(path) == False):
        os.mkdir(path)
#将字符串中的空格替换为%20
def fileNameforHtml(fileName):
    return fileName.replace(' ','%20')
# 获取res_id
def newestModel(mid,branch):
    sql = 'SELECT max(id) FROM d_model_resource WHERE materialsid = %s AND source = %s and iswork = 1'
    args = [mid,branch]
    maxFidsql ='select max(fileid) from d_res_path where res_id = %s'
    obj = Utils()
    id = obj.searchOneP(sql,args)
    maxFid = obj.searchOneP(maxFidsql,id)
    obj.close()
    return id[0],maxFid[0]

def branchFilePageList(materialsid,source):
    sql = """SELECT
           MAX(pid) maxpid, res_id, fileid
        FROM
            d_res_path
        WHERE
            res_id = (SELECT 
                   max(id)
                FROM
                    d_model_resource
                WHERE
                    materialsid = %s AND source = %s
                    and iswork = 1
            )
        and iswork = 1
        GROUP BY fileid , res_id ;
        """
    args = [materialsid,source]
    obj = Utils()
    list = obj.searchListP(sql,args)
    getRemarksql = 'select remark,path,filename ,suffix ,id from d_res_path  where pid = %s and res_id = %s and fileid = %s'
    ftpAddr = str(Config.ftpdAddr)
    resList = []
    for i in list:
        args = [i[0],i[1],i[2]]
        details = obj.searchOneP(getRemarksql,args)
        fname = fileNameforHtml(details[2])
        fullFtpAddr = ftpAddr+details[1]+'/'+fname
        j = i+details
        k = j+(fullFtpAddr,)
        resList.append(k)
    obj.close()
    return resList

# print(branchFilePageList('100092','c'))

def iterateFilePageList(iterateResId):
    sql = """select  pid, res_id, fileid ,remark,path,filename ,suffix ,id from d_res_path  where res_id = %s """
    args = [iterateResId,]
    obj = Utils()
    list = obj.searchListP(sql,args)
    ftpAddr = str(Config.ftpdAddr)
    resList = []
    for i in list:
        fname = fileNameforHtml(i[5])
        fullFtpAddr = ftpAddr+i[4]+'/'+fname
        k = i+(fullFtpAddr,)
        resList.append(k)
    obj.close()
    return resList
# print(branchFilePageList('100092','c'))
# print(iterateFilePageList('193'))

def historyList(resid,fileid):
    sql = """ SELECT * FROM d_res_path where res_id = %s and fileid = %s """
    args = [resid,fileid]
    obj = Utils()
    list = obj.searchListP(sql,args)
    ftpAddr = str(Config.ftpdAddr)
    resList = []
    for i in list:
        fname = fileNameforHtml(i[4])
        fullFtpAddr = ftpAddr+i[3]+'/'+fname
        k = i+(fullFtpAddr,)
        resList.append(k)
    obj.close()
    return resList

def getHistoryList(mid,branch):
    sql = """
    select name ,pid,
        (select m.source_name from  m_source m where m.source = res.source ) branch,
        (select owner_name from d_users u where u.user_id = creater) owner_name,remark ,id,source,materialsid 
     from d_model_resource res where materialsid = %s and source = %s
     and iswork = 1
     """
    args = [mid,branch]
    obj = Utils()
    res = obj.searchListP(sql,args)
    # print(res)
    obj.close()

    return res


# 将文件信息安排到数据库
def fileInfoToResPath(fileNameList,suffixList,resid,path):
    sql = 'insert into d_res_path (pid,res_id,path,filename,suffix,fileid) values(%s,%s,%s,%s,%s,%s)'
    obj = Utils()
    for i in (range(0,fileNameList.__len__())):
        print(fileNameList[i])
        args=[0,resid,path,fileNameList[i],suffixList[i],i]
        obj.create(sql,args)
    obj.commit()
    obj.close()


# 获取文件信息
def getFileList():
    pass

# 获取模型表ID
#先判断是否存在该数据，不存在则创建返回id存在则直接返回id
def getmodelresTabId(materialsid,branch):
    # 判断是否存在该数据
    sql = 'select max(id) id from d_model_resource where materialsid = %s and source  = %s'
    args = [materialsid,branch]
    obj = Utils()
    res_id = obj.searchOneP(sql,args)
    # 创建该条记录
    if res_id[0] is None:
        print('null')
        createsql = 'insert into d_model_resource (materials,source) values(%s,%s)'
        args = [materialsid,branch]
    else:
        return res_id

# 根据ID查找和版本查找出该版本是否存在
def branchExist(mid,branch,userId):
    sql = 'select count(*) num from d_model_resource where materialsid = %s and source = %s'
    args =[mid,branch]
    getName = 'select name from d_materials d where d.id = %s'
    obj = Utils()
    res = obj.searchOneP(sql,args)[0]
    name = obj.searchOneP(getName,[mid,])[0]
    if res == 0:
        createsql = 'insert  into d_model_resource (name,materialsid,source,pid,creater) values(%s,%s,%s,%s,%s)'
        args = [name,mid,branch,0,userId]
        obj.create(createsql,args)
        obj.commit()
        obj.close()
        return 1
    else:
        return 0


# a = branchFilePageList('100092','c')
# print(a)
