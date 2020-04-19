from dao.daoUtils import searchData, searchDataP

#初始查询列表返一个列表
def model_search():
    # 查询数据
    sql = """SELECT
            id,
            NAME,
            type,
            series,
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
                '%Y-%m-%d %H:%i:%s'
            ),
            tdp
        FROM
            d_materials AS m
        INNER JOIN d_users AS S
        where m.creater = S.user_id
        AND m.iswork = '1'
        AND m.create_date >= DATE('2019-01-01')
        AND m.create_date <= DATE('2019-11-01')
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
