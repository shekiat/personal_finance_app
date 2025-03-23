from flask import current_app, g
import sqlite3
import datetime
import click
import os
import dateutil
from dateutil.parser import parse
import psycopg2
import psycopg2.extras

month_to_int = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}


from flask import current_app, g
import sqlite3
import datetime
import click
import os
from dateutil.parser import parse

month_to_int = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}

# def get_db():
#     if 'db' not in g:
#         db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database_files', 'pf_app.db')
#         g.db = sqlite3.connect(db_path)
#         g.db.row_factory = sqlite3.Row
#     return g.db


# def close_db(e=None):
#     db = g.pop('db', None)

#     if db is not None:
#         db.close()

# def parse_date(date):
#         try:
#             return parse(date)
#         except ValueError:
#             return None  # Return None if the input is not a valid date



# # transactions
# def write_transaction(user, amount, date, category, memo):
#     db = get_db()
#     res = db.execute("SELECT MAX(TRANS_ID) FROM TRANSACTIONS")
#     max_id = res.fetchone()[0]
#     new_id = 0
#     if max_id is not None:
#         new_id = max_id + 1
#     else:
#         new_id = 0

#     amount = amount 
    
#     if str(amount)[0] == '$':
#         amount = int(str(amount)[1:])

#     data = (new_id, amount, category.title(), date, memo if memo else '')
#     db.execute(f"INSERT INTO TRANSACTIONS VALUES(?, ?, ?, ?, ?)", data)
#     db.commit()

# def read_transactions(month, year):
#     db = get_db()
#     res = db.execute("SELECT * FROM TRANSACTIONS WHERE MONTH = ? AND YEAR = ? ORDER BY TRANS_DATE DESC", (month, year)) # (TRANS_ID, TRANS_AMOUNT, TRANS_CATEGORY, TRANS_DATE, TRANS_MEMO)
#     trans_list = res.fetchall()

#     return trans_list

# def delete_transaction(trans_id):
#     db = get_db()
#     db.execute("DELETE FROM TRANSACTIONS WHERE TRANS_ID = ?", (trans_id,))
#     db.commit()



# # income
# def write_income(user, amount, date, memo):
#     db = get_db()
#     res = db.execute("SELECT MAX(INCOME_ID) FROM INCOME")
#     max_id = res.fetchone()[0]
#     new_id = 0
#     if max_id is not None:
#         new_id = max_id + 1
#     else:
#         new_id = 0

#     amount = amount 
    
#     if str(amount)[0] == '$':
#         amount = int(str(amount)[1:])

#     data = (new_id, amount, date, memo if memo else '')
#     db.execute(f"INSERT INTO INCOME VALUES(?, ?, ?, ?)", data)
#     db.commit()

# def read_income(month, year):
#     db = get_db()
#     res = db.execute("SELECT * FROM INCOME WHERE MONTH = ? AND YEAR = ? ORDER BY INCOME_DATE DESC", (month, year)) # (INCOME_ID, INCOME_AMOUNT, INCOME_CATEGORY, INCOME_DATE, INCOME_MEMO, MONTH, YEAR)
#     income_list = res.fetchall()

#     return income_list

# def delete_income(income_id):
#     db = get_db()
#     db.execute("DELETE FROM INCOME WHERE INCOME_ID = ?", (income_id,))
#     db.commit()



# # totals
# # once a new month is picked, check if it exists in the TOTALS_PER_MONTH table
# def check_and_read_month_totals(month, year, for_dashboard):
#     db = get_db()
#     # get information from current month
#     res = db.execute("SELECT TOTAL_BALANCE, TOTAL_EXPENSES, TOTAL_INCOME FROM TOTALS_PER_MONTH WHERE MONTH = ? AND YEAR = ?", (month, year))
#     res_totals = res.fetchall()

#     total_values = [0, 0, 0]

#     # if month is in db fetch totals, if month is not add a row with totals
#     if len(res_totals) != 0:
#         total_values = res_totals[0]

#     total_values = [round(total, 2) for total in total_values]

#     print(total_values)
    
#     total_differences = list(total_values)
#     total_differences_percs = list(total_values)
#     past_month_values = [0, 0, 0]

#     if not for_dashboard:
#         # get information from past month
#         res = db.execute("SELECT TOTAL_BALANCE, TOTAL_EXPENSES, TOTAL_INCOME FROM TOTALS_PER_MONTH WHERE MONTH = ? AND YEAR = ?", (int(month) - 1 if month != 1 else 12, year if month != 1 else int(year) - 1))
#         res_totals = res.fetchall()
        
#         # if month is in db fetch diffs
#         if len(res_totals) != 0 and res_totals[0][2] is not None:
#             past_month_values = res_totals[0]
#             total_differences = [round(x - y, 2) for x, y in zip(total_differences, past_month_values)]
#             for i in range(3):
#                 if past_month_values[i] != 0:
#                     total_differences_percs[i] = round(total_differences_percs[i] / past_month_values[i] * 100 - 100, 2)
#         else:
#             total_differences = [0, 0, 0]

#     return total_values, total_differences, total_differences_percs

# def update_totals(month=None, year=None):
#     db = get_db()

#     if [month, year] != [None, None]: # = [None, None] if we are not adding a transaction
#         res = db.execute("SELECT * FROM TOTALS_PER_MONTH WHERE MONTH = ? AND YEAR = ?", (month, year))
#         if len(res.fetchall()) == 0: 
#             db.execute("INSERT INTO TOTALS_PER_MONTH VALUES(?, ?, 0, 0, 0)", (month, year))

#     db.execute("UPDATE TOTALS_PER_MONTH SET TOTAL_EXPENSES = month_sum_table.MONTH_SUMS FROM (SELECT  SUM(TRANS_AMOUNT) AS MONTH_SUMS, MONTH, YEAR FROM TRANSACTIONS GROUP BY MONTH, YEAR) AS month_sum_table WHERE TOTALS_PER_MONTH.MONTH =  month_sum_table.MONTH AND  TOTALS_PER_MONTH.YEAR=  month_sum_table.YEAR")
#     db.execute("UPDATE TOTALS_PER_MONTH SET TOTAL_INCOME = month_sum_table.MONTH_SUMS FROM (SELECT  SUM(INCOME_AMOUNT) AS MONTH_SUMS, MONTH, YEAR FROM INCOME GROUP BY MONTH, YEAR) AS month_sum_table WHERE TOTALS_PER_MONTH.MONTH =  month_sum_table.MONTH AND TOTALS_PER_MONTH.YEAR = month_sum_table.YEAR")
#         # UPDATE TOTALS_PER_MONTH
#         # SET TOTAL_EXPENSES/INCOME = month_sum_table.MONTH_SUMS
#         # FROM (SELECT  SUM(TRANS/INCOME_AMOUNT) AS MONTH_SUMS, MONTH, YEAR FROM TRANSACTIONS/INCOME  GROUP BY MONTH, YEAR) AS month_sum_table
#         # WHERE TOTALS_PER_MONTH.MONTH =  month_sum_table.MONTH AND  TOTALS_PER_MONTH.YEAR=  month_sum_table.YEAR 

#     db.commit()

# def read_categories():
#     db = get_db()

#     res = db.execute("SELECT DISTINCT TRANS_CATEGORY FROM TRANSACTIONS ORDER BY TRANS_CATEGORY")
#     categories = [row['TRANS_CATEGORY'] for row in res.fetchall()]

#     return categories



# # dashboard
# def read_month_totals_for_line_graph(year):
#     months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

#     total_balances = []
#     total_expenses = []
#     total_incomes = []

#     for month in months:
#         total_values, _, _ = check_and_read_month_totals(months.index(month) + 1, year, True)
#         total_balances.append(total_values[0])
#         total_expenses.append(total_values[1])
#         total_incomes.append(total_values[2])

#     return total_balances, total_expenses, total_incomes

# def read_category_totals_for_pie_graph(month, year):
#     db = get_db()

#     res = db.execute("SELECT TRANS_CATEGORY, SUM(TRANS_AMOUNT) AS AMOUNT FROM TRANSACTIONS WHERE MONTH = ? AND YEAR = ? GROUP BY TRANS_CATEGORY", (month_to_int[month], year))
#     categories_totals = res.fetchall()
#     categories_totals = [dict(row) for row in categories_totals]
#     pie_dict = {}
#     for i in range(len(categories_totals)):
#         pie_dict[categories_totals[i]["TRANS_CATEGORY"]] = categories_totals[i]["AMOUNT"]

#     return pie_dict




# def init_db():
#     db = get_db()

#     # initialize db schema here

# # create command line command: call initialize db and 
# @click.command('init-db')
# def init_db_command():
#     # """Clear the existing data and create new tables."""
#     init_db()
#     click.echo('Initialized the database.')


# sqlite3.register_converter(
#     "timestamp", lambda v: datetime.fromisoformat(v.decode())
# )

# def init_app(app):
#     app.teardown_appcontext(close_db) # call when cleaning up after returning response
#     app.cli.add_command(init_db_command)

def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(dbname='MoneyMateDB',
            user='nsteiner25',
            host='localhost',
            password='235jl'
        ).cursor(cursor_factory=psycopg2.extras.DictCursor)
        
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



# transactions
def write_transaction(user, amount, date, category, memo):
    db = get_db()
    db.execute("SELECT MAX(TRANS_ID) FROM TRANSACTIONS")
    max_id = db.fetchone()[0]
    new_id = 0
    if max_id is not None:
        new_id = max_id + 1
    else:
        new_id = 0

    amount = amount 
    
    if str(amount)[0] == '$':
        amount = int(str(amount)[1:])

    data = (new_id, amount, category.title(), date, memo if memo else '')
    db.execute(f"INSERT INTO TRANSACTIONS VALUES(%s, %s, %s, %s, %s)", data)
    db.commit()

def read_transactions(month, year):
    db = get_db()
    db.execute("SELECT * FROM TRANSACTIONS WHERE MONTH = %s AND YEAR = %s ORDER BY TRANS_DATE DESC", (month, year)) # (TRANS_ID, TRANS_AMOUNT, TRANS_CATEGORY, TRANS_DATE, TRANS_MEMO)
    trans_list_res = db.fetchall()
    trans_list = []

    for transaction in trans_list_res:
        trans_list_element = []
        for i in range(len(transaction)):
            if i == 1:
                trans_list_element.append(float(transaction[i]))
            elif i == 3:
                trans_list_element.append(transaction[i].strftime('%Y-%m-%d'))
            else:
                trans_list_element.append(transaction[i])
        trans_list.append(trans_list_element)

    return trans_list

def delete_transaction(trans_id):
    db = get_db()
    db.execute("DELETE FROM TRANSACTIONS WHERE TRANS_ID = %s", (trans_id,))
    db.commit()



# income
def write_income(user, amount, date, memo):
    db = get_db()
    db.execute("SELECT MAX(INCOME_ID) FROM INCOME")
    max_id = db.fetchone()[0]
    new_id = 0
    if max_id is not None:
        new_id = max_id + 1
    else:
        new_id = 0

    amount = amount 
    
    if str(amount)[0] == '$':
        amount = int(str(amount)[1:])

    data = (new_id, amount, date, memo if memo else '')
    db.execute(f"INSERT INTO INCOME VALUES(%s, %s, %s, %s)", data)
    db.commit()

def read_income(month, year):
    db = get_db()
    db.execute("SELECT * FROM INCOME WHERE MONTH = %s AND YEAR = %s ORDER BY INCOME_DATE DESC", (month, year)) # (INCOME_ID, INCOME_AMOUNT, INCOME_CATEGORY, INCOME_DATE, INCOME_MEMO, MONTH, YEAR)
    income_list_res = db.fetchall()
    income_list = []

    for income in income_list_res:
        income_list_element = []
        for i in range(len(income)):
            if i == 1:
                income_list_element.append(float(income[i]))
            elif i == 2:
                income_list_element.append(income[i].strftime('%Y-%m-%d'))
            else:
                income_list_element.append(income[i])
        income_list.append(income_list_element)

    return income_list

def delete_income(income_id):
    db = get_db()
    db.execute("DELETE FROM INCOME WHERE INCOME_ID = %s", (income_id,))
    db.commit()



# totals
# once a new month is picked, check if it exists in the TOTALS_PER_MONTH table
def check_and_read_month_totals(month, year, for_dashboard):
    db = get_db()
    # get information from current month
    db.execute("SELECT TOTAL_BALANCE, TOTAL_EXPENSES, TOTAL_INCOME FROM TOTALS_PER_MONTH WHERE MONTH = %s AND YEAR = %s", (month, year))
    res_totals = db.fetchall()

    total_values = [0, 0, 0]

    # if month is in db fetch totals, if month is not add a row with totals
    if len(res_totals) != 0:
        total_values = res_totals[0]

    total_values = [round(total, 2) for total in total_values]
    
    total_differences = list(total_values)
    total_differences_percs = list(total_values)
    past_month_values = [0, 0, 0]

    if not for_dashboard:
        # get information from past month
        db.execute("SELECT TOTAL_BALANCE, TOTAL_EXPENSES, TOTAL_INCOME FROM TOTALS_PER_MONTH WHERE MONTH = %s AND YEAR = %s", (int(month) - 1 if month != 1 else 12, year if month != 1 else int(year) - 1))
        res_totals = db.fetchall()
        
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

def update_totals(month=None, year=None):
    db = get_db()

    if [month, year] != [None, None]: # = [None, None] if we are not adding a transaction
        db.execute("SELECT * FROM TOTALS_PER_MONTH WHERE MONTH = %s AND YEAR = %s", (month, year))
        if len(db.fetchall()) == 0: 
            db.execute("INSERT INTO TOTALS_PER_MONTH VALUES(%s, %s, 0, 0, 0)", (month, year))

    db.execute("UPDATE TOTALS_PER_MONTH SET TOTAL_EXPENSES = month_sum_table.MONTH_SUMS FROM (SELECT  SUM(TRANS_AMOUNT) AS MONTH_SUMS, MONTH, YEAR FROM TRANSACTIONS GROUP BY MONTH, YEAR) AS month_sum_table WHERE TOTALS_PER_MONTH.MONTH =  month_sum_table.MONTH AND  TOTALS_PER_MONTH.YEAR=  month_sum_table.YEAR")
    db.execute("UPDATE TOTALS_PER_MONTH SET TOTAL_INCOME = month_sum_table.MONTH_SUMS FROM (SELECT  SUM(INCOME_AMOUNT) AS MONTH_SUMS, MONTH, YEAR FROM INCOME GROUP BY MONTH, YEAR) AS month_sum_table WHERE TOTALS_PER_MONTH.MONTH =  month_sum_table.MONTH AND TOTALS_PER_MONTH.YEAR = month_sum_table.YEAR")
        # UPDATE TOTALS_PER_MONTH
        # SET TOTAL_EXPENSES/INCOME = month_sum_table.MONTH_SUMS
        # FROM (SELECT  SUM(TRANS/INCOME_AMOUNT) AS MONTH_SUMS, MONTH, YEAR FROM TRANSACTIONS/INCOME  GROUP BY MONTH, YEAR) AS month_sum_table
        # WHERE TOTALS_PER_MONTH.MONTH =  month_sum_table.MONTH AND  TOTALS_PER_MONTH.YEAR=  month_sum_table.YEAR 

    db.commit()

def read_categories():
    db = get_db()

    db.execute("SELECT DISTINCT TRANS_CATEGORY FROM TRANSACTIONS ORDER BY TRANS_CATEGORY")
    categories = [row[0] for row in db.fetchall()]

    return categories



# dashboard
def read_month_totals_for_line_graph(year):
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    total_balances = []
    total_expenses = []
    total_incomes = []

    for month in months:
        total_values, _, _ = check_and_read_month_totals(months.index(month) + 1, year, True)
        total_balances.append(total_values[0])
        total_expenses.append(total_values[1])
        total_incomes.append(total_values[2])

    return total_balances, total_expenses, total_incomes

def read_category_totals_for_pie_graph(month, year):
    db = get_db()

    db.execute("SELECT TRANS_CATEGORY, SUM(TRANS_AMOUNT) AS AMOUNT FROM TRANSACTIONS WHERE MONTH = %s AND YEAR = %s GROUP BY TRANS_CATEGORY", (month_to_int[month], year))
    categories_totals = db.fetchall()
    pie_dict = {}
    for i in range(len(categories_totals)):
        pie_dict[categories_totals[i][0]] = float(categories_totals[i][1])

    return pie_dict




def init_db():
    db = get_db()

    # initialize db schema here

# create command line command: call initialize db and 
@click.command('init-db')
def init_db_command():
    # """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db) # call when cleaning up after returning response
    app.cli.add_command(init_db_command)