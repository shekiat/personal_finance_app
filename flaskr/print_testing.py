import sqlite3

# setup database
conn = sqlite3.connect("./database_files/pf_app.db")
cursor = conn.cursor() # set up cursor object for executing SQL statements

res = cursor.execute("SELECT * FROM TRANSACTIONS")
trans_list = res.fetchall()
print(trans_list)