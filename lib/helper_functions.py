from flask import jsonify

from db import db

from .authenticate import authenticate, authenticate_return_auth
from models.users import Users
from models.groups import Groups
from models.roles import Roles


@authenticate_return_auth
def users_group_check(user_id, auth_info):
    user_query = db.session.query(Users).filter(Users.user_id == user_id).first()

    user_groups = []
    for group in user_query.groups:
        group_query = db.session.query(Groups).filter(Groups.group_id == group.group_id).first()
        if group_query:
            user_groups.append(group_query.group_id)
        else:
            return jsonify({'message': 'no groups found'})

    return user_groups


@authenticate_return_auth
def users_role_check(user_id, auth_info):
    user_query = db.session.query(Users).filter(Users.user_id == user_id).first()

    user_roles = []
    for role in user_query.roles:
        role_query = db.session.query(Roles).filter(Roles.role_id == role.role_id).first()
        if role_query:
            user_roles.append(role_query.role_id)
        else:
            return jsonify({'message': 'no roles found'})

    return user_roles
