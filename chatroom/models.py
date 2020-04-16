from flask import g
from datetime import datetime
import random
import string
import os

from chatroom.extensions import db


assist_table = db.Table('association',
                        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                        db.Column('room_id', db.Integer, db.ForeignKey('room.id')))


class Message(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.Enum('text', 'picture', 'file'))
    content = db.Column(db.String(300))  # when type is not text, it contains postfix
    create_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', back_populates='messages')

    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))
    room = db.relationship('Room', back_populates='messages')

    def __init__(self, content='message'):
        self.content = content
        self.create_at = datetime.utcnow()
        self.updated_at = self.create_at


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(10), unique=True)
    key = db.Column(db.String(16))
    create_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    messages = db.relationship('Message', back_populates='author', cascade='all')

    rooms = db.relationship('Room', back_populates='users', secondary=assist_table)

    @classmethod
    def create_user(cls):
        user = cls()
        db.session.add(user)
        db.session.commit()
        user.username = 'customer' + str(user.id)
        db.session.commit()
        return user

    def is_master(self, room):
        if room.master_id == self.id:
            return True
        else:
            return False

    def __init__(self):
        # generate a 16-length random string as token key
        self.key = "".join(random.choice(string.ascii_letters + string.digits) for i in range(16))
        self.create_at = datetime.utcnow()
        self.updated_at = self.create_at


class Room(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), unique=True)
    introduce = db.Column(db.String(100))
    key = db.Column(db.String(8), default="".join(random.choice(string.ascii_letters+string.digits) for i in range(12)))
    create_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    master_id = db.Column(db.Integer)

    messages = db.relationship('Message', back_populates='room', cascade='all')

    users = db.relationship('User', back_populates='rooms', secondary=assist_table)

    @classmethod  # need a auth_required decorator
    def create_room(cls, name=None, introduce=None):
        room = cls()
        db.session.add(room)
        db.session.commit()
        if name is None:
            room.name = 'room' + str(room.id)
        if introduce is None:
            room.introduce = 'the master is so lazy!'
        room.master_id = g.user.id
        db.session.commit()
        return room

    def __init__(self):
        self.create_at = datetime.utcnow()
        self.updated_at = self.create_at
