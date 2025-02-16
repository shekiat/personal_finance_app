import sqlite3
from .db import *
import datetime
from datetime import timezone

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
import pytz
EST = pytz.timezone("US/Eastern")

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
    # once information appearing in totals is implemented, may have to change session vars logic

    # if called through "/submit", get whether the submit was successful; if called through "/month-change", get the month and year
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
    session.clear()

    # get the totals and transactions for current month
    trans_list = []

    chosen_month = session_vars['chosen_month']
    chosen_year = session_vars['chosen_year']

    total_values, total_diffs, total_diff_percs = check_and_read_month_totals(chosen_month, chosen_year, False) # [balance, expenses, income]
    trans_list = read_transactions(chosen_month, chosen_year)
    income_list = read_income(chosen_month, chosen_year)
    
    # format differences for presentation
    for i in range(3):
        if total_diffs[i] < 0:
            total_diffs[i] = "- $" + str(total_diffs[i])[1:]
        elif total_diffs[i] > 0:
            total_diffs[i] = "$" + str(total_diffs[i])

    # get categories for drop down
    category_list = read_categories()

    # year list for drop down
    year_list = []
    for year in range (datetime.datetime.now(tz=EST).year - 10, datetime.datetime.now(tz=EST).year - 2):
        year_list.append(year)

    # month converted to string
    if isinstance(session_vars["chosen_month"], int):
        chosen_month_string = int_to_month[session_vars["chosen_month"]]
        
    return render_template("home.html", trans_list=trans_list, income_list=income_list, session_vars=session_vars, total_values=total_values, total_diffs=total_diffs, total_diff_percs=total_diff_percs, category_list=category_list, year_list=year_list, current_year = datetime.datetime.now(tz=EST).year, chosen_month_string=chosen_month_string)
    
    
@bp.route('/submit-transaction', methods=['POST'])
def submit():
    amount = request.form['amount']
    category = request.form['hidden-category']
    date = request.form['date']
    if request.form.get('memo'):
        memo = request.form['memo']
    else:
        memo = None 

    session['chosen_month'] = int(request.form['month'])
    session['chosen_year'] = int(request.form['year'])

    parsed_date_full = parse_date(date) # format date for comparison, to add to db
    parsed_date = parsed_date_full.date()

    current_date = datetime.datetime.strptime(str(parsed_date), '%Y-%m-%d')

    try:
        float(amount)

        if EST.localize(current_date) <= datetime.datetime.now(tz=EST):
            write_transaction(user="Jim Gorden", amount=amount, category=category.lower(), date=parsed_date, memo=memo)
            update_totals(parsed_date_full.month, parsed_date_full.year)
            session['submit_successful'] = True
        else:
            # if the date is in the future, notify user, add info to session so it stays in the input boxes
            session['submit_successful'] = False
            session['unsuccessful_reason'] = "date"
            session['amount'] = amount
            session['category'] = category
            session['date'] = date
            if memo:
                session['memo'] = memo       
    except ValueError:
        session['submit_successful'] = False
        session['amount'] = amount
        session['category'] = category
        session['date'] = date
        if memo:
            session['memo'] = memo   
        session['unsuccessful_reason'] = "amount"
    
    session['expense_income'] = 0

    return redirect(url_for("home.home"))


@bp.route('/submit-income', methods=['POST'])
def submit_inc():
    amount = request.form['amount']
    date = request.form['date']
    if request.form.get('memo'):
        memo = request.form['memo']
    else:
        memo = None 

    session['chosen_month'] = int(request.form['month'])
    session['chosen_year'] = int(request.form['year'])

    parsed_date_full = parse_date(date) # format date for comparison, to add to db
    parsed_date = parsed_date_full.date()

    current_date = datetime.datetime.strptime(str(parsed_date), '%Y-%m-%d')

    try:
        float(amount)
        if EST.localize(current_date) <= datetime.datetime.now(tz=EST):
            write_income(user="Jim Gorden", amount=amount, date=parsed_date, memo=memo)
            update_totals(parsed_date_full.month, parsed_date_full.year)
            session['submit_successful'] = True
        else:
            # if the date is in the future, notify user, add info to session so it stays in the input boxes
            session['submit_successful'] = False
            session['amount'] = amount
            session['date'] = date
            if memo:
                session['memo'] = memo

            session["unsuccessful_reason"] = "date"
    except ValueError:
        session['submit_successful'] = False
        session['amount'] = amount
        session['date'] = date
        if memo:
            session['memo'] = memo

        session['unsuccessful_reason'] = "amount"

    session['expense_income'] = 1
    
    return redirect(url_for("home.home"))


@bp.route('/submit-date', methods=['POST'])
def month_change():
    month = request.form["month"]
    year = request.form["year"]
    session['expense_income'] = request.form['expense_income']

    month_number = datetime.datetime.strptime(month, "%B").month

    session['chosen_month'] = int(month_number)
    session['chosen_year'] = int(year)

    return redirect(url_for("home.home"))


@bp.route('/delete-transaction', methods=['POST'])
def delete():
    transaction_id = request.form['transaction_id']
    session['chosen_month'] = int(request.form['month'])
    session['chosen_year'] = int(request.form['year'])

    delete_transaction(transaction_id)
    update_totals()

    # Feedback that transaction has been deleted?

    return redirect(url_for("home.home"))

@bp.route('/delete-income', methods=['POST'])
def delete_inc():
    income_id = request.form['income_id']
    session['chosen_month'] = int(request.form['month'])
    session['chosen_year'] = int(request.form['year'])

    session['expense_income'] = 1

    delete_income(income_id)
    update_totals()

    # Feedback that transaction has been deleted?

    return redirect(url_for("home.home"))
