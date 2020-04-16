from chatroom.models import Room


def get_room(id_or_name):
    try:
        id = int(id_or_name)
        room = Room.query.get_or_404(id)
    except ValueError:
        room = Room.query.filter_by(name=id_or_name).first_or_404()
    return room