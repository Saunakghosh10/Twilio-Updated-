import os 
from flask import Flask, render_template, request, redirect, url_for
from twilio.rest import Client
from dotenv import load_dotenv
load_dotenv()
import json


account_sid = 'ACca9e164677ddf5066dbacee83d8679a7'
auth_token = '138cabefeac77fcdbd3d504cb3877e27'
client = Client(account_sid, auth_token)
FROM = 'whatsapp:+14155238886'

def send_initial_message(person_name, to_number):
    initial_message = (
        f"Hi {person_name}! Welcome to *LeadgenAI* 👋\n\n"
        "I'm LeadgenAI—your friendly AI synergy bot here to help you find suitable leads and vendors for your requirements, as well as discover, connect, and meet with interesting people across the globe. Follow the steps below to start receiving AI-recommended leads:\n\n"
        "*1*. Fill in your details  \n"
        "*2*. About your company  \n"
        "*3*. LinkedIn link  \n"
        "*4*. Product link  \n"
        "*5*. Your best sales pitch  \n"
        "*6*. Post your requirements to find vendors for you\n\n"
        # "Interested to join? Reply with *YES* or *NO*."
    )
    try:
            # print(f"Text message sent successfully. SID: {message.sid}")
            template_message = client.messages.create(
                from_=FROM,
                to=f'whatsapp:{to_number}',
                body = "Are you interested in joining LeadgenAI?",
                content_sid = "HXf3d6d41aa8a58e8c5d562703c636841e", 
                content_variables=json.dumps({        
                                "1": person_name    })
            )
    except Exception as e:
            print(f"Error sending message: {e}")
            return None
    return template_message.sid
    

person_name = 'Swati'
to_number = '+917506114081' 
send_initial_message(person_name, to_number)



