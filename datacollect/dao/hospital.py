# coding: utf-8


from datacollect.common import to_type, to_d_m_s, Result
from datacollect.dao import sqlite3_row_to_dict, get_town_from_address, FUTIAN


def select_by_id(db, id):
    sql = "select * from hospital_survey where id=?"
    hospital = db.execute(sql, [id]).fetchone()
    item = sqlite3_row_to_dict(hospital)
    return item


def delete_by_id(db, id):
    item = select_by_id(db, id)
    if item:
        sql = "delete from hospital_survey where id=?"
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
            sql = "update hospital_survey set "
            sql += ",".join("{0}=?".format(f) for f in fields)
            sql += " where id=?"
            values.append(id)
        else:
            sql = "insert into hospital_survey({0})".format(",".join(fields))
            sql += " values ({0})".format(",".join("?" * len(fields)))
        db.execute(sql, values)
        db.commit()
    except Exception as e:
        return str(e)


def import_hospital_from_array(array, db, updated_date, updated_by):
    """导入餐饮表，返回导入的记录数"""
    columns = array[0]
    rows = array[1:]
    valid_names = {
        "统一社会信用代码": "uniform_credit_code",
        "单位名称": "ent_name",
        "单位地址": "address",
        "经度": "longitude:float",
        "纬度": "latitude:float",
        "法人代表": "legal_person",
        "开业时间": "open_date",
        "联系人": "ent_contact",
        "手机号码": "ent_phone:str",
        "建筑面积": "building_area:float",
        "床位数": "bed_num:int",
        "是否安装在线监测": "water_monitor",
        "填表人": "survey_person",
        "废水处理工艺名称": "water_process_name",
        "年废水排放量": "water_waster_emit",
        "废水排放浓度COD": "water_cod",
        "废水排放浓度BOD": "water_bod",
        "粪大肠菌群": "water_fecal_coliform",
        "医疗废物1名称、类别": "waster1_type",
        "医疗废物1年生产量": "waster1_annual",
        "医疗废物1交持证单位量": "waster1_jcz",
        "医疗废物2名称、类别": "waster2_type",
        "医疗废物2年生产量": "waster2_annual",
        "医疗废物2交持证单位量": "waster2_jcz",
        "医疗废物3名称、类别": "waster3_type",
        "医疗废物3年生产量": "waster3_annual",
        "医疗废物3交持证单位量": "waster3_jcz",
        "区划代码": "region_code",
        "年就诊人数": "patient_num",
        "年营业额": "annual_turnover",
    }
    success_count = 0
    for row in rows:
        item = {}
        town = ""
        for i, col in enumerate(columns):
            val = row[i]
            if col in valid_names:
                valid_name = valid_names[col]
                if ":" in valid_name:
                    valid_name, type_str = valid_name.split(":")
                    val = to_type(val, type_str)
                item[valid_name] = val
            elif col == "街道办":
                town = val

        item["updated_date"] = updated_date
        item["updated_by"] = updated_by
        item.update(FUTIAN)
        item["town"] = get_town_from_address(town, startswith=True)
        err_msg = insert_update(db, item)
        if not err_msg:
            success_count += 1
    return success_count


def delete_all(db):
    try:
        sql = "delete from hospital_survey"
        db.execute(sql)
        db.commit()
        return Result()
    except Exception as e:
        return Result(message="删除失败:%s" % e)
