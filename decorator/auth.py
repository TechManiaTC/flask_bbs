from functools import wraps
from flask import request, Response
from werkzeug.exceptions import abort

from plugin.exception import UnauthorizedError
from utils import token


def token_login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not request.cookies.get('token'):
            abort(Response("请登录", status=401))
        token.get('user_id')
        return func(*args, **kwargs)

    return decorated_view
