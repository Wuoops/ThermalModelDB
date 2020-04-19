from django.shortcuts import render
from django.http import HttpResponse
from DataManager.Models.uploadModels import *

from dao.uitlsPlus import *
from django.shortcuts import redirect


uList = getUsers()
ulist = {}
for i in uList:
    ulist[i[0]] = i[3]

def save_file(file):
    with open(file,'wb') as fp:
        for chunk in file.chunks():
            fp.write(chunk)


def dimmul(request):

    if request.method == 'GET':
        return render(request,'modelHtml/dimmUpload.html',{'user_list':ulist})
    else :

        list = request.POST
        print(list)

        sql_dimm='INSERT INTO d_dimm_materials (`bord`,`type`,`mem_name`,`frequency`,`size`,`ptd`,`other_tec`) VALUES (%s,%s,%s,%s,%s,%s,%s);'

        arg_dimm=(list['bord'],list['type'],list['name'],list['frequency'],list['size'],list['ptd'],list['other'])
        obj = Utils()
        id = obj.create(sql_dimm,arg_dimm)
        print(id)


        sql_model='INSERT INTO d_model (`name`,`type`,`source`,`model`,`creater`) VALUES(%s,%s,%s,%s,%s);'
        arg_mod=(list['name'],'DIMM',list['source'],id,list['creater'])
        mid=obj.create(sql_model,arg_mod)
        print(mid)
        obj.commit()
        obj.close()

        return redirect('/DIMM/?id='+str(id))

        # file = request.FILES.get('files')
        # save_file(file)
        # return render(request,'modelHtml/dimmUpload.html',{'user_list':ulist})
