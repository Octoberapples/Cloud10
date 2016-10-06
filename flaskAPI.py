#!flask/bin/python
# coding=utf-8
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET'])

def startProcess(angle_start, angle_stop, n_angles, n_nodes, n_levels):




if __name__ == '__main__':
    
    app.run(host='0.0.0.0',debug=True)


