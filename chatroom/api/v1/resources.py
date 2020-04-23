from flask_restful import Resource
from flask import g, request
import os

from chatroom.extensions import db
from chatroom.models import User, Room, Message
from chatroom.api.v1.reqparses import user_put_reqparse, room_put_reqparse, room_post_reqparse, message_post_reqparse
from chatroom.api.v1.schemas import user_schema, users_schema, make_resp, room_schema, message_schema, messages_schema
from chatroom.api.v1.errors import PermissionDenied, api_abort, InvalidAccessKey
from chatroom.api.v1.utils import get_room, secure_filename, allowed_file, check_name


class UserAPI(Resource):

    def get(self):
        # raise InvalidTokenError
        # from werkzeug.exceptions import NotFound
        # raise NotFound
        # abort(404)
        # the existed exceptions in werkzeug.exceptions can not be registered to a function
        if request.args.get('user', None) is not None:
            user = User.query.get_or_404(request.args.get('user'))
            data = user_schema(user, False, False, True)
        else:
            user = g.user
            data = user_schema(user)
        return make_resp(data)

    def put(self):
        user = g.user
        data = user_put_reqparse.parse_args()

        if data['username'] is not None:
            check_name('user', data['username'])
            user.username = data['username']
        if data['room_id'] is not None:
            room = Room.query.get_or_404(data['room_id'])
            action = data['action']
            key = data['key']

            if action == 'join' and not user.join_room(room, key):
                raise InvalidAccessKey
            elif action == 'leave':
                if user.is_master(room):
                    return api_abort(400, "the master can't leave the room")
                user.rooms.remove(room)

        db.session.commit()
        return make_resp(user_schema(user))

    def delete(self):
        user = g.user
        if Room.query.filter_by(master_id=user.id).first() is not None:
            return api_abort('400', 'you are the master of the room')
        data = user_schema(user)
        os.remove('chatroom/static/avatars/user/{}.png'.format(user.id))
        db.session.delete(user)
        db.session.commit()
        return make_resp(data)


class UserListAPI(Resource):

    def get(self):
        room_id = request.args.get('room', None)
        if room_id is not None:
            room = Room.query.get_or_404(room_id)
            if room not in g.user.rooms:
                raise PermissionDenied
            users = room.users
        else:
            users = User.query.all()
        return make_resp(users_schema(users, room_id))


class RoomAPI(Resource):

    def get(self, id_or_name):
        room = get_room(id_or_name)
        if g.user not in room.users:
            raise PermissionDenied
        return make_resp(room_schema(room))

    def put(self, id_or_name):
        room = get_room(id_or_name)
        if not g.user.is_master(room):
            raise PermissionDenied

        data = room_put_reqparse.parse_args()
        if data['name'] is not None:
            check_name('room', data['name'])
            room.name = data['name']
        if data['introduce'] is not None:
            room.introduce = data['introduce']
        if data['key'] is not None:
            room.key = data['key']
        db.session.commit()

        resp = room_schema(room)
        return make_resp(resp)

    def delete(self, id_or_name):
        room = get_room(id_or_name)
        if not g.user.is_master(room):
            raise PermissionDenied
        resp = room_schema(room)
        os.remove('chatroom/static/avatars/room/{}.png'.format(room.id))
        db.session.delete(room)
        db.session.commit()
        return make_resp(resp)


class RoomListAPI(Resource):

    def post(self):
        data = room_post_reqparse.parse_args()
        if Room.query.filter_by(name=data['name']).first() is not None:
            return api_abort(400, "room's name already exit")
        room = Room.create_room(data['name'], data['introduce'], data['key'])
        resp = make_resp(room_schema(room))
        return resp


class MessageAPI(Resource):

    def get(self, mid):
        message = Message.query.get_or_404(mid)
        if message.room not in g.user.rooms:
            raise PermissionDenied
        return make_resp(message_schema(message))

    def delete(self, mid):
        pass


class MessageListAPI(Resource):
    def get(self, rid_or_name):
        room = get_room(rid_or_name)
        messages = room.messages
        if g.user not in room.users:
            raise PermissionDenied
        return make_resp(messages_schema(messages))

    def post(self, rid_or_name):
        room = get_room(rid_or_name)
        if g.user not in room.users:
            raise PermissionDenied
        data = message_post_reqparse.parse_args()
        new_message = g.user.send_message(data['type'], data['content'], room)

        if data['type'] != 'text':
            f = request.files['file']
            if not allowed_file(f.filename):
                return api_abort(400, 'invalid filename')
            filename = secure_filename(f.filename)
            if new_message.content != filename:
                new_message.content = filename
                db.session.commit()
            f.save('static/{}/{}'.format(data['type'], str(new_message.id)+'_'+filename))

        return make_resp(message_schema(new_message))