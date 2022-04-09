from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    if 'quad' in incoming_msg:
        # return a shuttles arriving at quad
        r = requests.get('http://shuttle.harvard.edu/')
        # beuatiful soup 
        responded = True
    #elif
        #responded = True
    if not responded:
        msg.body('Please text me a shuttle stop to get updates!')
    return str(resp)


if __name__ == '__main__':
    app.run()