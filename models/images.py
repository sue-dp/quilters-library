import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db


class Images(db.Model):
    __tablename__ = 'Images'

    image_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    quilt_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Quilts.quilt_id'), nullable=False)
    file_name = db.Column(db.String(), unique=True, nullable=False)
    uploader = db.Column(UUID(as_uuid=True), db.ForeignKey('Users.user_id'), nullable=False)

    quilt = db.relationship('Quilts', back_populates='images')
    uploader = db.relationship('Users', back_populates='images')

    def __init__(self, quilt_id, file_name, uploader):
        self.quilt_id = quilt_id
        self.file_name = file_name
        self.uploader = uploader

    def get_new_image():
        return Images('', '', '')


class ImagesSchema(ma.Schema):
    class Meta:
        fields = ['image_id', 'quilt', 'file_name', 'uploader']

    quilt = ma.fields.Nested('QuiltsSchema', many=False, exclude=['images'])
    uploader = ma.fields.Nested('UsersSchema', many=False, exclude=['images'])


image_schema = ImagesSchema()
images_schema = ImagesSchema(many=True)
