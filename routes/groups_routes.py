from flask import request, Blueprint

import controllers


groups = Blueprint('groups', __name__)


@groups.route('/group', methods=['POST'])
def group_add():
    return controllers.group_add(request)


@groups.route('/groups', methods=['GET'])
def groups_get_all():
    return controllers.groups_get_all(request)


@groups.route('/group/<group_id>', methods=['GET'])
def group_get_by_id(group_id):
    return controllers.group_get_by_id(request, group_id)


@groups.route('/group/delete/<group_id>', methods=['DELETE'])
def group_delete_by_id(group_id):
    return controllers.group_delete_by_id(request, group_id)


@groups.route('/group/<group_id>', methods=['PUT'])
def group_update(group_id):
    return controllers.group_update(request, group_id)


@groups.route('/group/user-add/<group_id>', methods=['POST'])
def group_add_user(group_id):
    return controllers.group_add_user(request, group_id)


@groups.route('/group/user-remove/<group_id>', methods=['POST'])
def group_remove_user(group_id):
    return controllers. group_remove_user(request, group_id)


@groups.route('/group/role-add/<group_id>', methods=['POST'])
def group_add_role(group_id):
    return controllers.group_add_role(request, group_id)


@groups.route('/group/role-remove/<group_id>', methods=['DELETE'])
def group_remove_role(group_id):
    return controllers. group_remove_role(request, group_id)


@groups.route('/group/activity/<group_id>', methods=['PATCH'])
def group_activity(group_id):
    return controllers.group_activity(request, group_id)
