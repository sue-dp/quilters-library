import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db
from .users_organizations_xref import users_organizations_xref


class Organizations(db.Model):
    __tablename__ = 'Organizations'

    organization_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_name = db.Column(db.String(), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    users = db.relationship('Users', secondary=users_organizations_xref, back_populates='organizations')
    roles = db.relationship('Roles', back_populates='organization')

    def __init__(self, organization_name, active):
        self.organization_name = organization_name
        self.active = active

    def get_new_organization():
        return Organizations('', True)


class OrganizationsSchema(ma.Schema):
    class Meta:
        fields = ['organization_id', 'organization_name', 'active', 'users', 'roles']

    users = ma.fields.Nested('UsersSchema', many=True, only=['first_name', 'last_name', 'user_id'])
    roles = ma.fields.Nested('RolesSchema', many=True, only=['role_id', 'role_name'])


organization_schema = OrganizationsSchema()
organizations_schema = OrganizationsSchema(many=True)
