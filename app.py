from flask import Flask
from flask_bcrypt import generate_password_hash
import psycopg2

from db import *
import config
from models.groups import Groups
from models.roles import Roles
from models.users import Users
from models.quilts import Quilts
from util.blueprints import register_blueprints
from lib.demo_data.demo_data import run_demo_data


app = Flask(__name__)


def create_all():
    with app.app_context():
        db.create_all()

        print(f"Querying for {config.group_name} group...")
        group_data = db.session.query(Groups).filter(Groups.group_name == config.group_name).first()

        if group_data == None:
            print(f"{config.group_name} group not found. Creating {config.group_name} Group in database...")
            group_data = Groups(group_name=config.group_name, active=True)

            db.session.add(group_data)
            db.session.commit()

        else:
            print(f"{config.group_name} Group found!")

        print(f'Querying for Roles for {group_data.group_name}...')
        role_data = db.session.query(Roles).filter(Roles.group_id == group_data.group_id).first()

        if role_data == None:
            print(f'Roles for {group_data.group_name} not found! Creating roles...')

            role_data = Roles(role_name='super-admin', group_id=group_data.group_id, active=True)

            db.session.add(role_data)
            db.session.commit()

        else:
            print(f'Found {group_data.group_name} Roles!')

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

            record.groups.append(group_data)
            record.roles.append(role_query)

            db.session.commit()

        else:
            print(f"{su_name} user found!")

        run_demo_data()


app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://127.0.0.1:5432/quilters-library'

init_db(app, db)


# def create_tables():
#     with app.app_context():
#         print('creating tables...')
#         db.create_all()
#         print('tables created successfuly')


register_blueprints(app)

if __name__ == '__main__':
    # create_tables()
    create_all()
    app.run(host='0.0.0.0', port='8086', debug=True)
