import sqlite3
from .db import get_db, write_to_db

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

bp = Blueprint('run_website', __name__)

@bp.route('/')
def index():
    db = get_db()
    res = db.execute("SELECT * FROM TRANSACTIONS ORDER BY TRANS_DATE DESC") # (TRANS_ID, TRANS_AMOUNT, TRANS_CATEGORY, TRANS_DATE, TRANS_MEMO)
    trans_list = res.fetchall()
    
    return render_template("index.html", trans_list=trans_list)


@bp.route('/submit', methods=['POST'])
def submit():
    amount = request.form['amount']
    # category = request.form['category']
    # description = request.form['description']
    if request.form.get("memo"):
        memo = request.form['amount']
    else:
        memo = None
    
    # Process the data (save to the database then print to console)
    #print(f"Received: Amount={amount}, Category={category}, Description={description}")
    
    #return f"Submitted: Amount={amount}, Category={category}, Description={description}"

    write_to_db(amount=amount)
    # write_to_db(amount=amount, date=date, category=category, memo=memo) <-- replace line above with this once all inputs are available
    
    return f"Submitted: Amount={amount}"