# coding: utf-8


def select_restaurant(db, param):
    sql = "select * from ent_restaurant_survey "
    print(param)
    restaurants = db.execute(sql).fetchall()
    return restaurants
