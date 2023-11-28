from flask import request, Blueprint

import controllers


organizations = Blueprint('organizations', __name__)


@organizations.route('/organization', methods=['POST'])
def organization_add():
    return controllers.organization_add(request)


@organizations.route('/organizations', methods=['GET'])
def organizations_get_all():
    return controllers.organizations_get_all(request)


@organizations.route('/organization/<org_id>', methods=['GET'])
def organization_get_by_id(org_id):
    return controllers.organization_get_by_id(request, org_id)


@organizations.route('/organization/delete/<org_id>', methods=['DELETE'])
def organization_delete_by_id(org_id):
    return controllers.organization_delete_by_id(request, org_id)


@organizations.route('/organization/<org_id>', methods=['PUT'])
def organization_update(org_id):
    return controllers.organization_update(request, org_id)


@organizations.route('/organization/user-add/<user_id>', methods=['POST'])
def organization_add_user(user_id):
    return controllers.organization_add_user(request, user_id)


@organizations.route('/organization/user-remove/<user_id>', methods=['DELETE'])
def organization_remove_user(user_id):
    return controllers. organization_remove_user(request, user_id)


@organizations.route('/organization/role-add/<role_id>', methods=['POST'])
def organization_add_role(role_id):
    return controllers.organization_add_role(request, role_id)


@organizations.route('/organization/role-remove/<role_id>', methods=['DELETE'])
def organization_remove_role(role_id):
    return controllers. organization_remove_role(request, role_id)


@organizations.route('/organization/activity/<org_id>', methods=['PATCH'])
def organization_activity(org_id):
    return controllers.organization_activity(request, org_id)
