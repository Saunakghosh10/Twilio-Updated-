from twilio.twiml.messaging_response import MessagingResponse
import pandas as pd
from response_check import match_vendors
import json
import time
from response_accept import accept_whatsapp_message




account_sid = 'ACca9e164677ddf5066dbacee83d8679a7'
auth_token = '138cabefeac77fcdbd3d504cb3877e27'
FROM = 'whatsapp:+14155238886'
from twilio.rest import Client
client = Client(account_sid, auth_token)

vendor_number = "+917387438683"
to_number = '+917506114081'

conversation_states = {}
user_details = {}

df = pd.read_excel(r"C:\Users\maury\OneDrive\Desktop\twilio demo code\Updated_Dummy_Service_Recommendation (1).xlsx")

def extract_vendor_name(text):
    # Split the text by the keyword 'I recommend connecting with'
    if 'I recommend you to speak with' in text:
        # Extract the part after 'I recommend connecting with'
        part = text.split('I recommend you to speak with')[1].strip()
        # Split again by space or punctuation to get the vendor's name
        vendor_name = part.split(' ')[0]
        return vendor_name
    return None

def handle_vendor_request(user_phone_number, incoming_msg):
    response = MessagingResponse()

    if user_phone_number not in conversation_states:
        conversation_states[user_phone_number] = {
            'stage': 'vendor_requirement',
            'name': None,
            'company_name': None,
            'website': None,
            'requirement_description': None,
            'requirement_keywords': None,
            'offerings': None,
            'offering_keywords': None,
            'sales_pitch': None,
            'linkedin': None,
            'email': None,
            'whatsapp': None,
            'designation': None,
            'role': None,
        }
        user_details[user_phone_number] = {}

    current_stage = conversation_states[user_phone_number]['stage']
    print("Current stage:", current_stage)
    print("Incoming message:", incoming_msg)

    if current_stage == 'name':
        user_details[user_phone_number]['name'] = incoming_msg
        conversation_states[user_phone_number]['stage'] = 'company_name'
    elif current_stage == 'company_name':
        user_details[user_phone_number]['company_name'] = incoming_msg
        conversation_states[user_phone_number]['stage'] = 'website'
    elif current_stage == 'website':
        user_details[user_phone_number]['website'] = incoming_msg
        conversation_states[user_phone_number]['stage'] = 'requirement_description'
    elif current_stage == 'requirement_description':
        user_details[user_phone_number]['requirement_description'] = incoming_msg
        conversation_states[user_phone_number]['stage'] = 'requirement_keywords'
    elif current_stage == 'requirement_keywords':
        user_details[user_phone_number]['requirement_keywords'] = incoming_msg
        conversation_states[user_phone_number]['stage'] = 'offerings'
    elif current_stage == 'offerings':
        user_details[user_phone_number]['offerings'] = incoming_msg
        conversation_states[user_phone_number]['stage'] = 'offering_keywords'
    elif current_stage == 'offering_keywords':
        user_details[user_phone_number]['offering_keywords'] = incoming_msg
        conversation_states[user_phone_number]['stage'] = 'sales_pitch'
    elif current_stage == 'sales_pitch':
        user_details[user_phone_number]['sales_pitch'] = incoming_msg
        conversation_states[user_phone_number]['stage'] = 'linkedin'
    elif current_stage == 'linkedin':
        user_details[user_phone_number]['linkedin'] = incoming_msg
        conversation_states[user_phone_number]['stage'] = 'email'
    elif current_stage == 'email':
        user_details[user_phone_number]['email'] = incoming_msg
        conversation_states[user_phone_number]['stage'] = 'whatsapp'
    elif current_stage == 'whatsapp':
        user_details[user_phone_number]['whatsapp'] = incoming_msg
        conversation_states[user_phone_number]['stage'] = 'designation'
    elif current_stage == 'designation':
        user_details[user_phone_number]['designation'] = incoming_msg
        conversation_states[user_phone_number]['stage'] = 'role'
    elif current_stage == 'role':
        user_details[user_phone_number]['role'] = incoming_msg
        response.message("Thank you! Your details have been recorded 🎉.\n Would you like to edit any details? Reply *edit* or *no edit*.")
        conversation_states[user_phone_number]['stage'] = 'awaiting_edit_choice'
        update_excel_with_user_details(user_phone_number)
        template_message = client.messages.create(
                from_=FROM,
                to=f'whatsapp:{to_number}',
                content_sid='HX708a597d786c92a29796b5d6e462c8b4')
               
        return template_message.sid
        # conversation_states[user_phone_number]['stage'] = 'awaiting_edit_choice'
        # update_excel_with_user_details(user_phone_number)
        # return str(response)
    


    if current_stage == 'awaiting_edit_choice':
        if incoming_msg.lower() == 'edit':
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

            response.message(
                "Which field would you like to edit?\n" +
                "\n".join(fields_list) +
                "\n\nReply with the corresponding field name you'd like to edit, or type 'no'"
            )

            conversation_states[user_phone_number]['stage'] = 'awaiting_edit_field'

        elif incoming_msg.lower() == 'no edit':
        
            time.sleep(5)
            # recommendations = get_recommended_vendors(user_details[user_phone_number]) 
            #data = pd.read_excel(r"C:\Users\maury\OneDrive\Desktop\twilio demo code\Updated_Dummy_Service_Recommendation (1).xlsx")   
            last_row = df.iloc[-1]
            matched_vendors_str = match_vendors(last_row)
            #user_recommendation_selection = {}
            #number = 1
            if matched_vendors_str:
                conversation_states[user_phone_number]['sent_recommendations'] = []  # Reset the recommendation list
    
                for idx, rec in enumerate(matched_vendors_str, 1):
                    vendor_name = extract_vendor_name(rec)
                    print(vendor_name)
                    # vendor_name = rec  # Assuming the vendor name is the recommendation text
                    # Send Twilio template message
                    template_message = client.messages.create(
                        from_=FROM,
                        to=f'whatsapp:{to_number}',
                        content_sid="HX8b420296f1455bef398d5b543971defb",
                        content_variables=json.dumps({"3": rec,'4':vendor_name})
                    )
                
                    # Save each sent recommendation to conversation state
                    conversation_states[user_phone_number]['sent_recommendations'].append({
                        'vendor_name': vendor_name,
                        'template_message_sid': template_message.sid  # Optional, for tracking Twilio message IDs
                    })
                
                    print(f"Recommendation {idx}: {vendor_name} sent, SID: {template_message.sid}")
                    time.sleep(2)  # Delay between messages (optional)
                
                #conversation_states[user_phone_number]['stage'] = 'awaiting_recommendation'
            else:
                response.message("Sorry, no recommendations were found.")
            return str(response)

    if current_stage == 'awaiting_recommendation':
        if 'connect' in incoming_msg.lower():
            matched_vendor = None
       
            for rec in conversation_states[user_phone_number]['sent_recommendations']:
                if rec['vendor_name'].lower() in incoming_msg.lower():
                    matched_vendor = rec
                    break
           
            # If we found a matching vendor
            if matched_vendor:
                vendor_name = matched_vendor['vendor_name']
                response.message(f"You have chosen to connect with {vendor_name}. The vendor will get in touch with you soon.")
                # accept_whatsapp_message(vendor_number)  # Ensure you pass the correct vendor number here
 
            else:
                response.message("Sorry, we couldn't find the vendor you mentioned. Please check and try again.")

    if current_stage == 'awaiting_edit_field':
        field_choice = incoming_msg.lower().strip()  
        
        valid_fields = [field.lower() for field in [
            "Name", "Company Name", "Website", "Requirement Description",
            "Requirement Description Keywords", "Offerings", "Offering Keywords",
            "Description about Offerings", "Sales Pitch", "LinkedIn",
            "WhatsApp Number", "Calendly Link", "Designation", "Role"]]
        
        if field_choice in valid_fields:
            field_name = [field for field in [
                "Name", "Company Name", "Website", "Requirement Description",
                "Requirement Description Keywords", "Offerings", "Offering Keywords",
                "Description about Offerings", "Sales Pitch", "LinkedIn",
                "WhatsApp Number", "Calendly Link", "Designation", "Role"] if field.lower() == field_choice][0]
            
            response.message(f"Please enter the new value for {field_name}.")
            conversation_states[user_phone_number]['stage'] = f'awaiting_{field_name.lower().replace(" ", "_")}_value'
        else:
            response.message("Please choose a valid field from the list.")
    
    
    elif current_stage.startswith('awaiting_'):
        new_value = incoming_msg  
        field_name = current_stage.split('awaiting_')[1].replace('_', ' ')
        conversation_states[user_phone_number][field_name] = new_value
        response.message(f"{field_name} has been updated to: {new_value}")
        update_excel_with_user_details(user_phone_number)
        




    # Ask the next question based on the current stage
    if current_stage == 'vendor_requirement':
        response.message("Great! What’s your Name? 😊")
        conversation_states[user_phone_number]['stage'] = 'name'
    elif current_stage == 'name':
        response.message("What’s your Company Name? 🏢")
    elif current_stage == 'company_name':
        response.message("Can you provide your Website? 🌐") #'Please provide Requirement Description'
    elif current_stage == 'website':
        response.message("Please provide Requirement Description 🔑")  
    elif current_stage == 'requirement_description':
        response.message("What are your Requirement Keywords (comma-separated)? 🔑")
    elif current_stage == 'requirement_keywords':
        response.message("What are your Offerings? 🌟")
    elif current_stage == 'offerings':
        response.message("Please provide Offering Keywords (comma-separated): 🔑")
    elif current_stage == 'offering_keywords':
        response.message("Please give me your best sales pitch ? 💬")
    elif current_stage == 'sales_pitch':
        response.message("Can you provide your LinkedIn Profile URL? 🌐")
    elif current_stage == 'linkedin':
        response.message("What is your Email Address? 📧")
    elif current_stage == 'email':
        response.message("Please provide your WhatsApp Number. 📱")
    elif current_stage == 'whatsapp':
        response.message("What is your Designation? 🎓")
    elif current_stage == 'designation':
        response.message("What is your Role? 🤝")


    
    
    if all(key in user_details[user_phone_number] for key in [
            'name', 'company_name', 'website', 'requirement_description',
            'requirement_keywords', 'offerings', 'offering_keywords',
            'sales_pitch', 'linkedin', 'email', 'whatsapp', 'designation', 'role'
        ]):
            update_excel_with_user_details(user_phone_number)

    return str(response)


def handle_client_request(user_phone_number, incoming_msg):
    response = MessagingResponse()

    if user_phone_number not in conversation_states:
        conversation_states[user_phone_number] = {
            'stage': 'vendor_requirement',
            'name': None,
            'company_name': None,
            'website': None,
            'requirement_description': None,
            'requirement_keywords': None,
            'offerings': None,
            'offering_keywords': None,
            'sales_pitch': None,
            'linkedin': None,
            'email': None,
            'whatsapp': None,
            'designation': None,
            'role': None,
        }
        user_details[user_phone_number] = {}

    current_stage = conversation_states[user_phone_number]['stage']
    print("Current stage:", current_stage)
    print("Incoming message:", incoming_msg)

    if current_stage == 'name':
        user_details[user_phone_number]['name'] = incoming_msg
        conversation_states[user_phone_number]['stage'] = 'company_name'
    elif current_stage == 'company_name':
        user_details[user_phone_number]['company_name'] = incoming_msg
        conversation_states[user_phone_number]['stage'] = 'website'
    elif current_stage == 'website':
        user_details[user_phone_number]['website'] = incoming_msg
        conversation_states[user_phone_number]['stage'] = 'requirement_description'
    elif current_stage == 'requirement_description':
        user_details[user_phone_number]['requirement_description'] = incoming_msg
        conversation_states[user_phone_number]['stage'] = 'requirement_keywords'
    elif current_stage == 'requirement_keywords':
        user_details[user_phone_number]['requirement_keywords'] = incoming_msg
        conversation_states[user_phone_number]['stage'] = 'offerings'
    elif current_stage == 'offerings':
        user_details[user_phone_number]['offerings'] = incoming_msg
        conversation_states[user_phone_number]['stage'] = 'offering_keywords'
    elif current_stage == 'offering_keywords':
        user_details[user_phone_number]['offering_keywords'] = incoming_msg
        conversation_states[user_phone_number]['stage'] = 'sales_pitch'
    elif current_stage == 'linkedin':
        user_details[user_phone_number]['linkedin'] = incoming_msg
        conversation_states[user_phone_number]['stage'] = 'email'
    elif current_stage == 'email':
        user_details[user_phone_number]['email'] = incoming_msg
        conversation_states[user_phone_number]['stage'] = 'whatsapp'
    elif current_stage == 'whatsapp':
        user_details[user_phone_number]['whatsapp'] = incoming_msg
        conversation_states[user_phone_number]['stage'] = 'designation'
    elif current_stage == 'designation':
        user_details[user_phone_number]['designation'] = incoming_msg
        conversation_states[user_phone_number]['stage'] = 'role'
    elif current_stage == 'role':
        user_details[user_phone_number]['role'] = incoming_msg
        response.message("Thank you! Your details have been recorded 🎉.\n Would you like to edit any details? Reply *edit* or *no edit*.")
        conversation_states[user_phone_number]['stage'] = 'awaiting_edit_choice'
        update_excel_with_user_details(user_phone_number)
        template_message = client.messages.create(
                from_=FROM,
                to=f'whatsapp:{to_number}',
                content_sid='HX708a597d786c92a29796b5d6e462c8b4')
               
        return template_message.sid
        # conversation_states[user_phone_number]['stage'] = 'awaiting_edit_choice'
        # update_excel_with_user_details(user_phone_number)
        # return str(response)
    


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
                "14. Role"] 
            # Format the message string with line breaks
            response.message(
                "Which field would you like to edit?\n" +
                "\n".join(fields_list) +
                "\n\nReply with the corresponding field name you'd like to edit, or type 'no'"
            )
 
            conversation_states[user_phone_number]['stage'] = 'awaiting_edit_field'

        elif incoming_msg.lower() == 'no edit':
            response.message("Thank you, your details have been saved. Sharing vendor details soon.")
            # recommendations = get_recommended_vendors(user_details[user_phone_number]) 
            #data = pd.read_excel(r"C:\Users\maury\OneDrive\Desktop\twilio demo code\Updated_Dummy_Service_Recommendation (1).xlsx")   
            last_row = df.iloc[-1]
            matched_vendors_str = match_vendors(last_row)
            user_recommendation_selection = {}
            number = 1
            if matched_vendors_str:
                #first_recommendation = matched_vendors_str[0]
                for rec in matched_vendors_str:

                    # message.body(f"Recommendation 1: {first_recommendation}\nDo you accept this recommendation? Reply *yes* or *no*.")
                    template_message = client.messages.create(
                    from_=FROM,
                    to=f'whatsapp:{to_number}',
                    content_sid = "HX3a43aa2a386dbe18e82f980b33538394", 
                    content_variables=json.dumps({        
                                    "2": rec})
                    )
                    # message_body = "Here are the recommendations:\n\n"
                    if incoming_msg.lower() == "accept":
                        conversation_states[user_phone_number]['stage'] = 'awaiting_recommendation'
                    # message.body(message_body)
                    user_recommendation_selection['matched_vendors'] = matched_vendors_str
                    time.sleep(10)
                    print(f"Recommendation sent, SID: {template_message.sid}")
                    
            else:
                response.message("Sorry, no recommendations were found.") 

    if current_stage == 'awaiting_recommendation':
        if incoming_msg.lower() == 'accept':
            # Call message_accept.py (or execute the necessary function here)
            print("connecting")
            accept_whatsapp_message(vendor_number)  # Ensure you have the correct path to the script
            response.message("You have chosen to connect. We will get in touch with you shortly.")
            return str(response)

    if current_stage == 'awaiting_edit_field':
        field_choice = incoming_msg.lower()
        if field_choice in [f"{i}. {field.lower()}" for i, field in enumerate([
            "Name", "Company Name", "Website", "Requirement Description",
            "Requirement Description Keywords", "Offerings", "Offering Keywords",
            "Description about Offerings", "Sales Pitch", "LinkedIn",
            "WhatsApp Number", "Calendly Link", "Designation", "Role"], start=1)]:
            response.message(f"Please enter the new value for {field_choice.split('.')[1].strip()}.")
            conversation_states[user_phone_number]['stage'] = f'awaiting_{field_choice.split(".")[1].strip().lower().replace(" ", "_")}_value'
        else:
            response.message("Please choose a valid field from the list.")

    


        
    
 
    # Ask the next question based on the current stage
    if current_stage == 'vendor_requirement':
        response.message("Great! What’s your Name? 😊")
        conversation_states[user_phone_number]['stage'] = 'name'
    elif current_stage == 'name':
        response.message("What’s your Company Name? 🏢")
    elif current_stage == 'company_name':
        response.message("Can you provide your Website? 🌐") #'Please provide Requirement Description'
    elif current_stage == 'website':
        response.message("Please provide Requirement Description 🔑")  
    elif current_stage == 'requirement_description':
        response.message("What are your Requirement Keywords (comma-separated)? 🔑")
    elif current_stage == 'requirement_keywords':
        response.message("What are your Offerings? 🌟")
    elif current_stage == 'offerings':
        response.message("Please provide Offering Keywords (comma-separated): 🔑")
    elif current_stage == 'offering_keywords':
        response.message("What is your Sales Pitch? 💬")
    elif current_stage == 'sales_pitch':
        response.message("Can you provide your LinkedIn Profile URL? 🌐")
    elif current_stage == 'linkedin':
        response.message("What is your Email Address? 📧")
    elif current_stage == 'email':
        response.message("Please provide your WhatsApp Number. 📱")
    elif current_stage == 'whatsapp':
        response.message("What is your Designation? 🎓")
    elif current_stage == 'designation':
        response.message("What is your Role? 🤝")


    
    
    if all(key in user_details[user_phone_number] for key in [
            'name', 'company_name', 'website', 'requirement_description',
            'requirement_keywords', 'offerings', 'offering_keywords',
            'sales_pitch', 'linkedin', 'email', 'whatsapp', 'designation', 'role'
        ]):
            update_excel_with_user_details(user_phone_number)

    return str(response)



def update_excel_with_user_details(user_phone_number):
    df = pd.read_excel(r"C:\Users\maury\OneDrive\Desktop\twilio demo code\Updated_Dummy_Service_Recommendation (1).xlsx")
    
    if user_phone_number not in conversation_states:
        raise ValueError(f"No conversation state found for {user_phone_number}")
    
    mapping = {
        'name': 'Name',
        'company_name': 'Company Name',
        'website': 'Website',
        'requirement_description': 'Requirement Description',
        'requirement_keywords': 'Requirement Description Keywords',
        'offerings': 'Offerings',
        'offering_keywords': 'Offering Keywords',
        'sales_pitch': 'Sales Pitch',
        'linkedin': 'LinkedIn',
        'email': 'Email',
        'whatsapp': 'WhatsApp Number',
        'designation': 'Designation',
        'role': 'Role'
    }


    user_data_mapped = {mapping[key]: value for key, value in conversation_states[user_phone_number].items() if key in mapping}

    if user_phone_number not in df['WhatsApp Number'].values:
        new_row = {'WhatsApp Number': user_phone_number, **user_data_mapped}
        new_row_df = pd.DataFrame([new_row])
        df = pd.concat([df, new_row_df], ignore_index=True)
    else:
        for column, value in user_data_mapped.items():
            df.loc[df['WhatsApp Number'] == user_phone_number, column] = value

    df.to_excel(r"C:\Users\maury\OneDrive\Desktop\twilio demo code\Updated_Dummy_Service_Recommendation (1).xlsx", index=False)
