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

bp = Blueprint('dashboard', __name__)

@bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    # Define Line Plot Data 
    line_labels = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
 
    # Using temporary dummy data for now
    income_data = [0, 10, 15, 8, 22, 18, 25, 30, 35, 40, 45, 50]
    expenses_data = [5, 12, 8, 10, 20, 15, 30, 25, 40, 35, 50, 45]

    # Query database to get the data for each month

    # Define Pie Chart Data

    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
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
        income_data=income_data,
        expenses_data=expenses_data,
        line_labels=line_labels,
        pie_data=pie_data,
        pie_labels=pie_labels,
        selected_month=selected_month,
        months=months
    )