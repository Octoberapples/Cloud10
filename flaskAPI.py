#!flask/bin/python
# coding=utf-8
from flask import Flask, jsonify, render_template, request 
from tasks import generateMesh

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def data_post():
    angle_start = request.form['s_angle']
    angle_stop = request.form['e_angle']
    n_angles = request.form['n_angle']
    n_nodes = request.form['n_nodes']
    n_levels = request.form['n_levels']
    
    processed_text = angle_start.upper()
    return processed_text
 



def startProcess(angle_start, angle_stop, n_angles, n_nodes, n_levels):
    #NACA four digit airfoil (Typcially NACA0012)
    NACA1 = 0
    NACA2 = 0
    NACA3 = 1
    NACA4 = 2

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
    
    


    ##ALL MESH TASKS HAVE BEEN FINISHED AND DELEGATES AS NEW TASKS.... 


if __name__ == '__main__':
    
    app.run(host='0.0.0.0',debug=True)


