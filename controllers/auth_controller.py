from flask import jsonify
from flask_bcrypt import check_password_hash
from datetime import datetime, timedelta

from db import db
from models.auth_tokens import AuthTokens, auth_token_schema
from models.users import Users, user_schema
from lib.authenticate import authenticate_return_auth


def auth_token_add(req):
    post_data = req.form if req.form else req.json

    post_data = {
        "email": post_data[0],
        "password": post_data[1]
    }

    fields = ['email', 'password']
    req_fields = ['email', 'password']

    values = {}

    for field in fields:
        print('field: ', post_data)
        field_data = post_data.get(field)
        values[field] = field_data

        if field in req_fields and not values[field]:
            return jsonify(f'{field} is required'), 400

    user_data = db.session.query(Users).filter(Users.email == values['email']).first()

    if not user_data:
        return jsonify({'message': 'Invalid Login'}), 401

    valid_password = check_password_hash(user_data.password, values['password'])

    if not valid_password:
        return jsonify({'message': 'Invalid Login'}), 401

    existing_tokens = db.session.query(AuthTokens).filter(AuthTokens.user_id == user_data.user_id).all()

    if existing_tokens:
        for token in existing_tokens:
            if token.expiration < datetime.utcnow():
                db.session.delete(token)

    expiry = datetime.now() + timedelta(hours=12)

    new_token = AuthTokens(user_data.user_id, expiry)

    db.session.add(new_token)
    db.session.commit()
    print("new_token: ", new_token.auth_token)

    return jsonify({'message': 'success', 'auth_info': auth_token_schema.dump(new_token)}), 201


@authenticate_return_auth
def auth_check_login(req, auth_info):
    user_data = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()
    print(user_data)

    return jsonify({"message": "success", "results": {"auth_info": auth_token_schema.dump(auth_info), "user_info": user_schema.dump(user_data)}}), 200
