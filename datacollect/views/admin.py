# coding: utf-8


from flask import Blueprint, render_template, request, g, jsonify
from werkzeug.security import generate_password_hash

from datacollect import get_db
from datacollect.common import Result
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


@bp.route("/save_user", methods=["POST"])
def save_user():
    param = request.json
    role = param.get("role") or "user"
    username = param.get("username")
    user_id = param.get("user_id")
    db = get_db()
    result = Result()

    if not username:
        result.message = '请输入用户名'
    else:
        if not user_id:
            sql = 'SELECT id FROM user WHERE username = ?'
            if db.execute(sql, (username,)).fetchone() is not None:
                result.message = '用户名 {0} 已经存在'.format(username)

    if result:
        if not user_id:
            db.execute(
                'INSERT INTO user (username, role, password) VALUES (?, ?, ?)',
                (username, role, generate_password_hash("888888"))
            )
        else:
            db.execute(
                'update user set username=?, role=? where id=?',
                (username, role, user_id)
            )
        db.commit()

    return jsonify(result.to_json())


@bp.route("/reset_pass", methods=["POST"])
def reset_pass():
    """重置密码"""
    param = request.json
    role = param.get("role") or "user"
    username = param.get("username")
    user_id = param.get("user_id")
    db = get_db()
    result = Result()

    if not username:
        result.message = '请输入用户名'
    else:
        if not user_id:
            sql = 'SELECT id FROM user WHERE username = ?'
            if db.execute(sql, (username,)).fetchone() is not None:
                result.message = '用户名 {0} 已经存在'.format(username)

    if result:
        if not user_id:
            db.execute(
                'INSERT INTO user (username, role, password) VALUES (?, ?, ?)',
                (username, role, generate_password_hash("888888"))
            )
        else:
            db.execute(
                'update user (username, role) set username=?, role=? where id=?',
                (username, role, user_id)
            )
        db.commit()

    return jsonify(result.to_json())
