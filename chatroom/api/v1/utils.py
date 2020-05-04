from flask import request, g

from chatroom.api.v1.schemas import make_resp, messages_schema
from chatroom.models import Room, User, Message
from chatroom.api.v1.errors import NameExistedError, api_abort, PermissionDenied
from chatroom.api.v1.auth import generate_token


def get_room(id_or_name):
    try:
        id = int(id_or_name)
        room = Room.query.get_or_404(id)
    except ValueError:
        room = Room.query.filter_by(name=id_or_name).first_or_404()
    return room


def allowed_file(filename):
    return filename.rsplit('.', 1)[1] not in ['php', 'html']


def secure_filename(filename):
    filename = filename.replace(' ', '_')
    filename = filename.replace('/', '_')
    return filename


def check_name(obj_name, name):
    if obj_name == 'room' and Room.query.filter_by(name=name).first() is not None:
        raise NameExistedError
    if obj_name == 'user' and User.query.filter_by(username=name).first() is not None:
        raise NameExistedError


def search():
    q = request.args.get('q', None)
    rid = request.args.get('rid', None)
    if q is None or rid is None:
        return api_abort(400, 'parm missing')
    room = Room.query.get_or_404(rid)
    if g.user not in room.users:
        raise PermissionDenied
    messages = Message.query.filter_by(room_id=rid).whooshee_search(q).all()
    if messages is None:
        return "None"
    return make_resp(messages_schema(messages))


def get_token():
    return generate_token()