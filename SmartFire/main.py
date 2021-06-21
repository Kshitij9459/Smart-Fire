from flask import Flask, jsonify,render_template,request
import webbrowser
import time
import random
import threading, queue
import serial 
import sys
from datetime import datetime
import json
import numpy
import pandas as pd
import csv
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
import tensorflow as tf
import matplotlib.pyplot as plt
from anfis import ANFIS

tf.compat.v1.disable_eager_execution()




app = Flask(__name__)

@app.route("/", methods = ['GET'])
def update_chart():
    return "Yo"

app.run(host = '0.0.0.0', port = 9000, debug = True)