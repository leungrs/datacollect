import os
from datetime import date, datetime
from flask import Flask
import flask_excel
from jinja2 import Undefined

from datacollect.db import get_db
from .config import STATIC_FOLDER, TEMPLATES_FOLDER


def create_app(config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, template_folder=TEMPLATES_FOLDER, static_folder=STATIC_FOLDER)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'datacollect.sqlite'),
    )

    app.add_template_filter(string_filter, "s")
    app.add_template_filter(number_filter, "num")
    app.add_template_filter(date_filter, "date")

    if config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.update(config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register the database commands
    from datacollect import db
    db.init_app(app)
    flask_excel.init_excel(app)

    # apply the blueprints to the app
    from datacollect.views import auth, restaurant, common, \
        hospital, admin, car, gas, river, org, life
    app.register_blueprint(auth.bp)
    app.register_blueprint(restaurant.bp)
    app.register_blueprint(common.bp)
    app.register_blueprint(hospital.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(car.bp)
    app.register_blueprint(gas.bp)
    app.register_blueprint(river.bp)
    app.register_blueprint(life.bp)
    app.register_blueprint(org.bp)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule('/', endpoint='restaurant.index')

    print(app.url_map)

    return app


def string_filter(value, length=0):
    if not value:
        return " " * length if length else ""
    return str(value)


def number_filter(value, n=2):
    if value is None or value == '' or isinstance(value, Undefined):
        return "    "
    if n == 0:
        return int(value)
    return round(value, n)


def date_filter(value):
    if not value:
        return ""
    if isinstance(value, (date, datetime)):
        return value.strftime("%Y-%m-%d")
    return ""
