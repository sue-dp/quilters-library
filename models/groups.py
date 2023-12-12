import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db
from .users_groups_xref import users_groups_xref


class Groups(db.Model):
    __tablename__ = 'Groups'

    group_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    group_name = db.Column(db.String(), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    users = db.relationship('Users', secondary=users_groups_xref, back_populates='groups')
    roles = db.relationship('Roles', back_populates='group')

    def __init__(self, group_name, active):
        self.group_name = group_name
        self.active = active

    def get_new_group():
        return Groups('', True)


class GroupsSchema(ma.Schema):
    class Meta:
        fields = ['group_id', 'group_name', 'active', 'users', 'roles']

    users = ma.fields.Nested('UsersSchema', many=True, only=['first_name', 'last_name', 'user_id'])
    roles = ma.fields.Nested('RolesSchema', many=True, only=['role_id', 'role_name'])


group_schema = GroupsSchema()
groups_schema = GroupsSchema(many=True)
