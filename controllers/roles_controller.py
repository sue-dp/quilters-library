from flask import jsonify

from db import db
from models.users import Users
from models.groups import Groups
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
def roles_get_by_group_id(req, group_id, auth_info):
    auth_user_query = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()
    super_role_query = db.session.query(Roles).filter(Roles.role_name == 'super-admin').first()
    group_query = db.session.query(Groups).filter(Groups.group_id == group_id).first()
    roles_query = db.session.query(Roles).filter(Roles.group_id == group_id).all()

    if super_role_query in auth_user_query.roles:

        return jsonify({'message': 'roles found', 'roles': roles_schema.dump(roles_query)}), 200

    if group_query in auth_user_query.groups:
        if auth_user_query.roles == 'admin':

            return jsonify({'message': 'roles found', 'roles': roles_schema.dump(roles_query)}), 200

    else:
        return jsonify({'message': 'unauthorized'}), 401


@authenticate_return_auth
def role_get_by_id(req, role_id, auth_info):
    auth_user_query = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()
    super_role_query = db.session.query(Roles).filter(Roles.role_name == 'super-admin').first()
    role_query = db.session.query(Roles).filter(Roles.role_id == role_id).first()
    group_query = db.session.query(Groups).filter(Groups.group_id == role_query.group_id).first()

    if super_role_query in auth_user_query.roles:

        return jsonify({'message': 'role found', 'role': role_schema.dump(role_query)}), 200

    if role_query.group_id == group_query.group_id:
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

        return jsonify({'message': 'role activity has been updated', 'group': role_schema.dump(role_query)}), 200

    # for group in auth_user_query.groups:
    #     admin_role_query = db.session.query(Roles).filter(Roles.group_id == group.group_id).filter(Roles.role_name == 'admin').first()
    #     if group in role_query.groups:
    #         if admin_role_query in auth_user_query.roles:
    #             role_query.active = not role_query.active

    #             db.session.commit()

    #             return jsonify({'message': 'role activity has been updated', 'role': role_schema.dump(role_query)}), 200

    else:
        return jsonify({'message': 'unauthorized'}), 401
