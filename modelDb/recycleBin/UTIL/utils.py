from dao.daoUtils import *
from dao.uitlsPlus import *
import re
#初始查询列表返一个列表
def model_search():
    # 查询数据
    sql = """
        select id ,
            (case when brand is null then '-' else brand end) brand,
            (case when platform is null then '-' else platform end) plat,
            (case when code is null then '-' else code end) co ,type, 
            (case when name is null then '-' else name end) name,
             ( SELECT u.owner_name FROM d_users u WHERE u.user_id = m.creater ) usr,
             (case when tdp is null then '-' else tdp end) tdp,
              DATE_FORMAT(m.create_date,'%Y-%m-%d') createdate,
           (case when spec is null then '-' else spec end) spec

                FROM d_materials AS m
                INNER JOIN d_users AS S
                where m.creater = S.user_id
                    AND m.iswork = '0'
                     order by id desc;
        """

    # data = ('OFFICIAL','CPU')
    # res = searchData(sql,data)

    res = searchData(sql)
    return res



def rollbackUtil(id):
    sql = "update d_materials set iswork = 1 where id = %s"

    up = Utils()
    rid = up.create(sql,id)
    up.commit()
    up.close()
