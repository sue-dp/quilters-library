from flask import request, Blueprint

import controllers


organizations = Blueprint('organizations', __name__)


@organizations.route('/organization', methods=['POST'])
def organization_add():
    return controllers.organization_add(request)


@organizations.route('/organizations', methods=['GET'])
def organizations_get_all():
    return controllers.organizations_get_all(request)


@organizations.route('/organization/<organization_id>', methods=['GET'])
def organization_get_by_id(organization_id):
    print("hi")
    return controllers.organization_get_by_id(request, organization_id)


@organizations.route('/organization/delete/<organization_id>', methods=['DELETE'])
def organization_delete_by_id(organization_id):
    return controllers.organization_delete_by_id(request, organization_id)


@organizations.route('/organization/<organization_id>', methods=['PUT'])
def organization_update(organization_id):
    return controllers.organization_update(request, organization_id)


@organizations.route('/organization/user-add/<organization_id>', methods=['POST'])
def organization_add_user(organization_id):
    return controllers.organization_add_user(request, organization_id)


@organizations.route('/organization/user-remove/<organization_id>', methods=['POST'])
def organization_remove_user(organization_id):
    return controllers. organization_remove_user(request, organization_id)


@organizations.route('/organization/role-add/<organization_id>', methods=['POST'])
def organization_add_role(organization_id):
    return controllers.organization_add_role(request, organization_id)


@organizations.route('/organization/role-remove/<organization_id>', methods=['DELETE'])
def organization_remove_role(organization_id):
    return controllers. organization_remove_role(request, organization_id)


@organizations.route('/organization/activity/<organization_id>', methods=['PATCH'])
def organization_activity(organization_id):
    return controllers.organization_activity(request, organization_id)
