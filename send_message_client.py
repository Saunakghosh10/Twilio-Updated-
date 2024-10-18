import os 
from flask import Flask, render_template, request, redirect, url_for
from twilio.rest import Client
from dotenv import load_dotenv
load_dotenv()


account_sid = os.environ.get('Account_sid')
auth_token = os.environ.get('Auth_token')
FROM = os.environ.get('From')
client = Client(account_sid, auth_token)


def send_initial_message(vendor, to_number,user_name):
    initial_message = (
        f"Hi {vendor}, {user_name} wants to connect with you for a requirement. Please reply with accept or reject."
    )

    try:
        message = client.messages.create(
            from_= FROM, 
            body=initial_message,
            to=f'whatsapp:{to_number}'
        )
        return message.sid
    except Exception as e:
        print(f"Error sending message: {e}")
        return None
    

# person_name = 'Hardik'
# to_number = '+917387438683' 
# send_initial_message(person_name, to_number)