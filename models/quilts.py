import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db


class Quilts(db.Model):
    __tablename__ = 'Quilts'

    quilt_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Users.user_id'), nullable=False)
    pattern_name = db.Column(db.String(), nullable=False)
    pattern_designer = db.Column(db.String())
    pattern_url = db.Column(db.String())
    fabric_line = db.Column(db.String())
    quilting_type = db.Column(db.String())
    long_arm_quilter = db.Column(db.String())
    long_arm_quilter_url = db.Column(db.String())
    notes = db.Column(db.String())
    public = db.Column(db.Boolean(), nullable=False, default=True)
    active = db.Column(db.Boolean(), nullable=False, default=True)

    images = db.relationship('Images', back_populates='quilt')
    user = db.relationship('Users', back_populates='quilts')

    def __init__(self, user_id, pattern_name, public=True, active=True):
        self.user_id = user_id
        self.pattern_name = pattern_name
        self.public = public
        self.active = active

    def get_new_quilt():
        return Quilts('', '', True, True)


class QuiltsSchema(ma.Schema):
    class Meta:
        fields = ['quilt_id', 'user', 'pattern_name', 'pattern_designer', 'pattern_url', 'fabric_line', 'quilting_type', 'long_arm_quilter', 'long_arm_quilter_url', 'notes', 'public', 'active', 'images']

    user = ma.fields.Nested('UsersSchema', many=False, exclude='quilts')
    images = ma.fields.Nested('ImagesSchema', many=True, exclude='quilt')


quilt_schema = QuiltsSchema()
quilts_schema = QuiltsSchema(many=True)
