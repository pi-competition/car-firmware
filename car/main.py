import flask 
from flask import request, jsonify
from flask_restful import Resource, Api
import threading
import urllib
import json
import server.driver as driver
import time
import paho.mqtt.client as mqtt
app = flask.Flask(__name__)
# app.config["DEBUG"] = True
api = Api(app)
app.debug = False

DEVICES = []

controller_ip = None

from server.routes.api.ping import Ping
api.add_resource(Ping, '/api/ping')
from server.routes.api.pos import Pos
api.add_resource(Pos, '/api/pos')
from server.routes.api.target import Target
api.add_resource(Target, '/api/target')

client = mqtt.Client("controller_telemetry")

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
                if j["data"]["type"] == "CONTROL":
                    # we done found controller
                    if controller_ip != device["ip"]:
                        client.connect(device["ip"]) # reconnect cuz controller ip changed somehow
                    controller_ip = device["ip"]
            except:
                device["status"] = "offline"
                device["info"] = None
        else:
            device["status"] = "offline"
            device["info"] = None
            if j["data"]["type"] == "CONTROL":
                # we done found controller
                controller_ip = None
    print(DEVICES)






get_devices()
threading.Timer(60, get_devices).start()
def run():
    app.run(port=5001, host="0.0.0.0", threaded=False)

comms_thread = threading.Thread(target=run)
comms_thread.start()


def telemetry():
    threading.Timer(0.1, telemetry).start() # this is probably too quick, alternatively move this to the bottom of the func
    temp = os.popen("cat /sys/class/thermal/thermal_zone0/temp").read()
    temp = int(temp) / 1000
    cpu = os.popen("top -bn1 | grep load | awk '{printf \"%.2f\", $(NF-2)}'").read()
    cpu = float(cpu)
    total, used, free = map(int, os.popen('free -t -m').readlines()[-1].split()[1:])
    if controller_ip != None:
        client.publish("car_temp", temp)
        client.publish("car_cpu", cpu)
        client.publish("car_ram_used", used)
        client.publish("car_ram_free", free)
        client.publish("car_ram_total", total)


telem = threading.Timer(0.1, telemetry)
telem.start()

print("does this work")

#while True:
#    driver.main()
#    time.sleep(0.1)

print("main thread says goodbye")

#while True:
#    driver.fakeIt()
