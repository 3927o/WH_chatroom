from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


errors = {
    "InvalidTokenError": {
        "message": 'Invalid Token',
        "status": 401
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
    pass


def invalid(e):
    return api_abort(401, "Invalid Token")

