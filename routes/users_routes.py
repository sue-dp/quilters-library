from flask import request, Blueprint

import controllers


users = Blueprint('users', __name__)


@users.route('/user', methods=['POST'])
def user_add():
    return controllers.user_add(request)


@users.route('/users', methods=['GET'])
def users_get_all():
    return controllers.users_get_all(request)


@users.route('/user/<user_id>', methods=['GET'])
def user_get_by_id(user_id):
    return controllers.user_get_by_id(request, user_id)


@users.route('/users/<org_id>', methods=['GET'])
def users_get_by_org__id(org_id):
    return controllers.user_get_by_org_id(request, org_id)


@users.route('/user/delete/<user_id>', methods={'DELETE'})
def user_delete_by_id(user_id):
    return controllers.user_delete_by_id(request, user_id)


@users.route('/user/<user_id>', methods=['PUT'])
def user_update(user_id):
    return controllers.user_update(request, user_id)


@users.route('/user/role/<org_id>/<role_id>', methods=['PATCH'])
def user_role_update(org_id, role_id):
    return controllers.user_role_update(request, org_id, role_id)


@users.route('/user/activity/<user_id>', methods=['PATCH'])
def user_activity(user_id):
    return controllers.user_activity(request, user_id)
