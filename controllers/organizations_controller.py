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


def organization_add(req):
    post_data = req.form if req.form else req.json

    new_organization = Organizations.get_new_organization()
    populate_object(new_organization, post_data)

    db.session.add(new_organization)
    db.session.commit()

    return jsonify(organization_schema.dump(new_organization)), 201


@authenticate_return_auth
def organizations_get_all(req, auth_info):
    organizations_query = db.session.query(Organizations).all()

    if auth_info.user.role == 'super-admin':
        return jsonify({'message': 'organizations found', 'organizations': organizations_schema.dump(organizations_query)}), 200
    else:
        return jsonify({'message': 'unauthorized'}), 401


@authenticate_return_auth
def organization_get_by_id(req, organization_id, auth_info):
    organization_query = db.session.query(Organizations).filter(Organizations.organization_id == organization_id).first()

    if organization_query:
        if auth_info.user.role == 'admin' or auth_info.user.role == 'super-admin' or organization_id == auth_info.organization.organization_id:
            # make a loop to check for org_id for admin
            return jsonify({'message': 'organization found', 'organization': organization_schema.dump(organization_query)}), 200

        else:
            return jsonify({'message': 'unauthorized'}), 401
    else:
        return jsonify({'message': 'organization not found'}), 404


@authenticate_return_auth
def organization_delete_by_id(req, organization_id, auth_info):
    if auth_info.user.role == 'admin' or auth_info.user.role == 'super-admin':
        organization_query = db.session.query(Organizations).filter(Organizations.organization_id == organization_id).first()

        if organization_query:
            auth_tokens = db.session.query(AuthTokens).filter(AuthTokens.organization_id == organization_id).all()
            for token in auth_tokens:
                db.session.delete(token)
            db.session.delete(organization_query)
            db.session.commit()

            return jsonify({'message': 'record successfully deleted'}), 200

        return jsonify({'message': 'organization not found'}), 404

    else:
        return jsonify({'message': 'unauthorized'}), 401


@authenticate_return_auth
def organization_update(req, organization_id, auth_info):
    post_data = req.form if req.form else req.json

    organization_query = db.session.query(Organizations).filter(Organizations.organization_id == organization_id).first()

    if organization_query:
        if auth_info.user.role == 'admin' or auth_info.user.role == 'super-admin':
            # make a loop to check for org_id
            populate_object(organization_query, post_data)

            db.session.commit()

            return jsonify({'message': 'organization updated', 'organization': organization_schema.dump(organization_query)}), 200

        else:
            return jsonify({'message': 'unauthorized'}), 401

    else:
        return jsonify({'message': 'organization not found'}), 404


@authenticate_return_auth
def organization_add_user(req, auth_info):
    post_data = req.form if req.form else req.json
    organization_id = auth_info.organization.organization_id
    # org_id = make loop to get org_id

    organization_query = db.session.query(Organizations).filter(Organizations.organization_id == organization_id).first()
    org_query = db.session.query(Organizations).filter(Organizations.org_id == org_id).first()
    role_query = db.session.query(Roles).filter(Roles.role_id == role_id).first()

    if organization_query and org_query:
        if auth_info.user.role == 'admin' or auth_info.user.role == 'super-admin':
            organization_query.organizations.append(org_query)
            db.session.commit()

            return jsonify({'message': 'product added to organization', 'organization': organization_schema.dump(organization_query)}), 201

        else:
            return jsonify({'message': 'unauthorized'}), 401

    else:
        return jsonify({'message': 'not found'}), 404


@authenticate_return_auth
def organization_remove_user(req, auth_info):
    post_data = req.form if req.form else req.json
    organization_id = auth_info.organization.organization_id
    # org_id = make loop to get org_id

    organization_query = db.session.query(Organizations).filter(Organizations.organization_id == organization_id).first()
    org_query = db.session.query(Organizations).filter(Organizations.org_id == org_id).first()
    role_query = db.session.query(Roles).filter(Roles.role_id == role_id).first()

    if organization_query and org_query:
        if auth_info.user.role == 'admin' or auth_info.user.role == 'super-admin':
            organization_query.organizations.append(org_query)
            db.session.commit()

            return jsonify({'message': 'product added to organization', 'organization': organization_schema.dump(organization_query)}), 201

        else:
            return jsonify({'message': 'unauthorized'}), 401

    else:
        return jsonify({'message': 'not found'}), 404


@authenticate_return_auth
def organization_add_role(req, auth_info):
    post_data = req.form if req.form else req.json
    organization_id = auth_info.organization.organization_id
    # org_id = make loop to get org_id

    organization_query = db.session.query(Organizations).filter(Organizations.organization_id == organization_id).first()
    org_query = db.session.query(Organizations).filter(Organizations.org_id == org_id).first()
    role_query = db.session.query(Roles).filter(Roles.role_id == role_id).first()

    if organization_query and org_query:
        if auth_info.user.role == 'admin' or auth_info.user.role == 'super-admin':
            organization_query.organizations.append(org_query)
            db.session.commit()

            return jsonify({'message': 'product added to organization', 'organization': organization_schema.dump(organization_query)}), 201

        else:
            return jsonify({'message': 'unauthorized'}), 401

    else:
        return jsonify({'message': 'not found'}), 404


@authenticate_return_auth
def organization_remove_role(req, auth_info):
    post_data = req.form if req.form else req.json
    organization_id = auth_info.organization.organization_id
    # org_id = make loop to get org_id

    organization_query = db.session.query(Organizations).filter(Organizations.organization_id == organization_id).first()
    org_query = db.session.query(Organizations).filter(Organizations.org_id == org_id).first()
    role_query = db.session.query(Roles).filter(Roles.role_id == role_id).first()

    if organization_query and org_query:
        if auth_info.user.role == 'admin' or auth_info.user.role == 'super-admin':
            organization_query.organizations.append(org_query)
            db.session.commit()

            return jsonify({'message': 'product added to organization', 'organization': organization_schema.dump(organization_query)}), 201

        else:
            return jsonify({'message': 'unauthorized'}), 401

    else:
        return jsonify({'message': 'not found'}), 404


@authenticate_return_auth
def organization_activity(req, organization_id, auth_info):
    organization_query = db.session.query(Organizations).filter(Organizations.organization_id == organization_id).first()

    if organization_query:
        if auth_info.user.role == 'admin' or auth_info.user.role == 'super-admin':
            organization_query.active = not organization_query.active

            db.session.commit()

            return jsonify({'message': 'organization activity has been updated', 'organization': organization_schema.dump(organization_query)}), 200

        else:
            return jsonify({'message': 'unauthorized'}), 401

    else:
        return jsonify({'message': 'organization not found'}), 404
