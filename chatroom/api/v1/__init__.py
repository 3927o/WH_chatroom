from flask import Blueprint
from flask_restful import Api
from flask_cors import CORS


from chatroom.api.v1.auth import generate_token


api_v1 = Blueprint('api_v1', __name__)
CORS(api_v1)
api = Api(api_v1)


@api_v1.route('/')
def index():
    return generate_token()