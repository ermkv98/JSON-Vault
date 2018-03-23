from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class BaseEntity():
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(32), unique=True)
