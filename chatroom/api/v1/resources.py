from flask_restful import Resource
from flask import g, request, abort

from chatroom.extensions import db
from chatroom.models import User, Room
from chatroom.api.v1.reqparses import user_put_reqparse
from chatroom.api.v1.schemas import user_schema, users_schema, make_resp


class UserAPI(Resource):

    def get(self):
        # raise InvalidTokenError
        # from werkzeug.exceptions import NotFound
        # raise NotFound
        # the existed exceptions in werkzeug.exceptions can not be registered to a function
        if request.args.get('user', None) is not None:
            user = User.query.get_or_404(request.args.get('user'))
            data = user_schema(user, False, False, True)
        else:
            user = g.user
            data = user_schema(user)
        return make_resp(data)

    def put(self):  # sent a put request to the RoomAPI to join and leave a room
        user = g.user
        data = user_put_reqparse.parse_args()
        if data['username'] is not None:
            user.username = data['username']
        db.session.commit()
        return make_resp(user_schema(user))

    def delete(self):
        user = g.user
        data = user_schema(user)
        db.session.delete(user)
        db.session.commit()
        return make_resp(data)


class UserListAPI(Resource):

    def get(self):
        room_id = request.args.get('room', None)
        if room_id is not None:
            users = Room.query.get_or_404(room_id).users
        else:
            users = User.query.all()
        return make_resp(users_schema(users, room_id))
