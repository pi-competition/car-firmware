# ping flask endpoint

from flask import Flask, Response, jsonify
from flask_restful import Resource, Api
import os
from server.utils.response import success

DEVICE_INFO = {
    "name": "CAR-1",
    "type": "CAR",
    "hostname": os.environ["HOSTNAME"] if "HOSTNAME" in os.environ else "unknown",
    "status": "online",
    "id": 38, #  ArUco tag value
}

class Ping(Resource):
    def get(self):
        DEVICE_INFO["uptime"] = int(os.popen("cat /proc/uptime").read().split(" ")[0])
        return success(DEVICE_INFO)

