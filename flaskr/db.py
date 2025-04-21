from flask import current_app, g, session
import sqlite3
import datetime
import click
import os
import dateutil
from dateutil.parser import parse
import psycopg2
import psycopg2.extras


import pytz
EST = pytz.timezone("US/Eastern")



month_to_int = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}


from flask import current_app, g
import sqlite3
import datetime
import click
import os
import boto3
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
        g.db = psycopg2.connect(
            host='moneymatedb.chgss626mp8s.us-east-2.rds.amazonaws.com',
            user='postgres',
            password='D$0?#oh4h.$3D?|L]w6bZ#UICbU1',
            database='MoneyMateDB',
            port='5432'
        )

        # g.db = psycopg2.connect(
        #     host='localhost',
        #     user='nsteiner25',
        #     database='awsBackup',
        #     port='5432'
        # )
        
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
        
def fetch_user_id(user_email):
    db = get_db()
    db_cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    db_cursor.execute("SELECT * FROM USERS WHERE EMAIL = %s", (user_email,))
    user_id_row = db_cursor.fetchall()
    if len(user_id_row) == 0:
        db_cursor.execute("SELECT MAX(USER_ID) FROM USERS")
        user_id = db_cursor.fetchall()[0][0] + 1

        # get user's full name
        cognito_client = boto3.client('cognito-idp', region_name='us-east-2')
        cognito_user = cognito_client.admin_get_user(
            UserPoolId='us-east-2_uiivhIHti',
            Username=user_email
        )
        print('\n')
        print(cognito_user)
        print('\n')
        for attr in cognito_user['UserAttributes']:
           print(attr)
           if attr['Name'] == 'name':
              user_name = attr['Value']

        # insert user into db
        db_cursor.execute("INSERT INTO USERS VALUES (%s, %s, %s)", (user_id[0], user_email, user_name)) # create user in USERS
        db.commit()
    else:
        user_id = user_id_row[0][0]
        user_name = user_id_row[0][2]

    db_cursor.close()

    return user_id, user_name

def fetch_group_id(user_id):
    db = get_db()
    db_cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    db_cursor.execute("SELECT GROUP_ID FROM USER_GROUPS WHERE USER_1_ID = %s OR USER_2_ID = %s OR USER_3_ID = %s OR USER_4_ID = %s OR USER_5_ID = %s", (user_id[0], user_id[0], user_id[0], user_id[0], user_id[0]))
    group_id_row = db_cursor.fetchall()

    if group_id_row != []:
        return group_id_row[0][0]
    else:
        return None
    
def fetch_user_name(user_id):
    db = get_db()
    db_cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    db_cursor.execute("SELECT NAME FROM USERS WHERE USER_ID = %s", (user_id,))
    
    full_name = db_cursor.fetchall()[0][0]
    return full_name


# transactions
def write_transaction(user, amount, date, category, memo, user_id, group_id=-1):
    db = get_db()
    db_cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if group_id == -1:
        db_cursor.execute("SELECT MAX(TRANS_ID) FROM TRANSACTIONS")
    else:
        db_cursor.execute("SELECT MAX(TRANS_ID) FROM GROUP_TRANSACTIONS")
    max_id = db_cursor.fetchone()[0]
    new_id = 0
    if max_id is not None:
        new_id = max_id + 1
    else:
        new_id = 0

    amount = amount 
    
    if str(amount)[0] == '$':
        amount = int(str(amount)[1:])

    if group_id == -1:
        data = (new_id, amount, category.title(), date, memo if memo else '', user_id[0])
        print(user_id)
        db_cursor.execute(f"INSERT INTO TRANSACTIONS (TRANS_ID, TRANS_AMOUNT, TRANS_CATEGORY, TRANS_DATE, TRANS_MEMO, USER_ID) VALUES(%s, %s, %s, %s, %s, %s)", data)
    else:
        data = (new_id, amount, category.title(), date, memo if memo else '', user_id[0], group_id[0])
        print(user_id)
        db_cursor.execute(f"INSERT INTO GROUP_TRANSACTIONS (TRANS_ID, TRANS_AMOUNT, TRANS_CATEGORY, TRANS_DATE, TRANS_MEMO, USER_ID, GROUP_ID) VALUES(%s, %s, %s, %s, %s, %s, %s)", data)

    print(user_id)
    db.commit()
    db_cursor.close()

def read_transactions(month, year, id, user_group=0):
    print(f"id: {id}")
    db = get_db()
    db_cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if user_group == 0:
        db_cursor.execute("SELECT * FROM TRANSACTIONS WHERE MONTH = %s AND YEAR = %s AND USER_ID = %s ORDER BY TRANS_DATE DESC", (month, year, id[0])) # (TRANS_ID, TRANS_AMOUNT, TRANS_CATEGORY, TRANS_DATE, TRANS_MEMO)
    else:
        db_cursor.execute("SELECT * FROM GROUP_TRANSACTIONS WHERE MONTH = %s AND YEAR = %s AND GROUP_ID = %s ORDER BY TRANS_DATE DESC", (month, year, id[0])) # (TRANS_ID, TRANS_AMOUNT, TRANS_CATEGORY, TRANS_DATE, TRANS_MEMO)


    trans_list_res = db_cursor.fetchall()
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
        if user_group == 0:
            full_name = session["full_name"]
        else:
            full_name = fetch_user_name(transaction[8])
        trans_list_element.append(full_name)
        trans_list.append(trans_list_element)

    print(f"trans list from db{trans_list}")
    return trans_list

def delete_transaction(trans_id, user_group=0):
    db = get_db()
    db_cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if user_group == 0:
        db_cursor.execute("DELETE FROM TRANSACTIONS WHERE TRANS_ID = %s", (trans_id,))
    else:
        db_cursor.execute("DELETE FROM GROUP_TRANSACTIONS WHERE TRANS_ID = %s", (trans_id,))

    db.commit()
    db_cursor.close()



# income
def write_income(user, amount, date, memo, user_id, group_id=-1):
    db = get_db()
    db_cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if group_id == -1:
        db_cursor.execute("SELECT MAX(INCOME_ID) FROM INCOME")
    else:
        db_cursor.execute("SELECT MAX(INCOME_ID) FROM GROUP_INCOME")

    max_id = db_cursor.fetchone()[0]
    new_id = 0
    if max_id is not None:
        new_id = max_id + 1
    else:
        new_id = 0

    amount = amount 
    
    if str(amount)[0] == '$':
        amount = int(str(amount)[1:])


    if group_id == -1:
        data = (new_id, amount, date, memo if memo else '', user_id)
        db_cursor.execute(f"INSERT INTO INCOME (INCOME_ID, INCOME_AMOUNT, INCOME_DATE, INCOME_MEMO, USER_ID) VALUES(%s, %s, %s, %s, %s)", data)
    else:
        data = (new_id, amount, date, memo if memo else '', user_id, group_id)
        db_cursor.execute(f"INSERT INTO GROUP_INCOME (INCOME_ID, INCOME_AMOUNT, INCOME_DATE, INCOME_MEMO, USER_ID, GROUP_ID) VALUES(%s, %s, %s, %s, %s, %s)", data)
    db.commit()
    db_cursor.close()

def read_income(month, year, id, user_group=0):
    db = get_db()
    db_cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if user_group == 0:
        db_cursor.execute("SELECT * FROM INCOME WHERE MONTH = %s AND YEAR = %s AND USER_ID = %s ORDER BY INCOME_DATE DESC", (month, year, id[0])) # (INCOME_ID, INCOME_AMOUNT, INCOME_CATEGORY, INCOME_DATE, INCOME_MEMO, MONTH, YEAR)
    else:
        db_cursor.execute("SELECT * FROM GROUP_INCOME WHERE MONTH = %s AND YEAR = %s AND GROUP_ID = %s ORDER BY INCOME_DATE DESC", (month, year, id[0])) # (INCOME_ID, INCOME_AMOUNT, INCOME_CATEGORY, INCOME_DATE, INCOME_MEMO, MONTH, YEAR)

    income_list_res = db_cursor.fetchall()
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
        if user_group == 0:
            full_name = session["full_name"]
        else:
            full_name = fetch_user_name(income[7])
        income_list_element.append(full_name)
        income_list.append(income_list_element)

    return income_list

def delete_income(income_id, user_group=0):
    db = get_db()
    db_cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if user_group == 0:
        db_cursor.execute("DELETE FROM INCOME WHERE INCOME_ID = %s", (income_id[0],))
    else:
        db_cursor.execute("DELETE FROM GROUP_INCOME WHERE INCOME_ID = %s", (income_id[0],))

    db.commit()
    db_cursor.close()



# totals
# once a new month is picked, check if it exists in the TOTALS_PER_MONTH table
# def check_and_read_month_totals(month, year, for_dashboard, user_id):
#     db = get_db()
#     db_cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
#     # get information from current month
#     db_cursor.execute("SELECT TOTAL_BALANCE, TOTAL_EXPENSES, TOTAL_INCOME FROM TOTALS_PER_MONTH WHERE MONTH = %s AND YEAR = %s", (month, year))
#     res_totals = db_cursor.fetchall()

#     total_values = [0, 0, 0]

#     # if month is in db fetch totals, if month is not add a row with totals
#     if len(res_totals) != 0:
#         total_values = res_totals[0]

#     total_values = [round(total, 2) for total in total_values]

#     total_differences = list(total_values)
#     total_differences_percs = list(total_values)
#     past_month_values = [0, 0, 0]

#     if not for_dashboard:
#         # get information from past month
#         db_cursor.execute("SELECT TOTAL_BALANCE, TOTAL_EXPENSES, TOTAL_INCOME FROM TOTALS_PER_MONTH WHERE MONTH = %s AND YEAR = %s", (int(month) - 1 if month != 1 else 12, year if month != 1 else int(year) - 1))
#         res_totals = db_cursor.fetchall()
        
#         # if month is in db fetch diffs
#         if len(res_totals) != 0 and res_totals[0][2] is not None:
#             past_month_values = res_totals[0]
#             total_differences = [round(x - y, 2) for x, y in zip(total_differences, past_month_values)]
#             for i in range(3, user_id):
#                 if past_month_values[i] != 0:
#                     total_differences_percs[i] = round(total_differences_percs[i] / past_month_values[i] * 100 - 100, 2)
#         else:
#             total_differences = [0, 0, 0]

#     return total_values, total_differences, total_differences_percs


# def update_totals(month=None, year=None, user_id):
#     db = get_db()
#     db_cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)

#     if [month, year] != [None, None]: # = [None, None] if we are deleting transaction
#         db_cursor.execute("SELECT * FROM TOTALS_PER_MONTH WHERE MONTH = %s AND YEAR = %s", (month, year))
#         if len(db_cursor.fetchall()) == 0: 
#             db_cursor.execute("INSERT INTO TOTALS_PER_MONTH VALUES(%s, %s, 0, 0)", (month, year))

#     db_cursor.execute("UPDATE TOTALS_PER_MONTH SET TOTAL_EXPENSES = month_sum_table.MONTH_SUMS FROM (SELECT  SUM(TRANS_AMOUNT) AS MONTH_SUMS, MONTH, YEAR FROM TRANSACTIONS GROUP BY MONTH, YEAR) AS month_sum_table WHERE TOTALS_PER_MONTH.MONTH =  month_sum_table.MONTH AND  TOTALS_PER_MONTH.YEAR=  month_sum_table.YEAR")
#     db_cursor.execute("UPDATE TOTALS_PER_MONTH SET TOTAL_INCOME = month_sum_table.MONTH_SUMS FROM (SELECT  SUM(INCOME_AMOUNT) AS MONTH_SUMS, MONTH, YEAR FROM INCOME GROUP BY MONTH, YEAR) AS month_sum_table WHERE TOTALS_PER_MONTH.MONTH =  month_sum_table.MONTH AND TOTALS_PER_MONTH.YEAR = month_sum_table.YEAR")
#         # UPDATE TOTALS_PER_MONTH
#         # SET TOTAL_EXPENSES/INCOME = month_sum_table.MONTH_SUMS
#         # FROM (SELECT  SUM(TRANS/INCOME_AMOUNT) AS MONTH_SUMS, MONTH, YEAR FROM TRANSACTIONS/INCOME  GROUP BY MONTH, YEAR) AS month_sum_table
#         # WHERE TOTALS_PER_MONTH.MONTH =  month_sum_table.MONTH AND  TOTALS_PER_MONTH.YEAR=  month_sum_table.YEAR 

#     db.commit()
#     db_cursor.close()

def read_month_totals(month, year, id, user_group=0):
    print(month, year)
    db = get_db()
    db_cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if user_group == 0:
        db_cursor.execute("SELECT SUM(TRANS_AMOUNT) FROM TRANSACTIONS WHERE MONTH = %s AND YEAR = %s AND USER_ID = %s", (month, year, id))
    else:
        db_cursor.execute("SELECT SUM(TRANS_AMOUNT) FROM GROUP_TRANSACTIONS WHERE MONTH = %s AND YEAR = %s AND GROUP_ID = %s", (month, year, id))

    expense_row = db_cursor.fetchone()[0]
    if expense_row != None:
        expense_total = float(expense_row)
    else: 
        expense_total = 0

    if id == 0:
        db_cursor.execute("SELECT SUM(INCOME_AMOUNT) FROM INCOME WHERE MONTH = %s AND YEAR = %s AND USER_ID = %s", (month, year, id))
    else:
        db_cursor.execute("SELECT SUM(INCOME_AMOUNT) FROM GROUP_INCOME WHERE MONTH = %s AND YEAR = %s AND GROUP_ID = %s", (month, year, id))

    income_row = db_cursor.fetchone()[0]
    if  income_row != None:
        income_total = float(income_row)
    else: 
        income_total = 0

    balance_total = round(income_total - expense_total, 2)

    return balance_total, expense_total, income_total



# categories 
def read_categories(id, user_group=0):
    db = get_db()
    db_cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if user_group == 0:
        db_cursor.execute("SELECT DISTINCT TRANS_CATEGORY FROM TRANSACTIONS WHERE USER_ID = %s ORDER BY TRANS_CATEGORY", (id,))
    else:
        db_cursor.execute("SELECT DISTINCT TRANS_CATEGORY FROM GROUP_TRANSACTIONS WHERE GROUP_ID = %s ORDER BY TRANS_CATEGORY", (id,))

    categories = [row[0] for row in db_cursor.fetchall()]

    return categories



# dashboard
def read_month_totals_for_line_graph(year, user_id):
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

    total_balances = []
    total_expenses = []
    total_incomes = []

    for month in months:
        total_values = read_month_totals(months.index(month) + 1, year, user_id)
        total_balances.append(total_values[0])
        total_expenses.append(total_values[1])
        total_incomes.append(total_values[2])

    return total_balances, total_expenses, total_incomes

def read_category_totals_for_pie_graph(month, year, user_id):
    db = get_db()
    db_cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)

    db_cursor.execute("SELECT TRANS_CATEGORY, SUM(TRANS_AMOUNT) AS AMOUNT FROM TRANSACTIONS WHERE MONTH = %s AND YEAR = %s AND USER_ID = %s GROUP BY TRANS_CATEGORY", (month_to_int[month], year, user_id))
    categories_totals = db_cursor.fetchall()
    pie_dict = {}
    for i in range(len(categories_totals)):
        pie_dict[categories_totals[i][0]] = float(categories_totals[i][1])

    return pie_dict



# group budget function
def add_user_to_group(creator_id, new_user_email):
    db = get_db()
    db_cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    print(f"new user email: {new_user_email}")
    new_user_id, _ = fetch_user_id(new_user_email)
    print(f"new user id: {new_user_id}")

    db_cursor.execute("SELECT * FROM USER_GROUPS WHERE USER_1_ID = %s  OR USER_2_ID = %s OR USER_3_ID = %s OR USER_4_ID = %s OR USER_5_ID = %s", (creator_id, creator_id, creator_id, creator_id, creator_id))
    group_id_row = db_cursor.fetchall()
    if len(group_id_row) == 0:
        db_cursor.execute("SELECT MAX(group_ID) FROM USER_GROUPS")
        groud_id_row = db_cursor.fetchall()[0][0]
        if group_id_row != []:
            group_id = group_id_row + 1
        else:
            group_id = 1
        db_cursor.execute("INSERT INTO USER_GROUPS VALUES (%s, %s, %s, 0, 0, 0)", (group_id, creator_id, new_user_id))
        print("budget created, user invited")
        db.commit()
        return 1 # 1 = budget created, user added
    else:
        group_id = group_id_row[0][0]
        for i in range(2, 6):
            if group_id_row[0][i] == 0:
                new_user_number = f"USER_{i}_ID"
                print(new_user_number)
                db_cursor.execute(f"UPDATE USER_GROUPS SET {new_user_number} = %s WHERE GROUP_ID = %s", (new_user_id, group_id))
                print("user invited to budget")
                db.commit()
                return 2 # 2 = successfully added
            elif group_id_row[0][i] == new_user_id:
                return 0 # 0 = user already in DB
    
    




def init_db():
    db = get_db()
    db_cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)

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

# group chat functions
def insert_group_message(group_id, user_id, message):
    """Insert a new message into the GROUP_CHAT table."""
    db = get_db()
    db_cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    # Get the current time in UTC
    utc_now = datetime.datetime.now(tz=pytz.UTC)

    
    db_cursor.execute(
        "INSERT INTO GROUP_CHAT (group_id, user_id, message) VALUES (%s, %s, %s)",
        (group_id, user_id, message)
    )
    db.commit()
    db_cursor.close()


def fetch_group_messages(group_id, limit=500):
    """Fetch the latest messages for a group."""
    db = get_db()
    db_cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    db_cursor.execute("SELECT u.name, gc.message, gc.timestamp FROM GROUP_CHAT gc JOIN USERS u ON gc.user_id = u.user_id WHERE gc.group_id = %s ORDER BY gc.timestamp LIMIT %s", (group_id, limit))
    messages = db_cursor.fetchall()
    db_cursor.close()
    return messages