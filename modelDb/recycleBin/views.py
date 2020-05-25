from django.shortcuts import render,redirect
from django.core.paginator import Paginator,Page,PageNotAnInteger,EmptyPage
from .UTIL.utils import *
from materials.Utils.utils import *
from config import Config
from Login.utils import Users
from django.contrib.auth.decorators import login_required


@login_required
def recycleBin(request):

    typeData = getRecyList('type')
    brandData = getRecyList('brand')
    usrData = getRecyList('usr')
    search = request.GET.get('search')
    # queryDict = request.GET.dict()
    queryDict = request.GET.dict()
    list = recyBinsearch(queryDict)
    # if search != '':
    #     list = reSearch(search)
    #     print(list)

    lines = Config.lines
    current_page = request.GET.get('page')
    if current_page is None:
        current_page = 1
    paginator = Paginator(list,lines)
    try:
        posts = paginator.page(current_page)
        print(posts)
    except PageNotAnInteger as e :
        posts = paginator.page(1)
    except EmptyPage as e :
        posts = paginator.page(1)
    pagemax=paginator.num_pages
    # print(posts.object_list)
    issuper = request.user.is_superuser
    # return render(request,'recycleBin.html', {'pagemax':pagemax,'page':current_page,'typeData':typeData,'brandData':brandData,'usrData':usrData})

    if issuper:
        superbtn = '<button type="button" class="btn-sm btn-info" onclick="window.document.location = %s" >修改</button>'
        return render(request,'recycleBin.html', {'posts':posts,'pagemax':pagemax,'page':current_page,'typeData':typeData,'brandData':brandData,'usrData':usrData})
    else:
        return render(request,'recycleBin.html',{'posts':posts,'pagemax':pagemax,'page':current_page,'typeData':typeData,'brandData':brandData,'usrData':usrData})

@login_required
def rollback(request):
    id = request.GET.get('id')
    print(id)
    rollbackUtil(id)
    return redirect('/recyclebin')

