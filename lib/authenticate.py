import os
import functools
from flask import Response
from datetime import datetime
from uuid import UUID
import boto3

from db import db
from models.auth_tokens import AuthTokens

key_id = os.getenv("PUBLIC_KEY_ID")
app_key = os.getenv("PUBLIC_APP_KEY")
s3_region = os.getenv("S3_REGION")
s3_endpoint = os.getenv("S3_ENDPOINT")


def validate_uuid4(uuid_string):
    try:
        UUID(uuid_string, version=4)

        return True
    except:

        return False


def validate_token(args):
    auth_token = args.headers['auth']

    if not auth_token or not validate_uuid4(auth_token):

        return False

    try:
        auth_record = db.session.query(AuthTokens).filter(AuthTokens.auth_token == auth_token).filter(AuthTokens.expiration > datetime.utcnow()).first()
        return auth_record

    except:
        return False


def fail_response():
    return Response('authentication required', 401)


def authenticate(func):
    @functools.wraps(func)
    def wrapper_auth_return(*args, **kwargs):
        auth_info = validate_token(args[0])

        if auth_info:
            return func(*args, **kwargs)
        else:
            return fail_response()
    return wrapper_auth_return


def authenticate_return_auth(func):
    @functools.wraps(func)
    def wrapper_auth_return(*args, **kwargs):
        auth_info = validate_token(args[0])
        kwargs['auth_info'] = auth_info

        if auth_info:
            return func(*args, **kwargs)
        else:
            return fail_response()
    return wrapper_auth_return


def get_s3_client(func):
    @functools.wraps(func)
    def get_s3_client_wrapper(*args, **kwargs):
        if not key_id or not app_key or not s3_region or not s3_endpoint:
            return Response("S3 Credentials Missing Information", 401)

        s3_session = boto3.Session(key_id, app_key, region_name=s3_region)
        s3_client = s3_session.client("s3", endpoint_url=s3_endpoint)

        kwargs['s3_client'] = s3_client
        return func(*args, **kwargs)
    return get_s3_client_wrapper
