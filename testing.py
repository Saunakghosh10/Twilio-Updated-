from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import pandas as pd
from twilio.rest import Client
import json
import time
from response_check import match_vendors

############################################ Twilio Account Details #############################################################
account_sid = 'ACca9e164677ddf5066dbacee83d8679a7'
auth_token = '138cabefeac77fcdbd3d504cb3877e27'
FROM = 'whatsapp:+14155238886'
client = Client(account_sid, auth_token)

# Configurations
to_number = '+917506114081'
conversation_states = {}

# Load Excel data dynamically
df = pd.read_excel(r"C:\Users\maury\OneDrive\Desktop\twilio demo code\Updated_Dummy_Service_Recommendation (1).xlsx")


# Initialize Flask app
app = Flask(__name__)

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    incoming_msg = request.values.get('Body', '').strip().lower()
    user_phone_number = request.values.get('From', '').replace('whatsapp:', '')
    response = MessagingResponse()
    message = response.message()

    # Initialize conversation state if new user
    if user_phone_number not in conversation_states:
        conversation_states[user_phone_number] = {
            'sent_recommendations': [],
            'stage': 'awaiting_edit_choice'
        }

    current_stage = conversation_states[user_phone_number]['stage']

    if current_stage == 'awaiting_edit_choice':
        if incoming_msg == 'edit':
            # List of fields the user can edit
            fields_list = [
                "1. Name",
                "2. Company Name",
                "3. Website",
                "4. Requirement Description",
                "5. Requirement Description Keywords",
                "6. Offerings",
                "7. Offering Keywords",
                "8. Description about Offerings",
                "9. Sales Pitch",
                "10. LinkedIn",
                "11. WhatsApp Number",
                "12. Calendly Link",
                "13. Designation",
                "14. Role"
            ] 
            # Send the list of editable fields to the user
            response.message(
                "Which field would you like to edit?\n" +
                "\n".join(fields_list) +
                "\n\nReply with the corresponding field name you'd like to edit, or type 'no'."
            )

            conversation_states[user_phone_number]['stage'] = 'awaiting_edit_field'

    elif current_stage == 'awaiting_edit_field':
        # List of valid field names (case-insensitive matching)
        field_names = [
            "Name", "Company Name", "Website", "Requirement Description",
            "Requirement Description Keywords", "Offerings", "Offering Keywords",
            "Description about Offerings", "Sales Pitch", "LinkedIn",
            "WhatsApp Number", "Calendly Link", "Designation", "Role"
        ]

        # Normalize and try to match the user's choice with available fields
        field_choice = incoming_msg.strip().lower()
        matching_field = None
        for field in field_names:
            if field.lower() == field_choice:
                matching_field = field
                break

        if matching_field:
            # Ask the user for the new value for the selected field
            response.message(f"Please enter the new value for {matching_field}.")
            # Update conversation state to wait for the value input
            conversation_states[user_phone_number]['stage'] = f'awaiting_{matching_field.lower().replace(" ", "_")}_value'
        else:
            # If no valid field is matched, prompt the user again
            response.message("Please choose a valid field from the list.")

    return str(response)

if __name__ == "__main__":
    app.run(debug=True)
