from flask import url_for, jsonify, request


def make_resp(data, status=200, message='succeed'):
    resp = jsonify({
        'status': status,
        'message': message,
        'data': data
    })
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.status_code = status
    return resp


def user_schema(user, messages=True, rooms=True, parm=False):
    data = {
        'id': user.id,
        'kind': 'User',
        'self': request.host_url[0:-1]+url_for('api_v1.user'),
        'username': user.username,
        'phone': user.phone,
        'email': user.email,
        'country': user.country,
        'area': user.area,
        'avatar': request.host_url[0:-1]+url_for('avatar.get_user_avatar', uid=user.id),
        'create_at': str(user.create_at),
        'update_at': str(user.updated_at),
    }
    if messages is True:
        data['messages'] = [message_schema(message_) for message_ in user.messages]  # 加个数据个数，用字典
    if rooms is True:
        data['rooms'] = [room_schema(room, False, False) for room in user.rooms]
    if parm is True:
        data['self'] = request.host_url[0:-1]+url_for('api_v1.user', user=user.id)
    return data


def users_schema(users, room_id=None):
    data = {
        'self': request.host_url[0:-1]+url_for('api_v1.users'),
        'kind': 'UserList',
        'count': len(users),
        'users': [user_schema(user, messages=False, rooms=False) for user in users]
    }
    if room_id is not None:
        data['self'] = request.host_url[0:-1]+url_for('api_v1.users', room=room_id)  # the parm room is in url
    return data


def room_schema(room, user=True, message=True):
    data = {
        'self': request.host_url[0:-1]+url_for('api_v1.room', id_or_name=room.id),
        'kind': 'Room',
        'id': room.id,
        'name': room.name,
        'introduce': room.introduce,
        'topic': room.topic,
        'master_id': room.master_id,
        'avatar': request.host_url[0:-1]+url_for('avatar.get_room_avatar', rid=room.id),
        'create_at': room.create_at,
        'updated_at': room.updated_at
    }
    if user:
        data['users'] = [user_schema(user, messages=False, rooms=False) for user in room.users]
    if message:
        data['messages'] = [message_schema(message_) for message_ in room.messages]
    return data


def message_schema(message):
    data = {
        'self': request.host_url[0:-1]+url_for('api_v1.message', mid=message.id),
        'kind': 'Message',
        'id': message.id,
        'type': message.type,
        'author': message.author.username,  # 或许可以用user_schema?
        'room': message.room.name,  # 用room_schema?
        'content': message.content,
        'create_at': str(message.create_at),
        'updated_at': str(message.updated_at)
    }
    if data['type'] == 'file':
        data['self'] = request.host_url[0:-1]+url_for('resource_bp.get_file', fid=data['id'])
    if data['type'] == 'picture':
        data['self'] = request.host_url[0:-1]+url_for('resource_bp.get_picture', pid=data['id'])
    return data


def messages_schema(messages):
    if len(messages) == 0:
        data = {
            'self': request.host_url[0:-1]+url_for('api_v1.messages', rid_or_name=0),
            'kind': 'MessageList',
            'count': 0,
            'messages': []
        }
    else:
        data = {
            'self': request.host_url[0:-1]+url_for('api_v1.messages', rid_or_name=messages[0].room.id),
            'kind': 'MessageList',
            'count': len(messages),
            'messages': [message_schema(message) for message in messages]
        }
    return data
