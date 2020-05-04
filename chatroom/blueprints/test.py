from flask import Blueprint, render_template

from chatroom.api.v1.auth import generate_token


test = Blueprint('test', __name__)


# @test.route('/token', methods=['POST'])
# def index():
#     return generate_token()
