from flask_socketio import leave_room, join_room, close_room
from flask import g

from chatroom.extensions import socketio_
from chatroom.models import Message, Room
from chatroom.api.v1.schemas import message_schema


def new_message(data):
    message = Message.query.get(int(data))
    data = message_schema(message)
    socketio_.emit('new message', data, room=message.room.name)


def _leave_room(data):
    room = Room.query.get(int(data['id']))
    leave_room(room.name)
    socketio_.emit('leave room', data['username'], room=room.name)


def _join_room(data):
    room = Room.query.get(int(data['id']))
    join_room(room.name)
    socketio_.emit('join room', data['username'], room=room.name)


def delete_room(data):
    room = Room.query.get(int(data))
    close_room(room.name)
    socketio_.emit('delete room', data, room=room.name)
