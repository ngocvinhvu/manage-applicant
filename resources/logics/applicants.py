import os
import xlsxwriter
from common import http_status_code
from exceptions import ApplicantNotFoundException
from flask import abort, request, jsonify, send_file
from models.applicants import Applicants, ApplicantService, verify_dob, verify_email
from resources.verify_request import VerifyRequest
from schema.applicants import ApplicantSchema, AppllicantPostSchema
from libs.libs import Generate
from common import LOG


class ApplicantsLogic(object):
    def __init__(self, items_per_page=None, page=None):
        self.applicants, self.count = ApplicantService.find_all_applicants(
            items_per_page, page
        )

    def get(self):
        message = []
        for applicant in self.applicants:
            msg, _ = ApplicantSchema().dump(applicant)
            message.append(msg)
        return jsonify({"applicants": message, "total": self.count})

    def post(self):
        verified = VerifyRequest(request).verify_payload(AppllicantPostSchema)
        if not verified["data"]:
            LOG.debug("Error when load body request: %s" % verified["message"])
            abort(verified["code"], "%s" % verified["message"])
        payload = verified["data"]
        dob = verify_dob(payload.get("dob"))
        email = verify_email(payload.get("email"))
        payload.update({"dob": dob, "email": email})
        applicant = Applicants(**payload)
        applicant.create(applicant)
        LOG.info(f"Created a new applicant {applicant.id} successfully")
        message, _ = ApplicantSchema().dump(applicant)
        resp = jsonify(message)
        resp.status_code = http_status_code.HTTP_201_CREATED
        return resp

    def generate(self):
        file_name = 'Applicants-Infomation.xlsx'
        _ = Generate(xlsxwriter).generate(file_name, self.applicants)
        LOG.info("Writing successfully infos")
        return send_file(f"{os.getcwd()}/{file_name}", as_attachment=True)


class ApplicantIdLogic(object):
    def __init__(self, applicant_id):
        self.applicant_id = applicant_id
        try:
            applicant = ApplicantService.find_by_id(self.applicant_id)
        except ApplicantNotFoundException as e:
            abort(e.code, "%s" % e.msg)
        self.applicant = applicant

    def get(self):
        message, _ = ApplicantSchema().dump(self.applicant)
        return jsonify(message)

    def put(self):
        verified = VerifyRequest(request).verify_payload(AppllicantPostSchema)
        if not verified["data"]:
            LOG.debug("Error when load body request: %s" % verified["message"])
            abort(verified["code"], "%s" % verified["message"])
        for (k, v) in verified["data"].items():
            if k == "email":
                v = verify_email(v)
            if k == "dob":
                v = verify_dob(v)
            setattr(self.applicant, k, v)
        self.applicant.update()

        LOG.info("Update applicant %s successful" % self.applicant_id)
        message, errors = ApplicantSchema().dump(self.applicant)
        return jsonify(message)

    def delete(self):
        self.applicant.delete(self.applicant)
        LOG.info(f"Deleted applicant {self.applicant_id} successful")
        return jsonify({"message": f"Delete applicant {self.applicant_id} successful"})

    def generate(self):
        file_name = f"Applicant-Infomation-{str(self.applicant_id)}.xlsx"
        applicant = [self.applicant]
        _ = Generate(xlsxwriter).generate(file_name, applicant)
        LOG.info("Writing successfully infos")
        return send_file(f"{os.getcwd()}/{file_name}", as_attachment=True)
