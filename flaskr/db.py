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

def write_transaction(user, amount, date, category, memo):
    db = get_db()
    res = db.execute("SELECT MAX(TRANS_ID) FROM TRANSACTIONS")
    max_id = res.fetchone()[0]
    new_id = 0
    if max_id is not None:
        new_id = max_id + 1
    else:
        new_id = 0

    data = (new_id, amount, category, date, memo if memo else '')
    db.execute(f"INSERT INTO TRANSACTIONS VALUES(?, ?, ?, ?, ?)", data)
    db.commit()

def read_transactions(month, year):
    db = get_db()
    res = db.execute("SELECT * FROM TRANSACTIONS WHERE TRANS_MONTH = ? AND TRANS_YEAR = ? ORDER BY TRANS_DATE DESC", (month, year)) # (TRANS_ID, TRANS_AMOUNT, TRANS_CATEGORY, TRANS_DATE, TRANS_MEMO)
    trans_list = res.fetchall()

    return trans_list

# once a new month is picked, check if it exists in the TOTALS_PER_MONTH table
def check_and_read_month_totals(month, year):
    db = get_db()
    # get information from current month
    res = db.execute("SELECT TOTAL_BALANCE, TOTAL_EXPENSES, TOTAL_INCOME FROM TOTALS_PER_MONTH WHERE MONTH = ? AND YEAR = ?", (month, year))
    res_totals = res.fetchall()

    total_values = [0, 0, 0]

    # if month is in db fetch totals, if month is not add a row with totals
    if len(res_totals) != 0:
        total_values = res_totals[0]

    # get information from past month
    res = db.execute("SELECT TOTAL_BALANCE, TOTAL_EXPENSES, TOTAL_INCOME FROM TOTALS_PER_MONTH WHERE MONTH = ? AND YEAR = ?", (int(month) - 1 if month != 1 else 12, year if month != 1 else int(year) - 1))
    res_totals = res.fetchall()

    total_differences = list(total_values)
    total_differences_percs = list(total_values)
    past_month_values = [0, 0, 0]
    
    # if month is in db fetch diffs
    if len(res_totals) != 0 and res_totals[0][2] is not None:
        past_month_values = res_totals[0]
        total_differences = [round(x - y, 2) for x, y in zip(total_differences, past_month_values)]
        for i in range(3):
            if past_month_values[i] != 0:
                total_differences_percs[i] = round(total_differences_percs[i] / past_month_values[i] * 100 - 100, 2)
    else:
        total_differences = [0, 0, 0]

    return total_values, total_differences, total_differences_percs

def update_totals(month, year, amount):
    db = get_db()

    res = db.execute("SELECT * FROM TOTALS_PER_MONTH WHERE MONTH = ? AND YEAR = ?", (month, year))
    if len(res.fetchall()) != 0: 
        # if month exists in table, update
        db.execute("UPDATE TOTALS_PER_MONTH SET TOTAL_EXPENSES = TOTAL_EXPENSES + ? WHERE MONTH = ? AND YEAR = ?", (amount, month, year))
    else:
        # if month does not exist in table, add it
        db.execute("INSERT INTO TOTALS_PER_MONTH VALUES(?, ?, 0, ?, 0)", (month, year, amount))

    db.commit()

def read_categories():
    db = get_db()

    res = db.execute("SELECT DISTINCT TRANS_CATEGORY FROM TRANSACTIONS ORDER BY TRANS_CATEGORY")
    categories = [row['TRANS_CATEGORY'] for row in res.fetchall()]

    return categories

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