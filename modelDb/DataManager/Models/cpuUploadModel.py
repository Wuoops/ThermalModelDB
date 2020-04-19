from dao.uitlsPlus import *
from DataManager.Models.uploadModels import *
from django.shortcuts import render
from django.shortcuts import redirect

def getLists(id):

    obj = Utils()

    sql = 'select * from d_cpu_materials where id = %s'
    model_sql = 'select * from d_materials where id = %s'

    obj.connectDB()
    model = obj.searchListP(model_sql,id)
    theCpu = obj.searchListP(sql,model[0][6])

    obj.close()
    return model,theCpu

#update CPU的方法
def updateCPU(list,mid,cid):

    #     #更新这两个表的数据
    #     #返回model表id就行了
    #     sqlModelUpdate='update d_materials set name = %s , source = %s, modify_source = %s ,creater = %s where id = %s'

    sqlCpuUpdate="""UPDATE d_cpu_materials SET `instractionSet` = %s, `bord` = %s, `platform` = %s, `code` = %s, `series` = %s, `family` = %s, `genoration` = %s, `cpu_name` = %s, `core` = %s, `threads` = %s, `frequency` = %s, `turbo` = %s, `process` = %s, `TDP` = %s, `suatus` = %s, `launchDate` = %s, `socket` = %s, `cache` = %s, `mem_max` = %s, `mem_type` = %s, `mem_ecc` = %s, `gpu_inside` = %s, `gpu_name` = %s WHERE id = %s"""
    if (list['source'] == 'MODIFY'):
        sqlModelUpdate='update d_materials set name = %s , source = %s, modify_source = %s ,creater = %s where id = %s'
        modArgs=(list['name'],list['source'],int(list['modify_source']),list['creater'],mid)

    else:
        sqlModelUpdate='update d_materials set name = %s , source = %s ,creater = %s where id = %s'
        modArgs=(list['name'],list['source'],list['creater'],mid)

    cpuArgs=(list['instractionSet'],list['bord'],list['platform'],list['code'],list['series'],
            list['family'],list['genoration'],list['name'],list['core'],
            list['threads'],list['frequency'],list['turbo'],list['process'],
            list['TDP'],list['suatus'],list['launchDate'],list['socket'],
            list['cache'],list['mem_max'],list['mem_type'],list['mem_ecc'],
            list['gpu_inside'],list['gpu_name'],cid)
    obj = Utils()
    obj.modifyP(sqlModelUpdate,modArgs)
    obj.modifyP(sqlCpuUpdate,cpuArgs)
    obj.commit()
    obj.close()

#修改cpu
def editCpu(request):
    #获取model表id
    mid = request.POST.get('mid')
    #获取cpu表的id
    cid = request.POST.get('cid')
    file = request.FILES.get('files',None)
    list = request.POST
    print(list)
    #没有重新上传
    if file == None:
        updateCPU(list,mid,cid)

    #重新上传文件
    else:

        updateCPU(list,mid,cid)
        sqlResource='update d_resource set path = %s where mod_id = %s'
        arg_res=(file.name,mid)
        obj = Utils()
        obj.modifyP(sqlResource,arg_res)
        # save_file(file)
        f = FileUpload(fileUl=file)
        f.save()
        obj.commit()
        obj.close()
    return mid


#插入一条cpu
def insertCpu(request):
    file = request.FILES.get('files',None)
    list = request.POST
    print(list)

    sql_cpu="""INSERT INTO d_cpu_materials
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
    print(cid)

    # cid = instertCpuTable(list)

    # if (list['source'] == 'MODIFY'):
    #     if(list['modify_source'] == ''):
    #         pass
    #     else:
    #         sql_model='INSERT INTO d_materials (`name`,`type`,`source`,`modify_source`,`details`,`creater`) VALUES(%s,%s,%s,%s,%s,%s);'
    #         arg_mod=(list['name'],'CPU',list['source'],int(list['modify_source']),cid,list['creater'])
    #         #model表id
    #         mid=obj.create(sql_model,arg_mod)
    #         if file == None:
    #             pass
    #         else:
    #             print('将文件'+file.name+'找个地方放着，同时放到那个resource表里面')
    #             sql_res = 'INSERT INTO d_resource (`mod_id`,`path`) VALUES(%s,%s);'
    #             arg_res=(mid,file.name)
    #             fid=obj.create(sql_res,arg_res)
    #             f = FileUpload(fileUl=file)
    #             f.save()
    #             obj.commit()
    #             obj.close()
    #             return redirect('/CPU/?id='+str(mid))
    #
    # else:
    #     sql_model='INSERT INTO d_materials (`name`,`type`,`source`,`details`,`creater`) VALUES(%s,%s,%s,%s,%s);'
    #     arg_mod=(list['name'],'CPU',list['source'],cid,list['creater'])
    #     mid=obj.create(sql_model,arg_mod)
    #     if file == None:
    #         pass
    #     else:
    #         print('将文件'+file.name+'找个地方放着，同时放到那个resource表里面')
    #         sql_res = 'INSERT INTO d_resource (`mod_id`,`path`) VALUES(%s,%s);'
    #         arg_res=(mid,file.name)
    #         fid=obj.create(sql_res,arg_res)
    #         # save_file(file)
    #         f = FileUpload(fileUl=file)
    #         f.save()
    #     obj.commit()
    #     obj.close()
    #
    #     return mid
        # return redirect('/CPU/?id='+str(mid))

    sql_model='INSERT INTO d_materials (`name`,`type`,`details`,`creater`,`tdp`) VALUES(%s,%s,%s,%s,%s);'
    arg_mod=(list['name'],'CPU',cid,list['creater'],list['TDP'])
    mid=obj.create(sql_model,arg_mod)
    if file == None:
        pass
    else:
        print('将文件'+file.name+'找个地方放着，同时放到那个resource表里面')
        sql_res = 'INSERT INTO d_resource (`mod_id`,`path`) VALUES(%s,%s);'
        arg_res=(mid,file.name)
        fid=obj.create(sql_res,arg_res)
        # save_file(file)
        f = FileUpload(fileUl=file)
        f.save()
    obj.commit()
    obj.close()

    return mid
