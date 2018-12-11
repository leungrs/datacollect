# coding: utf-8

from datetime import datetime
from flask_excel import make_response_from_array

from flask import (
    Blueprint, g, request, jsonify
)

from datacollect.common import Result
from datacollect.dao.restaurant import import_restaurant_from_array
from datacollect.db import get_db
from datacollect.dao import get_excel_array
from datacollect.views.auth import login_required

bp = Blueprint('common', __name__, url_prefix='/common')


@bp.route("/import", methods=["POST"])
@login_required
def import_excel():
    """"""
    array = request.get_array(field_name='file')
    excel_type = request.form["excel_type"]
    updated_date = datetime.now()
    updated_by = g.user["username"]
    result = import_from_array(array, get_db(), excel_type, updated_date, updated_by)
    return jsonify(result.to_json())


@bp.route("/export", methods=["GET"])
@login_required
def export_excel():
    """"""
    excel_type = request.args["excel_type"]
    array = get_excel_array(get_db(), excel_type)
    if array:
        return make_response_from_array(array, "xlsx", sheet_name="Sheet1", file_name="{0}.xlsx".format(excel_type))
    else:
        return "Not Data Found"


def import_from_array(data, db, excel_type, updated_date, updated_by):
    result = Result()
    success_count = 0
    if excel_type == "restaurant":
        success_count = import_restaurant_from_array(data, db, updated_date, updated_by)
    result.data = success_count
    result.message = "导入成功{}条记录".format(success_count)
    return result
