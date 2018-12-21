# coding: utf-8


from flask import Blueprint, render_template, request, g, jsonify

from datacollect import get_db
from datacollect.dao import select

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route("/users")
def users():
    return render_template("admin/users.html")


@bp.route("/query_user", methods=["POST"])
def query_user():
    param = request.json
    total, rows = select(
        db=get_db(),
        select_fields=[
            "id", "username", "role"
        ],
        table_name="user",
        param=param
    )
    data = {"total": total, "rows": rows}
    return jsonify(data)
