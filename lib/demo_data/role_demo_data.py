import config
from db import db
from models.roles import Roles
from models.users import Users
from models.organizations import Organizations


def add_roles_to_org():
    orgs = db.session.query(Organizations).all()

    for org in orgs:
        org_roles = db.session.query(Roles).filter(Roles.org_id == org.org_id).all()

        if org_roles == []:
            for role in config.roles:
                role_name = role
                org_id = org.org_id

                new_role = Roles(role_name=role_name, active=True, org_id=org_id)

                db.session.add(new_role)

    db.session.commit()


def add_roles_to_users():
    orgs = db.session.query(Organizations).all()

    for org in orgs:
        admin_role = db.session.query(Roles).filter(Roles.org_id == org.org_id).filter(Roles.role_name == 'admin').first()
        user_role = db.session.query(Roles).filter(Roles.org_id == org.org_id).filter(Roles.role_name == 'user').first()

        for user in org.users:
            user_roles = user.roles
            first_name = user.first_name

            if first_name == 'Sue':
                user_roles.append(admin_role)

            else:
                user_roles.append(user_role)

    db.session.commit()
