from flask_restful import Resource, reqparse
from flask import abort
from common import http_status_code
from resources.logics.applicants import ApplicantsLogic, ApplicantIdLogic
from common import LOG


class ApplicantResource(Resource):
    # Getting all applicants
    def get(self, *args, **kwargs):
        """
        List all applicants
        ---
        parameters:
          - in: query
            name: page
            type: int
            required: false
          - in: query
            name: items_per_page
            type: int
            requred: false
        responses:
          200:
            description: A list of applicants
        """
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
        """
        Create an applicant
        ---
        summary: Creates a new applicant.
        consumes:
          - application/json
        parameters:
          - in: body
            name: applicant
            description: The applicant to create.
            schema:
              type: object
              required:
                - name
                - email
                - dob
                - country
                - identify_number
                - phone_number
                - permanent_residence
                - nationality
                - new_applicant
                - place
              properties:
                name:
                  type: string
                email:
                  type: string
                dob:
                  type: string
                country:
                  type: string
                identify_number:
                  type: integer
                phone_number:
                  type: integer
                permanent_residence:
                  type: string
                nationality:
                  type: string
                new_applicant:
                  type: boolean
                place:
                  type: string
        responses:
          201:
            description: Created
        """
        LOG.info("Request create an applicant")
        applicant_logic = ApplicantsLogic()
        return applicant_logic.post()


class GenerateInfosResource(Resource):
    def get(self, *args, **kwargs):
      """
      Generate the infomation of all applicants
      ---
      responses:
        200:
          description: A list of applicants
      """
      LOG.info("Request create an applicant")
      applicant_logic = ApplicantsLogic()
      return applicant_logic.generate()
  

class ApplicantIdResource(Resource):

    # Getting an applicant
    def get(self, applicant_id, *args, **kwargs):
        """
        Get an applicant
        ---
        parameters:
          - in: path
            name: applicant_id
            type: string
            format: uuid
            required: true
        responses:
          200:
            description: Get an applicants
        """
        LOG.info("Get an applicant info: %s" % applicant_id)
        applicant_logic = ApplicantIdLogic(applicant_id)
        return applicant_logic.get()

    # Updating an applicant
    def put(self, applicant_id, *args, **kwargs):
        """
        Create an applicant
        ---
        summary: Creates a new applicant.
        consumes:
          - application/json
        parameters:
          - in: path
            name: applicant_id
            type: string
            format: uuid
            required: true
          - in: body
            name: applicant
            description: The applicant to create.
            schema:
              type: object
              required:
                - name
                - email
                - dob
                - country
                - identify_number
                - phone_number
                - permanent_residence
                - nationality
                - new_applicant
                - place
              properties:
                name:
                  type: string
                email:
                  type: string
                dob:
                  type: string
                country:
                  type: string
                identify_number:
                  type: integer
                phone_number:
                  type: integer
                permanent_residence:
                  type: string
                nationality:
                  type: string
                new_applicant:
                  type: boolean
                place:
                  type: string
        responses:
          204:
            description: Updated
        """
        LOG.info("Update an applicant: %s" % applicant_id)
        applicant_id_logic = ApplicantIdLogic(applicant_id)
        return applicant_id_logic.put()

    # Deleting an appicant
    def delete(self, applicant_id, *args, **kwargs):
        """
        Delete an applicant
        ---
        parameters:
          - in: path
            name: applicant_id
            type: string
            format: uuid
            required: true
        responses:
          202:
            description: Get an applicants
        """
        LOG.info("Delete an applicant: %s" % applicant_id)
        applicant_logic = ApplicantIdLogic(applicant_id)
        return applicant_logic.delete()


class GenerateInfoResource(Resource):
    def get(self, applicant_id):
        """
        Generate info of this applicant
        ---
        parameters:
          - in: path
            name: applicant_id
            type: string
            format: uuid
            required: true
        responses:
          200:
            description: Generate an applicants
        """
        LOG.info("Get an applicant info: %s" % applicant_id)
        applicant_logic = ApplicantIdLogic(applicant_id)
        return applicant_logic.generate()
