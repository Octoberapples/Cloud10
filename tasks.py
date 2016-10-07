# coding=utf-8
from celery import Celery
import json
import subprocess
import shlex
import tempfile
import os
import dolfin_converter


cApp = Celery('tasks', broker='amqp://guest@localhost//')


@cApp.task
def generateMesh(naca1, naca2, naca3, naca4, angle, n_nodes):
    pass


def converter(mesh):
    with tempfile.NamedTemporaryFile() as f:
        # TODO: Download `mesh` from Swift
        dolfin_converter.gmsh2xml(mesh, f.name)
        # TODO: upload `f` to Swift


@cApp.task
def calculator(mesh):
    # TODO: Download `mesh` from Swift

    # Changing the working directory to a temporary directory
    # where `airfoil` will output the result files.
    temp_dir = tempfile.mkdtemp()
    os.chdir(temp_dir)

    # TODO: Investigate if the arguments are supposed to be
    # customizable.
    subprocess.call([
        '/home/ubuntu/naca_airfoil/navier_stokes_solver/airfoil',
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

    # TODO: Analyze the generated files and extract only
    # the information we care about, for later comparsion
    # against other results.
