from django.shortcuts import render
from DataManager.Models.uploadModels import *
from DataManager.Models.uploadModels import FileUpload
# from DataManager.Models.FileUpload import FileUpload
from django.shortcuts import redirect

from dao.uitlsPlus import *
uList = getUsers()
ulist = {}
for i in uList:
    ulist[i[0]] = i[3]

def hddUpload(request):

    if request.method == 'GET':
        return render(request,'modelHtml/diskUpload.html',{'user_list':ulist})

    else :
        file = request.FILES.get('files',None)

        list = request.POST
        print(list)
        sql_dimm='INSERT INTO d_disk_materials (`bord`,`type`,`name`,`capacity`,`speed`,`ptd`,`socket`,`size`,`othertec`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);'
        arg_dimm=(list['bord'],list['type'],list['name'],list['capacity'],list['speed'],list['ptd'],list['socket'],list['size'],list['othertec'])
        obj = Utils()
        #dimm表id
        did = obj.create(sql_dimm,arg_dimm)
        print(did)

        if (list['source'] == 'MODIFY'):
            if(list['modify_source'] == ''):
                pass
            else:
                sql_model='INSERT INTO d_model (`name`,`type`,`source`,`modify_source`,`details`,`creater`) VALUES(%s,%s,%s,%s,%s,%s);'
                arg_mod=(list['name'],'DIMM',list['source'],int(list['modify_source']),did,list['creater'])
                #model表id
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
                    return redirect('/HDD/?id='+str(mid))

        else:
            sql_model='INSERT INTO d_model (`name`,`type`,`source`,`details`,`creater`) VALUES(%s,%s,%s,%s,%s);'
            arg_mod=(list['name'],'DISK',list['source'],did,list['creater'])
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



            return redirect('/DISK/?id='+str(mid))
