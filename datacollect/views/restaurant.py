# coding: utf-8
from datetime import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template,
    request, url_for, jsonify
)
from werkzeug.exceptions import abort

from datacollect import get_db
from datacollect.views.auth import login_required
from datacollect.dao import restaurant

bp = Blueprint('restaurant', __name__, url_prefix="/restaurant")


@bp.route('/')
@login_required
def index():
    return render_template('restaurant/index.html')


@bp.route("/query", methods=["POST"])
@login_required
def query():
    param = request.json
    total, restaurants = restaurant.select_by_page(get_db(), param)
    results = []
    for item in restaurants:
        results.append(
            {
                "id": item["id"],
                "ent_name": item["ent_name"],
                "uniform_credit_code": item["uniform_credit_code"],
                "province": item["province"],
            }
        )
    data = {"total": total, "rows": results}
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
    """Delete a post.

    Ensures that the post exists and that the logged in user is the
    author of the post.
    """
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))
