# coding: utf-8

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
    restaurants = restaurant.select_restaurant(get_db(), {})
    return render_template('restaurant/index.html')


@bp.route("/query", methods=["POST"])
@login_required
def query():
    restaurants = restaurant.select_restaurant(get_db(), {})
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


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    """Create a new post for the current user."""
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('restaurant/create.html')


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    """Update a post if the current user is the author."""
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ? WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


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
