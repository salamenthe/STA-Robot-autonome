from time import sleep
import threading
from flask import Flask, render_template, url_for, request, jsonify

import cls_ServerTCP

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

cls_TCP = cls_ServerTCP.cls_ServerTCP("192.168.0.124", 600)
cls_TCP.start()

#--------------------------------------------------------------------------------------#
#---------------------------------------Code Web---------------------------------------#
#--------------------------------------------------------------------------------------#


app = Flask(__name__)
@app.route('/')
def index() :
    return render_template('index.html')

@app.route('/motor', methods=['POST', 'GET'])
def process_set_motor():
    global lMessageToClient
    data = request.get_json()
    lMessageToClient[int(data["indexSocket"])].append(data["val"])
    results = {'processed': 'true'}
    return jsonify(results)

if __name__ == "__main__":
    threading.Thread(target=lambda : app.run(debug=True, host='192.168.0.124', port=500, use_reloader=False)).start()

#--------------------------------------------------------------------------------------#
#----------------------------------Code Communications---------------------------------#
#--------------------------------------------------------------------------------------#

lMessageToClient = []

lMessageToClient.append([])
lMessageToClient.append([])
lMessageToClient.append([])

while True :
    for i in range(len(lMessageToClient)) :
        if (len(lMessageToClient[i]) > 0 and i < len(cls_TCP.lMessageToClient)) :
            cls_TCP.lMessageToClient[i].append(lMessageToClient[i].pop())
    
    sleep(0.002)
