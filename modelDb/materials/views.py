from django.shortcuts import render,redirect,HttpResponse
from django.core.paginator import Paginator,Page,PageNotAnInteger,EmptyPage
from .Utils.utils import *
from django.utils.safestring import mark_safe
from modelRes.UTILS.util import *
from django.contrib.auth.decorators import login_required
import re
from config import Config
from dao.uitlsPlus import Utils
#materials主页
@login_required
def materials(request):

    lines = Config.lines
    typeData = getMaterList('type')
    brandData = getMaterList('brand')
    usrData = getMaterList('usr')
    current_page = request.GET.get('page')
    queryDict = request.GET.dict()
    # print(queryDict)
    list = model_search(queryDict)

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



    issuper = request.user.is_superuser
    if issuper:
        superbtn = '<button type="button" class="btn-sm btn-info" onclick="window.document.location = %s" >修改</button>'
        return render(request,'materials.html',{'posts':posts,'typeData':typeData,'brandData':brandData,'usrData':usrData,'pagemax':pagemax,'page':current_page})
    else:
        return render(request,'materials.html',{'posts':posts,'typeData':typeData,'brandData':brandData,'usrData':usrData,'pagemax':pagemax,'page':current_page})


#创建物料页
@login_required
def createMaterial(request):
    userId = request.session.get('_auth_user_id')
    massage = """<tr><td>%s</td></tr>"""
    #获取Type表数据
    typeData = getMaterList('type')
    #获取CPU Platform 和Code 信息
    platformList = getPlatformList()
    codeList = getCodeList()
    if request.method == 'GET':
        return render(request,'createMaterial.html',{'typeData':typeData,'platformList':platformList,'codeList':codeList})
    else:
        type = request.POST.get('type')
        brand= request.POST.get('brand')
        name = request.POST.get('name')
        tdp = request.POST.get('TDP')
        platform = request.POST.get('platform')
        code = request.POST.get('code')
        next = request.POST.get('next')
        spec = request.POST.get('SPEC')
        # temptype = request.POST.get('temptype')
        print(code)
        if (type == '' or brand == '' or name == ''):
            massage = mark_safe(massage % '什么也没做')
            return render(request,'createMaterial.html',{'typeData':typeData,'massage':massage})
        elif(str(type).upper() == 'CPU'):
            if (platform == '' and code == ''):
                # print('缺少CPU平台或代号信息')
                massage = mark_safe(massage % '缺少CPU平台或代号信息')
                return render(request,'createMaterial.html',{'typeData':typeData,'type':type,'brand':brand,'name':name,'massage':massage,'platformList':platformList,'codeList':codeList})
            else:
                #填写到数据库
                print('将CPU数据填写到数据库')
                res = insertCpuTomaterial(request,userId)
        else:
            #填写到数据库
            print('将其他元器件的数据填写到数据库')
            res =insertOther(request,userId)

        if res == -1:
            massage = mark_safe(massage % 'TDP和SPEC应为数字')
            return render(request,'createMaterial.html',{'typeData':typeData,'type':type,'brand':brand,'name':name,'platform':platform,'code':code,'massage':massage,'platformList':platformList,'codeList':codeList})
        elif res == 'tdp' :
            massage = mark_safe(massage % 'TDP应为数字')
            return render(request,'createMaterial.html',{'typeData':typeData,'type':type,'brand':brand,'name':name,'platform':platform,'code':code,'SPEC':spec,'massage':massage,'platformList':platformList,'codeList':codeList})
        elif res == 'spec':
            massage = mark_safe(massage % 'SPEC应为数字')
            return render(request,'createMaterial.html',{'typeData':typeData,'type':type,'brand':brand,'name':name,'platform':platform,'code':code,'TDP':tdp,'massage':massage,'platformList':platformList,'codeList':codeList})
        elif res is None:
            print('DO NOTHING')
        else:
            if (next == '仅提交'):
                return redirect('/materials')
            elif(next == '提交并完善详细信息'):
                print('跳转到对应的详细数据上传页')
                return redirect('/createtags?id='+str(res))
            elif(next == '提交并上传模型'):
                print('跳转模型上传页')
                return redirect('/resupload/?id='+str(res))


#创建物料标签
@login_required
def createMaterialTags(request):
    mid = request.POST.get('id')
    if request.method == 'POST' :
        queryDict = request.POST.dict()
        num = 1
        kList=[]
        vList=[]
        for k ,v in queryDict.items():
            print(k)
            if k != 'id':
                matchObj = re.search( str(num),k,re.M|re.I)
                if matchObj:
                    kList.append(v)
                    num=num+1
                else:
                    vList.append(v)
        print(kList)
        print(vList)
        sql = 'insert into d_materials_tag values(%s,%s,%s)'
        daoPlus = Utils()
        delsql = 'delete from d_materials_tag where materid = '+str(mid)
        daoPlus.modify(delsql)
        for i in range(0,len(kList)):
            args=[mid,kList[i],vList[i]]
            daoPlus.modifyP(sql,args)
        daoPlus.commit()
        daoPlus.close()
        return redirect('/resource?id='+str(mid))
    else:
        mid = request.GET.get('id')

        #获取ftp地址
        ftpAddr = Config.ftpdAddr
        ftpPath = Config.ftpPath
        #物料附件地址
        materFileAddr = ftpAddr+'materFile/mater'+mid
        materFilePath = ftpPath+'materFile/mater'+mid
        if (os.path.exists(materFilePath) == False):
            materFileHtml = "<div></div>"
        else:
            materFileHtml="""<a href='"""+materFileAddr+"""' class="btn btn-success w-100">查看附件</a>"""


        #获取封面
        picAddr,cover = getCover(mid)
        if cover == None:
            picHtml = """<div></div>"""
        else:
            picHtml = """<div onclick="window.open('"""+picAddr+"""')"><img src="""+picAddr+""" class="w-100"/></div>"""
        #获取物料信息
        materInfoList = getMaterByid(mid)
        #根据物料ID查询物料信息
        res = getMaterTags(mid)
        num = res.__len__()
        kList = []
        vList = []
        for tags in res:
            kList.append(tags[1])
            vList.append(tags[2])
        #将两个list合并成一个dict
        taglist = listsTodict(kList,vList)
        return render(request,'createMaterialTags.html',{"mid":mid,'materInfoList':materInfoList,\
                                                         'taglist':taglist,'num':num,'cover':picHtml,'materfile':materFileHtml})


#更新标签
@login_required
def updateMaterialTags(request):

    queryDict = request.POST.dict()

    sql = 'update d_materials_tag set tag_v = %s where tag_k =%s '
    daoPlus = Utils()
    for k ,v in queryDict.items():
        args = [v,k]
        daoPlus.modifyP(sql,args)

    daoPlus.commit()
    daoPlus.close()

    mid = request.POST.get('id')
    return redirect('/resource?id='+str(mid))

#更新物料信息
@login_required
def updateMaterial(request):
    mid = request.GET.get('id')
    massage = """<tr><td>%s</td></tr>"""
    userId = request.session.get('_auth_user_id')

    #根据物料ID查询物料信息
    materInfo = getMaterByid(str(mid))
    print(materInfo)
    type = materInfo[6]
    brand = materInfo[5]
    tdp =  materInfo[7]
    spec = materInfo[8]
    platform = materInfo[3]
    code = materInfo[4]
    name = materInfo[0]
    #获取Type表数据
    typeData = getMaterList('type')
    typeData = listpTotop(type,typeData)
    #获取CPU Platform 和Code 信息
    platformList = getPlatformList()
    if platform is not None:
        platformList = listpTotop(platform,platformList)
    codeList = getCodeList()
    if code is not None:
        codeList = listpTotop(code,codeList)

    if tdp is  None:
        tdp = ''
    if spec is  None:
        spec = ''
    if request.method == 'GET':
        return render(request,'updateMaterial.html',{'typeData':typeData,'platformList':platformList,'codeList':codeList,'brand':brand,'TDP':tdp,'SPEC':spec,'name':name})
    #提交
    else:
        type = request.POST.get('type')
        brand= request.POST.get('brand')
        name = request.POST.get('name')
        tdp = request.POST.get('TDP')
        platform = request.POST.get('platform')
        code = request.POST.get('code')
        next = request.POST.get('next')
        spec = request.POST.get('SPEC')

        if (type == '' or brand == '' or name == ''):
            massage = mark_safe(massage % '什么也没做')
            return render(request,'updateMaterial.html',{'typeData':typeData,'massage':massage})
        elif(str(type).upper() == 'CPU'):
            if (platform == '' and code == ''):
                # print('缺少CPU平台或代号信息')
                massage = mark_safe(massage % '缺少CPU平台或代号信息')
                return render(request,'updateMaterial.html',{'typeData':typeData,'type':type,'brand':brand,'name':name,'massage':massage,'platformList':platformList,'codeList':codeList})
            else:
                #填写到数据库
                print('CPU数据填提交更改')
                res = updateCpuTomaterial(request,userId)

        else:
            #填写到数据库
            print('其他元器件的数据提交更改')
            res =updateOther(request,userId)

        if res == -1:
            massage = mark_safe(massage % 'TDP和SPEC应为数字')
            return render(request,'updateMaterial.html',{'typeData':typeData,'type':type,'brand':brand,'name':name,'platform':platform,'code':code,'massage':massage,'platformList':platformList,'codeList':codeList})
        elif res == 'tdp' :
            massage = mark_safe(massage % 'TDP应为数字')
            return render(request,'updateMaterial.html',{'typeData':typeData,'type':type,'brand':brand,'name':name,'platform':platform,'code':code,'SPEC':spec,'massage':massage,'platformList':platformList,'codeList':codeList})
        elif res == 'spec':
            massage = mark_safe(massage % 'SPEC应为数字')
            return render(request,'updateMaterial.html',{'typeData':typeData,'type':type,'brand':brand,'name':name,'platform':platform,'code':code,'TDP':tdp,'massage':massage,'platformList':platformList,'codeList':codeList})
        elif res is None:
            print('DO NOTHING')
        else:
            if (next == '仅提交'):
                return redirect('/resource/?id='+str(mid))
            elif(next == '提交并完善详细信息'):
                print('跳转到对应的详细数据上传页')
                return redirect('/createtags?id='+str(mid))
            elif(next == '提交并上传模型'):
                print('跳转模型上传页')
                return redirect('/resupload/?id='+str(mid))


#删除
@login_required
def deleteMaterial(request):
    id = request.GET.get('id')
    print(id)
    movoToRecyclebin(id)
    return redirect('/materials')



@login_required
def uploadCover(request):
    mid = request.GET.get('id')

    cover = request.FILES.getlist('cover')
    strpath = 'cover_'+str(mid)
    #获取后缀名
    back = os.path.splitext(str(cover[0]))[1]
    ftpPath = Config.ftpPath+'covers/'
    filePath = strpath+back
    mkdir_p(ftpPath)
    FileUploadRename(cover,ftpPath,filePath)
    #将图片名称写入数据库
    dao = Utils()
    updatesql = 'update d_materials set cover = %s where id = %s'
    args = [filePath,mid]
    dao.modifyP(updatesql,args)
    dao.commit()
    dao.close()

    return redirect('/createtags?id='+str(mid))


@login_required
def uploadFiles(request):
    mid = request.GET.get('id')
    ftpPath=Config.ftpPath
    mkdir_p(ftpPath+'materFile/mater'+mid)
    fileAddr = ftpPath+'materFile/mater'+mid
    files = request.FILES.getlist('files')
    FileUpload(files,fileAddr)
    print(files)
    return  redirect('/createtags?id='+str(mid))
