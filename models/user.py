import hashlib

from app import db
from models import BaseModelWithTime


class User(db.Model, BaseModelWithTime):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, default='')
    password = db.Column(db.String(255), nullable=False, default='')
    user_image = db.Column(db.String(255), nullable=False, default='')
    signature = db.Column(db.String(255), nullable=False, default='')
    is_delete = db.Column(db.Boolean, nullable=False, default=False)

    @staticmethod
    def salted_password(password, salt='$!@><?>HUI&DWQa`'):
        def sha256(ascii_str):
            return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()

        hash1 = sha256(password)
        hash2 = sha256(hash1 + salt)
        return hash2

    @staticmethod
    def hashed_password(pwd):
        # 用 ascii 编码转换成 bytes 对象
        p = pwd.encode('ascii')
        s = hashlib.sha256(p)
        # 返回摘要字符串
        return s.hexdigest()

    @classmethod
    def register(cls, form):
        name = form.get('username', '')
        password = form.get('password', '')
        if len(name) > 2 and User.one(username=name) is None:
            password = User.salted_password(password)
            u = User.new(dict(
                username=name,
                password=password,
            ))
            return u
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        u = User.one(username=form.get('username', ''))
        if u is not None:
            print('first', u.password, 'second', User.salted_password(form['password']))
            if u.password == User.salted_password(form['password']):
                return u
            else:
                return None
        else:
            return None

    def __repr__(self):
        return '<id %r>' % self.id
