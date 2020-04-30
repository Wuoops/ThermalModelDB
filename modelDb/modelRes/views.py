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
@login_required
def upload(request):
    list = model_search()
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
    # print(posts)
    return render(request,'uploadPage.html',{'posts':posts,'pagemax':pagemax})
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

            # return render(request,'uploadPage/branch.html',{'branch_set':'<div class="col"><td><input type="submit" value="版本分支设置" class="btn btn-info w-100"></td></div>','list':materList,'user_list':userDic,'branch_list':branchDic})
            return render(request,'branch.html',{'branch_set':'<div class="col"><td><input type="submit" value="版本分支设置" class="btn btn-info w-100"></td></div>','list':list,'user_list':dic,'branch_list':allBranckDict})

        else:
            dic,list,allBranckDict = resBranchmod(request)
            return render(request,'branch.html',{'list':list,'user_list':dic,'branch_list':allBranckDict})
    else :
        #POST请求过来
        file = request.FILES.getlist('files')

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
            FileUpload(file,ftpPath)
        # return render(request,'uploadPage/branch.html')
        return redirect('/resource/?id='+str(request.POST.get('mid')))

@login_required
def resource(request):

    mid = request.GET.get('id')
    #版本分支刘表
    branchList = getBranchList()
    branch_list= changeListToDIct(branchList)
    #数据列表
    list = resourceModel(mid)
    current_page = request.GET.get('page')
    paginator = Paginator(list,10)
    try:
        posts = paginator.page(current_page)
    except PageNotAnInteger as e :
        posts = paginator.page(1)
    except EmptyPage as e :
        posts = paginator.page(1)
    pagemax=paginator.num_pages


    #获取ftp地址
    ftpAddr = Config.ftpdAddr

    #左侧详情
    materInfo = getMaterByid(str(mid))

    #根据物料ID查询物料信息
    res = getMaterTags(mid)
    kList = []
    vList = []
    for tags in res:
        kList.append(tags[1])
        vList.append(tags[2])
    #将两个list合并成一个dict
    taglist = listsTodict(kList,vList)

    return render(request,'resource.html',{'posts':posts,'branch_list':branch_list,'mid':mid,'ftpAddr':ftpAddr,'materInfo':materInfo,'taglist':taglist})
#############################
#数据上传
from django.views.generic.edit import FormView
from .forms import FileFieldForm

class FileFieldView(FormView):
    form_class = FileFieldForm
    template_name = 'upload.html'  # Replace with your template.
    success_url = '...'  # Replace with your URL or reverse().

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        if form.is_valid():
            for f in files:
                ...  # Do something with each file.
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
