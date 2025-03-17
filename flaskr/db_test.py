
import psycopg2
import sqlite3
import os

try:
    conn = psycopg2.connect("dbname='MoneyMateDB' user='nsteiner25' host='localhost'")
except:
    print("I am unable to connect to the database")

# we use a context manager to scope the cursor session
with conn.cursor() as curs:

    try:
        curs.execute("SELECT TRANS_CATEGORY, SUM(TRANS_AMOUNT) AS AMOUNT FROM TRANSACTIONS WHERE MONTH = %s AND YEAR = %s GROUP BY TRANS_CATEGORY", (1, 2025))
        trans_list = curs.fetchone()
        print(f"psql: {trans_list}")

    # a more robust way of handling errors
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database_files', 'pf_app.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
res = cursor.execute("SELECT * FROM INCOME WHERE MONTH = ? AND YEAR = ? ORDER BY INCOME_DATE DESC", (1, 2025))
print(res.fetchone())