# coding: utf-8


from datacollect.common import to_type, to_d_m_s
from datacollect.dao import sqlite3_row_to_dict


def select_by_id(db, id):
    sql = "select * from org_survey where id=?"
    org = db.execute(sql, [id]).fetchone()
    item = sqlite3_row_to_dict(org)
    return item


def delete_by_id(db, id):
    item = select_by_id(db, id)
    if item:
        sql = "delete from org_survey where id=?"
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
            sql = "update org_survey set "
            sql += ",".join("{0}=?".format(f) for f in fields)
            sql += " where id=?"
            values.append(id)
        else:
            sql = "insert into org_survey({0})".format(",".join(fields))
            sql += " values ({0})".format(",".join("?" * len(fields)))
        db.execute(sql, values)
        db.commit()
    except Exception as e:
        return str(e)


def import_org_from_array(array, db, updated_date, updated_by):
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
        err_msg = insert_update(db, item)
        if not err_msg:
            success_count += 1
    return success_count
