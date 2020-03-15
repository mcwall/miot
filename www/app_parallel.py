import logging
import os

from flask import Flask, request, render_template
from flask_ask import Ask, session, question, statement
import RPi.GPIO as GPIO
from rpi_rf import RFDevice

from multiprocessing import Pool

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

tx_gpio_pins = [23, 24]
n_repeat = 1

n_devices = 2
protocols = [1, 1]
pulselengths = [355, 363]
on_codes = [5768088, 9986913]
off_codes = [5768084, 9986914]

STATUSON = ['on']
STATUSOFF = ['off']

# Should we do mode setting here?
GPIO.setmode(GPIO.BCM)
GPIO.setup(tx_gpio_pins[0], GPIO.OUT)
GPIO.setup(tx_gpio_pins[1], GPIO.OUT)

rfdevices = [RFDevice(tx_gpio_pins[0]), RFDevice(tx_gpio_pins[1])]
rfdevices[0].enable_tx()
rfdevices[1].enable_tx()

@ask.launch
def launch():
    speech_text = 'Welcome to Raspberry Pi Automation.'
    return question(speech_text).reprompt(speech_text).simple_card(speech_text)

@ask.intent('GpioIntent', mapping = {'status':'status'})
def Gpio_Intent(status,room):
    # We should do multiple attempts here to mitigate chance of RF interference
    if status in STATUSON:
	    toggle(True)
	    return statement('turning {} lights'.format(status))
    elif status in STATUSOFF:
        toggle(False)
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

@app.route('/ui')
def index():
    return render_template('index.html')

def tx(device, code, protocol, pulselength):
    print("Sending code " + str(code))
    device.tx_code(code, protocol, pulselength)
    return 0

def toggle(state):
    codes = on_codes if state else off_codes
    pool = Pool()
    result1 = pool.apply_async(tx, [rfdevices[0], codes[0], protocols[0], pulselengths[0]])
    result2 = pool.apply_async(tx, [rfdevices[1], codes[1], protocols[1], pulselengths[1]])
    answer1 = result1.get(timeout=10)
    answer2 = result2.get(timeout=10)


@app.route('/ui/light')
def light():
    state = request.args.get('state')
    on = state == 'true'
    print('Turning ' + ('on' if on else 'off') + '...' )
    toggle(on)

    return render_template('index.html')


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True, host='0.0.0.0')