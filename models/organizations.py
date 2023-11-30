import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db
from .users_orgs_xref import users_orgs_xref


class Organizations(db.Model):
    __tablename__ = 'Organizations'

    org_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    org_name = db.Column(db.String(), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    users = db.relationship('Users', secondary=users_orgs_xref, back_populates='organizations')
    roles = db.relationship('Roles', back_populates='organizations')

    def __init__(self, org_name, active):
        self.org_name = org_name
        self.active = active

    def get_new_organization():
        return Organizations('', True)


class OrganizationsSchema(ma.Schema):
    class Meta:
        fields = ['org_id', 'org_name', 'active', 'users']

    users = ma.fields.Nested('UsersSchema', many=True, only=['first_name', 'last_name', 'user_id'])
    # roles = ma.fields.Nested('RolesSchema', many=True, exclude=['organizations'])


organization_schema = OrganizationsSchema()
organizations_schema = OrganizationsSchema(many=True)
