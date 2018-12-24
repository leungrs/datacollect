# coding: utf-8
from datetime import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template,
    request, url_for, jsonify, make_response
)
from pyexcel_webio import make_response_from_array

from datacollect import get_db
from datacollect.common import ADMIN_HANDLER
from datacollect.views.auth import login_required
from datacollect.dao import restaurant, select


bp = Blueprint('restaurant', __name__, url_prefix="/restaurant")


@bp.route('/')
@login_required
def index():
    ADMIN_HANDLER.select_by_index()
    return render_template('restaurant/index.html', admins=ADMIN_HANDLER.get_admins())


@bp.route("/query", methods=["POST"])
@login_required
def query():
    param = request.json
    user = g.user
    username = user['username']
    role = user['role']
    if role == 'user':
        param["uniform_credit_code"] = username

    total, rows = select(
        db=get_db(),
        select_fields=[
            "id", "ent_name", "province",
            "uniform_credit_code"
        ],
        table_name="ent_restaurant_survey",
        param=param
    )
    data = {"total": total, "rows": rows}
    return jsonify(data)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    """Create a new post for the current user."""
    item = None
    if request.method == 'POST':
        item = request.form.copy()
        item["updated_date"] = datetime.now()
        item["updated_by"] = g.user["username"]
        error = restaurant.insert_update(get_db(), item)
        if error is not None:
            flash(error)
        else:
            return redirect(url_for('restaurant.index'))
    ADMIN_HANDLER.select_by_item(item)
    admins = ADMIN_HANDLER.get_admins()
    return render_template('restaurant/update.html', item=None, admins=admins)


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    """Update a post if the current user is the author."""
    if request.method == 'POST':
        item = request.form
        error = restaurant.insert_update(get_db(), item, id)
        if error is not None:
            flash(error)
        else:
            return redirect(url_for('restaurant.index'))
    else:
        item = restaurant.select_by_id(get_db(), id)
    ADMIN_HANDLER.select_by_item(item)
    admins = ADMIN_HANDLER.get_admins()
    return render_template('restaurant/update.html', item=item, admins=admins)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    restaurant.delete_by_id(get_db(), id)
    return redirect(url_for('restaurant.index'))


@bp.route('/<int:id>/export', methods=('GET',))
@login_required
def export(id):
    item = restaurant.select_by_id(get_db(), id)
    result = render_template("restaurant/rest.xml", item=item)
    response = make_response(result)
    response.headers["Content-Disposition"] = "attachment; filename=restaurant.doc"
    return response


@bp.route("/stat_exp", methods=["POST"])
def stat_export():
    """统计导出"""
    param = request.form
    array = restaurant.stat_exp(get_db(), param)
    file_name = "餐饮统计-"
    town = param.get("town")
    if not town:
        town = "全部"
    file_name += town
    return make_response_from_array(array, "xlsx", sheet_name="Sheet1", file_name="{0}.xlsx".format(file_name))

