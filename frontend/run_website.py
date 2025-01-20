from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)



@app.route('/')

def index():
    # setup database
    conn = sqlite3.connect("./backend/database_files/pf_app.db")
    cursor = conn.cursor() # set up cursor object for executing SQL statements

    res = cursor.execute("SELECT * FROM TRANSACTIONS")
    trans_list = res.fetchall()

    cursor.close()
    
    # return trans_list
    return render_template("index.html", trans_list=trans_list)


@app.route('/submit', methods=['POST'])
def submit():
    amount = request.form['amount']
    # category = request.form['category']
    # description = request.form['description']
    
    # Process the data (save to the database then print to console)
    #print(f"Received: Amount={amount}, Category={category}, Description={description}")
    
    #return f"Submitted: Amount={amount}, Category={category}, Description={description}"

    conn = sqlite3.connect("./backend/database_files/pf_app.db")
    cursor = conn.cursor() # set up cursor object for executing SQL statements

    cursor.execute(f"INSERT INTO TRANSACTIONS VALUES(4, {amount}, 'BILLS', '01-24-2025', 'TEST')")
    conn.commit()

    cursor.close()

    return f"Submitted: Amount={amount}"