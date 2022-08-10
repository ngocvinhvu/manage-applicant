from flask_restful import Resource, reqparse
from flask import current_app as app
from flask import g, abort
from common import http_status_code
from resources.logics.applicants import ApplicantsLogic, ApplicantIdLogic


class ApplicantResource(Resource):

    # Creating a new applicant
    def post(self, *args, **kwargs):
        app.logger.info('Request create an applicant')
        applicant_logic = ApplicantsLogic()
        return applicant_logic.post()
