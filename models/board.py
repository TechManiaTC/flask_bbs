from app import db
from models import BaseModelWithTime, QueryWithSoftDelete


class Board(db.Model, BaseModelWithTime):
    query_class = QueryWithSoftDelete

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, default='')
    is_delete = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return '<id %r>' % self.id

