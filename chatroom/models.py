from flask import g, url_for
from datetime import datetime
import random
import string
from flask_socketio import emit

from chatroom.utils import generate_avatar
from chatroom.extensions import db, whooshee


assist_table = db.Table('association',
                        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                        db.Column('room_id', db.Integer, db.ForeignKey('room.id')))


@whooshee.register_model('content')
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

    def __init__(self, type_, content):
        self.type = type_
        self.content = content
        self.create_at = datetime.utcnow()
        self.updated_at = self.create_at


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
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
        generate_avatar(user.username, 'chatroom/static/avatars/user/{}.png'.format(user.id))
        db.session.commit()
        return user

    def is_master(self, room):
        if room.master_id == self.id:
            return True
        else:
            return False

    def join_room(self, room, key):
        if room.key == key:
            self.rooms.append(room)
            db.session.commit()
            return True
        return False

    def send_message(self, type_, content, room):
        new_message = Message(type_, content)
        room.messages.append(new_message)
        self.messages.append(new_message)
        db.session.add(new_message)
        db.session.commit()
        return new_message

    def __init__(self):
        # generate a 16-length random string as token key
        self.key = "".join(random.choice(string.ascii_letters + string.digits) for i in range(16))
        self.create_at = datetime.utcnow()
        self.updated_at = self.create_at


class Room(db.Model):

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    name = db.Column(db.String(10), unique=True, index=True)
    introduce = db.Column(db.String(100))
    key = db.Column(db.String(20))
    create_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    master_id = db.Column(db.Integer)

    messages = db.relationship('Message', back_populates='room', cascade='all')

    users = db.relationship('User', back_populates='rooms', secondary=assist_table)

    @classmethod  # move to User's method
    def create_room(cls, name=None, introduce=None, key=None):
        room = cls()
        db.session.add(room)
        db.session.commit()
        if name is None:
            room.name = 'room' + str(room.id)
        else:
            room.name = name
        if introduce is None:
            room.introduce = 'the master is so lazy!'
        else:
            room.introduce = introduce
        if key is None:
            room.key = "123456"
        else:
            room.key = key
        room.master_id = g.user.id
        g.user.rooms.append(room)
        generate_avatar(room.name, 'chatroom/static/avatars/room/{}.png'.format(room.id))
        db.session.commit()
        return room

    def __init__(self):
        self.create_at = datetime.utcnow()
        self.updated_at = self.create_at


def update_time(target, value, oldvalue, initiator):
    target.updated = datetime.utcnow()


db.event.listen(Room.name, 'set', update_time)
db.event.listen(Room.introduce, 'set', update_time)
db.event.listen(Room.messages, 'set', update_time)
db.event.listen(Room.users, 'set', update_time)
db.event.listen(Room.master_id, 'set', update_time)
db.event.listen(User.username, 'set', update_time)
db.event.listen(User.messages, 'set', update_time)
db.event.listen(User.rooms, 'set', update_time)
db.event.listen(Message.content, 'set', update_time)