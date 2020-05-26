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

def branchFilePageList(materialsid,source,pid):
    sql = """ 
            SELECT 
            MAX(pid) maxpid, res_id, fileid, filename, suffix, path
        FROM
            d_res_path
        WHERE
            res_id = (SELECT 
                    id
                FROM
                    d_model_resource
                WHERE
                    materialsid = %s AND source = %s
                        AND pid = %s)
        GROUP BY fileid , filename , suffix , res_id , path;
        """
    args = [materialsid,source,pid]
    obj = Utils()
    list = obj.searchListP(sql,args)
    getRemarksql = 'select remark  from d_res_path where pid = %s and res_id = %s and fileid = %s'
    ftpAddr = str(Config.ftpdAddr)
    resList = []
    for i in list:
        args = [i[0],i[1],i[3]]
        remark = obj.searchListP(getRemarksql,args)
        fname = fileNameforHtml(i[3])
        fullFtpAddr = ftpAddr+i[5]+'/'+fname
        j = i+remark[0]
        k = j+(fullFtpAddr,)
        resList.append(k)
    obj.close()
    return resList

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
