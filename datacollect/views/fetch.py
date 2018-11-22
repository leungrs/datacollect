from flask import request, render_template, jsonify, Blueprint

bp = Blueprint("fetch", __name__, url_prefix="/fetch")


@bp.route('/', defaults={'js': 'plain'})
@bp.route('/<any(plain, jquery, fetch):js>')
def fetch(js):
    return render_template('{0}.html'.format(js), js=js)


@bp.route('/add', methods=['POST'])
def add():
    a = request.form.get('a', 0, type=float)
    b = request.form.get('b', 0, type=float)
    return jsonify(result=a + b)
