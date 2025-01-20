from flask import Flask
import sqlite3
import os

# object to create a flask application
app = Flask(__name__, template_folder=os.path.abspath('../frontend/templates'), 
            static_folder=os.path.abspath('../frontend/static'))

# setup database
conn = sqlite3.connect("database_files/pf_app.db")
cursor = conn.cursor() # set up cursor object for executing SQL statements

# route to a web address (placeholder route /)
@app.route('/')

def index():
    return 'hello'