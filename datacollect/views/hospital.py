# coding: utf-8

from datetime import datetime
from urllib.parse import quote

from flask import (
    Blueprint, flash, g, redirect, render_template,
    request, url_for, jsonify, make_response
)

from datacollect import get_db
from datacollect.common import ADMIN_HANDLER
from datacollect.views.auth import login_required
from datacollect.dao import hospital, select


bp = Blueprint('hospital', __name__, url_prefix="/hospital")


@bp.route('/')
@login_required
def index():
    return render_template('hospital/index.html')


@bp.route("/query", methods=["POST"])
@login_required
def query():
    param = request.json
    user = g.user
    username = user['username']
    role = user['role']
    if role == 'user':
        param["updated_by"] = username

    like_condition = {}
    uniform_credit_code = param.pop("uniform_credit_code", "").strip()
    if uniform_credit_code:
        like_condition["uniform_credit_code"] = uniform_credit_code
    ent_name = param.pop("ent_name", "").strip()
    if ent_name:
        like_condition["ent_name"] = ent_name

    total, rows = select(
        db=get_db(),
        select_fields=[
            "id", "ent_name", "province",
            "uniform_credit_code"
        ],
        like_condition=like_condition,
        table_name="hospital_survey",
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
        error = hospital.insert_update(get_db(), item)
        if error is not None:
            flash(error)
        else:
            return redirect(url_for('hospital.index'))
    ADMIN_HANDLER.select_by_item(item)
    admins = ADMIN_HANDLER.get_admins()
    return render_template('hospital/update.html', item=None, admins=admins)


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    """Update a post if the current user is the author."""
    if request.method == 'POST':
        item = request.form
        error = hospital.insert_update(get_db(), item, id)
        if error is not None:
            flash(error)
        else:
            return redirect(url_for('hospital.index'))
    else:
        item = hospital.select_by_id(get_db(), id)
    ADMIN_HANDLER.select_by_item(item)
    admins = ADMIN_HANDLER.get_admins()
    return render_template('hospital/update.html', item=item, admins=admins)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    hospital.delete_by_id(get_db(), id)
    return redirect(url_for('hospital.index'))


@bp.route('/<int:id>/export', methods=('GET',))
@login_required
def export(id):
    item = hospital.select_by_id(get_db(), id)
    result = render_template("hospital/hospital.xml", item=item)
    response = make_response(result)
    filename = quote("医疗表-" + item["ent_name"] + ".doc")
    response.headers["Content-Disposition"] = "attachment; filename*=utf-8''{}".format(filename)
    return response


@bp.route('/delete_all', methods=('POST',))
@login_required
def delete_all_data():
    result = hospital.delete_all(get_db())
    return jsonify(result.to_json())
