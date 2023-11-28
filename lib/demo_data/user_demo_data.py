from flask_bcrypt import generate_password_hash

import config
from db import db
from models.users import Users
from models.roles import Roles


def add_user_demo_data():
    for name in config.users:
        split_name = name.split()
        first_name = split_name[0]
        last_name = split_name[1]

        new_user = db.session.query(Users).filter(Users.first_name == first_name).first()

        if new_user == None:
            first_name = first_name
            last_name = last_name
            email = f'{first_name.lower()}{last_name.lower()}@test.com'
            password = '1234'

            new_password = generate_password_hash(password).decode('utf8')

            new_user = Users(first_name=first_name, last_name=last_name, email=email, password=new_password)

            db.session.add(new_user)

    db.session.commit()


def add_role_to_user():
    user_list = []
    for name in config.users:
        split_name = name.split()
        first_name = split_name[0]
        user = db.session.query(Users).filter(Users.first_name == first_name).first()
        user_list.append(user)

    role_list = []
    for role_name in config.roles:
        role = db.session.query(Roles).filter(Roles.role_name == role_name).first()
        role_list.append(role)
