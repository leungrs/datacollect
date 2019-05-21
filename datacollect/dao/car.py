# coding: utf-8


from datacollect.common import to_type, to_d_m_s, Result
from datacollect.dao import sqlite3_row_to_dict


def select_by_id(db, id):
    sql = "select * from car_survey where id=?"
    car = db.execute(sql, [id]).fetchone()
    item = sqlite3_row_to_dict(car)
    return item


def delete_by_id(db, id):
    item = select_by_id(db, id)
    if item:
        sql = "delete from car_survey where id=?"
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
            if k == "longitude":
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
            sql = "update car_survey set "
            sql += ",".join("{0}=?".format(f) for f in fields)
            sql += " where id=?"
            values.append(id)
        else:
            sql = "insert into car_survey({0})".format(",".join(fields))
            sql += " values ({0})".format(",".join("?" * len(fields)))
        db.execute(sql, values)
        db.commit()
    except Exception as e:
        return str(e)


def delete_all(db):
    try:
        sql = "delete from car_survey"
        db.execute(sql)
        db.commit()
        return Result()
    except Exception as e:
        return Result(message="删除失败:%s" % e)