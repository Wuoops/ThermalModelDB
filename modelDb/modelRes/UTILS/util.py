from dao.uitlsPlus import *
import os
def resourceModel(mid):

    # mid = request.GET.get('id')
    sql = """
        SELECT
        `id`,
        `name`,
        `materialsid`,
        `pid`,
        `path`,
        `cover`,
        (
            SELECT
                u.owner_name
            FROM
                d_users u
            WHERE
                u.user_id = r.creater
        ) username,
        `remark`,
        DATE_FORMAT(
            r.create_date,
            "%%Y-%%m-%%d %%H:%%i:%%s"
        ) creattime,
        `modify_time`,
        `type`,
        (select ce.source_name from m_source ce where ce.source = r.source) sourcename,
        (select ce.color from m_source ce where ce.source = r.source) color,
        r.source,r.creater
    FROM
        d_model_resource r
        where materialsid = %s
        ORDER BY r.source ,r.id desc
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


#文件上传
def FileUpload(file,ftpPath):
    for obj in file:
        f = open(ftpPath+'/'+obj.name, 'wb')
        for chunk in obj.chunks():
            f.write(chunk)
        f.close()

#文件上传
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
