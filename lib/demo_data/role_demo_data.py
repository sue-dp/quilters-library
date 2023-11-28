import config
from db import db
from models.roles import Roles
from models.organizations import Organizations


def add_role_demo_data():
    for role_name in config.roles:

        new_role = db.session.query(Roles).filter(Roles.role_name == role_name).first()

        if new_role == None:
            role_name = role_name

            new_role = Roles(role_name=role_name, active=True)

            db.session.add(new_role)

    db.session.commit()


def add_roles_to_org():
    role_list = []
    for role_name in config.roles:
        role = db.session.query(Roles).filter(Roles.role_name == role_name).first()
        role_list.append(role)

    org_list = []
    for org_name in config.organizations:
        org = db.session.query(Organizations).filter(Organizations.org_name == org_name).first()
        org_list.append(org)

    for org in org_list:
        org.roles.append(role_list)

    db.session.commit()
