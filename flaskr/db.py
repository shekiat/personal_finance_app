from flask import current_app, g
import sqlite3
import datetime
import click
import os
from dateutil.parser import parse

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

def write_to_db(user="Jim Gorden", amount=None, date='12-25-2024', category='BILLS', memo='TEST'):
    def parse_date(date):
        try:
            return parse(date)
        except ValueError:
            return None  # Return None if the input is not a valid date

    db = get_db()
    data = (db.execute("SELECT MAX(TRANS_ID) FROM TRANSACTIONS").fetchone()[0] + 1, amount, category, parse_date(date).date(), memo)
    db.execute(f"INSERT INTO TRANSACTIONS VALUES(?, ?, ?, ?, ?)", data)
    db.commit()


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