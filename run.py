from chatroom import creat_app
from chatroom.extensions import db

app = creat_app('testing')
ctx = app.test_request_context()
ctx.push()
db.create_all()


if __name__ == '__main__':
    app.run('127.0.0.1', port=80, debug=True)
