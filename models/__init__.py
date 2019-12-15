import datetime

from flask_sqlalchemy import BaseQuery

from app import db


class BaseModel:

    @classmethod
    def valid_names(cls):
        names = [
            # (字段名, 类型, 默认值)
            ('is_delete', bool, False),
        ]
        return names

    @classmethod
    def all(cls, **kwargs):
        query = cls.query
        if kwargs:
            query = query.filter_by(**kwargs)
        objects = query.all()
        return objects

    @classmethod
    def one(cls, **kwargs):
        objects = cls.all(**kwargs)
        if len(objects) > 0:
            return objects[0]
        else:
            return None

    @classmethod
    def assemble(cls, form, **kwargs):
        m = cls()

        for name in cls.valid_names():
            k, t, v = name
            if k in form:
                setattr(m, k, t(form[k]))
            else:
                # 设置默认值
                setattr(m, k, v)

        # 处理额外的参数 kwargs
        for k, v in kwargs.items():
            if hasattr(m, k):
                setattr(m, k, v)
            else:
                raise KeyError

        return m

    @classmethod
    def new(cls, form, **kwargs):
        o = cls.assemble(form, **kwargs)
        o.save()
        return o

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def soft_delete(self):
        self.is_delete = True
        self.save()
        return self

    def update(self, data):
        o = self.__class__.new(data)
        o.save()

    def json(self):
        d = self.__dict__
        return d

    def __repr__(self):
        class_name = self.__class__.__name__
        properties = ('{0} = {1}'.format(k, v) for k, v in self.__dict__.items())
        return '<{0}: \n  {1}\n>'.format(class_name, '\n  '.join(properties))


class BaseModelWithTime(BaseModel):
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)


class QueryWithSoftDelete(BaseQuery):
    _with_deleted = False

    def __new__(cls, *args, **kwargs):
        obj = super(QueryWithSoftDelete, cls).__new__(cls)
        obj._with_deleted = kwargs.pop('_with_deleted', False)
        if len(args) > 0:
            super(QueryWithSoftDelete, obj).__init__(*args, **kwargs)
            return obj.filter_by(is_delete=False) if not obj._with_deleted else obj
        return obj

    def __init__(self, *args, **kwargs):
        pass

    def with_deleted(self):
        return self.__class__(db.class_mapper(self._mapper_zero().class_),
                              session=db.session(), _with_deleted=True)

    def _get(self, *args, **kwargs):
        # this calls the original query.get function from the base class
        return super(QueryWithSoftDelete, self).get(*args, **kwargs)

    def get(self, *args, **kwargs):
        # the query.get method does not like it if there is a filter clause
        # pre-loaded, so we need to implement it using a workaround
        obj = self.with_deleted()._get(*args, **kwargs)
        return obj if obj is None or self._with_deleted or not obj.is_delete else None
