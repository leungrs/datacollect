# coding: utf-8

from datacollect.common import Result, to_type
from datacollect.dao import restaurant
import pandas as pd


def import_restaurant_from_df(df, db, updated_date, updated_by):
    """导入餐饮表，返回导入的记录数"""
    columns = df.columns.tolist()
    row_count = len(df)
    rows = []
    for i in range(1, row_count):
        rows.append(df.ix[i].tolist())
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


def import_from_df(df, db,  excel_type, updated_date, updated_by):
    result = Result()
    success_count = 0
    if excel_type == "restaurant":
        success_count = import_restaurant_from_df(df, db, updated_date, updated_by)
    result.data = success_count
    result.message = "导入成功{}条记录".format(success_count)
    return result
