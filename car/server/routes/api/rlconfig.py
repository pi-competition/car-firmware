# ping flask endpoint

from flask import Flask, Response, jsonify
from flask_restful import Resource, Api
import os
from server.utils.response import success
import server.driver


class RlConfig(Resource): # why didnt we call this restart!?!??!?!
    def post(self):
        # there should be some password verification here, butttt there isnt
        server.driver.rlconfig()
        return success({}, 204)

