from flask import Blueprint, send_from_directory, request, redirect, url_for

avatar_bp = Blueprint('avatar', __name__)


@avatar_bp.route('/room/<int:rid>', methods=['GET', 'POST'])
def get_room_avatar(rid):
    if request.method == "GET":
        return send_from_directory('static/avatars/room', str(rid)+'.png')
    else:
        if 'avatar' in request.files:
            f = request.files['avatar']
            f.save('chatroom/static/avatars/room/{}.png'.format(rid))
        return redirect(url_for('api_v1.room', id_or_name=rid))


@avatar_bp.route('/user/<int:uid>', methods=['GET', 'POST'])
def get_user_avatar(uid):
    if request.method == 'GET':
        return send_from_directory('static/avatars/user', str(uid)+'.png')
    else:
        if 'avatar' in request.files:
            f = request.files['avatar']
            f.save('chatroom/static/avatars/user/{}.png'.format(uid))
        return redirect(url_for('api_v1.user'))