from flask_restful import Resource
from resources.logics.results import ResultsLogic
from common import LOG


class ResultResource(Resource):

    # Creating a new applicant
    def post(self, *args, **kwargs):
        LOG.info("Request check an applicant status")
        result_logic = ResultsLogic()
        return result_logic.post()
