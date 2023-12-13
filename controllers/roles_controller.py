from flask import jsonify

from db import db
from models.users import Users
from models.organizations import Organizations
from models.roles import Roles, role_schema, roles_schema
from models.auth_tokens import AuthTokens
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth


@authenticate_return_auth
def role_add(req, auth_info):
    post_data = req.form if req.form else req.json

    auth_user_query = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()
    super_role_query = db.session.query(Roles).filter(Roles.role_name == 'super-admin').first()

    if super_role_query in auth_user_query.roles:

        new_role = Roles.get_new_role()
        populate_object(new_role, post_data)

        db.session.add(new_role)
        db.session.commit()

        return jsonify(role_schema.dump(new_role)), 201

    return jsonify({'message': 'unauthorized'}), 201


@authenticate_return_auth
def roles_get_all(req, auth_info):
    auth_user_query = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()
    super_role_query = db.session.query(Roles).filter(Roles.role_name == 'super-admin').first()

    if super_role_query in auth_user_query.roles:
        roles_query = db.session.query(Roles).all()

        return jsonify({'message': 'roles found', 'roles': roles_schema.dump(roles_query)}), 200

    else:
        return jsonify({'message': 'unauthorized'}), 401


@authenticate_return_auth
def roles_get_by_organization_id(req, organization_id, auth_info):
    auth_user_query = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()
    super_role_query = db.session.query(Roles).filter(Roles.role_name == 'super-admin').first()
    organization_query = db.session.query(Organizations).filter(Organizations.organization_id == organization_id).first()
    roles_query = db.session.query(Roles).filter(Roles.organization_id == organization_id).all()

    if super_role_query in auth_user_query.roles:

        return jsonify({'message': 'roles found', 'roles': roles_schema.dump(roles_query)}), 200

    if organization_query in auth_user_query.organizations:
        if auth_user_query.roles == 'admin':

            return jsonify({'message': 'roles found', 'roles': roles_schema.dump(roles_query)}), 200

    else:
        return jsonify({'message': 'unauthorized'}), 401


@authenticate_return_auth
def role_get_by_id(req, role_id, auth_info):
    auth_user_query = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()
    super_role_query = db.session.query(Roles).filter(Roles.role_name == 'super-admin').first()
    role_query = db.session.query(Roles).filter(Roles.role_id == role_id).first()
    organization_query = db.session.query(Organizations).filter(Organizations.organization_id == role_query.organization_id).first()

    if super_role_query in auth_user_query.roles:

        return jsonify({'message': 'role found', 'role': role_schema.dump(role_query)}), 200

    if role_query.organization_id == organization_query.organization_id:
        if auth_user_query.roles == 'admin':

            return jsonify({'message': 'role found', 'role': role_schema.dump(role_query)}), 200

    else:
        return jsonify({'message': 'unauthorized'}), 401


@authenticate_return_auth
def role_delete_by_id(req, role_id, auth_info):
    auth_user_query = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()
    super_role_query = db.session.query(Roles).filter(Roles.role_name == 'super-admin').first()
    role_query = db.session.query(Roles).filter(Roles.role_id == role_id).first()

    if super_role_query in auth_user_query.roles:

        db.session.delete(role_query)
        db.session.commit()

        return jsonify({'message': 'role successfully deleted'}), 200

    else:
        return jsonify({'message': 'unauthorized'}), 401


@authenticate_return_auth
def role_update(req, role_id, auth_info):
    post_data = req.form if req.form else req.json

    auth_user_query = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()
    super_role_query = db.session.query(Roles).filter(Roles.role_name == 'super-admin').first()
    role_query = db.session.query(Roles).filter(Roles.role_id == role_id).first()

    if role_query:
        if super_role_query in auth_user_query.roles:
            populate_object(role_query, post_data)

            db.session.commit()

            return jsonify({'message': 'role updated', 'role': role_schema.dump(role_query)}), 200

        else:
            return jsonify({'message': 'unauthorized'}), 401

    else:
        return jsonify({'message': 'role not found'}), 404


@authenticate_return_auth
def role_activity(req, role_id, auth_info):
    auth_user_query = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()
    super_role_query = db.session.query(Roles).filter(Roles.role_name == 'super-admin').first()
    role_query = db.session.query(Roles).filter(Roles.role_id == role_id).first()

    if super_role_query in auth_user_query.roles:
        role_query.active = not role_query.active

        db.session.commit()

        return jsonify({'message': 'role activity has been updated', 'organization': role_schema.dump(role_query)}), 200

    # for organization in auth_user_query.organizations:
    #     admin_role_query = db.session.query(Roles).filter(Roles.organization_id == organization.organization_id).filter(Roles.role_name == 'admin').first()
    #     if organization in role_query.organizations:
    #         if admin_role_query in auth_user_query.roles:
    #             role_query.active = not role_query.active

    #             db.session.commit()

    #             return jsonify({'message': 'role activity has been updated', 'role': role_schema.dump(role_query)}), 200

    else:
        return jsonify({'message': 'unauthorized'}), 401
