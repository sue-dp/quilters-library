from flask import jsonify

from db import db
from models.users import Users
from models.groups import Groups, group_schema, groups_schema
from models.roles import Roles
from models.auth_tokens import AuthTokens
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth, authenticate


@authenticate
def group_add(req):
    post_data = req.form if req.form else req.json

    new_group = Groups.get_new_group()
    populate_object(new_group, post_data)

    db.session.add(new_group)
    db.session.commit()

    return jsonify(group_schema.dump(new_group)), 201


@authenticate_return_auth
def groups_get_all(req, auth_info):
    role_query = db.session.query(Roles).filter(Roles.role_name == 'super-admin').first()
    auth_user_query = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()

    if role_query in auth_user_query.roles:
        groups_query = db.session.query(Groups).all()

        return jsonify({'message': 'groups found', 'groups': groups_schema.dump(groups_query)}), 200

    else:
        return jsonify({'message': 'unauthorized'}), 401


@authenticate_return_auth
def group_get_by_id(req, group_id, auth_info):
    auth_user_query = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()
    super_role_query = db.session.query(Roles).filter(Roles.role_name == 'super-admin').first()

    group_query = db.session.query(Groups).filter(Groups.group_id == group_id).first()

    if super_role_query in auth_user_query.roles:
        return jsonify({'message': 'group found', 'user': group_schema.dump(group_query)}), 200

    if group_query in auth_user_query.groups:
        return jsonify({'message': 'group found', 'user': group_schema.dump(group_query)}), 200

    else:
        return jsonify({'message': 'unauthorized'}), 401


@authenticate_return_auth
def group_delete_by_id(req, group_id, auth_info):
    super_role_query = db.session.query(Roles).filter(Roles.role_name == 'super-admin').first()
    auth_user_query = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()
    group_query = db.session.query(Groups).filter(Groups.group_id == group_id).first()
    users_query = db.session.query(Users).all()
    group_roles_query = db.session.query(Roles).filter(Roles.group_id == group_id).all()

    group_users_list = []
    for user in users_query:
        if group_query in user.groups:
            group_users_list.append(user)

    if super_role_query in auth_user_query.roles:
        for user in group_users_list:
            for group_role in group_roles_query:
                if group_role in user.roles:
                    user.roles.remove(group_role)

        for role in group_roles_query:
            db.session.delete(role)

        db.session.delete(group_query)
        db.session.commit()

        return jsonify({'message': 'group deleted'}), 200

    else:
        return jsonify({'message': 'unauthorized'}), 401


@authenticate_return_auth
def group_update(req, group_id, auth_info):
    post_data = req.form if req.form else req.json

    auth_user_query = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()
    super_role_query = db.session.query(Roles).filter(Roles.role_name == 'super-admin').first()
    group_query = db.session.query(Groups).filter(Groups.group_id == group_id).first()

    if group_query:
        if super_role_query in auth_user_query.roles:
            populate_object(group_query, post_data)

            db.session.commit()

            return jsonify({'message': 'group updated', 'group': group_schema.dump(group_query)}), 200

        for group in auth_user_query.groups:
            admin_role_query = db.session.query(Roles).filter(Roles.group_id == group.group_id).filter(Roles.role_name == 'admin').first()

            if admin_role_query in auth_user_query.roles:
                populate_object(group_query, post_data)

                db.session.commit()

                return jsonify({'message': 'group updated', 'group': group_schema.dump(group_query)}), 200

            else:
                return jsonify({'message': 'unauthorized'}), 401

    else:
        return jsonify({'message': 'group not found'}), 404


@authenticate_return_auth
def group_add_user(req, group_id, auth_info):
    post_data = req.form if req.form else req.json

    user_ids = post_data.get('users')

    auth_user_query = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()
    super_role_query = db.session.query(Roles).filter(Roles.role_name == 'super-admin').first()
    group_query = db.session.query(Groups).filter(Groups.group_id == group_id).first()

    if group_query:
        admin_role_query = db.session.query(Roles).filter(Roles.group_id == group_id).filter(Roles.role_name == 'admin').first()
        user_role_query = db.session.query(Roles).filter(Roles.group_id == group_id).filter(Roles.role_name == 'user').first()

        if super_role_query in auth_user_query.roles or admin_role_query in auth_user_query.roles:
            for user in user_ids:
                user_query = db.session.query(Users).filter(Users.user_id == user).first()
                if user_query:
                    group_query.users.append(user_query)
                    user_query.roles.append(user_role_query)

                    db.session.commit()

                    return jsonify({'message': 'group updated', 'group': group_schema.dump(group_query)}), 200

                else:
                    return jsonify({'message': 'unauthorized'}), 401

    else:
        return jsonify({'message': 'not found'}), 404


@authenticate_return_auth
def group_remove_user(req, group_id, auth_info):
    post_data = req.form if req.form else req.json

    user_ids = post_data.get('users')

    auth_user_query = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()
    super_role_query = db.session.query(Roles).filter(Roles.role_name == 'super-admin').first()
    group_query = db.session.query(Groups).filter(Groups.group_id == group_id).first()

    if group_query:
        admin_role_query = db.session.query(Roles).filter(Roles.group_id == group_id).filter(Roles.role_name == 'admin').first()
        user_role_query = db.session.query(Roles).filter(Roles.group_id == group_id).filter(Roles.role_name == 'user').first()

        if super_role_query in auth_user_query.roles or admin_role_query in auth_user_query.roles:
            for user in user_ids:
                user_query = db.session.query(Users).filter(Users.user_id == user).first()
                if user_query:
                    user_query.roles.remove(user_role_query)
                    group_query.users.remove(user_query)

                    db.session.commit()

                    return jsonify({'message': 'group updated', 'group': group_schema.dump(group_query)}), 200

                else:
                    return jsonify({'message': 'unauthorized'}), 401

    else:
        return jsonify({'message': 'not found'}), 404


@authenticate_return_auth
def group_activity(req, group_id, auth_info):
    auth_user_query = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()
    group_query = db.session.query(Groups).filter(Groups.group_id == group_id).first()
    super_role_query = db.session.query(Roles).filter(Roles.role_name == 'super-admin').first()

    if super_role_query in auth_user_query.roles:
        group_query.active = not group_query.active

        db.session.commit()

        return jsonify({'message': 'group activity has been updated', 'group': group_schema.dump(group_query)}), 200

    for group in auth_user_query.groups:
        admin_role_query = db.session.query(Roles).filter(Roles.group_id == group.group_id).filter(Roles.role_name == 'admin').first()
        if group in group_query.groups:
            if admin_role_query in auth_user_query.roles:
                group_query.active = not group_query.active

                db.session.commit()

                return jsonify({'message': 'group activity has been updated', 'group': group_schema.dump(group_query)}), 200

            else:
                return jsonify({'message': 'unauthorized'}), 401

    return jsonify({'message': 'group not found'}), 404
