from flask import request, Blueprint

import controllers


images = Blueprint('images', __name__)


@images.route('/image/<quilt_id>', methods=['POST'])
def image_add(quilt_id):
    return controllers.image_add(request, quilt_id)


@images.route('/images', methods=['GET'])
def images_get_all():
    return controllers.images_get_all(request)


@images.route('/image/<image_id>', methods=['GET'])
def image_get_by_id(image_id):
    return controllers.image_get_by_id(request, image_id)


@images.route('/images/<quilt_id>', methods=['GET'])
def images_get_by_quilt_id(quilt_id):
    return controllers.image_get_by_quilt_id(request, quilt_id)


@images.route('/image/<image_id>', methods=['DELETE'])
def image_delete_by_id(image_id):
    return controllers.image_delete_by_id(request, image_id)


@images.route('/image/<image_id>', methods=['PUT'])
def image_update(image_id):
    return controllers.image_update(request, image_id)


@images.route('/image/activity/<image_id>', methods=['PATCH'])
def image_activity(image_id):
    return controllers.image_activity(request, image_id)
