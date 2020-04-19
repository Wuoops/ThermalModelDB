from dao.uitlsPlus import *
from django.db import models
from django.core.files.storage import FileSystemStorage


def getUsers():
    obj = Utils()
    sql = 'select * from d_users'
    uList = obj.searchList(sql)
    return uList

#插入CPU表
def instertCpuTable(list):
    sql_cpu="""INSERT INTO d_cpu_model
        (`instractionSet`,
        `bord`,
        `platform`,
        `code`,
        `series`,
        `family`,
        `genoration`,
        `cpu_name`,
        `core`,
        `threads`,
        `frequency`,
        `turbo`,
        `process`,
        `TDP`,
        `suatus`,
        `launchDate`,
        `socket`,
        `cache`,
        `mem_max`,
        `mem_type`,
        `mem_ecc`,
        `gpu_inside`,
        `gpu_name`)
        VALUES
        (%s,%s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s,%s,
        %s,%s);"""
    arg_cpu=(list['instractionSet'],list['bord'],list['platform'],list['code'],list['series'],
                list['family'],list['genoration'],list['name'],list['core'],
                list['threads'],list['frequency'],list['turbo'],list['process'],
                list['TDP'],list['suatus'],list['launchDate'],list['socket'],
                list['cache'],list['mem_max'],list['mem_type'],list['mem_ecc'],
                list['gpu_inside'],list['gpu_name'],)
    obj = Utils()
    #cpu表id
    cid = obj.create(sql_cpu,arg_cpu)
    return cid
#update CPU表
def updateCpuTable():
    pass



#文件上传
class FileUpload(models.Model):
    fileUl = models.FileField(upload_to='files')
