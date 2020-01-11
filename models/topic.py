from app import db
from models.user import User
from models import BaseModelWithTime, QueryWithSoftDelete


class Topic(db.Model, BaseModelWithTime):
    query_class = QueryWithSoftDelete

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, default='')
    views = db.Column(db.Integer, nullable=False, default=0)
    content = db.Column(db.Text, nullable=False, default='')
    user_id = db.Column(db.Integer, nullable=False, default=0)
    board_id = db.Column(db.Integer, nullable=False, default=0)
    author = db.Column(db.String(255), nullable=False, default='')
    is_delete = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return '<id %r>' % self.id

    @classmethod
    def find(cls, id):
        m = cls.one(id=id)
        m.views += 1
        m.save()
        return m

    def replies(self):
        from .reply import Reply
        ms = Reply.all(topic_id=self.id)
        return ms

    def board(self):
        from .board import Board
        m = Board.one(id=self.board_id)
        return m

    def user(self):
        u = User.one(id=self.user_id)
        return u
