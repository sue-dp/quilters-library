import config
from db import db
from models.roles import Roles


def add_role_demo_data():
    for role_name in config.roles:

        new_role = db.session.query(Roles).filter(Roles.role_name == role_name).first()

        if new_role == None:
            role_name = role_name

            new_role = Roles(role_name=role_name, active=True)

            db.session.add(new_role)

    db.session.commit()
