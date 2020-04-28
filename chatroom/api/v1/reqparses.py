from flask_restful import reqparse

user_put_reqparse = reqparse.RequestParser()
user_put_reqparse.add_argument('username', type=str)
user_put_reqparse.add_argument('phone', type=str)
user_put_reqparse.add_argument('email', type=str)
user_put_reqparse.add_argument('country', type=str)
user_put_reqparse.add_argument('area', type=str)
user_put_reqparse.add_argument('room_id', type=str, location='json')
user_put_reqparse.add_argument('action', choices=('join', 'leave'), type=str, location='json')
user_put_reqparse.add_argument('key', type=str, location='json')
user_put_reqparse.add_argument('name', type=str, location='json')

room_put_reqparse = reqparse.RequestParser()
room_put_reqparse.add_argument('name', type=str, location='json')
room_put_reqparse.add_argument('introduce', type=str, location='json')
room_put_reqparse.add_argument('key', type=str, location='json')
room_put_reqparse.add_argument('topic', type=str, location='json')

room_post_reqparse = reqparse.RequestParser()
room_post_reqparse.add_argument('name', type=str)
room_post_reqparse.add_argument('introduce', type=str)
room_post_reqparse.add_argument('key', type=str)
room_post_reqparse.add_argument('topic', type=str)

message_post_reqparse = reqparse.RequestParser()
message_post_reqparse.add_argument('type', choices=('text', 'file', 'picture'),
                                   type=str, required=True)
message_post_reqparse.add_argument('content', type=str, required=True)
