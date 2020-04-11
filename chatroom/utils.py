from flask import g

from chatroom.extensions import db
from chatroom.models import User
# from chatroom.api.v1.auth import auth_required


# @auth_required
def create_room(name=None, introduce=None):
    from chatroom.models import Room
    room = Room()
    if name is None:
        room.name = 'room' + str(room.id)
    if introduce is None:
        room.introduce = 'the master is so lazy!'
    room.master_id = g.user.id
    db.session.add(room)
    db.session.commit()
    return room


def create_user():
    # from chatroom.models import User
    user = User()
    db.session.add(user)
    db.session.commit()
    user.username = 'customer' + str(user.id)
    db.session.commit()
    return user
