from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_whooshee import Whooshee


db = SQLAlchemy()
socketio = SocketIO()
whooshee = Whooshee()