from dao.uitlsPlus import *

def resourceModel(request):

    mid = request.GET.get('id')
    sql = """
        SELECT
        `id`,
        `name`,
        `materialsid`,
        `pid`,
        `path`,
        `cover`,
        (
            SELECT
                u.owner_name
            FROM
                d_users u
            WHERE
                u.user_id = r.creater
        ) username,
        `remark`,
        DATE_FORMAT(
            r.create_date,
            "%%Y-%%m-%%d %%H:%%i:%%s"
        ) creattime,
        `modify_time`,
        `type`,
        (select ce.source_name from m_source ce where ce.source = r.source) sourcename,
        (select ce.color from m_source ce where ce.source = r.source) color,
        r.source,r.creater
    FROM
        d_model_resource r
        where materialsid = %s
        ORDER BY r.source ,r.id desc
    """
    obj = Utils()
    list = obj.searchListP(sql,mid)
    obj.close()
    return list

