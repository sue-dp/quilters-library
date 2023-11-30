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
from lib.helper_functions import users_org_check


def user_add(req):
    post_data = req.form if req.form else req.json

    new_user = Users.get_new_user()
    populate_object(new_user, post_data)

    db.session.add(new_user)
    db.session.commit()

    return jsonify(user_schema.dump(new_user)), 201


@authenticate_return_auth
def users_get_all(req, auth_info):
    print('test 1')
    users_query = db.session.query(Users).all()
    print("test 2")
    # for user in users_query:
    #     print(user.organizations)
    print("users   ", users_query)
    # if auth_info.user.role == 'admin' or auth_info.user.role == 'super-admin':
    return jsonify({'message': 'users found', 'users': users_schema.dump(users_query)}), 200

    # else:
    #     return jsonify({'message': 'unauthorized'}), 401


@authenticate_return_auth
def user_get_by_id(req, user_id, auth_info):

    user_query = db.session.query(Users).filter(Users.user_id == user_id).first()

    if user_query:
        # if auth_info.user.role == 'admin' or auth_info.user.role == 'super-admin' or user_id == auth_info.user.user_id:
        # make a loop to check for org_id for admin
        return jsonify({'message': 'user found', 'user': user_schema.dump(user_query)}), 200
        print(users_org_check(user_id, auth_info))

        # else:
        #     return jsonify({'message': 'unauthorized'}), 401
    else:
        return jsonify({'message': 'user not found'}), 404


@authenticate_return_auth
def user_delete_by_id(req, user_id, auth_info):
    if auth_info.user.user_id == user_id or auth_info.user.role == 'super-admin':
        user_query = db.session.query(Users).filter(Users.user_id == user_id).first()

        if user_query:
            auth_tokens = db.session.query(AuthTokens).filter(AuthTokens.user_id == user_id).all()
            for token in auth_tokens:
                db.session.delete(token)
            db.session.delete(user_query)
            db.session.commit()

            return jsonify({'message': 'record successfully deleted'}), 200

        return jsonify({'message': 'user not found'}), 404

    else:
        return jsonify({'message': 'unauthorized'}), 401


@authenticate_return_auth
def user_update(req, user_id, auth_info):
    post_data = req.form if req.form else req.json

    user_query = db.session.query(Users).filter(Users.user_id == user_id).first()

    if user_query:
        if auth_info.user.role == 'admin' or auth_info.user.role == 'super-admin' or user_id == auth_info.user.user_id:
            # make a loop to check for org_id
            populate_object(user_query, post_data)

            db.session.commit()

            return jsonify({'message': 'user updated', 'user': user_schema.dump(user_query)}), 200

        else:
            return jsonify({'message': 'unauthorized'}), 401

    else:
        return jsonify({'message': 'user not found'}), 404


@authenticate_return_auth
def user_role_update(req, auth_info):
    post_data = req.form if req.form else req.json
    user_id = auth_info.user.user_id
    # org_id = make loop to get org_id

    user_query = db.session.query(Users).filter(Users.user_id == user_id).first()
    org_query = db.session.query(Organizations).filter(Organizations.org_id == org_id).first()
    role_query = db.session.query(Roles).filter(Roles.role_id == role_id).first()

    if user_query and org_query:
        user_query.organizations.append(org_query)
        db.session.commit()

        return jsonify({'message': 'product added to user', 'user': user_schema.dump(user_query)}), 201

    else:
        return jsonify({'message': 'not found'}), 404


@authenticate_return_auth
def user_activity(req, user_id, auth_info):
    user_query = db.session.query(Users).filter(Users.user_id == user_id).first()

    if user_query:
        if auth_info.user.role == 'admin' or auth_info.user.role == 'super-admin':
            user_query.active = not user_query.active

            db.session.commit()

            return jsonify({'message': 'user activity has been updated', 'user': user_schema.dump(user_query)}), 200

        else:
            return jsonify({'message': 'unauthorized'}), 401

    else:
        return jsonify({'message': 'user not found'}), 404
