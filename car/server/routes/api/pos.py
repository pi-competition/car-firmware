from flask import Flask, Response, jsonify, request
from flask_restful import Resource, Api
import os
from server.utils.response import success
import server.driver as driver
from threading import Timer
import os

timestop = 0.2
if "CAR_TIMESTOP" in os.environ.keys():
    try:
        timestop = float(os.environ["CAR_TIMESTOP"])
    except:
        pass

dstop = driver.stop

countdown = Timer(timestop, dstop)
countdown.start()

def resetTimer():
    global countdown
    try:
        if countdown.is_alive():
            countdown.cancel()
    except:
        pass
    countdown = Timer(timestop, driver.stop)
    countdown.start()

class Pos(Resource):
    def get(self):
        return success({"x": driver.self_x, "y": driver.self_y, "angle": driver.self_angle})
    def post(self):
        # print(request.get_json())
        # print(type(request.get_json()))
#        print("update pos")
        data = request.get_json()
        driver.updateSelfPos(data["x"], data["y"], float(data["angle"]))
        print("updated", data["angle"])
        # driver.drive(driver.angleCorrection())
        driver.main()
        print("mained")
        resetTimer()
        return success({})

