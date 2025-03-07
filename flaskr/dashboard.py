import sqlite3
from .db import *
import datetime
from datetime import timezone
from flask import Blueprint, jsonify, render_template, request, session
import pytz
import math
import random

import random

rgb_colors = [
    "rgb(255, 0, 0)",  # Red
    "rgb(0, 255, 0)",  # Green
    "rgb(0, 0, 255)",  # Blue
    "rgb(255, 255, 0)",  # Yellow
    "rgb(255, 165, 0)",  # Orange
    "rgb(128, 0, 128)",  # Purple
    "rgb(0, 255, 255)",  # Cyan
    "rgb(255, 0, 255)",  # Magenta
    "rgb(192, 192, 192)",  # Silver
    "rgb(128, 128, 128)",  # Gray
    "rgb(0, 0, 0)",  # Black
    "rgb(255, 255, 255)",  # White
    "rgb(128, 0, 0)",  # Maroon
    "rgb(128, 128, 0)",  # Olive
    "rgb(0, 128, 0)",  # Dark Green
    "rgb(0, 128, 128)",  # Teal
    "rgb(0, 0, 128)",  # Navy
    "rgb(139, 69, 19)",  # Saddle Brown
    "rgb(210, 105, 30)",  # Chocolate
    "rgb(255, 192, 203)",  # Pink
    "rgb(255, 182, 193)",  # Light Pink
    "rgb(75, 0, 130)",  # Indigo
    "rgb(173, 216, 230)",  # Light Blue
    "rgb(144, 238, 144)",  # Light Green
    "rgb(250, 128, 114)",  # Salmon
    "rgb(244, 164, 96)",  # Sandy Brown
    "rgb(255, 228, 181)",  # Moccasin
    "rgb(255, 215, 0)",  # Gold
    "rgb(176, 224, 230)",  # Powder Blue
    "rgb(245, 245, 220)"  # Beige
]

pie_colors = rgb_colors

EST = pytz.timezone("US/Eastern")

bp = Blueprint('dashboard', __name__)

@bp.route('/dashboard', methods=['GET'])
def dashboard():
    # data for line graph
    months = ["January", "February", "March", "April", "May", "June", 
              "July", "August", "September", "October", "November", "December"]
    default_year = datetime.datetime.now(tz=EST).strftime('%Y')
    years = [year for year in range(int(default_year), int(default_year) - 11, -1)]
    total_balances, total_expenses, total_incomes = read_month_totals_for_line_graph(default_year)
    max_income_expense = max(total_expenses)
    max_income_expense = max(total_incomes) if max(total_incomes) > max_income_expense else max_income_expense
    max_income_expense = 500 * (math.ceil(max_income_expense / 500))
    max_balance = max(total_balances)
    max_balance = 500 * (math.ceil(max_balance / 500))
    min_balance = min(total_balances)
    min_balance = 500 * (math.floor(min_balance / 500))
  
    # data for pie chart
    default_month = datetime.datetime.now(tz=EST).strftime('%B')
    categories = read_categories()
    pie_dict = read_category_totals_for_pie_graph(default_month, default_year)

    pie_labels = []
    pie_data = []
    for category in categories:
        pie_labels.append(category)
        if category in pie_dict.keys():
            pie_data.append(pie_dict[category])
        else:
            pie_data.append(0)

    return render_template(
        "dashboard.html",
        total_incomes=total_incomes,
        total_expenses=total_expenses,
        total_balances=total_balances,
        line_labels=months,
        pie_data=pie_data,
        pie_labels=pie_labels,
        pie_colors = pie_colors,
        months=months,
        years=years,
        selected_month=default_month,
        selected_year=default_year,
        default_state = True,
        max_income_expense = max_income_expense,
        max_balance = max_balance,
        min_balance = min_balance,
        default_month = default_month
    )

@bp.route('/api/dashboard_data', methods=['POST'])
def dashboard_data():
    # fetch json if month is picked
    data = request.get_json()
    selected_month = data.get("selected_month")
    selected_year = data.get("selected_year")

    # get data for line graph
    months = ["January", "February", "March", "April", "May", "June", 
              "July", "August", "September", "October", "November", "December"]
    total_balances, total_expenses, total_incomes = read_month_totals_for_line_graph(selected_year)
    max_income_expense = max(total_expenses)
    max_income_expense = max(total_incomes) if max(total_incomes) > max_income_expense else max_income_expense
    max_income_expense = 500 * (math.ceil(max_income_expense / 500))
    max_balance = max(total_balances)
    max_balance = 500 * (math.ceil(max_balance / 500))
    min_balance = min(total_balances)
    min_balance = 500 * (math.floor(min_balance / 500))

    # get data for pie chart
    categories = read_categories()
    pie_dict = read_category_totals_for_pie_graph(selected_month, selected_year)

    pie_labels = []
    pie_data = []
    for category in categories:
        pie_labels.append(category)
        if category in pie_dict.keys():
            pie_data.append(pie_dict[category])
        else:
            pie_data.append(0)

    return jsonify({
        "total_incomes": total_incomes,
        "total_expenses": total_expenses,
        "total_balances": total_balances,
        "line_labels": months,
        "pie_data": pie_data,
        "pie_labels": pie_labels,
        "pie_colors": pie_colors,
        "selected_month": selected_month,
        "default_state": False,
        "max_income_expense": max_income_expense,
        "max_balance": max_balance,
        "min_balance": min_balance
    })
