from flask import jsonify

from db import db
from models.users import Users
from models.organizations import Organizations, organization_schema, organizations_schema
from models.roles import Roles
from models.auth_tokens import AuthTokens
from util.reflection import populate_object
from lib.authenticate import authenticate_return_auth, authenticate


@authenticate
def organization_add(req):
    post_data = req.form if req.form else req.json

    new_organization = Organizations.get_new_organization()
    populate_object(new_organization, post_data)

    db.session.add(new_organization)
    db.session.commit()

    return jsonify(organization_schema.dump(new_organization)), 201


@authenticate_return_auth
def organizations_get_all(req, auth_info):
    role_query = db.session.query(Roles).filter(Roles.role_name == 'super-admin').first()
    auth_user_query = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()

    if role_query in auth_user_query.roles:
        organizations_query = db.session.query(Organizations).all()

        return jsonify({'message': 'organizations found', 'organizations': organizations_schema.dump(organizations_query)}), 200

    else:
        return jsonify({'message': 'unauthorized'}), 401


@authenticate_return_auth
def organization_get_by_id(req, organization_id, auth_info):
    auth_user_query = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()
    super_role_query = db.session.query(Roles).filter(Roles.role_name == 'super-admin').first()

    organization_query = db.session.query(Organizations).filter(Organizations.organization_id == organization_id).first()

    if super_role_query in auth_user_query.roles:
        return jsonify({'message': 'organization found', 'user': organization_schema.dump(organization_query)}), 200

    if organization_query in auth_user_query.organizations:
        return jsonify({'message': 'organization found', 'user': organization_schema.dump(organization_query)}), 200

    else:
        return jsonify({'message': 'unauthorized'}), 401


@authenticate_return_auth
def organization_delete_by_id(req, organization_id, auth_info):
    super_role_query = db.session.query(Roles).filter(Roles.role_name == 'super-admin').first()
    auth_user_query = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()
    organization_query = db.session.query(Organizations).filter(Organizations.organization_id == organization_id).first()
    users_query = db.session.query(Users).all()
    organization_roles_query = db.session.query(Roles).filter(Roles.organization_id == organization_id).all()

    organization_users_list = []
    for user in users_query:
        if organization_query in user.organizations:
            organization_users_list.append(user)

    if super_role_query in auth_user_query.roles:
        for user in organization_users_list:
            for organization_role in organization_roles_query:
                if organization_role in user.roles:
                    user.roles.remove(organization_role)

        for role in organization_roles_query:
            db.session.delete(role)

        db.session.delete(organization_query)
        db.session.commit()

        return jsonify({'message': 'organization deleted'}), 200

    else:
        return jsonify({'message': 'unauthorized'}), 401


@authenticate_return_auth
def organization_update(req, organization_id, auth_info):
    post_data = req.form if req.form else req.json

    auth_user_query = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()
    super_role_query = db.session.query(Roles).filter(Roles.role_name == 'super-admin').first()
    organization_query = db.session.query(Organizations).filter(Organizations.organization_id == organization_id).first()

    if organization_query:
        if super_role_query in auth_user_query.roles:
            populate_object(organization_query, post_data)

            db.session.commit()

            return jsonify({'message': 'organization updated', 'organization': organization_schema.dump(organization_query)}), 200

        for organization in auth_user_query.organizations:
            admin_role_query = db.session.query(Roles).filter(Roles.organization_id == organization.organization_id).filter(Roles.role_name == 'admin').first()

            if admin_role_query in auth_user_query.roles:
                populate_object(organization_query, post_data)

                db.session.commit()

                return jsonify({'message': 'organization updated', 'organization': organization_schema.dump(organization_query)}), 200

            else:
                return jsonify({'message': 'unauthorized'}), 401

    else:
        return jsonify({'message': 'organization not found'}), 404


@authenticate_return_auth
def organization_add_user(req, organization_id, auth_info):
    post_data = req.form if req.form else req.json

    user_ids = post_data.get('users')

    auth_user_query = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()
    super_role_query = db.session.query(Roles).filter(Roles.role_name == 'super-admin').first()
    organization_query = db.session.query(Organizations).filter(Organizations.organization_id == organization_id).first()

    if organization_query:
        admin_role_query = db.session.query(Roles).filter(Roles.organization_id == organization_id).filter(Roles.role_name == 'admin').first()
        user_role_query = db.session.query(Roles).filter(Roles.organization_id == organization_id).filter(Roles.role_name == 'user').first()

        if super_role_query in auth_user_query.roles or admin_role_query in auth_user_query.roles:
            for user in user_ids:
                user_query = db.session.query(Users).filter(Users.user_id == user).first()
                if user_query:
                    organization_query.users.append(user_query)
                    user_query.roles.append(user_role_query)

                    db.session.commit()

                    return jsonify({'message': 'organization updated', 'organization': organization_schema.dump(organization_query)}), 200

                else:
                    return jsonify({'message': 'unauthorized'}), 401

    else:
        return jsonify({'message': 'not found'}), 404


@authenticate_return_auth
def organization_remove_user(req, organization_id, auth_info):
    post_data = req.form if req.form else req.json

    user_ids = post_data.get('users')

    auth_user_query = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()
    super_role_query = db.session.query(Roles).filter(Roles.role_name == 'super-admin').first()
    organization_query = db.session.query(Organizations).filter(Organizations.organization_id == organization_id).first()

    if organization_query:
        admin_role_query = db.session.query(Roles).filter(Roles.organization_id == organization_id).filter(Roles.role_name == 'admin').first()
        user_role_query = db.session.query(Roles).filter(Roles.organization_id == organization_id).filter(Roles.role_name == 'user').first()

        if super_role_query in auth_user_query.roles or admin_role_query in auth_user_query.roles:
            for user in user_ids:
                user_query = db.session.query(Users).filter(Users.user_id == user).first()
                if user_query:
                    user_query.roles.remove(user_role_query)
                    organization_query.users.remove(user_query)

                    db.session.commit()

                    return jsonify({'message': 'organization updated', 'organization': organization_schema.dump(organization_query)}), 200

                else:
                    return jsonify({'message': 'unauthorized'}), 401

    else:
        return jsonify({'message': 'not found'}), 404


@authenticate_return_auth
def organization_activity(req, organization_id, auth_info):
    auth_user_query = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()
    organization_query = db.session.query(Organizations).filter(Organizations.organization_id == organization_id).first()
    super_role_query = db.session.query(Roles).filter(Roles.role_name == 'super-admin').first()

    if super_role_query in auth_user_query.roles:
        organization_query.active = not organization_query.active

        db.session.commit()

        return jsonify({'message': 'organization activity has been updated', 'organization': organization_schema.dump(organization_query)}), 200

    for organization in auth_user_query.organizations:
        admin_role_query = db.session.query(Roles).filter(Roles.organization_id == organization.organization_id).filter(Roles.role_name == 'admin').first()
        if organization in organization_query.organizations:
            if admin_role_query in auth_user_query.roles:
                organization_query.active = not organization_query.active

                db.session.commit()

                return jsonify({'message': 'organization activity has been updated', 'organization': organization_schema.dump(organization_query)}), 200

            else:
                return jsonify({'message': 'unauthorized'}), 401

    return jsonify({'message': 'organization not found'}), 404
