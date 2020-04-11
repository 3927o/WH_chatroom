from functools import wraps
from itsdangerous import JSONWebSignatureSerializer as Serializer
from flask import g

from chatroom.utils import create_user
# from chatroom.extensions import db
# from chatroom.models import User


def auth_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        user = 1
        g.user = user
        return f(*args, **kwargs)

    return decorator()


def generate_token():
    # new_user = User()
    # db.session.add(new_user)
    # db.session.commit()
    # new_user.username = 'customer' + str(new_user.id)
    # db.session.commit()
    new_user = create_user()
    s = Serializer(new_user.key)
    data = {'name': new_user.username, 'create_at': str(new_user.create_at)}
    token = str(new_user.id) + '.' + s.dumps(data).decode('ascii')
    return token
