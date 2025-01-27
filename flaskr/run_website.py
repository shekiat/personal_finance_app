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
        "chosen_month": session.get("chosen_month", None),
        "chosen_year": session.get("chosen_year", None)
    }
    session.clear()

    # get the totals and transactions for current month
    current_month = datetime.datetime.now().month
    current_year = datetime.datetime.now().year
    trans_list = []

    if session_vars["chosen_month"] is not None:
        parsed_chosen_date = parse_date(session_vars["session_date"])
        chosen_month = parsed_chosen_date.month()
        chosen_year = parsed_chosen_date.year()

        total_values, total_diffs, total_diff_percs = check_and_read_month_totals(chosen_month, chosen_year) # [balance, expenses, income]
        trans_list = read_transactions(chosen_month, chosen_year)
    else:
        total_values, total_diffs, total_diff_percs = check_and_read_month_totals(current_month, current_year)
        trans_list = read_transactions(current_month, current_year)
    
    # format differences for presentation
    for i in range(3):
        if total_diffs[i] < 0:
            total_diffs[i] = "- $" + str(total_diffs[i])[1:]
        elif total_diffs[i] > 0:
            total_diffs[i] = "$" + str(total_diffs[i])
        
    return render_template("index.html", trans_list=trans_list, session_vars=session_vars, total_values=total_values, total_diffs=total_diffs, total_diff_percs=total_diff_percs)
    
    
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

    parsed_date_full = parse_date(date) # format date for comparison, to add to db
    parsed_date = parsed_date_full.date()


    if str(datetime.datetime.strptime(str(parsed_date), '%Y-%m-%d')) <= datetime.datetime.now(timezone.utc).strftime('%Y-%m-%d'):
        write_transaction(user="Jim Gorden", amount=amount, category=category, date=parsed_date, memo=memo)
        update_totals(parsed_date_full.month, parsed_date_full.year, amount)
    else:
        # if the date is in the future, notify user, add info to session so it stays in the input boxes
        session['submit_successful'] = False
        session['amount'] = amount
        session['category'] = category
        session['date'] = date
        if memo:
            session['memo'] = memo
    
    return redirect(url_for("run_website.index"))