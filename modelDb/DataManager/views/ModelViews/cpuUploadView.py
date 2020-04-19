from django.shortcuts import render
from DataManager.Models.uploadModels import *
from DataManager.Models.uploadModels import FileUpload
from django.shortcuts import redirect
from dao.uitlsPlus import *

from DataManager.Models.cpuUploadModel import *

uList = getUsers()
ulist = {}

for i in uList:
    ulist[i[0]] = i[3]

def cpuUpload(request):
    if request.method == 'GET':

        id = request.GET.get('id')
        #提交
        if id is None:
            return render(request,'modelHtml/cpuUpload.html',{'user_list':ulist,'button':'<input type="submit" value=''提交'' class="btn btn-primary w-100" style="margin-bottom: 20px;"></input>'})
        #修改
        else:
            mList,cpuList=getLists(id)
            print(mList)
            uid=int(mList[0][9])
            choice = {mList[0][9]:ulist.get(int(mList[0][9]))}
            # del ulist[uid]
            user={}
            user.update(choice)
            user.update(ulist)
            return render(request,'modelHtml/cpuUpload.html',{'user_list':user,'mList':mList[0],'cpuList':cpuList[0],'button':'<input type="submit" value=''修改'' class="btn btn-primary w-100" style="margin-bottom: 20px;"></input>'})

    else :
        #从request获取model表id
        mid = request.POST.get('mid')
        #新增数据
        if str(mid) == '':
            mid = insertCpu(request=request)
            return redirect('/CPU/?id='+str(mid))
        #update
        else:
            mid = editCpu(request)
            return redirect('/CPU/?id='+str(mid))
