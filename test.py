from flask import Flask, g, request, make_response, redirect
from functools import wraps

app = Flask(__name__)


def test():
    return '2333hhhhhhhhhhhhhh'


app.before_request(test)


# def test_auth(f):
#     @wraps(f)
#     def decorator(*args, **kwargs):
#         cookies = request.cookies.get('key', None)
#         if cookies is None:
#             resp = make_response(redirect(request.url))
#             resp.set_cookie('key', '123')
#             return resp
#         return f(*args, **kwargs)
#
#     return decorator


@app.route('/')
# @test_auth
def index():
    return "2333"


if __name__ == '__main__':
    app.run(port=80, debug=True)


