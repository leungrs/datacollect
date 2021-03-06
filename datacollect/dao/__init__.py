# coding: utf-8


from datacollect.dao.table import RestaurantTable


def select(db, table_name, select_fields=None,
           order_field="id", like_condition=None, sort_order="desc",
           fetchone=False, return_count=False, param=None):
    param = param or {}
    limit = param.pop("limit", None)
    offset = param.pop("offset", 0)
    order = param.pop("order", "asc")

    w_fields = []
    w_values = []
    for k, v in param.items():
        if isinstance(v, str):
            v = v.strip()
            if not v:
                continue
        w_fields.append(k)
        w_values.append(v)

    where = " and ".join("{}=?".format(f) for f in w_fields)
    if like_condition:
        if where:
            where += " and "
        where += " and ".join("{} like '%{}%'".format(k, v) for k, v in like_condition.items())

    fields = "*"
    if select_fields:
        fields = ",".join(select_fields)

    sql = "select {} from {}".format(fields, table_name)
    if where:
        sql += " where {}".format(where)

    if order_field:
        sql += " order by {0} {1}".format(order_field, sort_order)

    count = 0
    if limit:
        return_count = True
        sql_count = "select count(*) from ({0})".format(sql)
        r = db.execute(sql_count, w_values).fetchone()
        count = r[0]
        sql += " limit {0} offset {1}".format(limit, offset)

    if fetchone:
        return_count = False
        data = db.execute(sql, w_values).fetchone()
        result = sqlite3_row_to_dict(data)
    else:
        data = db.execute(sql, w_values).fetchall()
        result = [sqlite3_row_to_dict(row) for row in data]

    if return_count:
        return count, result
    else:
        return result


def select_survey_types(db):
    sql = "select * from survey_types"
    survey_types = db.execute(sql).fetchall()
    return survey_types


def export_array(db, excel_type):
    return get_excel_array(db, excel_type)


def get_excel_array(db, excel_type):
    array = []
    if excel_type == "restaurant":
        table_fields = RestaurantTable.TABLE_FIELDS
        table_name = RestaurantTable.TABLE_NAME
    else:
        return []

    result = select(db=db, table_name=table_name)
    exclude_fields = ("updated_by", "updated_date")
    array.append([f for _, f in table_fields if _ not in exclude_fields])
    if result:
        for row in result:
            array.append(
                [row.get(field_name, "")
                for field_name, _ in table_fields
                if field_name not in exclude_fields]
             )
    return array


def sqlite3_row_to_dict(row):
    if row:
        return {
            key: row[key]
            for key in row.keys()
        }


def sqlite3_rows_to_dict(rows):
    result = []
    for row in rows:
        result.append(sqlite3_row_to_dict(row))


FUTIAN = {
    "province": "广东省",
    "city": "深圳市",
    "district": "福田区"
}


FUTIAN_TOWN = {
    "南园街道": "南园街道办事处",
    "福田街道": "福田街道办事处",
    "园岭街道": "园岭街道办事处",
    "沙头街道": "沙头街道办事处",
    "香蜜湖街道": "香蜜湖街道办事处",
    "梅林街道": "梅林街道办事处",
    "福保街道": "福保街道办事处",
    "莲花街道": "莲花街道办事处",
    "华富街道": "华富街道办事处",
    "华强北街道": "华强北街道办事处",
}


def get_town_from_address(address, startswith=False):
    for key, value in FUTIAN_TOWN.items():
        if startswith:
            if key.startswith(address):
                return key
        elif key in address:
            return key

    return ""
