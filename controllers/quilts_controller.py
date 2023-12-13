from flask import jsonify

from db import db
from models.quilts import Quilts, quilt_schema, quilts_schema
from models.users import Users
from models.organizations import Organizations
from models.roles import Roles
from models.auth_tokens import AuthTokens
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth, authenticate


@authenticate_return_auth
def quilt_add(req, auth_info):
    post_data = req.form if req.form else req.json

    user_id = auth_info.user.user_id

    new_quilt = Quilts.get_new_quilt(user_id)
    populate_object(new_quilt, post_data)

    db.session.add(new_quilt)
    db.session.commit()

    return jsonify({'message': 'quilt added', 'quilt': quilt_schema.dump(new_quilt)}), 201


@authenticate_return_auth
def quilts_get_all(req, auth_info):
    role_query = db.session.query(Roles).filter(Roles.role_name == 'super-admin').first()
    auth_user_query = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()

    if role_query in auth_user_query.roles:
        quilts_query = db.session.query(Quilts).all()

        return jsonify({'message': 'quilts found', 'quilts': quilts_schema.dump(quilts_query)}), 200

    else:
        return jsonify({'message': 'unauthorized'}), 401


@authenticate_return_auth
def quilt_get_by_id(req, quilt_id, auth_info):
    auth_user_query = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()
    super_role_query = db.session.query(Roles).filter(Roles.role_name == 'super-admin').first()
    organization_query = db.session.query(Organizations).all()

    quilt_query = db.session.query(Quilts).filter(Quilts.quilt_id == quilt_id).first()

    if str(auth_info.user.user_id) == Quilts.user_id:
        return jsonify({'message': 'quilt found', 'quilt': quilt_schema.dump(quilt_query)}), 200

    if super_role_query in auth_user_query.roles:
        return jsonify({'message': 'quilt found', 'quilt': quilt_schema.dump(quilt_query)}), 200

    if organization_query in auth_user_query.organizations:
        admin_role_query = db.session.query(Roles).filter(Roles.organization_id == Users.organization_id).filter(Roles.role_name == 'admin').first()
        if admin_role_query:
            return jsonify({'message': 'quilt found', 'quilt': quilt_schema.dump(quilt_query)}), 200

    else:
        return jsonify({'message': 'unauthorized'}), 401


@authenticate_return_auth
def quilts_get_by_user(req, user_id, auth_info):
    auth_user_query = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()
    super_role_query = db.session.query(Roles).filter(Roles.role_name == 'super-admin').first()
    organization_query = db.session.query(Organizations).all()

    quilts_query = db.session.query(Quilts).filter(Quilts.user_id == user_id).all()

    if str(auth_info.user.user_id) == user_id:
        return jsonify({'message': 'quilts found', 'quilts': quilts_schema.dump(quilts_query)}), 200

    if super_role_query in auth_user_query.roles:
        return jsonify({'message': 'quilts found', 'quilts': quilts_schema.dump(quilts_query)}), 200

    for organization in organization_query:
        if organization in auth_user_query.organizations:
            admin_role_query = db.session.query(Roles).filter(Roles.organization_id == Users.organization_id).filter(Roles.role_name == 'admin').first()
            if admin_role_query:
                return jsonify({'message': 'quilts found', 'quilts': quilts_schema.dump(quilts_query)}), 200

        else:
            return jsonify({'message': 'unauthorized'}), 401


@authenticate_return_auth
def quilt_delete_by_id(req, quilt_id, auth_info):
    super_role_query = db.session.query(Roles).filter(Roles.role_name == 'super-admin').first()
    auth_user_query = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()

    quilt_query = db.session.query(Quilts).filter(Quilts.quilt_id == quilt_id).first()

    if str(auth_info.user.user_id) == Quilts.user_id:

        db.session.delete(quilt_query)
        db.session.commit()

        return jsonify({'message': 'quilt deleted'}), 200

    if super_role_query in auth_user_query.roles:

        db.session.delete(quilt_query)
        db.session.commit()

        return jsonify({'message': 'quilt deleted'}), 200

    else:
        return jsonify({'message': 'unauthorized'}), 401


@authenticate_return_auth
def quilt_update(req, quilt_id, auth_info):
    post_data = req.form if req.form else req.json

    auth_user_query = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()
    super_role_query = db.session.query(Roles).filter(Roles.role_name == 'super-admin').first()
    quilt_query = db.session.query(Quilts).filter(Quilts.quilt_id == quilt_id).first()

    if quilt_query:
        if super_role_query in auth_user_query.roles or str(auth_info.user.user_id) == Quilts.user_id:
            populate_object(quilt_query, post_data)

            db.session.commit()

            return jsonify({'message': 'quilt updated', 'quilt': quilt_schema.dump(quilt_query)}), 200

        else:
            return jsonify({'message': 'unauthorized'}), 401

    else:
        return jsonify({'message': 'quilt not found'}), 404


@authenticate_return_auth
def quilt_public(req, quilt_id, auth_info):
    auth_user_query = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()
    quilt_query = db.session.query(Quilts).filter(Quilts.quilt_id == quilt_id).first()
    super_role_query = db.session.query(Roles).filter(Roles.role_name == 'super-admin').first()

    if quilt_query:
        if super_role_query in auth_user_query.roles or str(auth_info.user.user_id) == Quilts.user_id:
            quilt_query.public = not quilt_query.public

            db.session.commit()

            return jsonify({'message': 'quilt publicity has been updated', 'quilt': quilt_schema.dump(quilt_query)}), 200

        else:
            return jsonify({'message': 'unauthorized'}), 401

    return jsonify({'message': 'quilt not found'}), 404
