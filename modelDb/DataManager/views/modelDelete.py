from dao.uitlsPlus import *
from django.shortcuts import redirect
def modeldelete(request):
    mid = request.GET.get('mid')
    print('delete data where id = '+str(mid))
    del_sql='update d_materials set iswork = 0 where id = %s'
    obj = Utils()
    obj.modifyP(del_sql,mid)
    obj.commit()
    obj.close()

    return redirect('/model/')
