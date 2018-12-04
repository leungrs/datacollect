import sqlite3

import click
import os
import time
from flask import current_app, g
from flask.cli import with_appcontext


schema_sql_file = "sql/schema.sqlite.sql"
data_sql_file = "sql/data.sqlite.sql"


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """Clear existing data and create new tables."""

    # backup old db if exists
    database = current_app.config['DATABASE']
    timestamp = time.strftime("%Y%m%d%H%M%S")
    if os.path.exists(database):
        os.rename(database, database + "." + timestamp)

    db = get_db()

    with current_app.open_resource(schema_sql_file) as f:
        db.executescript(f.read().decode('utf8'))
    with current_app.open_resource(data_sql_file) as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def create_database():
    db = sqlite3.connect(
        current_app.config['DATABASE'],
        detect_types=sqlite3.PARSE_DECLTYPES
    )
    g.db.row_factory = sqlite3.Row


@click.command("passhash")
@with_appcontext
def password_hash(password):
    import sys
    from werkzeug.security import generate_password_hash
    print(sys.argv)
    h = generate_password_hash("666888")
    print(h)
