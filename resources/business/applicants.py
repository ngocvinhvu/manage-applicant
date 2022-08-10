from flask_restful import Resource, reqparse
from flask import current_app as app
from flask import g, abort
from common import http_status_code
from resources.logics.applicants import ApplicantsLogic, ApplicantIdLogic


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
        app.logger.info("Get all applicants")
        applicant_logic = ApplicantsLogic(**params)
        return applicant_logic.get()

    # Creating a new applicant
    def post(self, *args, **kwargs):
        app.logger.info("Request create an applicant")
        applicant_logic = ApplicantsLogic()
        return applicant_logic.post()


class ApplicantIdResource(Resource):

    # Getting an applicant
    def get(self, applicant_id, *args, **kwargs):
        app.logger.info("Get an applicant info: %s" % applicant_id)
        applicant_logic = ApplicantIdLogic(applicant_id)
        return applicant_logic.get()

    # Updating an applicant
    def patch(self, applicant_id, *args, **kwargs):
        app.logger.info("Update an applicant: %s" % applicant_id)
        applicant_id_logic = ApplicantIdLogic(applicant_id)
        return applicant_id_logic.patch()

    # Deleting an appicant
    def delete(self, applicant_id, *args, **kwargs):
        app.logger.info("Delete an applicant: %s" % applicant_id)
        applicant_logic = ApplicantIdLogic(applicant_id)
        return applicant_logic.delete()
