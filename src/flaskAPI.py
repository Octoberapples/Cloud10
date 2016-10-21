#!flask/bin/python
# coding=utf-8
from flask import Flask, jsonify, render_template, request, url_for
import time
from threading import Thread
import tasks


app = Flask(__name__)
response_airfoil = {}
nr_msh_job_finished = 0;
nr_xml_job_finished = 0;
nr_airfoil_job_finished = 0;

total_nr_of_jobs = 30;


## This function shows how an example for the progress bar
def updateResponse(jobFinished):
    global response_airfoil
    global nr_msh_job_finished
    global nr_xml_job_finished
    global nr_airfoil_job_finished
    global total_nr_of_jobs
    nr_job_finished = nr_msh_job_finished +  nr_xml_job_finished + nr_airfoil_job_finished

    if jobFinished == "mesh":
        nr_msh_job_finished += 1

        response_airfoil = {
            'current': nr_job_finished + 1,
            'total': total_nr_of_jobs,
            'status': "Generating mesh files..."
        }

    if jobFinished == "xml":
        nr_xml_job_finished += 1

        response_airfoil = {
            'current': nr_job_finished + 1,
            'total': total_nr_of_jobs,
            'status': "Converting to XML..."
        }

    if jobFinished == "airfoil":
        nr_airfoil_job_finished += 1

        response_airfoil = {
            'current': nr_job_finished + 1,
            'total': total_nr_of_jobs,
            'status': "Running airfoil..."
        }


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def data_post():
    angle_start = int(request.form['s_angle'])
    angle_stop = int(request.form['e_angle'])
    n_angles = int(request.form['n_angle'])
    n_nodes = int(request.form['n_nodes'])
    n_levels = int(request.form['n_levels'])

    t = tasks.build_workflow(angle_start, angle_stop, n_angles, n_nodes, n_levels)
    graphs = t.get()
    return render_template('result.html', graphs=graphs)


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
