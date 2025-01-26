import sqlite3
from .db import *
import datetime
from datetime import timezone

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

bp = Blueprint('run_website', __name__)

@bp.route('/')
def index():
    # once information appearing in totals is implemented, may have to change session vars logic

    # if called through "/submit", get whether the submit was successful; if called through "/month-change", get the month and year
    session_vars = {
        # for transactions
        "submit_successful": session.get("submit_successful", True),
        "session_amount": session.get("amount", None),
        "session_date": session.get("date", None),
        "session_category": session.get("category", None),
        "session_memo": session.get("memo", ''),

        # for totals
        "current_month": session.get("current_month", None),
        "current_year": session.get("current_year", None)
    }
    session.clear()

    # get the transactions for current month
    # trans_list = read_transactions(month, year)
    
    trans_list = read_transactions()

    # get the total for current month
    total_balance, total_expenses, total_income = (0, 0, 0)
    if session_vars["current_month"] is not None:
        total_balance, total_expenses, total_income = check_and_read_month_totals(parse_date(session_vars["session_vars"], session_vars["session_vars"]))
    else:
        total_balance, total_expenses, total_income = check_and_read_month_totals(datetime.datetime.now().month, datetime.datetime.now().year)
    totals = [total_balance, total_expenses, total_income]

    return render_template("index.html", trans_list=trans_list, session_vars=session_vars, totals=totals)
    
    
@bp.route('/submit', methods=['POST'])
def submit():
    amount = request.form['amount']
    category = request.form['category']
    date = request.form['date']
    if request.form.get('memo'):
        memo = request.form['memo']
    else:
        memo = None 

    # write_to_db(amount=amount, category=category, date=date, memo=memo)
    # return f"Submitted amount={amount}, category={category}, date={date}"

    parsed_date = parse_date(date).date() # format date for comparison, to add to db

    if str(datetime.datetime.strptime(str(parsed_date), '%Y-%m-%d')) <= datetime.datetime.now(timezone.utc).strftime('%Y-%m-%d'):
        write_transaction(amount=amount, category=category, date=parsed_date, memo=memo)
    else:
        # if the date is in the future, notify user, add info to session so it stays in the input boxes
        session['submit_successful'] = False
        session['amount'] = amount
        session['category'] = category
        session['date'] = date
        if memo:
            session['memo'] = memo
    
    return redirect(url_for("run_website.index"))