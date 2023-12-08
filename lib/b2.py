import os
import boto3
from botocore.client import Config
import functools
from flask import Response
from dotenv import load_dotenv, find_dotenv

import config

bucket_name = 'Quilters-Library'


def load_env_variables():
    load_dotenv(find_dotenv('../../env'))

    environ_variables = {
        endpoint: os.getenv('B2_ENDPOINT'),
        key_id: os.getenv('PUBLIC_KEY_ID'),
        application_key: os.getenv('PUBLIC_APP_KEY'),
    }

    return environ_variables


def get_b2_resource(endpoint, key_id, application_key):
    b2 = boto3.resource(service_nbame='s3', endpoint_url=endpoint, aws_access_key_id=key_id, aws_secret_access_key=application_key, config=Config(signature_version='s3v4'))

    return b2


def upload_image_to_b2(b2, bucket_name, file_name, file_path):
    b2.Bucket(bucket_name).upload_file(Filename=file_path, Key=file_name)


def download_image_from_b2(b2, bucket_name, file_name, file_path):
    b2.Bucket(bucket_name).download_file(Key=file_name, Filename=file_path)


# def add_image_to_db(quilt_id, file_name, file_url, uploader_id):
#        new_image = Images(quilt_id, file_name, file_url, uploader_id)
#        db.session.add(new_image)
#        db.session.commit()
# (func):
#     @functools.wraps(func)
#     def get_s3_client_wrapper(*args, **kwargs):

#         key_id = config.s3_private_key_id
#         app_key = config.s3_private_app_key

#         if "type" in kwargs.keys() and kwargs["type"] == "public":
#             key_id = config.s3_public_key_id
#             app_key = config.s3_public_app_key

#         if not key_id or not app_key or not config.s3_region or not config.s3_endpoint:

#             return failure_response()

#         s3_session = boto3.Session(key_id, app_key, region_name=config.s3_region)
#         s3_client = s3_session.client("s3", endpoint_url=config.s3_endpoint)
#         kwargs['s3_client'] = s3_client

#         return func(*args, **kwargs)

#     return get_s3_client_wrapper


# def failure_response():
#     return Response("S3 Credentials Missing Information", 401)


# @get_s3_client
# def s3_upload(file, s3_client, type="public"):
#     key_name = config.s3_public_key_name

#     if type == "private":
#         key_name = config.s3_private_key_name

#     filename = file.filename
#     extra_args = {'ContentType': file.content_type, 'ContentDisposition': 'inline'}

#     s3_client.upload_fileobj(file, key_name, filename, ExtraArgs=extra_args)

#     if type == "public":
#         s3_url = f"https://f005.backblazeb2.com/file/{config.s3_public_bucket}/{filename}"

#     elif type == "private":
#         s3_url = s3_client.generate_presigned_url('get_object', Params={'Bucket': config.s3_private_bucket, 'Key': file.filename}, ExpiresIn=3600)

#     return s3_url
