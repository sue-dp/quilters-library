import config
from db import db
from models.roles import Roles
from models.users import Users
from models.organizations import Organizations


def add_roles_to_organization():
    organizations = db.session.query(Organizations).all()

    for organization in organizations:
        organization_roles = db.session.query(Roles).filter(Roles.organization_id == organization.organization_id).all()

        if organization_roles == []:
            for role in config.roles:
                role_name = role
                organization_id = organization.organization_id

                new_role = Roles(role_name=role_name, active=True, organization_id=organization_id)

                db.session.add(new_role)

    db.session.commit()


def add_roles_to_users():

    for organization in config.organizations:
        organization_data = db.session.query(Organizations).filter(Organizations.organization_name == organization).first()

        admin_role = db.session.query(Roles).filter(Roles.organization_id == organization_data.organization_id).filter(Roles.role_name == 'admin').first()
        user_role = db.session.query(Roles).filter(Roles.organization_id == organization_data.organization_id).filter(Roles.role_name == 'user').first()

        for user in organization_data.users:
            user_roles = user.roles
            first_name = user.first_name

            if first_name == 'Sue':
                user_roles.append(admin_role)

            else:
                user_roles.append(user_role)

    db.session.commit()
