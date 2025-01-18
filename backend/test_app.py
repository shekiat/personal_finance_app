from flask import Flask
import sqlite3

# object to create a flask application
app = Flask(__name__)

# setup database
conn = sqlite3.connect("database_files/pf_app.db")
cursor = conn.cursor() # set up cursor object for executing SQL statements

# route to a web address (placeholder route /)
@app.route('/')

def index():
    return 'hello yes'