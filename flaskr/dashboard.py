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
def home():
    return render_template('dashboard.html')