# coding=utf-8
from celery import Celery
import json
from subprocess import call
import shlex
from naca2gmsh_geo import main as naca2gmsh
import tempfile
import os
import dolfin_converter
import swift

#GMSHBIN="/usr/bin/gmsh"
GMSHBIN = "/Applications/Gmsh.app/Contents/MacOS/gmsh"

cApp = Celery('tasks', broker='amqp://guest@localhost//')

@cApp.task

def generateMesh(naca1, naca2, naca3, naca4, angle, n_nodes, n_levels):
    fileList = []
    filename="a"+str(angle)+"n"+str(n_nodes)

    with open(filename + ".geo", "w") as file :
        file.write(naca2gmsh(naca1, naca2, naca3, naca4, angle, n_nodes))

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

    return fileList
    

@cApp.task
def converter(mesh):
    with tempfile.NamedTemporaryFile() as f:
        # TODO: Download `mesh` from Swift
        dolfin_converter.gmsh2xml(mesh, f.name)
        swift.upload_object('group10_test', 'test123', f)
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
