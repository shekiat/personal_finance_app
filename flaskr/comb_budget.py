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
import math

bp = Blueprint('combined_budget', __name__)

@bp.route('/combined_budget')
def combined_budget():
    return(render_template("combined_budget.html"))