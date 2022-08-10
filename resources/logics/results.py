import os
from common import http_status_code
from exceptions import ApplicantNotFoundException
from flask import abort, request, jsonify
from flask import current_app as app
from models.applicants import Applicants, ApplicantService
from models.results import Results, generate_key, check_dob_odd_or_even
from resources.verify_request import VerifyRequest
from schema.applicants import ApplicantSchema
from schema.results import ProcessResults


class ResultsLogic(object):
    def __init__(self):
        verified = VerifyRequest(request).verify_payload(ProcessResults)
        if not verified["data"]:
            app.logger.debug("Error when load body request: %s" % verified["message"])
            abort(verified["code"], "%s" % verified["message"])
        self.applicant_id = verified["data"].get("applicant_id")
        try:
            applicant = ApplicantService.find_by_id(self.applicant_id)
        except ApplicantNotFoundException as e:
            abort(e.code, "%s" % e.msg)
        self.applicant = applicant

    def post(self):
        payload = {}
        payload.applicant_id = self.applicant_id
        payload.client_id = generate_key(128)
        dob = self.applicant.dob
        status = check_dob_odd_or_even(dob)
        payload.status = status
        results = Results(**payload)
        results.create(results)
        app.logger.info(f"Check applicant {self.applicant_id} status {status}")
        self.applicant.status = status
        self.applicant.update()
        app.logger.info(f"Update status of applicant {self.applicant_id} to {status}")
        message, _ = ProcessResults().dump(results)
        resp = jsonify(message)
        resp.status_code = http_status_code.HTTP_201_CREATED
        return resp
