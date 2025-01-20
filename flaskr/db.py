from flask import current_app, g
import sqlite3
import datetime
import click
import os


def get_db():
    if 'db' not in g:
        db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database_files', 'pf_app.db')
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    # initialize db schema here

# create command line command: call initialize db and 
@click.command('init-db')
def init_db_command():
    # """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)

def init_app(app):
    app.teardown_appcontext(close_db) # call when cleaning up after returning response
    app.cli.add_command(init_db_command)