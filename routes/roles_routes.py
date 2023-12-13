from flask import request, Blueprint

import controllers


roles = Blueprint('roles', __name__)


@roles.route('/role', methods=['POST'])
def role_add():
    return controllers.role_add(request)


@roles.route('/roles', methods=['GET'])
def roles_get_all():
    return controllers.roles_get_all(request)


@roles.route('/roles/<organization_id>', methods=['GET'])
def roles_get_by_organization_id(organization_id):
    return controllers.roles_get_by_organization_id(request, organization_id)


@roles.route('/role/<role_id>', methods=['GET'])
def role_get_by_id(role_id):
    return controllers.role_get_by_id(request, role_id)


@roles.route('/role/delete/<role_id>', methods=['DELETE'])
def role_delete_by_id(role_id):
    return controllers.role_delete_by_id(request, role_id)


@roles.route('/role/<role_id>', methods=['PUT'])
def role_update(role_id):
    return controllers.role_update(request, role_id)


@roles.route('/role/activity/<role_id>', methods=['PATCH'])
def role_activity(role_id):
    return controllers.role_activity(request, role_id)
