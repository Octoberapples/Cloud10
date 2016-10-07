# coding=utf-8
from celery import Celery
import json
from subprocess import call
import shlex
from naca2gmsh_geo import main as naca2gmsh

#GMSHBIN="/usr/bin/gmsh"
GMSHBIN = "/Applications/Gmsh.app/Contents/MacOS/gmsh"

cApp = Celery('tasks', broker='amqp://guest@localhost//')

#@cApp.task

def generateMesh(naca1, naca2, naca3, naca4, angle, n_nodes, n_levels):
    
    filename="a"+str(angle)+"n"+str(n_nodes)

    with open(filename + ".geo", "w") as file :
        file.write(naca2gmsh(naca1, naca2, naca3, naca4, angle, n_nodes))

    # $GMSHBIN -v 0 -nopopup -2 -o $MSHDIR/r0$mshfile $GEODIR/$i;
    call(GMSHBIN + " -v 0 -nopopup -2 -o r0" + filename + ".msh " + filename + ".geo", shell=True)

    oldname = "r0" + filename + ".msh"
    for i in range(0,n_levels) : 
        newname="r"+str(i+1)+filename+".msh"; 
        call("cp " + oldname + " " + newname, shell=True)
        call(GMSHBIN +" -refine -v 0 " + newname, shell=True)
        oldname = newname
    

@cApp.task

def converter():
    pass


@cApp.task

def calculator():
    pass


