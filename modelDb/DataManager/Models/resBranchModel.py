from dao.uitlsPlus import *
from dao.utils import *

def resBranchmod(request):
        id = request.GET.get('id')
        branch = request.GET.get('branch')
        if branch is None:
                #获取物料信息
                branchInfoSql ='select id,name,type,(select u.owner_name from d_users u where u.user_id = creater) cr from d_materials where id = %s'
                #
                version = 0
                #最大版本号再加1，避免重复
                # version = int(version[0])+1
                obj = Utils()
                branchInfoList = obj.searchOneP(branchInfoSql,id)
                obj.close()
                branchList = getBranchList()
                userList = getUserList()
                dic=changeListToDIct(userList)
                branchDic=changeListToDIct(branchList)


                # selectedBranck={branch:branchDic[branch]}
                # allBranckDict={}
                # allBranckDict.update(selectedBranck)
                # allBranckDict.update(branchDic)


                list=[id,branchInfoList[1],branchInfoList[2],branchInfoList[3],branch,version]

                return dic,list,branchDic
        else:
                #获取物料信息
                branchInfoSql ='select id,name,type,(select u.owner_name from d_users u where u.user_id = creater) cr from d_materials where id = %s'
                #取最大版本号
                v_sql = 'select  max(pid) version from d_model_resource where source = %s and materialsid =%s '
                v_args=[branch,id]
                obj = Utils()
                version = obj.searchOneP(v_sql,v_args)
                #最大版本号再加1，避免重复
                version = int(version[0])+1
                branchInfoList = obj.searchOneP(branchInfoSql,id)
                obj.close()
                branchList = getBranchList()
                userList = getUserList()
                dic=changeListToDIct(userList)
                branchDic=changeListToDIct(branchList)


                selectedBranck={branch:branchDic[branch]}
                allBranckDict={}
                allBranckDict.update(selectedBranck)
                allBranckDict.update(branchDic)


                list=[id,branchInfoList[1],branchInfoList[2],branchInfoList[3],branch,version]

                return dic,list,allBranckDict

def getMaterInfo(id):
        obj = Utils()
        sql = 'select id,name,type,(select u.owner_name from d_users u where u.user_id = s.creater) creater from d_materials s where s.id = %s '
        mater = obj.searchOneP(sql,id)
        obj.close()
        return mater
