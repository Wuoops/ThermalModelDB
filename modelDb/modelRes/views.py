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
    #版本分支刘表
    branchList = getBranchList()
    branch_list={}
    for i in branchList:
        branch_list[i[0]]=i[1]
    # print(branch_list)
    #数据列表
    list = resourceModel(mid)
    # print(list)
    current_page = request.GET.get('page')
    paginator = Paginator(list,10)
    try:
        posts = paginator.page(current_page)
    except PageNotAnInteger as e :
        posts = paginator.page(1)
    except EmptyPage as e :
        posts = paginator.page(1)
    pagemax=paginator.num_pages

    return render(request,'resourceUpload.html',{'posts':posts,'branch_list':branch_list,'mid':mid})
#从版本分支页面进行数据上传
@login_required
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

            branchset = """<div class="col"><td><input onclick="window.document.location = '/branchSet?id=%s' " type="button" value="版本分支设置" class="btn btn-info w-100"></td></div>""" %mid
            return render(request,'branch.html',{'branch_set':branchset,'list':list,'user_list':dic,'branch_list':allBranckDict})
        else:
            dic,list,allBranckDict = resBranchmod(request)
            return render(request,'branch.html',{'list':list,'user_list':dic,'branch_list':allBranckDict})
    else :
        #POST请求过来
        file = request.FILES.getlist('files')
        print(file)
        if file == None:
            pass
        else:
            """
            select * from d_model_resource;
            在该表中的path字段中填写如下拼接字符
            'rp'+id+source+pid
                （意义为rp = resource path+表id+版本号+迭代版本）
            生成唯一字符串
            以该字符串在FTP目录创建文件夹
            将所有相关文件上传到该文件夹当中
            
            下载的时候访问该文件夹相关的FTP服务地址即可
            """
            #用于获取物料（material）信息的sql
            get_mater_sql='select name,type,s.id from d_materials s where s.id = %s'
            gm_args = [request.POST.get('mid')]
            #用于插入模型表的sql
            sql = 'insert into d_model_resource (name,type,materialsid,source,pid,path,creater,remark) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)'
            branch = request.POST.get('branch')
            pid = request.POST.get('version')
            path = 'DefaultPath'
            # owner = request.POST.get('owner')
            owner = request.session.get('_auth_user_id')
            remark = request.POST.get('remarks')
            args = [branch,pid,path,owner,remark]

            #update sql
            updatsql =  'update d_model_resource set path = %s where id = %s'


            obj = Utils()
            #物料信息
            mater = obj.searchOneP(get_mater_sql,gm_args)
            a = tuple(args)
            #整合为插入数据库所需参数
            materlist_args = mater+a
            print(materlist_args)
            #插入数据库
            did = obj.create(sql,materlist_args)
            print(did)
            #根据d_model_resource_id更新d_model_resource表path数据
            strpath = 'rp_'+str(did)+str(branch)+str(pid)
            argPath = (strpath,did)
            obj.create(updatsql,argPath)
            obj.commit()
            obj.close()

            #确定文件上传路径
            ftpPath = Config.ftpPath+strpath
            mkdir_p(ftpPath)
            #文件上传的方法
            fileNameList,suffixList = FileUpload(file,ftpPath)
            #将文件信息写入数据库
            print(fileNameList)
            print(suffixList)

        return redirect('/resource/?id='+str(request.POST.get('mid')))

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
    list = branchFilePageList(materialsid,source,pid)
    print(list)
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
    fileid = request.GET.get('fileid')
    #数据列表
    list = historyList(resid,fileid)
    print(list)
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


