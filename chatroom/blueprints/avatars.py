from flask import Blueprint,send_from_directory, request

avatar_bp = Blueprint('avatar', __name__)


@avatar_bp.route('/room/<int:rid>', methods=['GET', 'POST'])
def get_room_avatar(rid):
    if request.method == "GET":
        return send_from_directory('static/avatars/room', str(rid)+'.png')
    else:
        f = request.files['avatar']
        f.save('static/avatars/room/{}.png'.format(rid))


@avatar_bp.route('/user/<int:uid>', methods=['GET', 'POST'])
def get_user_avatar(uid):
    if request.method == 'GET':
        return send_from_directory('static/avatars/user', str(uid)+'.png')
    else:
        f = request.files['avatar']
        f.save('static/avatars/user/{}.png'.format(uid))