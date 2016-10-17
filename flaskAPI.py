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
    angle, _, _ = t.get()
    return angle
    #return render_template('status.html')


##These functions are constantly pulled by jquery script in status.html #######
@app.route('/status_airfoil')
def status_airfoil():
     return jsonify(response_airfoil)

@app.route('/airfoil', methods=['POST'])
def airfoil():

     return jsonify({}), 202, {'Location': url_for('status_airfoil')}

###############################################################################


def startProcess(angle_start, angle_stop, n_angles, n_nodes, n_levels):
    #NACA four digit airfoil (Typcially NACA0012)
    NACA1 = 0
    NACA2 = 0
    NACA3 = 1
    NACA4 = 2

    #TODO: Calculate total amount of jobs to be done
    ##START OF MESH TASKS

    angleDiff = (angle_stop-angle_start)/n_angles
    gMTasks = []

    ##Push work related to creating .msh files to celery workers
    for i in range(0,n_angles):
        angle = angle_start + angleDiff * i
        tasks = generateMesh.delay(NACA1,NACA2,NACA3,NACA4,angle,n_nodes,n_levels)
        gMTasks.append(tasks) #Each gmTasks.get() will contain the generated names for .msh files that should be delegated as new tasks.


    while (len(gMTasks) != 0):
        for task in gMTasks:
            if task.ready():
                ## Create new chain converter-airfoil tasks...
                gMTasks.remove(task)



if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
