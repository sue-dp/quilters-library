from flask import jsonify

from db import db
from models.users import Users, user_schema, users_schema
from models.organizations import Organizations, organization_schema, organizations_schema
from models.roles import Roles, role_schema, roles_schema
from models.quilts import Quilts, quilt_schema, quilts_schema
from models.images import Images, image_schema, images_schema
from models.auth_tokens import AuthTokens
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth, authenticate


@authenticate_return_auth
def role_add(req, auth_info):
    post_data = req.form if req.form else req.json

    new_role = Roles.get_new_role()
    populate_object(new_role, post_data)

    db.session.add(new_role)
    db.session.commit()

    return jsonify(role_schema.dump(new_role)), 201


@authenticate_return_auth
def roles_get_all(req, auth_info):
    roles_query = db.session.query(Roles).all()

    if auth_info.role.role == 'admin' or auth_info.role.role == 'super-admin':
        return jsonify({'message': 'roles found', 'roles': roles_schema.dump(roles_query)}), 200
    else:
        return jsonify({'message': 'unauthorized'}), 401


@authenticate_return_auth
def role_get_by_id(req, role_id, auth_info):
    role_query = db.session.query(Roles).filter(Roles.role_id == role_id).first()

    if role_query:
        if auth_info.role.role == 'admin' or auth_info.role.role == 'super-admin' or role_id == auth_info.role.role_id:
            # make a loop to check for org_id for admin
            return jsonify({'message': 'role found', 'role': role_schema.dump(role_query)}), 200

        else:
            return jsonify({'message': 'unauthorized'}), 401
    else:
        return jsonify({'message': 'role not found'}), 404


@authenticate_return_auth
def role_delete_by_id(req, role_id, auth_info):
    if auth_info.role.role_id == role_id or auth_info.role.role == 'super-admin':
        role_query = db.session.query(Roles).filter(Roles.role_id == role_id).first()

        if role_query:
            auth_tokens = db.session.query(AuthTokens).filter(AuthTokens.role_id == role_id).all()
            for token in auth_tokens:
                db.session.delete(token)
            db.session.delete(role_query)
            db.session.commit()

            return jsonify({'message': 'record successfully deleted'}), 200

        return jsonify({'message': 'role not found'}), 404

    else:
        return jsonify({'message': 'unauthorized'}), 401


@authenticate_return_auth
def role_update(req, role_id, auth_info):
    post_data = req.form if req.form else req.json

    role_query = db.session.query(Roles).filter(Roles.role_id == role_id).first()

    if role_query:
        if auth_info.role.role == 'admin' or auth_info.role.role == 'super-admin' or role_id == auth_info.role.role_id:
            # make a loop to check for org_id
            populate_object(role_query, post_data)

            db.session.commit()

            return jsonify({'message': 'role updated', 'role': role_schema.dump(role_query)}), 200

        else:
            return jsonify({'message': 'unauthorized'}), 401

    else:
        return jsonify({'message': 'role not found'}), 404


@authenticate_return_auth
def role_activity(req, role_id, auth_info):
    role_query = db.session.query(Roles).filter(Roles.role_id == role_id).first()

    if role_query:
        if auth_info.role.role == 'admin' or auth_info.role.role == 'super-admin':
            role_query.active = not role_query.active

            db.session.commit()

            return jsonify({'message': 'role activity has been updated', 'role': role_schema.dump(role_query)}), 200

        else:
            return jsonify({'message': 'unauthorized'}), 401

    else:
        return jsonify({'message': 'role not found'}), 404
