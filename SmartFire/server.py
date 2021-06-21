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


ser = serial.Serial("COM4",9600)

app = Flask(__name__)
q = []

temperature = []
humidity = []
smoke = []
time_ax = []

####  Training ######


m = 16  # number of rules
alpha = 0.01  # learning rate
D = 3
num_epochs = 100
fis = ANFIS(n_inputs=D, n_rules=m, learning_rate=alpha)

ts = numpy.array(pd.read_csv('train.csv'))#numpy.loadtxt('c:\\Python_fiddling\\myProject\\MF\\trainingSet.txt',usecols=[1,2,3])
X = ts[:,0:3]
Y = ts[:,3]
with tf.compat.v1.Session() as sess:
# Initialize model parameters
    sess.run(fis.init_variables)
    trn_costs = []
    val_costs = []
    time_start = time.time()
    for epoch in range(num_epochs):
    #  Run an update step
        trn_loss, trn_pred = fis.train(sess, X, Y)
        print("Train cost after epoch %i: %f" % (epoch, trn_loss))
        if epoch == num_epochs - 1:
            time_end = time.time()
            print("Elapsed time: %f" % (time_end - time_start))

def training_afsis():
    ts = numpy.array(pd.read_csv('train.csv'))#numpy.loadtxt('c:\\Python_fiddling\\myProject\\MF\\trainingSet.txt',usecols=[1,2,3])
    X = ts[:,0:3]
    Y = ts[:,3]
    with tf.compat.v1.Session() as sess:
    # Initialize model parameters
        sess.run(fis.init_variables)
        trn_costs = []
        val_costs = []
        time_start = time.time()
        for epoch in range(num_epochs):
        #  Run an update step
            trn_loss, trn_pred = fis.train(sess, X, Y)
            print("Train cost after epoch %i: %f" % (epoch, trn_loss))
            if epoch == num_epochs - 1:
                time_end = time.time()
                print("Elapsed time: %f" % (time_end - time_start))
    

########  ENd #######




scheduler = BackgroundScheduler()
scheduler.add_job(func=training_afsis, trigger="interval", seconds=120)
scheduler.start()



def data_collection():
    
    while(1):
        #set variables
        i = 0
        #read is blocking so waits till next packet of data is sent
        temperature_r = ser.read(5).decode('utf-8')
        humidity_r = ser.read(5).decode('utf-8')
        smoke_r = ser.read(5).decode('utf-8')
        time_of_reading = datetime.now()
        #put data in queue
        q.append(temperature_r)
        q.append(humidity_r)
        q.append(smoke_r)
        q.append(time_of_reading.strftime("%H:%M"))



@app.route('/flameyo', methods=['GET', 'POST'])
def handle_request():
    content = request.json
    print(content['KEY1'])
    if(content['KEY1']=="Flame"):
        with open('train.csv','a') as f:
            writer_object = csv.writer(f)
            writer_object.writerow([q[-4]-q[-8],q[-3]-q[-7],q[-2]-q[-6],1])
    
    elif(content['KEY1'=="No Flame"]):
        with open('train.csv','a') as f:
            writer_object = csv.writer(f)
            writer_object.writerow([q[-4]-q[-8],q[-3]-q[-7],q[-2]-q[-6],0])

    return "Success"

@app.route('/map', methods=['GET', 'POST'])
def handle():
    ini_string = {'result': "pin 2"}
    ini_string = json.dumps(ini_string)
    print ("initial 1st dictionary", ini_string)
    return(ini_string)

@app.route("/update", methods = ['GET','POST'])
def update_chart():
    
    while  q:
        temperature.append(q.pop(0))
        humidity.append(q.pop(0))
        smoke.append(q.pop(0))
        time_ax.append(q.pop(0))
    
    return jsonify(results = [temperature,humidity,smoke,time_ax])


@app.route("/")
def index():
    
    return render_template('index.html')

@app.route("/check")
def fire_predict():
    Xt = numpy.zeros((1,3))
    Xt[0] = numpy.array([q[-4]-q[-8],q[-3]-q[-7],q[-2]-q[-6]])
    sess = tf.compat.v1.Session()
    e = tf.compat.v1.constant([[q[-4]-q[-8],q[-3]-q[-7],q[-2]-q[-6]]])
    val_pred = fis.infer(sess,e)
    
    if(val_pred[0]>=0.5):
        return "Alert: Fire"
    else:
        return "Safe"

@app.route("/check_length")
def yo():
    return len(q)


x = threading.Thread(target=data_collection)
x.start()
app.run(host = '0.0.0.0', port = 7000)

