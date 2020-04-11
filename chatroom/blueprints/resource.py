from flask import Blueprint, send_from_directory
# from chatroom.models import Message

resource_bp = Blueprint('resource', __name__, static_folder='/static')


@resource_bp.errorhandler(404)
def not_found():
    pass


@resource_bp.route('/pictures/<int:id>')
def get_picture(id):
    from chatroom.models import Message
    message = Message.query.get_or_404(id)  # 影响速度
    return send_from_directory('static/pictures', str(id)+message.content)


@resource_bp.route('/files/<int:id>')
def get_file(id):
    from chatroom.models import Message
    message = Message.query.get_or_404(id)
    return send_from_directory('static/files', str(id)+message.content)
