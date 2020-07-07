from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .utils import *


@login_required
def branchSet(request):

    mid = request.GET.get('id')
    branchList = getBranch()

    return render(request,'branchSet.html',{'branchList':branchList,'mid':mid})

@login_required
def createBranch(request):
    mid = request.POST.get('id')
    queryDict = request.POST.dict()
    num = 0
    idList=[]
    nameList = []
    colorList = []
    print(queryDict)

    for k ,v in queryDict.items():
        if k != 'id':
            idM = re.search('inputId',k,re.M|re.I)
            if idM:
                idList.append(v)
            nameM = re.search('inputName',k,re.M|re.I)
            if nameM:
                nameList.append(v)
            colorM = re.search('inputColor',k,re.M|re.I)
            if colorM:
                colorList.append(v)
    sql = 'insert into m_source values(%s,%s,%s)'
    daoPlus = Utils()
    for i in range(0,len(idList)):
        args=[idList[i],nameList[i],colorList[i]]
        print(args)
        daoPlus.modifyP(sql,args)
    daoPlus.commit()
    daoPlus.close()
    return redirect('/resupload?id='+str(mid))

@login_required
def updateBranch(request):
    queryDict = request.POST.dict()

    print(queryDict)
    sql = 'update m_source set source_name=%s,color=%s where source=%s'
    daoPlus = Utils()
    for k ,v in queryDict.items():
        if k !='id':
            nameMarch = re.search('_name',k,re.M|re.I)
            color=''
            if nameMarch:
                id = k[0]
                name = v
            else:
                color = v
            args = [name,color,id]

            daoPlus.modifyP(sql,args)

    daoPlus.commit()
    daoPlus.close()

    mid = request.POST.get('id')

    return redirect('/resupload?id='+str(mid))

@login_required
def deleteModal(request):

    return render(request,'deleteModal.html')
