from flask import jsonify

from db import db

from .authenticate import authenticate, authenticate_return_auth
from models.users import Users
from models.organizations import Organizations
from models.roles import Roles


@authenticate_return_auth
def users_organization_check(user_id, auth_info):
    user_query = db.session.query(Users).filter(Users.user_id == user_id).first()

    user_organizations = []
    for organization in user_query.organizations:
        organization_query = db.session.query(Organizations).filter(Organizations.organization_id == organization.organization_id).first()
        if organization_query:
            user_organizations.append(organization_query.organization_id)
        else:
            return jsonify({'message': 'no organizations found'})

    return user_organizations


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
