from dao.daoUtils import *
from dao.uitlsPlus import *
import re


#查询所有版本分支信息
def getBranch():
    sql = 'select * from m_source '
    u = Utils()
    data = u.searchList(sql)
    return data
