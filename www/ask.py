import logging
import os

from flask import Flask
from flask_ask import Ask, request, session, question, statement
import RPi.GPIO as GPIO
from rpi_rf import RFDevice

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

pulselength = 355
protocol = 1
tx_gpio = 23
on_code = 5768088
off_code = 5768084

STATUSON = ['on']
STATUSOFF = ['off']

# Should we do mode setting here?
GPIO.setmode(GPIO.BCM)
GPIO.setup(tx_gpio, GPIO.OUT)
rfdevice = RFDevice(tx_gpio)
rfdevice.enable_tx()

@ask.launch
def launch():
    speech_text = 'Welcome to Raspberry Pi Automation.'
    return question(speech_text).reprompt(speech_text).simple_card(speech_text)

@ask.intent('GpioIntent', mapping = {'status':'status'})
def Gpio_Intent(status,room):
    # We should do multiple attempts here to mitigate chance of RF interference
    if status in STATUSON:
	    rfdevice.tx_code(on_code, protocol, pulselength)
	    return statement('turning {} lights'.format(status))
    elif status in STATUSOFF:
        rfdevice.tx_code(off_code, protocol, pulselength)
        return statement('turning {} lights'.format(status))
    else:
        return statement('Sorry not possible.')
 
@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'You can say hello to me!'
    return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)


@ask.session_ended
def session_ended():
    return "{}", 200


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True)