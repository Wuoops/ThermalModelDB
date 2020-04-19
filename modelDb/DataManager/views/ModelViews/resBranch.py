from django.shortcuts import render
from DataManager.Models.resBranchModel import *
from django.shortcuts import redirect
from DataManager.Models.uploadModels import FileUpload
from dao.uitlsPlus import *

def resBranch(request):

    if request.method == 'GET':
        id = request.GET.get('id')
        branch = request.GET.get('branch')
        if (branch is None):
            # return redirect('/newBranchAndUpload/')
            mid = request.GET.get('id')
            materList = getMaterInfo(mid)
            # dic,list,allBranckDict = resBranchmod(request)
            userList = getUserList()
            userDic = changeListToDIct(userList)
            branchList = getBranchList()
            branchDic=changeListToDIct(branchList)
            dic,list,allBranckDict = resBranchmod(request)

            # return render(request,'uploadPage/branch.html',{'branch_set':'<div class="col"><td><input type="submit" value="版本分支设置" class="btn btn-info w-100"></td></div>','list':materList,'user_list':userDic,'branch_list':branchDic})
            return render(request,'uploadPage/branch.html',{'branch_set':'<div class="col"><td><input type="submit" value="版本分支设置" class="btn btn-info w-100"></td></div>','list':list,'user_list':dic,'branch_list':allBranckDict})

        else:
            dic,list,allBranckDict = resBranchmod(request)
            return render(request,'uploadPage/branch.html',{'list':list,'user_list':dic,'branch_list':allBranckDict})
    else :
        #POST请求过来
        file = request.FILES.get('files',None)
        if file == None:
            pass
        else:
            print(request.POST)
            get_mater_sql='select name,type,s.id from d_materials s where s.id = %s'
            gm_args = [request.POST.get('mid')]

            sql = 'insert into d_model_resource (name,type,materialsid,source,pid,path,creater,remark) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)'

            args = [request.POST.get('branch'),request.POST.get('version'),file.name,request.POST.get('owner'),request.POST.get('remarks')]

            obj = Utils()
            mater = obj.searchOneP(get_mater_sql,gm_args)
            a = tuple(args)

            materlist_args = mater+a
            print(materlist_args)
            obj.create(sql,materlist_args)
            obj.commit()
            obj.close()
            f = FileUpload(fileUl=file)
            f.save()
        # return render(request,'uploadPage/branch.html')
        return redirect('/resource/?id='+str(request.POST.get('mid')))
