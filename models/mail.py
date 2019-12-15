from app import db
from models import BaseModelWithTime, QueryWithSoftDelete


class Mail(db.Model, BaseModelWithTime):
    query_class = QueryWithSoftDelete

    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, nullable=False, default=0)
    title = db.Column(db.String(255), nullable=False, default='')
    content = db.Column(db.Text, nullable=False, default='')
    sender_id = db.Column(db.Integer, nullable=False, default=0)
    receiver_id = db.Column(db.Integer, nullable=False, default=0)
    sender_user = db.Column(db.String(255), nullable=False, default='')
    receiver_user = db.Column(db.String(255), nullable=False, default='')
    is_delete = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return '<id %r>' % self.id

