from flask_sqlalchemy import Model, SQLAlchemy
from datetime import datetime
import random
import string

from chatroom.extensions import db


assist_table = db.Table('association',
                        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                        db.Column('room_id', db.Integer, db.ForeignKey('room.id')))


class Message(db.Model):
    # __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.Enum('text', 'picture', 'file'))
    content = db.Column(db.String(300))  # when type is not text, it contains postfix
    create_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', back_populates='messages')

    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    room = db.relationship('Room', back_populates='messages')

    def __init__(self, content='message'):
        self.content = content


class User(db.Model):
    # __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(10), unique=True)
    key = db.Column(db.String(16))
    create_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())

    messages = db.relationship('Message', back_populates='author', cascade='all')

    rooms = db.relationship('Room', back_populates='users', secondary=assist_table)

    def is_master(self, room):
        if room.master_id == self.id:
            return True
        else:
            return False

    def __init__(self):
        # generate a 16-length random string as token key
        self.key = "".join(random.choice(string.ascii_letters + string.digits) for i in range(16))


class Room(db.Model):
    # __tablename__ = 'room'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), unique=True)
    introduce = db.Column(db.String(100))
    create_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())
    master_id = db.Column(db.Integer)

    messages = db.relationship('Message', back_populates='room', cascade='all')

    users = db.relationship('User', back_populates='rooms', secondary=assist_table)

    def __init__(self):
        pass
