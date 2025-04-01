# import sqlite3
# from .db import *
# import datetime
# from datetime import timezone

# from flask import (
#     Blueprint, flash, g, redirect, render_template, request, url_for, session
# )
# from werkzeug.exceptions import abort
# import pytz
# EST = pytz.timezone("US/Eastern")
# import math

# bp = Blueprint('home', __name__)

# int_to_month = {
#     1 : "January",
#     2 : "February",
#     3 : "March",
#     4 : "April",
#     5 : "May",
#     6 : "June",
#     7 : "July",
#     8 : "August",
#     9 : "September",
#     10 : "October",
#     11 : "November",
#     12 : "December"
# }

# @bp.route('/')
# def home():
#     if "user" not in session:
#         return redirect("/cognito-login")
#     else:
#         print(f"user{session['user']}")
#         user_session = session["user"]
#         state_session = session['state']
#         user_id = session["user_id"]

#     # if called through "/submit", get whether the submit was successful; if called through "/month-change", get the month and year
#     session_vars = {
#         # for transactions
#         "submit_successful": session.get("submit_successful", None),
#         "unsuccessful_reason": session.get("unsuccessful_reason", -1),
#         "session_amount": session.get("amount", None),
#         "session_date": session.get("date", None),
#         "session_category": session.get("category", None),
#         "session_memo": session.get("memo", ''),
#         "expense_income": session.get("expense_income", 0),

#         # for totals
#         "chosen_month": session.get("chosen_month", datetime.datetime.now(tz=EST).month),
#         "chosen_year": session.get("chosen_year", datetime.datetime.now(tz=EST).year)
#     }

#     # re-input user info to session
#     session["user"] = user_session
#     session['state'] = state_session
#     session["user_id"] = user_id

#     # get the totals and transactions for current month
#     trans_list = []

#     chosen_month = session_vars['chosen_month']
#     chosen_year = session_vars['chosen_year']

#     # total_values, total_diffs, total_diff_percs = check_and_read_month_totals(chosen_month, chosen_year, False) # [balance, expenses, income]
    
#     # total values current month = check_and_read(this month, year)
#     # total values past month = check_and_read(this month - 1, year - 1)
#     # calculate diffs and diff percs here

#     # fetch current and past month totals
#     total_values = read_month_totals(chosen_month, chosen_year, session["user_id"])
#     past_month_total_values = read_month_totals(chosen_month - 1, chosen_year - 1, session["user_id"])
#     # calculate differences, percent differences
#     total_diffs = [0, 0, 0]
#     total_diff_percs = [0, 0, 0]
#     if past_month_total_values != (0, 0, 0):
#         total_diffs = [round(x - y, 2) for x, y in zip(total_values, past_month_total_values)]
#         for i in range(3):
#             if past_month_total_values[i] != 0:
#                 total_diff_percs[i] = round(total_values[i] / past_month_total_values[i] * 100 - 100, 2)

#     print(f"user id on home page: {session['user_id']}")
#     trans_list = read_transactions(chosen_month, chosen_year, session["user_id"])
#     income_list = read_income(chosen_month, chosen_year, session["user_id"])
    
#     # format differences for presentation
#     for i in range(3):
#         if total_diffs[i] < 0:
#             total_diffs[i] = "-$" + str(int(total_diffs[i]))[1:]
#         elif total_diffs[i] > 0:
#             total_diffs[i] = "+$" + str(total_diffs[i])

#     # get categories for drop down
#     category_list = read_categories(session["user_id"])

#     # year list for drop down
#     year_list = []
#     for year in range (datetime.datetime.now(tz=EST).year - 10, datetime.datetime.now(tz=EST).year - 2):
#         year_list.append(year)

#     # month converted to string
#     if isinstance(session_vars["chosen_month"], int):
#         chosen_month_string = int_to_month[session_vars["chosen_month"]]
        
#     return render_template("home.html", trans_list=trans_list, income_list=income_list, session_vars=session_vars, total_values=total_values, total_diffs=total_diffs, total_diff_percs=total_diff_percs, category_list=category_list, year_list=year_list, current_year = datetime.datetime.now(tz=EST).year, chosen_month_string=chosen_month_string)
    
# @bp.route('/submit-transaction', methods=['POST'])
# def submit():
#     amount = request.form['amount']
#     category = request.form['hidden-category']
#     date = request.form['date']
#     if request.form.get('memo'):
#         memo = request.form['memo']
#     else:
#         memo = None 

#     session['chosen_month'] = int(request.form['month'])
#     session['chosen_year'] = int(request.form['year'])

#     parsed_date_full = parse_date(date) # format date for comparison, to add to db
#     parsed_date = parsed_date_full.date()

#     current_date = datetime.datetime.strptime(str(parsed_date), '%Y-%m-%d')

#     try:
#         float(amount)

#         if EST.localize(current_date) <= datetime.datetime.now(tz=EST):
#             write_transaction(user="Jim Gorden", amount=amount, category=category.lower(), date=parsed_date, memo=memo, user_id=session["user_id"])
#             session['submit_successful'] = True
#         else:
#             # if the date is in the future, notify user, add info to session so it stays in the input boxes
#             session['submit_successful'] = False
#             session['unsuccessful_reason'] = "date"
#             session['amount'] = amount
#             session['category'] = category
#             session['date'] = date
#             if memo:
#                 session['memo'] = memo       
#     except ValueError:
#         session['submit_successful'] = False
#         session['amount'] = amount
#         session['category'] = category
#         session['date'] = date
#         if memo:
#             session['memo'] = memo   
#         session['unsuccessful_reason'] = "amount"
    
#     session['expense_income'] = 0

#     return redirect(url_for("home.home"))


# @bp.route('/submit-income', methods=['POST'])
# def submit_inc():
#     amount = request.form['amount']
#     date = request.form['date']
#     if request.form.get('memo'):
#         memo = request.form['memo']
#     else:
#         memo = None 

#     session['chosen_month'] = int(request.form['month'])
#     session['chosen_year'] = int(request.form['year'])

#     parsed_date_full = parse_date(date) # format date for comparison, to add to db
#     parsed_date = parsed_date_full.date()

#     current_date = datetime.datetime.strptime(str(parsed_date), '%Y-%m-%d')

#     try:
#         float(amount)
#         if EST.localize(current_date) <= datetime.datetime.now(tz=EST):
#             write_income(user="Jim Gorden", amount=amount, date=parsed_date, memo=memo, user_id=session["user_id"])
#             session['submit_successful'] = True
#         else:
#             # if the date is in the future, notify user, add info to session so it stays in the input boxes
#             session['submit_successful'] = False
#             session['amount'] = amount
#             session['date'] = date
#             if memo:
#                 session['memo'] = memo

#             session["unsuccessful_reason"] = "date"
#     except ValueError:
#         session['submit_successful'] = False
#         session['amount'] = amount
#         session['date'] = date
#         if memo:
#             session['memo'] = memo

#         session['unsuccessful_reason'] = "amount"

#     session['expense_income'] = 1
    
#     return redirect(url_for("home.home"))


# @bp.route('/submit-date', methods=['POST'])
# def month_change():
#     month = request.form["month"]
#     year = request.form["year"]
#     session['expense_income'] = request.form['expense_income']

#     month_number = datetime.datetime.strptime(month, "%B").month

#     session['chosen_month'] = int(month_number)
#     session['chosen_year'] = int(year)

#     return redirect(url_for("home.home"))


# @bp.route('/delete-transaction', methods=['POST'])
# def delete():
#     transaction_id = request.form['transaction_id']
#     session['chosen_month'] = int(request.form['month'])
#     session['chosen_year'] = int(request.form['year'])

#     delete_transaction(transaction_id, session["user_id"])

#     # Feedback that transaction has been deleted?

#     return redirect(url_for("home.home"))

# @bp.route('/delete-income', methods=['POST'])
# def delete_inc():
#     income_id = request.form['income_id']
#     session['chosen_month'] = int(request.form['month'])
#     session['chosen_year'] = int(request.form['year'])

#     session['expense_income'] = 1

#     delete_income(income_id, session["user_id"])

#     # Feedback that transaction has been deleted?

#     return redirect(url_for("home.home"))




#################################################






import sqlite3
from .db import *
import datetime
from datetime import timezone

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session, jsonify
)
from werkzeug.exceptions import abort
import pytz
EST = pytz.timezone("US/Eastern")
import math

bp = Blueprint('home', __name__)

int_to_month = {
    1 : "January",
    2 : "February",
    3 : "March",
    4 : "April",
    5 : "May",
    6 : "June",
    7 : "July",
    8 : "August",
    9 : "September",
    10 : "October",
    11 : "November",
    12 : "December"
}

@bp.route('/')
def home():
    if "user" not in session:
        return redirect("/cognito-login")
    
    session_vars = {
        # for transactions
        "submit_successful": session.get("submit_successful", None),
        "unsuccessful_reason": session.get("unsuccessful_reason", -1),
        "session_amount": session.get("amount", None),
        "session_date": session.get("date", None),
        "session_category": session.get("category", None),
        "session_memo": session.get("memo", ''),
        "expense_income": session.get("expense_income", 0),

        # for totals
        "chosen_month": session.get("chosen_month", datetime.datetime.now(tz=EST).month),
        "chosen_year": session.get("chosen_year", datetime.datetime.now(tz=EST).year)
    }

    # get the totals and transactions for current month
    trans_list = []
    session['current_month'] = datetime.datetime.now().month
    session['current_year'] = datetime.datetime.now().year

    # fetch current and past month totals
    total_values = read_month_totals(session['current_month'], session['current_year'], session["user_id"])
    past_month_total_values = read_month_totals(session['current_month'] - 1, session['current_year'] - 1, session["user_id"])
    # calculate differences, percent differences
    total_diffs = [0, 0, 0]
    total_diff_percs = [0, 0, 0]
    if past_month_total_values != (0, 0, 0):
        total_diffs = [round(x - y, 2) for x, y in zip(total_values, past_month_total_values)]
        for i in range(3):
            if past_month_total_values[i] != 0:
                total_diff_percs[i] = round(total_values[i] / past_month_total_values[i] * 100 - 100, 2)

    print(f"user id on home page: {session['user_id']}")
    trans_list = read_transactions(session['current_month'], session['current_year'], session["user_id"])
    income_list = read_income(session['current_month'], session['current_year'], session["user_id"])
    
    # format differences for presentation, JS SCRIPT
    for i in range(3):
        if total_diffs[i] < 0:
            total_diffs[i] = "-$" + str(int(total_diffs[i]))[1:]
        elif total_diffs[i] > 0:
            total_diffs[i] = "+$" + str(total_diffs[i])

    # get categories for drop down
    category_list = read_categories(session["user_id"])

    # year list for drop down
    year_list = []
    for year in range (datetime.datetime.now(tz=EST).year - 10, datetime.datetime.now(tz=EST).year - 2):
        year_list.append(year)
    session["year_list"] = year_list

    # month converted to string
    if isinstance(session['current_month'], int):
        current_month_string = int_to_month[session['current_month']]
        
    return render_template("home.html", session_vars=session_vars, trans_list=trans_list, income_list=income_list, total_values=total_values, total_diffs=total_diffs, total_diff_percs=total_diff_percs, category_list=category_list, year_list=year_list, current_year = session['current_year'], current_month=session["current_month"], current_month_string=current_month_string)
    
@bp.route('/api/submit-transaction', methods=['POST'])
def submit():
    data = request.json
    amount = data.get('amount')
    category = data.get('category')
    date = data.get('date')
    memo = data.get('memo', '')
    print(f"amount: {amount}")
    print(f"category: {category}")
    print(f"date: {date}")
    print(f"memo: {memo}")

    # NOT NEEDED?
    # session['chosen_month'] = int(request.form['month'])
    # session['chosen_year'] = int(request.form['year'])

    parsed_date_full = parse_date(date) # format date for comparison, to add to db
    parsed_date = parsed_date_full.date()

    current_date = datetime.datetime.strptime(str(parsed_date), '%Y-%m-%d') # formatted for comparison vs current date

    return_value = 0 # 0 = success, 1 = date is in the future, 2 = amount is not a valid number

    try:
        float(amount)
        print(f"input date: {current_date}")
        print(f"current date: {datetime.datetime.now(tz=EST)}")
        if EST.localize(current_date) <= datetime.datetime.now(tz=EST):
            write_transaction(user="Jim Gorden", amount=amount, category=category.lower(), date=parsed_date, memo=memo, user_id=session["user_id"])
        else:
            return_value = 1      
            return jsonify({"return_value" : return_value, 'success' : False, 'amount': amount, 'date': date, 'category': category, 'memo': memo})
    except ValueError:
        return_value = 2
        return jsonify({"return_value" : return_value, 'success' : False, 'amount': amount, 'date': date, 'category': category, 'memo': memo})

    trans_list = read_transactions(session['current_month'], session['current_year'], session["user_id"])
    income_list = read_income(session['current_month'], session['current_year'], session["user_id"])
    
    

    # try:
    #     float(amount)

    #     if EST.localize(current_date) <= datetime.datetime.now(tz=EST):
    #         write_transaction(user="Jim Gorden", amount=amount, category=category.lower(), date=parsed_date, memo=memo, user_id=session["user_id"])
    #         session['submit_successful'] = True
    #     else:
    #         # if the date is in the future, notify user, add info to session so it stays in the input boxes
    #         session['submit_successful'] = False
    #         session['unsuccessful_reason'] = "date"
    #         session['amount'] = amount
    #         session['category'] = category
    #         session['date'] = date
    #         if memo:
    #             session['memo'] = memo       
    # except ValueError:
    #     session['submit_successful'] = False
    #     session['amount'] = amount
    #     session['category'] = category
    #     session['date'] = date
    #     if memo:
    #         session['memo'] = memo   
    #     session['unsuccessful_reason'] = "amount"
    
    # session['expense_income'] = 0

    return jsonify({"return_value" : return_value, 'success' : True})


@bp.route('/api/submit-income', methods=['POST'])
def submit_inc():
    amount = request.form.get('amount')
    date = request.form.get('date')
    memo = request.form.get('memo', '')

    parsed_date_full = parse_date(date) # format date for comparison, to add to db
    parsed_date = parsed_date_full.date()

    current_date = datetime.datetime.strptime(str(parsed_date), '%Y-%m-%d')

    return_value = 0 # 0 = success, 1 = amount not valid, 2 = date is in the future

    try:
        float(amount)
        if EST.localize(current_date) <= datetime.datetime.now(tz=EST):
            write_income(user="Jim Gorden", amount=amount, date=parsed_date, memo=memo, user_id=session["user_id"])
        else:
            return_value = 2
    except ValueError:
        return_value = 1
    
    return jsonify({"return_value" : return_value})


@bp.route('/api/submit-date', methods=['POST'])
def month_change():
    data = request.json
    month = data.get('month')
    year = data.get('year')
    print(f"submitted month: {month}")

    month_number = datetime.datetime.strptime(month, "%B").month

    session['current_month'] = int(month_number)
    session['current_year'] = int(year)

    return jsonify({"chosen_month" : month_number, "chosen_year" : year})


@bp.route('/api/delete-transaction', methods=['POST'])
def delete():
    data = request.json
    transaction_id = data.get('transaction_id')

    # REMOVE?
    # session['chosen_month'] = int(data.get('month'))
    # session['chosen_year'] = int(data.get('year'))

    delete_transaction(transaction_id, session["user_id"])

    return jsonify({'success' : True})

@bp.route('/api/delete-income', methods=['POST'])
def delete_inc():
    data = request.json
    income_id = data.get('income_id')
    
    # REMOVE?
    # session['chosen_month'] = int(request.form['month'])
    # session['chosen_year'] = int(request.form['year'])

    delete_income(income_id, session["user_id"])

    # Feedback that transaction has been deleted?

@bp.route("/api/update-stats", methods=["POST"])
def update_stats_and_totals():
    # fetch current and past month totals
    total_values = read_month_totals(session['current_month'], session['current_year'], session["user_id"])
    past_month_total_values = read_month_totals(session['current_month'] - 1, session['current_year'] - 1, session["user_id"])
    # calculate differences, percent differences
    total_diffs = [0, 0, 0]
    total_diff_percs = [0, 0, 0]
    if past_month_total_values != (0, 0, 0):
        total_diffs = [round(x - y, 2) for x, y in zip(total_values, past_month_total_values)]
        for i in range(3):
            if past_month_total_values[i] != 0:
                total_diff_percs[i] = round(total_values[i] / past_month_total_values[i] * 100 - 100, 2)

    for i in range(3):
        if total_diffs[i] < 0:
            total_diffs[i] = "-$" + str(int(total_diffs[i]))[1:]
        elif total_diffs[i] > 0:
            total_diffs[i] = "+$" + str(total_diffs[i])
    print(f'total_values: {total_values}')
    return jsonify({
        "total_values": total_values,
        "total_diffs": total_diffs,
        "total_diff_percs": total_diff_percs
    })

@bp.route("/api/update-transaction-table")
def update_transaction_table():
    print(f"updating transaction")
    trans_list = read_transactions(session["current_month"], session["current_year"])
    return trans_list

@bp.route("/api/update-income-table")
def update_income_table():
    income_list = read_income(session["current_month"], session["current_year"])
    return income_list