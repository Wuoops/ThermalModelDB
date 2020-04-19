from django.shortcuts import render
from django.core.paginator import Paginator,Page,PageNotAnInteger,EmptyPage
from DataManager.Models.models import *
from Login.views import LoginView
import datetime
from dao.uitlsPlus import Utils


def uploadPage(request):
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
        return render(request,'uploadPage/uploadPage.html',{'posts':posts,'pagemax':pagemax})

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
            return render(request,'uploadPage/uploadPage.html',{'posts':posts,'pagemax':pagemax})
        else:
            # req={'list':list[page] ,'page':page+1,'pagemax':str(len(list)) }
            req={'posts':posts  ,'pagemax':pagemax}

            for i in request.GET:
                if request.GET.get(i) != '':
                    req[i] = request.GET.get(i)
            print(req)
            return render(request,'uploadPage/uploadPage.html',req)


