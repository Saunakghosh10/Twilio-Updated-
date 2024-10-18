from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import pandas as pd
from twilio.rest import Client
import os
import json
from get_vendor import handle_vendor_request
from response_accept import accept_whatsapp_message
from response_check import match_vendors

############################################ Twilio Account Details #############################################################

account_sid = 'ACca9e164677ddf5066dbacee83d8679a7'
auth_token = '138cabefeac77fcdbd3d504cb3877e27'
client = Client(account_sid, auth_token)
FROM = 'whatsapp:+14155238886'


vendor_number = "+9176354637283"  # Vendor's phone number

user_states = {}
global conversation_states


# Configurations
person_name = 'Swati'
to_number = '+917506114081' 
conversation_states = {}
user_details = {}
fields_list = [
    'Name','Company Name', 'Website', 'Requirement Description', 'Requirement description Keywords',
    'Offerings', 'Offering Keywords', 'Sales Pitch',
    'LinkedIn', 'Email','WhatsApp Number', 'Calendly Link', 'Designation', 'Role'
]

user_states = {}

# Load Excel data
data = pd.read_excel(r"C:\Users\maury\OneDrive\Desktop\twilio demo code\Updated_Dummy_Service_Recommendation (1).xlsx")

# Save user details to Excel
def save_user_details_to_excel(details):
    global data
    new_row = {
        'Name': details['Name'],
        'Company Name': details.get('Company Name', ''),
        'Website': details.get('Website', ''),
        'Requirement Description': details.get('Requirement Description', ''),
        'Requirement description Keywords': details.get('Requirement description Keywords', ''),
        'Offerings': details.get('Offerings', ''),
        'Offering Keywords': details.get('Offering Keywords', ''),
        'Sales Pitch': details.get('Sales Pitch', ''),
        'LinkedIn': details.get('LinkedIn', ''),
        'Email': details.get('Email',''),
        'WhatsApp Number': details.get('WhatsApp Number', ''),
        'Calendly Link': details.get('Calendly Link', ''),
        'Designation': details.get('Designation', ''),
        'Role': details.get('Role', '')
    }
    data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)
    data.to_excel(r"C:\Users\maury\OneDrive\Desktop\twilio demo code\Updated_Dummy_Service_Recommendation (1).xlsx", index=False)
   

############################################ Get the next field for data collection ############################################################
def get_next_field(current_field):
    if current_field is None:
        return fields_list[0]
    else:
        current_index = fields_list.index(current_field)
        if current_index + 1 < len(fields_list):
            return fields_list[current_index + 1]
        else:
            return None

 
def get_recommended_vendors(user_data):
    keywords = user_data.get('Requirement description Keywords', '')
    requirement_description = user_data.get('Requirement Description', '')
    user_company = user_data.get('Company Name', '')  # Get the user's company name from user_data

    # Initialize an empty list to store matched vendors
    matched_vendors_str = []

    # If no keywords or requirement description is provided, return an empty list
    if not keywords and not requirement_description:
        return matched_vendors_str

    # Filter vendors based on the keywords
    if keywords:
        filtered_vendors = data[
            data['Requirement description Keywords'].str.contains(keywords, case=False, na=False)
        ]
    else:
        filtered_vendors = data

    # Further filter vendors based on the requirement description
    if requirement_description:
        filtered_vendors = filtered_vendors[
            filtered_vendors['Requirement Description'].str.contains(requirement_description, case=False, na=False)
        ]

    # Create a list of matched vendors, excluding the user's company
    if not filtered_vendors.empty:
        for _, row in filtered_vendors.iterrows():
            # Skip recommending the user's own company based on the company name
            if row['Company Name'].lower() == user_company.lower():
                continue  # Skip this vendor if the company matches the user

            vendor_details = f"Name: {row['Name']}, WhatsApp: {row['WhatsApp Number']}, LinkedIn: {row['LinkedIn']}, Company: {row['Company Name']}"
            matched_vendors_str.append(vendor_details)

    return matched_vendors_str


app = Flask(__name__)

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    incoming_msg = request.values.get('Body', '').strip().lower()
    user_phone_number = request.values.get('From', '').replace('whatsapp:', '')
    response = MessagingResponse()
    message = response.message()

    if user_phone_number not in conversation_states:
        conversation_states[user_phone_number] = {'stage': 'initial'}
    
    if user_phone_number not in user_details:
        user_details[user_phone_number] = {}

    # Get the current stage for the user
    current_stage = conversation_states[user_phone_number]['stage']

    # Initial stage of the conversation
    if current_stage == 'initial':
        if incoming_msg == 'yes':
            template_message = client.messages.create(
                from_=FROM,
                to=f'whatsapp:{to_number}',
                content_sid='HX3c421466f6af84b942a04c1782077469'
                #HX708a597d786c92a29796b5d6e462c8b4
            )
            return template_message.sid
        elif incoming_msg == "get vendor for me":
            conversation_states[user_phone_number]['stage'] = 'vendor_requirement'
            message.body("*Great!* Can you write a text on what you are looking for? ✍️")

        elif incoming_msg == "get client for me":
            conversation_states[user_phone_number]['stage'] = 'client requirement'
            message.body("*Great*! Can you write a text on what you are looking for?")

        elif incoming_msg == "meet like-minded":
            conversation_states[user_phone_number]['stage'] = 'meet like minded requirement'
            message.body("*Great*! Let me help you to connect with like-minded people!")
            message.body(
              "🎉 **Festival Bonanza: Unbeatable AI/ML Services from Adaapt!** 🎉\n\n"
              "This festive season, **Adaapt** is excited to offer incredible deals on top-tier AI and machine learning solutions designed to elevate your business! 🚀\n\n"
              "**What We Offer:**\n"
              "At **Adaapt**, we champion the cause of **Hyperautomation**—bringing tasks to completion through innovative chat interfaces. Our expertise in **Robotic Process Automation (RPA)** and **Artificial Intelligence (AI)** has empowered organizations across sectors like **Automation, Healthcare, Finance,** and **Banking**.\n\n"
              "We excel at identifying and simplifying complex processes, reducing license-related risks, and minimizing operational costs. With our unique approach, businesses can seamlessly automate tasks, explore various RPA tools, and achieve an impressive **45% reduction in operational expenses**!\n\n"
              "🔥 **Special festival pricing is available for a limited time only!** Don’t miss this chance to supercharge your business with cutting-edge AI solutions.\n\n"
              "Let’s make your business smarter this season! 💡\n\n"
              "Best,\n"
              "Srikanth\n"
              "CEO, Adaapt\n"
              "[Adaapt Website](https://www.adaapt.ai/)\n"
              "[LinkedIn Profile](https://www.linkedin.com/in/srikanth-ravinutala-7634221a9/)")
        else:
            message.body("Response Invalid.")
        return str(response)
        
    # Requirement stage
    # elif current_stage == 'requirement': 
    #     response_message = handle_vendor_request(user_phone_number, incoming_msg)
    #     print(response_message)
    #     response = MessagingResponse()
    #     response.message(response_message)  
    #     return str(response) 
    
    elif current_stage == 'vendor_requirement': 
        response_message = handle_vendor_request(user_phone_number, incoming_msg)
        print(response_message)
        return response_message


    # Handle dynamic progression for all fields in fields_list
    for field in fields_list:
        field_key = field.lower().replace(" ", "_")
        if conversation_states[user_phone_number]['stage'] == f'awaiting_{field_key}':
            user_details[user_phone_number][field] = incoming_msg
            next_field = get_next_field(field)
            if next_field:
                conversation_states[user_phone_number]['stage'] = f'awaiting_{next_field.lower().replace(" ", "_")}'
                message.body(f"Please provide your {next_field}.")
            else:
                save_user_details_to_excel(user_details[user_phone_number])
                conversation_states[user_phone_number]['stage'] = 'awaiting_edit_choice'
                #message.body("Your details have been saved. Would you like to edit any details? Reply *edit* or *no edit*.")
                template_message = client.messages.create(
                from_=FROM,
                to=f'whatsapp:{to_number}',
                content_sid='HX708a597d786c92a29796b5d6e462c8b4')
                
                return template_message.sid
            return str(response)

    # Editing details
    
    if current_stage == 'awaiting_edit_choice':
        if incoming_msg.lower() == 'edit':
            # Format the message with line breaks and numbers for better readability
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

            # Format the message string with line breaks
            message.body(
                "Which field would you like to edit?\n" + 
                "\n".join(fields_list) + 
                "\n\nReply with the corresponding field name you'd like to edit, or type 'connect' for assistance or 'other recommendation'."
            )

            conversation_states[user_phone_number]['stage'] = 'awaiting_edit_field'

        
        elif incoming_msg.lower() == 'no edit':
            message.body("Thank you, your details have been saved. Sharing vendor details soon.")
            recommendations = get_recommended_vendors(user_details[user_phone_number])    
            last_row = data.iloc[-1]
            matched_vendors_str = match_vendors(last_row)
            user_recommendation_selection = {}
            number = 1
            if matched_vendors_str:
                first_recommendation = matched_vendors_str[0]
                # message.body(f"Recommendation 1: {first_recommendation}\nDo you accept this recommendation? Reply *yes* or *no*.")
                template_message = client.messages.create(
                from_=FROM,
                to=f'whatsapp:{to_number}',
                content_sid = "HXf3d6d41aa8a58e8c5d562703c636841e", 
                content_variables=json.dumps({        
                                "1": first_recommendation})
                )
                # message_body = "Here are the recommendations:\n\n"
                conversation_states[user_phone_number]['stage'] = 'awaiting_recommendation'
                # message.body(message_body)
                user_recommendation_selection['matched_vendors'] = matched_vendors_str
                return template_message.sid
            else:
                message.body("Sorry, no recommendations were found.")  # Fetch recommendations based on current user data
            
            #conversation_states.pop(user_phone_number)


    # Handle connection or other recommendations
    if current_stage == 'awaiting_recommendation':
        if incoming_msg.lower() == 'connect':
            # Call message_accept.py (or execute the necessary function here)
            print("connecting")
            accept_whatsapp_message(vendor_number)  # Ensure you have the correct path to the script
            message.body("You have chosen to connect. We will get in touch with you shortly.")
            return str(response)
        elif incoming_msg.lower() == 'other recommendation':
            # Fetch and display new recommendations
            recommendations = get_recommended_vendors(user_details[user_phone_number])  # Fetch new recommendations
            
            if recommendations:
                for idx, recommendation in enumerate(recommendations, start=1):
                    message.body(f"{idx}. {recommendation}")
                message.body("Feel free to ask if you want to connect with any of them! Reply with 'connect' or 'other recommendation'.")
            else:
                message.body("Sorry, no further recommendations were found.")
        else:
            message.body("Please reply with 'connect' or 'other recommendation'.")

        #return str(response)


    # Handle field editing
    if current_stage == 'awaiting_edit_field':
        field_to_edit = incoming_msg.lower().strip()
        valid_fields = [f.lower() for f in fields_list]
        if field_to_edit in valid_fields:
            conversation_states[user_phone_number]['stage'] = f'editing_{field_to_edit}'
            message.body(f"Please provide the new value for {field_to_edit}.")
        else:
            message.body("Invalid field. Please choose a valid field to edit.")
        return str(response)

    # Saving edited details
    if current_stage.startswith('editing_'):
        field_to_edit = current_stage.split('_')[1]
        field = field_to_edit.replace("_", " ").title()
        user_details[user_phone_number][field] = incoming_msg
        save_user_details_to_excel(user_details[user_phone_number])
        message.body(f"Your {field} has been updated.")
        conversation_states[user_phone_number]['stage'] = 'awaiting_edit_choice'
        message.body("Would you like to edit anything else? Reply *edit* or *no edit*.")
        return str(response)

    return str(response)




if __name__ == "__main__":
    app.run(debug=True)
