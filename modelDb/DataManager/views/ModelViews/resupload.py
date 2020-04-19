from django.shortcuts import render
from DataManager.Models.resourceModel import *
from DataManager.Models.models import *
from django.core.paginator import Paginator,Page,PageNotAnInteger,EmptyPage
from dao.utils import *
def resupload(request):

    mid = request.GET.get('id')
    #版本分支刘表
    branchList = getBranchList()
    branch_list={}
    for i in branchList:
        branch_list[i[0]]=i[1]
    # print(branch_list)
    #数据列表
    list = resourceModel(request)
    print(list)
    current_page = request.GET.get('page')
    paginator = Paginator(list,10)
    try:
        posts = paginator.page(current_page)
    except PageNotAnInteger as e :
        posts = paginator.page(1)
    except EmptyPage as e :
        posts = paginator.page(1)
    pagemax=paginator.num_pages


    return render(request,'uploadPage/resourceUpload.html',{'list':posts,'branch_list':branch_list,'mid':mid})
