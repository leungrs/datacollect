# coding: utf-8


from datacollect.common import to_type, to_d_m_s, Result, get_d_m_s
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
        for k, v in param.items():
            if k == "longitude":
                d, m, s = get_d_m_s(v)
                fields.extend(["lon_d","lon_m","lon_s"])
                values.extend([d, m, s])
                continue
            elif k == "latitude":
                d, m, s = get_d_m_s(v)
                fields.extend(["lat_d", "lat_m", "lat_s"])
                values.extend([d, m, s])
                continue

            fields.append(k)
            values.append(v)

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
        "统一社会信用代码": "uniform_credit_code:str",
        "单位详细名称": "ent_name:str",
        "区划代码": "region_code:str",
        "地址": "address:str",
        "经度": "longitude:str",
        "纬度": "latitude:str",
        "法定代表人（单位负责人）": "legal_person:str",
        "开业（成立）时间": "open_date:str",
        "联系人": "ent_contact:str",
        "联系电话": "ent_phone:str",
        "是/否正常运营": "run_normally:str",
        "餐饮类型": "restaurant_type:str",
        "可容纳就餐人数": "customer_capacity:int",
        "员工数量": "employee_num:int",
        "年营业额（万元）": "annual_turnover:float",
        "经营面积（m2）": "ent_area:float",
        "食用油使用量（吨）": "cooking_oil:float",
        "年用水量（m³）": "water_used:float",
        "是否有隔油设施": "oil_device:str",
        "年废水排放量": "water_waster_emit:float",
        "化学需氧量浓度": "water_cod:float",
        "动植物油浓度": "water_oil:float",
        "氨氮浓度": "water_nh4:float",
        "总磷浓度": "water_tp:float",
        "是否安装在线监测": "water_monitor:str",
        "是否有油烟净化装置": "gas_device:str",
        "油烟排放风量": "gas_emission_vol:float",
        "油烟颗粒物浓度（mg/m3）": "gas_solid:float",
        "非甲烷总烃浓度（mg/m3）": "not_ch4:float",
        "油烟排放设施年运行时间": "device_runtime:float",
        "餐厨垃圾产生量": "kitchen_waster_volume:float",
        "餐厨垃圾去向": "kitchen_waster_gone:str",
        "炉头数": "burner_num:int",
        "街道办": "town:str",
    }
    success_count = 0
    for row in rows:
        item = {}
        for i, col in enumerate(columns):
            val = row[i]
            if col in valid_names:
                valid_name = valid_names[col]
                valid_name, type_str = valid_name.split(":")
                val = to_type(val, type_str)
                if val is not None:
                    item[valid_name] = val
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
