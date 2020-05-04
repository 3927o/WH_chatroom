from flask import Blueprint, abort, request, g
from flask_restful import Api
from flask_cors import CORS

from chatroom.api.v1.schemas import make_resp, messages_schema
from chatroom.api.v1.auth import auth_required, generate_token
from chatroom.api.v1.errors import api_abort, errors, not_found, invalid, permission_denied, invalid_key, name_exit,\
    InvalidTokenError, InvalidAccessKey, PermissionDenied, NameExistedError
from chatroom.api.v1.resources import UserAPI, UserListAPI, RoomAPI, RoomListAPI, MessageAPI, MessageListAPI, Message, Room
from chatroom.api.v1.utils import search, get_token


def create_api_bp(name='api_bp'):
    api_bp = Blueprint(name, __name__)
    api = Api(api_bp, errors=errors)
    CORS(api_bp)

    api_bp.add_url_rule('/search', view_func=search)
    api_bp.add_url_rule('/token', view_func=get_token)

    register_errors(api_bp)
    register_resources(api)

    api_bp.before_request(auth_required)
    return api_bp


def register_errors(api_bp):
    api_bp.register_error_handler(404, not_found)
    api_bp.register_error_handler(InvalidTokenError, invalid)
    api_bp.register_error_handler(PermissionDenied, permission_denied)
    api_bp.register_error_handler(InvalidAccessKey, invalid_key)
    api_bp.register_error_handler(NameExistedError, name_exit)


def register_resources(api):
    api.add_resource(UserAPI, '/user/', endpoint='user')
    api.add_resource(UserListAPI, '/users/', endpoint='users')
    api.add_resource(RoomAPI, '/room/<string:id_or_name>', endpoint='room')
    api.add_resource(RoomListAPI, '/rooms/', endpoint='rooms')
    api.add_resource(MessageAPI, '/message/<int:mid>', endpoint='message')
    api.add_resource(MessageListAPI, '/messages/<int:rid_or_name>', endpoint='messages')


api_v1 = create_api_bp('api_v1')


@api_v1.route('/')
def test():
    abort(404)  # raise NotFound
    if request.cookies.get('token', None) is not None:
        return str(request.cookies.get('token'))
    else:
        return 'None'
