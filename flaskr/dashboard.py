import sqlite3
from .db import *
import datetime
from datetime import timezone

from flask import (
    Blueprint, jsonify, render_template, request, url_for, session
)
import pytz

EST = pytz.timezone("US/Eastern")

bp = Blueprint('dashboard', __name__)

@bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    total_incomes, total_expenses, total_balances = read_for_line_graph("January", "December")

    print(total_incomes)
    print(total_balances)
    print(total_expenses)

    pie_labels = ["Income", "Expenses", "Savings", "Investments"]
    pie_data = [25, 25, 25, 25]

    if request.method == "POST":
        selected_month = request.form["month"]
        session['selected_month'] = selected_month
        # Update data based on the selected month
        # query the database to get the data for the selected month
        # Using temporary dummy data for now
        pie_data = [30, 20, 25, 25]
    else:
        selected_month = session.get('selected_month', None)
 

    # Return the components to the HTML template 
    return render_template(
        "dashboard.html",
        total_incomes=total_incomes,
        total_expenses=total_expenses,
        total_balances=total_balances,
        line_labels=months,
        pie_data=pie_data,
        pie_labels=pie_labels,
        selected_month=selected_month,
        months=months
    )

# @bp.route('/api/dashboard_data')
# def dashboard_data():
#     months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
#     total_incomes, total_expenses, total_balances = read_for_line_graph("January", "December")

#     pie_labels = ["Income", "Expenses", "Savings", "Investments"]
 
#     pie_data = [25, 25, 25, 25]

#     if request.method == "POST":
#         selected_month = request.form["month"]
#         session['selected_month'] = selected_month
#         # Update data based on the selected month
#         # query the database to get the data for the selected month
#         # Using temporary dummy data for now
#         pie_data = [30, 20, 25, 25]
#     else:
#         selected_month = session.get('selected_month', None)
 

#     # Return the components to the HTML template 
#     return render_template(
#         "dashboard.html",
#         total_incomes=total_incomes,
#         total_expenses=total_expenses,
#         total_balances=total_balances,
#         line_labels=months,
#         pie_data=pie_data,
#         pie_labels=pie_labels,
#         selected_month=selected_month,
#         months=months
#     )
    )
