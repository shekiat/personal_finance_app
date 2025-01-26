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

def parse_date(date):
        try:
            return parse(date)
        except ValueError:
            return None  # Return None if the input is not a valid date

def write_transaction(user="Jim Gorden", amount=None, date='12-25-2024', category='BILLS', memo=None):
    db = get_db()
    data = (db.execute("SELECT MAX(TRANS_ID) FROM TRANSACTIONS").fetchone()[0] + 1, amount, category, date, memo if memo else '')
    db.execute(f"INSERT INTO TRANSACTIONS VALUES(?, ?, ?, ?, ?)", data)
    db.commit()

def read_transactions():
    db = get_db()
    res = db.execute("SELECT * FROM TRANSACTIONS ORDER BY TRANS_DATE DESC") # (TRANS_ID, TRANS_AMOUNT, TRANS_CATEGORY, TRANS_DATE, TRANS_MEMO)
    trans_list = res.fetchall()

    return trans_list

# once a new month is picked, check if it exists in the TOTALS_PER_MONTH table
def check_and_read_month_totals(month, year):
    db = get_db()
    res = db.execute("SELECT TOTAL_BALANCE, TOTAL_EXPENSES, TOTAL_INCOME FROM TOTALS_PER_MONTH WHERE MONTH = ? AND YEAR = ?", (month, year))
    res_totals = res.fetchall()

    total_balance = 0
    total_expenses = 0
    total_income = 0

    # if month is in db fetch totals, if month is not add a row with totals
    if len(res_totals) == 0:
        db.execute("INSERT INTO TOTALS_PER_MONTH VALUES(?, ?, 0, 0, 0)", (month, year))
        db.commit()
    else:
        total_balance, total_expenses, total_income = res_totals[0]

    return total_balance, total_expenses, total_income
        



        
    



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