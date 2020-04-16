from flask_restful import reqparse

user_put_reqparse = reqparse.RequestParser()
user_put_reqparse.add_argument('username', type=str, location='json')
