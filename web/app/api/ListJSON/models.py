from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from ..BaseEntity.models import BaseEntity

db = SQLAlchemy()
ma = Marshmallow()


class ListJSON(db.Model, BaseEntity):
    files = db.relationship('file_meta',
                            backref='listed',
                            lazy='dynamic')


class ListJSONSchema(ma.Schema):
    class Meta:
        fields = ('files', 'url')
        model = ListJSON


list_schema = ListJSONSchema()
