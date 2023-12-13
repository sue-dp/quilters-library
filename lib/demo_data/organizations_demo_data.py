import config
from db import db
from models.organizations import Organizations
from models.users import Users


def add_organization_demo_data():
    for organization_name in config.organizations:

        new_organization = db.session.query(Organizations).filter(Organizations.organization_name == organization_name).first()

        if new_organization == None:
            organization_name = organization_name

            new_organization = Organizations(organization_name=organization_name, active=True)

            db.session.add(new_organization)

    db.session.commit()


def add_users_to_organizations():
    user_list = []
    for name in config.users:
        split_name = name.split()
        first_name = split_name[0]
        user = db.session.query(Users).filter(Users.first_name == first_name).first()
        user_list.append(user)

    organization_list = []
    for organization_name in config.organizations:
        organization = db.session.query(Organizations).filter(Organizations.organization_name == organization_name).first()
        organization_list.append(organization)

    for user in user_list:
        for organization in organization_list:
            user.organizations.append(organization)

    db.session.commit()
