from flask import Flask
import pacmd_parser
import json
import os
app = Flask(__name__)

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
    data.update(pacmd_parser.get_sinks())
    data.update(pacmd_parser.get_sink_inputs())
    return json.dumps(data)

@app.route("/")
def hello():
    return file_get_contents('index.htm')
