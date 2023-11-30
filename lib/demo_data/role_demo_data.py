import config
from db import db
from models.roles import Roles
from models.users import Users
from models.groups import Groups


def add_roles_to_group():
    groups = db.session.query(Groups).all()

    for group in groups:
        group_roles = db.session.query(Roles).filter(Roles.group_id == group.group_id).all()

        if group_roles == []:
            for role in config.roles:
                role_name = role
                group_id = group.group_id

                new_role = Roles(role_name=role_name, active=True, group_id=group_id)

                db.session.add(new_role)

    db.session.commit()


def add_roles_to_users():

    for group in config.groups:
        group_data = db.session.query(Groups).filter(Groups.group_name == group).first()

        admin_role = db.session.query(Roles).filter(Roles.group_id == group_data.group_id).filter(Roles.role_name == 'admin').first()
        user_role = db.session.query(Roles).filter(Roles.group_id == group_data.group_id).filter(Roles.role_name == 'user').first()

        for user in group_data.users:
            user_roles = user.roles
            first_name = user.first_name

            if first_name == 'Sue':
                user_roles.append(admin_role)

            else:
                user_roles.append(user_role)

    db.session.commit()
