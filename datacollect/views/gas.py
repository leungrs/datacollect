# coding: utf-8

from datetime import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template,
    request, url_for, jsonify, make_response
)

from datacollect import get_db
from datacollect.common import ADMIN_HANDLER
from datacollect.views.auth import login_required
from datacollect.dao import gas, select

bp = Blueprint('gas', __name__, url_prefix="/gas")


@bp.route('/')
@login_required
def index():
    return render_template('gas/index.html')


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
        table_name="gas_survey",
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
        error = gas.insert_update(get_db(), item)
        if error is not None:
            flash(error)
        else:
            return redirect(url_for('gas.index'))
    ADMIN_HANDLER.select_by_item(item)
    admins = ADMIN_HANDLER.get_admins()
    return render_template('gas/update.html', item=item, admins=admins)


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    """Update a post if the current user is the author."""
    if request.method == 'POST':
        item = request.form
        error = gas.insert_update(get_db(), item, id)
        if error is not None:
            flash(error)
        else:
            return redirect(url_for('gas.index'))
    else:
        item = gas.select_by_id(get_db(), id)
    ADMIN_HANDLER.select_by_item(item)
    admins = ADMIN_HANDLER.get_admins()
    return render_template('gas/update.html', item=item, admins=admins)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    gas.delete_by_id(get_db(), id)
    return redirect(url_for('gas.index'))


@bp.route('/<int:id>/export', methods=('GET',))
@login_required
def export(id):
    item = gas.select_by_id(get_db(), id)
    result = render_template("gas/rest.xml", item=item)
    response = make_response(result)
    response.headers["Content-Disposition"] = "attachment; filename=gas.doc"
    return response
