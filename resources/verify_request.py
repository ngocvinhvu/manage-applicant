from typing import Dict
from common import http_status_code


class VerifyRequest(object):

    def __init__(self, request):
        self.request = request

    def verify_payload(self, schema):
        if not self.request.data:
            msg = "The request not have payload"
            return {"code": http_status_code.HTTP_400_BAD_REQUEST, "message": msg, "data": None}

        if self.request.headers.get('Content-Type') != 'application/json':
            msg = "The request must include 'Content-Type: application/json' header"
            return {"code": http_status_code.HTTP_400_BAD_REQUEST, "message": msg, "data": None}
        body = self.request.json
        data, errors = schema().load(body)
        if errors:
            return {"code": http_status_code.HTTP_400_BAD_REQUEST, "message": errors, "data": None}

        if not data:
            msg = 'The payload invalid format'
            return {"code": http_status_code.HTTP_400_BAD_REQUEST, "message": msg, "data": None}

        return {"code": None, "message": None, "data": data}

    def verify_list_payload(self, schema):
        if not self.request.data:
            msg = "The request not have payload"
            return {"code": http_status_code.HTTP_400_BAD_REQUEST, "message": msg, "data": None}
        if self.request.headers.get('Content-Type') != 'application/json':
            msg = "The request must include 'Content-Type: application/json' header"
            return {"code": http_status_code.HTTP_400_BAD_REQUEST, "message": msg, "data": None}
        
        body = self.request.json
        args = []
        for arg in body:
            data, errors = schema().load(arg)
            if not data:
                msg = 'The payload invalid format'
                return {"code": http_status_code.HTTP_400_BAD_REQUEST, "message": msg, "data": None}
            args.append(data)
        return {"code": None, "message": None, "data": args}

    def verify_attributes_item(self, schema):
        body = self.request.json
        attributes = body['attributes']
        data, errors = schema().load(attributes)
        if errors:
            return {"code": http_status_code.HTTP_400_BAD_REQUEST, "message": errors, "data": None}
        if not data:
            msg = 'The payload invalid format'
            return {"code": http_status_code.HTTP_400_BAD_REQUEST, "message": msg, "data": None}
        return {"code": None, "message": None, "data": data}
