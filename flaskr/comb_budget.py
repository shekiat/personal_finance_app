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

# set up the invite route for combined budget

@app.route('/send-invite', methods=['POST'])
def send_invite():
    email = request.json.get('email')
    if not email:
        return jsonify({'error': 'Email is required'}), 400

    try:
        # Initialize Cognito client
        client = boto3.client('cognito-idp', region_name=us-east-2)

        # Create user and send invite
        response = client.admin_create_user(
            UserPoolId=us-east-2_lHuYP7sWl,
            Username=email,
            UserAttributes=[
                {'Name': 'email', 'Value': email},
                {'Name': 'email_verified', 'Value': 'true'}
            ],
            
            MessageAction='SUPPRESS'  # Use 'SUPPRESS' to skip sending the default email
        )