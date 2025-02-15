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
    labels = [
        'January',
        'February',
        'March',
        'April',
        'May',
        'June'
    ]
 
    data = [0, 10, 15, 8, 22, 18, 25]
 
    # Return the components to the HTML template 
    return render_template(
        template_name_or_list='dashboard.html',
        data=data,
        labels=labels,
    )

