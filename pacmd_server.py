from flask import Flask, request
from time import time
from sys import argv
import pacmd_handler
import json
import os
import logging
app = Flask(__name__)
T0 = time()

def file_get_contents(fpath, binary=False):
    if binary:
        mode = 'rb'
    else:
        mode = 'r'
    with open(fpath, mode) as f:
        return f.read()

@app.route('/pa_data.json')
def get_pa_data():
    data = {}
    data.update(pacmd_handler.get_sinks())
    data.update(pacmd_handler.get_sink_inputs())
    return json.dumps(data)

@app.route('/pa_control', methods=['POST'])
def pa_control():
    data = request.get_json()
    method = data.get('method', None)
    # print(request.__dict__)
    print('%s  /pa_control: %s' % (request.environ['REMOTE_ADDR'], data))
    if method == 'set_sin_volume':
        pacmd_handler.set_sink_volume(data['id'], data['value'])
    elif method == 'set_input_volume':
        pacmd_handler.set_input_volume(data['id'], data['value'])
    return ''
        

@app.route("/")
def hello():
    return file_get_contents('index.htm')

if __name__ == '__main__':
    host = '0.0.0.0'

    if 'debug' in argv:
        app.debug = True
    if 'localhost' in argv:
        host = 'localhost'

    # log = logging.getLogger('werkzeug')
    # log.setLevel(logging.ERROR)
    app.run(host=host, port=5000, threaded=True)
