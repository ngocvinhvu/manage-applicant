from flask_restful import Resource, reqparse
from flask import abort
from common import http_status_code
from resources.logics.applicants import ApplicantsLogic, ApplicantIdLogic
from common import LOG


class ApplicantResource(Resource):
    # Getting all applicants
    def get(self, *args, **kwargs):
        parser = reqparse.RequestParser()
        parser.add_argument("items_per_page", required=False, location="args", type=int)
        parser.add_argument("page", required=False, location="args", type=int)
        params = parser.parse_args()
        if (
            params["items_per_page"]
            and params["items_per_page"] < 1
            and params["page"]
            and params["page"] < 1
        ):
            abort(
                http_status_code.HTTP_406_NOT_ACCEPTABLE, "%s" % "Parameters is invalid"
            )
        LOG.info("Get all applicants")
        applicant_logic = ApplicantsLogic(**params)
        return applicant_logic.get()

    # Creating a new applicant
    def post(self, *args, **kwargs):
        LOG.info("Request create an applicant")
        applicant_logic = ApplicantsLogic()
        return applicant_logic.post()


class ApplicantIdResource(Resource):

    # Getting an applicant
    def get(self, applicant_id, *args, **kwargs):
        LOG.info("Get an applicant info: %s" % applicant_id)
        applicant_logic = ApplicantIdLogic(applicant_id)
        return applicant_logic.get()

    # Updating an applicant
    def put(self, applicant_id, *args, **kwargs):
        LOG.info("Update an applicant: %s" % applicant_id)
        applicant_id_logic = ApplicantIdLogic(applicant_id)
        return applicant_id_logic.put()

    # Deleting an appicant
    def delete(self, applicant_id, *args, **kwargs):
        LOG.info("Delete an applicant: %s" % applicant_id)
        applicant_logic = ApplicantIdLogic(applicant_id)
        return applicant_logic.delete()
