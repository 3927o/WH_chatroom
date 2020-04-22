from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


errors = {
    "NotFound": {
        'message': 'resource not found',
        'status': 404
    }
}


def api_abort(code, message=None, **kwargs):
    if message is None:
        message = HTTP_STATUS_CODES.get(code, '')

    resp = jsonify(status=code, message=message, **kwargs)
    resp.status_code = code
    return resp


def not_found(e):
    return api_abort(404, 'resource not found')


class InvalidTokenError(Exception):

    def __init__(self, description=None):
        self.description = description
        if description is None:
            self.description = 'Invalid Token'


def invalid(e):
    return api_abort(401, "Invalid Token")


class InvalidAccessKey(Exception):
    pass


class PermissionDenied(Exception):
    pass


class NameExistedError(Exception):
    pass


def permission_denied(e):
    return api_abort(403, "Permission Denied")


def invalid_key(e):
    return api_abort(401, "Invalid access key.")


def name_exit(e):
    return api_abort(400, 'name already exit')


# def error_handler(e):
#     return api_abort(e.code, e.detail)
