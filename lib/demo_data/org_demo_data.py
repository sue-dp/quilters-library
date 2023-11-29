import config
from db import db
from models.organizations import Organizations
from models.users import Users


def add_org_demo_data():
    for org_name in config.organizations:

        new_org = db.session.query(Organizations).filter(Organizations.org_name == org_name).first()

        if new_org == None:
            org_name = org_name

            new_org = Organizations(org_name=org_name, active=True)

            db.session.add(new_org)

    db.session.commit()


def add_users_to_orgs():
    user_list = []
    for name in config.users:
        split_name = name.split()
        first_name = split_name[0]
        user = db.session.query(Users).filter(Users.first_name == first_name).first()
        user_list.append(user)

    org_list = []
    for org_name in config.organizations:
        org = db.session.query(Organizations).filter(Organizations.org_name == org_name).first()
        org_list.append(org)

    for user in user_list:
        for org in org_list:
            user.organizations.append(org)

    db.session.commit()
