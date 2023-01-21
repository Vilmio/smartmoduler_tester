from time import time,sleep
import json
from typing import IO
from flask import Flask, jsonify, render_template, request
from flask.wrappers import Request
import rs485
import os
from sys import getsizeof

STATIC_PATH = 'main'
STATIC_URL_PATH = '/main'
TEMPLATE_PATH = 'main/template/'

app = Flask(__name__,template_folder=TEMPLATE_PATH,static_url_path=STATIC_URL_PATH,static_folder=STATIC_PATH)

rs485 = rs485.Com()

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/overview')
def overview():
    return render_template('overview.html')


@app.route('/updateData')
def updateData():
    rs485.updateData()
    datalayer = {'U1':rs485.data.U1,'U2':rs485.data.U2,'U3':rs485.data.U3,'I1':rs485.data.I1,'I2':rs485.data.I2,'I3':rs485.data.I3,'evState':rs485.data.evState,
                'rfidCounter':rs485.data.rfidCounter,'rfidLength':rs485.data.rfidLength,'rfidID':rs485.data.rfidID,'evseMaxCurrent':rs485.data.evseMaxCurrent,
                'serial':rs485.data.serial,'serialStatus':rs485.data.serialStatus,'hdo':rs485.data.hdo}
    response = app.response_class(
        response =json.dumps(datalayer),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/test',methods = ['POST','GET'])
def test():
    for i in request.form:
        data = json.loads(i)
        if data["cmd"] == "get_firmware_version":
            datalayer = {'Status':rs485.firmwareVersion,'Tester':getVersion()}


    response = app.response_class(
        response =json.dumps(datalayer),
        status=200,
        mimetype='application/json'
    )
    return response

def getVersion():
    arr = os.listdir()
    for i in arr:
        if i[:3] == "rev":
            version = i[3:]
            version = version.split("_")
            return version[1]
    return "0.0.0"

if __name__ =='__main__':
    app.run(host="0.0.0.0",port=8000,debug=True)
    #loop = asyncio.get_event_loop

