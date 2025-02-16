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

@bp.route('/dashboard')
def dashboard():
    # Define Plot Data 
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    total_incomes, total_expenses, total_balances = read_for_line_graph("January", "December")
 
    # Return the components to the HTML template 
    return render_template(
        'dashboard.html',
        total_incomes=total_incomes,
        total_expenses=total_expenses,
        total_balances=total_balances,
        labels=months,
    )

