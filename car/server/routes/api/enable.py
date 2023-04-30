# ping flask endpoint

from flask import Flask, Response, jsonify
from flask_restful import Resource, Api
import os
from server.utils.response import success
import server

class Enable(Resource):
    def get(self):
        server.driver.enable = True
        return success({})
