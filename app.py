from flask import Flask
import psycopg2

from db import *
from util.blueprints import register_blueprints


app = Flask(__name__)


def create_all():
    with app.app_context():
        db.create_all()


app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://127.0.0.1:5432/quilters-library'

init_db(app, db)


def create_tables():
    with app.app_context():
        print('creating tables...')
        db.create_all()
        print('tables created successfuly')


register_blueprints(app)

if __name__ == '__main__':
    create_all()
    create_tables()
    app.run(host='0.0.0.0', port='8086', debug=True)
