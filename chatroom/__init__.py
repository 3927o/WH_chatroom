from flask import Flask
import os

from settings import config
from chatroom.api.v1 import api_v1
from chatroom.extensions import socketio_, db, whooshee
from chatroom.socketio import new_message, _join_room, _leave_room, delete_room
from chatroom.blueprints.resource import resource_bp
from chatroom.blueprints.test import test
from chatroom.blueprints.avatars import avatar_bp


socketio_.on_event('new_message', new_message)
socketio_.on_event('leave_room', _leave_room)
socketio_.on_event('join_room', _join_room)
socketio_.on_event('delete_room', delete_room)


def creat_app(config_name=None):
    if config_name is None:
        config_name = os.getenv("FLASK_CONFIG", 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app):
    db.init_app(app)
    socketio_.init_app(app)
    whooshee.init_app(app)


def register_blueprints(app):
    app.register_blueprint(resource_bp, url_prefix='/resource')
    app.register_blueprint(api_v1, url_prefix='/api/v1')
    app.register_blueprint(test)
    app.register_blueprint(avatar_bp, url_prefix='/avatars')
