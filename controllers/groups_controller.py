from flask import jsonify

from db import db
from models.users import Users, user_schema, users_schema
from models.groups import Groups, group_schema, groups_schema
from models.roles import Roles, role_schema, roles_schema
from models.quilts import Quilts, quilt_schema, quilts_schema
from models.images import Images, image_schema, images_schema
from models.auth_tokens import AuthTokens
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth, authenticate


def group_add(req):
    post_data = req.form if req.form else req.json

    new_group = Groups.get_new_group()
    populate_object(new_group, post_data)

    db.session.add(new_group)
    db.session.commit()

    return jsonify(group_schema.dump(new_group)), 201


@authenticate_return_auth
def groups_get_all(req, auth_info):
    groups_query = db.session.query(Groups).all()

    if auth_info.user.role == 'super-admin':
        return jsonify({'message': 'groups found', 'groups': groups_schema.dump(groups_query)}), 200
    else:
        return jsonify({'message': 'unauthorized'}), 401


@authenticate_return_auth
def group_get_by_id(req, group_id, auth_info):
    group_query = db.session.query(Groups).filter(Groups.group_id == group_id).first()

    if group_query:
        if auth_info.user.role == 'admin' or auth_info.user.role == 'super-admin' or group_id == auth_info.group.group_id:
            # make a loop to check for group_id for admin
            return jsonify({'message': 'group found', 'group': group_schema.dump(group_query)}), 200

        else:
            return jsonify({'message': 'unauthorized'}), 401
    else:
        return jsonify({'message': 'group not found'}), 404


@authenticate_return_auth
def group_delete_by_id(req, group_id, auth_info):
    if auth_info.user.role == 'admin' or auth_info.user.role == 'super-admin':
        group_query = db.session.query(Groups).filter(Groups.group_id == group_id).first()

        if group_query:
            auth_tokens = db.session.query(AuthTokens).filter(AuthTokens.group_id == group_id).all()
            for token in auth_tokens:
                db.session.delete(token)
            db.session.delete(group_query)
            db.session.commit()

            return jsonify({'message': 'record successfully deleted'}), 200

        return jsonify({'message': 'group not found'}), 404

    else:
        return jsonify({'message': 'unauthorized'}), 401


@authenticate_return_auth
def group_update(req, group_id, auth_info):
    post_data = req.form if req.form else req.json

    group_query = db.session.query(Groups).filter(Groups.group_id == group_id).first()

    if group_query:
        if auth_info.user.role == 'admin' or auth_info.user.role == 'super-admin':
            # make a loop to check for group_id
            populate_object(group_query, post_data)

            db.session.commit()

            return jsonify({'message': 'group updated', 'group': group_schema.dump(group_query)}), 200

        else:
            return jsonify({'message': 'unauthorized'}), 401

    else:
        return jsonify({'message': 'group not found'}), 404


@authenticate_return_auth
def group_add_user(req, auth_info):
    post_data = req.form if req.form else req.json
    group_id = auth_info.group.group_id
    # group_id = make loop to get group_id

    group_query = db.session.query(Groups).filter(Groups.group_id == group_id).first()
    group_query = db.session.query(Groups).filter(Groups.group_id == group_id).first()
    role_query = db.session.query(Roles).filter(Roles.role_id == role_id).first()

    if group_query and group_query:
        if auth_info.user.role == 'admin' or auth_info.user.role == 'super-admin':
            group_query.groups.append(group_query)
            db.session.commit()

            return jsonify({'message': 'product added to group', 'group': group_schema.dump(group_query)}), 201

        else:
            return jsonify({'message': 'unauthorized'}), 401

    else:
        return jsonify({'message': 'not found'}), 404


@authenticate_return_auth
def group_remove_user(req, auth_info):
    post_data = req.form if req.form else req.json
    group_id = auth_info.group.group_id
    # group_id = make loop to get group_id

    group_query = db.session.query(Groups).filter(Groups.group_id == group_id).first()
    group_query = db.session.query(Groups).filter(Groups.group_id == group_id).first()
    role_query = db.session.query(Roles).filter(Roles.role_id == role_id).first()

    if group_query and group_query:
        if auth_info.user.role == 'admin' or auth_info.user.role == 'super-admin':
            group_query.groups.append(group_query)
            db.session.commit()

            return jsonify({'message': 'product added to group', 'group': group_schema.dump(group_query)}), 201

        else:
            return jsonify({'message': 'unauthorized'}), 401

    else:
        return jsonify({'message': 'not found'}), 404


@authenticate_return_auth
def group_add_role(req, auth_info):
    post_data = req.form if req.form else req.json
    group_id = auth_info.group.group_id
    # group_id = make loop to get group_id

    group_query = db.session.query(Groups).filter(Groups.group_id == group_id).first()
    group_query = db.session.query(Groups).filter(Groups.group_id == group_id).first()
    role_query = db.session.query(Roles).filter(Roles.role_id == role_id).first()

    if group_query and group_query:
        if auth_info.user.role == 'admin' or auth_info.user.role == 'super-admin':
            group_query.groups.append(group_query)
            db.session.commit()

            return jsonify({'message': 'product added to group', 'group': group_schema.dump(group_query)}), 201

        else:
            return jsonify({'message': 'unauthorized'}), 401

    else:
        return jsonify({'message': 'not found'}), 404


@authenticate_return_auth
def group_remove_role(req, auth_info):
    post_data = req.form if req.form else req.json
    group_id = auth_info.group.group_id
    # group_id = make loop to get group_id

    group_query = db.session.query(Groups).filter(Groups.group_id == group_id).first()
    group_query = db.session.query(Groups).filter(Groups.group_id == group_id).first()
    role_query = db.session.query(Roles).filter(Roles.role_id == role_id).first()

    if group_query and group_query:
        if auth_info.user.role == 'admin' or auth_info.user.role == 'super-admin':
            group_query.groups.append(group_query)
            db.session.commit()

            return jsonify({'message': 'product added to group', 'group': group_schema.dump(group_query)}), 201

        else:
            return jsonify({'message': 'unauthorized'}), 401

    else:
        return jsonify({'message': 'not found'}), 404


@authenticate_return_auth
def group_activity(req, group_id, auth_info):
    group_query = db.session.query(Groups).filter(Groups.group_id == group_id).first()

    if group_query:
        if auth_info.user.role == 'admin' or auth_info.user.role == 'super-admin':
            group_query.active = not group_query.active

            db.session.commit()

            return jsonify({'message': 'group activity has been updated', 'group': group_schema.dump(group_query)}), 200

        else:
            return jsonify({'message': 'unauthorized'}), 401

    else:
        return jsonify({'message': 'group not found'}), 404
