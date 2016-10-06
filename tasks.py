# coding=utf-8
from celery import Celery
import json
import subprocess
import shlex


cApp = Celery('tasks', broker='amqp://guest@localhost//')

@cApp.task

def generateMesh(naca1, naca2, naca3, naca4, angle, n_nodes):
    


@cApp.task

def converter():



@cApp.task

def calculator():



