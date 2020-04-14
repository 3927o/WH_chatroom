from flask import Blueprint, request
from flask_restful import Api
from flask_cors import CORS

from chatroom.api.v1.auth import auth_required
from chatroom.api.v1.errors import api_abort, errors, not_found, invalid, InvalidTokenError


def create_api_bp(name='api_bp'):
    api_bp = Blueprint(name, __name__)
    CORS(api_bp)
    register_errors(api_bp)
    api_bp.before_request(auth_required)
    return api_bp


def register_errors(api_bp):
    api_bp.register_error_handler(404, not_found)
    api_bp.register_error_handler(InvalidTokenError, invalid)


api_v1 = create_api_bp('api_v1')
api = Api(api_v1)


@api_v1.route('/')
def test():
    if request.cookies.get('token', None) is not None:
        return str(request.cookies.get('token'))
    else:
        return 'None'
