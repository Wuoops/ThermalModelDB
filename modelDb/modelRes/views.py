from django.core.paginator import Paginator,Page,PageNotAnInteger,EmptyPage
from .UTILS.util import *
from config import Config
from django.shortcuts import render
from DataManager.Models.resBranchModel import *
from django.shortcuts import redirect
from dao.uitlsPlus import *
from django.http import FileResponse
from config import *
from materials.Utils.utils import *


from django.contrib.auth.decorators import login_required
from config import Config
@login_required
def upload(request):
    lines = Config.lines
    typeData = getMaterList('type')
    brandData = getMaterList('brand')
    usrData = getMaterList('usr')
    current_page = request.GET.get('page')
    queryDict = request.GET.dict()
    # print(queryDict)
    list = model_search(queryDict)

    current_page = request.GET.get('page')
    if current_page is None:
        current_page = 1
    paginator = Paginator(list,lines)
    try:
        posts = paginator.page(current_page)
    except PageNotAnInteger as e :
        posts = paginator.page(1)
    except EmptyPage as e :
        posts = paginator.page(1)
    pagemax=paginator.num_pages
    # print(posts)
    return render(request,'uploadPage.html',{'posts':posts,'pagemax':pagemax,'page':current_page,'typeData':typeData,'brandData':brandData,'usrData':usrData})
@login_required
def resupload(request):
    mid = request.GET.get('id')
    #左侧详情
    materInfo = getMaterByid(str(mid))
    #获取封面html
    picHtml = getPicHtml(mid)
    #根据物料ID查询物料信息
    taglist = getMaterTagList(mid)
    #获取物料信息html
    materFileHtml = getMaterFileHtml(mid)
    dic,list,allBranckDict = resBranchmod(request)

    #数据列表
    list = resourceModel(mid)
    current_page = request.GET.get('page')
    if current_page is None:
        current_page = 1
    paginator = Paginator(list,10)
    try:
        posts = paginator.page(current_page)
    except PageNotAnInteger as e :
        posts = paginator.page(1)
    except EmptyPage as e :
        posts = paginator.page(1)
    pagemax=paginator.num_pages

    return render(request,'resourceUpload.html',{'page':current_page,'posts':posts,'branch_list':allBranckDict,\
                                           'mid':mid,'pagemax':pagemax,\
                                           'materInfo':materInfo,'taglist':taglist,'cover':picHtml,'materfile':materFileHtml})

#从版本分支页面进行数据上传
@login_required
def resBranch(request):
    mid = request.GET.get('id')

    #左侧详情
    materInfo = getMaterByid(str(mid))
    #获取封面html
    picHtml = getPicHtml(mid)
    #根据物料ID查询物料信息
    taglist = getMaterTagList(mid)
    #获取物料信息html
    materFileHtml = getMaterFileHtml(mid)
    # 获取版本信息
    branch = request.GET.get('branch')

    branchInfo = getBranchInfoByMaterId(mid,branch)
    #数据列表
    # list = resourceModel(mid)
    list = branchFilePageList(mid,branch)

    current_page = request.GET.get('page')
    if current_page is None:
        current_page = 1
    paginator = Paginator(list,10)
    try:
        posts = paginator.page(current_page)
    except PageNotAnInteger as e :
        posts = paginator.page(1)
    except EmptyPage as e :
        posts = paginator.page(1)
    pagemax=paginator.num_pages

    return render(request,'branch.html',{'page':current_page,'posts':posts,'branchInfo':branchInfo,\
                                       'mid':mid,'pagemax':pagemax,'branch':branch,\
                                       'materInfo':materInfo,'taglist':taglist,'cover':picHtml,'materfile':materFileHtml})
# 上传文件
@login_required
def resBranchFileupload(request):
    mid = request.POST.get('id')
    branch = request.POST.get('branch')

    file = request.FILES.getlist('files')
    print(file)
    if file == []:
        branch = request.POST.get('branch')
        return redirect('/resBranch/?id='+str(mid)+'&branch='+str(branch))
    else:
        strpath = 'model_'+str(mid)+str(branch)
        ftpPath = Config.ftpPath+strpath
        mkdir_p(ftpPath)
        #文件上传的方法
        fileNameList,suffixList = FileUpload(file,ftpPath)
        # 写入数据库
        # 获取res_id
        res_id,maxFid = newestModel(mid,branch)
        if(maxFid == None):
            maxFid = -1
        # 获取最大file_id
        sql = 'insert into d_res_path (pid,res_id,path,filename,suffix,fileid) values (%s,%s,%s,%s,%s,%s)'
        obj = Utils()
        for i in range(0,fileNameList.__len__()):
            fname = fileNameList[i]
            suffix = suffixList[i]
            args = [0,res_id,strpath,fname,suffix,int(maxFid)+i+1]
            obj.create(sql,args)
        obj.commit()
        obj.close()

        return redirect('/resBranch/?id='+str(mid)+'&branch='+str(branch))

@login_required
def resource(request):
    mid = request.GET.get('id')

    #左侧详情
    materInfo = getMaterByid(str(mid))
    #获取封面html
    picHtml = getPicHtml(mid)
    #根据物料ID查询物料信息
    taglist = getMaterTagList(mid)
    #获取物料信息html
    materFileHtml = getMaterFileHtml(mid)

    #数据列表
    list = resourceModel(mid)
    current_page = request.GET.get('page')
    if current_page is None:
        current_page = 1
    paginator = Paginator(list,10)
    try:
        posts = paginator.page(current_page)
    except PageNotAnInteger as e :
        posts = paginator.page(1)
    except EmptyPage as e :
        posts = paginator.page(1)
    pagemax=paginator.num_pages

    return render(request,'resource.html',{'page':current_page,'posts':posts,\
                                           'mid':mid,'pagemax':pagemax,\
                                           'materInfo':materInfo,'taglist':taglist,'cover':picHtml,'materfile':materFileHtml})


def historyFilePage(request):
    mid = request.GET.get('id')
    #左侧详情
    materInfo = getMaterByid(str(mid))
    #获取封面html
    picHtml = getPicHtml(mid)
    #根据物料ID查询物料信息
    taglist = getMaterTagList(mid)
    #获取物料信息html
    materFileHtml = getMaterFileHtml(mid)
    #数据列表
    # list = branchFilePageList(materialsid,source)
    resid = request.GET.get('resid')
    # print(resid)
    list = iterateFilePageList(resid)
    # print(list)
    current_page = request.GET.get('page')
    if current_page is None:
        current_page = 1
    paginator = Paginator(list,10)
    try:
        posts = paginator.page(current_page)
    except PageNotAnInteger as e :
        posts = paginator.page(1)
    except EmptyPage as e :
        posts = paginator.page(1)
    pagemax=paginator.num_pages
    return render(request,'branchfilepage.html',{'materInfo':materInfo,'taglist':taglist,'cover':picHtml,'materfile':materFileHtml,\
                                                 'page':current_page,'posts':posts,\
                                                    'mid':mid,'pagemax':pagemax})

def branchFilePage(request):
    mid = request.GET.get('id')
    #左侧详情
    materInfo = getMaterByid(str(mid))
    #获取封面html
    picHtml = getPicHtml(mid)
    #根据物料ID查询物料信息
    taglist = getMaterTagList(mid)
    #获取物料信息html
    materFileHtml = getMaterFileHtml(mid)
    materialsid = request.GET.get('id')
    source = request.GET.get('source')
    pid = request.GET.get('latest')
    #数据列表
    list = branchFilePageList(materialsid,source)
    current_page = request.GET.get('page')
    if current_page is None:
        current_page = 1
    paginator = Paginator(list,10)
    try:
        posts = paginator.page(current_page)
    except PageNotAnInteger as e :
        posts = paginator.page(1)
    except EmptyPage as e :
        posts = paginator.page(1)
    pagemax=paginator.num_pages
    return render(request,'branchfilepage.html',{'materInfo':materInfo,'taglist':taglist,'cover':picHtml,'materfile':materFileHtml,\
                                                 'page':current_page,'posts':posts,\
                                                    'mid':mid,'pagemax':pagemax})

def branchHistory(request):

    mid = request.GET.get('id')
    #左侧详情
    materInfo = getMaterByid(str(mid))
    #获取封面html
    picHtml = getPicHtml(mid)
    #根据物料ID查询物料信息
    taglist = getMaterTagList(mid)
    #获取物料信息html
    materFileHtml = getMaterFileHtml(mid)
    resid = request.GET.get('resid')
    branch = request.GET.get('source')
    #数据列表
    # list = historyList(resid,fileid)
    list = getHistoryList(mid,branch)

    current_page = request.GET.get('page')
    if current_page is None:
        current_page = 1
    paginator = Paginator(list,10)
    try:
        posts = paginator.page(current_page)
    except PageNotAnInteger as e :
        posts = paginator.page(1)
    except EmptyPage as e :
        posts = paginator.page(1)
    pagemax=paginator.num_pages

    return render(request,'branchHistory.html',{'materInfo':materInfo,'taglist':taglist,'cover':picHtml,'materfile':materFileHtml,\
                                               'page':current_page,'posts':posts,\
                                                    'mid':mid,'pagemax':pagemax })



def deletefile(request):

    pid = request.GET.get('pid')
    resid = request.GET.get('resid')
    fileid = request.GET.get('fileid')
    mid = request.GET.get('id')
    branch = request.GET.get('branch')

    sql = 'delete  from d_res_path where pid = %s and res_id = %s and fileid = %s'
    # sql = 'update d_res_path set iswork = 0 where pid = %s and res_id = %s and fileid = %s'
    args = [pid,resid,fileid]


    obj = Utils()
    obj.create(sql,args)
    obj.commit()
    obj.close()

    return redirect('/resBranch/?id='+str(mid)+'&branch='+str(branch))


def branchremark(request):
    mid = request.GET.get('id')
    branch = request.GET.get('branch')

    queryDict = request.GET.dict()

    sql = 'update d_res_path set remark = %s where pid = %s and res_id = %s and fileid = %s'
    obj = Utils()
    for k ,v in queryDict.items():
        if (k != 'id') & (k != 'branch'):
            # 将更改提交到数据库
            #解析Key中的数据
            pid,resid,fileid = str(k).split('_')
            args = [v,pid,resid,fileid]
            obj.create(sql,args)

    obj.commit()
    obj.close()
    return redirect('/resBranch/?id='+str(mid)+'&branch='+str(branch))

# 新增分支
def newBranch(request):
    mid = request.GET.get('id')
    branch = request.GET.get('branch')
    userId = request.session.get('_auth_user_id')

    # 根据ID查找和版本查找出该版本是否存在
    #
    res = branchExist(mid,branch,userId)

    return redirect('/resupload/?id='+str(mid))

# 文件迭代
def updateFile(request):
    mid = request.GET.get('id')
    branch = request.GET.get('branch')
    pid = request.GET.get('pid')
    resid = request.GET.get('resid')
    fileid = request.GET.get('fileid')


    return redirect('/resBranch/?id='+str(mid)+'&branch='+str(branch))

#版本迭代
def branchIterate(request):
    mid = request.GET.get('id')
    creater = request.session.get('_auth_user_id')
    branch = request.GET.get('branch')

    #左侧详情
    materInfo = getMaterByid(str(mid))
    #获取封面html
    picHtml = getPicHtml(mid)
    #根据物料ID查询物料信息
    taglist = getMaterTagList(mid)
    #获取物料信息html
    materFileHtml = getMaterFileHtml(mid)
    # 将数据迭代到d_model_resource和d_res_path表
    resId = iterate(mid,branch)
    # iterateResId = iterateRes[0][0]
    # 获取版本信息
    branchInfo = getBranchIterateInfo(mid,branch,creater,0)
    #数据列表
    list = iterateFilePageList(resId)
    # list = branchFilePageList(mid,branch)
    current_page = request.GET.get('page')
    if current_page is None:
        current_page = 1
    paginator = Paginator(list,10)
    try:
        posts = paginator.page(current_page)
    except PageNotAnInteger as e :
        posts = paginator.page(1)
    except EmptyPage as e :
        posts = paginator.page(1)
    pagemax=paginator.num_pages

    return render(request,'branchIterate.html',{'page':current_page,'posts':posts,'branchInfo':branchInfo,'iterateResId':resId,\
                                       'mid':mid,'pagemax':pagemax,'branch':branch,\
                                       'materInfo':materInfo,'taglist':taglist,'cover':picHtml,'materfile':materFileHtml})


# 放弃迭代
def giveupiterate(request):
    mid = request.GET.get('id')
    creater = request.session.get('_auth_user_id')
    branch = request.GET.get('branch')

    modelSql = 'select id from d_model_resource where materialsid = %s and source = %s and iswork = 0;'
    modelArgs = [mid,branch]
    obj = Utils()
    resid = obj.searchOneP(modelSql,modelArgs)
    delModelSql = 'delete from d_model_resource where materialsid = %s and source = %s and iswork = 0;'
    delResSql = 'delete from d_res_path where res_id = %s'
    print('done')
    obj.modifyP(delModelSql,modelArgs)
    obj.modifyP(delResSql,resid)
    obj.commit()
    obj.close()

    return redirect('/resBranch?id='+mid+'&branch='+branch)
#迭代确认
def iterateCommit(request):
    mid = request.GET.get('id')
    creater = request.session.get('_auth_user_id')
    branch = request.GET.get('branch')
    iterateResId = request.GET.get('iterateResId')

    queryDict = request.GET.dict()

    sql = 'update d_res_path set remark = %s where pid = %s and res_id = %s and fileid = %s'

    # 根据最新的resid将model_resource表和res_path表中的iswork更新为1
    updateModelResSql = 'update d_model_resource set iswork = 1 where id = %s '
    updatePathSql = 'update d_res_path set iswork = 1 where res_id = %s'
    args = [iterateResId,]

    obj = Utils()
    obj.modifyP(updateModelResSql,args)
    obj.modifyP(updatePathSql,args)

    for k ,v in queryDict.items():
        if (k != 'id') & (k != 'branch') & ( k != 'iterateResId'):
            print(k)
            # 将更改提交到数据库
            #解析Key中的数据
            m = str(k).split('_')
            print(m)
            pid = m[0]
            resid = m[1]
            fileid = m[2]
            args = [v,pid,resid,fileid]
            obj.create(sql,args)

    obj.commit()
    obj.close()

    return redirect('/resBranch?id='+mid+'&branch='+branch)

# 迭代版本文件上传
def iterateFileupload(request):
    mid = request.POST.get('id')
    creater = request.session.get('_auth_user_id')
    branch = request.POST.get('branch')
    iterateResId = request.POST.get('iterateResId')
    print(iterateResId)
    file = request.FILES.getlist('files')
    if file == []:
        branch = request.POST.get('branch')
        return redirect('/branchIterate/?id='+str(mid)+'&branch='+str(branch))
    else:

        strpath = 'model_'+str(mid)+str(branch)+'/'+str(iterateResId)
        ftpPath = Config.ftpPath+strpath
        mkdir_p(ftpPath)


        #文件上传的方法
        fileNameList,suffixList = FileUpload(file,ftpPath)
        # 写入数据库
        res_id,maxFid = newestModel(mid,branch)
        if(maxFid == None):
            maxFid = -1
        sql = 'insert into d_res_path (pid,res_id,path,filename,suffix,fileid,iswork) values (%s,%s,%s,%s,%s,%s,%s)'
        obj = Utils()
        for i in range(0,fileNameList.__len__()):
            fname = fileNameList[i]
            suffix = suffixList[i]
            args = [0,iterateResId,strpath,fname,suffix,int(maxFid)+i+1,0]
            obj.create(sql,args)
        obj.commit()
        obj.close()


    return redirect('/branchIterate/?id='+mid+'&branch='+branch)
