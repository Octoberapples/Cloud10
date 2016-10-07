# coding=utf-8
from celery import Celery
import json
import subprocess
import shlex
import tempfile
import os


cApp = Celery('tasks', broker='amqp://guest@localhost//')

@cApp.task

def generateMesh(naca1, naca2, naca3, naca4, angle, n_nodes):
    


@cApp.task

def converter():



@cApp.task



def calculator(nameFile):

	tempDir = mkdtemp()

	os.chdir(tempDir)

	args = ["/home/ubuntu/naca_airfoil/navier_stokes_solver/airfoil", "10", "0.0001", "10.", "1",nameFile] 
	subprocess.call(args)

	print(os.listdir(tempDir))


