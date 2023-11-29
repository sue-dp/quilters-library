from flask import Flask
from flask_bcrypt import generate_password_hash
import psycopg2

from db import *
import config
from models.organizations import Organizations
from models.roles import Roles
from models.users import Users
from util.blueprints import register_blueprints
from lib.demo_data.demo_data import run_demo_data


app = Flask(__name__)


def create_all():
    with app.app_context():
        db.create_all()

        print(f"Querying for {config.org_name} organization...")
        org_data = db.session.query(Organizations).filter(Organizations.org_name == config.org_name).first()

        if org_data == None:
            print(f"{config.org_name} organization not found. Creating {config.org_name} Organization in database...")
            org_data = Organizations(org_name=config.org_name, active=True)

            db.session.add(org_data)
            db.session.commit()

        else:
            print(f"{config.org_name} Organization found!")

        print(f'Querying for Roles for {org_data.org_name}...')
        role_data = db.session.query(Roles).filter(Roles.org_id == org_data.org_id).first()

        if role_data == None:
            print(f'Roles for {org_data.org_name} not found! Creating roles...')

            role_data = Roles(role_name='super-admin', org_id=org_data.org_id, active=True)

            db.session.add(role_data)
            db.session.commit()

        else:
            print(f'Found {org_data.org_name} Roles!')

        su_name = f'{config.su_first_name} {config.su_last_name}'
        print(f"Querying for {su_name} user...")
        user_data = db.session.query(Users).filter(Users.email == config.su_email).first()

        if user_data == None:
            print(f'{su_name} not found! Creating {config.su_email} user...')

            new_pw = input(f' Enter password for {su_name}: ')
            hashed_password = generate_password_hash(new_pw).decode('utf8')

            role_query = db.session.query(Roles).filter(Roles.role_name == 'super-admin').first()

            record = Users(first_name=config.su_first_name, last_name=config.su_last_name, email=config.su_email, password=hashed_password, active=True)

            db.session.add(record)

            record.roles.append(role_query)

            db.session.commit()

        else:
            print(f"{su_name} user found!")

        run_demo_data()


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
