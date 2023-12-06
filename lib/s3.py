import os
import boto3
import functools
from flask import Response

import config


def get_s3_client(func):
    @functools.wraps(func)
    def get_s3_client_wrapper(*args, **kwargs):

        key_id = config.s3_private_key_id
        app_key = config.s3_private_app_key

        if "type" in kwargs.keys() and kwargs["type"] == "public":
            key_id = config.s3_public_key_id
            app_key = config.s3_public_app_key

        if not key_id or not app_key or not config.s3_region or not config.s3_endpoint:

            return failure_response()

        s3_session = boto3.Session(key_id, app_key, region_name=config.s3_region)
        s3_client = s3_session.client("s3", endpoint_url=config.s3_endpoint)
        kwargs['s3_client'] = s3_client

        return func(*args, **kwargs)

    return get_s3_client_wrapper


def failure_response():
    return Response("S3 Credentials Missing Information", 401)


@get_s3_client
def s3_upload(file, s3_client, type="public"):
    key_name = config.s3_public_key_name

    if type == "private":
        key_name = config.s3_private_key_name

    filename = file.filename
    extra_args = {'ContentType': file.content_type, 'ContentDisposition': 'inline'}

    s3_client.upload_fileobj(file, key_name, filename, ExtraArgs=extra_args)

    if type == "public":
        s3_url = f"https://f005.backblazeb2.com/file/{config.s3_public_bucket}/{filename}"

    elif type == "private":
        s3_url = s3_client.generate_presigned_url('get_object', Params={'Bucket': config.s3_private_bucket, 'Key': file.filename}, ExpiresIn=3600)

    return s3_url
