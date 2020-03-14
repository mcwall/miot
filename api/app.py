from flask import Flask, request
import json
app = Flask(__name__)

@app.route('/ask', methods=['GET', 'POST'])
def hello_world():
    req = request.get_json()
    app.logger.info('got GET ask: %s', json.dumps(req))
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')