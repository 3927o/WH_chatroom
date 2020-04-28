from flask_socketio import SocketIO, emit
from flask_sqlalchemy import SQLAlchemy
from flask_whooshee import Whooshee


db = SQLAlchemy()
socketio_ = SocketIO(cors_allowed_origins="*")
whooshee = Whooshee()