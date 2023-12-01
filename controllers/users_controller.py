from flask import jsonify

from db import db
from models.users import Users, user_schema, users_schema
from models.groups import Groups
from models.roles import Roles
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth


def user_add(req):
    post_data = req.form if req.form else req.json

    new_user = Users.get_new_user()
    populate_object(new_user, post_data)

    db.session.add(new_user)
    db.session.commit()

    return jsonify(user_schema.dump(new_user)), 201


@authenticate_return_auth
def users_get_all(req, auth_info):
    role_query = db.session.query(Roles).filter(Roles.role_name == 'super-admin').first()
    auth_user_query = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()

    if role_query in auth_user_query.roles:
        users_query = db.session.query(Users).all()

        return jsonify({'message': 'users found', 'users': users_schema.dump(users_query)}), 200

    else:
        return jsonify({'message': 'unauthorized'}), 401


@authenticate_return_auth
def user_get_by_id(req, user_id, auth_info):
    auth_user_query = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()
    user_query = db.session.query(Users).filter(Users.user_id == user_id).first()
    super_role_query = db.session.query(Roles).filter(Roles.role_name == 'super-admin').first()

    if str(auth_info.user.user_id) == user_id:
        return jsonify({'message': 'user found', 'user': user_schema.dump(user_query)}), 200

    if super_role_query in auth_user_query.roles:
        return jsonify({'message': 'user found', 'user': user_schema.dump(user_query)}), 200

    for group in auth_user_query.groups:
        admin_role_query = db.session.query(Roles).filter(Roles.group_id == group.group_id).filter(Roles.role_name == 'admin').first()
        if group in user_query.groups:
            if admin_role_query in auth_user_query.roles:
                return jsonify({'message': 'user found', 'user': user_schema.dump(user_query)}), 200

            else:
                return jsonify({'message': 'unauthorized'}), 401

    return jsonify({'message': 'user not found'}), 404


@authenticate_return_auth
def users_get_by_group_id(req, group_id, auth_info):
    auth_user_query = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()
    group_query = db.session.query(Groups).filter(Groups.group_id == group_id).first()
    users_query = db.session.query(Users).all()
    super_role_query = db.session.query(Roles).filter(Roles.role_name == 'super-admin').first()
    users_list = []

    for user in users_query:
        if group_query in user.groups:
            users_list.append(user)

    if group_query in auth_user_query.groups or super_role_query in auth_user_query.roles:
        return jsonify({'message': 'users found', 'users': users_schema.dump(users_list)}), 200

    else:
        return jsonify({'message': 'unauthorized'}), 401


@authenticate_return_auth
def user_delete_by_id(req, user_id, auth_info):
    auth_user_query = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()
    user_query = db.session.query(Users).filter(Users.user_id == user_id).first()
    super_role_query = db.session.query(Roles).filter(Roles.role_name == 'super-admin').first()

    if str(auth_info.user.user_id) == user_id:
        db.session.delete(user_query)
        db.session.commit()

        return jsonify({'message': 'user deleted'}), 200

    if super_role_query in auth_user_query.roles:
        db.session.delete(user_query)
        db.session.commit()

        return jsonify({'message': 'user deleted'}), 200

    else:
        return jsonify({'message': 'unauthorized'}), 401


@authenticate_return_auth
def user_update(req, user_id, auth_info):
    post_data = req.form if req.form else req.json

    auth_user_query = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()
    user_query = db.session.query(Users).filter(Users.user_id == user_id).first()
    super_role_query = db.session.query(Roles).filter(Roles.role_name == 'super-admin').first()

    if str(auth_info.user.user_id) == user_id:
        populate_object(user_query, post_data)

        db.session.commit()

        return jsonify({'message': 'user updated', 'user': user_schema.dump(user_query)}), 200

    if super_role_query in auth_user_query.roles:
        populate_object(user_query, post_data)

        db.session.commit()

        return jsonify({'message': 'user updated', 'user': user_schema.dump(user_query)}), 200

    for group in auth_user_query.groups:
        admin_role_query = db.session.query(Roles).filter(Roles.group_id == group.group_id).filter(Roles.role_name == 'admin').first()
        if group in user_query.groups:
            if admin_role_query in auth_user_query.roles:
                populate_object(user_query, post_data)
            else:
                return jsonify({'message': 'unauthorized'}), 401

        db.session.commit()

        return jsonify({'message': 'user updated', 'user': user_schema.dump(user_query)}), 200

    else:
        return jsonify({'message': 'user not found'}), 404


@authenticate_return_auth
def user_role_update(req, user_id, auth_info):
    post_data = req.form if req.form else req.json
    role_id = post_data.get("role")

    auth_user_query = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()
    user_query = db.session.query(Users).filter(Users.user_id == user_id).first()
    super_role_query = db.session.query(Roles).filter(Roles.role_name == 'super-admin').first()
    role_query = db.session.query(Roles).filter(Roles.role_id == role_id).first()

    if super_role_query in auth_user_query.roles:
        if role_query not in user_query.roles:
            user_query.roles.append(role_query)
        elif role_query in user_query.roles:
            user_query.roles.remove(role_query)

        db.session.commit()

        return jsonify({'message': 'user roles updated', 'user': user_schema.dump(user_query)}), 200

    for group in auth_user_query.groups:
        admin_role_query = db.session.query(Roles).filter(Roles.group_id == group.group_id).filter(Roles.role_name == 'admin').first()
        if group in user_query.groups:
            if admin_role_query in auth_user_query.roles:
                if role_query not in user_query.roles:
                    user_query.roles.append(role_query)
                elif role_query in user_query.roles:
                    user_query.roles.remove(role_query)

                db.session.commit()

                return jsonify({'message': 'user roles updated', 'user': user_schema.dump(user_query)}), 200

            else:
                return jsonify({'message': 'unauthorized'}), 401

    return jsonify({'message': 'user not found'}), 404


@authenticate_return_auth
def user_activity(req, user_id, auth_info):
    auth_user_query = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()
    user_query = db.session.query(Users).filter(Users.user_id == user_id).first()
    super_role_query = db.session.query(Roles).filter(Roles.role_name == 'super-admin').first()

    if super_role_query in auth_user_query.roles:
        user_query.active = not user_query.active

        db.session.commit()

        return jsonify({'message': 'user activity has been updated', 'user': user_schema.dump(user_query)}), 200

    for group in auth_user_query.groups:
        admin_role_query = db.session.query(Roles).filter(Roles.group_id == group.group_id).filter(Roles.role_name == 'admin').first()
        if group in user_query.groups:
            if admin_role_query in auth_user_query.roles:
                user_query.active = not user_query.active

                db.session.commit()

                return jsonify({'message': 'user activity has been updated', 'user': user_schema.dump(user_query)}), 200

            else:
                return jsonify({'message': 'unauthorized'}), 401

    return jsonify({'message': 'user not found'}), 404
