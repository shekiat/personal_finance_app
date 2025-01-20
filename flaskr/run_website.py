import sqlite3
from .db import get_db

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

bp = Blueprint('run_website', __name__)

@bp.route('/')
def index():
    db = get_db()
    res = db.execute("SELECT * FROM TRANSACTIONS")
    trans_list = res.fetchall()
    
    # return trans_list
    return render_template("index.html", trans_list=trans_list)


@bp.route('/submit', methods=['POST'])
def submit():
    amount = request.form['amount']
    # category = request.form['category']
    # description = request.form['description']
    
    # Process the data (save to the database then print to console)
    #print(f"Received: Amount={amount}, Category={category}, Description={description}")
    
    #return f"Submitted: Amount={amount}, Category={category}, Description={description}"

    db = get_db()

    db.execute(f"INSERT INTO TRANSACTIONS VALUES(4, {amount}, 'BILLS', '01-24-2025', 'TEST')")
    db.commit()
    
    return f"Submitted: Amount={amount}"