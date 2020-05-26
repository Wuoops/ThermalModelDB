from dao.daoUtils import *
from dao.uitlsPlus import *
import re
from django.shortcuts import render,redirect
from config import Config
import os
# 判断一个字符串是否是小数
def IsFloat(s):
    pattern = '^-?\d+\.?\d*$'
    match = re.match(pattern, s)
    return match != None


#初始查询列表返一个列表
def model_search(queryDict):
    # 查询数据
    if queryDict == {} :
        sql =  " SELECT * FROM v_materials"
        res = searchData(sql)
        return res
    else :
        for k ,v in  queryDict.items():
            if k != 'page':
                sql = 'select * from v_materials where '+str(k)+' = ' +"'%s'" %v
            else:
                sql =  " SELECT * FROM v_materials"
            res = searchData(sql)
            return res
#日期拼接
def dateSplice(y,m,d):
    # print(d)
    if  y =='' :
        yy = '2019'
    else:
        yy=y
    if  m =='' :
        mm='01'
    else:
        mm=m
    if  d =='':
        dd='01'
    else:
        dd=d
    date=yy+'-'+mm+'-'+dd
    return (date)


#检索查询列表返一个列表
def search(request,fdate,tdate):

    sql = """SELECT id ,name,        type, series,
        (select u.owner_name from d_users u where u.user_id = m.creater) usr,
        DATE_FORMAT(m.create_date,'%%Y-%%m-%%d %%H:%%i:%%s'),tdp
        FROM d_materials as m INNER JOIN
        d_users AS S 
				where m.creater = S.user_id
				and m.iswork = '1'
				and 	m.create_date >= DATE('%s') and m.create_date <= DATE('%s')""" %(fdate,tdate)
    #拼接对照字典
    tableDict={'creater':'S.owner_name','type':'m.type','name':'m.name','tdp':'m.tdp'}



    type = request.GET.get('type')
    name = request.GET.get('name')
    tdp  = request.GET.get('tdp')
    creater = request.GET.get('creater')

    dic=[]
    res=[]
    # print(request.GET)
    for i in request.GET:
        # print(request.GET.get(i))
        if request.GET.get(i) !='':
            dic.append(i)
            res.append(request.GET.get(i))

    # print(dic)
    # print(res)

    for d in range(0,len(dic)):
        if dic[d] in tableDict:
            # print(d)
            sql +=  "and "+tableDict.get(dic[d])+' like\'%'+res[d]+'%\''
            # print(sql)
    print(sql)

    data = searchData(sql)
    # print(data)
    return data

#分析列表，分页返回列表
def pagination(list):
    lst=[]
    for i in range(0,len(list),10):
        lst.append(list[i:i+10])

    return lst

def getMaterList(name):
    sql ="select distinct "+str(name)+" from v_materials"
    data = searchData(sql)
    list = []
    for i in data:
        list.append(i[0])
    return list


#将其他元器件数据插入物料表
def insertOther(request,userId):
    type = request.POST.get('type')
    brand= request.POST.get('brand')
    name = request.POST.get('name')
    tdp = request.POST.get('TDP')
    spec = request.POST.get('SPEC')
    temptype = request.POST.get('temptype')


    if (tdp == '') & (spec == ''):
        sql = "insert into d_materials (type,brand,name,creater,temptype) values (%s,%s,%s,%s,%s);"
        par = [type,brand,name,userId,temptype]
    elif (tdp != '') & (spec == ''):
        if IsFloat(tdp):
            sql = "insert into d_materials (type,brand,name,creater,tdp,temptype) values (%s,%s,%s,%s,%s,%s);"
            par = [type,brand,name,userId,tdp,temptype]
        else:
            return 'tdp'
    elif (tdp =='') & (spec !=''):
        if IsFloat(spec):
            sql = "insert into d_materials (type,brand,name,creater,spec,temptype) values (%s,%s,%s,%s,%s,%s);"
            par = [type,brand,name,userId,spec,temptype]
        else:
            return 'spec'
    elif (tdp != '') & (spec !=''):
        if IsFloat(spec) & IsFloat(tdp):
            sql = "insert into d_materials (type,brand,name,creater,spec,temptype,tdp) values (%s,%s,%s,%s,%s,%s,%s);"
            par = [type,brand,name,userId,spec,temptype,tdp]
        else:
            return -1

    up = Utils()
    rid = up.create(sql,par)
    up.commit()
    up.close()
    return rid

#将其他元器件数据插入物料表
def updateOther(request,userId):
    id = request.GET.get('id')
    type = request.POST.get('type')
    brand= request.POST.get('brand')
    name = request.POST.get('name')
    tdp = request.POST.get('TDP')
    spec = request.POST.get('SPEC')
    temptype = request.POST.get('temptype')


    if (tdp == '') & (spec == ''):
        sql = "update d_materials set type = %s ,brand = %s,name = %s,creater = %s ,temptype = %s where id = %s"
        par = [type,brand,name,userId,temptype,id]
    elif (tdp != '') & (spec == ''):
        if IsFloat(tdp):
            sql = "update d_materials set type = %s ,brand = %s,name = %s,creater = %s ,tdp = %s,temptype= %s  where id = %s"
            par = [type,brand,name,userId,tdp,temptype,id]
        else:
            return 'tdp'
    elif (tdp =='') & (spec !=''):
        if IsFloat(spec):
            sql = "update d_materials set type = %s ,brand = %s,name = %s,creater = %s,spec=%s ,temptype = %s where id = %s"
            par = [type,brand,name,userId,spec,temptype,id]
        else:
            return 'spec'
    elif (tdp != '') & (spec !=''):
        if IsFloat(spec) & IsFloat(tdp):
            sql = "update d_materials set type = %s ,brand = %s,name = %s,creater = %s,tdp=%s,spec=%s ,temptype=%s  where id = %s"
            par = [type,brand,name,userId,tdp,spec,temptype,id]
        else:
            return -1

    up = Utils()
    rid = up.create(sql,par)
    up.commit()
    up.close()
    return rid

#将CPU数据插入物料表
def insertCpuTomaterial(request,userId):
    type = str(request.POST.get('type'))
    brand= str(request.POST.get('brand'))
    name = str(request.POST.get('name'))
    platform = str(request.POST.get('platform'))
    code = str(request.POST.get('code'))
    tdp = request.POST.get('TDP')
    spec = request.POST.get('SPEC')
    temptype = request.POST.get('temptype')

    if (tdp == '') & (spec == ''):
        sql = "insert into d_materials (type,brand,name,platform,code,creater,temptype) values (%s,%s,%s,%s,%s,%s,%s);"
        par = [type,brand,name,platform,code,userId,temptype]
    elif (tdp != '') & (spec == ''):
        if IsFloat(tdp):
            sql = "insert into d_materials (type,brand,name,platform,code,creater,tdp,temptype) values (%s,%s,%s,%s,%s,%s,%s,%s);"
            par = [type,brand,name,platform,code,userId,tdp,temptype]
        else:
            return 'tdp'
    elif (tdp =='') & (spec !=''):
        if IsFloat(spec):
            sql = "insert into d_materials (type,brand,name,platform,code,creater,spec,temptype) values (%s,%s,%s,%s,%s,%s,%s,%s);"
            par = [type,brand,name,platform,code,userId,spec,temptype]
        else:
            return 'spec'
    elif (tdp != '') & (spec !=''):
        if IsFloat(spec) & IsFloat(tdp):
            sql = "insert into d_materials (type,brand,name,platform,code,creater,tdp,spec,temptype) values (%s,%s,%s,%s,%s,%s,%s,%s,%s);"
            par = [type,brand,name,platform,code,userId,tdp,spec,temptype]
        else:
            return -1

    up = Utils()
    rid = up.create(sql,par)
    up.commit()
    up.close()

    return rid


#将CPU数据提交更改
def updateCpuTomaterial(request,userId):
    id = request.GET.get('id')
    type = str(request.POST.get('type'))
    brand= str(request.POST.get('brand'))
    name = str(request.POST.get('name'))
    platform = str(request.POST.get('platform'))
    code = str(request.POST.get('code'))
    tdp = request.POST.get('TDP')
    spec = request.POST.get('SPEC')
    temptype = request.POST.get('temptype')

    if (tdp == '') & (spec == ''):
        sql = "update d_materials set type = %s ,brand = %s,name = %s,platform = %s,code = %s,creater = %s ,temptype = %s where id = %s"
        par = [type,brand,name,platform,code,userId,temptype,id]
    elif (tdp != '') & (spec == ''):
        if IsFloat(tdp):
            sql = "update d_materials set type = %s ,brand = %s,name = %s,platform = %s,code = %s,creater = %s ,tdp = %s,temptype=%s where id = %s"
            par = [type,brand,name,platform,code,userId,tdp,temptype,id]
        else:
            return 'tdp'
    elif (tdp =='') & (spec !=''):
        if IsFloat(spec):
            sql = "update d_materials set type = %s ,brand = %s,name = %s,platform = %s,code = %s,creater = %s  ,spec = %s,temptype=%s where id = %s"
            par = [type,brand,name,platform,code,userId,spec,temptype,id]
        else:
            return 'spec'
    elif (tdp != '') & (spec !=''):
        if IsFloat(spec) & IsFloat(tdp):
            sql = "update d_materials set type = %s ,brand = %s,name = %s,platform = %s,code = %s,creater = %s ,tdp = %s ,spec = %s ,temptype = %s where id = %s"
            par = [type,brand,name,platform,code,userId,tdp,spec,temptype,id]
        else:
            return -1

    up = Utils()
    rid = up.create(sql,par)
    up.commit()
    up.close()

    return rid


#根据物料ID查询物料信息
def getMaterTags(mid):
    sql = 'select * from d_materials_tag where materid = %s'
    mid=[mid,]
    u = Utils()
    data = u.searchListP(sql,mid)
    return data

def getMaterTagList(mid):
    res = getMaterTags(mid)
    kList = []
    vList = []
    for tags in res:
        kList.append(tags[1])
        vList.append(tags[2])
    taglist = listsTodict(kList,vList)
    return taglist
#根据id查询物料信息
def getMaterByid(mid):
    sql = """    SELECT
            NAME,
            (
                SELECT
                    u.owner_name
                FROM
                    d_users u
                WHERE
                    u.user_id = m.creater
            ) usr,
            DATE_FORMAT(
                m.create_date,
                '%%Y-%%m-%%d %%H:%%i:%%s'
            )  create_time    
                 ,platform,code,brand,type,tdp,spec,temptype
                FROM
            d_materials AS m
        INNER JOIN d_users AS S
        where m.creater = S.user_id
        AND m.iswork = '1'
        and id = %s
    """

    data = searchDataP(sql,mid)
    # print(data)
    dList=[]
    for d in data[0]:
        if d is None:
            dList.append('-')
        else:
            dList.append(d)
    return (dList)

#合并两个list为一个Dict
def listsTodict(kList,vList):
    dic = {}
    for num in range(0,len(kList)):
        dic[kList[num]] = vList[num]
    return dic

def getPlatformList():
    up = Utils()
    sql = 'SELECT platform FROM m_cpu_platform'
    pList = up.searchList(sql)
    up.commit()
    up.close()
    platformList=[]
    platformList.append('--')
    for i in pList:
        platformList.append(i[0])
    return platformList
def getCodeList():
    up = Utils()
    sql = 'SELECT code FROM m_cpu_code'
    cList = up.searchList(sql)
    up.commit()
    up.close()
    codeList=[]

    codeList.append('--')
    for i in cList:
        codeList.append(i[0])
    return codeList

#排序置顶
def listpTotop(topValue,theList):
    td=[]
    td.append(topValue)
    for i in theList:
        if i != topValue:
            td.append(i)

    return td


#移动至回收站
def movoToRecyclebin(id):
    sql = "update d_materials set iswork = 0 where id = %s"

    up = Utils()
    rid = up.create(sql,id)
    up.commit()
    up.close()

# 获取封面
def getCover(mid):
    daoPlus = Utils()
    sql = 'select cover from d_materials where id = %s'
    args = [mid,]
    cover = daoPlus.searchListP(sql,args)[0][0]
    daoPlus.close()
    picAddr=Config.picAddr+str(cover)

    return picAddr,cover

def getPicHtml(mid):
    picAddr,cover = getCover(mid)
    if cover == None:
        picHtml = """<div></div>"""
    else:
        picHtml = """<div onclick="window.open('"""+picAddr+"""')"><img src="""+picAddr+""" class="w-100"/></div>"""
    return picHtml
def getMaterFileHtml(mid):
    ftpAddr = Config.ftpdAddr
    ftpPath = Config.ftpPath
     #物料附件地址
    materFileAddr = ftpAddr+'materFile/mater'+mid
    materFilePath = ftpPath+'materFile/mater'+mid
    if (os.path.exists(materFilePath) == False):
        materFileHtml = "<div></div>"
    else:
        materFileHtml="""<a href='"""+materFileAddr+"""' class="btn btn-success">下载附件</a>"""

    return  materFileHtml
