# coding: utf-8


from datacollect.common import to_type


def select_by_page(db, param):
    limit = param["limit"]
    offset = param["offset"]
    sql = "select * from ent_restaurant_survey order by id desc limit {0} offset {1}".format(limit, offset)
    sql_count = "select count(*) from ent_restaurant_survey"
    r = db.execute(sql_count).fetchone()
    count = r[0]
    restaurants = db.execute(sql).fetchall()
    return count, restaurants


def to_d_m_s(val):
    i_d = int(val)
    m=(val-i_d)*60
    i_m = int(m)
    i_s = int((m - i_m) * 60)
    return i_d, i_m, i_s


def select_by_id(db, id):
    sql = "select * from ent_restaurant_survey where id=?"
    restaurant = db.execute(sql, [id]).fetchone()
    item = None
    if restaurant:
        item = {}
        for f in restaurant.keys():
            item[f] = restaurant[f]

        longitude = to_type(item["longitude"], float, 0)
        latitude = to_type(item["latitude"], float, 0)
        lon_d, lon_m, lon_s = to_d_m_s(longitude)
        lat_d, lat_m, lat_s = to_d_m_s(latitude)
        item["lon_d"] = lon_d
        item["lon_m"] = lon_m
        item["lon_s"] = lon_s
        item["lat_d"] = lat_d
        item["lat_m"] = lat_m
        item["lat_s"] = lat_s
    return item


def insert_update(db, param, id=None):
    try:
        fields = []
        values = []
        longitude = 0
        latitude = 0
        for k, v in param.items():
            if k == "lon_d":
                longitude += to_type(v, float, 0)
                continue
            if k == "lon_m":
                longitude += to_type(v, float, 0) / 60
                continue
            if k == "lon_s":
                longitude += to_type(v, float, 0) / 3600
                continue
            if k == "lat_d":
                latitude += to_type(v, float, 0)
                continue
            if k == "lat_m":
                latitude += to_type(v, float, 0)/60
                continue
            if k == "lat_s":
                latitude += to_type(v, float, 0)/3600
                continue

            fields.append(k)
            values.append(v)

        fields.extend(["longitude", "latitude"])
        values.extend([longitude, latitude])

        if id is not None:
            sql = "update ent_restaurant_survey set "
            sql += ",".join("{0}=?".format(f) for f in fields)
            sql += " where id=?"
            values.append(id)
        else:
            sql = "insert into ent_restaurant_survey({0})".format(",".join(fields))
            sql += " values ({0})".format(",".join("?" * len(fields)))
        db.execute(sql, values)
        db.commit()
    except Exception as e:
        return str(e)
