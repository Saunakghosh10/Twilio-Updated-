import os
from twilio.rest import Client
account_sid = 'ACca9e164677ddf5066dbacee83d8679a7'
auth_token = '138cabefeac77fcdbd3d504cb3877e27'
client = Client(account_sid, auth_token)
FROM = os.environ.get('From')
client = Client(account_sid, auth_token)

def accept_whatsapp_message(vendor_phone_number):
    
    # Send the message to the vendor
    try:
        message = client.messages.create(
            from_='whatsapp:+14155238886', 
            to=f'whatsapp:{vendor_phone_number}',
            # body="Hey! Someone is interested in your offerings. Do you accept their request to connect? Please reply with 'accept' or 'reject'.",
            content_sid = "HX9d77ccf838609a846385b3dcb348a0b8"
        )
        
    except Exception as e:
        print(f"An error occurred: {e}")

    return message.sid

# vendor_number = "+917387438683"
# accept_whatsapp_message(vendor_number)