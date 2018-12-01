# coding: utf-8


from datacollect.common import Result, to_type, RestaurantTable
from datacollect.dao import restaurant


def select(db, table_name, select_fields=None,
           order_field="id", sort_order="desc",
           fetchone=False, return_count=False, param=None):
    param = param or {}
    limit = param.pop("limit", None)
    offset = param.pop("offset", 0)
    order = param.pop("order", "asc")

    w_fields = []
    w_values = []
    for k, v in param.items():
        w_fields.append(k)
        w_values.append(v)

    where = " and ".join("{}=?".format(f) for f in w_fields)

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
        r = db.execute(sql_count).fetchone()
        count = r[0]
        sql += " limit {0} offset {1}".format(limit, offset)

    if fetchone:
        return_count = False
        data = db.execute(sql).fetchone()
        result = sqlite3_row_to_dict(data)
    else:
        data = db.execute(sql).fetchall()
        result = [sqlite3_row_to_dict(row) for row in data]

    if return_count:
        return count, result
    else:
        return result


def select_survey_types(db):
    sql = "select * from survey_types"
    survey_types = db.execute(sql).fetchall()
    return survey_types


def import_restaurant_from_array(array, db, updated_date, updated_by):
    """导入餐饮表，返回导入的记录数"""
    columns = array[0]
    rows = array[1:]
    valid_names = {
        "餐饮企业名称": "ent_name",
        "经营地址": "address",
        "经度": "longitude:float",
        "纬度": "latitude:float",
        "法人代表": "legal_person",
        "投产时间": "open_date",
        "企业联系人": "ent_contact",
        "联系电话": "ent_phone:str",
        "餐饮类型.1": "restaurant_type",
        "可容纳用餐人数": "customer_capacity:float",
        "员工人数": "employee_num:int",
        "经营面积": "ent_area:float",
        "用水量": "water_used:float",
        "餐厨垃圾处置去向": "kitchen_waster_gone"
    }
    success_count = 0
    for row in rows:
        burner_count = 0
        item = {}
        for i, col in enumerate(columns):
            val = row[i]
            if col in valid_names:
                valid_name = valid_names[col]
                if ":" in valid_name:
                    valid_name, type_str = valid_name.split(":")
                    val = to_type(val, type_str)
                item[valid_name] = val
            elif "炉" in col:
                burner_count += to_type(val, int, 0)
        # 处理炉头数
        item["burner_num"] = burner_count
        item["updated_date"] = updated_date
        item["updated_by"] = updated_by
        err_msg = restaurant.insert_update(db, item)
        if not err_msg:
            success_count += 1
    return success_count


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

def import_from_array(data, db, excel_type, updated_date, updated_by):
    result = Result()
    success_count = 0
    if excel_type == "restaurant":
        success_count = import_restaurant_from_array(data, db, updated_date, updated_by)
    result.data = success_count
    result.message = "导入成功{}条记录".format(success_count)
    return result


def sqlite3_row_to_dict(row):
    if row:
        return {
            key: row[key]
            for key in row.keys()
        }
