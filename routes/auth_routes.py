from flask import request, Blueprint

import controllers


auth = Blueprint('auth', __name__)


@auth.route('/auth', methods=['POST'])
def auth_token_add():
    return controllers.auth_token_add(request)


@auth.route("/check-login", methods=["GET"])
def auth_check_login():
    return controllers.auth_check_login(request)
