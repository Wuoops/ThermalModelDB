from dao.uitlsPlus import *
from django.shortcuts import render
def disk(request):

    id = request.GET.get('id')
    # print(id)
    sql = 'select m.id,m.name,(select s.source_name from m_source s where s.source = m.source) source,m.modify_source,u.owner_name from d_model m INNER JOIN d_users u where u.user_id = m.creater and  m.id = %s'
    obj = Utils()
    res = obj.searchOneP(sql,id)
    sql_info = 'SELECT bord, type, capacity, speed, ptd, `socket`, othertec FROM d_disk_moldel c WHERE c.ID = (SELECT MODEL FROM d_model M WHERE M.ID = %s)'
    res_info = obj.searchOneP(sql_info,id)


    print(res_info)

    name = res[1]
    source = res[2]
    modefy_source = res[3]
    creater = res[4]

    sql_file='select path from d_resource where mod_id = %s'
    file_name=obj.searchOneP(sql_file,id)
    obj.close()
    print(file_name)
    if file_name is not None:
        print('bushi none')
        return render(request,'disk.html',{'name':name,'source':source,'modefy_source':modefy_source,'creater':creater,'list':res_info,'file_name':file_name[0]})
    else:
        print('shi none')
        return render(request,'disk.html',{'name':name,'source':source,'modefy_source':modefy_source,'creater':creater,'list':res_info })

    # return render(request,'cpu.html',{'name':name,'source':source,'modefy_source':modefy_source,'creater':creater,'list':res_info})
