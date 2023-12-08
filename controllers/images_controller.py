from flask import jsonify, request
from botocore.exceptions import NoCredentialsError
import os
import boto3
import uuid

from db import db
from models.images import Images, image_schema, images_schema
from models.users import Users
from models.quilts import Quilts
from lib.authenticate import authenticate, authenticate_return_auth, get_s3_client, validate_uuid4
from util.reflection import populate_object

key_name = os.getenv('KEY_NAME')


@authenticate_return_auth
@get_s3_client
def image_add(req, s3_client, auth_info):
    post_data = req.form
    uploaded_filenames = []
    quilt_id = post_data.get('quilt_id')
    quilt = uuid.UUID(quilt_id)

    auth_user_query = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()
    quilt_query = db.session.query(Quilts).filter(Quilts.quilt_id == quilt_id).first()

    if auth_info.user_id == auth_user_query.user_id and quilt_query:
        if 'file' in req.files:
            files = req.files.getlist('file')

            if not files[0]:
                return jsonify({'message': 'image not selected'}), 400

            for file in files:
                extra_args = {'ContentType': file.content_type, 'ContentDisposition': 'inline'}

                if file.content_type != 'image/jpeg' and file.content_type != 'image/png':
                    return jsonify({'message': 'incorrect file type'}), 404

                try:
                    new_image = Images.get_new_image()
                    populate_object(new_image, post_data)

                    s3_filename = f'{new_image.image_id}+{file.filename}'

                    new_image.file_name = s3_filename
                    new_image.uploader_id = auth_info.user_id
                    print(new_image.uploader_id)
                    new_image.quilt_id = quilt

                    db.session.add(new_image)
                    db.session.flush()

                    try:
                        db.session.commit()

                    except Exception as error:
                        db.session.rollback()
                        return jsonify({'message': 'database error', 'error': str(error)}), 500

                    s3_client.upload_fileobj(file, key_name, s3_filename, ExtraArgs=extra_args)

                    uploaded_filenames.append(s3_filename)

                except NoCredentialsError:
                    return jsonify({'message': 'no valid files uploaded'}), 400

        return jsonify({'message': 'image uploaded', 'results': images_schema.dump(uploaded_filenames)}), 201

    else:
        return jsonify({'message': 'unauthorized'}), 401
