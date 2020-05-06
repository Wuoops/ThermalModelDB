from dao.daoUtils import *
from dao.uitlsPlus import *
import re
from django.shortcuts import render,redirect


# 判断一个字符串是否是小数
def IsFloat(s):
    pattern = '^-?\d+\.?\d*$'
    match = re.match(pattern, s)
    return match != None


#初始查询列表返一个列表
def model_search():
    # 查询数据
    sql = """
        select id ,
            (case when brand is null then '-' else brand end) brand,
            (case when platform is null then '-' else platform end) plat,
            (case when code is null then '-' else code end) co ,type, 
            (case when name is null then '-' else name end) name,
             ( SELECT u.owner_name FROM d_users u WHERE u.user_id = m.creater ) usr,
             (case when tdp is null then '-' else tdp end) tdp,
              DATE_FORMAT(m.create_date,'%Y-%m-%d') createdate,
           (case when spec is null then '-' else spec end) spec

                FROM d_materials AS m
                INNER JOIN d_users AS S
                where m.creater = S.user_id
                    AND m.iswork = '1'
                     order by id desc;
        """

    # data = ('OFFICIAL','CPU')
    # res = searchData(sql,data)

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

#获取Type表数据
def getTypeData():
    sql ="select * from m_type"
    data = searchData(sql)
    list = []
    for i in data:
        list.append(i[1])
    return list

#将其他元器件数据插入物料表
def insertOther(request,userId):
    type = request.POST.get('type')
    brand= request.POST.get('brand')
    name = request.POST.get('name')
    tdp = request.POST.get('TDP')
    spec = request.POST.get('SPEC')


    if (tdp == '') & (spec == ''):
        sql = "insert into d_materials (type,brand,name,creater) values (%s,%s,%s,%s);"
        par = [type,brand,name,userId]
    elif (tdp != '') & (spec == ''):
        if IsFloat(tdp):
            sql = "insert into d_materials (type,brand,name,creater,tdp) values (%s,%s,%s,%s,%s);"
            par = [type,brand,name,userId,tdp]
        else:
            return 'tdp'
    elif (tdp =='') & (spec !=''):
        if IsFloat(spec):
            sql = "insert into d_materials (type,brand,name,creater,spec) values (%s,%s,%s,%s,%s);"
            par = [type,brand,name,userId,spec]
        else:
            return 'spec'
    elif (tdp != '') & (spec !=''):
        if IsFloat(spec) & IsFloat(tdp):
            sql = "insert into d_materials (type,brand,name,creater,spec,tdp) values (%s,%s,%s,%s,%s,%s);"
            par = [type,brand,name,userId,spec,tdp]
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


    if (tdp == '') & (spec == ''):
        sql = "update d_materials set type = %s ,brand = %s,name = %s,creater = %s where id = %s"
        par = [type,brand,name,userId,id]
    elif (tdp != '') & (spec == ''):
        if IsFloat(tdp):
            sql = "update d_materials set type = %s ,brand = %s,name = %s,creater = %s ,tdp = %s where id = %s"
            par = [type,brand,name,userId,tdp,id]
        else:
            return 'tdp'
    elif (tdp =='') & (spec !=''):
        if IsFloat(spec):
            sql = "update d_materials set type = %s ,brand = %s,name = %s,creater = %s,spec=%s where id = %s"
            par = [type,brand,name,userId,spec,id]
        else:
            return 'spec'
    elif (tdp != '') & (spec !=''):
        if IsFloat(spec) & IsFloat(tdp):
            sql = "update d_materials set type = %s ,brand = %s,name = %s,creater = %s,tdp=%s,spec=%s where id = %s"
            par = [type,brand,name,userId,spec,tdp,id]
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

    if (tdp == '') & (spec == ''):
        sql = "insert into d_materials (type,brand,name,platform,code,creater) values (%s,%s,%s,%s,%s,%s);"
        par = [type,brand,name,platform,code,userId]
    elif (tdp != '') & (spec == ''):
        if IsFloat(tdp):
            sql = "insert into d_materials (type,brand,name,platform,code,creater,tdp) values (%s,%s,%s,%s,%s,%s,%s);"
            par = [type,brand,name,platform,code,userId,tdp]
        else:
            return 'tdp'
    elif (tdp =='') & (spec !=''):
        if IsFloat(spec):
            sql = "insert into d_materials (type,brand,name,platform,code,creater,spec) values (%s,%s,%s,%s,%s,%s,%s);"
            par = [type,brand,name,platform,code,userId,spec]
        else:
            return 'spec'
    elif (tdp != '') & (spec !=''):
        if IsFloat(spec) & IsFloat(tdp):
            sql = "insert into d_materials (type,brand,name,platform,code,creater,tdp,spec) values (%s,%s,%s,%s,%s,%s,%s,%s);"
            par = [type,brand,name,platform,code,userId,tdp,spec]
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

    if (tdp == '') & (spec == ''):
        sql = "update d_materials set type = %s ,brand = %s,name = %s,platform = %s,code = %s,creater = %s where id = %s"
        par = [type,brand,name,platform,code,userId,id]
    elif (tdp != '') & (spec == ''):
        if IsFloat(tdp):
            sql = "update d_materials set type = %s ,brand = %s,name = %s,platform = %s,code = %s,creater = %s ,tdp = %s where id = %s"
            par = [type,brand,name,platform,code,userId,tdp,id]
        else:
            return 'tdp'
    elif (tdp =='') & (spec !=''):
        if IsFloat(spec):
            sql = "update d_materials set type = %s ,brand = %s,name = %s,platform = %s,code = %s,creater = %s  ,spec = %s where id = %s"
            par = [type,brand,name,platform,code,userId,spec,id]
        else:
            return 'spec'
    elif (tdp != '') & (spec !=''):
        if IsFloat(spec) & IsFloat(tdp):
            sql = "update d_materials set type = %s ,brand = %s,name = %s,platform = %s,code = %s,creater = %s ,tdp = %s ,spec = %s where id = %s"
            par = [type,brand,name,platform,code,userId,tdp,spec,id]
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
                 ,platform,code,brand,type,tdp,spec
                FROM
            d_materials AS m
        INNER JOIN d_users AS S
        where m.creater = S.user_id
        AND m.iswork = '1'
        and id = %s
    """

    data = searchDataP(sql,mid)
    return (data[0])

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
