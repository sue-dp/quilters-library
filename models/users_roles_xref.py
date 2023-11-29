from db import db
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma


users_roles_xref = db.Table(
    'UsersRolesXref',
    db.Model.metadata,
    db.Column('user_id', db.ForeignKey('Users.user_id'), primary_key=True),
    db.Column('role_id', db.ForeignKey('Roles.role_id'), primary_key=True)
)
