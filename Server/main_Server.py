from time import sleep
import threading
from flask import Flask, render_template, url_for, request, jsonify

import cls_ServerTCP

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

cls_TCP = cls_ServerTCP.cls_ServerTCP("127.0.0.1", 500)
cls_TCP.start()

#--------------------------------------------------------------------------------------#
#---------------------------------------Code Web---------------------------------------#
#--------------------------------------------------------------------------------------#


app = Flask(__name__)
@app.route('/')
def index() :
    return render_template('index.html')

@app.route('/setMotor', methods=['POST', 'GET'])
def process_set_motor():
    global lMessageToClient
    data = request.get_json()
    lMessageToClient['valToSend'][lMessageToClient["IPClient"].index(str(data["socketIp"]))].append(str(data["val"]))
    results = {'processed': 'true'}
    return jsonify(results)

@app.route('/getConnexions', methods=['POST', 'GET'])
def process_get_connexions():
    global lMessageToClient
    results = {'ipConnected': lMessageToClient['IPClient']}
    return jsonify(results)

if __name__ == "__main__":
    threading.Thread(target=lambda : app.run(debug=False, host='192.168.0.124', port=5000, use_reloader=False)).start()

#--------------------------------------------------------------------------------------#
#----------------------------------Code Communications---------------------------------#
#--------------------------------------------------------------------------------------#

lMessageToClient = {"IPClient" : [],
                    "valToSend" : [],
                    "indexClient": []}

while True :
    for i in range(len(lMessageToClient['IPClient'])) :
        if (len(lMessageToClient['valToSend'][i]) > 0) :
            cls_TCP.lMessageToClient[lMessageToClient['indexClient'][i]].append(lMessageToClient['valToSend'][i].pop())
    
    for i in range(len(cls_TCP.lIpClients)) :
        lMessageToClient['IPClient'].append(cls_TCP.lIpClients.pop())
        lMessageToClient['indexClient'].append(cls_TCP.lIndexClients.pop())
        lMessageToClient['valToSend'].append([])
    
    sleep(0.002)
