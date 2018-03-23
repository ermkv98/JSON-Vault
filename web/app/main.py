from flask import Flask
from api.FileMeta.controllers import File
from api.FileMeta.models import db as file_db


app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['json'])

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://test:test@db/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'you-will-never-guess'


with app.app_context():
    file_db.init_app(app)
    file_db.create_all()

app.register_blueprint(File, url_prefix='/File')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
