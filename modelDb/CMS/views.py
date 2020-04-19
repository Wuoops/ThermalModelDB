from django.shortcuts import render
from CMS.models import *
def homePage(request):

    # zNodes="""
    # var zNodes =[
    # { id:1, pId:0, name:"CPU", open:true},
    # { id:11, pId:1, name:"品牌/系列", open:true},
    #     { id:111, pId:11, name:"INTEL", open:true},
    #     { id:1111, pId:111, name:"Broadwell", open:true},
    #     { id:11111, pId:1111, name:"Xeon", open:true},
    #     { id:111111, pId:11111, name:"E5", open:true},
    #     { id:111112, pId:11111, name:"E7", open:true},
    #     { id:1111122, pId:111112, name:"V3", open:true},
    #     { id:11111121, pId:1111122, name:"E7-3850", open:true},
    #     { id:1111121, pId:111112, name:"V4", open:true},
    #     { id:11111121, pId:1111121, name:"E7-4850", open:true},
    #
    #     { id:12, pId:11, name:"AMD"},
    #     { id:121, pId:12, name:"叶子节点 1-2-1"},
    #     { id:122, pId:12, name:"叶子节点 1-2-2"},
    #     { id:123, pId:12, name:"叶子节点 1-2-3"},
    #     { id:124, pId:12, name:"叶子节点 1-2-4"},
    # { id:13, pId:1, name:"规格", open:true},
    #     { id:131, pId:13, name:"核心数"},
    #     { id:132, pId:13, name:"主频"},
    #     { id:133, pId:13, name:"睿频"},
    #     { id:134, pId:13, name:"制程"},
    #     { id:135, pId:13, name:"TDP"},
    #     { id:136, pId:13, name:"插槽类型"},
    #     { id:137, pId:13, name:"最大缓存"},
    #     { id:138, pId:13, name:"最大内存"},
    #     { id:139, pId:13, name:"内存类型"},
    #     { id:140, pId:13, name:"是否制程ECC内存"},
    #     { id:141, pId:13, name:"是否包含GPU"},
    #
    #     { id:2, pId:0, name:"DIMM"},
    #     { id:21, pId:2, name:"子菜单 2-1"},
    #     { id:211, pId:21, name:"叶子节点 2-1-1"},
    #     { id:212, pId:21, name:"叶子节点 2-1-2"},
    #     { id:213, pId:21, name:"叶子节点 2-1-3"},
    #     { id:214, pId:21, name:"叶子节点 2-1-4"},
    #     { id:22, pId:2, name:"子菜单 2-2"},
    #     { id:221, pId:22, name:"叶子节点 2-2-1"},
    #     { id:222, pId:22, name:"叶子节点 2-2-2"},
    #     { id:223, pId:22, name:"叶子节点 2-2-3"},
    #     { id:224, pId:22, name:"叶子节点 2-2-4"},
    #     { id:3, pId:0, name:"DISK"},
    #     { id:31, pId:3, name:"子菜单 3-1"},
    #     { id:311, pId:31, name:"叶子节点 3-1-1"},
    #     { id:312, pId:31, name:"叶子节点 3-1-2"},
    #     { id:313, pId:31, name:"叶子节点 3-1-3"},
    #     { id:314, pId:31, name:"叶子节点 3-1-4"},
    #     { id:32, pId:3, name:"子菜单 3-2"},
    #     { id:321, pId:32, name:"叶子节点 3-2-1"},
    #     { id:322, pId:32, name:"叶子节点 3-2-2"},
    #     { id:323, pId:32, name:"叶子节点 3-2-3"},
    #     { id:324, pId:32, name:"叶子节点 3-2-4"}
    # ];
    # """


    zNodes=[]
    id=1
    for i in ['CPU','DIMM','DISK','OTHERS']:

        # TitleList="{id:1, pId:0, name:"+i+", open:true}"
        TitleList={}
        TitleList.update(id=id)
        TitleList.update(pId=0)
        TitleList.update(name=i)
        # TitleList.update(open=True)
        id=id+1
        zNodes.append(TitleList)

    TitleList={}
    TitleList.update(id=11)
    TitleList.update(pId=1)
    TitleList.update(name='品牌/系列')
    # TitleList.update(open='true')
    zNodes.append(TitleList)

    TitleList={}
    TitleList.update(id=12)
    TitleList.update(pId=2)
    TitleList.update(name='规格')
    # TitleList.update(open='true')
    zNodes.append(TitleList)

    TitleList={}
    TitleList.update(id=111)
    TitleList.update(pId=11)
    TitleList.update(name='Intel')
    # TitleList.update(open='true')
    zNodes.append(TitleList)

    # return render(request,'homePage.html',{'zNodesList':zNodes})
    zTreeList()

    return render(request,'homePage.html')

