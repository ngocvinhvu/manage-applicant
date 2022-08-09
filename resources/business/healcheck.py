from common import http_status_code
from flask import jsonify
from flask_restful import Resource


class HealthCheckResource(Resource):
    def get(self):
        resp = jsonify({"result": "ok"})
        resp.status_code = http_status_code.HTTP_200_OK
        return resp
