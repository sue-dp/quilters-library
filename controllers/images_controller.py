from flask import jsonify
from botocore.exceptions import NoCredentialsError
import os

from db import db
from models.images import Images, image_schema, images_schema
from models.users import Users
from models.quilts import Quilts
from models.roles import Roles
from lib.authenticate import authenticate_return_auth, get_s3_client
from util.reflection import populate_object

key_name = os.getenv('KEY_NAME')


@authenticate_return_auth
@get_s3_client
def image_add(req, s3_client, auth_info):
    post_data = req.form
    uploaded_filenames = []
    quilt_id = post_data.get('quilt_id')
    uploader_id = auth_info.user_id

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
                    new_image = Images.get_new_image(uploader_id)
                    populate_object(new_image, post_data)

                    db.session.add(new_image)
                    db.session.flush()

                    s3_filename = f'{new_image.image_id}+{file.filename}'

                    new_image.file_name = s3_filename

                    try:
                        db.session.commit()

                    except Exception as error:
                        db.session.rollback()
                        return jsonify({'message': 'database error', 'error': str(error)}), 500

                    s3_client.upload_fileobj(file, key_name, s3_filename, ExtraArgs=extra_args)

                    uploaded_filenames.append(s3_filename)

                except NoCredentialsError:
                    return jsonify({'message': 'no valid files uploaded'}), 400

        return jsonify({'message': 'image uploaded', 'results': uploaded_filenames}), 201

    else:
        return jsonify({'message': 'unauthorized'}), 401


@authenticate_return_auth
@get_s3_client
def images_get_from_auth(req, s3_client, auth_info):
    auth_user_query = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()

    if auth_info.user_id == auth_user_query.user_id:
        user_images = db.session.query(Images).filter(Images.uploader_id == auth_user_query.user_id).all()

        all_images = images_schema.dump(user_images)
        for image in all_images:
            image["url"] = s3_client.generate_presigned_url('get_object', Params={'Bucket': os.getenv("KEY_NAME"), 'Key': image["file_name"]})

        return jsonify({'message': 'images found', 'images': all_images}), 200

    else:
        return jsonify({'message': 'unauthorized'}), 401


@authenticate_return_auth
@get_s3_client
def image_get_by_id(req, image_id, s3_client, auth_info):
    auth_user_query = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()
    image_query = db.session.query(Images).filter(Images.image_id == image_id).first()

    if auth_info.user_id == auth_user_query.user_id:
        if image_query:
            image = image_schema.dump(image_query)
            image["url"] = s3_client.generate_presigned_url('get_object', Params={'Bucket': os.getenv("KEY_NAME"), 'Key': image["file_name"]})

            return jsonify({'message': 'image found', 'image': image}), 200

        else:
            return jsonify({'message': 'image not found'}), 404

    else:
        return jsonify({'message': 'unauthorized'}), 401


@authenticate_return_auth
@get_s3_client
def images_get_by_quilt_id(req, quilt_id, s3_client, auth_info):
    auth_user_query = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()
    quilt_query = db.session.query(Quilts).filter(Quilts.quilt_id == quilt_id).first()

    if auth_info.user_id == auth_user_query.user_id:
        if quilt_query:
            quilt_images = db.session.query(Images).filter(Images.quilt_id == quilt_id).all()

            all_images = images_schema.dump(quilt_images)
            for image in all_images:
                image["url"] = s3_client.generate_presigned_url('get_object', Params={'Bucket': os.getenv("KEY_NAME"), 'Key': image["file_name"]})

                return jsonify({'message': 'images found', 'images': all_images}), 200

        else:
            return jsonify({'message': 'quilt not found'}), 400

    else:
        return jsonify({'message': 'unauthorized'}), 401


@authenticate_return_auth
@get_s3_client
def images_get_all(req, s3_client, auth_info):
    auth_user_query = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()
    role_query = db.session.query(Roles).filter(Roles.role_name == 'super-admin').first()

    if auth_info.user_id == auth_user_query.user_id:
        if role_query in auth_user_query.roles:

            quilt_images = db.session.query(Images).all()

            all_images = images_schema.dump(quilt_images)
            for image in all_images:
                image["url"] = s3_client.generate_presigned_url('get_object', Params={'Bucket': os.getenv("KEY_NAME"), 'Key': image["file_name"]})

                return jsonify({'message': 'images found', 'images': all_images}), 200

        else:
            return jsonify({'message': 'images not found'}), 400

    else:
        return jsonify({'message': 'unauthorized'}), 401


@authenticate_return_auth
@get_s3_client
def image_delete_by_id(req, image_id, s3_client, auth_info):
    auth_user_query = db.session.query(Users).filter(Users.user_id == auth_info.user_id).first()
    role_query = db.session.query(Roles).filter(Roles.role_name == 'super-admin').first()
    image_data = db.session.query(Images).filter(Images.image_id == image_id).first()

    if auth_info.user_id == image_data.uploader_id or role_query in auth_user_query.roles:

        if image_data == None:
            return jsonify({'message': 'image not found'}), 404

        s3_client.delete_object(Bucket=key_name, Key=image_data.file_name)

        db.session.delete(image_data)
        db.session.commit()

        return jsonify({'message': 'image deleted'}), 200

    else:
        return jsonify({'message': 'unauthorized'}), 401
