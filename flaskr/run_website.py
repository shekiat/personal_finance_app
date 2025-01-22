import sqlite3
from .db import get_db, write_to_db
import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort

bp = Blueprint('run_website', __name__)

@bp.route('/')
def index(trans_submitted=None):
    # if called through "/submit", get whether the submit was successful
    submit_successful = session.get("submit_successful", "True")

    db = get_db()
    res = db.execute("SELECT * FROM TRANSACTIONS ORDER BY TRANS_DATE DESC") # (TRANS_ID, TRANS_AMOUNT, TRANS_CATEGORY, TRANS_DATE, TRANS_MEMO)
    trans_list = res.fetchall()
    
    return render_template("index.html", trans_list=trans_list, submit_successful=submit_successful)
    
    


@bp.route('/submit', methods=['POST'])
def submit():
    amount = request.form['amount']
    category = request.form['category']
    date = request.form['date']
    if request.form.get("memo"):
        memo = request.form['memo']
    else:
        memo = None

    write_to_db(amount=amount, category=category, date=date, memo=memo)

    # if datetime.datetime.strptime(current_date, "%d/%m/%Y").date() <= datetime.datetime.now():
    #     
    # else:
    #     # if the date is in the future, notify user
    #     session['submitted'] = False
    
    # return f"Submitted amount={amount}, category={category}, date={date}"

    return redirect(url_for("run_website.index"))