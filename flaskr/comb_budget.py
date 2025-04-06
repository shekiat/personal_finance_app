import sqlite3, boto3, os, json, requests
from .db import *
import datetime
from datetime import timezone

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session, jsonify
)
from werkzeug.exceptions import abort
import pytz
EST = pytz.timezone("US/Eastern")
import math


bp = Blueprint('combined_budget', __name__)


@bp.route('/combined_budget')
def combined_budget():
    return(render_template("combined_budget.html"))

# create temporary user 

COGNITO_USER_POOL_ID = 'us-east-2_uiivhIHti'  
AWS_REGION = 'us-east-2'  

# Initialize Cognito client
cognito_client = boto3.client('cognito-idp', region_name=AWS_REGION)

@bp.route('/invite-user', methods=['POST'])
def invite_user():
    email = request.json.get('email')
    if not email:
        return jsonify({'error': 'Email is required'}), 400

    try:
        # Check if the user already exists in Cognito
        try:
            cognito_client.admin_get_user(
                UserPoolId=COGNITO_USER_POOL_ID,
                Username=email
            )
            user_exists = True
        except cognito_client.exceptions.UserNotFoundException:
            user_exists = False

        if user_exists:
            # User already exists
            add_email_to_budget_db(email)  # Add email to multi-user budget DB
            send_email(email, link_only=True)  # Send email with link only
            return jsonify({'message': 'User already exists. Email sent with link only.'}), 200     
        else:
            # Create temporary user in Cognito and send invite
            cognito_client.admin_create_user(
                UserPoolId=COGNITO_USER_POOL_ID,
                Username=email,
                UserAttributes=[
                    {'Name': 'email', 'Value': email},
                    {'Name': 'email_verified', 'Value': 'true'}
                ],
                MessageAction='SUPPRESS'  # Use 'SUPPRESS' to skip sending the default email
            )
            add_email_to_budget_db(email)  # Add email to multi-user budget DB
            send_email(email, link_only=False, temp_password='TemporaryPassword123!')  # Send email with link and temp password
            return jsonify({'message': 'Temporary user created and email sent.'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

def add_email_to_budget_db(email):
    # Add the email to your database for the multi-user budget
    pass    

    
def send_email(email, link_only, temp_password=None):
    # Initialize the SES client using environment variables set in Heroku
    ses_client = boto3.client(
        'ses', 
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_DEFAULT_REGION')) 

    # Email content
    if link_only:
        subject = "You've Been Invited to Join the Budget"
        body = f"""
        Hi,

        You've been invited to join the budget. Click the link below to log in:
        https://money-mate-f79a354aaf62.herokuapp.com/

        Thank you,
        MoneyMate Team
        """
    else:
        subject = "Complete Your Account Setup"
        body = f"""
        Hi,

        You've been invited to join the budget. Use the following temporary password to log in and complete your account setup:

        Temporary Password: {temp_password}

        Click the link below to log in:
        https://money-mate-f79a354aaf62.herokuapp.com/

        Thank you,
        MoneyMate Team
        """

    # Send the email using Amazon SES
    try:
        response = ses_client.send_email(
            Source='shekiatillerson@oakland.edu',  # My verified email address
            Destination={
                'ToAddresses': [email]  # Recipient's email address
            },
            Message={
                'Subject': {
                    'Data': subject
                },
                'Body': {
                    'Text': {
                        'Data': body
                    }
                }
            }
        )
        print(f"Email sent to {email}: {response}")
    except Exception as e:
        print(f"Error sending email to {email}: {e}")
# Testing the send_email function

send_email('shekia313tillerson@gmail.com', link_only=False, temp_password='TemporaryPassword123!') 

# set up the invite route for combined budget

# @app.route('/send-invite', methods=['POST'])
# def send_invite():
#     email = request.json.get('email')
#     if not email:
#         return jsonify({'error': 'Email is required'}), 400

#     try:
#         # Initialize Cognito client
#         client = boto3.client('cognito-idp', region_name=us-east-2)

#         # Create user and send invite
#         response = client.admin_create_user(
#             UserPoolId=us-east-2_lHuYP7sWl,
#             Username=email,
#             UserAttributes=[
#                 {'Name': 'email', 'Value': email},
#                 {'Name': 'email_verified', 'Value': 'true'}
#             ],
            
#             MessageAction='SUPPRESS'  # Use 'SUPPRESS' to skip sending the default email
#         )