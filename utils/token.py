from flask import request, current_app
from werkzeug.exceptions import abort

from plugin.exception import UnauthorizedError
import jwt
import time


def parse_token(token):
    res = parse_token_without_expire(token)
    if res['expire_time'] < time.time():
        UnauthorizedError('token已过期')
    return res


def parse_token_without_expire(token):
    if not token:
        raise UnauthorizedError('请在登陆后访问')
    key = current_app.config['JWT_KEY']
    try:
        res = jwt.decode(token, key, algorithm='HS256')
    except Exception as e:
        raise UnauthorizedError('token无效')
    return res


def get_from_token(key, token, default=None):
    token_data = parse_token_without_expire(token)
    return token_data.get(key, default)


def encryption_set(data):
    key = current_app.config['JWT_KEY']
    timeout = current_app.config['JWT_TIMEOUT']
    jwt.leeway = 60
    data['expire_time'] = time.time() + timeout
    res = jwt.encode(data, key, algorithm='HS256')
    return res


def get(key, default=None):
    token = request.cookies.get('token')
    if not token:
        raise UnauthorizedError('请在登陆后访问')
    token_data = parse_token(token)
    return token_data.get(key, default)


def refresh():
    token = request.cookies.get('token')
    if not token:
        raise UnauthorizedError('请在登陆后访问')
    token_data = parse_token_without_expire(token)
    return encryption_set(token_data)

