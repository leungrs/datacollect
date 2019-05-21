# coding: utf-8


from datacollect.common import to_type, to_d_m_s, Result, get_d_m_s
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
        "统一社会信用代码": "uniform_credit_code:str",
        "单位名称": "ent_name:str",
        "单位地址": "address:str",
        "经度": "longitude:float",
        "纬度": "latitude:float",
        "法人代表": "legal_person:str",
        "开业时间": "open_date:str",
        "联系人": "ent_contact:str",
        "手机号码": "ent_phone:str",
        "建筑面积": "building_area:float",
        "床位数": "bed_num:int",
        "是否安装在线监测": "water_monitor:str",
        "填表人": "survey_person:str",
        "是否正常运营": "run_normally:str",
        "废水处理工艺名称": "water_process_name:str",
        "年废水排放量（m3）": "water_waster_emit:float",
        "年用水量（m3）": "water_used:float",
        "废水排放浓度COD(mg/m3)": "water_cod:float",
        "BOD(mg/m3)": "water_bod:float",
        "粪大肠菌群（个/L）": "water_fecal_coliform:float",
        "医疗废物1名称、类别": "waster1_type:str",
        "医疗废物1年产生量（吨）": "waster1_annual:float",
        "医疗废物1交持证单位量（吨）": "waster1_jcz:float",
        "医疗废物2名称、类别": "waster2_type:str",
        "医疗废物2年产生量（吨）": "waster2_annual:float",
        "医疗废物2交持证单位量（吨）": "waster2_jcz:float",
        "医疗废物3名称、类别": "waster3_type:str",
        "医疗废物3年产生量（吨）": "waster3_annual:float",
        "医疗废物3交持证单位量（吨）": "waster3_jcz:float",
        "区划代码": "region_code:str",
        "年就诊人数（人）": "patient_num:int",
        "年营业额（万元）": "annual_turnover:float",
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
        if not item.get("town"):
            item["town"] = get_town_from_address(item.get("address") or "")
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
