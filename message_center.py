from twilio.rest import Client
import sys


class MessageCenter:

    def __init__(self, image_path, message_text):
        self.image_path = image_path
        self.message_text = message_text
        self.TWILIO_ACCOUNT_SID = "AC90cc0a23b940f86bfcc6968a00400188"  # your twilio account_sid
        self.TWILIO_TOKEN = "1d309528795ea78b61ee2ec6ea27ebfa"  # your twilio auth_token
        self.messaging_service_id = "MG7ed0576a842afd96042a1dd161b07d48"
        self.from_number = '+14753291766'
        self.to_numbers = "+972522306872,+972509095295,+972547620141"
        self.counter = 0

    def send_message(self, service_flag):
        if service_flag == 'WHATSAPP':
            self.from_number = 'whatsapp:+14155238886'
        for phone_to in self.to_numbers.split(","):
            if service_flag == 'WHATSAPP':
                phone_to = "whatsapp:" + phone_to
            else:
                self.from_number = '+14753291766'
                pass
            try:
                client = Client(self.TWILIO_ACCOUNT_SID, self.TWILIO_TOKEN)
                message = client.messages.create(
                    ##messaging_service_sid=self.messaging_service_id,
                    from_=self.from_number,
                    body=self.message_text,
                    media_url=['https://incontrol-sys.com/' + self.image_path],
                    to=phone_to
                    # messaging_service_sid='MG7ed0576a842afd96042a1dd161b07d48',
                )

                self.counter = self.counter + 1

            except:
                print("Unexpected error:", sys.exc_info()[0])
                pass

        return "sent to " + str(self.counter) + " Recipients"
