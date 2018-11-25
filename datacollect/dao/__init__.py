# coding: utf-8


def select_survey_types(db):
    sql = "select * from survey_types"
    survey_types = db.execute(sql).fetchall()
    return survey_types
