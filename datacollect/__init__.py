import os

from flask import Flask, render_template

from datacollect.db import get_db
from .config import STATIC_FOLDER, TEMPLATES_FOLDER


def create_app(config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, template_folder=TEMPLATES_FOLDER, static_folder=STATIC_FOLDER)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'datacollect.sqlite'),
    )

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

    # apply the blueprints to the app
    from datacollect.views import auth, restaurant, blog
    app.register_blueprint(auth.bp)
    app.register_blueprint(restaurant.bp)
    app.register_blueprint(blog.bp)

    # make url_for('index') == url_for('blog.index')
    # in another app, you might define a separate main index here with
    # app.route, while giving the blog blueprint a url_prefix, but for
    # the tutorial the blog will be the main index
    app.add_url_rule('/', endpoint='blog.index')

    print(app.url_map)

    return app

