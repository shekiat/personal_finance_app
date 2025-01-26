import sqlite3
from db import *

# setup database
conn = sqlite3.connect("./database_files/pf_app.db")
cursor = conn.cursor() # set up cursor object for executing SQL statements

res = cursor.execute("SELECT TOTAL_BALANCE, TOTAL_EXPENSES, TOTAL_INCOME FROM TOTALS_PER_MONTH WHERE MONTH = ? AND YEAR = ?", (1, 2))

total_balance = 0
total_expenses = 0
total_income = 0

print(res.fetchall())
