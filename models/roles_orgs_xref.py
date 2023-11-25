from db import db


roles_orgs_xref = db.Table(
    'RolesOrgsXref',
    db.Model.metadata,
    db.Column('role_id', db.ForeignKey('Roles.role_id'), primary_key=True),
    db.Column('org_id', db.ForeignKey('Organizations.org_id'), primary_key=True)
)
