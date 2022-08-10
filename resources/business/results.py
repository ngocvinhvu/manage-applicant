from flask_restful import Resource, reqparse
from flask import current_app as app
from flask import g, abort
from common import http_status_code
from resources.logics.results import ResultsLogic


class ResultResource(Resource):

    # Creating a new applicant
    def post(self, *args, **kwargs):
        app.logger.info("Request check an applicant status")
        result_logic = ResultsLogic()
        return result_logic.post()
