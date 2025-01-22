import sqlite3
from .db import get_db, write_to_db, parse_date
import datetime
from datetime import timezone

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

bp = Blueprint('run_website', __name__)

@bp.route('/')
def index():
    # if called through "/submit", get whether the submit was successful
    session_vars = {
        "submit_successful": session.get("submit_successful", True),
        "session_amount": session.get("amount", None),
        "session_date": session.get("date", None),
        "session_category": session.get("category", None),
        "session_memo": session.get("memo", '')
    }
    session.clear()

    db = get_db()
    res = db.execute("SELECT * FROM TRANSACTIONS ORDER BY TRANS_DATE DESC") # (TRANS_ID, TRANS_AMOUNT, TRANS_CATEGORY, TRANS_DATE, TRANS_MEMO)
    trans_list = res.fetchall()
    
    return render_template("index.html", trans_list=trans_list, session_vars=session_vars)
    
    


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

    parsed_date = parse_date(date).date() # format date for comparison and to add to db

    if str(datetime.datetime.strptime(str(parsed_date), '%Y-%m-%d')) <= datetime.datetime.now(timezone.utc).strftime('%Y-%m-%d'):
        write_to_db(amount=amount, category=category, date=parsed_date, memo=memo)
    else:
        # if the date is in the future, notify user, add info to session so it stays in the input boxes
        session['submit_successful'] = False
        session['amount'] = amount
        session['category'] = category
        session['date'] = date
        if memo:
            session['memo'] = memo
    
    return redirect(url_for("run_website.index"))