from flask_restful import Resource
from resources.logics.results import ResultsLogic
from common import LOG


class ResultResource(Resource):

    # Check an applicant status
    def post(self, *args, **kwargs):
        """
        Check an applicant status
        ---
        summary: Check an applicant status.
        consumes:
          - application/json
        parameters:
          - in: body
            name: applicant
            description: Check an applicant status.
            schema:
              type: object
              required:
                - applicant_id
              properties:
                applicant_id:
                  type: string
                  format: uuid
        responses:
          201:
            description: Check an applicant status.
        """
        LOG.info("Request check an applicant status")
        result_logic = ResultsLogic()
        return result_logic.post()
