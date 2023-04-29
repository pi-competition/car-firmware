from flask import Flask, Response, jsonify, request
from flask_restful import Resource, Api
import os
from server.utils.response import success
import driver

class Pos(Resource):
    def get(self):
        return success({"x": driver.self_x, "y": driver.self_y, "angle": driver.self_angle})
    def post(self):
        # print(request.get_json())
        # print(type(request.get_json()))
        data = request.get_json()
        driver.updateSelfPos(data["x"], data["y"], data["angle"])
        return success({})

