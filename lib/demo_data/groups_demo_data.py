import config
from db import db
from models.groups import Groups
from models.users import Users


def add_group_demo_data():
    for group_name in config.groups:

        new_group = db.session.query(Groups).filter(Groups.group_name == group_name).first()

        if new_group == None:
            group_name = group_name

            new_group = Groups(group_name=group_name, active=True)

            db.session.add(new_group)

    db.session.commit()


def add_users_to_groups():
    user_list = []
    for name in config.users:
        split_name = name.split()
        first_name = split_name[0]
        user = db.session.query(Users).filter(Users.first_name == first_name).first()
        user_list.append(user)

    group_list = []
    for group_name in config.groups:
        group = db.session.query(Groups).filter(Groups.group_name == group_name).first()
        group_list.append(group)

    for user in user_list:
        for group in group_list:
            user.groups.append(group)

    db.session.commit()
