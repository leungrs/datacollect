# coding: utf-8


from datacollect.common import to_type, to_d_m_s, Result
from datacollect.dao import sqlite3_row_to_dict, RestaurantTable, FUTIAN, get_town_from_address


def select_by_id(db, id):
    sql = "select * from restaurant_survey where id=?"
    restaurant = db.execute(sql, [id]).fetchone()
    item = sqlite3_row_to_dict(restaurant)
    return item


def delete_by_id(db, id):
    item = select_by_id(db, id)
    if item:
        sql = "delete from restaurant_survey where id=?"
        db.execute(sql, [id])
        db.commit()
        return True
    return False


def insert_update(db, param, id=None):
    try:
        fields = []
        values = []
        longitude = 0
        latitude = 0
        for k, v in param.items():
            if k == "lon_d":
                longitude += to_type(v, float, 0)
            elif k == "lon_m":
                longitude += to_type(v, float, 0) / 60
            elif k == "lon_s":
                longitude += to_type(v, float, 0) / 3600
            elif k == "lat_d":
                latitude += to_type(v, float, 0)
            elif k == "lat_m":
                latitude += to_type(v, float, 0) / 60
            elif k == "lat_s":
                latitude += to_type(v, float, 0) / 3600
            elif k == "longitude":
                longitude = to_type(v, float, 0)
            elif k == "latitude":
                latitude = to_type(v, float, 0)

            fields.append(k)
            values.append(v)

        if "longitude" not in fields:
            # 非导入，使用的是度分秒计算出的数据
            fields.extend(["longitude", "latitude"])
            values.extend([longitude, latitude])
        else:
            fields.extend(["lon_d", "lon_m", "lon_s"])
            values.extend(to_d_m_s(longitude))
            fields.extend(["lat_d", "lat_m", "lat_s"])
            values.extend(to_d_m_s(latitude))

        if id is not None:
            sql = "update restaurant_survey set "
            sql += ",".join("{0}=?".format(f) for f in fields)
            sql += " where id=?"
            values.append(id)
        else:
            sql = "insert into restaurant_survey({0})".format(",".join(fields))
            sql += " values ({0})".format(",".join("?" * len(fields)))
        db.execute(sql, values)
        db.commit()
    except Exception as e:
        return str(e)


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
        "餐饮类型": "restaurant_type",
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
        item.update(FUTIAN)
        item["town"] = get_town_from_address(item.get("address") or "")
        err_msg = insert_update(db, item)
        if not err_msg:
            success_count += 1
    return success_count


def stat_exp(db, param):
    fields = []
    fields_en = []
    headers = []

    field_name_dict = dict(RestaurantTable.TABLE_FIELDS)

    fields.append("town")
    fields_en.append("town")
    headers.append(field_name_dict["town"])

    if param.get("customer_capacity") == "on":
        fields.append("sum({0}) as {0}".format("customer_capacity"))
        fields_en.append("customer_capacity")
        headers.append(field_name_dict["customer_capacity"])

    if param.get("burner_num") == "on":
        fields.append("sum({0}) as {0}".format("burner_num"))
        fields_en.append("burner_num")
        headers.append(field_name_dict["burner_num"])

    if param.get("employee_num") == "on":
        fields.append("sum({0}) as {0}".format("employee_num"))
        fields_en.append("employee_num")
        headers.append(field_name_dict["employee_num"])

    if param.get("annual_turnover") == "on":
        fields.append("sum({0}) as {0}".format("annual_turnover"))
        fields_en.append("annual_turnover")
        headers.append(field_name_dict["annual_turnover"])

    if param.get("ent_area") == "on":
        fields.append("sum({0}) as {0}".format("ent_area"))
        fields_en.append("ent_area")
        headers.append(field_name_dict["ent_area"])

    if param.get("cooking_oil") == "on":
        fields.append("sum({0}) as {0}".format("cooking_oil"))
        fields_en.append("cooking_oil")
        headers.append(field_name_dict["cooking_oil"])

    if param.get("water_used") == "on":
        fields.append("sum({0}) as {0}".format("water_used"))
        fields_en.append("water_used")
        headers.append(field_name_dict["water_used"])

    if param.get("water_waster_emit") == "on":
        fields.append("sum({0}) as {0}".format("water_waster_emit"))
        fields_en.append("water_waster_emit")
        headers.append(field_name_dict["water_waster_emit"])

    if param.get("kitchen_waster_volume") == "on":
        fields.append("sum({0}) as {0}".format("kitchen_waster_volume"))
        fields_en.append("kitchen_waster_volume")
        headers.append(field_name_dict["kitchen_waster_volume"])

    town = param.get("town")
    sql = "select town, {} from {}".format(
        ",".join(fields),
        RestaurantTable.TABLE_NAME
    )
    if town:
        sql += " where town=? group by town"
        result = db.execute(sql, [town]).fetchall()
    else:
        sql += " group by town"
        result = db.execute(sql).fetchall()

    rows = [sqlite3_row_to_dict(item) for item in result]
    array_result = [headers]
    for row in rows:
        array_result.append([row[f] for f in fields_en])
    return array_result


def delete_all(db):
    try:
        sql = "delete from restaurant_survey"
        db.execute(sql)
        db.commit()
        return Result()
    except Exception as e:
        return Result(message="删除失败:%s" % e)
