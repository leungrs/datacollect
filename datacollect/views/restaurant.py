# coding: utf-8
from datetime import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template,
    request, url_for, jsonify, make_response
)

from datacollect import get_db
from datacollect.views.auth import login_required
from datacollect.dao import restaurant, select

bp = Blueprint('restaurant', __name__, url_prefix="/restaurant")


@bp.route('/')
@login_required
def index():
    return render_template('restaurant/index.html')


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
    if request.method == 'POST':
        data = request.form.copy()
        data["updated_date"] = datetime.now()
        data["updated_by"] = g.user["username"]
        error = restaurant.insert_update(get_db(), data)
        if error is not None:
            flash(error)
        else:
            return redirect(url_for('restaurant.index'))
    return render_template('restaurant/update.html', item=None)


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
    return render_template('restaurant/update.html', item=item)


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
