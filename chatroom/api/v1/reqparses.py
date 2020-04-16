from flask_restful import reqparse

user_put_reqparse = reqparse.RequestParser()
user_put_reqparse.add_argument('username', type=str, location='json')
user_put_reqparse.add_argument('room_id', type=str, location='json')
user_put_reqparse.add_argument('action', choices=('join', 'leave'), type=str, location='json')
user_put_reqparse.add_argument('key', type=str, location='json')

room_put_reqparse = reqparse.RequestParser()
room_put_reqparse.add_argument('name', type=str, location='json')
room_put_reqparse.add_argument('introduce', type=str, location='json')
room_put_reqparse.add_argument('key', type=str, location='json')

room_post_reqparse = reqparse.RequestParser()
room_post_reqparse.add_argument('name', type=str, location='json')
room_post_reqparse.add_argument('introduce', type=str, location='json')
room_post_reqparse.add_argument('key', type=str, location='json')