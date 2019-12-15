from app import db
from models import BaseModelWithTime, QueryWithSoftDelete


class Reply(db.Model, BaseModelWithTime):
    query_class = QueryWithSoftDelete

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False, default=0)
    topic_title = db.Column(db.String(255), nullable=False, default='')
    content = db.Column(db.Text, nullable=False, default='')
    topic_id = db.Column(db.Integer, nullable=False, default=0)
    author_avatar = db.Column(db.String(255), nullable=False, default='')
    is_delete = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return '<id %r>' % self.id

    def user(self):
        from .user import User
        u = User.one(id=self.user_id)
        return u
