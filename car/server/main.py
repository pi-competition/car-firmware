import flask 
from flask import request, jsonify
from flask_restful import Resource, Api
import threading
import urllib
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True
api = Api(app)
app.debug = False

DEVICES = []

from server.routes.api.ping import Ping
api.add_resource(Ping, '/api/ping')


def get_devices():
    global DEVICES
    try:
        res = urllib.request.urlopen("http://127.0.0.1:5000/devices").read()
    except:
        return print("RADAR IS OFFLINE")
    DEVICES = json.loads(res.decode("utf-8"))["data"]["devices"]

    for device in DEVICES:
        if device["ip"] != None:
            try:
                res = urllib.request.urlopen(f"http://{device['ip']}:5000/api/ping").read()
                j = json.loads(res.decode("utf-8"))
                if(not j["success"]):
                    device["status"] = "offline"
                    device["info"] = None
                    continue
                # j = json.loads(res.decode("utf-8"))
                device["info"] = j
            except:
                device["status"] = "offline"
                device["info"] = None
        else:
            device["status"] = "offline"
            device["info"] = None
    print(DEVICES)






get_devices()
threading.Timer(60, get_devices).start()
def run():
    app.run(port=5001, host="0.0.0.0", threaded=False)

comms_thread = threading.Thread(target=run)
comms_thread.start()

print("does this work")



