from flask import Flask, request, render_template
from rpi_rf import RFDevice

app = Flask(__name__)

pulselength = 355
protocol = 1
tx_gpio = 23
on_code = 5768088
off_code = 5768084

rfdevice = RFDevice(tx_gpio)
rfdevice.enable_tx()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/light')
def light():
    state = request.args.get('state')
    on = state == 'true'
    code = on_code if on else off_code
    print('Turning ' + ('on' if on else 'off') + '...' )
    rfdevice.tx_code(code, protocol, pulselength)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')