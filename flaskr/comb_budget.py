import sqlite3, boto3, os, json, requests, uuid
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

# Testing AWS credentials
from botocore.exceptions import NoCredentialsError
import botocore.session

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
            # Generate a unique username (UUID)
            temp_username = f"user_{uuid.uuid4().hex[:8]}"  # Generate a short unique username
            temp_password = 'TemporaryPassword123!'  # Define a temporary password

            # Create temporary user in Cognito and send invite
            cognito_client.admin_create_user(
                UserPoolId=COGNITO_USER_POOL_ID,
                Username=temp_username,
                UserAttributes=[
                    {'Name': 'email', 'Value': email},
                    {'Name': 'email_verified', 'Value': 'true'}
                ],
                TemporaryPassword=temp_password,  # Set the temporary password
                MessageAction='SUPPRESS'  # Use 'SUPPRESS' to skip sending the default email
            )
            add_email_to_budget_db(email)  # Add email to multi-user budget DB
            send_email(email, link_only=False, temp_username=temp_username, temp_password=temp_password)  # Send email with temp username and password
            return jsonify({'message': 'Temporary user created and email sent.'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

def add_email_to_budget_db(email):
    # Add the email to your database for the multi-user budget
    pass    

    
def send_email(email, link_only, temp_username=None, temp_password=None):
    # Initialize the SES client using environment variables set in Heroku
    
    def check_credentials():
        session = botocore.session.get_session()
        creds = session.get_credentials()
        print("Creds loaded:", creds)
        
    check_credentials()

    ses_client = boto3.client(
        'ses',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name='us-east-2'
    ) 
        
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

        You've been invited to join the budget. Use the following temporary username and password to log in and complete your account setup:

        Temporary Username: {temp_username}
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