# coding: utf-8


def select_restaurant(db, param):
    sql = "select * from ent_restaurant_survey "
    print(param)
    restaurants = db.execute(sql).fetchall()
    return restaurants


def save(db, param):
    try:
        fields = []
        values = []
        for k,v in param.items():
            fields.append(k)
            values.append(v)

        sql = "insert into ent_restaurant_survey({0})".format(",".join(fields))
        sql += " values ({0})".format(",".join("?"*len(fields)))
        db.execute(sql, values)
        db.commit()
    except Exception as e:
        return str(e)



