# coding=utf-8
import uuid
import json
import shlex
import tempfile
import os
import dolfin_converter
import swift
import numpy
import shutil
import graph
from StringIO import StringIO
from celery import Celery, chord
from subprocess import call
from naca2gmsh_geo import main as naca2gmsh


GMSHBIN = "gmsh"
CONTAINER = 'group10_container'
GRAPH_CONTAINER = 'group10_graphs'

cApp = Celery('tasks', broker='amqp://guest@master//', backend='amqp://')


@cApp.task
def generateMesh(naca1, naca2, naca3, naca4, angle, n_nodes, n_levels):
    # Change the working directory to a temporary directory
    temp_dir = tempfile.mkdtemp()
    os.chdir(temp_dir)

    fileList = []
    filename="a"+str(angle)+"n"+str(n_nodes)
    newname = "r"+str(n_levels)+filename+".msh"

    if not swift.search_for_object(CONTAINER, newname):
        with open(filename + ".geo", "w") as f:
            f.write(naca2gmsh(naca1, naca2, naca3, naca4, angle, n_nodes))

        # $GMSHBIN -v 0 -nopopup -2 -o $MSHDIR/r0$mshfile $GEODIR/$i;
        call(GMSHBIN + " -v 0 -nopopup -2 -o r0" + filename + ".msh " + filename + ".geo", shell=True)

        oldname = "r0" + filename + ".msh"
        fileList.append(oldname)
        for i in range(0,n_levels) :
            newname="r"+str(i+1)+filename+".msh";
            call("cp " + oldname + " " + newname, shell=True)
            call(GMSHBIN +" -refine -v 0 " + newname, shell=True)
            fileList.append(newname)
            oldname = newname

        # Upload to Swift here?
        with open(newname, 'r') as f:
            swift.upload_object(CONTAINER, newname, f)

    shutil.rmtree(temp_dir)
    return newname


@cApp.task(bind=True)
def converter(self, mesh):
    try:
        temp_dir = tempfile.mkdtemp()
        os.chdir(temp_dir)

        name = '{}.xml'.format(mesh[:-4])
        if not swift.search_for_object(CONTAINER,name):
            with tempfile.NamedTemporaryFile() as f:
                swift.download_object(CONTAINER, mesh)
                dolfin_converter.gmsh2xml(mesh, f.name)
                swift.upload_object(CONTAINER, name, f)

        shutil.rmtree(temp_dir)
        return name
    except swift.SwiftException as exc:
        self.retry(exc=exc, countdown=10)


@cApp.task(bind=True)
def calculator(self, mesh):
    try:
        # Changing the working directory to a temporary directory
        # where `airfoil` will output the result files.
        temp_dir = tempfile.mkdtemp()
        os.chdir(temp_dir)
        os.mkdir('result')

        swift.download_object(CONTAINER, mesh)

        # TODO: Investigate if the arguments are supposed to be
        # customizable.
        call([
            'airfoil',
            # Number of samples
            '10',
            # Viscosity
            '0.0001',
            # Speed
            '10.',
            # Total time
            '1',
            # Input file
            mesh
        ])

        liftArray = []
        dragArray = []

        with open('results/drag_ligt.m') as f:
            for line in f:
                val = line.split()
                liftArray.append(val[1])
                dragArray.append(val[2])


        #Ignore x initial values for algoritm to stabilise
        valueRange = 10
        for i in range(0,valueRange):
            liftArray.pop(0)
            dragArray.pop(0)

        #Convert to floats to calculate the mean
        liftArray = [float (i) for i in liftArray]
        dragArray = [float (i) for i in dragArray]

        angle = mesh[mesh.find("a")+1:mesh.find("n")] #Extract angle from file name...

        liftMean = numpy.mean(liftArray)
        dragMean = numpy.mean(dragArray)

        shutil.rmtree(temp_dir)
        return angle, liftMean, dragMean
    except swift.SwiftException as exc:
        self.retry(exc=exc, countdown=10)


@cApp.task
def build_graph(results):
    temp_dir = tempfile.mkdtemp()
    os.chdir(temp_dir)

    sorted_results = sorted(results, key=lambda x: x[0])
    angles, lift, drag = zip(*sorted_results)

    name1 = '{}.png'.format(uuid.uuid4())
    name2 = '{}.png'.format(uuid.uuid4())

    with tempfile.NamedTemporaryFile() as f:
        graph.build_graph(f, 'Lift', angles, lift)
        f.seek(0)
        swift.upload_object(GRAPH_CONTAINER, name1, f)

    with tempfile.NamedTemporaryFile() as f:
        graph.build_graph(f, 'Drag', angles, lift)
        f.seek(0)
        swift.upload_object(GRAPH_CONTAINER, name2, f)

    shutil.rmtree(temp_dir)

    return name1, name2


def build_workflow(angle_start, angle_stop, n_angles, n_nodes, n_levels):
    step = (float(angle_stop) - float(angle_start)) / float(n_angles)
    tasks = [
        generateMesh.s(0, 0, 1, 2, float(angle_start) + n * step, n_nodes, n_levels) | converter.s() | calculator.s()
        for n in range(0, n_angles)
    ]
    return chord(tasks)(build_graph.s())
