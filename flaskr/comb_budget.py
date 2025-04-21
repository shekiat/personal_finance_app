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

    # Check if the user already exists in Cognito
    try:
        cognito_client.admin_get_user(
            UserPoolId=COGNITO_USER_POOL_ID,
            Username=email
        )
        user_exists = True
    except cognito_client.exceptions.UserNotFoundException:
        user_exists = False
        
    if session["budget_exists"] == 0:
        session["budget_exists"] = 1
        budget_created = True
    else:
        budget_created = False

    if user_exists:
        # User already exists
        user_added = add_user_to_group(session["user_id"], email)  # Add email to multi-user budget DB
        if user_added == 0:
            return jsonify({'message': 'User already in budget', 'budget_created': budget_created}), 200
        elif user_added == 1:
            send_email(email, link_only=True)  # Send email with temp username and password
            return jsonify({'message': 'Budget created, user added!', 'budget_created': budget_created}), 200
        else:
            send_email(email, link_only=True)  # Send email with temp username and password
            return jsonify({'message': 'User added to budget!', 'budget_created': budget_created}), 200    
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
        user_added = add_user_to_group(email)  # Add email to multi-user budget DB; 0 = user already in budget, 1 = budget created and added, 2 = added
        if user_added == 0:
            return jsonify({'message': 'User already in budget', 'budget_created': budget_created}), 200
        elif user_added == 1:
            send_email(email, link_only=False, temp_username=temp_username, temp_password=temp_password)  # Send email with temp username and password
            return jsonify({'message': 'Budget created, user added!', 'budget_created': budget_created}), 200
        else:
            send_email(email, link_only=False, temp_username=temp_username, temp_password=temp_password)  # Send email with temp username and password
            return jsonify({'message': 'User added to budget!', 'budget_created': budget_created}), 200
    
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

# copy over home.py functionality

int_to_month = {
    1 : "January",
    2 : "February",
    3 : "March",
    4 : "April",
    5 : "May",
    6 : "June",
    7 : "July",
    8 : "August",
    9 : "September",
    10 : "October",
    11 : "November",
    12 : "December"
}

@bp.route('/combined_budget')
def comb_budget():
    # get group id, set as session variable
    group_id = fetch_group_id(session["user_id"])
    if group_id == None:
        session["group_id"] = None
        session["budget_exists"] = 0
        return render_template("combined_budget.html", budget_exists=0, trans_list=[], income_list=[], total_values=[], total_diffs=[], total_diff_percs=[], category_list=[], year_list=[], current_year=0, current_month=0, current_month_string="", user_name="", user_email="")
    else:
        session["budget_exists"] = 1
        session["group_id"] = group_id

        # get the totals and transactions for current month
        trans_list = []
        session['current_group_month'] = datetime.datetime.now().month
        session['current_group_year'] = datetime.datetime.now().year

        # fetch current and past month totals
        print(session['current_group_month'] - 1)
        total_values = read_month_totals(session['current_group_month'], session['current_group_year'], session["group_id"], 1)
        past_month_total_values = read_month_totals(session['current_group_month'] - 1, session['current_group_year'], session["group_id"], 1)
        print(f"total_values in cb.py: {total_values}")
        print(f"past_month_total_values in cb.py: {past_month_total_values}")
        # calculate differences, percent differences
        total_diffs = [0, 0, 0]
        total_diff_percs = [0, 0, 0]
        if past_month_total_values != (0, 0, 0):
            total_diffs = [round(x - y, 2) for x, y in zip(total_values, past_month_total_values)]
            for i in range(3):
                if past_month_total_values[i] != 0:
                    total_diff_percs[i] = round((total_values[i] - past_month_total_values[i]) / abs(past_month_total_values[i]) * 100, 2)

        trans_list = read_transactions(session['current_group_month'], session['current_group_year'], session["group_id"], 1)
        income_list = read_income(session['current_group_month'], session['current_group_year'], session["group_id"], 1)
        
        # format differences for presentation, JS SCRIPT
        for i in range(3):
            if total_diffs[i] < 0:
                total_diffs[i] = "-$" + str(int(total_diffs[i]))[1:]
            elif total_diffs[i] > 0:
                total_diffs[i] = "+$" + str(total_diffs[i])

        # get categories for drop down
        category_list = read_categories(session["group_id"], 1)

        # year list portion, this is fetched from session variable

        # month converted to string
        if isinstance(session['current_group_month'], int):
            current_month_string = int_to_month[session['current_group_month']]
            
        print(income_list)
        return render_template("combined_budget.html", budget_exists=1, trans_list=trans_list, income_list=income_list, total_values=total_values, total_diffs=total_diffs, total_diff_percs=total_diff_percs, category_list=category_list, year_list=session["year_list"], current_year = session['current_group_year'], current_month=session["current_group_month"], current_month_string=current_month_string, user_name=session['full_name'], user_email=session['user']['email'])
    
@bp.route('/api/group-submit-transaction', methods=['POST'])
def group_submit():
    data = request.json
    amount = data.get('amount')
    category = data.get('category')
    date = data.get('date')
    memo = data.get('memo', '')
    print(f"amount: {amount}")
    print(f"category: {category}")
    print(f"date: {date}")
    print(f"memo: {memo}")
    
    return_value = 0 # 0 = success, 1 = date is in the future, 2 = amount is not a valid number

    try:
        parsed_date_full = parse_date(date) # format date for comparison, to add to db
        parsed_date = parsed_date_full.date()

        current_date = datetime.datetime.strptime(str(parsed_date), '%Y-%m-%d') # formatted for comparison vs current date
    except AttributeError:
        return jsonify({"return_value" : 3, 'success' : False, 'amount': amount, 'date': date, 'category': category, 'memo': memo})
    
    try:
        float(amount)
        print(f"input date: {current_date}")
        print(f"current date: {datetime.datetime.now(tz=EST)}")
        if EST.localize(current_date) <= datetime.datetime.now(tz=EST):
            write_transaction(user=session['full_name'], amount=amount, category=category.lower(), date=parsed_date, memo=memo, user_id=session["user_id"], group_id=session["group_id"])
        else:     
            return jsonify({"return_value" : 1, 'success' : False, 'amount': amount, 'date': date, 'category': category, 'memo': memo})
    except ValueError:
        return jsonify({"return_value" : 2, 'success' : False, 'amount': amount, 'date': date, 'category': category, 'memo': memo})

    return jsonify({"return_value" : return_value, 'success' : True})


@bp.route('/api/group-submit-income', methods=['POST'])
def group_submit_inc():
    data = request.json
    amount = data.get('amount')
    date = data.get('date')
    memo = data.get('memo', '')

    return_value = 0 # 0 = success, 1 = amount not valid, 2 = date is in the future

    try:
        parsed_date_full = parse_date(date) # format date for comparison, to add to db
        parsed_date = parsed_date_full.date()

        current_date = datetime.datetime.strptime(str(parsed_date), '%Y-%m-%d')
    except AttributeError:
        return jsonify({"return_value" : 3, "success" : False, 'amount': amount, 'date': date, 'memo': memo})

    try:
        float(amount)
        if EST.localize(current_date) <= datetime.datetime.now(tz=EST):
            write_income(user=session['full_name'], amount=amount, date=parsed_date, memo=memo, user_id=session["user_id"], group_id=session["group_id"])
        else:
            return jsonify({"return_value" : 1, "success" : False, 'amount': amount, 'date': date, 'memo': memo})
    except ValueError:
        return jsonify({"return_value" : 2, "success" : False, 'amount': amount, 'date': date, 'memo': memo})
    
    return jsonify({"return_value" : return_value, "success" : True})


@bp.route('/api/group-delete-transaction', methods=['POST'])
def group_delete():
    data = request.json
    transaction_id = data.get('transaction_id')

    # REMOVE?
    # session['chosen_month'] = int(data.get('month'))
    # session['chosen_year'] = int(data.get('year'))

    delete_transaction(transaction_id, 1)

    return jsonify({'success' : True})

@bp.route('/api/group-delete-income', methods=['POST'])
def group_delete_inc():
    data = request.json
    income_id = data.get('income_id')
    
    # REMOVE?
    # session['chosen_month'] = int(request.form['month'])
    # session['chosen_year'] = int(request.form['year'])

    delete_income(income_id, 1)

    # Feedback that transaction has been deleted?

    return jsonify({'success' : True})

@bp.route('/api/group-submit-date', methods=['POST'])
def group_month_change():
    data = request.json
    month = data.get('month')
    year = data.get('year')
    print(f"submitted month: {month}")

    month_number = datetime.datetime.strptime(month, "%B").month

    session['current_group_month'] = int(month_number)
    session['current_group_year'] = int(year)

    return jsonify({"chosen_month" : month, "chosen_year" : session['current_group_year']})

@bp.route("/api/group-update-stats", methods=["POST"])
def group_update_stats_and_totals():
    # fetch current and past month totals
    total_values = read_month_totals(session['current_group_month'], session['current_group_year'], session["group_id"], 1)
    past_month_total_values = read_month_totals(session['current_group_month'] - 1, session['current_group_year'], session["group_id"], 1)
    # calculate differences, percent differences
    total_diffs = [0, 0, 0]
    total_diff_percs = [0, 0, 0]
    if past_month_total_values != (0, 0, 0):
        total_diffs = [round(x - y, 2) for x, y in zip(total_values, past_month_total_values)]
        for i in range(3):
            if past_month_total_values[i] != 0:
                total_diff_percs[i] = round((total_values[i] - past_month_total_values[i]) / abs(past_month_total_values[i]) * 100, 2)

    for i in range(3):
        if total_diffs[i] < 0:
            total_diffs[i] = "-$" + str(int(total_diffs[i]))[1:]
        elif total_diffs[i] > 0:
            total_diffs[i] = "+$" + str(total_diffs[i])
    print(f'total_values: {total_values}')
    return jsonify({
        "total_values": total_values,
        "total_diffs": total_diffs,
        "total_diff_percs": total_diff_percs
    })

@bp.route("/api/group-update-transaction-table")
def group_update_transaction_table():
    print(f"updating transactions")
    trans_list = read_transactions(session["current_group_month"], session["current_group_year"], session["group_id"], 1)
    print(trans_list)
    return jsonify({"trans_list": trans_list})

@bp.route("/api/group-update-income-table")
def group_update_income_table():
    income_list = read_income(session["current_group_month"], session["current_group_year"], session["group_id"], 1)
    return jsonify({"income_list": income_list})
  
# call group chat functions from db.py
@bp.route('/api/send-message', methods=['POST'])
def send_message():
    """Handle sending a message to the group chat."""
    data = request.get_json()
    message = data.get('message')
    user_id = session.get('user_id')  
    group_id = session.get('group_id')  

    if not message:
        return jsonify({'success': False, 'error': 'Message cannot be empty'}), 400

    try:
        insert_group_message(group_id, user_id, message)
        return jsonify({'success': True, 'message': 'Message sent successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@bp.route('/api/get-messages', methods=['GET'])
def get_messages():
    """Handle fetching messages for the group chat."""
    group_id = session["group_id"]
    print(f"group id at message fetch: {group_id}")
    messages = fetch_group_messages(group_id)
    formatted_messages = []
    for row in messages:
        # Convert the timestamp to EST
        timestamp = row['timestamp']
        if timestamp:
            localized_timestamp = timestamp.replace(tzinfo=pytz.UTC).astimezone(EST)
            formatted_timestamp = localized_timestamp.strftime('%Y-%m-%d %I:%M %p')  # Format as desired
        else:
            formatted_timestamp = None

        formatted_messages.append({
            'user': row['name'],
            'message': row['message'],
            'timestamp': formatted_timestamp
        })
    return jsonify({'success': True, 'messages': formatted_messages})

