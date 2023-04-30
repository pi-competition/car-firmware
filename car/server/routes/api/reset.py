# ping flask endpoint

from flask import Flask, Response, jsonify
from flask_restful import Resource, Api
import os
from server.utils.response import success


class Reset(Resource): # why didnt we call this restart!?!??!?!
    def post(self):
        # there should be some password verification here, butttt there isnt
        def restart():
            time.sleep(1)
            print("goodbye")
            os.system("sudo reboot")
        threading.Thread(target=restart).start()
        return success({}, 204)

