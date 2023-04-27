from flask import Flask, Response, jsonify, request
from flask_restful import Resource, Api
import os
from server.utils.response import success
import server.driver as driver

class Target(Resource):
    def get(self):
        return success({"x": driver.target_x, "y": driver.target_y})
    def post(self):
        # print(request.get_json())
        # print(type(request.get_json()))
#        print("update targ")
        data = request.get_json()
        driver.updateTargetPos(data["x"], data["y"])
        return success({})
