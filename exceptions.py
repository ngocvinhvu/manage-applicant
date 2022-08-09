from flask_babel import lazy_gettext as _l
class BaseException(Exception):
    """Base Exception"""

    message = _l("An unknown exception")
    code = 500
    headers = {}
    safe = False

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs
        self.kwargs['message'] = message

        if 'code' not in self.kwargs:
            try:
                self.kwargs['code'] = self.code
            except AttributeError:
                print("AttributeError")

        try:
            message = self.message % kwargs
        except Exception:
            if not message:
                message = self.message
        self.msg = message
        super(BaseException, self).__init__(message)


class NotFoundException(BaseException):
    message = 'Resource could not be found'
    code = 404
    safe = True


class ApplicantNotFoundException(NotFoundException):
    message = 'Applicant could not be found'
