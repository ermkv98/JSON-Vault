from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from ..BaseEntity.models import BaseEntity


db = SQLAlchemy()
ma = Marshmallow()


class FileMeta(db.Model, BaseEntity):
    weight = db.Column(db.Float(precision=2, decimal_return_scale=True))
    protected = db.Column(db.Boolean, default=False)
    password = db.Column(db.String(128))

    def __init__(self, link, weight, protected, password):
        self.password = password
        self.weight = weight
        self.protected = protected
        self.link = link


class FileMetaSchema(ma.Schema):
    class Meta:
        fields = ('link', 'weight', 'protected')
        model = FileMeta


file_meta_schema = FileMetaSchema()
