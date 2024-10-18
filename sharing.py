from twilio.rest import Client
account_sid = 'ACca9e164677ddf5066dbacee83d8679a7'
auth_token = '138cabefeac77fcdbd3d504cb3877e27'
FROM = 'whatsapp:+14155238886'
client = Client(account_sid, auth_token)
to_number = '+917506114081'
def sharing_option(to_number):
    try:
        # print(f"Text message sent successfully. SID: {message.sid}")
        template_message = client.messages.create(
            from_=FROM,
            to=f'whatsapp:{to_number}',
            # body = "Are you interested in joining LeadgenAI?",
            content_sid = "HXe54910a4a4e2a4462db590b430a937da",
            # content_variables=json.dumps({        
            #                 "1": person_name    })
        )
    except Exception as e:
        print(f"Error sending message: {e}")
        return None
    return template_message.sid
    # print(f"Message sent with SID: {template_message.sid}")
 
 
sharing_option(to_number)