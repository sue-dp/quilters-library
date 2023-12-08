from flask import request, Blueprint

import controllers


images = Blueprint('images', __name__)


@images.route('/image', methods=['POST'])
def image_add():
    return controllers.image_add(request)


@images.route('/image/<image_id>', methods=['GET'])
def image_get_by_id(image_id):
    return controllers.image_get_by_id(request, image_id)


@images.route('/images/<quilt_id>', methods=['GET'])
def images_get_by_quilt_id(quilt_id):
    return controllers.image_get_by_quilt_id(request, quilt_id)


@images.route('/image/<image_id>', methods=['DELETE'])
def image_delete_by_id(image_id):
    return controllers.image_delete_by_id(request, image_id)
