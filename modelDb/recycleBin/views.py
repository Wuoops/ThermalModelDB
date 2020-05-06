from django.shortcuts import render,redirect
from django.core.paginator import Paginator,Page,PageNotAnInteger,EmptyPage
from .UTIL.utils import *


def recycleBin(request):

    list = model_search()
    current_page = request.GET.get('page')
    paginator = Paginator(list,10)
    try:
        posts = paginator.page(current_page)
    except PageNotAnInteger as e :
        posts = paginator.page(1)
    except EmptyPage as e :
        posts = paginator.page(1)
    pagemax=paginator.num_pages
    # print(posts.object_list)
    issuper = request.user.is_superuser
    if issuper:
        superbtn = '<button type="button" class="btn-sm btn-info" onclick="window.document.location = %s" >修改</button>'
        return render(request,'recycleBin.html',{'posts':posts,'pagemax':pagemax,})
    else:
        return render(request,'recycleBin.html',{'posts':posts,'pagemax':pagemax,})


def rollback(request):
    id = request.GET.get('id')
    print(id)
    rollbackUtil(id)
    return redirect('/recyclebin')

