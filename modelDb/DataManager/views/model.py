from django.shortcuts import render
from django.core.paginator import Paginator,Page,PageNotAnInteger,EmptyPage
from DataManager.Models.models import *
# from Login.views import LoginView
import datetime
from dao.uitlsPlus import Utils


def model(request):
    list=[]
    list = model_search()
    # list = pagination(list)
    # print(list)
    paginator = Paginator(list,10)
    type = request.GET.get('type')
    name = request.GET.get('name')
    tdp  = request.GET.get('tdp')
    creater = request.GET.get('creater')


    fy = request.GET.get('fy')
    fm = request.GET.get('fm')
    fd = request.GET.get('fd')
    ty = request.GET.get('ty')
    tm = request.GET.get('tm')
    td = request.GET.get('td')

    page = request.GET.get('page')
    # pagemax = len(list)
    # if (page == None):
    #     page = 0
    # else:
    #     page = int(page)-1


    fy = fy if fy != None else ''
    fm = fm if fm != None else ''
    fd = fd if fd != None else ''
    ty = ty if ty != None else ''
    tm = tm if tm != None else ''
    td = td if td != None else ''

    fdate = dateSplice(fy,fm,fd)
    # print(fdate)
    now = datetime.datetime.now()+ datetime.timedelta(days=1)
    tdate = now.strftime('%Y-%m-%d')


    if (type == None ) & ( name == None )& ( tdp == None )& ( creater == None )& ( fy == None )& ( fm == None )& ( fd == None )& ( ty == None )& ( tm == None )& ( td == None ):
        # print('username:' + LoginView.usernamme)
        # return render(request,'model.html',{'list':list[page] ,'page':page+1 ,'pagemax':pagemax})

        current_page = request.GET.get('page')
        paginator = Paginator(list,10)
        try:
            posts = paginator.page(current_page)
        except PageNotAnInteger as e :
            posts = paginator.page(1)
        except EmptyPage as e :
            posts = paginator.page(1)
        pagemax=paginator.num_pages
        print(posts)
        return render(request,'model.html',{'posts':posts,'pagemax':pagemax})

    else:

        lst = search(request,str(fdate),str(tdate))
        # list = pagination(lst)
        # print('pagemax '+str(len(list)))
        current_page = request.GET.get('page')
        # print( 'currtpage : '+current_page)
        paginator = Paginator(lst,10)
        try:
            posts = paginator.page(current_page)
        except PageNotAnInteger as e :
            posts = paginator.page(1)
        except EmptyPage as e :
            posts = paginator.page(1)
        pagemax=paginator.num_pages

        if  (len(list) == 0):
            print('list = 0')
            # return render(request,'model.html',{'page':page+1,'pagemax':str(len(list)) })
            return render(request,'model.html',{'posts':posts,'pagemax':pagemax})
        else:
            # req={'list':list[page] ,'page':page+1,'pagemax':str(len(list)) }
            req={'posts':posts  ,'pagemax':pagemax}

            for i in request.GET:
                if request.GET.get(i) != '':
                    req[i] = request.GET.get(i)
            print(req)
            return render(request,'model.html',req)



def update(request):
    page=0
    list = model_search()
    return render(request,'update.html',{'list':list[page] })



def cpu(request):

    id = request.GET.get('id')
    # print(id)
    sql = 'select m.id,m.name,(select s.source_name from m_source s where s.source = m.source) source,m.modify_source,u.owner_name,	 DATE_FORMAT( m.create_date,"%%Y-%%m-%%d %%H:%%i:%%s") createdate from d_materials m INNER JOIN d_users u where u.user_id = m.creater and  m.id = %s'
    obj = Utils()
    res = obj.searchOneP(sql,id)
    # sql_info = 'select id,instractionSet,bord,platform,code,series,family,genoration,cpu_name,core,threads,frequency,turbo,process,TDP,suatus,launchDate,socket,cache,mem_max,mem_type,(case when c.mem_ecc = 1 then "是" when c.mem_ecc = 0 then "否" else "未知" end) ecc,gpu_inside,gpu_name from d_cpu_materials c WHERE c.ID = (SELECT details FROM d_materials M WHERE M.ID = %s)'
    sql_info = """
        SELECT
            c.id,
            c.instractionSet,
            c.bord,
            c.platform,
            c.CODE,
            c.series,
            c.family,
            c.genoration,
            c.cpu_name,
            c.core,
            c.threads,
            c.frequency,
            c.turbo,
            c.process,
            c.TDP,
            c.suatus,
            c.launchDate,
            c.SOCKET,
            c.CACHE,
            c.mem_max,
            c.mem_type,
            
            (
                CASE
                WHEN c.mem_ecc = 1 THEN
                    "是"
                WHEN c.mem_ecc = 0 THEN
                    "否"
                ELSE
                    "未知"
                END
            ) ecc,
            gpu_inside,
            gpu_name,
            m.cover
        FROM
            d_cpu_materials c
        INNER JOIN
            d_materials m
        where 
            c.ID = m.details
        and m.id = %s
        """
    res_info = obj.searchOneP(sql_info,id)


    print(id)

    id = res[0]
    name = res[1]
    creater = res[4]
    creatdate = res[5]
    sql_file='select path from d_resource where mod_id = %s'
    file_name=obj.searchOneP(sql_file,id)
    obj.close()
    if file_name is not None:
        return render(request,'cpu.html',{'name':name,'id':id,'creatdate':creatdate,'creater':creater,'list':res_info,'file_name':file_name[0]})
    else:
        return render(request,'cpu.html',{'name':name,'id':id,'creatdate':creatdate,'creater':creater,'list':res_info })

    # return render(request,'cpu.html',{'name':name,'source':source,'modefy_source':modefy_source,'creater':creater,'list':res_info})

def dimm(request):
    id = request.GET.get('id')
    # print(id)
    sql = 'select m.id,m.name,(select s.source_name from m_source s where s.source = m.source) source,m.modify_source,u.owner_name from d_materials m INNER JOIN d_users u where u.user_id = m.creater and  m.id = %s'
    obj = Utils()
    res = obj.searchOneP(sql,id)
    sql_info = 'select d.bord,d.type,d.frequency,d.size,d.ptd,d.other_tec from d_dimm_materials d WHERE d.ID = (SELECT details FROM d_materials M WHERE M.ID = %s)'
    res_info = obj.searchOneP(sql_info,id)

    sql_file='select path from d_resource where mod_id = %s'
    file_name=obj.searchOneP(sql_file,id)
    # print(file_name)
    obj.close()


    name = res[1]
    source = res[2]
    modefy_source = res[3]
    creater = res[4]

    bord = res_info[0]
    type = res_info[1]
    frequency = res_info[2]
    size = res_info[3]
    ptd = res_info[4]
    other = res_info[5]

    # return render(request,'dimm.html',{'name':name,'source':source,'modefy_source':modefy_source,'creater':creater,'bord':bord,'type':type,'frequency':frequency,'size':size,'ptd':ptd,'other_tec':other })


    if file_name is not None:
        return render(request,'dimm.html',{'name':name,'source':source,'modefy_source':modefy_source,'creater':creater,'bord':bord,'type':type,'frequency':frequency,'size':size,'ptd':ptd,'other_tec':other ,'file_name':file_name[0]})
    else:
        return render(request,'dimm.html',{'name':name,'source':source,'modefy_source':modefy_source,'creater':creater,'bord':bord,'type':type,'frequency':frequency,'size':size,'ptd':ptd,'other_tec':other })

from django.http import FileResponse
from django.shortcuts import HttpResponse
def file_down(request):

    file_name = request.GET.get('file_name')
    file=open('files/files/'+file_name,'rb')
    response =FileResponse(file)
    response['Content-Type']='application/octet-stream'
    # response['Content-Type']='application/x-jpg'
    response['Content-Disposition']='attachment;filename=%s'%(file_name)

    return response
def getImg(request):
    file_name = request.GET.get('file_name')
    file=open('files/files/'+file_name,'rb')
    response =FileResponse(file)
    # response['Content-Type']='application/octet-stream'
    response['Content-Type']='application/x-jpg'
    response['Content-Disposition']='attachment;filename=%s'%(file_name)

    return response
