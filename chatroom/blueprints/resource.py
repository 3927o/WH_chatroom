from flask import Blueprint, send_from_directory
from chatroom.models import Message

resource_bp = Blueprint('resource_bp', __name__, static_folder='/static')


@resource_bp.errorhandler(404)
def not_found():
    pass


@resource_bp.route('/pictures/<int:pid>')
def get_picture(pid):
    message = Message.query.get_or_404(pid)
    return send_from_directory('static/picture', str(pid)+'_'+message.content)


@resource_bp.route('/files/<int:fid>')
def get_file(fid):
    message = Message.query.get_or_404(fid)
    return send_from_directory('static/file', str(fid)+'_'+message.content)
