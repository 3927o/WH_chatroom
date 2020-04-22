from chatroom.models import Room, User
from chatroom.api.v1.errors import NameExistedError


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
    if obj_name == 'room' and Room.query.filter_by(name=name) is not None:
        raise NameExistedError
    if obj_name == 'user' and User.query.filter_by(username=name) is not None:
        raise NameExistedError
